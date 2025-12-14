# Datasets Phase 6.1 - Génération de Tests de Contrat

Ce dossier contient les datasets pour la validation expérimentale des questions de recherche RQ1 à RQ5.

## 📊 Vue d'ensemble

**46 endpoints d'APIs réelles** répartis sur **3 collections** avec **4 niveaux de complétude** = **12 datasets** + **splits train/test** + **oracles de validation**.

### Composition des Datasets

```
3 Collections API × 4 Niveaux de Complétude = 12 Datasets
├── JSONPlaceholder (30 endpoints CRUD)
├── ReqRes (7 endpoints utilisateurs + auth)
└── HTTPBin (9 endpoints tests HTTP)

Chaque dataset contient:
├── endpoints.json       → Liste des endpoints avec leur documentation
├── metadata.json        → Métadonnées (domaine, complétude, stats)
└── ground_truth.json    → Oracles de validation (règles attendues)
```

### Structure des Dossiers

```
experiments/datasets/
│
├── variants/                    # 12 datasets organisés par collection et complétude
│   ├── httpbin_testing_api/
│   │   ├── completeness_100/    # Documentation complète (100%)
│   │   ├── completeness_75/     # Documentation partielle (75%)
│   │   ├── completeness_50/     # Documentation minimale (50%)
│   │   └── completeness_25/     # Documentation très incomplète (25%)
│   ├── jsonplaceholder_rest_api/
│   │   └── [4 niveaux de complétude]
│   └── reqres_users_api/
│       └── [4 niveaux de complétude]
│
├── splits/                      # Séparation train/test (70/30)
│   └── default/
│       ├── train/               # 8 datasets pour l'entraînement
│       └── test/                # 4 datasets pour l'évaluation
│
├── ground_truths/               # Oracles de validation par collection
│   ├── httpbin_testing_api_gt_full.json
│   ├── jsonplaceholder_rest_api_gt_full.json
│   └── reqres_users_api_gt_full.json
│
├── validation/                  # Rapports de qualité des datasets
│   └── validation_report.html
│
└── exports/                     # Exports des métadonnées
    ├── datasets_catalog.json
    └── datasets_metadata.csv
```

---

## 🎯 Collections d'APIs

### 1. JSONPlaceholder REST API
**Source**: https://jsonplaceholder.typicode.com  
**Type**: API REST CRUD complète  
**Endpoints**: 30 (6 ressources × 5 opérations CRUD)  
**Authentification**: Aucune

| # | Méthode | Endpoint | Ressource | Opération |
|---|---------|----------|-----------|-----------|
| 1 | GET | `/posts` | Posts | Liste tous les posts |
| 2 | GET | `/posts/{id}` | Posts | Récupère un post par ID |
| 3 | POST | `/posts` | Posts | Crée un nouveau post |
| 4 | PUT | `/posts/{id}` | Posts | Modifie un post existant |
| 5 | DELETE | `/posts/{id}` | Posts | Supprime un post |
| 6 | GET | `/comments` | Comments | Liste tous les commentaires |
| 7 | GET | `/comments/{id}` | Comments | Récupère un commentaire par ID |
| 8 | POST | `/comments` | Comments | Crée un nouveau commentaire |
| 9 | PUT | `/comments/{id}` | Comments | Modifie un commentaire existant |
| 10 | DELETE | `/comments/{id}` | Comments | Supprime un commentaire |
| 11 | GET | `/albums` | Albums | Liste tous les albums |
| 12 | GET | `/albums/{id}` | Albums | Récupère un album par ID |
| 13 | POST | `/albums` | Albums | Crée un nouveau album |
| 14 | PUT | `/albums/{id}` | Albums | Modifie un album existant |
| 15 | DELETE | `/albums/{id}` | Albums | Supprime un album |
| 16 | GET | `/photos` | Photos | Liste toutes les photos |
| 17 | GET | `/photos/{id}` | Photos | Récupère une photo par ID |
| 18 | POST | `/photos` | Photos | Crée une nouvelle photo |
| 19 | PUT | `/photos/{id}` | Photos | Modifie une photo existante |
| 20 | DELETE | `/photos/{id}` | Photos | Supprime une photo |
| 21 | GET | `/todos` | Todos | Liste toutes les tâches |
| 22 | GET | `/todos/{id}` | Todos | Récupère une tâche par ID |
| 23 | POST | `/todos` | Todos | Crée une nouvelle tâche |
| 24 | PUT | `/todos/{id}` | Todos | Modifie une tâche existante |
| 25 | DELETE | `/todos/{id}` | Todos | Supprime une tâche |
| 26 | GET | `/users` | Users | Liste tous les utilisateurs |
| 27 | GET | `/users/{id}` | Users | Récupère un utilisateur par ID |
| 28 | POST | `/users` | Users | Crée un nouvel utilisateur |
| 29 | PUT | `/users/{id}` | Users | Modifie un utilisateur existant |
| 30 | DELETE | `/users/{id}` | Users | Supprime un utilisateur |

**Domaines couverts**: `user_management`, `content_management`, `rest_crud`

---

### 2. ReqRes Users API
**Source**: https://reqres.in/api  
**Type**: API utilisateurs avec authentification  
**Endpoints**: 7  
**Authentification**: Token-based

| # | Méthode | Endpoint | Description |
|---|---------|----------|-------------|
| 1 | GET | `/users` | Liste les utilisateurs (avec pagination) |
| 2 | GET | `/users/{id}` | Récupère un utilisateur spécifique |
| 3 | POST | `/users` | Crée un nouvel utilisateur |
| 4 | PUT | `/users/{id}` | Met à jour un utilisateur |
| 5 | DELETE | `/users/{id}` | Supprime un utilisateur |
| 6 | POST | `/register` | Enregistre un nouvel utilisateur |
| 7 | POST | `/login` | Authentifie un utilisateur |

**Domaines couverts**: `user_management`, `authentication`, `rest_crud`

---

### 3. HTTPBin Testing API
**Source**: https://httpbin.org  
**Type**: API de tests HTTP  
**Endpoints**: 9  
**Authentification**: Basic Auth (pour tests)

| # | Méthode | Endpoint | Description |
|---|---------|----------|-------------|
| 1 | GET | `/get` | Retourne les données de la requête GET |
| 2 | POST | `/post` | Retourne les données de la requête POST |
| 3 | GET | `/status/200` | Retourne le code HTTP 200 (succès) |
| 4 | GET | `/status/400` | Retourne le code HTTP 400 (erreur client) |
| 5 | GET | `/status/404` | Retourne le code HTTP 404 (non trouvé) |
| 6 | GET | `/status/500` | Retourne le code HTTP 500 (erreur serveur) |
| 7 | GET | `/headers` | Retourne les en-têtes de la requête |
| 8 | GET | `/delay/{n}` | Répond après un délai de n secondes |
| 9 | GET | `/basic-auth/{user}/{pass}` | Teste l'authentification basique |

**Domaines couverts**: `authentication`, `user_management`, `content_management`, `rest_crud`

---

## 📐 Niveaux de Complétude

Les 4 niveaux simulent différentes qualités de documentation d'API :

### 🟢 Niveau 100% - Documentation Complète
**Contenu**:
- ✅ Tous les endpoints documentés
- ✅ Schémas complets requête/réponse
- ✅ Exemples pour toutes les opérations
- ✅ Tous les codes HTTP (200, 400, 404, 500, etc.)
- ✅ Tous les headers (requis et optionnels)
- ✅ Règles de validation
- ✅ Documentation des cas d'erreur

**Cas d'usage**: Baseline pour les comparaisons

### 🟡 Niveau 75% - Documentation Partielle
**Contenu**:
- ✅ Tous les endpoints documentés
- ✅ Schémas partiels (75% complets)
- ⚠️ Exemples limités (50%)
- ⚠️ Codes HTTP principaux uniquement (200, 400, 500)
- ⚠️ Headers critiques seulement
- ❌ Quelques règles de validation manquantes (25%)
- ❌ Documentation d'erreurs incomplète

**Cas d'usage**: Simule une "bonne documentation mais incomplète"

### 🟠 Niveau 50% - Documentation Minimale
**Contenu**:
- ✅ Tous les endpoints listés
- ⚠️ Schémas basiques (types uniquement)
- ❌ Pas d'exemples
- ⚠️ Code de succès uniquement (200)
- ⚠️ Header Content-Type seulement
- ❌ Pas de règles de validation
- ❌ Pas de documentation d'erreurs

**Cas d'usage**: Simule une documentation "minimale acceptable"

### 🔴 Niveau 25% - Documentation Très Incomplète
**Contenu**:
- ✅ Liste des endpoints avec méthodes HTTP
- ❌ Pas de schémas détaillés
- ❌ Pas d'exemples
- ❌ Pas de codes HTTP
- ❌ Pas de headers
- ❌ Pas de validation
- ❌ Pas de documentation d'erreurs

**Cas d'usage**: Simule une documentation "pauvre ou obsolète"

---

## 🎓 Oracles de Validation (Ground Truth)

Les oracles sont créés via :

1. **Annotation Automatique**: Appels réels aux APIs pour collecter les réponses
2. **Inférence de Schémas**: Extraction automatique des schémas JSON
3. **Validation Manuelle**: Révision et amélioration par des experts (quand disponible)

**Structure d'un Oracle**:

```json
{
  "endpoint_id": "uuid",
  "status_code": 200,
  "required_headers": {
    "Content-Type": "application/json"
  },
  "optional_headers": {
    "X-RateLimit-Remaining": "integer"
  },
  "response_schema": {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
      "id": {"type": "integer"},
      "name": {"type": "string"}
    }
  },
  "business_rules": [
    "L'ID doit être un entier positif",
    "Le nom ne peut pas être vide"
  ],
  "source": "auto|manual|consensus",
  "confidence": 0.95,
  "annotator": "expert|auto"
}
```

**Fichiers d'oracles**:
- `httpbin_testing_api_gt_full.json` (9 oracles)
- `jsonplaceholder_rest_api_gt_full.json` (30 oracles)
- `reqres_users_api_gt_full.json` (7 oracles)

---

## 📊 Splits Train/Test

**Configuration**:
- **Train**: 70% (8 datasets)
- **Test**: 30% (4 datasets)
- **Stratification**: Par domaine, niveau de complétude, complexité
- **Seed aléatoire**: 42 (pour reproductibilité)

**Critères de validation**:
- ✅ Pas de fuite de données (samples uniques)
- ✅ Distribution équilibrée entre strates
- ✅ Minimum d'échantillons par strate (train: 2, test: 1)

**Distribution**:

| Collection | Complétude | Train | Test |
|------------|------------|-------|------|
| HTTPBin | 100% | ✓ | |
| HTTPBin | 75% | ✓ | |
| HTTPBin | 50% | | ✓ |
| HTTPBin | 25% | ✓ | |
| JSONPlaceholder | 100% | ✓ | |
| JSONPlaceholder | 75% | | ✓ |
| JSONPlaceholder | 50% | ✓ | |
| JSONPlaceholder | 25% | ✓ | |
| ReqRes | 100% | | ✓ |
| ReqRes | 75% | ✓ | |
| ReqRes | 50% | | ✓ |
| ReqRes | 25% | ✓ | |

---

## ✅ Métriques de Qualité

### Seuils de Qualité des Datasets

| Métrique | Seuil | Description |
|----------|-------|-------------|
| Complétude | ≥ 90% | % des champs annotés |
| Cohérence | ≥ 85% | Cohérence inter-variants |
| Confiance | ≥ 80% | Confiance des oracles |
| Couverture | 100% | % d'endpoints avec oracles |

### Validations Effectuées

1. **Métadonnées**: Tous les champs requis présents
2. **Endpoints**: Structure valide et méthodes HTTP correctes
3. **Schémas**: Cohérence des schémas entre variants
4. **Oracles**: Annotations de haute confiance
5. **Splits**: Stratification correcte sans fuite

---

## 🚀 Utilisation

### 1. Charger un Dataset

```python
import json
from pathlib import Path

# Charger le variant 75% de complétude
dataset_path = Path("experiments/datasets/variants/jsonplaceholder_rest_api/completeness_75")

with open(dataset_path / "endpoints.json", 'r') as f:
    endpoints = json.load(f)

with open(dataset_path / "ground_truth.json", 'r') as f:
    ground_truths = json.load(f)

with open(dataset_path / "metadata.json", 'r') as f:
    metadata = json.load(f)

print(f"Collection: {metadata['collection']}")
print(f"Endpoints: {len(endpoints['endpoints'])}")
print(f"Complétude: {metadata['completeness_level']*100}%")
```

### 2. Accéder aux Splits Train/Test

```python
# Charger les échantillons d'entraînement
with open("experiments/datasets/splits/default/train/samples_index.json", 'r') as f:
    train_samples = json.load(f)

# Charger les échantillons de test
with open("experiments/datasets/splits/default/test/samples_index.json", 'r') as f:
    test_samples = json.load(f)

print(f"Train: {len(train_samples['samples'])} datasets")
print(f"Test: {len(test_samples['samples'])} datasets")
```

### 3. Exécuter le Workflow Complet

```bash
# Workflow complet (crawl + création + split + validation)
python scripts/run_phase_6.1.py --mode full

# Workflow rapide (utilise les collections existantes)
python scripts/run_phase_6.1.py --mode quick
```

### 4. Valider les Datasets

```python
from experiments.dataset_validator import DatasetValidator

validator = DatasetValidator()
reports = validator.validate_all_datasets(generate_report=True)

# Vérifier le rapport de validation
passed = sum(1 for r in reports.values() if r.passed)
print(f"Validation: {passed}/{len(reports)} datasets passés")

# Voir le rapport HTML
print("Rapport: experiments/datasets/validation/validation_report.html")
```

### 5. Exporter les Datasets

```python
from experiments.dataset_exporter import DatasetExporter

exporter = DatasetExporter()

# Générer le catalogue
catalog_path = exporter.generate_catalog()
print(f"Catalogue: {catalog_path}")

# Exporter les métadonnées en CSV
csv_path = exporter.export_metadata_to_csv()
print(f"CSV: {csv_path}")

# Exporter tout en ZIP
zip_path = exporter.export_all_to_zip()
print(f"Archive: {zip_path}")
```

---

## 🔬 Intégration avec les Questions de Recherche

### RQ1: Précision des Oracles

**Objectif**: Évaluer la précision des oracles générés automatiquement

```python
from experiments.rq1_orchestrator import RQ1Orchestrator

orchestrator = RQ1Orchestrator()
results = orchestrator.run_experiment(
    train_set="experiments/datasets/splits/default/train",
    test_set="experiments/datasets/splits/default/test"
)

# Métriques: Précision, Rappel, F1-score des oracles
```

**Datasets utilisés**: Tous les niveaux de complétude (100%, 75%, 50%, 25%)

---

### RQ2: Détection des Inconsistances

**Objectif**: Mesurer la capacité à détecter les inconsistances oracle-code

```python
from experiments.rq2_orchestrator import RQ2Orchestrator

orchestrator = RQ2Orchestrator()
results = orchestrator.run_experiment(
    test_set="experiments/datasets/splits/default/test"
)

# Métriques: Taux de détection, Faux positifs, Faux négatifs
```

**Datasets utilisés**: Variants avec inconsistances injectées

---

### RQ3: Qualité du Code

**Objectif**: Évaluer la qualité du code généré

```python
from experiments.rq345_orchestrator import RQ345Orchestrator

orchestrator = RQ345Orchestrator()
results = orchestrator.run_rq3_experiment(
    test_set="experiments/datasets/splits/default/test"
)

# Métriques: Maintenabilité, Complexité cyclomatique, Duplication
```

**Datasets utilisés**: Tous les niveaux de complétude

---

### RQ4: Comparaison des LLMs

**Objectif**: Comparer 5 LLMs (GPT-4, Claude, Gemini, Mistral, Llama)

```python
results = orchestrator.run_rq4_experiment(
    test_set="experiments/datasets/splits/default/test",
    llms=["gpt-4", "claude-3", "gemini-pro", "mistral-large", "llama-3.1"]
)

# Métriques: Performance, Précision, Temps, Coût
```

**Datasets utilisés**: Ensemble de test (4 datasets)

---

### RQ5: Impact de la Complétude

**Objectif**: Analyser l'impact de la complétude sur la performance

```python
results = orchestrator.run_rq5_experiment(
    datasets_by_completeness={
        100: [...],  # Datasets 100%
        75: [...],   # Datasets 75%
        50: [...],   # Datasets 50%
        25: [...]    # Datasets 25%
    }
)

# Métriques: Corrélation complétude-performance
```

**Datasets utilisés**: 3 collections × 4 niveaux = 12 comparaisons

---

## 📈 Résumé des Datasets

| Métrique | Valeur |
|----------|--------|
| **Collections** | 3 (JSONPlaceholder, ReqRes, HTTPBin) |
| **Endpoints totaux** | 46 |
| **Niveaux de complétude** | 4 (100%, 75%, 50%, 25%) |
| **Datasets (variants)** | 12 |
| **Oracles** | 46 (1 par endpoint) |
| **Train samples** | 8 datasets (70%) |
| **Test samples** | 4 datasets (30%) |
| **Validation** | 100% réussite |
| **Domaines** | 4 (auth, user_mgmt, content_mgmt, rest_crud) |

---

## 🛠️ Maintenance

### Ajouter une Nouvelle Collection

1. Créer le crawler dans `experiments/collection_crawler.py`
2. Générer la collection Bruno
3. Exécuter `python scripts/run_phase_6.1.py --mode full`

### Modifier les Niveaux de Complétude

Éditer `experiments/create_datasets.py`:
- Méthode `_reduce_completeness()`
- Ajuster les seuils de dégradation

### Régénérer les Datasets

```bash
# Nettoyer et régénérer
rm -rf experiments/datasets/variants experiments/datasets/splits
python scripts/run_phase_6.1.py --mode full
```

---

## 📝 Références

- **Bruno Collections**: https://www.usebruno.com/
- **JSONPlaceholder**: https://jsonplaceholder.typicode.com/
- **ReqRes**: https://reqres.in/
- **HTTPBin**: https://httpbin.org/
- **Documentation Projet**: `docs/PHASE_6.1_DATASETS.md`

---

**Dernière mise à jour**: 12 décembre 2025  
**Version**: Phase 6.1 - Datasets complets et validés
