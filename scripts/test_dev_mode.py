#!/usr/bin/env python3
"""
Script de test pour vérifier le mode développement économique.
Teste le fonctionnement avec ENABLE_CLOUD_MODELS=false.
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import load_config
from src.utils.logging import setup_logging

def test_dev_mode():
    """Test le mode développement avec uniquement Ollama."""
    print("=" * 70)
    print("🧪 TEST MODE DÉVELOPPEMENT ÉCONOMIQUE")
    print("=" * 70)
    print()
    
    # Setup logging
    setup_logging()
    
    # Check environment variable
    enable_cloud = os.getenv("ENABLE_CLOUD_MODELS", "false").lower()
    print(f"📋 Variable d'environnement ENABLE_CLOUD_MODELS: {enable_cloud}")
    print()
    
    if enable_cloud == "true":
        print("⚠️  ATTENTION: Les modèles cloud sont activés!")
        print("   Pour tester le mode économique, configurez:")
        print("   ENABLE_CLOUD_MODELS=false dans .env")
        print()
    else:
        print("✅ Mode développement économique activé")
        print("   → Coût: 0€ (utilisation exclusive d'Ollama)")
        print()
    
    # Load configuration
    try:
        config = load_config()
        print(f"✅ Configuration chargée: {config.environment}")
        print()
    except Exception as e:
        print(f"❌ Erreur lors du chargement de la configuration: {e}")
        return False
    
    # Check loaded models
    print(f"📦 Modèles LLM chargés: {len(config.llm_models)}")
    print()
    
    cloud_models = []
    ollama_models = []
    
    for name, model in config.llm_models.items():
        provider = model.provider
        model_name = model.model
        
        if provider in ["openai", "anthropic", "google"]:
            cloud_models.append(f"{name} ({provider})")
            print(f"   ☁️  {name}: {model_name} (provider: {provider})")
        elif provider == "ollama":
            ollama_models.append(f"{name} ({model_name})")
            print(f"   🏠 {name}: {model_name} (provider: {provider})")
        else:
            print(f"   ❓ {name}: {model_name} (provider: {provider})")
    
    print()
    
    # Summary
    print("=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    print()
    print(f"Modèles Cloud (payants): {len(cloud_models)}")
    for model in cloud_models:
        print(f"   • {model}")
    if not cloud_models:
        print("   ✅ Aucun modèle cloud chargé (économie maximale)")
    
    print()
    print(f"Modèles Ollama (gratuits): {len(ollama_models)}")
    for model in ollama_models:
        print(f"   • {model}")
    if not ollama_models:
        print("   ⚠️  Aucun modèle Ollama trouvé!")
        print("   Installez au moins un modèle: ollama pull mistral")
        return False
    
    print()
    
    # Validation
    if enable_cloud == "false":
        if cloud_models:
            print("❌ ÉCHEC: Des modèles cloud sont chargés alors que ENABLE_CLOUD_MODELS=false")
            print("   Vérifiez la configuration dans src/utils/config.py")
            return False
        elif ollama_models:
            print("✅ SUCCÈS: Mode développement économique fonctionnel!")
            print()
            print("💰 COÛT ESTIMÉ:")
            print(f"   • Modèles cloud: 0€ (désactivés)")
            print(f"   • Modèles Ollama: 0€ (local)")
            print(f"   • TOTAL: 0€")
            print()
            print("🎯 AVANTAGES:")
            print("   ✓ Développement sans frais d'API")
            print("   ✓ Tests illimités en local")
            print("   ✓ Confidentialité des données")
            print("   ✓ Disponibilité hors ligne")
            return True
        else:
            print("⚠️  AVERTISSEMENT: Aucun modèle disponible")
            return False
    else:
        print("ℹ️  INFO: Mode production (cloud + Ollama)")
        print()
        print("💰 COÛT ESTIMÉ:")
        print(f"   • Modèles cloud: Variable selon usage")
        print(f"   • Modèles Ollama: 0€ (local)")
        print()
        return True

def test_ollama_availability():
    """Vérifie si Ollama est disponible."""
    print()
    print("=" * 70)
    print("🔍 VÉRIFICATION OLLAMA")
    print("=" * 70)
    print()
    
    try:
        import requests
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        response = requests.get(f"{ollama_url}/api/version", timeout=5)
        
        if response.status_code == 200:
            version_data = response.json()
            version = version_data.get("version", "unknown")
            print(f"✅ Ollama disponible: version {version}")
            print(f"   URL: {ollama_url}")
            return True
        else:
            print(f"❌ Ollama répond avec le code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Ollama non disponible sur {ollama_url}")
        print("   Démarrez Ollama: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification Ollama: {e}")
        return False

def main():
    """Point d'entrée principal."""
    try:
        # Test Ollama availability
        ollama_ok = test_ollama_availability()
        
        # Test development mode
        dev_mode_ok = test_dev_mode()
        
        print()
        print("=" * 70)
        
        if ollama_ok and dev_mode_ok:
            print("✅ TOUS LES TESTS RÉUSSIS!")
            print()
            print("🚀 Vous pouvez maintenant développer avec un coût de 0€")
            print("   en utilisant uniquement Ollama (Mistral et Llama)")
            sys.exit(0)
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            print()
            if not ollama_ok:
                print("🔧 Action requise: Installer et démarrer Ollama")
                print("   1. Télécharger: https://ollama.ai")
                print("   2. Installer un modèle: ollama pull mistral")
                print("   3. Démarrer le service: ollama serve")
            if not dev_mode_ok:
                print("🔧 Action requise: Vérifier la configuration")
                print("   1. Vérifier .env: ENABLE_CLOUD_MODELS=false")
                print("   2. Relancer le test: python scripts/test_dev_mode.py")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
