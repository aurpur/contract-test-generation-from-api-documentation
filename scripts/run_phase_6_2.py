"""Phase 6.2 end-to-end runner.

Generates REAL experiment reports (RQ1–RQ5) from the Phase 6.1 dataset variants.

Outputs:
- experiments/results/rq1/rq1_report_<id>.json
- experiments/results/rq2/rq2_report_<id>.json
- experiments/results/rq3/rq3_report_<id>.json
- experiments/results/rq4/rq4_report_<id>.json
- experiments/results/rq5/rq5_report_<id>.json

Notes:
- Uses the LLM models configured in config/llm_config.yaml (via src.utils.config.load_config).
- No synthetic fallback data is generated; if a variant is missing, the run fails.
"""

from __future__ import annotations

import sys
import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

# Add project root to path so `import src...` works when running as a script
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.base_agent import AgentConfig
from src.agents.contractor import ContractorAgent
from src.agents.oracle import OracleAgent
from src.orchestration import EventBus, InMemoryTaskQueue, MessageRouter, Task
from src.shared_context import AgentType
from src.shared_context.context_manager import ContextManager
from src.shared_context.models import EndpointContext, HTTPMethod
from src.shared_context.storage import InMemoryStorage
from src.utils.config import load_config
from src.utils.logging import logger
from src.validation.inconsistency_detector import InconsistencyDetector
from src.validation.oracle_metrics import GroundTruth, OracleMetricsCalculator

from experiments.rq2_consistency_validation import (
    ConsistencyExperimentConfig,
    RQ2ExperimentRunner,
)
from experiments.rq3_quality_validation import QualityExperimentConfig, RQ3ExperimentRunner
from experiments.rq4_llm_comparison import LLMComparisonConfig, RQ4ExperimentRunner
from experiments.rq5_completeness_impact import CompletenessExperimentConfig, RQ5ExperimentRunner


VARIANTS_DIR = Path("experiments/datasets/variants")


def _variant_dir(dataset_name: str, completeness: float) -> Path:
    percent = int(round(completeness * 100))
    return VARIANTS_DIR / dataset_name / f"completeness_{percent}"


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    with open(path, "r") as f:
        return json.load(f)


def load_variant(dataset_name: str, completeness: float) -> Tuple[List[EndpointContext], Dict[UUID, GroundTruth]]:
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
    missing = [m for m in model_names if m not in config.llm_models]
    if missing:
        raise ValueError(
            "Requested models are not available (check ENABLE_CLOUD_MODELS and config/llm_config.yaml): "
            + ", ".join(missing)
        )

    resolved: Dict[str, Dict[str, Any]] = {}
    for name in model_names:
        model_cfg = config.llm_models[name]
        resolved[name] = model_cfg.model_dump() if hasattr(model_cfg, "model_dump") else dict(model_cfg)
    return resolved


async def generate_oracles_and_tests(
    *,
    endpoints: List[EndpointContext],
    model_name: str,
    llm_config: Dict[str, Any],
    include_real_api_calls: bool,
    session_label: str,
) -> Tuple[UUID, Dict[UUID, Any], Dict[UUID, Any], Dict[str, float]]:
    """Generate oracles and tests using the real agent implementations."""
    storage = InMemoryStorage()
    await storage.initialize()

    context_manager = ContextManager(storage=storage)

    session = await context_manager.create_session(
        collection_name=session_label,
        collection_path=str(VARIANTS_DIR),
        llm_models={AgentType.ORACLE: model_name},
        config={"session_label": session_label, "model": model_name},
    )

    for endpoint in endpoints:
        await context_manager.add_endpoint(session.id, endpoint)

    router = MessageRouter()
    event_bus = EventBus()
    task_queue = InMemoryTaskQueue()

    oracle_agent = OracleAgent(
        config=AgentConfig(agent_type=AgentType.ORACLE),
        context_manager=context_manager,
        message_router=router,
        event_bus=event_bus,
        task_queue=task_queue,
        llm_configs=[llm_config],
        consensus_threshold=0.0,
        enable_api_calls=include_real_api_calls,
    )

    contractor_agent = ContractorAgent(
        config=AgentConfig(agent_type=AgentType.CONTRACTOR),
        context_manager=context_manager,
        message_router=router,
        event_bus=event_bus,
        task_queue=task_queue,
    )

    perf: Dict[str, float] = {
        "total_generation_time_ms": 0.0,
        "avg_generation_time_ms": 0.0,
        "avg_input_tokens": 0.0,
        "avg_output_tokens": 0.0,
    }

    start = datetime.utcnow()

    oracle_task = Task(
        agent_type=AgentType.ORACLE,
        task_type="derive_oracles",
        session_id=session.id,
        payload={"context_ids": [str(e.id) for e in endpoints]},
    )
    await oracle_agent.process_task(oracle_task)

    oracles = await context_manager.get_oracles(session.id)
    oracles_by_endpoint = {o.endpoint_id: o for o in oracles}

    test_task = Task(
        agent_type=AgentType.CONTRACTOR,
        task_type="generate_tests",
        session_id=session.id,
        payload={
            "session_id": str(session.id),
            "oracle_ids": [str(o.id) for o in oracles],
        },
    )
    await contractor_agent.process_task(test_task)

    tests = await context_manager.get_tests(session.id)
    tests_by_endpoint = {t.endpoint_id: t for t in tests}

    elapsed_ms = (datetime.utcnow() - start).total_seconds() * 1000.0
    perf["total_generation_time_ms"] = elapsed_ms
    perf["avg_generation_time_ms"] = elapsed_ms / max(len(endpoints), 1)

    return session.id, oracles_by_endpoint, tests_by_endpoint, perf


def build_rq1_report(
    *,
    experiment_id: str,
    dataset_name: str,
    completeness: float,
    started_at: datetime,
    completed_at: datetime,
    include_real_api_calls: bool,
    model_names: List[str],
    endpoints: List[EndpointContext],
    ground_truths: Dict[UUID, GroundTruth],
    oracles_by_model: Dict[str, Dict[UUID, Any]],
    performance_by_model: Optional[Dict[str, Dict[str, float]]] = None,
) -> Dict[str, Any]:
    calculator = OracleMetricsCalculator()
    for gt in ground_truths.values():
        calculator.add_ground_truth(gt)

    endpoint_results: List[Dict[str, Any]] = []

    for endpoint in endpoints:
        gt = ground_truths.get(endpoint.id)
        if gt is None:
            raise ValueError(f"Missing ground truth for endpoint {endpoint.id}")

        generated_oracles: Dict[str, Any] = {}
        metrics_by_model: Dict[str, Any] = {}
        endpoint_errors: Dict[str, str] = {}
        endpoint_execution_times: Dict[str, float] = {}

        for model in model_names:
            oracle = oracles_by_model.get(model, {}).get(endpoint.id)
            if oracle is None:
                continue

            try:
                m = calculator.calculate_metrics(oracle=oracle, endpoint=endpoint, ground_truth=gt)
                metrics_by_model[model] = {
                    "precision": m.precision,
                    "recall": m.recall,
                    "f1_score": m.f1_score,
                    "completeness_score": m.completeness_score,
                    "true_positives": m.true_positives,
                    "false_positives": m.false_positives,
                    "false_negatives": m.false_negatives,
                }

                generated_oracles[model] = {
                    "oracle_id": str(oracle.id),
                    "name": oracle.name,
                    "status_code": oracle.status_code,
                    "required_headers": oracle.required_headers,
                    "response_schema": oracle.response_schema,
                    "confidence": getattr(oracle, "confidence_score", 0.0),
                }

                if performance_by_model and model in performance_by_model:
                    endpoint_execution_times[model] = float(
                        performance_by_model[model].get("avg_generation_time_ms", 0.0)
                    ) / 1000.0
            except Exception as e:
                endpoint_errors[model] = str(e)

        endpoint_results.append(
            {
                "endpoint_id": str(endpoint.id),
                "endpoint_name": endpoint.name,
                "ground_truth": {
                    "endpoint_id": str(gt.endpoint_id),
                    "status_code": gt.status_code,
                    "required_headers": gt.required_headers,
                    "optional_headers": gt.optional_headers,
                    "response_schema": gt.response_schema,
                    "business_rules": gt.business_rules,
                    "source": gt.source,
                    "confidence": gt.confidence,
                },
                "generated_oracles": generated_oracles,
                "metrics": metrics_by_model,
                "errors": endpoint_errors,
                "execution_times": endpoint_execution_times,
            }
        )

    # Aggregate metrics
    aggregate_metrics: Dict[str, Dict[str, float]] = {}
    successful_generations: Dict[str, int] = {}
    failed_generations: Dict[str, int] = {}

    for model in model_names:
        model_metrics = [
            er["metrics"][model]
            for er in endpoint_results
            if model in er.get("metrics", {})
        ]
        if not model_metrics:
            continue

        import statistics

        aggregate_metrics[model] = {
            "precision_mean": statistics.mean(m["precision"] for m in model_metrics),
            "precision_std": statistics.stdev(m["precision"] for m in model_metrics) if len(model_metrics) > 1 else 0.0,
            "recall_mean": statistics.mean(m["recall"] for m in model_metrics),
            "recall_std": statistics.stdev(m["recall"] for m in model_metrics) if len(model_metrics) > 1 else 0.0,
            "f1_mean": statistics.mean(m["f1_score"] for m in model_metrics),
            "f1_std": statistics.stdev(m["f1_score"] for m in model_metrics) if len(model_metrics) > 1 else 0.0,
            "completeness_mean": statistics.mean(m["completeness_score"] for m in model_metrics),
            "completeness_std": statistics.stdev(m["completeness_score"] for m in model_metrics) if len(model_metrics) > 1 else 0.0,
        }

        successful_generations[model] = len(model_metrics)
        failed_generations[model] = len(endpoints) - len(model_metrics)

    llm_rankings: Dict[str, int] = {}
    if aggregate_metrics:
        sorted_models = sorted(aggregate_metrics.items(), key=lambda x: x[1]["f1_mean"], reverse=True)
        for rank, (model, _) in enumerate(sorted_models, 1):
            llm_rankings[model] = rank

    return {
        "experiment_id": experiment_id,
        "config": {
            "experiment_id": experiment_id,
            "name": f"RQ1 - {dataset_name} - completeness {int(completeness*100)}",
            "description": "RQ1 oracle precision/completeness evaluation (Phase 6.2)",
            "llm_models": model_names,
            "num_endpoints": len(endpoints),
            "include_real_api_calls": include_real_api_calls,
        },
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "total_endpoints": len(endpoints),
        "endpoint_results": endpoint_results,
        "aggregate_metrics": aggregate_metrics,
        "llm_rankings": llm_rankings,
        "successful_generations": successful_generations,
        "failed_generations": failed_generations,
    }


async def run_phase_6_2(
    *,
    dataset: str,
    models: List[str],
    completeness_levels: List[float],
    include_real_api_calls: bool,
    out_dir: Path,
) -> None:
    config = load_config()
    llm_configs = _ensure_models_available(config, models)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # Structure required by RQ5
    results_by_completeness_and_model: Dict[float, Dict[str, Dict[str, Any]]] = {}

    # For RQ4 baseline: use the highest completeness level
    baseline_level = max(completeness_levels)
    baseline_results_by_model: Dict[str, Dict[str, Any]] = {}
    baseline_endpoints: Optional[List[EndpointContext]] = None

    for level in completeness_levels:
        level_started_at = datetime.utcnow()
        endpoints, ground_truths = load_variant(dataset, level)
        if baseline_endpoints is None and level == baseline_level:
            baseline_endpoints = endpoints

        level_results: Dict[str, Dict[str, Any]] = {}

        # RQ1 data assembly across models for this level
        oracles_by_model: Dict[str, Dict[UUID, Any]] = {}
        performance_by_model: Dict[str, Dict[str, float]] = {}

        for model_name in models:
            logger.info(f"Phase 6.2: dataset={dataset} completeness={level} model={model_name}")

            llm_cfg = llm_configs[model_name]
            session_label = f"{dataset}|c{int(level*100)}|{model_name}|{timestamp}"

            session_id, oracles_by_endpoint, tests_by_endpoint, perf = await generate_oracles_and_tests(
                endpoints=endpoints,
                model_name=model_name,
                llm_config=llm_cfg,
                include_real_api_calls=include_real_api_calls,
                session_label=session_label,
            )

            oracles_by_model[model_name] = oracles_by_endpoint
            performance_by_model[model_name] = perf

            # Build RQ2 consistency report for this model+level
            detector = InconsistencyDetector()
            consistency_reports = []
            for ep in endpoints:
                oracle = oracles_by_endpoint.get(ep.id)
                test = tests_by_endpoint.get(ep.id)
                if not oracle or not test:
                    continue

                inc = detector.detect_inconsistencies(oracle=oracle, test=test)
                consistency_reports.append(
                    {
                        "endpoint_id": str(ep.id),
                        "coherence_score": inc.coherence_score,
                        "java_coverage": inc.java_coverage_ratio,
                        "gherkin_coverage": inc.gherkin_coverage_ratio,
                        "inconsistency_count": inc.total_inconsistencies,
                    }
                )

            # Build RQ1 per-endpoint oracle metrics for RQ4/RQ5 consumption
            calc = OracleMetricsCalculator()
            for gt in ground_truths.values():
                calc.add_ground_truth(gt)
            oracle_metrics_rows = []
            for ep in endpoints:
                oracle = oracles_by_endpoint.get(ep.id)
                gt = ground_truths.get(ep.id)
                if not oracle or not gt:
                    continue
                m = calc.calculate_metrics(oracle=oracle, endpoint=ep, ground_truth=gt)
                oracle_metrics_rows.append(
                    {
                        "endpoint_id": str(ep.id),
                        "precision": m.precision,
                        "recall": m.recall,
                        "f1": m.f1_score,
                        "confidence": getattr(oracle, "confidence_score", 0.0),
                    }
                )

            # Build RQ3 quality report rows for RQ4/RQ5 consumption
            rq3_config = QualityExperimentConfig(
                experiment_id=f"{dataset}_c{int(level*100)}_{model_name}_{timestamp}",
                name=f"RQ3 - {dataset} - {model_name} - completeness {int(level*100)}",
                description="RQ3 test quality evaluation (Phase 6.2)",
                llm_models=[model_name],
                num_endpoints=len(endpoints),
                output_dir=out_dir / "rq3",
            )
            rq3_runner = RQ3ExperimentRunner(rq3_config)
            rq3_report = await rq3_runner.run_experiment(
                endpoints=endpoints,
                oracles=oracles_by_endpoint,
                generated_tests=tests_by_endpoint,
            )
            rq3_report.completed_at = datetime.utcnow()
            rq3_path = rq3_report.save()
            quality_reports = [
                {
                    "endpoint_id": str(r.endpoint_id),
                    "correctness": r.correctness_score,
                    "readability": r.readability_score,
                    "maintainability": r.maintainability_score,
                    "overall": r.overall_quality_score,
                }
                for r in rq3_report.endpoint_results
            ]

            # Build and save RQ2 report (full schema) for this model+level
            rq2_config = ConsistencyExperimentConfig(
                experiment_id=f"{dataset}_c{int(level*100)}_{model_name}_{timestamp}",
                name=f"RQ2 - {dataset} - {model_name} - completeness {int(level*100)}",
                description="RQ2 oracle-test consistency validation (Phase 6.2)",
                llm_models=[model_name],
                num_endpoints=len(endpoints),
                output_dir=out_dir / "rq2",
            )
            rq2_runner = RQ2ExperimentRunner(rq2_config)
            rq2_report = await rq2_runner.run_experiment(
                endpoints=endpoints,
                oracles=oracles_by_endpoint,
                generated_tests=tests_by_endpoint,
            )
            rq2_report.completed_at = datetime.utcnow()
            rq2_path = rq2_report.save()

            level_results[model_name] = {
                "session_id": str(session_id),
                "oracles": oracle_metrics_rows,
                "tests": [str(t.id) for t in tests_by_endpoint.values()],
                "quality_reports": quality_reports,
                "consistency_reports": consistency_reports,
                "performance_metrics": perf,
                "rq2_report_path": str(rq2_path),
                "rq3_report_path": str(rq3_path),
            }

            if level == baseline_level:
                baseline_results_by_model[model_name] = level_results[model_name]

        # Save RQ1 report for this completeness level (multi-model)
        rq1_started = level_started_at
        rq1_completed = datetime.utcnow()
        rq1_report = build_rq1_report(
            experiment_id=f"{dataset}_c{int(level*100)}_{timestamp}",
            dataset_name=dataset,
            completeness=level,
            started_at=rq1_started,
            completed_at=rq1_completed,
            include_real_api_calls=include_real_api_calls,
            model_names=models,
            endpoints=endpoints,
            ground_truths=ground_truths,
            oracles_by_model=oracles_by_model,
            performance_by_model=performance_by_model,
        )
        rq1_out_dir = out_dir / "rq1"
        rq1_out_dir.mkdir(parents=True, exist_ok=True)
        rq1_path = rq1_out_dir / f"rq1_report_{rq1_report['experiment_id']}.json"
        with open(rq1_path, "w") as f:
            json.dump(rq1_report, f, indent=2)

        results_by_completeness_and_model[level] = level_results

    # RQ4 (baseline comparison at highest completeness level)
    if baseline_endpoints is None:
        raise ValueError("No baseline endpoints loaded")

    rq4_config = LLMComparisonConfig(
        experiment_id=f"{dataset}_rq4_{timestamp}",
        name=f"RQ4 - {dataset} - LLM comparison",
        description="RQ4 comparative evaluation across LLMs (Phase 6.2)",
        llm_models=models,
        num_endpoints=len(baseline_endpoints),
        output_dir=out_dir / "rq4",
    )
    rq4_runner = RQ4ExperimentRunner(rq4_config)
    rq4_report = await rq4_runner.run_experiment(
        endpoints=baseline_endpoints,
        results_by_model=baseline_results_by_model,
    )
    rq4_report.completed_at = datetime.utcnow()
    rq4_report.save()

    # RQ5 (completeness impact)
    rq5_config = CompletenessExperimentConfig(
        experiment_id=f"{dataset}_rq5_{timestamp}",
        name=f"RQ5 - {dataset} - completeness impact",
        description="RQ5 impact of documentation completeness (Phase 6.2)",
        llm_models=models,
        completeness_levels=completeness_levels,
        output_dir=out_dir / "rq5",
    )
    rq5_runner = RQ5ExperimentRunner(rq5_config)
    rq5_report = await rq5_runner.run_experiment(results_by_completeness_and_model)
    rq5_report.completed_at = datetime.utcnow()
    rq5_report.save()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 6.2 experiments and generate RQ1–RQ5 reports")
    parser.add_argument(
        "--dataset",
        required=True,
        choices=[p.name for p in VARIANTS_DIR.iterdir() if p.is_dir()],
        help="Dataset variant name under experiments/datasets/variants",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=None,
        help="Model names as defined in config/llm_config.yaml (default: all available)",
    )
    parser.add_argument(
        "--allow-cloud-models",
        action="store_true",
        help=(
            "Allow non-Ollama providers (OpenAI/Anthropic/Google) when selecting models. "
            "By default, Phase 6.2 uses only local Ollama models for reproducible, cost-free experiments."
        ),
    )
    parser.add_argument(
        "--completeness",
        nargs="+",
        type=float,
        default=[1.0, 0.75, 0.5, 0.25],
        help="Completeness levels to run (e.g. 1.0 0.75 0.5 0.25)",
    )
    parser.add_argument(
        "--real-api",
        action="store_true",
        help="Enable real API calls in OracleAgent",
    )
    parser.add_argument(
        "--out-dir",
        default="experiments/results",
        help="Base output directory for reports",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    cfg = load_config()

    # Default behavior: Ollama-only models (local, reproducible, no API keys)
    # Override with --allow-cloud-models if you explicitly want to include cloud providers.
    if args.models:
        models = list(args.models)
    else:
        models = list(cfg.llm_models.keys())

    if not args.allow_cloud_models:
        # Filter to Ollama-only, and fail fast if user explicitly asked for a cloud model.
        filtered: List[str] = []
        non_ollama: List[str] = []
        for name in models:
            mcfg = cfg.llm_models.get(name)
            if not mcfg:
                continue
            if getattr(mcfg, "provider", None) == "ollama":
                filtered.append(name)
            else:
                non_ollama.append(name)

        if args.models and non_ollama:
            raise ValueError(
                "Cloud models are not allowed for this run (add --allow-cloud-models to override). "
                "Non-Ollama requested: " + ", ".join(sorted(set(non_ollama)))
            )

        models = filtered

    if not models:
        raise ValueError(
            "No models selected. Ensure you have at least one Ollama model configured in config/llm_config.yaml "
            "and available in your environment."
        )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    asyncio.run(
        run_phase_6_2(
            dataset=args.dataset,
            models=models,
            completeness_levels=args.completeness,
            include_real_api_calls=args.real_api,
            out_dir=out_dir,
        )
    )


if __name__ == "__main__":
    main()
