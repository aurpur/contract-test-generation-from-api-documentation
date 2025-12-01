# Structure du Projet

**Auteur** : Aurel IKAMA HONEY

```
contract-test-generation-from-api-documentation/
├── README.md
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── setup.py
│
├── config/                          # Configuration globale
│   ├── llm_config.yaml             # Config des modèles LLM
│   ├── agents_config.yaml          # Config des agents
│   └── metrics_config.yaml         # Config des métriques
│
├── src/
│   ├── __init__.py
│   │
│   ├── parsers/                    # Parsing de documentation
│   │   ├── __init__.py
│   │   ├── bruno_parser.py         # Parser collections Bruno
│   │   ├── bruno_models.py         # Modèles Pydantic pour Bruno
│   │   └── schema_validator.py     # Validation des schémas
│   │
│   ├── agents/                     # Les 6 agents spécialisés
│   │   ├── __init__.py
│   │   ├── base_agent.py           # Classe abstraite agent
│   │   ├── factory.py              # Factory pattern pour création agents
│   │   ├── inductor.py             # Agent 1: Induction contexte
│   │   ├── oracle.py               # Agent 2: Dérivation oracles (+ appels API réels)
│   │   ├── validation_agent.py     # Agent 3: Validation des oracles
│   │   ├── contractor.py           # Agent 4: Matérialisation contrats
│   │   ├── code_quality_agent.py   # Agent 5: Validation qualité code
│   │   └── runner.py               # Agent 6: Exécution & feedback
│   │
│   ├── orchestration/              # Orchestration multi-agent
│   │   ├── __init__.py
│   │   ├── workflow.py             # Workflow LangGraph/CrewAI
│   │   ├── communication.py        # Communication inter-agents
│   │   └── feedback_loop.py        # Boucle de réparation adaptative
│   │
│   ├── shared_context/             # Contexte partagé entre agents
│   │   ├── __init__.py
│   │   ├── context_manager.py      # Gestion du contexte
│   │   ├── models.py               # Modèles de données
│   │   └── storage.py              # Interface PostgreSQL/Redis
│   │
│   ├── code_generation/            # Génération de code Java
│   │   ├── __init__.py
│   │   ├── templates/              # Templates Jinja2
│   │   │   ├── test_class.j2
│   │   │   ├── test_method.j2
│   │   │   └── pom_xml.j2
│   │   ├── generator.py            # Générateur de tests
│   │   └── java_formatter.py       # Formatage du code Java
│   │
│   ├── validation/                 # Validation & Métriques (RQ1-RQ5)
│   │   ├── __init__.py
│   │   ├── oracle_metrics.py       # RQ1: Précision des oracles
│   │   ├── inconsistency_detector.py # RQ2: Détection incohérences
│   │   ├── test_quality_analyzer.py  # RQ3: Qualité des tests
│   │   ├── llm_comparator.py       # RQ4: Comparaison modèles
│   │   └── completeness_analyzer.py  # RQ5: Documentation incomplète
│   │
│   ├── execution/                  # Exécution des tests
│   │   ├── __init__.py
│   │   ├── maven_runner.py         # Exécution Maven
│   │   ├── test_executor.py        # Orchestration exécution
│   │   └── results_parser.py       # Parsing des résultats
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging.py              # Configuration logging
│       ├── llm_client.py           # Client LLM unifié
│       ├── java_code_analyzer.py   # Analyseur de code Java (smells/antipatterns)
│       ├── config.py               # Gestion de configuration
│       ├── report_generator.py     # Génération de rapports
│       └── helpers.py              # Fonctions utilitaires
│
├── generated_tests/                # Tests Java générés
│   ├── src/
│   │   └── test/
│   │       └── java/
│   │           └── generated/
│   ├── pom.xml                     # Maven config
│   └── .gitignore
│
├── bruno_collections/              # Collections Bruno d'entrée
│   └── example_api/
│       ├── request1.bru
│       └── request2.bru
│
├── data/                           # Données persistantes
│   ├── contexts/                   # Contextes sauvegardés
│   ├── oracles/                    # Oracles générés
│   └── metrics/                    # Données de métriques
│
├── experiments/                    # Expérimentations (RQ1-RQ5)
│   ├── notebooks/                  # Jupyter notebooks
│   │   ├── rq1_oracle_analysis.ipynb
│   │   ├── rq2_inconsistency_study.ipynb
│   │   ├── rq3_quality_evaluation.ipynb
│   │   ├── rq4_llm_comparison.ipynb
│   │   └── rq5_completeness_impact.ipynb
│   ├── datasets/                   # Datasets de test
│   └── results/                    # Résultats expérimentations
│
├── tests/                          # Tests unitaires du système
│   ├── __init__.py
│   ├── test_parsers/
│   ├── test_agents/
│   ├── test_orchestration/
│   └── test_validation/
│
├── docs/                           # Documentation
│   ├── architecture.md
│   ├── api_reference.md
│   └── research_methodology.md
│
├── scripts/                        # Scripts utilitaires
│   ├── setup_environment.sh
│   ├── run_experiment.py
│   └── generate_report.py
│
└── docker/                         # Configuration Docker
    ├── Dockerfile.agents
    ├── Dockerfile.java
    └── docker-compose.yml
```

## Description des Modules

### Parsers
Module responsable du parsing des collections Bruno et de la validation des schémas JSON/API.

### Agents
Les six agents spécialisés de l'architecture multi-agent (Phase 5.0) :
- **Inductor** : Analyse la documentation et extrait le contexte
- **Oracle** : Dérive les règles de validation + appels API réels pour amélioration itérative
- **ValidationAgent** : Valide la qualité et cohérence des oracles générés
- **Contractor** : Génère les scripts de test Rest-Assured + Gherkin
- **CodeQualityAgent** : Valide la qualité du code généré et mesure l'écart oracle-code
- **Runner** : Exécute les tests et collecte les métriques

### Orchestration
Gestion du workflow multi-agent, communication inter-agents et boucle de feedback adaptatif.

### Shared Context
Contexte partagé entre tous les agents avec persistance PostgreSQL/Redis.

### Code Generation
Génération de code Java Rest-Assured à partir de templates Jinja2.

### Validation
Modules de validation et métriques pour répondre aux questions de recherche (RQ1-RQ5).

### Execution
Orchestration de l'exécution des tests Maven et parsing des résultats.

### Experiments
Notebooks Jupyter et datasets pour les expérimentations scientifiques.

### Tests
Suite de tests unitaires et d'intégration du système.

## Points Clés

1. **Séparation des responsabilités** : Chaque agent a son module distinct
2. **Validation intégrée** : Module dédié pour répondre aux RQ1-RQ5
3. **Expérimentations tracées** : Dossier `experiments/` pour la recherche
4. **Tests générés isolés** : Projet Maven séparé
5. **Contexte centralisé** : Module `shared_context/` pour communication inter-agents
6. **Extensibilité** : Architecture modulaire permettant d'ajouter de nouveaux agents ou métriques
