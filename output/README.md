# Output Directory Structure

Ce dossier contient tous les fichiers générés par le système de génération de tests de contrat.

## 📁 Structure des Dossiers

```
output/
├── README.md                    # Ce fichier
├── tests/                       # Tests générés
│   ├── java/                    # Fichiers Java (.java)
│   │   ├── GetUsersTest.java
│   │   ├── CreateUserTest.java
│   │   └── ...
│   └── gherkin/                 # Fichiers Gherkin (.feature)
│       ├── get_users.feature
│       ├── create_user.feature
│       └── ...
├── reports/                     # Rapports d'exécution
│   ├── html/                    # Rapports HTML interactifs
│   │   ├── agent_execution_report_YYYYMMDD_HHMMSS.html
│   │   └── test_execution_report_YYYYMMDD_HHMMSS.html
│   ├── graphs/                  # Graphiques et visualisations
│   │   ├── agent_metrics_YYYYMMDD_HHMMSS.png
│   │   └── test_results_YYYYMMDD_HHMMSS.png
│   ├── logs/                    # Logs détaillés
│   │   └── workflow_log_YYYYMMDD_HHMMSS.log
│   └── traces/                  # Traces JSON complètes
│       └── execution_trace_YYYYMMDD_HHMMSS.json
├── oracles/                     # Oracles générés
│   ├── oracle_list_YYYYMMDD_HHMMSS.txt
│   └── oracle_details_YYYYMMDD_HHMMSS.json
└── contexts/                    # Contextes extraits
    └── endpoint_contexts_YYYYMMDD_HHMMSS.json
```

---

## 📋 Conventions de Nommage

### Tests Java
- **Format** : `{EndpointName}Test.java`
- **Convention** : PascalCase + suffix `Test`
- **Exemples** : `GetUsersTest.java`, `CreateOrderTest.java`

### Tests Gherkin
- **Format** : `{endpoint_name}.feature`
- **Convention** : snake_case
- **Exemples** : `get_users.feature`, `create_order.feature`

### Rapports
- **Format** : `{type}_{timestamp}.{ext}`
- **Convention** : snake_case + timestamp (YYYYMMDD_HHMMSS)
- **Exemples** :
  - `agent_execution_report_20251120_011813.html`
  - `test_execution_report_20251120_011813.html`
  - `agent_metrics_20251120_011813.png`
  - `workflow_log_20251120_011813.log`

### Oracles et Contextes
- **Format** : `{type}_{timestamp}.{ext}`
- **Convention** : snake_case + timestamp
- **Exemples** :
  - `oracle_list_20251120_011813.txt`
  - `endpoint_contexts_20251120_011813.json`

---

## 🎯 Utilisation

### Accès aux Tests Générés

```bash
# Lister tous les tests Java
ls -1 output/tests/java/*.java

# Lister tous les fichiers Gherkin
ls -1 output/tests/gherkin/*.feature

# Derniers tests générés
ls -t output/tests/java/*.java | head -5
```

### Accès aux Rapports

```bash
# Ouvrir le dernier rapport d'agents
open $(ls -t output/reports/html/agent_execution_report_*.html | head -1)

# Ouvrir le dernier rapport de tests
open $(ls -t output/reports/html/test_execution_report_*.html | head -1)

# Voir les derniers logs
cat $(ls -t output/reports/logs/workflow_log_*.log | head -1)

# Analyser la dernière trace JSON
cat $(ls -t output/reports/traces/execution_trace_*.json | head -1) | jq .
```

### Accès aux Oracles

```bash
# Lire la liste des oracles
cat $(ls -t output/oracles/oracle_list_*.txt | head -1)

# Analyser les détails des oracles
cat $(ls -t output/oracles/oracle_details_*.json | head -1) | jq .
```

### Accès aux Contextes

```bash
# Analyser les contextes extraits
cat $(ls -t output/contexts/endpoint_contexts_*.json | head -1) | jq .
```

---

## 🧹 Nettoyage

### Supprimer les anciens fichiers

```bash
# Supprimer les fichiers de plus de 7 jours
find output -type f -mtime +7 -delete

# Garder seulement les 10 derniers rapports
cd output/reports/html && ls -t *.html | tail -n +11 | xargs rm -f
cd output/reports/graphs && ls -t *.png | tail -n +11 | xargs rm -f
cd output/reports/logs && ls -t *.log | tail -n +11 | xargs rm -f
cd output/reports/traces && ls -t *.json | tail -n +11 | xargs rm -f
```

### Script de nettoyage automatique

```bash
# Créer un script de nettoyage
cat > scripts/clean_output.sh << 'EOF'
#!/bin/bash
# Nettoyer les fichiers générés de plus de 7 jours
find output -type f -mtime +7 -delete
echo "✓ Fichiers de plus de 7 jours supprimés"

# Garder seulement les 10 derniers de chaque type
for dir in output/reports/{html,graphs,logs,traces} output/oracles output/contexts; do
    cd "$dir" 2>/dev/null && ls -t | tail -n +11 | xargs rm -f 2>/dev/null
done
echo "✓ Gardé seulement les 10 derniers fichiers par catégorie"
EOF

chmod +x scripts/clean_output.sh
```

---

## 📊 Statistiques

### Compter les fichiers générés

```bash
# Total de tests Java
echo "Tests Java: $(find output/tests/java -name '*.java' | wc -l)"

# Total de fichiers Gherkin
echo "Fichiers Gherkin: $(find output/tests/gherkin -name '*.feature' | wc -l)"

# Total de rapports
echo "Rapports HTML: $(find output/reports/html -name '*.html' | wc -l)"
echo "Graphiques: $(find output/reports/graphs -name '*.png' | wc -l)"
echo "Logs: $(find output/reports/logs -name '*.log' | wc -l)"
echo "Traces: $(find output/reports/traces -name '*.json' | wc -l)"

# Espace disque utilisé
du -sh output/*
```

---

## 🔒 Gitignore

Les fichiers générés sont exclus du contrôle de version (voir `.gitignore`):

```gitignore
# Generated output files
output/tests/
output/reports/
output/oracles/
output/contexts/

# Keep structure
!output/tests/.gitkeep
!output/reports/.gitkeep
!output/oracles/.gitkeep
!output/contexts/.gitkeep
!output/README.md
```

---

## 📖 Référence

Pour plus d'informations sur les conventions de nommage, voir :
- `/docs/NAMING_CONVENTIONS.md` - Conventions complètes
- `/reports/README.md` - Documentation des rapports

---

**Dernière mise à jour** : 20 novembre 2025  
**Auteur** : Aurel IKAMA HONEY
