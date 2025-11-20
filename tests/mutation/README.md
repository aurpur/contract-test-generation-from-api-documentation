# Tests de Mutation

Ce répertoire contient tous les fichiers et outils liés aux tests de mutation du projet.

## 📂 Structure

```
tests/mutation/
├── README.md                    # Ce fichier
├── .mutmut-config.py           # Configuration mutmut
├── run_mutation_tests.sh       # Script d'exécution
├── pytest_wrapper.sh           # Wrapper pytest
├── mutants/                    # Code muté généré
│   ├── src/                    # Sources mutées
│   └── logs/                   # Logs de mutation
├── mutation_*.log              # Logs d'exécution
└── test_results_full.log       # Résultats complets
```

## 🧬 Qu'est-ce que le Mutation Testing ?

Le mutation testing consiste à introduire des modifications (mutations) dans le code source pour vérifier si les tests détectent ces changements. C'est une mesure de la qualité des tests.

## 🚀 Exécution

```bash
# Depuis la racine du projet
cd tests/mutation

# Exécuter les tests de mutation
./run_mutation_tests.sh

# Voir les résultats
cat mutation_test_output.txt
```

## 📊 Métriques

Les métriques de mutation incluent :
- **Killed** : Mutations détectées par les tests ✅
- **Survived** : Mutations non détectées ⚠️
- **Timeout** : Mutations causant timeout ⏱️
- **Suspicious** : Mutations suspectes 🔍

## 📖 Documentation

Pour plus de détails, consultez :
- [`docs/MUTATION_TESTING.md`](../../docs/MUTATION_TESTING.md) - Guide complet
- [`docs/MUTATION_TESTING_STATUS.md`](../../docs/MUTATION_TESTING_STATUS.md) - État actuel

## 🔧 Configuration

La configuration mutmut se trouve dans `.mutmut-config.py` et définit :
- Les chemins à tester
- Les patterns à exclure
- Les options d'exécution
- Le timeout par mutation

## ⚠️ Notes

- Les tests de mutation sont longs à exécuter
- Les fichiers mutants sont dans `mutants/` et ne doivent pas être commités
- Les logs sont conservés pour analyse
