# Rapports de Génération de Tests

Ce dossier contient tous les rapports générés automatiquement par le système de génération de tests de contrat.

## 📊 Types de Rapports

### 1. Rapport d'Exécution des Agents
**Fichier**: `agent_execution_report_YYYYMMDD_HHMMSS.html`

Rapport HTML interactif contenant:
- ✅ **Métriques globales**: durée totale, nombre d'agents, taux de succès
- 📈 **Performance par agent**: tâches traitées, réussies, échouées
- 📊 **Graphiques**: distribution des tâches par agent (barres)
- 🎨 **Interface**: design moderne avec code couleur

**Usage**: Ouvrir dans un navigateur pour visualiser l'exécution des 4 agents (Inductor, Oracle, Contractor, Runner)

---

### 2. Rapport d'Exécution des Tests
**Fichier**: `test_execution_report_YYYYMMDD_HHMMSS.html`

Rapport HTML détaillé avec:
- ✅ **Résultats**: nombre de tests passés/échoués, taux de réussite
- ⏱️ **Performance**: temps d'exécution moyen, par test
- 📋 **Détails**: liste complète des tests avec statuts
- 📊 **Graphiques**: 
  - Pie chart: répartition succès/échecs
  - Bar chart: temps d'exécution par test

**Usage**: Analyser les résultats d'exécution des tests générés

---

### 3. Liste des Oracles
**Fichier**: `oracle_list_YYYYMMDD_HHMMSS.txt`

Liste texte structurée des oracles générés:
```
1. Get Users
   - Oracle ID: xxx-xxx-xxx
   - Endpoint ID: yyy-yyy-yyy
   - Expected Status: 200
   - Confidence: 0.85
   - Assertions: 3
```

**Usage**: Référence rapide des oracles par nom d'endpoint

---

### 4. Trace d'Exécution
**Fichier**: `traces/execution_trace_YYYYMMDD_HHMMSS.json`

JSON structuré complet du workflow:
```json
{
  "session_id": "...",
  "duration_seconds": 71.03,
  "workflow_phases": [
    {
      "phase": 1,
      "name": "Context Extraction",
      "agent": "Inductor",
      "endpoints_extracted": 3,
      "endpoints": [...]
    },
    ...
  ],
  "summary": {
    "total_tests": 3,
    "tests_passed": 3,
    "pass_rate": 100.0
  }
}
```

**Usage**: 
- Audit complet du workflow
- Debugging et analyse
- Intégration CI/CD
- Export vers outils de monitoring

---

### 5. Log du Workflow
**Fichier**: `logs/workflow_log_YYYYMMDD_HHMMSS.log`

Log texte avec timestamps:
```
[2025-11-20 01:11:05] INFO: Initializing system components
[2025-11-20 01:11:08] SUCCESS: Phase 1 complete: Extracted 1 endpoints
[2025-11-20 01:12:09] SUCCESS: Phase 2 complete: Generated 1 oracles
```

**Usage**: Tracking séquentiel des événements du workflow

---

## 📈 Graphiques Générés

### Dossier: `graphs/`

1. **`agent_metrics_YYYYMMDD_HHMMSS.png`**
   - Bar chart des métriques d'agents
   - 3 barres par agent: Processed, Succeeded, Failed
   - Couleurs: Bleu (traité), Vert (succès), Rouge (échec)

2. **`test_results_YYYYMMDD_HHMMSS.png`**
   - Pie chart: répartition succès/échecs
   - Bar chart: temps d'exécution par test
   - Couleurs selon statut (vert=passé, rouge=échec)

---

## 🔧 Utilisation

### Génération Automatique
Les rapports sont générés automatiquement à chaque exécution:
```bash
python src/main.py bruno_collections/example_api/Sample_API_Collection.json
```

### Accès aux Rapports
```bash
# Lister tous les rapports
ls -lh reports/*.html reports/*/*.{json,log,png}

# Ouvrir le dernier rapport d'agents
open $(ls -t reports/agent_execution_report_*.html | head -1)

# Ouvrir le dernier rapport de tests
open $(ls -t reports/test_execution_report_*.html | head -1)

# Lire la liste des oracles
cat $(ls -t reports/oracle_list_*.txt | head -1)

# Examiner la trace JSON
cat $(ls -t reports/traces/*.json | head -1) | jq .
```

---

## 📦 Structure des Dossiers

```
reports/
├── README.md                              # Ce fichier
├── agent_execution_report_*.html          # Rapports HTML des agents
├── test_execution_report_*.html           # Rapports HTML des tests
├── oracle_list_*.txt                      # Listes d'oracles
├── graphs/
│   ├── agent_metrics_*.png               # Graphes des agents
│   └── test_results_*.png                # Graphes des tests
├── traces/
│   └── execution_trace_*.json            # Traces JSON complètes
└── logs/
    └── workflow_log_*.log                # Logs de workflow
```

---

## 🎯 Cas d'Usage

### 1. Monitoring de Production
- Vérifier le taux de succès des agents
- Analyser les temps d'exécution
- Détecter les anomalies

### 2. Debugging
- Trace JSON complète pour reproduire les bugs
- Logs horodatés pour identifier les problèmes
- Graphiques pour visualiser les patterns

### 3. Reporting
- Rapports HTML prêts à partager
- Graphiques exportables
- Métriques quantifiables

### 4. CI/CD Integration
- Parse du JSON pour les pipelines
- Fail si pass_rate < threshold
- Archivage des rapports historiques

---

## 🔍 Métriques Clés

| Métrique | Localisation | Format |
|----------|--------------|--------|
| Taux de succès global | HTML/JSON | Percentage |
| Durée totale | HTML/JSON | Seconds |
| Tests passés/échoués | HTML/JSON | Count |
| Temps d'exécution moyen | HTML/JSON | Milliseconds |
| Oracles générés | TXT/JSON | Count |
| Endpoints extraits | JSON | Count |

---

## 📝 Notes

- Les rapports sont horodatés (format: YYYYMMDD_HHMMSS)
- Les graphiques utilisent matplotlib (backend non-interactif)
- Les rapports HTML sont standalone (CSS inline)
- Les traces JSON sont compatibles avec jq
- Les logs sont au format texte simple

---

## 🚀 Améliorations Futures

- [ ] Export PDF des rapports HTML
- [ ] Dashboard temps réel avec rafraîchissement
- [ ] Comparaison entre sessions
- [ ] Alertes automatiques sur échecs
- [ ] Intégration Prometheus/Grafana
- [ ] Archive automatique des anciens rapports

---

**Généré par**: Contract Test Generation System v0.1.0  
**Auteur**: Aurel IKAMA HONEY  
**Date**: Novembre 2025
