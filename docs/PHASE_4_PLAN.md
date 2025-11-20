# Phase 4 - Agent Implementation Plan

**Branch:** `feature/phase-4-agents`  
**Status:** 🚧 En cours  
**Date de début:** 19 novembre 2024

## 🎯 Objectif

Implémenter les 4 agents du système multi-agents :
1. **Inductor Agent** - Extraction du contexte API
2. **Oracle Agent** - Dérivation des assertions
3. **Contractor Agent** - Génération du code de test
4. **Runner Agent** - Exécution et analyse des résultats

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent System                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Inductor   │───▶│    Oracle    │───▶│  Contractor  │  │
│  │              │    │              │    │              │  │
│  │ Extract API  │    │  Generate    │    │  Generate    │  │
│  │  Context     │    │  Oracles     │    │  Test Code   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         └────────────────────┼────────────────────┘          │
│                              ▼                               │
│                     ┌──────────────┐                        │
│                     │    Runner    │                        │
│                     │              │                        │
│                     │   Execute    │                        │
│                     │    Tests     │                        │
│                     └──────────────┘                        │
│                              │                               │
│                              ▼                               │
│                     ┌──────────────┐                        │
│                     │   Feedback   │                        │
│                     │     Loop     │                        │
│                     └──────────────┘                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Phase 4.1 - Base Agent

### Objectifs
- [ ] Créer classe abstraite `BaseAgent`
- [ ] Implémenter cycle de vie de l'agent
- [ ] Intégrer avec l'infrastructure de communication
- [ ] Connecter au système de task queue

### Fichiers à créer
- `src/agents/base_agent.py` (~300 lignes)
- `tests/test_agents/test_base_agent.py` (~200 lignes)

### API BaseAgent

```python
class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(
        self,
        agent_type: AgentType,
        context_manager: ContextManager,
        router: MessageRouter,
        task_queue: TaskQueue,
    ):
        pass
    
    @abstractmethod
    async def process_task(self, task: Task) -> Any:
        """Process a task assigned to this agent."""
        pass
    
    async def start(self):
        """Start the agent."""
        pass
    
    async def stop(self):
        """Stop the agent gracefully."""
        pass
    
    async def send_message(self, message: AgentMessage):
        """Send message to another agent."""
        pass
    
    async def handle_message(self, message: AgentMessage):
        """Handle incoming message."""
        pass
```

## 📦 Phase 4.2 - Inductor Agent

### Objectifs
- [ ] Implémenter extraction du contexte depuis Bruno collections
- [ ] Intégrer Bruno parser existant
- [ ] Extraire endpoints, méthodes, paramètres
- [ ] Analyser la structure de l'API
- [ ] Stocker le contexte dans shared_context

### Fichiers à créer
- `src/agents/inductor.py` (~400 lignes)
- `src/agents/prompts/inductor_prompts.py` (~200 lignes)
- `tests/test_agents/test_inductor.py` (~300 lignes)

### Fonctionnalités
1. **Parse Bruno Collection**
   - Utiliser `BrunoParser` existant
   - Extraire tous les endpoints
   - Identifier relations entre endpoints

2. **Context Extraction**
   - Extraire headers, query params, body schemas
   - Identifier authentification requirements
   - Analyser response schemas

3. **Storage**
   - Créer `EndpointContext` pour chaque endpoint
   - Stocker dans `context_manager`
   - Publier event `CONTEXT_EXTRACTED`

### Prompts LLM
```python
EXTRACT_CONTEXT_PROMPT = """
Analyze this API endpoint and extract structured context:

Endpoint: {method} {path}
Request: {request_info}
Response: {response_info}

Extract:
1. Purpose and description
2. Request schema
3. Response schema
4. Authentication requirements
5. Potential edge cases
"""
```

## 📦 Phase 4.3 - Oracle Agent

### Objectifs
- [ ] Implémenter dérivation d'oracles
- [ ] Générer assertions pour status codes
- [ ] Générer validations pour response schemas
- [ ] Générer validations pour headers
- [ ] Support consensus multi-LLM

### Fichiers à créer
- `src/agents/oracle.py` (~500 lignes)
- `src/agents/prompts/oracle_prompts.py` (~300 lignes)
- `src/validation/oracle_validator.py` (~200 lignes)
- `tests/test_agents/test_oracle.py` (~400 lignes)

### Fonctionnalités
1. **Status Code Oracles**
   - Success cases (200, 201, 204)
   - Error cases (400, 401, 404, 500)
   - Edge cases

2. **Schema Oracles**
   - JSON schema validation
   - Required fields
   - Type validations
   - Format validations

3. **Header Oracles**
   - Content-Type validation
   - Custom headers
   - CORS headers

4. **Multi-LLM Consensus**
   - Query multiple LLMs
   - Compare oracles
   - Vote on assertions
   - Confidence scoring

### Prompts LLM
```python
DERIVE_ORACLES_PROMPT = """
Based on this endpoint context, derive test oracles:

Endpoint: {method} {path}
Context: {endpoint_context}

Generate oracles for:
1. Expected status codes (success and error cases)
2. Response schema validation rules
3. Required headers
4. Business logic assertions
5. Edge cases to test

Format as structured JSON.
"""
```

## 📦 Phase 4.4 - Contractor Agent

### Objectifs
- [ ] Implémenter génération de code Rest-Assured
- [ ] Utiliser templates Jinja2
- [ ] Générer tests Java complets
- [ ] Intégrer oracles dans le code
- [ ] Formater code Java

### Fichiers à créer
- `src/agents/contractor.py` (~400 lignes)
- `src/code_generation/generator.py` (~300 lignes)
- `src/code_generation/java_formatter.py` (~200 lignes)
- `src/code_generation/templates/test_class.j2` (~150 lignes)
- `src/code_generation/templates/test_method.j2` (~100 lignes)
- `tests/test_agents/test_contractor.py` (~350 lignes)

### Fonctionnalités
1. **Code Generation**
   - Generate test class structure
   - Generate test methods
   - Inject oracles as assertions
   - Add setup/teardown

2. **Rest-Assured Integration**
   - Request building
   - Response validation
   - JSON path expressions
   - Schema validation

3. **Java Formatting**
   - Proper indentation
   - Import organization
   - Javadoc comments

### Template Example
```java
@Test
public void test{{ method_name }}() {
    given()
        {% for header in headers %}
        .header("{{ header.name }}", "{{ header.value }}")
        {% endfor %}
        {% if body %}
        .body({{ body }})
        {% endif %}
    .when()
        .{{ http_method|lower }}("{{ endpoint }}")
    .then()
        .statusCode({{ expected_status }})
        {% for assertion in oracles %}
        .body("{{ assertion.path }}", {{ assertion.matcher }})
        {% endfor %}
        ;
}
```

## 📦 Phase 4.5 - Runner Agent

### Objectifs
- [ ] Implémenter exécution Maven
- [ ] Parser résultats JUnit
- [ ] Analyser échecs
- [ ] Collecter métriques
- [ ] Feedback loop

### Fichiers à créer
- `src/agents/runner.py` (~400 lignes)
- `src/execution/maven_runner.py` (~300 lignes)
- `src/execution/results_parser.py` (~250 lignes)
- `src/execution/feedback_analyzer.py` (~200 lignes)
- `tests/test_agents/test_runner.py` (~350 lignes)

### Fonctionnalités
1. **Maven Execution**
   - Execute `mvn test`
   - Capture output
   - Handle errors
   - Timeout management

2. **Results Parsing**
   - Parse JUnit XML
   - Extract pass/fail
   - Capture error messages
   - Collect stack traces

3. **Feedback Analysis**
   - Identify failure patterns
   - Suggest fixes
   - Update oracles
   - Trigger re-generation

4. **Metrics Collection**
   - Execution time
   - Pass rate
   - Coverage
   - Store in context_manager

## 📦 Phase 4.6 - Integration & Tests

### Objectifs
- [ ] Intégrer tous les agents
- [ ] Tests end-to-end
- [ ] Tests de charge
- [ ] Validation RQ1-RQ5

### Tests à créer
- `tests/test_integration/test_workflow.py` (~500 lignes)
- `tests/test_integration/test_feedback_loop.py` (~300 lignes)
- `tests/test_integration/test_multi_llm.py` (~200 lignes)

### Scénarios de test
1. **Single Endpoint Flow**
   - Parse → Extract → Oracle → Generate → Execute
   - Validate each step
   - Check metrics

2. **Multi-Endpoint Flow**
   - Process multiple endpoints
   - Handle dependencies
   - Parallel execution

3. **Feedback Loop**
   - Execute test
   - Detect failure
   - Trigger regeneration
   - Validate fix

4. **Multi-LLM Consensus**
   - Compare oracle outputs
   - Validate voting
   - Check confidence scores

## 📊 Métriques de succès

### Performance
- [ ] Temps d'exécution < 5min pour 10 endpoints
- [ ] Génération de code < 30s par endpoint
- [ ] Exécution tests < 2min

### Qualité (RQ1-RQ5)
- [ ] **RQ1**: Précision oracles > 85%
- [ ] **RQ2**: Cohérence code/oracles > 90%
- [ ] **RQ3**: Efficacité multi-LLM mesurée
- [ ] **RQ4**: Performance LLMs comparée
- [ ] **RQ5**: Complétude > 80%

### Robustesse
- [ ] Retry automatique en cas d'échec
- [ ] Gestion timeout
- [ ] Recovery après erreur
- [ ] Logs détaillés

## 📝 Documentation

### À créer
- [ ] README pour chaque agent
- [ ] Guide d'utilisation
- [ ] Exemples de prompts
- [ ] Métriques et benchmarks
- [ ] PHASE_4_SUMMARY.md

## 🔄 Workflow de développement

1. **Créer base agent** (2-3h)
   - Implémenter BaseAgent
   - Tests unitaires
   - Documentation

2. **Inductor agent** (4-5h)
   - Implémenter extraction
   - Intégrer Bruno parser
   - Tests avec collection réelle

3. **Oracle agent** (5-6h)
   - Implémenter dérivation
   - Multi-LLM consensus
   - Tests de validation

4. **Contractor agent** (4-5h)
   - Templates Jinja2
   - Génération Rest-Assured
   - Tests de code généré

5. **Runner agent** (4-5h)
   - Exécution Maven
   - Parsing résultats
   - Feedback loop

6. **Integration** (3-4h)
   - Tests end-to-end
   - Validation RQ1-RQ5
   - Documentation finale

**Total estimé: 22-28 heures**

## 🚀 Commandes utiles

```bash
# Exécuter tests d'un agent
pytest tests/test_agents/test_inductor.py -v

# Exécuter tests d'intégration
pytest tests/test_integration/ -v

# Vérifier couverture
pytest tests/test_agents/ --cov=src/agents --cov-report=html

# Exécuter le workflow complet
python src/main.py --workflow full --collection bruno_collections/example_api/

# Mode développement (avec logs détaillés)
python src/main.py --workflow full --collection example.json --debug
```

## 📚 Références

- [Phase 3.1 Summary](PHASE_3.1_SUMMARY.md)
- [Phase 3.2 Summary](PHASE_3.2_SUMMARY.md)
- [Action Plan](ACTION_PLAN.md)
- [Project Structure](PROJECT_STRUCTURE.md)

---

**Date de création:** 19 novembre 2024  
**Auteur:** Aurel IKAMA HONEY  
**Statut:** 📋 Planification
