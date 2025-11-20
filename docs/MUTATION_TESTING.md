# Tests de Mutation avec Mutmut

## Introduction

Les tests de mutation sont une technique pour évaluer la qualité de votre suite de tests. Mutmut crée automatiquement des versions "mutantes" de votre code source (par exemple, en changeant `==` en `!=`, `+` en `-`, etc.) et vérifie si vos tests détectent ces changements.

### Score de Mutation

Le score de mutation indique le pourcentage de mutations détectées par vos tests :
- **100%** : Tous les mutants ont été tués (excellent !)
- **80-99%** : Très bonne couverture
- **60-79%** : Couverture acceptable
- **<60%** : Amélioration nécessaire

## Installation

Mutmut est déjà inclus dans `requirements.txt`. Pour l'installer :

```bash
pip install -r requirements.txt
```

## Configuration

La configuration se trouve dans deux fichiers :
- **setup.cfg** : Configuration principale de mutmut
- **.mutmut-config.py** : Hooks personnalisés pour filtrer certaines mutations

## Utilisation

### 1. Exécuter tous les tests de mutation

```bash
mutmut run
```

Cette commande :
1. Analyse le code source dans `src/`
2. Crée des mutations
3. Exécute vos tests pytest pour chaque mutation
4. Détermine si le mutant est tué (test échoue) ou survit (test passe)

### 2. Voir les résultats

```bash
mutmut results
```

Affiche un résumé des résultats :
- **Killed** : Mutants détectés par les tests ✓
- **Survived** : Mutants non détectés (problème potentiel) ✗
- **Suspicious** : Mutants avec comportement inattendu
- **Timeout** : Mutations causant des timeouts

### 3. Examiner les mutants survivants

```bash
mutmut show <ID>
```

Affiche le code muté pour un mutant spécifique. Exemple :

```bash
mutmut show 5
```

### 4. Examiner tous les survivants

```bash
mutmut show survived
```

### 5. Appliquer une mutation pour la tester

```bash
mutmut apply <ID>
```

**Attention** : Cela modifie réellement votre code source ! N'oubliez pas de restaurer :

```bash
git checkout -- <fichier>
```

### 6. Générer un rapport HTML

```bash
mutmut html
```

Ouvre un rapport interactif dans votre navigateur.

### 7. Exécuter les mutations sur un fichier spécifique

```bash
mutmut run --paths-to-mutate=src/agents/oracle.py
```

### 8. Reprendre après une interruption

```bash
mutmut run --resume
```

## Workflow recommandé

### Phase 1 : Premier scan

```bash
# Exécuter sur un module spécifique d'abord
mutmut run --paths-to-mutate=src/agents/

# Voir les résultats
mutmut results

# Générer le rapport HTML
mutmut html
```

### Phase 2 : Analyser et améliorer

```bash
# Identifier les survivants
mutmut show survived

# Pour chaque survivant, analyser pourquoi il a survécu :
# - Le code est-il réellement non testé ?
# - Le code est-il équivalent (faux positif) ?
# - Faut-il ajouter un test ?
```

### Phase 3 : Scan complet

```bash
# Une fois satisfait, scanner tout le projet
mutmut run

# Suivre la progression
mutmut results
```

## Interpréter les résultats

### Mutant tué (Killed) ✓

```python
# Code original
if x > 0:
    return True

# Mutation : > devient >=
if x >= 0:
    return True

# Si un test échoue → Mutant tué ✓
```

Vos tests détectent correctement cette différence.

### Mutant survivant (Survived) ✗

```python
# Code original
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# Mutation : += devient -=
total -= item.price

# Si aucun test n'échoue → Mutant survit ✗
```

**Action** : Ajouter un test qui vérifie que `calculate_total([item1, item2])` donne la somme correcte.

### Mutants équivalents

Certains mutants sont "équivalents" au code original et ne peuvent pas être tués :

```python
# Original
x = x + 1

# Mutation équivalente
x += 1
```

Ces faux positifs sont rares mais normaux.

## Optimisation des performances

Les tests de mutation peuvent être lents. Voici quelques astuces :

### 1. Parallélisation

```bash
mutmut run --use-coverage --rerun-all
```

### 2. Utiliser la couverture de code

Mutmut utilise automatiquement les données de couverture pour ne muter que le code couvert.

```bash
# D'abord générer la couverture
pytest --cov=src --cov-report=

# Puis exécuter mutmut
mutmut run --use-coverage
```

### 3. Tester par modules

Au lieu de tout tester d'un coup :

```bash
mutmut run --paths-to-mutate=src/agents/oracle.py
mutmut run --paths-to-mutate=src/agents/contractor.py
mutmut run --paths-to-mutate=src/orchestration/
```

## Intégration CI/CD

Vous pouvez ajouter les tests de mutation à votre pipeline CI :

```yaml
# .github/workflows/mutation-tests.yml
name: Mutation Tests

on:
  pull_request:
    branches: [ main ]
  schedule:
    # Exécuter hebdomadairement
    - cron: '0 0 * * 0'

jobs:
  mutation-testing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run mutation tests
        run: mutmut run --use-coverage
      - name: Generate report
        run: mutmut results
```

## Objectifs de qualité

Pour ce projet, visons :
- **>90%** pour les agents critiques (OracleAgent, ContractorAgent)
- **>85%** pour les modules d'orchestration
- **>80%** pour les utilitaires et helpers

## Commandes rapides

```bash
# Démarrage rapide
mutmut run --paths-to-mutate=src/agents/

# Voir le score global
mutmut results

# Examiner les problèmes
mutmut show survived

# Nettoyer et recommencer
mutmut run --rerun-all

# Générer rapport HTML
mutmut html
```

## Troubleshooting

### Les tests sont trop lents

- Utilisez `--use-coverage` pour limiter les mutations au code couvert
- Testez par modules plutôt que tout d'un coup
- Optimisez vos tests pytest (évitez les fixtures lourdes)

### Trop de faux positifs

Ajustez [.mutmut-config.py](.mutmut-config.py) pour ignorer certains types de mutations.

### Mutmut plante

```bash
# Nettoyer le cache
rm -rf .mutmut-cache/

# Recommencer
mutmut run
```

## Ressources

- [Documentation officielle Mutmut](https://mutmut.readthedocs.io/)
- [Introduction au mutation testing](https://en.wikipedia.org/wiki/Mutation_testing)
- [Best practices](https://pitest.org/)

## Exemple de session

```bash
$ mutmut run --paths-to-mutate=src/agents/oracle.py

- Mutation testing starting -

These are the steps:
1. A full test suite run will be made to make sure we can run the tests successfully and we have a baseline
2. Mutants will be generated and checked

Running tests without mutations... Done

Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be killed.
🙁 Survived.         This means your tests need to be expanded.
🔇 Skipped.          Skipped.

Mutation testing: 100%|████████████████████| 234/234 [05:23<00:00,  1.38s/it]

$ mutmut results
Survived: 12
Killed: 210
Timeout: 2
Suspicious: 0
Skipped: 10

Mutation score: 89.74%

$ mutmut show survived
# Affiche les 12 mutants survivants pour analyse
```
