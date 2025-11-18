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

## Phase 2 : Parser Bruno (Semaine 2)

### 2.1 Développement du Parser
- [ ] Analyser le format `.bru` (structure, syntaxe)
- [ ] Implémenter `bruno_parser.py` (lecture fichiers)
- [ ] Créer les modèles Pydantic (`bruno_models.py`)
- [ ] Implémenter `schema_validator.py`
- [ ] Tests unitaires du parser

### 2.2 Validation
- [ ] Créer des collections Bruno de test
- [ ] Valider l'extraction des endpoints, headers, body
- [ ] Gérer les cas d'erreur et documentation incomplète

## Phase 3 : Contexte Partagé (Semaine 3)

### 3.1 Storage Layer
- [ ] Implémenter `context_manager.py`
- [ ] Définir les modèles de données (`models.py`)
- [ ] Interface PostgreSQL (`storage.py`)
- [ ] Cache Redis pour performance
- [ ] Tests d'intégration storage

### 3.2 Communication
- [ ] Protocole de communication inter-agents
- [ ] Sérialisation/désérialisation des messages
- [ ] File d'attente des tâches

## Phase 4 : Agent Inductor (Semaine 4)

### 4.1 Développement
- [ ] Implémenter `base_agent.py` (classe abstraite)
- [ ] Développer `inductor.py`
- [ ] Intégrer client LLM (`llm_client.py`)
- [ ] Prompts engineering pour l'induction
- [ ] Tests avec différents LLMs

### 4.2 Validation
- [ ] Tester extraction du contexte
- [ ] Mesurer la complétude (RQ5)
- [ ] Gérer la documentation incomplète

## Phase 5 : Agent Oracle (Semaine 5)

### 5.1 Développement
- [ ] Implémenter `oracle.py`
- [ ] Dérivation des règles de validation
- [ ] Génération des oracles (status codes, headers, schemas)
- [ ] Consensus multi-LLM
- [ ] Tests unitaires

### 5.2 Validation (RQ1)
- [ ] Mesurer précision des oracles (`oracle_metrics.py`)
- [ ] Mesurer complétude des oracles
- [ ] Comparer avec oracles manuels (ground truth)

## Phase 6 : Agent Contractor (Semaine 6)

### 6.1 Génération de Code
- [ ] Créer templates Jinja2 pour Rest-Assured
- [ ] Implémenter `contractor.py`
- [ ] Implémenter `generator.py`
- [ ] Formateur de code Java (`java_formatter.py`)
- [ ] Génération `pom.xml` dynamique

### 6.2 Validation (RQ2)
- [ ] Détecter incohérences oracles/code (`inconsistency_detector.py`)
- [ ] Tests de cohérence
- [ ] Validation syntaxique Java

## Phase 7 : Agent Runner (Semaine 7)

### 7.1 Exécution
- [ ] Implémenter `runner.py`
- [ ] Implémenter `maven_runner.py`
- [ ] Parser les résultats JUnit (`results_parser.py`)
- [ ] Collecte des métriques
- [ ] Gestion des timeouts et erreurs

### 7.2 Feedback Loop
- [ ] Implémenter `feedback_loop.py`
- [ ] Transmission des erreurs aux agents amont
- [ ] Raffinement itératif
- [ ] Condition d'arrêt (convergence/max iterations)

## Phase 8 : Orchestration (Semaine 8)

### 8.1 Workflow
- [ ] Implémenter workflow LangGraph/CrewAI
- [ ] Séquençage des agents (Inductor → Oracle → Contractor → Runner)
- [ ] Gestion des états
- [ ] Parallélisation quand possible

### 8.2 Communication
- [ ] Implémenter `communication.py`
- [ ] Message passing entre agents
- [ ] Event-driven architecture

## Phase 9 : Validation & Métriques (Semaine 9-10)

### 9.1 Implémentation Métriques
- [ ] `oracle_metrics.py` (RQ1)
- [ ] `inconsistency_detector.py` (RQ2)
- [ ] `test_quality_analyzer.py` (RQ3)
- [ ] `llm_comparator.py` (RQ4)
- [ ] `completeness_analyzer.py` (RQ5)

### 9.2 Qualité du Code (RQ3)
- [ ] Métriques de correction (assertions valides)
- [ ] Métriques de lisibilité (complexité cyclomatique)
- [ ] Métriques de maintenabilité (duplication, structure)
- [ ] Intégration SonarQube

## Phase 10 : Expérimentations (Semaine 11-12)

### 10.1 Datasets
- [ ] Collecter collections Bruno variées
- [ ] Créer documentation incomplète (RQ5)
- [ ] Annoter ground truth
- [ ] Diviser train/test sets

### 10.2 Notebooks Jupyter
- [ ] `rq1_oracle_analysis.ipynb`
- [ ] `rq2_inconsistency_study.ipynb`
- [ ] `rq3_quality_evaluation.ipynb`
- [ ] `rq4_llm_comparison.ipynb`
- [ ] `rq5_completeness_impact.ipynb`

### 10.3 Expériences
- [ ] Exécuter pour chaque LLM (GPT-4, Claude, Gemini, Mistral, Llama)
- [ ] Varier complétude documentation (100%, 75%, 50%, 25%)
- [ ] Collecter métriques (précision, recall, F1, temps)
- [ ] Analyse statistique (moyennes, écart-types, tests)

## Phase 11 : Monitoring & Reporting (Semaine 13)

### 11.1 Monitoring
- [ ] Setup Prometheus + Grafana
- [ ] Dashboards métriques temps réel
- [ ] Setup MLflow pour tracking
- [ ] Elasticsearch pour logs

### 11.2 Reporting
- [ ] Scripts de génération de rapports
- [ ] Visualisations (Matplotlib/Seaborn)
- [ ] Tableaux comparatifs
- [ ] Export LaTeX pour publication

## Phase 12 : Tests & Documentation (Semaine 14)

### 12.1 Tests
- [ ] Tests unitaires (coverage > 80%)
- [ ] Tests d'intégration
- [ ] Tests end-to-end
- [ ] Tests de performance (benchmarks)

### 12.2 Documentation
- [ ] Documentation API (Sphinx)
- [ ] `architecture.md`
- [ ] `api_reference.md`
- [ ] `research_methodology.md`
- [ ] Tutoriels et exemples

## Phase 13 : Optimisation & Déploiement (Semaine 15)

### 13.1 Optimisation
- [ ] Profiling performance
- [ ] Optimisation requêtes LLM (caching)
- [ ] Parallélisation agents
- [ ] Réduction coûts API

### 13.2 Déploiement
- [ ] CI/CD GitHub Actions
- [ ] Déploiement Docker
- [ ] Documentation déploiement
- [ ] Script `run_experiment.py`

## Phase 14 : Analyse Finale (Semaine 16)

### 14.1 Résultats
- [ ] Compilation résultats RQ1-RQ5
- [ ] Analyse comparative LLMs
- [ ] Identification limitations
- [ ] Recommandations

### 14.2 Publication
- [ ] Rédaction article scientifique
- [ ] Préparation présentation
- [ ] Release v1.0
- [ ] Documentation utilisateur

---

## Livrables par Phase

**Phase 1-2** : Parser Bruno fonctionnel
**Phase 3-4** : Agent Inductor + contexte
**Phase 5-6** : Agents Oracle + Contractor
**Phase 7-8** : Agent Runner + orchestration complète
**Phase 9-10** : Système de validation + expérimentations
**Phase 11-12** : Monitoring + tests complets
**Phase 13-14** : Projet déployé + résultats recherche

---

## Priorisation

### Critique (MVP)
1. Parser Bruno
2. Agent Inductor
3. Agent Oracle
4. Agent Contractor
5. Agent Runner
6. Workflow basique

### Important
7. Feedback loop
8. Métriques RQ1-RQ5
9. Expérimentations
10. Tests complets

### Nice to have
11. Monitoring avancé
12. Optimisations performance
13. Interface utilisateur

---

## Timeline

- **Semaines 1-2** : Setup + Parser
- **Semaines 3-4** : Contexte + Agent Inductor
- **Semaines 5-6** : Agents Oracle + Contractor
- **Semaines 7-8** : Agent Runner + Orchestration
- **Semaines 9-10** : Validation + Expérimentations
- **Semaines 11-12** : Expériences complètes
- **Semaines 13-14** : Tests + Documentation
- **Semaines 15-16** : Optimisation + Publication
