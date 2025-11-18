# Configuration Ollama

**Auteur** : Aurel IKAMA HONEY

Ce document explique comment configurer et utiliser Ollama pour exécuter Mistral et Llama localement, sans clé API.

## Avantages d'Ollama

- ✅ **Gratuit** : Pas de frais d'API
- ✅ **Privé** : Vos données restent locales
- ✅ **Rapide** : Pas de latence réseau
- ✅ **Hors ligne** : Fonctionne sans connexion internet
- ✅ **Illimité** : Pas de quota ou limite de requêtes

## Mode Développement Économique

Le projet supporte un **mode développement avec coût 0€** en désactivant les modèles cloud (OpenAI, Anthropic, Google) et en utilisant uniquement Ollama.

### Activation du mode économique

Dans le fichier `.env`, configurez :
```bash
# Désactiver les modèles cloud pour économiser les coûts
ENABLE_CLOUD_MODELS=false

# Les clés API cloud ne sont pas nécessaires en mode développement
# OPENAI_API_KEY=...
# ANTHROPIC_API_KEY=...
# GOOGLE_API_KEY=...
```

### Comportement automatique

Lorsque `ENABLE_CLOUD_MODELS=false` :
- ✅ Les modèles OpenAI, Anthropic et Google sont **automatiquement désactivés**
- ✅ Tous les agents utilisent **Ollama comme fallback** (Mistral ou Llama)
- ✅ **Coût total : 0€** - Tout fonctionne en local
- ✅ Pas besoin de clés API cloud
- ✅ Parfait pour le développement, tests et expérimentations

### Passage en mode production

Pour activer les modèles cloud en production :
```bash
# Activer les modèles cloud
ENABLE_CLOUD_MODELS=true

# Ajouter les clés API nécessaires
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

## Installation

### macOS
```bash
# Télécharger depuis https://ollama.com
# Ou via Homebrew
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Version actuelle
- **Ollama** : 0.12.11

## Modèles installés

### 1. Mistral (Recommandé pour le projet)
```bash
ollama pull mistral
```
- **Taille** : ~4.4 GB
- **Utilisation** : Code generation, structured output, reasoning
- **Configuration** : `mistral:latest` dans `llm_config.yaml`

### 2. Llama 3.1
```bash
ollama pull llama3.1
```
- **Taille** : ~4.9 GB
- **Utilisation** : General purpose, multilingual
- **Configuration** : `llama3.1:latest` dans `llm_config.yaml`

### 3. Autres modèles utiles (optionnel)

#### CodeLlama - Spécialisé pour le code
```bash
ollama pull codellama
```

#### Mixtral - Modèle puissant
```bash
ollama pull mixtral
```

#### Llama 3.2 - Version plus légère
```bash
ollama pull llama3.2
```

## Vérification de l'installation

### 1. Vérifier le service
```bash
# Vérifier si Ollama est en cours d'exécution
curl http://localhost:11434/api/version
```

### 2. Lister les modèles
```bash
ollama list
```

### 3. Tester un modèle
```bash
ollama run mistral "Dis bonjour en une phrase"
```

### 4. Script de vérification automatique
```bash
python scripts/verify_ollama.py
```

## Configuration du projet

### 1. Fichier `.env`
```bash
# Ollama (Local LLM - No API Key Required)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MISTRAL_MODEL=mistral:latest
OLLAMA_LLAMA_MODEL=llama3.1:latest
```

### 2. Fichier `config/llm_config.yaml`
```yaml
llm:
  models:
    mistral:
      provider: ollama
      model: mistral:latest
      temperature: 0.2
      max_tokens: 4096
      base_url: http://localhost:11434
    
    llama:
      provider: ollama
      model: llama3.1:latest
      temperature: 0.2
      max_tokens: 4096
      base_url: http://localhost:11434
```

## Utilisation dans le code

### Exemple avec le client LLM
```python
from utils.llm_client import get_llm_client

# Utiliser Mistral via Ollama
mistral_client = get_llm_client("mistral")
response = mistral_client.generate("Your prompt here")

# Utiliser Llama via Ollama
llama_client = get_llm_client("llama")
response = llama_client.generate("Your prompt here")
```

## Commandes utiles

### Gestion des modèles
```bash
# Lister les modèles
ollama list

# Supprimer un modèle
ollama rm mistral

# Mettre à jour un modèle
ollama pull mistral

# Afficher les infos d'un modèle
ollama show mistral
```

### Gestion du service
```bash
# Démarrer Ollama (si pas déjà lancé)
ollama serve

# Tester la connexion
curl http://localhost:11434/api/tags
```

### Mode interactif
```bash
# Chat interactif avec un modèle
ollama run mistral

# Avec un prompt initial
ollama run mistral "Explique-moi les tests de contrat"
```

## Performance

### Mistral vs API Cloud

| Aspect | Mistral (Ollama) | Mistral API |
|--------|------------------|-------------|
| Coût | Gratuit | ~$0.001/1K tokens |
| Latence | ~100-500ms | ~500-2000ms |
| Confidentialité | 100% local | Cloud |
| Disponibilité | Hors ligne | Internet requis |
| Limite | Aucune | Quota API |

### Configuration matérielle recommandée
- **RAM** : Minimum 8 GB (16 GB recommandé)
- **Stockage** : ~10 GB pour 2-3 modèles
- **CPU/GPU** : GPU optionnel pour accélération

## Dépannage

### Le service ne démarre pas
```bash
# Vérifier le processus
ps aux | grep ollama

# Redémarrer le service
pkill ollama
ollama serve
```

### Modèle introuvable
```bash
# Vérifier les modèles installés
ollama list

# Réinstaller si nécessaire
ollama pull mistral
```

### Erreur de connexion
```bash
# Vérifier que le port 11434 est disponible
lsof -i :11434

# Tester la connexion
curl http://localhost:11434/api/version
```

### Performances lentes
- Fermer les applications inutiles pour libérer la RAM
- Utiliser des modèles plus petits (llama3.2 au lieu de llama3.1)
- Activer l'accélération GPU si disponible

## Comparaison des modèles

| Modèle | Taille | Force | Usage recommandé |
|--------|--------|-------|------------------|
| **mistral** | 4.4 GB | Code, structure | **Contractor, Oracle** |
| **llama3.1** | 4.9 GB | Général, multilingual | **Inductor** |
| **llama3.2** | 2.0 GB | Léger, rapide | Tests, prototypage |
| **codellama** | 3.8 GB | Code spécialisé | Génération de tests |
| **mixtral** | 26 GB | Très puissant | Tâches complexes |

## Ressources

- Documentation officielle : https://ollama.com/docs
- Liste des modèles : https://ollama.com/library
- GitHub : https://github.com/ollama/ollama
- Discord communautaire : https://discord.gg/ollama

## Migration depuis les API Cloud

Si vous utilisez actuellement Mistral API, la migration vers Ollama est simple :

### Avant (avec API)
```yaml
mistral:
  provider: mistral
  model: mistral-large-latest
  temperature: 0.2
  max_tokens: 4096
```

```bash
MISTRAL_API_KEY=your_api_key_here
```

### Après (avec Ollama)
```yaml
mistral:
  provider: ollama
  model: mistral:latest
  temperature: 0.2
  max_tokens: 4096
  base_url: http://localhost:11434
```

```bash
OLLAMA_BASE_URL=http://localhost:11434
# Pas de clé API nécessaire !
```

Le code de l'application reste identique, seule la configuration change !
