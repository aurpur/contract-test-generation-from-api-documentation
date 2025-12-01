# Contract Test Generation from API Documentation

**Auteur** : Aurel IKAMA HONEY  
**Projet de Recherche** : Génération Automatique de Tests de Contrat

## Description

Ce projet automatise la génération de tests de contrat à partir de documentation d'API sous forme de collection Bruno. Il permet de créer automatiquement des tests qui vérifient que l'implémentation d'une API respecte sa spécification, assurant ainsi la cohérence entre la documentation et le comportement réel de l'API.

## Architecture Multi-Agent

Notre approche repose sur une architecture collaborative de **six agents spécialisés** orchestrés pour transformer la documentation d'API en tests de contrat exécutables de haute qualité.

### Agents Spécialisés (Phase 5.0)

1. **Inductor** - Agent d'Induction du Contexte
2. **Oracle** - Agent de Dérivation des Oracles (+ Appels API Réels)
3. **ValidationAgent** - Agent de Validation des Oracles
4. **Contractor** - Agent de Matérialisation des Contrats
5. **CodeQualityAgent** - Agent de Validation de la Qualité du Code
6. **Runner** - Agent d'Exécution et Feedback

## Workflow Détaillé

### Phase 1 : Induction du Contexte

L'agent **Inductor** analyse la collection Bruno en entrée pour extraire :
- Les points d'accès (endpoints)
- Les méthodes HTTP
- Les paramètres de requête
- Les corps de requête
- Les schémas de réponse attendus

Cette phase construit un contexte partagé structuré accessible aux agents suivants, compensant l'incomplétude documentaire par inférence heuristique.

### Phase 2 : Dérivation des Oracles (+ Appels API Réels)

L'agent **Oracle** reçoit le contexte partagé et dérive les règles de validation :
- Codes de statut HTTP attendus
- Contraintes sur les en-têtes de réponse
- Invariants structurels JSON
- Contraintes de domaine (plages de valeurs, formats)

**Nouveauté Phase 5.0** : L'Oracle peut maintenant effectuer des **appels API réels** pour collecter des données authentiques et améliorer la précision des oracles de manière itérative (+20-40% de confidence). Support d'authentification Bearer, Basic et API Key.

### Phase 4 : Matérialisation des Contrats

L'agent **Contractor** traduit les oracles abstraits en scripts de test concrets utilisant le framework Rest-Assured. Cette phase assure la cohérence entre spécification (oracles) et implémentation (code Java exécutable), avec :
- Génération automatique des assertions
- Configurations d'authentification
- Gestion des dépendances

### Phase 6 : Exécution et Feedback

L'agent **Runner** orchestre l'exécution des tests générés contre l'API cible, collecte les métriques (taux de succès, couverture, temps d'exécution) et identifie les échecs. 

En cas d'échec, une boucle de réparation adaptative transmet les traces d'erreur aux agents amont (Oracle, ValidationAgent, Inductor) qui raffinent leurs productions jusqu'à convergence ou seuil maximal d'itérations.
- Détection de **5 antipatterns** (hard coding, copy-paste programming, etc.)
- Mesure quantitative de l'écart oracle-code (alignment score, coverage ratio)
- Génération de recommandations d'améliorationde (100-599)
- Validation des headers (présence et format)
- Validation du schéma de réponse (JSON Schema)
- Validation des assertions JSONPath
- Validation des règles métier
- Scoring de qualité et recommandations d'amélioration

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
- **Clients LLM Cloud (optionnels)** : OpenAI 2.8.1, Anthropic 0.73.0, Google Generative AI 0.8.5 pour GPT-4, Claude Sonnet 4, Gemini (RQ4)
- **Ollama 0.12.11** : Serveur local pour Mistral et Llama 3.1 (gratuit, sans API key)
- **Mode Développement Économique** : Possibilité de désactiver les modèles cloud (OpenAI, Anthropic, Google) pour un coût de 0€ en utilisant uniquement Ollama

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
- **Mode développement économique** : Désactivation des modèles cloud pour un coût de 0€
- **Organisation par exécution** : Chaque exécution crée un répertoire dédié avec tous ses outputs
- **Métriques de confidence** : Évaluation de la qualité des oracles générés

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le projet
git clone https://github.com/aurpur/contract-test-generation-from-api-documentation.git
cd contract-test-generation-from-api-documentation

# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Installer Ollama (requis pour le mode développement)
# Télécharger depuis https://ollama.ai puis:
ollama pull mistral
ollama pull llama3.1
```

### Exécution

```bash
# Mode développement (gratuit, Ollama uniquement)
export ENABLE_CLOUD_MODELS=false
python src/main.py bruno_collections/example_api/Sample_API_Collection.json

# Les outputs seront dans: output/exec_YYYYMMDD_HHMMSS/
```

### Structure des Outputs

Chaque exécution crée un répertoire dédié :

```
output/
└── exec_20251120_013959/          # Timestamp de l'exécution
    ├── tests/                      # Tests générés (Java + Gherkin)
    ├── reports/                    # Rapports HTML interactifs
    ├── graphs/                     # Graphiques PNG
    ├── logs/                       # Logs d'exécution
    ├── traces/                     # Traces JSON complètes
    ├── oracles/                    # Liste des oracles
    └── contexts/                   # Contextes extraits
```

### Consulter les Résultats

```bash
# Dernière exécution
LATEST=$(ls -td output/exec_* | head -1)

# Ouvrir le rapport HTML avec métriques de confidence
open $LATEST/reports/agent_execution_report.html

# Voir les tests générés
ls $LATEST/tests/java/
ls $LATEST/tests/gherkin/

# Analyser les oracles et leur confidence
cat $LATEST/oracles/oracle_list.txt
jq '.oracles[] | {name, confidence}' $LATEST/traces/execution_trace.json
```

## 📊 Métriques de Confidence

Les oracles générés incluent une **métrique de confidence** (0.0 à 1.0) qui évalue leur qualité :

| Score | Niveau | Signification |
|-------|--------|---------------|
| 🟢 ≥ 0.80 | Élevé | Oracle fiable, validation solide |
| 🟡 0.60-0.79 | Moyen | Oracle acceptable, à vérifier |
| 🔴 < 0.60 | Faible | Oracle incomplet ou fallback |

**Facteurs d'influence** :
- ✅ Qualité des prompts LLM et réponses générées
- ✅ Présence d'exemples dans la documentation
- ✅ Complétude des spécifications
- ❌ Timeouts LLM (déclenche mode fallback à 0.50)

**Visualisation** : Les rapports HTML affichent la confidence par couleur dans les tableaux récapitulatifs.

📖 **Documentation complète** : [`docs/CONFIDENCE_METRICS.md`](docs/CONFIDENCE_METRICS.md)

## Configuration

### Mode Développement vs Production

Le projet supporte deux modes de fonctionnement pour optimiser les coûts :

#### Mode Développement (ENABLE_CLOUD_MODELS=false)
- **Coût : 0€** - Utilise uniquement Ollama (modèles locaux)
- Modèles disponibles : Mistral, Llama 3.1
- Idéal pour le développement, tests locaux et expérimentations
- Pas besoin de clés API cloud
- Tous les agents utilisent automatiquement Ollama comme fallback

#### Mode Production (ENABLE_CLOUD_MODELS=true)
- Accès aux modèles cloud : GPT-4, Claude Sonnet 4, Gemini
- Meilleure performance pour les tâches complexes
- Nécessite les clés API : OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY
- Coût variable selon l'utilisation

### Configuration des Modèles

Modifiez la variable `ENABLE_CLOUD_MODELS` dans le fichier `.env` :

```bash
# Mode Développement (gratuit, Ollama uniquement)
ENABLE_CLOUD_MODELS=false

# Mode Production (cloud + Ollama)
ENABLE_CLOUD_MODELS=true
```

Lorsque `ENABLE_CLOUD_MODELS=false`, le système :
1. Désactive automatiquement les modèles OpenAI, Anthropic et Google
2. Utilise Ollama (Mistral ou Llama) comme fallback pour tous les agents
3. Charge uniquement les modèles locaux en mémoire
4. Ne nécessite pas de clés API cloud

### Prérequis

**Ollama (Obligatoire pour mode développement)** :
- Installation : Téléchargez depuis [ollama.ai](https://ollama.ai)
- Modèles requis : `mistral:latest` et `llama3.1:latest`
- Commandes :
  ```bash
  ollama pull mistral
  ollama pull llama3.1
  ```

**Clés API Cloud (Optionnelles, uniquement si ENABLE_CLOUD_MODELS=true)** :
- OpenAI : [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Anthropic : [console.anthropic.com](https://console.anthropic.com)
- Google : [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

Voir [docs/OLLAMA_SETUP.md](docs/OLLAMA_SETUP.md) pour plus de détails sur la configuration Ollama.

### Changer de Modèle LLM

Pour utiliser un modèle différent de Mistral, modifiez le fichier de configuration des agents :

**`config/agents_config.yaml`** :

```yaml
agents:
  inductor:
    model: "ollama/llama3.1:latest"  # Au lieu de mistral:latest
    timeout: 30
    
  oracle:
    models:
      - provider: "ollama"
        name: "llama3.1:latest"      # Au lieu de mistral:latest
        weight: 1.0
        
  contractor:
    model: "ollama/codellama:latest" # Pour génération de code
    timeout: 45
```

**Modèles Ollama disponibles** :
- `mistral:latest` - Modèle par défaut, bon équilibre performance/vitesse
- `llama3.1:latest` - Meilleure compréhension contextuelle
- `codellama:latest` - Optimisé pour génération de code
- `deepseek-coder:latest` - Excellent pour code Java/Python
- `phi3:latest` - Léger et rapide

**Installation d'un nouveau modèle** :
```bash
ollama pull llama3.1
ollama pull codellama
ollama list  # Vérifier les modèles installés
```

**Modèles cloud** (si `ENABLE_CLOUD_MODELS=true`) :
```yaml
oracle:
  models:
    - provider: "openai"
      name: "gpt-4-turbo-preview"
      weight: 1.0
    - provider: "anthropic"  
      name: "claude-3-sonnet-20240229"
      weight: 0.8
```

📖 **Documentation complète** : [`config/llm_config.yaml`](config/llm_config.yaml) contient tous les paramètres LLM disponibles.

