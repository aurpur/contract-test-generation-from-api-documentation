"""
===============================================================================
RQ1 Oracle Validation Experiment Runner
===============================================================================

OBJECTIF:
    Ce module orchestre les expériences pour valider la Question de Recherche 1:
    "Quelle est la précision et la complétude des oracles générés automatiquement?"

FONCTIONNEMENT:
    1. Charge les oracles de référence (ground truth) créés manuellement
    2. Exécute la génération d'oracles avec de VRAIS agents OracleAgent
    3. Compare les oracles générés aux oracles de référence
    4. Calcule les métriques de précision, rappel, F1-score et complétude
    5. Génère des rapports détaillés et des visualisations

MODÈLES LLM:
    Ce module utilise UNIQUEMENT des modèles Ollama locaux :
    - deepseek_r1       : Raisonnement avancé (deepseek-r1:8b)
    - deepseek_coder    : Spécialisé code (deepseek-coder-v2)
    - codellama_7b      : Meta CodeLlama 7B
    - qwen25_7b         : Qwen 2.5 généraliste
    - qwen25_coder_7b   : Qwen 2.5 code
    - llama31, llama32  : Meta Llama
    - mistral           : Mistral 7B

IMPORTANT:
    - PAS de simulation ou de mock - utilise les vrais agents
    - PAS de modèles cloud (OpenAI, Anthropic, Google)
    - Les modèles Ollama doivent être installés localement

Auteur: Aurel IKAMA HONEY
Date: December 11, 2025
===============================================================================
"""
import asyncio
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from uuid import UUID, uuid4
import statistics

# Ajouter la racine du projet au path Python
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Imports des composants internes du projet
from src.agents.base_agent import AgentConfig
from src.agents.oracle import OracleAgent
from src.orchestration import EventBus, InMemoryTaskQueue, MessageRouter, Task
from src.shared_context import AgentType
from src.shared_context.context_manager import ContextManager
from src.shared_context.models import EndpointContext, Oracle, HTTPMethod
from src.shared_context.storage import InMemoryStorage
from src.utils.config import load_config
from src.utils.logging import logger
from src.validation.oracle_metrics import (
    OracleMetricsCalculator,
    GroundTruth,
    OraclePrecisionMetrics
)


# ==============================================================================
# CONSTANTES ET CONFIGURATION
# ==============================================================================

# Répertoire des variantes de datasets pour les expériences
VARIANTS_DIR = Path("experiments/datasets/variants")

# Modèles Ollama disponibles pour les expériences RQ1
AVAILABLE_MODELS = [
    "deepseek_r1",      # Raisonnement avancé
    "deepseek_coder",   # Code spécialisé
    "codellama_7b",     # CodeLlama
    "qwen25_7b",        # Qwen généraliste
    "qwen25_coder_7b",  # Qwen code
    "llama31",          # Llama 3.1
    "llama32",          # Llama 3.2
    "mistral",          # Mistral 7B
]


# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================

def _load_json(path: Path) -> Dict[str, Any]:
    """Load JSON file."""
    if not path.exists():
        raise FileNotFoundError(str(path))
    with open(path, "r") as f:
        return json.load(f)


def _variant_dir(dataset_name: str, completeness: float) -> Path:
    """Get variant directory path."""
    percent = int(round(completeness * 100))
    return VARIANTS_DIR / dataset_name / f"completeness_{percent}"


def load_variant(dataset_name: str, completeness: float) -> Tuple[List[EndpointContext], Dict[UUID, GroundTruth]]:
    """Load endpoints and ground truths from a dataset variant."""
    variant_dir = _variant_dir(dataset_name, completeness)
    endpoints_path = variant_dir / "endpoints.json"
    ground_truth_path = variant_dir / "ground_truth.json"

    endpoints_data = _load_json(endpoints_path)
    gt_data = _load_json(ground_truth_path)

    endpoints: List[EndpointContext] = []
    for item in endpoints_data.get("endpoints", []):
        endpoints.append(
            EndpointContext(
                id=UUID(item["id"]),
                name=item["name"],
                method=HTTPMethod(item["method"]),
                url=item["url"],
                description=item.get("description"),
                documentation_completeness=float(item.get("documentation_completeness", completeness)),
            )
        )

    ground_truths: Dict[UUID, GroundTruth] = {}
    for item in gt_data.get("ground_truths", []):
        gt = GroundTruth(
            endpoint_id=UUID(item["endpoint_id"]),
            status_code=int(item["status_code"]),
            required_headers=dict(item.get("required_headers", {})),
            optional_headers=dict(item.get("optional_headers", {})),
            response_schema=dict(item.get("response_schema", {})),
            business_rules=list(item.get("business_rules", [])),
            source=str(item.get("source", "unknown")),
            confidence=float(item.get("confidence", 0.0)),
            annotator=item.get("annotator"),
            created_at=datetime.fromisoformat(item["created_at"]) if item.get("created_at") else None,
        )
        ground_truths[gt.endpoint_id] = gt

    if not endpoints:
        raise ValueError(f"No endpoints loaded from {endpoints_path}")

    return endpoints, ground_truths


def _ensure_models_available(config, model_names: List[str]) -> Dict[str, Dict[str, Any]]:
    """Ensure requested LLM models are available in config."""
    missing = [m for m in model_names if m not in config.llm_models]
    if missing:
        raise ValueError(
            "Requested models are not available (check config/llm_config.yaml): "
            + ", ".join(missing)
        )

    resolved: Dict[str, Dict[str, Any]] = {}
    for name in model_names:
        model_cfg = config.llm_models[name]
        resolved[name] = model_cfg.model_dump() if hasattr(model_cfg, "model_dump") else dict(model_cfg)
    return resolved


@dataclass
class ExperimentConfig:
    """Configuration for RQ1 validation experiments."""
    experiment_id: str
    name: str
    description: str
    llm_models: List[str]  # e.g., ["gpt-4", "claude-3-opus", "gemini-pro"]
    num_endpoints: int
    include_real_api_calls: bool = False
    max_retries: int = 2
    timeout_seconds: int = 30
    output_dir: Path = Path("experiments/results")
    
    def __post_init__(self):
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class EndpointExperimentResult:
    """Results for a single endpoint in RQ1 experiment."""
    endpoint_id: UUID
    endpoint_name: str
    ground_truth: GroundTruth
    generated_oracles: Dict[str, Oracle] = field(default_factory=dict)  # llm_model -> Oracle
    metrics: Dict[str, OraclePrecisionMetrics] = field(default_factory=dict)  # llm_model -> metrics
    errors: Dict[str, str] = field(default_factory=dict)  # llm_model -> error message
    execution_times: Dict[str, float] = field(default_factory=dict)  # llm_model -> seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "endpoint_id": str(self.endpoint_id),
            "endpoint_name": self.endpoint_name,
            "ground_truth": {
                "endpoint_id": str(self.ground_truth.endpoint_id),
                "status_code": self.ground_truth.status_code,
                "required_headers": self.ground_truth.required_headers,
                "optional_headers": self.ground_truth.optional_headers,
                "response_schema": self.ground_truth.response_schema,
                "business_rules": self.ground_truth.business_rules,
                "source": self.ground_truth.source,
                "confidence": self.ground_truth.confidence
            },
            "generated_oracles": {
                model: {
                    "oracle_id": str(oracle.id),
                    "name": oracle.name,
                    "status_code": oracle.status_code,
                    "required_headers": oracle.required_headers,
                    "response_schema": oracle.response_schema,
                    "confidence": oracle.confidence
                }
                for model, oracle in self.generated_oracles.items()
            },
            "metrics": {
                model: {
                    "precision": m.precision,
                    "recall": m.recall,
                    "f1_score": m.f1_score,
                    "completeness_score": m.completeness_score,
                    "true_positives": m.true_positives,
                    "false_positives": m.false_positives,
                    "false_negatives": m.false_negatives
                }
                for model, m in self.metrics.items()
            },
            "errors": self.errors,
            "execution_times": self.execution_times
        }


@dataclass
class ExperimentReport:
    """Aggregate report for entire RQ1 experiment."""
    experiment_id: str
    config: ExperimentConfig
    started_at: datetime
    completed_at: Optional[datetime] = None
    endpoint_results: List[EndpointExperimentResult] = field(default_factory=list)
    
    # Aggregate metrics per LLM
    aggregate_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Rankings
    llm_rankings: Dict[str, int] = field(default_factory=dict)  # model -> rank (1-based)
    
    # Statistics
    total_endpoints: int = 0
    successful_generations: Dict[str, int] = field(default_factory=dict)  # model -> count
    failed_generations: Dict[str, int] = field(default_factory=dict)  # model -> count
    
    def calculate_aggregates(self):
        """Calculate aggregate metrics across all endpoints."""
        for model in self.config.llm_models:
            model_metrics = [
                result.metrics[model]
                for result in self.endpoint_results
                if model in result.metrics
            ]
            
            if not model_metrics:
                continue
            
            self.aggregate_metrics[model] = {
                "precision_mean": statistics.mean(m.precision for m in model_metrics),
                "precision_std": statistics.stdev(m.precision for m in model_metrics) if len(model_metrics) > 1 else 0.0,
                "recall_mean": statistics.mean(m.recall for m in model_metrics),
                "recall_std": statistics.stdev(m.recall for m in model_metrics) if len(model_metrics) > 1 else 0.0,
                "f1_mean": statistics.mean(m.f1_score for m in model_metrics),
                "f1_std": statistics.stdev(m.f1_score for m in model_metrics) if len(model_metrics) > 1 else 0.0,
                "completeness_mean": statistics.mean(m.completeness_score for m in model_metrics),
                "completeness_std": statistics.stdev(m.completeness_score for m in model_metrics) if len(model_metrics) > 1 else 0.0,
            }
            
            self.successful_generations[model] = len(model_metrics)
            self.failed_generations[model] = self.total_endpoints - len(model_metrics)
        
        # Rank models by F1 score
        if self.aggregate_metrics:
            sorted_models = sorted(
                self.aggregate_metrics.items(),
                key=lambda x: x[1]["f1_mean"],
                reverse=True
            )
            for rank, (model, _) in enumerate(sorted_models, 1):
                self.llm_rankings[model] = rank
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "experiment_id": self.experiment_id,
            "config": {
                "experiment_id": self.config.experiment_id,
                "name": self.config.name,
                "description": self.config.description,
                "llm_models": self.config.llm_models,
                "num_endpoints": self.config.num_endpoints,
                "include_real_api_calls": self.config.include_real_api_calls
            },
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_endpoints": self.total_endpoints,
            "endpoint_results": [r.to_dict() for r in self.endpoint_results],
            "aggregate_metrics": self.aggregate_metrics,
            "llm_rankings": self.llm_rankings,
            "successful_generations": self.successful_generations,
            "failed_generations": self.failed_generations
        }
    
    def save(self, output_path: Optional[Path] = None):
        """Save report to JSON file."""
        if output_path is None:
            output_path = self.config.output_dir / f"rq1_report_{self.experiment_id}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return output_path


class RQ1ExperimentRunner:
    """
    Orchestrates RQ1 validation experiments using REAL OracleAgent.
    
    Runs experiments to measure oracle generation precision and completeness
    across different LLM models using the actual agent infrastructure.
    """
    
    def __init__(self, config: ExperimentConfig, llm_configs: Dict[str, Dict[str, Any]]):
        """
        Initialize RQ1 experiment runner.
        
        Args:
            config: Experiment configuration
            llm_configs: Dictionary mapping model names to their LLM configurations
        """
        self.config = config
        self.llm_configs = llm_configs
        self.calculator = OracleMetricsCalculator()
    
    async def _create_oracle_agent(
        self, 
        model_name: str, 
        context_manager: ContextManager
    ) -> OracleAgent:
        """Create a real OracleAgent for a specific LLM model."""
        router = MessageRouter()
        event_bus = EventBus()
        task_queue = InMemoryTaskQueue()
        
        llm_config = self.llm_configs.get(model_name)
        if not llm_config:
            raise ValueError(f"No LLM config found for model: {model_name}")
        
        agent = OracleAgent(
            config=AgentConfig(agent_type=AgentType.ORACLE),
            context_manager=context_manager,
            message_router=router,
            event_bus=event_bus,
            task_queue=task_queue,
            llm_configs=[llm_config],
            consensus_threshold=0.0,  # No consensus needed for single model
            enable_api_calls=self.config.include_real_api_calls,
        )
        
        return agent
    
    async def run_experiment(
        self,
        endpoints: List[EndpointContext],
        ground_truths: Dict[UUID, GroundTruth]
    ) -> ExperimentReport:
        """
        Run complete RQ1 experiment using real OracleAgent.
        
        Args:
            endpoints: List of endpoint contexts to test
            ground_truths: Ground truth oracles for each endpoint
            
        Returns:
            ExperimentReport with results and metrics
        """
        report = ExperimentReport(
            experiment_id=self.config.experiment_id,
            config=self.config,
            started_at=datetime.utcnow(),
            total_endpoints=len(endpoints)
        )
        
        # Add ground truths to calculator
        for gt in ground_truths.values():
            self.calculator.add_ground_truth(gt)
        
        # Run experiments for each model
        for model in self.config.llm_models:
            print(f"\n{'='*60}")
            print(f"Running experiments with model: {model}")
            print(f"{'='*60}")
            
            try:
                oracles_by_endpoint = await self._run_model_experiment(
                    model, endpoints
                )
                
                # Calculate metrics for each endpoint
                for endpoint in endpoints:
                    if endpoint.id not in ground_truths:
                        print(f"⚠️  Skipping {endpoint.name}: no ground truth available")
                        continue
                    
                    oracle = oracles_by_endpoint.get(endpoint.id)
                    gt = ground_truths[endpoint.id]
                    
                    # Find or create result for this endpoint
                    result = self._get_or_create_endpoint_result(report, endpoint, gt)
                    
                    if oracle:
                        result.generated_oracles[model] = oracle
                        
                        metrics = self.calculator.calculate_metrics(
                            oracle=oracle,
                            endpoint=endpoint,
                            ground_truth=gt
                        )
                        result.metrics[model] = metrics
                        
                        print(f"✓ {endpoint.name}: P={metrics.precision:.2f}, R={metrics.recall:.2f}, F1={metrics.f1_score:.2f}")
                    else:
                        result.errors[model] = "No oracle generated"
                        print(f"✗ {endpoint.name}: No oracle generated")
                        
            except Exception as e:
                logger.error(f"Error running experiment with {model}: {e}")
                print(f"✗ Model {model} failed: {e}")
                # Mark all endpoints as failed for this model
                for endpoint in endpoints:
                    if endpoint.id in ground_truths:
                        result = self._get_or_create_endpoint_result(
                            report, endpoint, ground_truths[endpoint.id]
                        )
                        result.errors[model] = str(e)
        
        # Calculate aggregate metrics
        report.completed_at = datetime.utcnow()
        report.calculate_aggregates()
        
        # Save report
        output_dir = self.config.output_dir / "rq1"
        output_dir.mkdir(parents=True, exist_ok=True)
        report.save(output_dir / f"rq1_report_{self.config.experiment_id}.json")
        
        return report
    
    def _get_or_create_endpoint_result(
        self, 
        report: 'ExperimentReport', 
        endpoint: EndpointContext, 
        ground_truth: GroundTruth
    ) -> EndpointExperimentResult:
        """Get existing endpoint result or create new one."""
        for result in report.endpoint_results:
            if result.endpoint_id == endpoint.id:
                return result
        
        result = EndpointExperimentResult(
            endpoint_id=endpoint.id,
            endpoint_name=endpoint.name,
            ground_truth=ground_truth
        )
        report.endpoint_results.append(result)
        return result
    
    async def _run_model_experiment(
        self,
        model: str,
        endpoints: List[EndpointContext]
    ) -> Dict[UUID, Oracle]:
        """
        Run oracle generation for all endpoints using a specific model.
        
        Returns dict mapping endpoint_id to generated Oracle.
        """
        # Create fresh storage and context manager for this run
        storage = InMemoryStorage()
        await storage.initialize()
        context_manager = ContextManager(storage=storage)
        
        # Create session
        session_label = f"rq1_{model}_{self.config.experiment_id}"
        session = await context_manager.create_session(
            collection_name=session_label,
            collection_path=str(VARIANTS_DIR),
            llm_models={AgentType.ORACLE: model},
            config={"session_label": session_label, "model": model},
        )
        
        # Add endpoints to session
        for endpoint in endpoints:
            await context_manager.add_endpoint(session.id, endpoint)
        
        # Create oracle agent
        oracle_agent = await self._create_oracle_agent(model, context_manager)
        
        # Generate oracles
        start_time = datetime.utcnow()
        
        oracle_task = Task(
            agent_type=AgentType.ORACLE,
            task_type="derive_oracles",
            session_id=session.id,
            payload={"context_ids": [str(e.id) for e in endpoints]},
        )
        
        await oracle_agent.process_task(oracle_task)
        
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        print(f"  Oracle generation completed in {elapsed:.2f}s")
        
        # Retrieve generated oracles
        oracles = await context_manager.get_oracles(session.id)
        oracles_by_endpoint = {o.endpoint_id: o for o in oracles}
        
        return oracles_by_endpoint


def create_sample_endpoints() -> List[EndpointContext]:
    """Create sample endpoint contexts for testing."""
    return [
        EndpointContext(
            name="Get User by ID",
            method=HTTPMethod.GET,
            url="/api/users/{id}",
            description="Retrieve a user by their unique identifier",
            parameters=[
                {"name": "id", "type": "path", "required": True, "description": "User ID"}
            ],
            documentation_completeness=1.0
        ),
        EndpointContext(
            name="Create User",
            method=HTTPMethod.POST,
            url="/api/users",
            description="Create a new user",
            request_body={
                "type": "object",
                "required": ["email", "name"],
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "name": {"type": "string", "minLength": 1}
                }
            },
            documentation_completeness=1.0
        ),
        EndpointContext(
            name="List Users",
            method=HTTPMethod.GET,
            url="/api/users",
            description="Get a paginated list of users",
            parameters=[
                {"name": "page", "type": "query", "required": False, "description": "Page number"},
                {"name": "limit", "type": "query", "required": False, "description": "Items per page"}
            ],
            documentation_completeness=0.8
        )
    ]


def create_sample_ground_truths(endpoints: List[EndpointContext]) -> Dict[UUID, GroundTruth]:
    """Create sample ground truth oracles for testing."""
    ground_truths = {}
    
    for endpoint in endpoints:
        if "Get User by ID" in endpoint.name:
            ground_truths[endpoint.id] = GroundTruth(
                endpoint_id=endpoint.id,
                status_code=200,
                required_headers={
                    "Content-Type": "application/json"
                },
                optional_headers={
                    "Cache-Control": "max-age=3600"
                },
                response_schema={
                    "type": "object",
                    "required": ["id", "email", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string"},
                        "name": {"type": "string"},
                        "created_at": {"type": "string"}
                    }
                },
                business_rules=[
                    "User ID must be positive integer",
                    "Email must be unique",
                    "Created_at must be ISO8601 timestamp"
                ],
                source="manual_annotation",
                confidence=1.0
            )
        
        elif "Create User" in endpoint.name:
            ground_truths[endpoint.id] = GroundTruth(
                endpoint_id=endpoint.id,
                status_code=201,
                required_headers={
                    "Content-Type": "application/json",
                    "Location": "/api/users/{id}"
                },
                optional_headers={},
                response_schema={
                    "type": "object",
                    "required": ["id", "email", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string"},
                        "name": {"type": "string"}
                    }
                },
                business_rules=[
                    "Returns 409 if email already exists",
                    "Returns 400 if email format invalid"
                ],
                source="manual_annotation",
                confidence=1.0
            )
        
        elif "List Users" in endpoint.name:
            ground_truths[endpoint.id] = GroundTruth(
                endpoint_id=endpoint.id,
                status_code=200,
                required_headers={
                    "Content-Type": "application/json"
                },
                optional_headers={
                    "X-Total-Count": "integer"
                },
                response_schema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "email": {"type": "string"},
                            "name": {"type": "string"}
                        }
                    }
                },
                business_rules=[
                    "Default page=1, limit=10",
                    "Maximum limit=100"
                ],
                source="manual_annotation",
                confidence=1.0
            )
    
    return ground_truths


async def run_experiment_on_dataset(
    dataset_name: str = "jsonplaceholder_rest_api",
    completeness: float = 1.0,
    model_names: Optional[List[str]] = None
):
    """
    Run RQ1 experiment on a real dataset with real agents.
    
    Args:
        dataset_name: Name of the dataset (e.g., 'jsonplaceholder_rest_api')
        completeness: Documentation completeness level (0.0-1.0)
        model_names: List of LLM models to use. Defaults to available models.
    """
    # Load configuration
    app_config = load_config()
    
    # Determine models to use
    if model_names is None:
        # Use all available models
        model_names = list(app_config.llm_models.keys())
        if not model_names:
            raise ValueError("No LLM models configured. Check config/llm_config.yaml")
    
    print(f"Using models: {model_names}")
    
    # Get LLM configurations
    llm_configs = _ensure_models_available(app_config, model_names)
    
    # Load dataset
    print(f"\nLoading dataset: {dataset_name} (completeness={completeness})")
    endpoints, ground_truths = load_variant(dataset_name, completeness)
    print(f"Loaded {len(endpoints)} endpoints with {len(ground_truths)} ground truths")
    
    # Create experiment config
    experiment_id = f"rq1_{dataset_name}_{int(completeness*100)}pct_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    config = ExperimentConfig(
        experiment_id=experiment_id,
        name=f"RQ1 - {dataset_name}",
        description=f"Oracle validation on {dataset_name} with {completeness*100:.0f}% completeness",
        llm_models=model_names,
        num_endpoints=len(endpoints),
        include_real_api_calls=False,
        output_dir=Path("experiments/results")
    )
    
    # Run experiment with real agents
    runner = RQ1ExperimentRunner(config, llm_configs)
    report = await runner.run_experiment(endpoints, ground_truths)
    
    # Print summary
    print("\n" + "="*80)
    print(f"RQ1 Experiment Complete: {config.experiment_id}")
    print("="*80)
    print(f"Dataset: {dataset_name}")
    print(f"Completeness: {completeness*100:.0f}%")
    print(f"Total Endpoints: {report.total_endpoints}")
    print(f"Duration: {(report.completed_at - report.started_at).total_seconds():.2f}s")
    print("\nAggregate Metrics by LLM:")
    print("-"*80)
    
    for model, metrics in sorted(
        report.aggregate_metrics.items(),
        key=lambda x: x[1]["f1_mean"],
        reverse=True
    ):
        rank = report.llm_rankings.get(model, "-")
        print(f"\n{rank}. {model}")
        print(f"   Precision: {metrics['precision_mean']:.3f} (±{metrics['precision_std']:.3f})")
        print(f"   Recall:    {metrics['recall_mean']:.3f} (±{metrics['recall_std']:.3f})")
        print(f"   F1 Score:  {metrics['f1_mean']:.3f} (±{metrics['f1_std']:.3f})")
        print(f"   Complete:  {metrics['completeness_mean']:.3f} (±{metrics['completeness_std']:.3f})")
        print(f"   Success:   {report.successful_generations.get(model, 0)}/{report.total_endpoints}")
    
    print("\n" + "="*80)
    print(f"Report saved to: experiments/results/rq1/rq1_report_{config.experiment_id}.json")
    print("="*80)
    
    return report


async def run_sample_experiment():
    """Run RQ1 experiment on available datasets."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run RQ1 Oracle Validation Experiment")
    parser.add_argument(
        "--dataset", 
        type=str, 
        default="jsonplaceholder_rest_api",
        help="Dataset name to use (default: jsonplaceholder_rest_api)"
    )
    parser.add_argument(
        "--completeness",
        type=float,
        default=1.0,
        help="Documentation completeness level 0.0-1.0 (default: 1.0)"
    )
    parser.add_argument(
        "--models",
        type=str,
        nargs="+",
        default=None,
        help="LLM models to use (default: all available)"
    )
    
    args = parser.parse_args()
    
    return await run_experiment_on_dataset(
        dataset_name=args.dataset,
        completeness=args.completeness,
        model_names=args.models
    )


if __name__ == "__main__":
    asyncio.run(run_sample_experiment())
