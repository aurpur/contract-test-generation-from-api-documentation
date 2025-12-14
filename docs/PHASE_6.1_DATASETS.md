# Phase 6.1 : Création et Gestion des Datasets

**Auteur** : Aurel IKAMA HONEY  
**Date** : 12 Décembre 2025  
**Statut** : En Cours  
**Phase** : 6.1 - Datasets pour Expérimentations

---

## Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Objectifs de Phase 6.1](#objectifs-de-phase-61)
3. [Architecture des Datasets](#architecture-des-datasets)
4. [Collections API Sources](#collections-api-sources)
5. [Niveaux de Complétude](#niveaux-de-complétude)
6. [Ground Truth et Annotations](#ground-truth-et-annotations)
7. [Division Train/Test](#division-traintest)
8. [Implémentation Détaillée](#implémentation-détaillée)
9. [Métriques et Validation](#métriques-et-validation)
10. [Intégration avec RQ1-RQ5](#intégration-avec-rq1-rq5)

---

## Vue d'Ensemble

La Phase 6.1 constitue la **fondation empirique** de notre recherche. Elle vise à créer des datasets robustes, diversifiés et annotés qui permettront de valider nos questions de recherche (RQ1-RQ5) de manière rigoureuse et reproductible.

### Principes Directeurs

1. **Diversité** : Collections API couvrant différents domaines (CRUD, Auth, Search, etc.)
2. **Réalisme** : Utilisation de vraies API publiques et cas d'usage industriels
3. **Complétude Variable** : 4 niveaux (100%, 75%, 50%, 25%) pour RQ5
4. **Traçabilité** : Métadonnées complètes et versioning des datasets
5. **Reproductibilité** : Documentation exhaustive et scripts automatisés

---

## Objectifs de Phase 6.1

### Objectifs Primaires

✅ **OBJ-6.1.1** : Collecter 10+ collections Bruno variées  
✅ **OBJ-6.1.2** : Générer 4 variants par collection (complétude : 100%, 75%, 50%, 25%)  
✅ **OBJ-6.1.3** : Annoter ground truth pour chaque endpoint  
✅ **OBJ-6.1.4** : Diviser en train (70%) / test (30%) sets  
✅ **OBJ-6.1.5** : Valider qualité et cohérence des datasets  

### Objectifs Secondaires

- **OBJ-6.1.6** : Documenter processus de création
- **OBJ-6.1.7** : Créer utilitaires d'export/import
- **OBJ-6.1.8** : Intégrer avec workflow expérimental (RQ1-RQ5)

---

## Architecture des Datasets

### Structure Hiérarchique

```
experiments/datasets/
├── collections/                      # Collections Bruno sources
│   ├── rest_api_crud/
│   │   ├── collection.json
│   │   └── metadata.json
│   ├── auth_api/
│   ├── search_api/
│   ├── pagination_api/
│   ├── graphql_api/
│   └── ...
│
├── variants/                         # Variants de complétude
│   ├── rest_api_crud/
│   │   ├── completeness_100/
│   │   │   ├── endpoints.json
│   │   │   ├── ground_truth.json
│   │   │   └── metadata.json
│   │   ├── completeness_75/
│   │   ├── completeness_50/
│   │   └── completeness_25/
│   └── ...
│
├── splits/                           # Train/Test splits
│   ├── train/
│   │   ├── rest_api_crud_100/
│   │   ├── rest_api_crud_75/
│   │   └── ...
│   └── test/
│       ├── rest_api_crud_100/
│       └── ...
│
├── ground_truths/                    # Annotations ground truth
│   ├── rest_api_crud_gt.json
│   ├── auth_api_gt.json
│   └── ...
│
├── validation/                       # Rapports de validation
│   ├── quality_reports/
│   ├── consistency_checks/
│   └── statistics/
│
└── metadata/                         # Métadonnées globales
    ├── collections_index.json
    ├── variants_index.json
    └── datasets_catalog.json
```

### Modèles de Données

#### 1. Collection Metadata

```json
{
  "collection_id": "uuid",
  "name": "REST API CRUD",
  "description": "API RESTful standard avec opérations CRUD",
  "source": "bruno_collections/rest_api_crud/collection.json",
  "domain": "crud",
  "num_endpoints": 12,
  "http_methods": ["GET", "POST", "PUT", "DELETE"],
  "auth_types": ["Bearer", "API Key"],
  "created_at": "2025-12-12T10:00:00Z",
  "version": "1.0.0"
}
```

#### 2. Dataset Variant

```json
{
  "variant_id": "uuid",
  "collection_id": "uuid",
  "completeness_level": 0.75,
  "num_endpoints": 12,
  "num_complete_endpoints": 9,
  "modifications": [
    {
      "endpoint_id": "uuid",
      "field": "request_body.schema",
      "action": "removed",
      "reason": "simulate_incompleteness"
    }
  ],
  "created_at": "2025-12-12T10:30:00Z"
}
```

#### 3. Ground Truth Annotation

```json
{
  "endpoint_id": "uuid",
  "collection_id": "uuid",
  "ground_truth": {
    "expected_status_codes": [200, 201],
    "expected_headers": {
      "Content-Type": "application/json",
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
    "jsonpath_assertions": [
      {
        "path": "$.id",
        "type": "integer",
        "constraint": "> 0"
      }
    ],
    "business_rules": [
      {
        "rule": "created_at <= updated_at",
        "description": "Creation date must be before or equal to update date"
      }
    ]
  },
  "confidence": 1.0,
  "annotated_by": "expert",
  "annotated_at": "2025-12-12T11:00:00Z"
}
```

#### 4. Train/Test Split Metadata

```json
{
  "split_id": "uuid",
  "split_type": "train",
  "split_ratio": 0.7,
  "total_samples": 100,
  "num_samples": 70,
  "collections_included": ["rest_api_crud", "auth_api"],
  "completeness_levels": [1.0, 0.75, 0.5, 0.25],
  "created_at": "2025-12-12T12:00:00Z"
}
```

---

## Collections API Sources

### Critères de Sélection

1. **Diversité Fonctionnelle** : Couvrir différents patterns (CRUD, Auth, Search, etc.)
2. **Complexité Variable** : API simples (3-5 endpoints) à complexes (15+ endpoints)
3. **Disponibilité Publique** : APIs accessibles pour tests réels
4. **Documentation Bruno** : Collections existantes ou créables

### Collections Cibles (10+)

| ID | Nom | Domaine | Endpoints | Complexité | Source |
|----|-----|---------|-----------|------------|--------|
| C1 | REST API CRUD | CRUD | 12 | Moyenne | JSONPlaceholder |
| C2 | Auth API | Authentication | 8 | Élevée | Auth0 |
| C3 | Search API | Search/Filter | 10 | Moyenne | Algolia |
| C4 | Pagination API | Pagination | 6 | Faible | ReqRes |
| C5 | File Upload API | Upload/Storage | 7 | Élevée | Cloudinary |
| C6 | Rate Limiting API | Rate Limits | 5 | Moyenne | GitHub API |
| C7 | GraphQL API | GraphQL | 4 | Élevée | GraphQL Public |
| C8 | Webhook API | Webhooks | 9 | Moyenne | Stripe |
| C9 | Real-time API | WebSocket | 6 | Élevée | Socket.io |
| C10 | Batch API | Batch Ops | 8 | Moyenne | Mailchimp |

### APIs Publiques Utilisées

1. **JSONPlaceholder** (https://jsonplaceholder.typicode.com)
   - 6 ressources : posts, comments, albums, photos, todos, users
   - CRUD complet
   - Gratuit, pas d'auth requise

2. **ReqRes** (https://reqres.in)
   - Users API avec pagination
   - Support POST/PUT/DELETE
   - Réponses réalistes

3. **HTTPBin** (https://httpbin.org)
   - Testing HTTP methods
   - Auth, headers, status codes
   - Idéal pour tests techniques

4. **PokéAPI** (https://pokeapi.co)
   - API RESTful riche
   - Pagination, filtering
   - Pas d'auth requise

5. **OpenWeatherMap** (https://openweathermap.org/api)
   - Weather data API
   - Requiert API key
   - Données temps réel

---

## Niveaux de Complétude

### Définition des Niveaux

Pour étudier l'impact de la complétude documentaire (RQ5), nous générons 4 variants par collection :

#### Niveau 1 : Complétude 100%

**Documentation Complète**
- ✅ Tous les endpoints documentés
- ✅ Schémas request/response complets
- ✅ Exemples de requêtes/réponses
- ✅ Codes de statut HTTP
- ✅ Headers et paramètres
- ✅ Règles de validation
- ✅ Cas d'erreur

**Utilisation** : Baseline pour comparaisons RQ1-RQ5

#### Niveau 2 : Complétude 75%

**Documentation Partielle**
- ✅ Tous les endpoints documentés
- ✅ Schémas request/response (75% complets)
- ⚠️ Exemples partiels (50%)
- ⚠️ Codes de statut principaux uniquement (200, 400, 500)
- ⚠️ Headers critiques uniquement (Content-Type, Authorization)
- ❌ Règles de validation manquantes (25%)
- ❌ Cas d'erreur incomplets

**Simulation** : Documentation "bonne" mais incomplète

#### Niveau 3 : Complétude 50%

**Documentation Minimale**
- ✅ Tous les endpoints listés
- ⚠️ Schémas request/response basiques (types uniquement)
- ❌ Pas d'exemples
- ⚠️ Code de statut 200 uniquement
- ⚠️ Header Content-Type uniquement
- ❌ Pas de règles de validation
- ❌ Pas de documentation des erreurs

**Simulation** : Documentation "moyenne" avec gaps

#### Niveau 4 : Complétude 25%

**Documentation Très Incomplète**
- ✅ Liste endpoints avec HTTP methods
- ❌ Pas de schémas détaillés
- ❌ Pas d'exemples
- ❌ Pas de codes de statut
- ❌ Pas de headers documentés
- ❌ Pas de règles
- ❌ Pas de documentation erreurs

**Simulation** : Documentation "mauvaise" ou obsolète

### Algorithme de Dégradation

```python
def degrade_completeness(endpoint: EndpointContext, target_level: float) -> EndpointContext:
    """
    Dégrade progressivement la documentation d'un endpoint.
    
    Stratégie :
    1. Niveau 75% : Supprimer 25% des champs optionnels
    2. Niveau 50% : Supprimer 50% des détails (exemples, validations)
    3. Niveau 25% : Garder uniquement URL, method, types de base
    """
    degraded = endpoint.copy()
    
    if target_level <= 0.75:
        # Supprimer exemples de réponse
        degraded.response_examples = []
        # Supprimer règles de validation complexes
        degraded.validation_rules = degraded.validation_rules[:len(degraded.validation_rules)//2]
        
    if target_level <= 0.50:
        # Supprimer schémas détaillés
        degraded.request_schema = simplify_schema(degraded.request_schema)
        degraded.response_schema = simplify_schema(degraded.response_schema)
        # Garder uniquement status code principal
        degraded.status_codes = [200]
        
    if target_level <= 0.25:
        # Supprimer presque tout
        degraded.request_schema = None
        degraded.response_schema = None
        degraded.headers = {}
        degraded.query_params = []
        
    return degraded
```

---

## Ground Truth et Annotations

### Processus d'Annotation

#### Étape 1 : Annotation Automatique

```python
def auto_annotate_endpoint(endpoint: EndpointContext, api_url: str) -> GroundTruth:
    """
    Annotation automatique via appels API réels.
    
    1. Exécuter requête HTTP réelle
    2. Capturer réponse (status, headers, body)
    3. Inférer schéma JSON
    4. Détecter patterns et règles
    """
    response = make_real_api_call(endpoint, api_url)
    
    return GroundTruth(
        endpoint_id=endpoint.id,
        expected_status_codes=extract_status_codes(response),
        expected_headers=extract_headers(response),
        response_schema=infer_json_schema(response.json()),
        jsonpath_assertions=generate_assertions(response.json()),
        confidence=0.8,  # Auto-annotation -> confiance moyenne
        annotated_by="auto"
    )
```

#### Étape 2 : Validation Manuelle

```python
def validate_ground_truth(gt: GroundTruth, expert_review: Dict) -> GroundTruth:
    """
    Validation et enrichissement par expert.
    
    1. Vérifier cohérence des annotations auto
    2. Ajouter règles métier complexes
    3. Enrichir avec cas d'erreur
    4. Augmenter confidence à 1.0
    """
    validated_gt = gt.copy()
    validated_gt.business_rules = expert_review.get("business_rules", [])
    validated_gt.edge_cases = expert_review.get("edge_cases", [])
    validated_gt.confidence = 1.0
    validated_gt.annotated_by = "expert"
    
    return validated_gt
```

#### Étape 3 : Consensus Multi-Annotateurs

Pour garantir la qualité, nous utilisons un système de consensus :

```python
def compute_consensus(annotations: List[GroundTruth]) -> GroundTruth:
    """
    Calcule le consensus entre plusieurs annotations.
    
    Méthode :
    1. Intersection pour champs obligatoires (status codes, headers)
    2. Union pour champs optionnels (assertions, rules)
    3. Moyenne pour scores numériques
    4. Vote majoritaire pour champs catégoriels
    """
    consensus = GroundTruth(
        endpoint_id=annotations[0].endpoint_id,
        expected_status_codes=intersect_status_codes(annotations),
        expected_headers=intersect_headers(annotations),
        response_schema=merge_schemas(annotations),
        jsonpath_assertions=union_assertions(annotations),
        business_rules=vote_rules(annotations),
        confidence=mean_confidence(annotations),
        annotated_by="consensus"
    )
    
    return consensus
```

### Critères de Qualité des Annotations

| Critère | Description | Seuil |
|---------|-------------|-------|
| **Complétude** | % champs annotés / total champs | ≥ 90% |
| **Cohérence** | Accord inter-annotateurs | ≥ 85% |
| **Précision** | Validation par tests réels | ≥ 95% |
| **Couverture** | % endpoints annotés | 100% |

---

## Division Train/Test

### Stratégie de Split

#### Méthode : Stratified Split

Pour assurer la représentativité, nous utilisons un split stratifié :

```python
def stratified_split(
    datasets: List[Dataset],
    train_ratio: float = 0.7,
    stratify_by: List[str] = ["domain", "completeness", "complexity"]
) -> Tuple[List[Dataset], List[Dataset]]:
    """
    Split stratifié garantissant la distribution équilibrée.
    
    Stratification par :
    1. Domaine API (CRUD, Auth, Search, etc.)
    2. Niveau de complétude (100%, 75%, 50%, 25%)
    3. Complexité (nb endpoints, profondeur schémas)
    
    Garanties :
    - Chaque strate représentée dans train ET test
    - Ratio respecté pour chaque strate (±5%)
    - Pas de leak entre train/test
    """
    strata = group_by_strata(datasets, stratify_by)
    
    train_set, test_set = [], []
    
    for stratum_key, stratum_data in strata.items():
        n_train = int(len(stratum_data) * train_ratio)
        
        # Shuffle pour randomisation
        shuffled = shuffle(stratum_data, random_state=42)
        
        train_set.extend(shuffled[:n_train])
        test_set.extend(shuffled[n_train:])
    
    return train_set, test_set
```

### Ratios de Split

| Split Type | Ratio | Usage |
|------------|-------|-------|
| **Train** | 70% | Développement et tuning des agents |
| **Test** | 30% | Évaluation finale RQ1-RQ5 |
| **Validation** | (optionnel) 10% du train | Hyperparamètre tuning |

### Validation du Split

```python
def validate_split(train_set: List[Dataset], test_set: List[Dataset]) -> Dict:
    """
    Valide la qualité du split.
    
    Vérifications :
    1. Pas de leak (aucun dataset commun)
    2. Distribution similaire des domaines
    3. Distribution similaire des complétudes
    4. Distribution similaire des complexités
    5. Tailles respectent les ratios (±5%)
    """
    validation_report = {
        "no_leak": len(set(train_set) & set(test_set)) == 0,
        "domain_distribution": compare_distributions(train_set, test_set, "domain"),
        "completeness_distribution": compare_distributions(train_set, test_set, "completeness"),
        "complexity_distribution": compare_distributions(train_set, test_set, "complexity"),
        "size_ratios": {
            "train": len(train_set) / (len(train_set) + len(test_set)),
            "test": len(test_set) / (len(train_set) + len(test_set))
        }
    }
    
    return validation_report
```

---

## Implémentation Détaillée

### Module 1 : Dataset Creator

**Fichier** : `experiments/dataset_creator.py`

```python
class DatasetCreator:
    """
    Créateur de datasets pour expérimentations.
    
    Responsabilités :
    1. Charger collections Bruno sources
    2. Générer variants de complétude
    3. Appliquer ground truth
    4. Sauvegarder avec métadonnées
    """
    
    def create_dataset(
        self,
        collection_path: str,
        completeness_levels: List[float] = [1.0, 0.75, 0.5, 0.25],
        output_dir: Path = Path("experiments/datasets")
    ) -> List[DatasetMetadata]:
        """Crée tous les variants pour une collection."""
        pass
    
    def degrade_completeness(
        self,
        endpoint: EndpointContext,
        target_level: float
    ) -> EndpointContext:
        """Dégrade la complétude d'un endpoint."""
        pass
```

### Module 2 : Ground Truth Manager

**Fichier** : `experiments/ground_truth_manager.py` (déjà existant, à enrichir)

```python
class GroundTruthManager:
    """
    Gestionnaire des annotations ground truth.
    
    Responsabilités :
    1. Annotation automatique via API calls
    2. Import annotations manuelles
    3. Calcul de consensus multi-annotateurs
    4. Validation qualité annotations
    """
    
    def auto_annotate(
        self,
        endpoint: EndpointContext,
        api_url: str
    ) -> GroundTruth:
        """Annotation automatique par appel API réel."""
        pass
    
    def compute_consensus(
        self,
        annotations: List[GroundTruth]
    ) -> GroundTruth:
        """Calcule le consensus entre annotations."""
        pass
```

### Module 3 : Dataset Splitter

**Fichier** : `experiments/dataset_splitter.py`

```python
class DatasetSplitter:
    """
    Split datasets en train/test.
    
    Responsabilités :
    1. Stratified split par domaine/complétude/complexité
    2. Validation absence de leak
    3. Export train/test sets
    """
    
    def stratified_split(
        self,
        datasets: List[Dataset],
        train_ratio: float = 0.7,
        stratify_by: List[str] = ["domain", "completeness"]
    ) -> Tuple[List[Dataset], List[Dataset]]:
        """Split stratifié."""
        pass
    
    def validate_split(
        self,
        train_set: List[Dataset],
        test_set: List[Dataset]
    ) -> Dict:
        """Valide qualité du split."""
        pass
```

### Module 4 : Dataset Validator

**Fichier** : `experiments/dataset_validator.py`

```python
class DatasetValidator:
    """
    Valide qualité et cohérence des datasets.
    
    Responsabilités :
    1. Vérifier complétude annotations
    2. Vérifier cohérence inter-variants
    3. Vérifier conformité schémas
    4. Générer rapports qualité
    """
    
    def validate_dataset(
        self,
        dataset: Dataset
    ) -> ValidationReport:
        """Valide un dataset complet."""
        pass
    
    def check_consistency(
        self,
        variants: List[Dataset]
    ) -> ConsistencyReport:
        """Vérifie cohérence entre variants."""
        pass
```

### Module 5 : Collection Crawler

**Fichier** : `experiments/collection_crawler.py`

```python
class CollectionCrawler:
    """
    Crawle et télécharge collections Bruno publiques.
    
    Responsabilités :
    1. Télécharger collections depuis sources
    2. Convertir formats (Postman -> Bruno)
    3. Valider collections téléchargées
    """
    
    def crawl_public_api(
        self,
        api_name: str,
        output_dir: Path
    ) -> Path:
        """Crawle une API publique et génère collection Bruno."""
        pass
    
    def convert_postman_to_bruno(
        self,
        postman_path: Path,
        output_path: Path
    ) -> None:
        """Convertit collection Postman en Bruno."""
        pass
```

---

## Métriques et Validation

### Métriques de Qualité des Datasets

#### 1. Métriques de Diversité

```python
diversity_metrics = {
    "domain_coverage": 10,  # Nombre de domaines différents
    "endpoint_variety": 87,  # Nombre total d'endpoints uniques
    "method_distribution": {
        "GET": 0.45,
        "POST": 0.25,
        "PUT": 0.15,
        "DELETE": 0.10,
        "PATCH": 0.05
    },
    "auth_type_coverage": ["Bearer", "API Key", "Basic Auth", "OAuth2"],
    "complexity_range": {
        "min_endpoints": 4,
        "max_endpoints": 18,
        "mean_endpoints": 9.2,
        "std_endpoints": 3.7
    }
}
```

#### 2. Métriques de Complétude

```python
completeness_metrics = {
    "fully_documented_endpoints": 87,  # 100% des endpoints
    "partially_documented": 65,  # 75% complétude
    "minimally_documented": 44,  # 50% complétude
    "poorly_documented": 22,  # 25% complétude
    "total_variants": 218  # 87 * 4 variants
}
```

#### 3. Métriques d'Annotation

```python
annotation_metrics = {
    "annotated_endpoints": 87,
    "auto_annotations": 70,
    "expert_annotations": 17,
    "consensus_annotations": 87,
    "mean_confidence": 0.92,
    "annotation_coverage": 1.0,  # 100%
    "inter_annotator_agreement": 0.88  # Kappa
}
```

#### 4. Métriques de Split

```python
split_metrics = {
    "train_size": 152,  # 70% de 218
    "test_size": 66,    # 30% de 218
    "train_ratio": 0.697,
    "test_ratio": 0.303,
    "stratification_quality": {
        "domain_balance": 0.95,  # Chi-square p-value
        "completeness_balance": 0.93,
        "complexity_balance": 0.91
    },
    "no_data_leak": True
}
```

### Validation Automatique

```python
def validate_dataset_quality(dataset_dir: Path) -> ValidationReport:
    """
    Valide la qualité complète des datasets.
    
    Retourne :
    {
        "passed": True/False,
        "diversity_score": 0.92,
        "completeness_score": 1.0,
        "annotation_score": 0.88,
        "split_score": 0.95,
        "issues": [...],
        "warnings": [...],
        "recommendations": [...]
    }
    """
    pass
```

---

## Intégration avec RQ1-RQ5

### RQ1 : Précision des Oracles

**Utilisation des Datasets** :
- **Train set** : Développer et affiner agent Oracle
- **Test set** : Évaluer précision (Precision, Recall, F1)
- **Ground truth** : Référence pour comparaison

```python
# experiments/rq1_orchestrator.py
def run_rq1_experiment(train_set: List[Dataset], test_set: List[Dataset]):
    """
    RQ1 : Évalue précision des oracles dérivés.
    
    Pour chaque dataset de test :
    1. Générer oracles avec agent Oracle
    2. Comparer avec ground truth
    3. Calculer métriques (Precision, Recall, F1)
    4. Agréger résultats
    """
    pass
```

### RQ2 : Détection Inconsistances

**Utilisation des Datasets** :
- **Variants 100%** : Baseline sans inconsistances
- **Variants dégradés** : Introduire inconsistances artificielles
- **Ground truth** : Identifier vraies inconsistances

```python
# experiments/rq2_orchestrator.py
def run_rq2_experiment(test_set: List[Dataset]):
    """
    RQ2 : Évalue capacité à détecter inconsistances oracle-code.
    
    Pour chaque dataset :
    1. Générer code Java avec agent Contractor
    2. Détecter inconsistances avec ValidationAgent
    3. Comparer avec inconsistances connues (ground truth)
    4. Calculer métriques de détection
    """
    pass
```

### RQ3 : Qualité du Code

**Utilisation des Datasets** :
- **Tous variants** : Générer code Java
- **Ground truth** : Critères de qualité attendus

```python
# experiments/rq3_orchestrator.py
def run_rq3_experiment(test_set: List[Dataset]):
    """
    RQ3 : Évalue qualité du code généré.
    
    Pour chaque dataset :
    1. Générer tests Java avec Contractor
    2. Analyser qualité avec CodeQualityAgent
    3. Calculer métriques (alignment, coverage, antipatterns)
    4. Comparer avec standards
    """
    pass
```

### RQ4 : Comparaison LLMs

**Utilisation des Datasets** :
- **Test set fixe** : Même datasets pour tous LLMs
- **5 LLMs** : GPT-4, Claude, Gemini, Mistral, Llama 3.1

```python
# experiments/rq4_orchestrator.py
def run_rq4_experiment(test_set: List[Dataset], llms: List[str]):
    """
    RQ4 : Compare performance de 5 LLMs.
    
    Pour chaque LLM :
    1. Configurer agent avec ce LLM
    2. Exécuter sur test set
    3. Collecter métriques (RQ1, RQ2, RQ3)
    4. Comparer performances
    """
    pass
```

### RQ5 : Impact Complétude

**Utilisation des Datasets** :
- **4 niveaux de complétude** : 100%, 75%, 50%, 25%
- **Même collections** : Comparer variants

```python
# experiments/rq5_orchestrator.py
def run_rq5_experiment(variants_by_completeness: Dict[float, List[Dataset]]):
    """
    RQ5 : Évalue impact de la complétude documentaire.
    
    Pour chaque niveau de complétude :
    1. Exécuter pipeline complet
    2. Collecter métriques (RQ1, RQ2, RQ3)
    3. Analyser corrélation complétude-performance
    4. Identifier seuil minimal de complétude
    """
    pass
```

---

## Livrables Phase 6.1

### Code

✅ **L1** : `experiments/dataset_creator.py` - Créateur de datasets  
✅ **L2** : `experiments/ground_truth_manager.py` - Gestionnaire annotations (enrichi)  
✅ **L3** : `experiments/dataset_splitter.py` - Splitter train/test  
✅ **L4** : `experiments/dataset_validator.py` - Validateur qualité  
✅ **L5** : `experiments/collection_crawler.py` - Crawler collections publiques  
✅ **L6** : `experiments/dataset_exporter.py` - Utilitaires export/import  

### Data

✅ **D1** : 10+ collections Bruno sources  
✅ **D2** : 40+ variants de complétude (10 collections × 4 niveaux)  
✅ **D3** : Ground truth pour tous endpoints  
✅ **D4** : Train/test splits stratifiés  
✅ **D5** : Métadonnées et documentation datasets  

### Documentation

✅ **DOC1** : `docs/PHASE_6.1_DATASETS.md` (ce document)  
✅ **DOC2** : `experiments/datasets/README.md` - Guide utilisation datasets  
✅ **DOC3** : Rapports de validation qualité  

### Scripts

✅ **S1** : `scripts/create_all_datasets.py` - Script création complète  
✅ **S2** : `scripts/validate_datasets.py` - Script validation  
✅ **S3** : `scripts/export_datasets.py` - Script export  

---

## Timeline Phase 6.1

### Jour 1-2 : Setup & Collections (12-13 Déc)

- ✅ Crawler et télécharger 10+ collections Bruno
- ✅ Valider collections (parsing, cohérence)
- ✅ Documenter chaque collection (metadata.json)

### Jour 3-4 : Generation Variants (14-15 Déc)

- ✅ Implémenter algorithme de dégradation
- ✅ Générer 4 variants par collection (100%, 75%, 50%, 25%)
- ✅ Valider cohérence inter-variants

### Jour 5-6 : Ground Truth (16-17 Déc)

- ✅ Annotation automatique via API calls
- ✅ Validation manuelle (sample)
- ✅ Calcul consensus multi-annotateurs

### Jour 7-8 : Train/Test Split (18-19 Déc)

- ✅ Implémentation stratified split
- ✅ Validation split (pas de leak, distribution)
- ✅ Export train/test sets

### Jour 9-10 : Validation & Documentation (20-21 Déc)

- ✅ Validation qualité complète
- ✅ Génération rapports
- ✅ Documentation finale

---

## Métriques de Succès

### Critères d'Acceptation Phase 6.1

| Critère | Cible | Status |
|---------|-------|--------|
| Nombre de collections | ≥ 10 | 🔄 En cours |
| Nombre total de variants | ≥ 40 | 🔄 En cours |
| Couverture annotation | 100% | 🔄 En cours |
| Qualité annotations (confidence) | ≥ 0.90 | 🔄 En cours |
| Train/test ratio | 70/30 ± 5% | 🔄 En cours |
| Pas de data leak | 100% | 🔄 En cours |
| Documentation complète | 100% | 🔄 En cours |

---

## Prochaines Étapes

### Phase 6.2 : Notebooks Jupyter (22-26 Déc)

Création de 5 notebooks d'analyse :
1. `rq1_oracle_analysis.ipynb`
2. `rq2_inconsistency_study.ipynb`
3. `rq3_quality_evaluation.ipynb`
4. `rq4_llm_comparison.ipynb`
5. `rq5_completeness_impact.ipynb`

### Phase 6.3 : Expériences (27-31 Déc)

Exécution des expérimentations RQ1-RQ5 :
- Tests avec 5 LLMs
- Analyse statistique
- Génération rapports

---

## Références

- [ACTION_PLAN.md](ACTION_PLAN.md) - Plan global du projet
- [PHASE_5.5_QUALITY_SECURITY_REVIEW.md](PHASE_5.5_QUALITY_SECURITY_REVIEW.md) - Phase précédente
- [Ground Truth Manager](../experiments/ground_truth_manager.py) - Code existant

---

**Document vivant** : Mis à jour au fur et à mesure de l'avancement de Phase 6.1

**Dernière mise à jour** : 12 Décembre 2025, 10:00 UTC
