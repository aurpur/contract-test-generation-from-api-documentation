# Contract Test Generation from API Documentation

## Description

Ce projet automatise la génération de tests de contrat à partir de documentation d'API sous forme de collection Bruno. Il permet de créer automatiquement des tests qui vérifient que l'implémentation d'une API respecte sa spécification, assurant ainsi la cohérence entre la documentation et le comportement réel de l'API.

## Architecture Multi-Agent

Notre approche repose sur une architecture collaborative de quatre agents spécialisés orchestrés pour transformer la documentation d'API en tests de contrat exécutables.

### Agents Spécialisés

1. **Inductor** - Agent d'Induction du Contexte
2. **Oracle** - Agent de Dérivation des Oracles
3. **Contractor** - Agent de Matérialisation des Contrats
4. **Runner** - Agent d'Exécution et Feedback

## Workflow Détaillé

### Phase 1 : Induction du Contexte

L'agent **Inductor** analyse la collection Bruno en entrée pour extraire :
- Les points d'accès (endpoints)
- Les méthodes HTTP
- Les paramètres de requête
- Les corps de requête
- Les schémas de réponse attendus

Cette phase construit un contexte partagé structuré accessible aux agents suivants, compensant l'incomplétude documentaire par inférence heuristique.

### Phase 2 : Dérivation des Oracles

L'agent **Oracle** reçoit le contexte partagé et dérive les règles de validation :
- Codes de statut HTTP attendus
- Contraintes sur les en-têtes de réponse
- Invariants structurels JSON
- Contraintes de domaine (plages de valeurs, formats)

La collaboration inter-agent permet un consensus distribué où plusieurs LLMs proposent et vérifient mutuellement les oracles, réduisant les hallucinations et incohérences.

### Phase 3 : Matérialisation des Contrats

L'agent **Contractor** traduit les oracles abstraits en scripts de test concrets utilisant le framework Rest-Assured. Cette phase assure la cohérence entre spécification (oracles) et implémentation (code Java exécutable), avec :
- Génération automatique des assertions
- Configurations d'authentification
- Gestion des dépendances

### Phase 4 : Exécution et Feedback

L'agent **Runner** orchestre l'exécution des tests générés contre l'API cible, collecte les métriques (taux de succès, couverture, temps d'exécution) et identifie les échecs. 

En cas d'échec, une boucle de réparation adaptative transmet les traces d'erreur aux agents amont (Oracle, Inductor) qui raffinent leurs productions jusqu'à convergence ou seuil maximal d'itérations.

## Stack Technique

### Orchestration & Agents
- **Python 3.9.10** : Langage principal pour l'orchestration
- **LangGraph 0.4.0** : Framework multi-agent avec checkpointing (2.1.2)
- **LangChain 0.2.17** avec LangChain-Core 0.2.43 : Orchestration LLM
- **OpenAI 2.8.1, Anthropic 0.73.0, Google Generative AI 0.8.5, Ollama 0.1.7** : Clients LLM pour GPT-4, Claude Sonnet 4, Gemini, Mistral, Llama 3.1 (RQ4)

### Parsing & Analyse
- **Parser Bruno personnalisé** : Extraction des fichiers `.bru`
- **Pydantic 2.5.0** : Validation et modélisation des données avec Pydantic-Core 2.14.1
- **JSON Schema** : Validation des schémas d'API

### Génération de Tests
- **Java 17.0.1 LTS** avec **Maven 3.8.4**
- **Rest-Assured 5.x** : Framework de test API
- **JUnit 5** : Exécution des tests
- **Jinja2 3.1.2** : Templates pour génération de code Java

### Validation & Métriques (Réponse aux RQ)
- **Pytest 7.4.3** : Framework de validation des composants
- **pytest-cov 4.1.0** : Mesure de couverture de code avec Coverage.py 7.10.7
- **pytest-asyncio 0.21.1** : Support des tests asynchrones
- **Pylint 3.0.3** : Qualité et maintenabilité du code (RQ3)
- **Custom Metrics Engine** :
  - **Oracle Completeness Score** : Précision et complétude des oracles (RQ1)
  - **Inconsistency Detection Rate** : Taux de détection des incohérences (RQ2)
  - **Test Quality Metrics** : Correction, lisibilité, maintenabilité (RQ3)
  - **LLM Comparison Dashboard** : Performance comparative des modèles (RQ4)
  - **Documentation Completeness Impact** : Corrélation documentation/qualité (RQ5)

### Storage & Traçabilité
- **PostgreSQL** : Contexte partagé et historique des générations (psycopg2-binary 2.9.9)
- **Redis 5.0.1** : Cache des résultats intermédiaires
- **SQLAlchemy 2.0.23** : ORM pour la gestion de base de données
- **MLflow 2.9.2** : Tracking des expérimentations et métriques LLM
- **Elasticsearch** : Indexation et analyse des logs

### Monitoring & Reporting
- **Prometheus Client 0.19.0** : Collecte de métriques temps réel
- **Grafana** : Visualisation des métriques
- **Jupyter 1.0.0 / Notebook 7.0.6 / JupyterLab 4.4.10** : Analyse statistique et visualisation (RQ1-RQ5)
- **Pandas 2.3.2 / NumPy 1.26.4 / Matplotlib 3.9.4 / Seaborn 0.13.2** : Traitement et visualisation des données
- **Loguru 0.7.2** : Système de logging avancé
- **LaTeX / Pandoc** : Génération de rapports scientifiques

### Développement & Qualité
- **Black 23.12.1** : Formatage automatique du code
- **isort 5.13.2** : Organisation des imports
- **mypy 1.7.1** : Vérification de types statiques
- **Requests 2.31.0 / httpx 0.25.2** : Clients HTTP
- **python-dotenv 1.0.0** : Gestion des variables d'environnement

### CI/CD
- **Docker** : Containerisation des agents
- **GitHub Actions** : Exécution automatisée des expérimentations
- **pytest-benchmark** : Benchmarking des performances

## Questions de Recherche

Ce projet vise à répondre aux questions de recherche suivantes :

- **RQ1 — Oracle Generation** : Dans quelle mesure un agent IA peut-il générer automatiquement des oracles précis et complets à partir de documentation d'API ?

- **RQ2 — Gap Detection and Reduction** : Dans quelle mesure une architecture multi-agent permet-elle la détection et la réduction des incohérences entre les tests induits et les scripts générés ?

- **RQ3 — Test Validity** : Quelle est la validité quantitative et qualitative des tests générés en termes de correction, lisibilité et maintenabilité ?

- **RQ4 — LLM Model Performance** : Quel modèle de langage (GPT-4, Claude Sonnet 4, Gemini, Mistral, Llama 3.1) fournit les meilleurs résultats en induction, génération et cohérence ?

- **RQ5 — Incomplete Documentation Handling** : Dans quelle mesure l'architecture proposée peut-elle générer des oracles précis et complets à partir de documentation incomplète (collections Bruno) ?

## Fonctionnalités

- Génération automatique de tests de contrat à partir de collections Bruno
- Validation de la conformité entre spécification et implémentation
- Architecture multi-agent collaborative
- Boucle de réparation adaptative pour l'amélioration continue
- Support du format de documentation Bruno
- Système de validation et métriques pour l'évaluation empirique

