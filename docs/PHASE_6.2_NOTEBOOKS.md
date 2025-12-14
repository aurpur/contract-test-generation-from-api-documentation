# Phase 6.2 : Notebooks Jupyter d'Analyse

**Auteur** : Aurel IKAMA HONEY  
**Date** : 12 Décembre 2025  
**Statut** : En Cours  
**Phase** : 6.2 - Notebooks Jupyter pour Expérimentations

---

## Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Objectifs de Phase 6.2](#objectifs-de-phase-62)
3. [Architecture des Notebooks](#architecture-des-notebooks)
4. [Description des Notebooks](#description-des-notebooks)
5. [Méthodologie d'Analyse](#méthodologie-danalyse)
6. [Visualisations et Métriques](#visualisations-et-métriques)
7. [Implémentation](#implémentation)
8. [Intégration avec Phase 6.1 et 6.3](#intégration-avec-phase-61-et-63)

---

## Vue d'Ensemble

La Phase 6.2 constitue le **cœur analytique** de notre recherche. Elle vise à créer des notebooks Jupyter interactifs et reproductibles pour analyser chacune des 5 questions de recherche (RQ1-RQ5), en exploitant les datasets créés en Phase 6.1.

### Principes Directeurs

1. **Reproductibilité** : Notebooks entièrement exécutables avec seed fixe
2. **Clarté** : Documentation inline, visualisations explicites
3. **Modularité** : Réutilisation de code via modules communs
4. **Rigueur Scientifique** : Tests statistiques, intervalles de confiance
5. **Interactivité** : Widgets pour exploration dynamique des résultats

---

## Objectifs de Phase 6.2

### Objectifs Primaires

✅ **OBJ-6.2.1** : Créer 5 notebooks d'analyse (RQ1-RQ5)  
✅ **OBJ-6.2.2** : Intégrer avec datasets Phase 6.1  
✅ **OBJ-6.2.3** : Implémenter visualisations statistiques  
✅ **OBJ-6.2.4** : Documenter méthodologie d'analyse  
✅ **OBJ-6.2.5** : Valider reproductibilité des résultats  

### Objectifs Secondaires

- **OBJ-6.2.6** : Créer notebook master consolidé
- **OBJ-6.2.7** : Export résultats pour publication (LaTeX, CSV)
- **OBJ-6.2.8** : Tests unitaires pour fonctions d'analyse

---

## Architecture des Notebooks

### Structure des Notebooks

```
experiments/notebooks/
├── rq1_oracle_analysis.ipynb          # RQ1: Validation oracles automatiques
├── rq2_inconsistency_study.ipynb      # RQ2: Détection incohérences
├── rq3_quality_evaluation.ipynb       # RQ3: Qualité tests générés
├── rq4_llm_comparison.ipynb           # RQ4: Comparaison LLMs
├── rq5_completeness_impact.ipynb      # RQ5: Impact complétude doc
├── master_analysis.ipynb              # Notebook consolidé
├── utils/                              # Utilitaires communs
│   ├── __init__.py
│   ├── plotting.py                    # Fonctions visualisation
│   ├── statistics.py                  # Tests statistiques
│   ├── data_loader.py                 # Chargement datasets
│   └── export.py                      # Export résultats
└── outputs/                            # Résultats exportés
    ├── figures/                        # Figures PNG/PDF
    ├── tables/                         # Tableaux LaTeX/CSV
    └── reports/                        # Rapports Markdown
```

### Dépendances Communes

```python
# Data Science Stack
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical Analysis
from scipy import stats
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import statsmodels.api as sm

# Visualization
import plotly.express as px
import plotly.graph_objects as go

# Project Specific
import sys
sys.path.append('../..')
from experiments.rq1_oracle_validation import OracleValidator
from experiments.rq2_consistency_validation import ConsistencyChecker
# ... etc
```

---

## Description des Notebooks

### 1. RQ1: Oracle Validation Analysis (`rq1_oracle_analysis.ipynb`)

**Question de Recherche** : *Dans quelle mesure les oracles automatiques génèrent-ils des assertions correctes et complètes ?*

**Sections du Notebook** :

1. **Introduction & Context**
   - Définition des oracles
   - Hypothèses de recherche
   - Métriques évaluées

2. **Data Loading**
   - Chargement ground truth
   - Chargement résultats génération
   - Statistiques descriptives

3. **Analysis**
   - Taux de précision des oracles (Precision, Recall, F1)
   - Analyse par type d'assertion (status, body, headers)
   - Distribution des scores de confiance
   - Faux positifs/négatifs détaillés

4. **Visualizations**
   - Confusion matrices
   - Courbes precision-recall
   - Distribution scores confiance
   - Heatmaps par type d'endpoint

5. **Statistical Tests**
   - Tests de significativité (t-test, chi-square)
   - Intervalles de confiance (95%)
   - Analyse variance (ANOVA)

6. **Conclusions**
   - Synthèse résultats
   - Réponse à RQ1
   - Limitations et biais

**Métriques Clés** :
- Oracle Precision, Recall, F1-Score
- Assertion Coverage (%)
- False Positive/Negative Rate
- Confidence Score Distribution

---

### 2. RQ2: Inconsistency Detection Study (`rq2_inconsistency_study.ipynb`)

**Question de Recherche** : *Les agents détectent-ils efficacement les incohérences dans les spécifications API ?*

**Sections du Notebook** :

1. **Introduction & Context**
   - Types d'incohérences (status, schema, semantic)
   - Approches de détection
   - Ground truth creation

2. **Data Loading**
   - Datasets avec incohérences injectées
   - Résultats détection agents
   - Annotations manuelles

3. **Analysis**
   - Taux de détection par type d'incohérence
   - Temps de détection
   - Faux positifs (hallucinations)
   - Impact sur qualité tests

4. **Visualizations**
   - Sankey diagrams (flow détection)
   - Radar charts (performance par type)
   - Timeline détection
   - Error analysis

5. **Statistical Tests**
   - McNemar test (comparaison agents)
   - Cohen's Kappa (agreement)
   - Wilcoxon signed-rank test

6. **Conclusions**
   - Efficacité détection
   - Types difficiles à détecter
   - Recommandations

**Métriques Clés** :
- Detection Rate (par type d'incohérence)
- False Positive Rate
- Detection Time (ms)
- Impact Score (sur qualité tests)

---

### 3. RQ3: Quality Evaluation (`rq3_quality_evaluation.ipynb`)

**Question de Recherche** : *Quelle est la qualité des tests de contrat générés automatiquement ?*

**Sections du Notebook** :

1. **Introduction & Context**
   - Définition qualité (correctness, completeness, maintainability)
   - Métriques qualité standard
   - Comparaison avec tests manuels

2. **Data Loading**
   - Tests générés (5 LLMs × 4 complétudes)
   - Tests manuels (baseline)
   - Métriques exécution

3. **Analysis**
   - Taux de passage tests
   - Couverture API (endpoints, status codes, schemas)
   - Complexité cyclomatic
   - Duplication code
   - Maintenabilité (SonarQube metrics)

4. **Visualizations**
   - Stacked bar charts (qualité par LLM)
   - Coverage maps
   - Complexity distribution
   - Quality spider charts

5. **Statistical Tests**
   - Kruskal-Wallis H-test (comparaison LLMs)
   - Dunn's post-hoc test
   - Effect size (Cohen's d)

6. **Conclusions**
   - LLM le plus performant
   - Trade-offs qualité/coût
   - Best practices identifiées

**Métriques Clés** :
- Test Pass Rate (%)
- API Coverage (%)
- Cyclomatic Complexity
- Code Duplication (%)
- Maintainability Index

---

### 4. RQ4: LLM Comparison (`rq4_llm_comparison.ipynb`)

**Question de Recherche** : *Quel LLM génère les meilleurs tests de contrat (qualité vs coût) ?*

**Sections du Notebook** :

1. **Introduction & Context**
   - LLMs évalués (GPT-4, Claude, Gemini, Mistral, LLaMA)
   - Critères comparaison
   - Trade-offs qualité/coût/vitesse

2. **Data Loading**
   - Résultats 5 LLMs
   - Coûts API calls
   - Temps génération
   - Métriques qualité

3. **Analysis**
   - Performance relative (normalized scores)
   - Coût par test généré
   - Vitesse génération
   - Stabilité/variance résultats
   - Pareto optimal (qualité vs coût)

4. **Visualizations**
   - Radar charts (5 dimensions qualité)
   - Scatter plots (coût vs qualité)
   - Box plots (variance)
   - Pareto frontiers
   - Heatmap correlation

5. **Statistical Tests**
   - Friedman test (comparaison appariée)
   - Nemenyi post-hoc
   - Kendall's W (concordance)

6. **Conclusions**
   - Classement LLMs
   - Recommandations usage
   - Future work

**Métriques Clés** :
- Quality Score (composite)
- Cost per Test ($)
- Generation Time (s)
- Stability (σ)
- Value Score (quality/cost)

---

### 5. RQ5: Completeness Impact (`rq5_completeness_impact.ipynb`)

**Question de Recherche** : *Comment le niveau de complétude de la documentation impacte la qualité des tests générés ?*

**Sections du Notebook** :

1. **Introduction & Context**
   - 4 niveaux complétude (100%, 75%, 50%, 25%)
   - Hypothèse dégradation linéaire
   - Seuil minimal utilisabilité

2. **Data Loading**
   - Datasets 4 complétudes
   - Résultats génération par niveau
   - Métriques qualité

3. **Analysis**
   - Dégradation qualité vs complétude
   - Régression linéaire/polynomiale
   - Identification seuil critique
   - Robustesse LLMs au manque info

4. **Visualizations**
   - Line plots (dégradation)
   - Regression curves
   - Threshold analysis
   - Resilience heatmap (LLMs vs complétude)

5. **Statistical Tests**
   - Linear regression (R², p-value)
   - ANOVA (effet complétude)
   - Piecewise regression (seuils)

6. **Conclusions**
   - Relation complétude-qualité
   - Seuil minimal (> 50% recommandé)
   - LLM le plus robuste

**Métriques Clés** :
- Quality Degradation Rate (%/decrease)
- Minimum Completeness Threshold
- Resilience Score (par LLM)
- R² (fit régression)

---

## Méthodologie d'Analyse

### 1. Approche Statistique

**Tests Paramétriques** (si normalité + homoscédasticité) :
- T-test (comparaison 2 groupes)
- ANOVA (comparaison > 2 groupes)
- Linear Regression

**Tests Non-Paramétriques** (sinon) :
- Mann-Whitney U (2 groupes)
- Kruskal-Wallis H (> 2 groupes)
- Spearman correlation

**Post-Hoc Tests** :
- Tukey HSD (after ANOVA)
- Dunn's test (after Kruskal-Wallis)
- Bonferroni correction

**Seuil de significativité** : α = 0.05

### 2. Visualisations Standards

**Distributions** :
- Histograms + KDE
- Box plots
- Violin plots

**Comparaisons** :
- Bar charts (grouped/stacked)
- Radar charts
- Heatmaps

**Relations** :
- Scatter plots + regression
- Correlation matrices
- Sankey diagrams

**Performance** :
- ROC curves
- Precision-Recall curves
- Confusion matrices

### 3. Export Résultats

**Formats Publication** :
```python
# Figures haute résolution
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
plt.savefig('figure.png', dpi=300, bbox_inches='tight')

# Tableaux LaTeX
df.to_latex('table.tex', index=False, escape=False)

# Données brutes
df.to_csv('results.csv', index=False)
```

---

## Visualisations et Métriques

### Palette de Couleurs

```python
# Color schemes (colorblind-friendly)
PALETTE_QUALITATIVE = sns.color_palette("colorblind", 8)
PALETTE_SEQUENTIAL = sns.color_palette("YlGnBu", 8)
PALETTE_DIVERGING = sns.color_palette("RdYlGn", 11)

# Custom palette for LLMs
LLM_COLORS = {
    'gpt-4': '#10a37f',
    'claude': '#c17c5a', 
    'gemini': '#4285f4',
    'mistral': '#f67320',
    'llama': '#654321'
}
```

### Style Matplotlib

```python
# Professional style
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
```

### Métriques Composites

**Quality Score** (RQ3, RQ4) :
```
Quality Score = 0.40 × Pass_Rate + 
                0.30 × Coverage + 
                0.20 × (1 - Complexity_norm) + 
                0.10 × Maintainability
```

**Value Score** (RQ4) :
```
Value Score = Quality_Score / log(Cost + 1)
```

**Resilience Score** (RQ5) :
```
Resilience = 1 - (Quality_drop / Completeness_drop)
```

---

## Implémentation

### Structure d'un Notebook Type

```python
# ====================
# NOTEBOOK HEADER
# ====================
"""
Title: RQX - [Question Title]
Author: Aurel IKAMA HONEY
Date: 12 December 2025
Purpose: [Brief description]
"""

# ====================
# 1. SETUP & IMPORTS
# ====================
import warnings
warnings.filterwarnings('ignore')

# Set seeds for reproducibility
np.random.seed(42)

# Imports...

# ====================
# 2. CONFIGURATION
# ====================
CONFIG = {
    'dataset_path': '../../experiments/datasets/',
    'results_path': './outputs/',
    'alpha': 0.05,  # Significance level
    'n_bootstrap': 1000
}

# ====================
# 3. DATA LOADING
# ====================
def load_datasets():
    """Load all required datasets"""
    # Implementation...
    return data

data = load_datasets()
print(f"Loaded {len(data)} samples")
data.head()

# ====================
# 4. EXPLORATORY ANALYSIS
# ====================
# Descriptive statistics
data.describe()

# Missing values
data.isnull().sum()

# Distributions
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# Plots...

# ====================
# 5. STATISTICAL TESTS
# ====================
def perform_hypothesis_test(group1, group2):
    """Perform appropriate statistical test"""
    # Normality test
    _, p1 = stats.shapiro(group1)
    _, p2 = stats.shapiro(group2)
    
    if p1 > 0.05 and p2 > 0.05:
        # Parametric
        stat, p = stats.ttest_ind(group1, group2)
        test = "t-test"
    else:
        # Non-parametric
        stat, p = stats.mannwhitneyu(group1, group2)
        test = "Mann-Whitney U"
    
    return {'test': test, 'statistic': stat, 'p_value': p}

# Run tests...

# ====================
# 6. VISUALIZATIONS
# ====================
def create_figure_1():
    """Main results figure"""
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plot...
    return fig

fig1 = create_figure_1()
plt.savefig(f"{CONFIG['results_path']}/figures/rqX_figure1.pdf", dpi=300)
plt.show()

# ====================
# 7. RESULTS SUMMARY
# ====================
results_summary = {
    'metric': [],
    'mean': [],
    'std': [],
    'ci_lower': [],
    'ci_upper': []
}

# Populate summary...

results_df = pd.DataFrame(results_summary)
results_df.to_latex(f"{CONFIG['results_path']}/tables/rqX_summary.tex")
results_df.to_csv(f"{CONFIG['results_path']}/tables/rqX_summary.csv")

display(results_df)

# ====================
# 8. CONCLUSIONS
# ====================
"""
## Key Findings

1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Statistical Significance

- Test X: p = 0.XXX (significant/not significant)
- Effect size: Cohen's d = X.XX (small/medium/large)

## Answer to RQX

[Direct answer to research question]

## Limitations

- [Limitation 1]
- [Limitation 2]
"""
```

### Utilitaires Communs (`notebooks/utils/`)

**plotting.py** :
```python
def plot_confusion_matrix(y_true, y_pred, labels=None, save_path=None):
    """Plot confusion matrix with nice formatting"""
    pass

def plot_regression_with_ci(x, y, ci=95, save_path=None):
    """Scatter plot with regression line and confidence interval"""
    pass

def plot_comparison_radar(data_dict, metrics, save_path=None):
    """Multi-dimensional radar chart for comparisons"""
    pass
```

**statistics.py** :
```python
def check_assumptions(data, test_type='parametric'):
    """Check statistical assumptions (normality, homoscedasticity)"""
    pass

def compute_effect_size(group1, group2, method='cohen_d'):
    """Compute effect size (Cohen's d, Glass's delta, etc.)"""
    pass

def bootstrap_ci(data, statistic=np.mean, n_bootstrap=1000, ci=95):
    """Compute bootstrap confidence interval"""
    pass
```

**data_loader.py** :
```python
class DatasetLoader:
    """Centralized dataset loading with caching"""
    
    def load_ground_truths(self, collection_name):
        pass
    
    def load_generated_tests(self, collection_name, llm, completeness):
        pass
    
    def load_validation_results(self, rq_number):
        pass
```

**export.py** :
```python
def export_figure(fig, name, formats=['pdf', 'png'], dpi=300):
    """Export figure in multiple formats"""
    pass

def export_table(df, name, formats=['latex', 'csv', 'markdown']):
    """Export table in multiple formats"""
    pass

def generate_markdown_report(results, template='default'):
    """Generate markdown report from results dict"""
    pass
```

---

## Intégration avec Phase 6.1 et 6.3

### Inputs depuis Phase 6.1

```python
# Ground truths
GT_PATH = 'experiments/datasets/ground_truths/'

# Datasets splits
TRAIN_PATH = 'experiments/datasets/splits/train/'
TEST_PATH = 'experiments/datasets/splits/test/'

# Validation reports
VALIDATION_PATH = 'experiments/datasets/validation/'
```

### Outputs vers Phase 6.3

```python
# Results for experimentation
RESULTS_PATH = 'experiments/results/'

# Figures for publication
FIGURES_PATH = 'experiments/notebooks/outputs/figures/'

# Tables for paper
TABLES_PATH = 'experiments/notebooks/outputs/tables/'
```

### Workflow Intégré

```
Phase 6.1 (Datasets)
    ↓
    ├─ Ground Truths → RQ1, RQ2 analysis
    ├─ Variants (4 levels) → RQ5 analysis
    └─ Train/Test splits → All RQs
    ↓
Phase 6.2 (Notebooks) ← VOUS ÊTES ICI
    ↓
    ├─ Statistical analyses
    ├─ Visualizations
    └─ Results summaries
    ↓
Phase 6.3 (Experiments)
    ↓
    ├─ Run 5 LLMs on test sets
    ├─ Collect metrics
    └─ Generate final paper results
```

---

## Planning Détaillé Phase 6.2

### Jour 1-2 : Setup & RQ1/RQ2 (12-13 Déc) ✅

- ✅ Créer structure notebooks
- ✅ Utilitaires communs
- ✅ RQ1 notebook (oracle analysis)
- ✅ RQ2 notebook (inconsistency study)

### Jour 3 : RQ3 Quality Evaluation (14 Déc) 🔄

- [ ] Notebook RQ3
- [ ] Métriques qualité
- [ ] Visualisations qualité

### Jour 4 : RQ4 LLM Comparison (15 Déc) 🔄

- [ ] Notebook RQ4
- [ ] Comparaison multi-dimensionnelle
- [ ] Pareto optimal

### Jour 5 : RQ5 Completeness Impact (16 Déc) 🔄

- [ ] Notebook RQ5
- [ ] Régression complétude-qualité
- [ ] Seuil minimal

### Jour 6 : Master Notebook (17 Déc) 🔄

- [ ] Notebook consolidé
- [ ] Export publication-ready
- [ ] Documentation

### Jour 7 : Review & Validation (18 Déc) 🔄

- [ ] Tests reproductibilité
- [ ] Revue peer
- [ ] Corrections finales

---

## Métriques de Succès Phase 6.2

| Critère | Cible | Status |
|---------|-------|--------|
| Notebooks créés | 6/6 | 🔄 2/6 |
| Exécution sans erreur | 100% | 🔄 En attente |
| Reproductibilité | 100% | 🔄 En attente |
| Tests statistiques | ≥ 3 par RQ | 🔄 En cours |
| Visualisations | ≥ 5 par RQ | 🔄 En cours |
| Documentation inline | 100% | 🔄 En cours |
| Export figures PDF | 100% | 🔄 En attente |
| Temps exécution | < 5 min/notebook | 🔄 En attente |

---

## Références

- [PHASE_6.1_DATASETS.md](PHASE_6.1_DATASETS.md) - Phase précédente
- [ACTION_PLAN.md](ACTION_PLAN.md) - Plan global du projet
- [Notebook Examples](../experiments/notebooks/) - Notebooks existants

---

**Document vivant** : Mis à jour au fur et à mesure de l'avancement de Phase 6.2

**Dernière mise à jour** : 12 Décembre 2025, 11:00 UTC
