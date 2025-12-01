#!/usr/bin/env python3
"""
Script to list all available Ollama models and their details.
"""
import subprocess
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def list_ollama_models():
    """List all available Ollama models."""
    try:
        # Run ollama list command
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("=" * 80)
        print("🤖 AVAILABLE OLLAMA MODELS")
        print("=" * 80)
        print(result.stdout)
        
        # Parse output
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            print("No models found")
            return []
        
        # Skip header line
        models = []
        for line in lines[1:]:
            parts = line.split()
            if parts:
                model_name = parts[0]
                models.append(model_name)
        
        return models
        
    except subprocess.CalledProcessError as e:
        print(f"Error running ollama: {e}")
        return []
    except FileNotFoundError:
        print("Ollama not found. Please install Ollama first.")
        return []


def generate_llm_config(models):
    """Generate LLM configuration for the models."""
    print("\n" + "=" * 80)
    print("📝 SUGGESTED llm_config.yaml CONFIGURATION")
    print("=" * 80)
    
    config = {
        "llm": {
            "models": {},
            "consensus": {
                "enabled": True,
                "models": [],
                "threshold": 0.7
            }
        }
    }
    
    for model in models:
        # Clean model name for config key
        config_key = model.replace(":", "").replace(".", "")
        
        config["llm"]["models"][config_key] = {
            "provider": "ollama",
            "model": model,
            "temperature": 0.2,
            "max_tokens": 4096,
            "base_url": "http://localhost:11434"
        }
        
        config["llm"]["consensus"]["models"].append(config_key)
    
    # Pretty print YAML-like format
    print("\nllm:")
    print("  models:")
    for key, value in config["llm"]["models"].items():
        print(f"    {key}:")
        for k, v in value.items():
            print(f"      {k}: {v}")
        print()
    
    print("  consensus:")
    print(f"    enabled: {config['llm']['consensus']['enabled']}")
    print(f"    models: {config['llm']['consensus']['models']}")
    print(f"    threshold: {config['llm']['consensus']['threshold']}")
    
    return config


def main():
    """Main function."""
    print("\n🔍 Scanning for Ollama models...\n")
    
    models = list_ollama_models()
    
    if models:
        print(f"\n✅ Found {len(models)} model(s)")
        print("\nModels:")
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        
        # Generate configuration
        generate_llm_config(models)
        
        print("\n" + "=" * 80)
        print("💡 USAGE TIPS")
        print("=" * 80)
        print("1. Copy the configuration above to config/llm_config.yaml")
        print("2. Adjust temperature and max_tokens as needed")
        print("3. Set consensus threshold (0.5 = majority, 0.7 = strong agreement, 0.9 = near unanimous)")
        print("4. The Oracle agent will use all models for consensus voting")
        print()
    else:
        print("\n❌ No Ollama models found")
        print("Run: ollama pull <model-name>")
        print("Example: ollama pull mistral, ollama pull llama3.1, ollama pull llama3.2")


if __name__ == "__main__":
    main()
