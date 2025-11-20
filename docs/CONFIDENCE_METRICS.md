# 🎯 Confidence Metrics Documentation

Documentation des métriques de confidence dans le système de génération de tests de contrat.

## Vue d'Ensemble

La **confidence** représente le niveau de confiance attribué à un oracle généré par le système. Elle mesure la qualité et la fiabilité de l'oracle basé sur plusieurs facteurs.

## Valeurs de Confidence

| Plage | Niveau | Indicateur | Signification |
|-------|--------|-----------|---------------|
| 0.80 - 1.00 | **High** | 🟢 | Oracle de haute qualité, très fiable |
| 0.60 - 0.79 | **Medium** | 🟡 | Oracle acceptable, peut nécessiter révision |
| 0.00 - 0.59 | **Low** | 🔴 | Oracle à faible confiance, révision recommandée |

## Calcul de la Confidence

La confidence est calculée par l'agent **Oracle** lors de la génération des oracles. Elle prend en compte :

### Facteurs Principaux

1. **Complétude de la Spécification API**
   - Présence de schémas de réponse détaillés
   - Documentation complète des endpoints
   - Exemples de réponses fournis

2. **Qualité des Données d'Entrée**
   - Clarté des paramètres de requête
   - Précision des types de données
   - Cohérence des exemples

3. **Complexité de la Validation**
   - Simplicité des assertions à générer
   - Nombre de conditions à vérifier
   - Dépendances entre validations

4. **Expérience de l'Agent**
   - Succès des générations précédentes
   - Feedback des exécutions de tests
   - Historique des validations

## Utilisation dans les Rapports

### Rapport d'Exécution des Agents

Le rapport HTML `agent_execution_report.html` affiche une section dédiée aux métriques de confidence :

```
🎯 Oracle Confidence Metrics

Average Confidence: 75.5%
Min Confidence: 62.0%
Max Confidence: 89.0%
Total Oracles: 12

┌─────────────────────┬────────────┬─────────┐
│ Oracle Name         │ Confidence │ Quality │
├─────────────────────┼────────────┼─────────┤
│ GetUsersOracle      │ 89.0%      │ 🟢 High │
│ CreateUserOracle    │ 82.0%      │ 🟢 High │
│ UpdateUserOracle    │ 75.0%      │ 🟡 Medium│
│ DeleteUserOracle    │ 62.0%      │ 🟡 Medium│
└─────────────────────┴────────────┴─────────┘
```

### Liste des Oracles

Le fichier `oracle_list.txt` inclut la confidence pour chaque oracle :

```text
Oracle List - Session 550e8400-e29b-41d4-a716-446655440000
Generated: 2025-11-20 01:18:13
================================================================================

1. GetUsersOracle (Confidence: 0.89)
   - Endpoint: GET /api/users
   - Validation: Status code, response structure, data types

2. CreateUserOracle (Confidence: 0.82)
   - Endpoint: POST /api/users
   - Validation: Status code, created resource, headers
```

### Traces JSON

Le fichier `execution_trace.json` stocke la confidence avec toutes les métadonnées :

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "oracles": [
    {
      "id": "oracle_001",
      "name": "GetUsersOracle",
      "endpoint_id": "endpoint_001",
      "confidence": 0.89,
      "generated_at": "2025-11-20T01:18:13Z",
      "validation_rules": [...]
    }
  ]
}
```

## Amélioration de la Confidence

### Actions Recommandées par Niveau

#### 🔴 Low Confidence (< 0.60)

**Actions Immédiates :**
1. ✅ Revoir la spécification de l'endpoint
2. ✅ Ajouter des exemples de réponses
3. ✅ Clarifier les contraintes de validation
4. ✅ Vérifier la cohérence avec les autres endpoints

**Exemple de Révision :**
```yaml
# Avant (confidence = 0.45)
/api/users:
  get:
    responses:
      200:
        description: List of users

# Après (confidence = 0.85)
/api/users:
  get:
    responses:
      200:
        description: List of users
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/User'
            example:
              - id: 1
                name: "John Doe"
                email: "john@example.com"
```

#### 🟡 Medium Confidence (0.60 - 0.79)

**Actions Suggérées :**
1. ✓ Enrichir les exemples de réponse
2. ✓ Ajouter des cas limites
3. ✓ Documenter les codes d'erreur possibles
4. ✓ Valider avec des tests manuels

#### 🟢 High Confidence (≥ 0.80)

**Maintenance :**
- Surveiller les résultats des tests
- Maintenir la qualité de la documentation
- Mettre à jour si l'API évolue

## Analyse de la Confidence

### Comparer les Confidences Entre Exécutions

```bash
# Extraire les confidences de deux exécutions
jq '.oracles[] | {name: .name, confidence: .confidence}' \
   output/exec_20251120_011813/traces/execution_trace.json

jq '.oracles[] | {name: .name, confidence: .confidence}' \
   output/exec_20251121_092847/traces/execution_trace.json
```

### Statistiques de Confidence

```bash
# Moyenne de confidence d'une exécution
jq '[.oracles[].confidence] | add / length' \
   output/exec_20251120_011813/traces/execution_trace.json

# Oracles avec confidence < 0.60
jq '.oracles[] | select(.confidence < 0.60) | {name, confidence}' \
   output/exec_20251120_011813/traces/execution_trace.json
```

### Graphique d'Évolution

Pour visualiser l'évolution de la confidence :

```python
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Charger plusieurs exécutions
executions = sorted(Path("output").glob("exec_*"))

confidences = []
for exec_dir in executions:
    trace_file = exec_dir / "traces" / "execution_trace.json"
    with open(trace_file) as f:
        data = json.load(f)
        avg_conf = sum(o['confidence'] for o in data['oracles']) / len(data['oracles'])
        confidences.append(avg_conf)

# Graphique
plt.plot(confidences, marker='o')
plt.axhline(y=0.80, color='g', linestyle='--', label='High threshold')
plt.axhline(y=0.60, color='orange', linestyle='--', label='Medium threshold')
plt.xlabel('Execution')
plt.ylabel('Average Confidence')
plt.title('Oracle Confidence Evolution')
plt.legend()
plt.savefig('confidence_evolution.png')
```

## Impact sur les Tests

### Corrélation avec le Succès des Tests

La confidence des oracles est généralement corrélée avec le taux de succès des tests :

| Confidence Moyenne | Taux de Succès Attendu |
|-------------------|------------------------|
| ≥ 0.85 | > 90% |
| 0.70 - 0.84 | 75% - 90% |
| 0.60 - 0.69 | 60% - 75% |
| < 0.60 | < 60% |

### Utilisation pour la Priorisation

Les oracles peuvent être exécutés par ordre de confidence :

1. **Tests Haute Confidence d'abord** : Pour validation rapide
2. **Tests Basse Confidence en dernier** : Nécessitent plus d'attention
3. **Tests Medium Confidence au milieu** : Équilibre entre les deux

## API Programmatique

### Accès à la Confidence

```python
from shared_context import ContextManager, Oracle

# Récupérer un oracle
oracle = await context_manager.get_oracle(oracle_id)

# Accéder à la confidence
confidence = oracle.confidence  # float entre 0.0 et 1.0

# Catégoriser
if confidence >= 0.80:
    quality = "High"
elif confidence >= 0.60:
    quality = "Medium"
else:
    quality = "Low"

print(f"Oracle {oracle.name} has {quality} confidence ({confidence:.2%})")
```

### Filtrer par Confidence

```python
# Récupérer tous les oracles
oracles = await context_manager.list_oracles(session_id)

# Filtrer par confidence
high_confidence = [o for o in oracles if o.confidence >= 0.80]
low_confidence = [o for o in oracles if o.confidence < 0.60]

print(f"High confidence: {len(high_confidence)}")
print(f"Low confidence: {len(low_confidence)}")
```

## Configuration

### Seuils Personnalisables

Les seuils de confidence peuvent être configurés dans `config/agents_config.yaml` :

```yaml
oracle_agent:
  confidence:
    high_threshold: 0.80    # Seuil pour "High"
    medium_threshold: 0.60  # Seuil pour "Medium"
    min_acceptable: 0.50    # Confidence minimale acceptable
```

### Ajustement Dynamique

Le système peut ajuster les seuils en fonction des résultats :

```python
# Dans config/agents_config.yaml
oracle_agent:
  confidence:
    adaptive: true          # Ajuster en fonction des succès
    learning_rate: 0.05     # Vitesse d'apprentissage
```

## Bonnes Pratiques

### ✅ DO

- Monitorer régulièrement les confidences moyennes
- Investiguer les oracles à faible confidence
- Améliorer la documentation API pour augmenter la confidence
- Utiliser les rapports HTML pour visualiser les tendances
- Comparer les confidences entre exécutions

### ❌ DON'T

- Ignorer les warnings de faible confidence
- Déployer des tests basés sur des oracles < 0.50
- Modifier manuellement les valeurs de confidence
- Supprimer les oracles à faible confidence sans analyse

## Références

- **Code Source** : `src/agents/oracle.py` - Génération des oracles
- **Modèles** : `src/shared_context/models.py` - Modèle `Oracle`
- **Rapports** : `src/utils/report_generator.py` - Affichage de la confidence
- **Documentation** : `docs/PHASE_4.1_SUMMARY.md` - Évolution du système

---

**Version** : 2.0  
**Dernière mise à jour** : 20 novembre 2025  
**Auteur** : Aurel IKAMA HONEY
