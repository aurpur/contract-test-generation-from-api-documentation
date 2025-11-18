"""
Configuration loader for the contract test generation system.
Loads and validates configuration from YAML files and environment variables.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

def load_yaml_config(filepath: Path) -> Dict[str, Any]:
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

def load_config() -> Config:
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
    
    # Parse LLM models
    llm_models = {}
    if "llm" in llm_data and "models" in llm_data["llm"]:
        for name, model_config in llm_data["llm"]["models"].items():
            llm_models[name] = LLMConfig(**model_config)
    
    # Parse agents
    agents = {}
    if "agents" in agents_data:
        for name, agent_config in agents_data["agents"].items():
            agents[name] = AgentConfig(**agent_config)
    
    # Create main config
    config = Config(
        llm_models=llm_models,
        agents=agents
    )
    
    return config

# Global configuration instance
_config: Optional[Config] = None

def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config object
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config

def reload_config() -> Config:
    """
    Reload the configuration from files.
    
    Returns:
        New Config object
    """
    global _config
    _config = load_config()
    return _config

__all__ = ["Config", "LLMConfig", "AgentConfig", "get_config", "reload_config", "load_config"]
