"""
Configuration loader for the contract test generation system.
Loads and validates configuration from YAML files and environment variables.

Author: Aurel IKAMA HONEY
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

class LLMConfig(BaseModel):
    """Configuration for a single LLM model."""
    provider: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 4096
    base_url: Optional[str] = None
    
class AgentConfig(BaseModel):
    """Configuration for a single agent."""
    name: str
    description: str
    max_retries: int = 3
    timeout: int = 120
    consensus: Optional[Dict[str, Any]] = None

class DatabaseConfig(BaseModel):
    """Database configuration."""
    url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    pool_size: int = 10
    max_overflow: int = 20
    
class RedisConfig(BaseModel):
    """Redis configuration."""
    url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", ""))
    max_connections: int = 50

class Config(BaseModel):
    """Main application configuration."""
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    llm_models: Dict[str, LLMConfig] = {}
    agents: Dict[str, AgentConfig] = {}
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    mlflow_tracking_uri: str = Field(default_factory=lambda: os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        valid_envs = ["development", "test", "production"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v

def x_load_yaml_config__mutmut_orig(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_1(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_2(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(None)
    
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_3(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(None, "r") as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_4(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, None) as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_5(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open("r") as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_6(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, ) as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_7(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, "XXrXX") as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_8(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, "R") as f:
        return yaml.safe_load(f)

def x_load_yaml_config__mutmut_9(filepath: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        filepath: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, "r") as f:
        return yaml.safe_load(None)

x_load_yaml_config__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_yaml_config__mutmut_1': x_load_yaml_config__mutmut_1, 
    'x_load_yaml_config__mutmut_2': x_load_yaml_config__mutmut_2, 
    'x_load_yaml_config__mutmut_3': x_load_yaml_config__mutmut_3, 
    'x_load_yaml_config__mutmut_4': x_load_yaml_config__mutmut_4, 
    'x_load_yaml_config__mutmut_5': x_load_yaml_config__mutmut_5, 
    'x_load_yaml_config__mutmut_6': x_load_yaml_config__mutmut_6, 
    'x_load_yaml_config__mutmut_7': x_load_yaml_config__mutmut_7, 
    'x_load_yaml_config__mutmut_8': x_load_yaml_config__mutmut_8, 
    'x_load_yaml_config__mutmut_9': x_load_yaml_config__mutmut_9
}

def load_yaml_config(*args, **kwargs):
    result = _mutmut_trampoline(x_load_yaml_config__mutmut_orig, x_load_yaml_config__mutmut_mutants, args, kwargs)
    return result 

load_yaml_config.__signature__ = _mutmut_signature(x_load_yaml_config__mutmut_orig)
x_load_yaml_config__mutmut_orig.__name__ = 'x_load_yaml_config'

def x_load_config__mutmut_orig() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_1() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = None
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_2() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path(None)
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_3() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("XXconfigXX")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_4() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("CONFIG")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_5() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = None
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_6() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir * "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_7() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "XXllm_config.yamlXX"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_8() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "LLM_CONFIG.YAML"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_9() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = None
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_10() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(None) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_11() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = None
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_12() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir * "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_13() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "XXagents_config.yamlXX"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_14() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "AGENTS_CONFIG.YAML"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_15() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = None
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_16() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(None) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_17() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = None
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_18() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir * "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_19() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "XXmetrics_config.yamlXX"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_20() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "METRICS_CONFIG.YAML"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_21() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = None
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_22() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(None) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_23() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = None
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_24() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").upper() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_25() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv(None, "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_26() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", None).lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_27() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_28() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", ).lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_29() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("XXENABLE_CLOUD_MODELSXX", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_30() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("enable_cloud_models", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_31() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "XXfalseXX").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_32() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "FALSE").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_33() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() != "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_34() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "XXtrueXX"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_35() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "TRUE"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_36() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = None
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_37() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"XXopenaiXX", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_38() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"OPENAI", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_39() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "XXanthropicXX", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_40() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "ANTHROPIC", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_41() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "XXgoogleXX"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_42() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "GOOGLE"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_43() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = None
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_44() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = ""
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_45() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data or "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_46() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "XXllmXX" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_47() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "LLM" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_48() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" not in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_49() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "XXmodelsXX" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_50() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "MODELS" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_51() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" not in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_52() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["XXllmXX"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_53() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["LLM"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_54() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["XXllmXX"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_55() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["LLM"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_56() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["XXmodelsXX"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_57() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["MODELS"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_58() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = None
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_59() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get(None, "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_60() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", None)
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_61() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_62() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", )
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_63() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("XXproviderXX", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_64() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("PROVIDER", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_65() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "XXXX")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_66() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models or provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_67() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_68() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider not in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_69() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                break
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_70() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = None
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_71() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" or ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_72() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider != "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_73() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "XXollamaXX" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_74() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "OLLAMA" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_75() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is not None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_76() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = None
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_77() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = None
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_78() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "XXagentsXX" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_79() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "AGENTS" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_80() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" not in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_81() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["XXagentsXX"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_82() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["AGENTS"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_83() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = None
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_84() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback or "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_85() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models or ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_86() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_87() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "XXllmXX" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_88() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "LLM" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_89() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" not in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_90() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = None
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_91() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get(None, {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_92() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", None)
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_93() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get({})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_94() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", )
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_95() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["XXllmXX"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_96() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["LLM"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_97() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("XXdefault_modelsXX", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_98() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("DEFAULT_MODELS", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_99() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = None
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_100() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(None, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_101() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, None)
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_102() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get({})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_103() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, )
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_104() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["XXllmXX"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_105() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["LLM"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_106() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["XXmodelsXX"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_107() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["MODELS"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_108() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get(None) in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_109() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("XXproviderXX") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_110() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("PROVIDER") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_111() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") not in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_112() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = None
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_113() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["XXllmXX"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_114() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["LLM"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_115() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["XXdefault_modelsXX"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_116() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["DEFAULT_MODELS"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_117() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = None
    
    return config

def x_load_config__mutmut_118() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=None,
        agents=agents
    )
    
    return config

def x_load_config__mutmut_119() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=None
    )
    
    return config

def x_load_config__mutmut_120() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        agents=agents
    )
    
    return config

def x_load_config__mutmut_121() -> Config:
    """
    Load complete application configuration.
    
    Returns:
        Config object with all settings
    """
    config_dir = Path("config")
    
    # Load LLM configuration
    llm_config_path = config_dir / "llm_config.yaml"
    llm_data = load_yaml_config(llm_config_path) if llm_config_path.exists() else {}
    
    # Load agents configuration
    agents_config_path = config_dir / "agents_config.yaml"
    agents_data = load_yaml_config(agents_config_path) if agents_config_path.exists() else {}
    
    # Load metrics configuration
    metrics_config_path = config_dir / "metrics_config.yaml"
    metrics_data = load_yaml_config(metrics_config_path) if metrics_config_path.exists() else {}
    
    # Check if cloud models are enabled (cost optimization)
    enable_cloud_models = os.getenv("ENABLE_CLOUD_MODELS", "false").lower() == "true"
    cloud_providers = {"openai", "anthropic", "google"}
    
    # Parse LLM models
    llm_models = {}
    ollama_fallback = None
    
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            provider = model_config.get("provider", "")
            
            # Skip cloud models if disabled
            if not enable_cloud_models and provider in cloud_providers:
                continue
            
            llm_models[name] = LLMConfig(**model_config)
            
            # Find first Ollama model as fallback
            if provider == "ollama" and ollama_fallback is None:
                ollama_fallback = name
    
    # Parse agents and apply fallback if needed
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Update default models to use Ollama fallback if cloud is disabled
    if not enable_cloud_models and ollama_fallback and "llm" in llm_data:
        default_models = llm_data["llm"].get("default_models", {})
        for agent_name, model_name in default_models.items():
            model_config = llm_data["llm"]["models"].get(model_name, {})
            if model_config.get("provider") in cloud_providers:
                # Update to use Ollama fallback
                llm_data["llm"]["default_models"][agent_name] = ollama_fallback
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        )
    
    return config

x_load_config__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_config__mutmut_1': x_load_config__mutmut_1, 
    'x_load_config__mutmut_2': x_load_config__mutmut_2, 
    'x_load_config__mutmut_3': x_load_config__mutmut_3, 
    'x_load_config__mutmut_4': x_load_config__mutmut_4, 
    'x_load_config__mutmut_5': x_load_config__mutmut_5, 
    'x_load_config__mutmut_6': x_load_config__mutmut_6, 
    'x_load_config__mutmut_7': x_load_config__mutmut_7, 
    'x_load_config__mutmut_8': x_load_config__mutmut_8, 
    'x_load_config__mutmut_9': x_load_config__mutmut_9, 
    'x_load_config__mutmut_10': x_load_config__mutmut_10, 
    'x_load_config__mutmut_11': x_load_config__mutmut_11, 
    'x_load_config__mutmut_12': x_load_config__mutmut_12, 
    'x_load_config__mutmut_13': x_load_config__mutmut_13, 
    'x_load_config__mutmut_14': x_load_config__mutmut_14, 
    'x_load_config__mutmut_15': x_load_config__mutmut_15, 
    'x_load_config__mutmut_16': x_load_config__mutmut_16, 
    'x_load_config__mutmut_17': x_load_config__mutmut_17, 
    'x_load_config__mutmut_18': x_load_config__mutmut_18, 
    'x_load_config__mutmut_19': x_load_config__mutmut_19, 
    'x_load_config__mutmut_20': x_load_config__mutmut_20, 
    'x_load_config__mutmut_21': x_load_config__mutmut_21, 
    'x_load_config__mutmut_22': x_load_config__mutmut_22, 
    'x_load_config__mutmut_23': x_load_config__mutmut_23, 
    'x_load_config__mutmut_24': x_load_config__mutmut_24, 
    'x_load_config__mutmut_25': x_load_config__mutmut_25, 
    'x_load_config__mutmut_26': x_load_config__mutmut_26, 
    'x_load_config__mutmut_27': x_load_config__mutmut_27, 
    'x_load_config__mutmut_28': x_load_config__mutmut_28, 
    'x_load_config__mutmut_29': x_load_config__mutmut_29, 
    'x_load_config__mutmut_30': x_load_config__mutmut_30, 
    'x_load_config__mutmut_31': x_load_config__mutmut_31, 
    'x_load_config__mutmut_32': x_load_config__mutmut_32, 
    'x_load_config__mutmut_33': x_load_config__mutmut_33, 
    'x_load_config__mutmut_34': x_load_config__mutmut_34, 
    'x_load_config__mutmut_35': x_load_config__mutmut_35, 
    'x_load_config__mutmut_36': x_load_config__mutmut_36, 
    'x_load_config__mutmut_37': x_load_config__mutmut_37, 
    'x_load_config__mutmut_38': x_load_config__mutmut_38, 
    'x_load_config__mutmut_39': x_load_config__mutmut_39, 
    'x_load_config__mutmut_40': x_load_config__mutmut_40, 
    'x_load_config__mutmut_41': x_load_config__mutmut_41, 
    'x_load_config__mutmut_42': x_load_config__mutmut_42, 
    'x_load_config__mutmut_43': x_load_config__mutmut_43, 
    'x_load_config__mutmut_44': x_load_config__mutmut_44, 
    'x_load_config__mutmut_45': x_load_config__mutmut_45, 
    'x_load_config__mutmut_46': x_load_config__mutmut_46, 
    'x_load_config__mutmut_47': x_load_config__mutmut_47, 
    'x_load_config__mutmut_48': x_load_config__mutmut_48, 
    'x_load_config__mutmut_49': x_load_config__mutmut_49, 
    'x_load_config__mutmut_50': x_load_config__mutmut_50, 
    'x_load_config__mutmut_51': x_load_config__mutmut_51, 
    'x_load_config__mutmut_52': x_load_config__mutmut_52, 
    'x_load_config__mutmut_53': x_load_config__mutmut_53, 
    'x_load_config__mutmut_54': x_load_config__mutmut_54, 
    'x_load_config__mutmut_55': x_load_config__mutmut_55, 
    'x_load_config__mutmut_56': x_load_config__mutmut_56, 
    'x_load_config__mutmut_57': x_load_config__mutmut_57, 
    'x_load_config__mutmut_58': x_load_config__mutmut_58, 
    'x_load_config__mutmut_59': x_load_config__mutmut_59, 
    'x_load_config__mutmut_60': x_load_config__mutmut_60, 
    'x_load_config__mutmut_61': x_load_config__mutmut_61, 
    'x_load_config__mutmut_62': x_load_config__mutmut_62, 
    'x_load_config__mutmut_63': x_load_config__mutmut_63, 
    'x_load_config__mutmut_64': x_load_config__mutmut_64, 
    'x_load_config__mutmut_65': x_load_config__mutmut_65, 
    'x_load_config__mutmut_66': x_load_config__mutmut_66, 
    'x_load_config__mutmut_67': x_load_config__mutmut_67, 
    'x_load_config__mutmut_68': x_load_config__mutmut_68, 
    'x_load_config__mutmut_69': x_load_config__mutmut_69, 
    'x_load_config__mutmut_70': x_load_config__mutmut_70, 
    'x_load_config__mutmut_71': x_load_config__mutmut_71, 
    'x_load_config__mutmut_72': x_load_config__mutmut_72, 
    'x_load_config__mutmut_73': x_load_config__mutmut_73, 
    'x_load_config__mutmut_74': x_load_config__mutmut_74, 
    'x_load_config__mutmut_75': x_load_config__mutmut_75, 
    'x_load_config__mutmut_76': x_load_config__mutmut_76, 
    'x_load_config__mutmut_77': x_load_config__mutmut_77, 
    'x_load_config__mutmut_78': x_load_config__mutmut_78, 
    'x_load_config__mutmut_79': x_load_config__mutmut_79, 
    'x_load_config__mutmut_80': x_load_config__mutmut_80, 
    'x_load_config__mutmut_81': x_load_config__mutmut_81, 
    'x_load_config__mutmut_82': x_load_config__mutmut_82, 
    'x_load_config__mutmut_83': x_load_config__mutmut_83, 
    'x_load_config__mutmut_84': x_load_config__mutmut_84, 
    'x_load_config__mutmut_85': x_load_config__mutmut_85, 
    'x_load_config__mutmut_86': x_load_config__mutmut_86, 
    'x_load_config__mutmut_87': x_load_config__mutmut_87, 
    'x_load_config__mutmut_88': x_load_config__mutmut_88, 
    'x_load_config__mutmut_89': x_load_config__mutmut_89, 
    'x_load_config__mutmut_90': x_load_config__mutmut_90, 
    'x_load_config__mutmut_91': x_load_config__mutmut_91, 
    'x_load_config__mutmut_92': x_load_config__mutmut_92, 
    'x_load_config__mutmut_93': x_load_config__mutmut_93, 
    'x_load_config__mutmut_94': x_load_config__mutmut_94, 
    'x_load_config__mutmut_95': x_load_config__mutmut_95, 
    'x_load_config__mutmut_96': x_load_config__mutmut_96, 
    'x_load_config__mutmut_97': x_load_config__mutmut_97, 
    'x_load_config__mutmut_98': x_load_config__mutmut_98, 
    'x_load_config__mutmut_99': x_load_config__mutmut_99, 
    'x_load_config__mutmut_100': x_load_config__mutmut_100, 
    'x_load_config__mutmut_101': x_load_config__mutmut_101, 
    'x_load_config__mutmut_102': x_load_config__mutmut_102, 
    'x_load_config__mutmut_103': x_load_config__mutmut_103, 
    'x_load_config__mutmut_104': x_load_config__mutmut_104, 
    'x_load_config__mutmut_105': x_load_config__mutmut_105, 
    'x_load_config__mutmut_106': x_load_config__mutmut_106, 
    'x_load_config__mutmut_107': x_load_config__mutmut_107, 
    'x_load_config__mutmut_108': x_load_config__mutmut_108, 
    'x_load_config__mutmut_109': x_load_config__mutmut_109, 
    'x_load_config__mutmut_110': x_load_config__mutmut_110, 
    'x_load_config__mutmut_111': x_load_config__mutmut_111, 
    'x_load_config__mutmut_112': x_load_config__mutmut_112, 
    'x_load_config__mutmut_113': x_load_config__mutmut_113, 
    'x_load_config__mutmut_114': x_load_config__mutmut_114, 
    'x_load_config__mutmut_115': x_load_config__mutmut_115, 
    'x_load_config__mutmut_116': x_load_config__mutmut_116, 
    'x_load_config__mutmut_117': x_load_config__mutmut_117, 
    'x_load_config__mutmut_118': x_load_config__mutmut_118, 
    'x_load_config__mutmut_119': x_load_config__mutmut_119, 
    'x_load_config__mutmut_120': x_load_config__mutmut_120, 
    'x_load_config__mutmut_121': x_load_config__mutmut_121
}

def load_config(*args, **kwargs):
    result = _mutmut_trampoline(x_load_config__mutmut_orig, x_load_config__mutmut_mutants, args, kwargs)
    return result 

load_config.__signature__ = _mutmut_signature(x_load_config__mutmut_orig)
x_load_config__mutmut_orig.__name__ = 'x_load_config'

# Global configuration instance
_config: Optional[Config] = None

def x_get_config__mutmut_orig() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config object
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config

def x_get_config__mutmut_1() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config object
    """
    global _config
    if _config is not None:
        _config = load_config()
    return _config

def x_get_config__mutmut_2() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config object
    """
    global _config
    if _config is None:
        _config = None
    return _config

x_get_config__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_config__mutmut_1': x_get_config__mutmut_1, 
    'x_get_config__mutmut_2': x_get_config__mutmut_2
}

def get_config(*args, **kwargs):
    result = _mutmut_trampoline(x_get_config__mutmut_orig, x_get_config__mutmut_mutants, args, kwargs)
    return result 

get_config.__signature__ = _mutmut_signature(x_get_config__mutmut_orig)
x_get_config__mutmut_orig.__name__ = 'x_get_config'

def x_reload_config__mutmut_orig() -> Config:
    """
    Reload the configuration from files.
    
    Returns:
        New Config object
    """
    global _config
    _config = load_config()
    return _config

def x_reload_config__mutmut_1() -> Config:
    """
    Reload the configuration from files.
    
    Returns:
        New Config object
    """
    global _config
    _config = None
    return _config

x_reload_config__mutmut_mutants : ClassVar[MutantDict] = {
'x_reload_config__mutmut_1': x_reload_config__mutmut_1
}

def reload_config(*args, **kwargs):
    result = _mutmut_trampoline(x_reload_config__mutmut_orig, x_reload_config__mutmut_mutants, args, kwargs)
    return result 

reload_config.__signature__ = _mutmut_signature(x_reload_config__mutmut_orig)
x_reload_config__mutmut_orig.__name__ = 'x_reload_config'

__all__ = ["Config", "LLMConfig", "AgentConfig", "get_config", "reload_config", "load_config"]
