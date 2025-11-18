# Scripts Utilitaires

Ce dossier contient des scripts utilitaires pour le projet de génération de tests de contrat.

## Scripts disponibles

### `verify_ollama.py`
Script de vérification et de test de l'installation Ollama.

**Fonctionnalités :**
- ✅ Vérifie que le service Ollama est actif
- ✅ Liste tous les modèles installés
- ✅ Teste chaque modèle configuré (Mistral, Llama)
- ✅ Affiche les détails (taille, version, date de modification)

**Usage :**
```bash
python scripts/verify_ollama.py
```

**Exemple de sortie :**
```
============================================================
Ollama Verification Script
============================================================
✓ Ollama service is running (version 0.12.11)

✓ Found 3 Ollama models:
  • mistral:latest           4.37 GB  Modified: 2025-11-18
  • llama3.1:latest          4.92 GB  Modified: 2025-08-27
  • llama3.2:latest          2.01 GB  Modified: 2025-04-04

============================================================
Testing configured models from llm_config.yaml
============================================================
Testing model: mistral:latest...
✓ Model mistral:latest is working
  Response: Hello from Ollama!

Testing model: llama3.1:latest...
✓ Model llama3.1:latest is working
  Response: Hello from Ollama!

============================================================
✓ All Ollama models are working correctly!
============================================================
```

**Dépendances :**
- `requests` : Pour les appels API HTTP à Ollama
- `utils.logging` : Pour le logging formaté

**Codes de sortie :**
- `0` : Tous les tests ont réussi
- `1` : Au moins un test a échoué ou le service est inactif

---

### `test_dev_mode.py`
Script de test pour le mode développement économique avec coût 0€.

**Fonctionnalités :**
- ✅ Vérifie la disponibilité d'Ollama
- ✅ Teste le chargement des modèles selon ENABLE_CLOUD_MODELS
- ✅ Affiche les modèles cloud vs Ollama chargés
- ✅ Calcule le coût estimé (0€ en mode développement)
- ✅ Valide la configuration économique

**Usage :**
```bash
python scripts/test_dev_mode.py
```

**Exemple de sortie (mode développement):**
```
======================================================================
🔍 VÉRIFICATION OLLAMA
======================================================================

✅ Ollama disponible: version 0.12.11
   URL: http://localhost:11434
======================================================================
🧪 TEST MODE DÉVELOPPEMENT ÉCONOMIQUE
======================================================================

📋 Variable d'environnement ENABLE_CLOUD_MODELS: false

✅ Mode développement économique activé
   → Coût: 0€ (utilisation exclusive d'Ollama)

✅ Configuration chargée: development

📦 Modèles LLM chargés: 2

   🏠 mistral: mistral:latest (provider: ollama)
   🏠 llama: llama3.1:latest (provider: ollama)

======================================================================
📊 RÉSUMÉ
======================================================================

Modèles Cloud (payants): 0
   ✅ Aucun modèle cloud chargé (économie maximale)

Modèles Ollama (gratuits): 2
   • mistral (mistral:latest)
   • llama (llama3.1:latest)

✅ SUCCÈS: Mode développement économique fonctionnel!

💰 COÛT ESTIMÉ:
   • Modèles cloud: 0€ (désactivés)
   • Modèles Ollama: 0€ (local)
   • TOTAL: 0€

🎯 AVANTAGES:
   ✓ Développement sans frais d'API
   ✓ Tests illimités en local
   ✓ Confidentialité des données
   ✓ Disponibilité hors ligne
```

**Dépendances :**
- `utils.config` : Chargement de la configuration
- `utils.logging` : Logging formaté

**Codes de sortie :**
- `0` : Mode développement fonctionnel
- `1` : Configuration incorrecte ou Ollama indisponible

---

## À venir

D'autres scripts seront ajoutés au fur et à mesure du développement :

### `verify_api_keys.py` (À venir)
Vérification des clés API pour les services cloud (OpenAI, Anthropic, Google).

### `setup_database.py` (À venir)
Initialisation de la base de données PostgreSQL avec le schéma requis.

### `benchmark_llms.py` (À venir)
Benchmarking des performances des différents modèles LLM (RQ4).

### `export_metrics.py` (À venir)
Export des métriques d'expérimentation vers différents formats (CSV, JSON, LaTeX).

### `clean_cache.py` (À venir)
Nettoyage des données en cache (Redis, fichiers temporaires).

### `migrate_data.py` (À venir)
Migration des données entre différentes versions du schéma.

---

## Contribution

Lors de l'ajout de nouveaux scripts :

1. **Documentation** : Ajouter une description dans ce README
2. **Shebang** : Utiliser `#!/usr/bin/env python3`
3. **Logging** : Utiliser `utils.logging` pour la cohérence
4. **Arguments** : Utiliser `argparse` pour les options CLI
5. **Codes de sortie** : 0 pour succès, 1+ pour erreurs
6. **Permissions** : Rendre le script exécutable (`chmod +x`)

**Template de base :**
```python
#!/usr/bin/env python3
"""
Description du script.
"""
import sys
import argparse
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from utils.logging import logger


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument("--option", help="Description de l'option")
    args = parser.parse_args()
    
    logger.info("Starting script...")
    
    # Votre code ici
    
    logger.success("Script completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Exécution depuis n'importe où

Tous les scripts peuvent être exécutés depuis n'importe quel répertoire :

```bash
# Depuis la racine du projet
python scripts/verify_ollama.py

# Depuis n'importe où (avec chemin absolu)
python /path/to/project/scripts/verify_ollama.py

# Avec permissions d'exécution
./scripts/verify_ollama.py
```
