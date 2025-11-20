# Changelog

Toutes les modifications notables du projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet suit le [Semantic Versioning](https://semver.org/lang/fr/).

## [2.0.0] - 2025-11-20

### Ajouté

#### Organisation par Exécution
- Structure de répertoires par exécution (`exec_YYYYMMDD_HHMMSS/`)
- Sous-répertoires automatiques pour chaque type de fichier : `reports/`, `graphs/`, `logs/`, `traces/`, `oracles/`, `contexts/`, `tests/java/`, `tests/gherkin/`
- Isolation complète de chaque exécution dans son propre répertoire
- Simplification des noms de fichiers (timestamp dans le nom du répertoire parent)
- Documentation complète dans `output/README.md`

#### Métriques de Confidence
- Section "Oracle Confidence Metrics" dans le rapport HTML des agents
- Affichage de la confidence moyenne, minimale et maximale
- Tableau détaillé avec nom d'endpoint, confidence et niveau de qualité
- Classification visuelle par couleur (🟢 High ≥80%, 🟡 Medium 60-79%, 🔴 Low <60%)
- Affichage de la confidence dans `oracle_list.txt` et `execution_trace.json`
- CSS pour la mise en forme des métriques de confidence
- Documentation complète dans `docs/CONFIDENCE_METRICS.md`

#### Tracking des Interactions entre Agents
- Système de comptage des événements dans `EventBus` pour tracker les aller-retours entre agents
- Méthode `get_event_statistics()` pour récupérer les statistiques d'événements
- Section "Agent Interactions & Workflow Iterations" dans le rapport HTML avec :
  - Nombre total d'événements publiés (interactions entre agents)
  - Nombre de types d'événements uniques
  - Moyenne d'événements par type
  - Tableau de distribution des événements avec pourcentages
- Ajout de la section `agent_interactions` dans `execution_trace.json`
- Logging des statistiques d'événements dans la console pendant l'exécution
- Documentation des aller-retours et itérations du workflow dans les rapports

#### Noms d'Oracles
- Ajout de l'attribut `name` au modèle `Oracle` (champ requis)
- Génération automatique de noms significatifs pour les oracles :
  - Format consensus : `"{endpoint_name} Oracle"`
  - Format fallback : `"{endpoint_name} Oracle (Fallback)"`
- Affichage des noms d'oracles dans tous les rapports (`oracle_list.txt`, `execution_trace.json`, HTML)
- Colonne "Oracle Name" dans les tableaux de confidence

#### Modèles LLM dans les Rapports
- Ajout de la section "🤖 LLM Models" dans le rapport HTML des agents
- Tableau affichant le modèle LLM utilisé par chaque agent (Inductor, Oracle, Contractor, Runner)
- Amélioration de la transparence sur les modèles utilisés pour la génération
- Commentaires détaillés dans `main.py` expliquant la configuration des modèles LLM :
  - Extraction des modèles depuis `config.agents[agent_name].consensus.model`
  - Fallback vers 'mistral' si non configuré
  - Utilisation pour le tracking de session et les rapports

#### Gestion de la Régénération de Tests
- Ajout du support pour le type de message `regenerate_test` dans `ContractorAgent`
- Méthode `_regenerate_failed_test()` pour gérer les demandes de régénération de tests échoués
- Correction de l'erreur "No handler found for message type: regenerate_test"
- Logging des demandes de régénération avec test_id, failure_reason et retry_count
- Infrastructure prête pour l'implémentation future de la régénération intelligente

#### Documentation
- Guide de démarrage rapide dans `README.md` avec instructions d'installation et d'exécution
- Section sur la configuration des modèles LLM dans `README.md`
- `docs/PHASE_5_SUMMARY.md` - Résumé technique de la phase 5
- `docs/CONFIDENCE_METRICS.md` - Guide complet des métriques de confidence
- `output/README.md` - Restructuré pour l'organisation par exécution
- `CHANGELOG.md` - Ce fichier

#### Documentation
- `docs/PHASE_5_SUMMARY.md` - Résumé de la phase 5
- `docs/CONFIDENCE_METRICS.md` - Guide des métriques de confidence
- `output/README.md` - Restructuré pour organisation par exécution
- `CHANGELOG.md` - Ce fichier

### Modifié

#### Génération de Rapports (`src/utils/report_generator.py`)
- Constructeur : Ajout du paramètre `execution_id` (optionnel)
- Création automatique de `exec_YYYYMMDD_HHMMSS/` si `execution_id` non fourni
- Sous-répertoires créés : `reports/`, `graphs/`, `logs/`, `traces/`, `oracles/`, `contexts/`, `tests/java/`, `tests/gherkin/`
- Noms de fichiers simplifiés (pas de timestamp redondant)
- `generate_agent_execution_report()` : Ajout du paramètre `oracles` (optionnel)
- Section HTML ajoutée pour afficher les métriques de confidence des oracles

#### Workflow Principal (`src/main.py`)
- Import ajouté : `from datetime import datetime`
- Génération de `execution_id` au démarrage
- Initialisation de `ReportGenerator` avec `execution_id`
- Passage du paramètre `oracles` à `generate_agent_execution_report()`

#### Documentation
- `output/README.md` : Restructuré pour la nouvelle organisation
  - Exemples avec `$LATEST` pour accéder à la dernière exécution
  - Commandes de nettoyage adaptées
  - Section "Avantages de l'Organisation par Exécution"
- `.gitignore` : Simplifié pour ignorer `output/exec_*/`

### Corrigé

#### Chemins Relatifs dans Rapports HTML
- Correction des chemins d'images dans `agent_execution_report.html` et `test_execution_report.html`
- Changement de `<img src="{graph_path.name}">` vers `<img src="../graphs/{graph_path.name}">`
- Impact : Les graphiques s'affichent correctement dans les rapports HTML depuis le sous-répertoire `reports/`

#### Chemin du Répertoire d'Exécution
- Correction dans `ReportGenerator.__init__()` : `output_dir / execution_id` au lieu de `output_dir.parent / execution_id`
- Impact : Les fichiers sont maintenant créés dans `output/exec_XXX/` au lieu de `./exec_XXX/`

#### Attribut Confidence des Oracles
- Uniformisation sur `confidence_score` (nom correct du modèle Oracle) au lieu de `confidence`
- Corrections appliquées dans `oracle_list.txt`, `execution_trace.json` et section HTML de confidence
- Impact : La confidence s'affiche correctement partout (ex: 0.5 pour mode fallback après timeout LLM)

### Technique

#### Compatibilité
- Rétrocompatible : `execution_id` et `oracles` sont optionnels
- Anciennes exécutions dans `output/` restent valides
- Génération automatique de `execution_id` si non fourni

#### Statistiques
- **Lignes modifiées** : ~200
- **Fichiers modifiés** : 3 (`report_generator.py`, `main.py`, `README.md`)
- **Fichiers créés** : 4 (3 docs + CHANGELOG)
- **Documentation** : +1500 lignes
- **Bugs corrigés** : 3 (chemins graphiques, répertoire exécution, attribut confidence)

---

## [1.0.0] - 2025-11-19

### Ajouté

#### Système de Rapports Complets (Phase 4.1)
- `src/utils/report_generator.py` - Classe `ReportGenerator` (680 lignes)
- 5 types de rapports :
  1. Rapport d'exécution des agents (HTML + graphiques)
  2. Rapport d'exécution des tests (HTML + graphiques)
  3. Liste des oracles (TXT)
  4. Trace d'exécution complète (JSON)
  5. Fichier de log du workflow (LOG)
- Graphiques avec `matplotlib` :
  - Métriques des agents (tâches traitées/réussies/échouées)
  - Résultats des tests (succès/échecs)
- Intégration dans le workflow (`src/main.py`)

#### Conventions de Nommage (Phase 4)
- `docs/NAMING_CONVENTIONS.md` - Guide complet (350+ lignes)
- PascalCase pour les classes Java : `GetUsersTest.java`
- snake_case pour les features Gherkin : `get_users.feature`
- snake_case + timestamp pour les rapports : `agent_execution_report_20251120_011813.html`
- Application dans `src/agents/contractor.py`

#### Structure de Sortie Organisée
- `output/` - Répertoire centralisé pour tous les outputs
- `output/tests/java/` - Tests Java générés
- `output/tests/gherkin/` - Features Gherkin générées
- `output/reports/html/` - Rapports HTML
- `output/reports/graphs/` - Graphiques PNG
- `output/reports/logs/` - Logs texte
- `output/reports/traces/` - Traces JSON
- `output/oracles/` - Listes d'oracles
- `output/contexts/` - Contextes extraits
- `output/README.md` - Documentation de la structure

#### Scripts et Outils
- `scripts/clean_output.sh` - Nettoyage automatique
  - Suppression des fichiers > 7 jours
  - Conservation des 10 derniers fichiers par type
  - Calcul de l'espace libéré

### Corrigé

#### Modèles de Données (`src/shared_context/models.py`)
- `GeneratedTest` : Ajout de l'attribut `assertion_count` (int, default=0)
- `Oracle` : Ajout de l'attribut `endpoint_name` (str, optional)
- Correction des `AttributeError` dans les rapports

#### Génération de Tests (`src/agents/contractor.py`)
- Sortie vers `./output/tests/java/` et `./output/tests/gherkin/`
- Application des conventions PascalCase/snake_case

#### Exécution de Tests (`src/agents/runner.py`)
- Écriture dans `output/` et copie vers Maven
- Support des deux structures (output/ et generated_tests/)

### Documentation

- `docs/PHASE_4.1_SUMMARY.md` - Résumé de la phase 4.1
- `docs/PHASE_4_PLAN.md` - Plan de la phase 4
- `docs/PROJECT_STRUCTURE.md` - Structure du projet
- `docs/NAMING_CONVENTIONS.md` - Conventions de nommage
- `output/README.md` - Documentation de la structure de sortie

---

## [0.9.0] - 2025-11-18

### Ajouté

#### Système Multi-Agents Complet (Phase 3)
- Architecture basée sur la communication asynchrone
- 4 agents spécialisés :
  1. **InductorAgent** - Extraction des contextes d'endpoints
  2. **OracleAgent** - Génération des oracles de validation
  3. **ContractorAgent** - Génération des tests Java et Gherkin
  4. **RunnerAgent** - Exécution des tests avec Maven
- Orchestration via `MessageRouter`, `EventBus`, `TaskQueue`
- Métriques et monitoring pour chaque agent

#### Contexte Partagé (`src/shared_context/`)
- `ContextManager` - Gestionnaire centralisé du contexte
- `InMemoryStorage` - Backend de stockage en mémoire
- Modèles de données complets :
  - `EndpointContext`
  - `Oracle`
  - `GeneratedTest`
  - `TestExecutionResult`
- Gestion des sessions et des relations entre entités

#### Parser Bruno (`src/parsers/bruno_parser.py`)
- Parsing complet des collections Bruno JSON
- Extraction des requêtes HTTP, headers, body
- Support des variables d'environnement
- Tests unitaires complets

#### Configuration
- `config/agents_config.yaml` - Configuration des agents
- `config/llm_config.yaml` - Configuration des LLMs
- `config/metrics_config.yaml` - Configuration des métriques
- Support de plusieurs providers (OpenAI, Anthropic, Ollama, Azure)

### Modifié

#### Workflow Principal (`src/main.py`)
- Refactoring complet pour architecture multi-agents
- Workflow en 9 étapes :
  1. Initialisation
  2. Parsing de la collection
  3. Extraction des contextes (Inductor)
  4. Génération des oracles (Oracle)
  5. Génération des tests (Contractor)
  6. Exécution des tests (Runner)
  7. Collecte des résultats
  8. Génération des rapports
  9. Nettoyage
- Logging structuré et détaillé
- Gestion d'erreurs robuste

#### Système de Logging (`src/utils/logging.py`)
- Logger personnalisé avec couleurs
- Support du logging structuré (JSON)
- Niveaux : DEBUG, INFO, SUCCESS, WARNING, ERROR
- Rotation des fichiers de log

### Tests

#### Tests Unitaires
- `tests/test_parsers/` - Tests du parser Bruno
- `tests/test_agents/` - Tests des agents
- `tests/test_orchestration/` - Tests de l'orchestration
- `tests/test_shared_context/` - Tests du contexte partagé
- Coverage > 80% pour les composants critiques

#### Tests d'Intégration
- Workflow complet avec collection d'exemple
- Validation de bout en bout
- Vérification des artefacts générés

### Documentation

- `README.md` - Documentation principale
- `docs/PROJECT_STRUCTURE.md` - Architecture du projet
- `docs/ACTION_PLAN.md` - Plan d'action et roadmap
- `docs/PHASE_3.1_SUMMARY.md` - Résumé Phase 3.1
- `docs/PHASE_3.2_SUMMARY.md` - Résumé Phase 3.2
- `docs/OPTIMIZATIONS.md` - Optimisations implémentées
- `docs/COST_OPTIMIZATION.md` - Optimisation des coûts LLM
- `docs/OLLAMA_SETUP.md` - Configuration Ollama

---

## [0.5.0] - 2025-11-15

### Ajouté

#### Prototype Initial (Phase 1-2)
- Structure de base du projet
- Agent de génération de tests simple
- Support basique de Bruno Collections
- Génération de tests Java minimale
- README initial

#### Infrastructure
- Docker support (`docker-compose.yml`)
- Configuration Maven (`generated_tests/pom.xml`)
- Scripts de build

### Documentation
- `AUTHORS.md` - Liste des contributeurs
- `LICENSE` - Licence MIT

---

## Types de Changements

- `Ajouté` : Nouvelles fonctionnalités
- `Modifié` : Modifications de fonctionnalités existantes
- `Obsolète` : Fonctionnalités bientôt supprimées
- `Supprimé` : Fonctionnalités supprimées
- `Corrigé` : Corrections de bugs
- `Sécurité` : Corrections de vulnérabilités

---

## Conventions de Versions

- **Version majeure (X.0.0)** : Changements incompatibles
- **Version mineure (0.X.0)** : Nouvelles fonctionnalités compatibles
- **Version de patch (0.0.X)** : Corrections de bugs

---

**Maintenu par** : Aurel IKAMA HONEY  
**Projet** : Contract Test Generation from API Documentation
