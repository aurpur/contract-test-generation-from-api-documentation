#!/usr/bin/env python3
"""
Script to verify Ollama installation and available models.
"""
import sys
import requests
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from utils.logging import logger


def check_ollama_service():
    """Check if Ollama service is running."""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        if response.status_code == 200:
            version = response.json().get("version")
            logger.success(f"✓ Ollama service is running (version {version})")
            return True
        else:
            logger.error(f"✗ Ollama service returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("✗ Ollama service is not running")
        logger.info("  Start Ollama: ollama serve")
        return False
    except Exception as e:
        logger.error(f"✗ Error checking Ollama service: {e}")
        return False


def list_models():
    """List all available Ollama models."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            
            if models:
                logger.success(f"✓ Found {len(models)} Ollama models:")
                for model in models:
                    name = model.get("name")
                    size_gb = model.get("size", 0) / (1024**3)
                    modified = model.get("modified_at", "Unknown")
                    logger.info(f"  • {name:<25} {size_gb:>6.2f} GB  Modified: {modified[:10]}")
                return True
            else:
                logger.warning("⚠ No models found")
                logger.info("  Install models: ollama pull mistral")
                return False
        else:
            logger.error(f"✗ Failed to list models (status {response.status_code})")
            return False
    except Exception as e:
        logger.error(f"✗ Error listing models: {e}")
        return False


def test_model(model_name: str):
    """Test a specific model with a simple prompt."""
    try:
        logger.info(f"Testing model: {model_name}...")
        
        payload = {
            "model": model_name,
            "prompt": "Say 'Hello from Ollama!' in one sentence.",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("response", "").strip()
            logger.success(f"✓ Model {model_name} is working")
            logger.info(f"  Response: {generated_text}")
            return True
        else:
            logger.error(f"✗ Model {model_name} failed (status {response.status_code})")
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"✗ Model {model_name} timed out")
        return False
    except Exception as e:
        logger.error(f"✗ Error testing model {model_name}: {e}")
        return False


def main():
    """Main verification function."""
    logger.info("=" * 60)
    logger.info("Ollama Verification Script")
    logger.info("=" * 60)
    
    # Check service
    if not check_ollama_service():
        sys.exit(1)
    
    logger.info("")
    
    # List models
    if not list_models():
        sys.exit(1)
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Testing configured models from llm_config.yaml")
    logger.info("=" * 60)
    
    # Test models
    models_to_test = [
        "mistral:latest",
        "llama3.1:latest",
    ]
    
    all_passed = True
    for model in models_to_test:
        if not test_model(model):
            all_passed = False
        logger.info("")
    
    logger.info("=" * 60)
    if all_passed:
        logger.success("✓ All Ollama models are working correctly!")
    else:
        logger.warning("⚠ Some models failed verification")
    logger.info("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
