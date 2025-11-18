# Mode Développement Économique - Guide Complet

**Auteur** : Aurel IKAMA HONEY

## Vue d'ensemble

Le projet supporte maintenant un **mode développement économique** qui permet de désactiver les modèles LLM cloud (OpenAI, Anthropic, Google) pour un **coût de 0€** en utilisant uniquement des modèles locaux via Ollama.

## Motivation

### Problème
- Les modèles cloud (GPT-4, Claude, Gemini) sont payants
- Coûts variables pendant le développement et les tests
- Nécessite des clés API pour chaque service
- Dépendance à une connexion internet

### Solution
- **Mode développement** : Utilise uniquement Ollama (Mistral, Llama) - **Gratuit**
- **Mode production** : Active tous les modèles (cloud + Ollama) - **Payant mais performant**
- Configuration simple via une variable d'environnement

## Configuration

### Variable d'environnement

Dans le fichier `.env` :

```bash
# Mode Développement (Coût: 0€)
ENABLE_CLOUD_MODELS=false

# Mode Production (Coût: Variable)
ENABLE_CLOUD_MODELS=true
```

### Prérequis

#### Pour mode développement (ENABLE_CLOUD_MODELS=false)
- ✅ Ollama installé : [ollama.ai](https://ollama.ai)
- ✅ Au moins un modèle Ollama installé :
  ```bash
  ollama pull mistral
  ollama pull llama3.1
  ```
- ❌ Pas besoin de clés API cloud

#### Pour mode production (ENABLE_CLOUD_MODELS=true)
- ✅ Ollama installé (optionnel mais recommandé)
- ✅ Clés API cloud configurées dans `.env` :
  ```bash
  OPENAI_API_KEY=sk-...
  ANTHROPIC_API_KEY=sk-ant-...
  GOOGLE_API_KEY=AIza...
  ```

## Comportement automatique

### Mode développement (ENABLE_CLOUD_MODELS=false)

1. **Filtrage des modèles** : Les modèles cloud sont automatiquement exclus du chargement
2. **Fallback Ollama** : Tous les agents utilisent Ollama par défaut
3. **Économie maximale** : Coût total de 0€
4. **Configuration minimale** : Pas besoin de clés API cloud

**Exemple de configuration chargée :**
```python
llm_models = {
    "mistral": LLMConfig(provider="ollama", model="mistral:latest"),
    "llama": LLMConfig(provider="ollama", model="llama3.1:latest")
}
# gpt4, claude, gemini sont automatiquement exclus
```

### Mode production (ENABLE_CLOUD_MODELS=true)

1. **Tous les modèles** : Cloud + Ollama disponibles
2. **Assignation par défaut** : Chaque agent utilise son modèle configuré dans `llm_config.yaml`
3. **Performance maximale** : Accès aux meilleurs modèles
4. **Coûts variables** : Selon l'utilisation des API cloud

**Exemple de configuration chargée :**
```python
llm_models = {
    "gpt4": LLMConfig(provider="openai", model="gpt-4-turbo-preview"),
    "claude": LLMConfig(provider="anthropic", model="claude-3-sonnet-20240229"),
    "gemini": LLMConfig(provider="google", model="gemini-pro"),
    "mistral": LLMConfig(provider="ollama", model="mistral:latest"),
    "llama": LLMConfig(provider="ollama", model="llama3.1:latest")
}
```

## Implémentation technique

### Modifications apportées

#### 1. `.env.example` et `.env`
```bash
# Nouvelle variable ajoutée
ENABLE_CLOUD_MODELS=false  # Par défaut pour le développement

# Les clés API sont maintenant optionnelles
# (Seulement si ENABLE_CLOUD_MODELS=true)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

#### 2. `src/utils/config.py`
```python
def load_config() -> Config:
    # Check if cloud models are enabled
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    for name, model_config in llm_data["llm"]["models"].items():
        provider = model_config.get("provider", "")
        
        # Skip cloud models if disabled
        if not enable_cloud_models and provider in cloud_providers:
            continue
        
        llm_models[name] = LLMConfig(**model_config)
    
    # Apply Ollama fallback for agents if needed
    if not enable_cloud_models and ollama_fallback:
        for agent_name, model_name in default_models.items():
            if model_name in cloud_providers:
                default_models[agent_name] = ollama_fallback
```

#### 3. `scripts/test_dev_mode.py`
Script de validation qui :
- Vérifie la disponibilité d'Ollama
- Liste les modèles chargés (cloud vs local)
- Calcule le coût estimé
- Valide la configuration

## Tests et validation

### Test du mode développement

```bash
# Assurez-vous que ENABLE_CLOUD_MODELS=false dans .env
python scripts/test_dev_mode.py
```

**Résultat attendu :**
```
✅ Mode développement économique activé
   → Coût: 0€ (utilisation exclusive d'Ollama)

📦 Modèles LLM chargés: 2
   🏠 mistral: mistral:latest (provider: ollama)
   🏠 llama: llama3.1:latest (provider: ollama)

Modèles Cloud (payants): 0
   ✅ Aucun modèle cloud chargé (économie maximale)

💰 COÛT ESTIMÉ:
   • Modèles cloud: 0€ (désactivés)
   • Modèles Ollama: 0€ (local)
   • TOTAL: 0€
```

### Test du mode production

```bash
ENABLE_CLOUD_MODELS=true python scripts/test_dev_mode.py
```

**Résultat attendu :**
```
📦 Modèles LLM chargés: 5
   ☁️  gpt4: gpt-4-turbo-preview (provider: openai)
   ☁️  claude: claude-3-sonnet-20240229 (provider: anthropic)
   ☁️  gemini: gemini-pro (provider: google)
   🏠 mistral: mistral:latest (provider: ollama)
   🏠 llama: llama3.1:latest (provider: ollama)

Modèles Cloud (payants): 3
Modèles Ollama (gratuits): 2

💰 COÛT ESTIMÉ:
   • Modèles cloud: Variable selon usage
   • Modèles Ollama: 0€ (local)
```

## Comparaison des coûts

### Mode développement (ENABLE_CLOUD_MODELS=false)

| Ressource | Coût |
|-----------|------|
| Mistral (Ollama) | 0€ |
| Llama 3.1 (Ollama) | 0€ |
| **TOTAL** | **0€** |

**Avantages :**
- ✅ Coût nul
- ✅ Tests illimités
- ✅ Confidentialité totale
- ✅ Disponibilité hors ligne
- ✅ Pas de quota

**Inconvénients :**
- ⚠️ Performance inférieure aux modèles cloud pour certaines tâches
- ⚠️ Nécessite des ressources machine (RAM, stockage)

### Mode production (ENABLE_CLOUD_MODELS=true)

| Ressource | Coût estimé |
|-----------|-------------|
| GPT-4 Turbo | ~$0.01/1K tokens (input), ~$0.03/1K tokens (output) |
| Claude 3 Sonnet | ~$0.003/1K tokens (input), ~$0.015/1K tokens (output) |
| Gemini Pro | ~$0.0005/1K tokens |
| Mistral (Ollama) | 0€ |
| Llama 3.1 (Ollama) | 0€ |
| **TOTAL** | **Variable selon usage** |

**Avantages :**
- ✅ Performance maximale
- ✅ Meilleure qualité pour tâches complexes
- ✅ Pas de ressources machine nécessaires (cloud)

**Inconvénients :**
- ⚠️ Coûts variables et potentiellement élevés
- ⚠️ Dépendance internet
- ⚠️ Quotas et limites de taux
- ⚠️ Données envoyées aux services cloud

## Cas d'usage recommandés

### Utilisez le mode développement (ENABLE_CLOUD_MODELS=false) pour :
- 🔧 Développement local et tests
- 🧪 Expérimentations et prototypage
- 📚 Apprentissage et formation
- 🔐 Projets nécessitant une confidentialité totale
- 💰 Budgets limités ou phase de recherche

### Utilisez le mode production (ENABLE_CLOUD_MODELS=true) pour :
- 🚀 Déploiement en production
- 📊 Expérimentations nécessitant les meilleurs modèles (RQ4)
- 🎯 Tâches complexes nécessitant GPT-4 ou Claude
- ⚖️ Comparaison de performances entre modèles
- 📈 Génération de résultats pour publication

## Migration entre modes

### De production vers développement

1. Modifier `.env` :
   ```bash
   ENABLE_CLOUD_MODELS=false
   ```

2. Vérifier :
   ```bash
   python scripts/test_dev_mode.py
   ```

3. Relancer l'application :
   ```bash
   python src/main.py
   ```

**Pas de modification de code nécessaire !**

### De développement vers production

1. Ajouter les clés API dans `.env` :
   ```bash
   ENABLE_CLOUD_MODELS=true
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=AIza...
   ```

2. Vérifier :
   ```bash
   python scripts/test_dev_mode.py
   ```

3. Relancer l'application :
   ```bash
   python src/main.py
   ```

## Dépannage

### Problème : Aucun modèle chargé en mode développement

**Cause :** Ollama non installé ou aucun modèle disponible

**Solution :**
```bash
# Installer Ollama
# Télécharger depuis https://ollama.ai

# Installer les modèles
ollama pull mistral
ollama pull llama3.1

# Vérifier
python scripts/verify_ollama.py
```

### Problème : Les modèles cloud sont chargés malgré ENABLE_CLOUD_MODELS=false

**Cause :** Variable d'environnement non prise en compte

**Solution :**
```bash
# Vérifier le fichier .env
cat .env | grep ENABLE_CLOUD_MODELS

# Doit afficher : ENABLE_CLOUD_MODELS=false

# Relancer avec la variable explicite
ENABLE_CLOUD_MODELS=false python src/main.py
```

### Problème : Erreurs API en mode production

**Cause :** Clés API manquantes ou invalides

**Solution :**
```bash
# Vérifier les clés dans .env
cat .env | grep API_KEY

# Tester individuellement
# TODO: Créer scripts/verify_api_keys.py
```

## Évolutions futures

### Prévues
- [ ] Script `verify_api_keys.py` pour tester les clés cloud
- [ ] Configuration par agent (certains en cloud, d'autres en local)
- [ ] Métriques de coût en temps réel
- [ ] Dashboard de suivi des coûts par modèle

### Possibles
- [ ] Mode hybride intelligent (fallback automatique cloud → Ollama)
- [ ] Limitation de budget par session
- [ ] Cache des réponses pour réduire les coûts
- [ ] Support d'autres providers locaux (LM Studio, etc.)

## Références

- Documentation Ollama : [docs/OLLAMA_SETUP.md](OLLAMA_SETUP.md)
- Configuration LLM : [config/llm_config.yaml](../config/llm_config.yaml)
- Script de test : [scripts/test_dev_mode.py](../scripts/test_dev_mode.py)
- Configuration principale : [src/utils/config.py](../src/utils/config.py)

---

**Dernière mise à jour :** 2025-11-18  
**Version :** 1.0.0  
