# Plan d'Action - Contract Test Generation from API Documentation

**Auteur** : Aurel IKAMA HONEY

## Phase 1 : Setup Initial (Semaine 1)

### 1.1 Infrastructure de Base
- [x] Créer la structure de dossiers complète
- [x] Initialiser le projet Python (`setup.py`, `requirements.txt`)
- [x] Configurer Git (`.gitignore`, branches, workflow)
- [x] Setup Docker (`Dockerfile`, `docker-compose.yml`)
- [x] Configurer les environnements (dev, test, prod)

### 1.2 Configuration
- [x] Créer les fichiers de configuration YAML
- [x] Configurer Ollama pour Mistral et Llama (local, sans API key)
- [ ] Setup des clés API pour les LLMs cloud (GPT-4, Claude, Gemini) - **Manuel**
- [x] Configurer PostgreSQL et Redis
- [x] Setup du logging centralisé
- [x] Script de vérification Ollama (`scripts/verify_ollama.py`)
- [x] Documentation Ollama (`docs/OLLAMA_SETUP.md`)

## Phase 2 : Parser Bruno (Semaine 2) ✅

### 2.1 Développement du Parser
- [x] Analyser le format `.bru` (structure, syntaxe)
- [x] Implémenter `bruno_parser.py` (lecture fichiers)
- [x] Créer les modèles Pydantic (`bruno_models.py`)
- [x] Implémenter `schema_validator.py`
- [x] Tests unitaires du parser

### 2.2 Validation
- [x] Créer des collections Bruno de test
- [x] Valider l'extraction des endpoints, headers, body
- [x] Gérer les cas d'erreur et documentation incomplète

### 2.3 Résultats
**Fichiers créés:**
- `src/parsers/bruno_models.py` (266 lignes) - Modèles Pydantic complets
- `src/parsers/bruno_parser.py` (462 lignes) - Parser JSON et .bru
- `src/parsers/schema_validator.py` (334 lignes) - Validation et métriques
- `tests/test_parsers/test_bruno_parser.py` (243 lignes) - Tests unitaires

**Fonctionnalités:**
- ✅ Parsing de collections JSON Bruno
- ✅ Parsing de fichiers .bru individuels
- ✅ Parsing de dossiers contenant des .bru
- ✅ Validation de structure et schémas
- ✅ Métriques de complétude documentation (RQ5)
- ✅ Métriques de couverture tests
- ✅ Extraction endpoints, méthodes, headers, body
- ✅ Support authentification (basic, bearer, apikey)
- ✅ Gestion documentation incomplète

**Tests validés:**
- Collection "Sample API Collection": 1 requête, 0 dossier
- Documentation: 100% complète
- Validation: ✅ Succès

**Optimisations (19 Nov 2025):**
- ✅ Single-pass tree traversal (économie 74% temps parsing)
- ✅ Lazy JSON validation (validation différée jusqu'à besoin)
- ✅ Generator-based extraction (pas de listes intermédiaires)
- ✅ Early exit optimization (flags booléens)

**Performance:** 5.42ms pour parser + valider 120 requêtes (~30K req/ms)

## Phase 3 : Contexte Partagé (Semaine 3)

### 3.1 Storage Layer ✅
- [x] Définir les modèles de données (`models.py`)
- [x] Implémenter `context_manager.py`
- [x] Interface PostgreSQL (`storage.py`)
- [x] Cache Redis pour performance
- [x] Tests d'intégration storage

**Résultats:**
- `src/shared_context/models.py` (509 lignes) - 14 modèles Pydantic complets
- `src/shared_context/context_manager.py` (574 lignes) - API de haut niveau
- `src/shared_context/storage.py` (550 lignes) - Backend PostgreSQL + Redis
- `tests/test_shared_context.py` (636 lignes) - Tests d'intégration complets
- `src/shared_context/README.md` - Documentation complète

**Fonctionnalités:**
- ✅ Modèles pour WorkflowSession, EndpointContext, Oracle, GeneratedTest
- ✅ Modèles pour TestExecutionResult, AgentMessage
- ✅ Modèles métriques: QualityMetrics, LLMPerformanceMetrics, CompletenessAnalysis
- ✅ Modèle InconsistencyReport pour RQ2
- ✅ ContextManager avec API asynchrone complète
- ✅ Backend PostgreSQL avec SQLAlchemy async
- ✅ Cache Redis avec TTL configurable
- ✅ Gestion des sessions et workflow
- ✅ Communication inter-agents (messages)
- ✅ Gestion du feedback loop (iterations)
- ✅ Stockage des métriques pour RQ1-RQ5
- ✅ Tests d'intégration exhaustifs

### 3.2 Communication
- [x] Protocole de communication inter-agents
- [x] Sérialisation/désérialisation des messages
- [x] File d'attente des tâches

**Résultats Phase 3.2:**
- ✅ 2,249 lignes de code (3 modules: communication, serialization, task_queue)
- ✅ MessageRouter + EventBus pour routage et events
- ✅ MessageBuilder avec interface fluent
- ✅ Serializers JSON et Pickle
- ✅ InMemoryTaskQueue avec priorités
- ✅ TaskExecutor avec retry et timeout
- ✅ TaskBuilder pour construction de tâches
- ✅ 1,089 lignes de tests (53 tests)
- ✅ Documentation complète (PHASE_3.2_SUMMARY.md)

**PR #5:** Créé pour merge Phase 3 vers develop

## Phase 4 : Multi-Agent System (Semaine 4-8)

### 4.1 BaseAgent Infrastructure ✅
- [x] Implémenter `base_agent.py` (classe abstraite)
- [x] Développer `factory.py` (AgentFactory + AgentOrchestrator)
- [x] Lifecycle management (start, stop, pause, resume)
- [x] Message handling (send, receive, register handlers)
- [x] Task processing (submit, process, retry logic)
- [x] Event pub/sub (publish, subscribe)
- [x] Metrics collection
- [x] Tests unitaires (16/23 passing)
- [x] Documentation complète

**Résultats Phase 4.1:**
- ✅ `src/agents/base_agent.py` (685 lignes) - BaseAgent abstract class
- ✅ `src/agents/factory.py` (365 lignes) - Factory + Orchestrator
- ✅ `tests/test_agents/test_base_agent.py` (613 lignes) - Unit tests
- ✅ 1,663 lignes total (1,050 production + 613 tests)
- ✅ Integration avec Phase 3 validée
- ✅ Documentation: `docs/PHASE_4.1_SUMMARY.md`
- ✅ 2 commits créés et pushés sur feature/phase-4-agents

**Fonctionnalités:**
- ✅ Abstract BaseAgent avec lifecycle complet
- ✅ AgentState enum (7 états: IDLE→STARTING→RUNNING→PAUSED→STOPPING→STOPPED→ERROR)
- ✅ AgentConfig pour configuration flexible
- ✅ Message routing avec MessageRouter (Phase 3)
- ✅ Task queue avec priorités et retry
- ✅ Event bus pour pub/sub
- ✅ Metrics: tasks_processed, success/fail, messages, errors, active_tasks
- ✅ Graceful shutdown avec timeout
- ✅ Concurrency control (max_concurrent_tasks)
- ✅ Error handling et recovery

### 4.2 Agent Inductor (Semaine 4) ✅
- [x] Implémenter `inductor.py` (hérite de BaseAgent)
- [x] Intégrer BrunoParser existant (Phase 2)
- [x] Extraction contexte des endpoints
- [x] Stockage dans ContextManager
- [x] Prompts engineering pour l'induction
- [x] Tests avec différents LLMs
- [x] Tests unitaires créés (24 tests)
- [x] Documentation

**Résultats Phase 4.2:**
- ✅ `src/agents/inductor.py` (645 lignes) - InductorAgent class
- ✅ `tests/test_agents/test_inductor.py` (620 lignes) - Unit tests
- ✅ 1,265 lignes total (645 production + 620 tests)
- ✅ Integration BrunoParser (Phase 2) validée
- ✅ LLM enrichment (Ollama/OpenAI/Anthropic)
- ✅ Commit 07e3b3f créé et pushé

**Fonctionnalités:**
- ✅ process_task() pour "extract_context" task type
- ✅ Message handlers pour extraction requests (3 handlers)
- ✅ Integration avec BrunoParser (Phase 2)
- ✅ LLM prompts pour context enrichment
- ✅ Event publishing: "context_extracted"
- ✅ Metrics: endpoints_extracted, llm_enriched
- ✅ Schema inference automatique (JSON)
- ✅ Documentation completeness scoring (0.0-1.0)
- ✅ Authentication extraction (Basic/Bearer/APIKey)

### 4.3 Agent Oracle (Semaine 5)
- [ ] Implémenter `oracle.py` (hérite de BaseAgent)
- [ ] Dérivation des règles de validation
- [ ] Génération des oracles (status codes, headers, schemas)
- [ ] Consensus multi-LLM
- [ ] Tests unitaires
- [ ] Documentation

**Tâches détaillées:**
- [ ] process_task() pour "derive_oracles" task type
- [ ] Multi-LLM consensus mechanism
- [ ] Oracle quality validation
- [ ] Stockage oracles dans ContextManager
- [ ] Event publishing: "oracles_derived"
- [ ] Metrics: oracles_generated, consensus_votes, quality_scores

### 4.4 Agent Contractor (Semaine 6)
- [ ] Implémenter `contractor.py` (hérite de BaseAgent)
- [ ] Créer templates Jinja2 pour Rest-Assured
- [ ] Génération code Java avec oracles
- [ ] Formateur de code Java
- [ ] Génération `pom.xml` dynamique
- [ ] Tests unitaires
- [ ] Documentation

**Tâches détaillées:**
- [ ] process_task() pour "generate_code" task type
- [ ] Jinja2 templates pour Rest-Assured
- [ ] Injection oracles as assertions
- [ ] Java code formatting
- [ ] Event publishing: "code_generated"
- [ ] Metrics: tests_generated, lines_of_code, assertions_count

### 4.5 Agent Runner (Semaine 7)
- [ ] Implémenter `runner.py` (hérite de BaseAgent)
- [ ] Implémenter `maven_runner.py`
- [ ] Parser les résultats JUnit
- [ ] Collecte des métriques
- [ ] Feedback loop pour regeneration
- [ ] Gestion des timeouts et erreurs
- [ ] Tests unitaires
- [ ] Documentation

**Tâches détaillées:**
- [ ] process_task() pour "execute_tests" task type
- [ ] Maven execution wrapper
- [ ] JUnit XML parsing
- [ ] Failure analysis
- [ ] Event publishing: "tests_executed"
- [ ] Metrics: tests_run, passed, failed, execution_time

### 4.6 Integration & End-to-End Tests (Semaine 8)
- [ ] Workflow complet: Inductor→Oracle→Contractor→Runner
- [ ] Tests end-to-end pipeline
- [ ] Tests feedback loop (failure→regeneration)
- [ ] Tests multi-LLM consensus
- [ ] Validation RQ1-RQ5
- [ ] Performance benchmarking
- [ ] Documentation workflow complet

**Validation:**
- [ ] Tester extraction du contexte (Inductor)
- [ ] Mesurer précision oracles (RQ1)
- [ ] Détecter incohérences (RQ2)
- [ ] Mesurer qualité code (RQ3)
- [ ] Comparer LLMs (RQ4)
- [ ] Mesurer impact complétude (RQ5)

## Phase 5 : Validation & Métriques (Semaine 9-10)

### 5.1 Implémentation Métriques
- [ ] `oracle_metrics.py` (RQ1 - Précision oracles)
- [ ] `inconsistency_detector.py` (RQ2 - Cohérence oracles/code)
- [ ] `test_quality_analyzer.py` (RQ3 - Qualité code généré)
- [ ] `llm_comparator.py` (RQ4 - Comparaison LLMs)
- [ ] `completeness_analyzer.py` (RQ5 - Impact complétude)

### 5.2 Validation (RQ1)
- [ ] Mesurer précision des oracles
- [ ] Mesurer complétude des oracles
- [ ] Comparer avec oracles manuels (ground truth)

### 5.3 Validation (RQ2)
- [ ] Détecter incohérences oracles/code
- [ ] Tests de cohérence
- [ ] Validation syntaxique Java

### 5.4 Qualité du Code (RQ3)
- [ ] Métriques de correction (assertions valides)
- [ ] Métriques de lisibilité (complexité cyclomatique)
- [ ] Métriques de maintenabilité (duplication, structure)
- [ ] Intégration SonarQube

## Phase 6 : Expérimentations (Semaine 11-12)

### 6.1 Datasets
- [ ] Collecter collections Bruno variées
- [ ] Créer documentation incomplète (RQ5)
- [ ] Annoter ground truth
- [ ] Diviser train/test sets

### 6.2 Notebooks Jupyter
- [ ] `rq1_oracle_analysis.ipynb`
- [ ] `rq2_inconsistency_study.ipynb`
- [ ] `rq3_quality_evaluation.ipynb`
- [ ] `rq4_llm_comparison.ipynb`
- [ ] `rq5_completeness_impact.ipynb`

### 6.3 Expériences
- [ ] Exécuter pour chaque LLM (GPT-4, Claude, Gemini, Mistral, Llama)
- [ ] Varier complétude documentation (100%, 75%, 50%, 25%)
- [ ] Collecter métriques (précision, recall, F1, temps)
- [ ] Analyse statistique (moyennes, écart-types, tests)

## Phase 7 : Monitoring & Reporting (Semaine 13)

### 7.1 Monitoring
- [ ] Setup Prometheus + Grafana
- [ ] Dashboards métriques temps réel
- [ ] Setup MLflow pour tracking
- [ ] Elasticsearch pour logs

### 7.2 Reporting
- [ ] Scripts de génération de rapports
- [ ] Visualisations (Matplotlib/Seaborn)
- [ ] Tableaux comparatifs
- [ ] Export LaTeX pour publication

## Phase 8 : Tests & Documentation (Semaine 14)

### 8.1 Tests
- [ ] Tests unitaires (coverage > 80%)
- [ ] Tests d'intégration
- [ ] Tests end-to-end
- [ ] Tests de performance (benchmarks)

### 8.2 Documentation
- [ ] Documentation API (Sphinx)
- [ ] `architecture.md`
- [ ] `api_reference.md`
- [ ] `research_methodology.md`
- [ ] Tutoriels et exemples

## Phase 9 : Optimisation & Déploiement (Semaine 15)

### 9.1 Optimisation
- [ ] Profiling performance
- [ ] Optimisation requêtes LLM (caching)
- [ ] Parallélisation agents
- [ ] Réduction coûts API

### 9.2 Déploiement
- [ ] CI/CD GitHub Actions
- [ ] Déploiement Docker
- [ ] Documentation déploiement
- [ ] Script `run_experiment.py`

## Phase 10 : Analyse Finale (Semaine 16)

### 10.1 Résultats
- [ ] Compilation résultats RQ1-RQ5
- [ ] Analyse comparative LLMs
- [ ] Identification limitations
- [ ] Recommandations

### 10.2 Publication
- [ ] Rédaction article scientifique
- [ ] Préparation présentation
- [ ] Release v1.0
- [ ] Documentation utilisateur

---

## Livrables par Phase

**Phase 1-2** : Parser Bruno fonctionnel ✅
**Phase 3** : Storage + Communication Infrastructure ✅
**Phase 4** : Multi-Agent System (BaseAgent + 4 agents + integration) 🔄
**Phase 5** : Système de validation + métriques RQ1-RQ5
**Phase 6** : Expérimentations + notebooks
**Phase 7** : Monitoring + reporting
**Phase 8** : Tests complets + documentation
**Phase 9** : Optimisation + déploiement
**Phase 10** : Analyse finale + publication

---

## Priorisation

### Critique (MVP)
1. ✅ Parser Bruno
2. ✅ Infrastructure Phase 3 (Storage + Communication)
3. ✅ BaseAgent Infrastructure (Phase 4.1)
4. ✅ Agent Inductor (Phase 4.2)
5. 🔄 Agent Oracle (Phase 4.3)
6. 🔄 Agent Contractor (Phase 4.4)
7. 🔄 Agent Runner (Phase 4.5)
8. 🔄 Integration & E2E tests (Phase 4.6)

### Important
9. Feedback loop (intégré dans Runner)
10. Métriques RQ1-RQ5 (Phase 5)
11. Expérimentations (Phase 6)
12. Tests complets (Phase 8)

### Nice to have
13. Monitoring avancé (Phase 7)
14. Optimisations performance (Phase 9)
15. Interface utilisateur (futur)

---

## Timeline Révisée

- **Semaines 1-2** : ✅ Setup + Parser Bruno
- **Semaine 3** : ✅ Phase 3 (Storage + Communication)
- **Semaines 4-8** : 🔄 Phase 4 (Multi-Agent System)
  - Semaine 4 : ✅ BaseAgent (4.1) + ✅ Inductor (4.2)
  - Semaine 5 : 🔄 Oracle (4.3)
  - Semaine 6 : Contractor (4.4)
  - Semaine 7 : Runner (4.5)
  - Semaine 8 : Integration & E2E (4.6)
- **Semaines 9-10** : Métriques + Validation (Phase 5)
- **Semaines 11-12** : Expérimentations (Phase 6)
- **Semaine 13** : Monitoring + Reporting (Phase 7)
- **Semaine 14** : Tests + Documentation (Phase 8)
- **Semaine 15** : Optimisation + Déploiement (Phase 9)
- **Semaine 16** : Analyse finale + Publication (Phase 10)
