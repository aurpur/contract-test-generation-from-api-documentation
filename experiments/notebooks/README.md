# Notebooks d'Analyse Expérimentale

**Auteur** : Aurel IKAMA HONEY  
**Date** : Décembre 2025  
**Phase** : 6.2 - Analyse des Questions de Recherche

---

## Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Prérequis](#prérequis)
3. [Structure des Notebooks](#structure-des-notebooks)
4. [Ordre d'Exécution](#ordre-dexécution)
5. [Génération des Données](#génération-des-données)
6. [Dépannage](#dépannage)

---

## Vue d'Ensemble

Ce dossier contient les notebooks Jupyter pour l'analyse des 5 questions de recherche (RQ1–RQ5) du projet de génération automatique de tests de contrat API.

| Notebook | Question de Recherche | Description |
|----------|----------------------|-------------|
| `rq1_oracle_analysis.ipynb` | RQ1 — Oracle Generation | Précision et complétude des oracles générés |
| `rq2_inconsistency_study.ipynb` | RQ2 — Consistency | Détection des incohérences dans la documentation |
| `rq3_quality_evaluation.ipynb` | RQ3 — Test Quality | Qualité des tests générés (couverture, maintenabilité) |
| `rq4_llm_comparison.ipynb` | RQ4 — LLM Comparison | Comparaison des performances des modèles LLM |
| `rq5_completeness_impact.ipynb` | RQ5 — Completeness Impact | Impact de la complétude de la doc sur les résultats |
| `master_analysis.ipynb` | Synthèse | Vue globale et comparaison des RQ1–RQ5 |

---

## Prérequis

### 1. Environnement Python

```bash
# Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Dépendances Principales

Les notebooks requièrent les packages suivants (déjà inclus dans `requirements.txt`) :

```
pandas>=2.2.0
numpy>=1.26.2
matplotlib>=3.8.2
seaborn>=0.13.0
jupyter==1.0.0
notebook==7.0.6
```

### 3. Configuration Ollama (Modèles LLM Locaux)

Le projet utilise **exclusivement des modèles Ollama locaux** (pas d'APIs cloud). Vérifiez qu'Ollama est installé et que les modèles sont disponibles :

```bash
# Vérifier Ollama
ollama --version

# Lister les modèles disponibles
ollama list

# Modèles requis (installer si manquants) :
ollama pull deepseek-r1:8b
ollama pull deepseek-coder-v2
ollama pull codellama:7b
ollama pull qwen2.5:7b
ollama pull qwen2.5-coder:7b
ollama pull llama3.2
ollama pull llama3.1
ollama pull mistral
```

**Note** : Aucune clé API cloud n'est nécessaire. Tous les modèles tournent localement via Ollama.

### 4. Rapports Expérimentaux

Les notebooks analysent les rapports JSON générés par les scripts d'expérimentation. Ces rapports doivent exister dans :

```
experiments/results/
├── rq1/rq1_report_*.json
├── rq2/rq2_report_*.json
├── rq3/rq3_report_*.json
├── rq4/rq4_report_*.json
└── rq5/rq5_report_*.json
```

---

## Structure des Notebooks

Chaque notebook suit une structure standardisée :

1. **Description** — Objectif et contexte du notebook
2. **Énoncé RQ** — Question de recherche adressée
3. **Chargement des données** — Import du dernier rapport JSON
4. **Construction des métriques** — Tableaux de données
5. **Agrégation** — Calculs statistiques
6. **Visualisations** — Graphiques pour publication
7. **Export** — Sauvegarde des résultats (CSV, JSON, figures)

---

## Ordre d'Exécution

### Workflow Recommandé

```
┌─────────────────────────────────────────────────────────────┐
│                    ÉTAPE 1 : GÉNÉRATION                     │
│         Exécuter les scripts pour créer les rapports        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ÉTAPE 2 : ANALYSE RQ                     │
│         Exécuter les notebooks RQ1 → RQ5 (ordre libre)      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ÉTAPE 3 : SYNTHÈSE                       │
│         Exécuter master_analysis.ipynb en dernier           │
└─────────────────────────────────────────────────────────────┘
```

### Étape 1 — Génération des Rapports

Avant d'exécuter les notebooks, générez les rapports expérimentaux :

```bash
# Depuis la racine du projet
cd /path/to/contract-test-generation-from-api-documentation

# Option A : Exécuter tous les orchestrateurs RQ
python -m experiments.rq1_orchestrator
python -m experiments.rq2_orchestrator
python -m experiments.rq345_orchestrator

# Option B : Script unifié Phase 6.2
python scripts/run_phase_6_2.py
```

### Étape 2 — Notebooks RQ Individuels

Les notebooks RQ1–RQ5 sont **indépendants** et peuvent être exécutés dans n'importe quel ordre :

| Ordre | Notebook | Dépendance |
|-------|----------|------------|
| 1-5 | `rq1_oracle_analysis.ipynb` | `results/rq1/rq1_report_*.json` |
| 1-5 | `rq2_inconsistency_study.ipynb` | `results/rq2/rq2_report_*.json` |
| 1-5 | `rq3_quality_evaluation.ipynb` | `results/rq3/rq3_report_*.json` |
| 1-5 | `rq4_llm_comparison.ipynb` | `results/rq4/rq4_report_*.json` |
| 1-5 | `rq5_completeness_impact.ipynb` | `results/rq5/rq5_report_*.json` |

### Étape 3 — Master Analysis

Le notebook `master_analysis.ipynb` doit être exécuté **en dernier** car il agrège les résultats de tous les RQ :

```
Prérequis : Tous les rapports rq1–rq5 doivent exister
```

---

## Génération des Données

### Datasets Bruno

Les expérimentations utilisent des collections Bruno comme source de documentation API :

```
experiments/datasets/
├── train/          # Collections pour entraînement/calibration
├── test/           # Collections pour évaluation
└── full/           # Dataset complet
```

### Scripts de Génération

| Script | Description |
|--------|-------------|
| `experiments/rq1_orchestrator.py` | Génère `rq1_report_*.json` |
| `experiments/rq2_orchestrator.py` | Génère `rq2_report_*.json` |
| `experiments/rq345_orchestrator.py` | Génère `rq3/4/5_report_*.json` |
| `scripts/run_phase_6_2.py` | Exécute tous les orchestrateurs |

### Vérification des Données

```bash
# Vérifier que les rapports existent
ls -la experiments/results/rq*/

# Exemple de sortie attendue
experiments/results/rq1/rq1_report_20251223_010000.json
experiments/results/rq2/rq2_report_20251223_010500.json
...
```

---

## Dépannage

### Erreur : `ModuleNotFoundError: No module named 'experiments'`

Le chemin Python n'inclut pas la racine du projet. Solution dans le notebook :

```python
import sys
from pathlib import Path
PROJECT_ROOT = Path.cwd().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
```

### Erreur : `FileNotFoundError: No RQ1 report found`

Les rapports expérimentaux n'ont pas été générés. Exécutez d'abord :

```bash
python -m experiments.rq1_orchestrator
```

### Erreur : `ModuleNotFoundError: No module named 'experiments.reporting_utils'`

Le module utilitaire n'existe pas. Il a été créé dans `experiments/reporting_utils.py`.

### Kernel Jupyter non trouvé

```bash
# Installer le kernel dans l'environnement virtuel
pip install ipykernel
python -m ipykernel install --user --name=contract-test --display-name="Contract Test Gen"
```

---

## Outputs

Les notebooks génèrent les artefacts suivants :

### Figures (PNG + PDF)

```
experiments/results/figures/
├── rq1/
│   ├── rq1_mean_f1_by_oracle.png
│   └── rq1_f1_distribution_by_oracle.pdf
├── rq2/
├── rq3/
├── rq4/
└── rq5/
```

### Exports CSV/JSON

```
experiments/results/exports/
├── rq1/
│   ├── rq1_endpoint_metrics.csv
│   ├── rq1_aggregate_metrics.csv
│   └── rq1_summary.json
├── rq2/
...
```

---

## Références

- [Phase 6.2 Documentation](../../docs/PHASE_6.2_NOTEBOOKS.md)
- [Datasets Phase 6.1](../../docs/PHASE_6.1_DATASETS.md)
- [Project README](../../README.md)
