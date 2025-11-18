"""
Unified LLM client for interacting with different language models.
Supports OpenAI, Anthropic, Google, Mistral, and Ollama (Llama).
"""
import os
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Base class for LLM clients."""
    
    def __init__(self, model: str, temperature: float = 0.2, max_tokens: int = 4096):
        """
        Initialize the LLM client.
        
        Args:
            model: Model name/identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def generate_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate text from a list of messages (chat format).
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters
            
        Returns:
            Generated text
        """
        pass


class OpenAIClient(BaseLLMClient):
    """Client for OpenAI models (GPT-4, etc.)."""
    
    def __init__(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def generate_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content


class AnthropicClient(BaseLLMClient):
    """Client for Anthropic models (Claude)."""
    
    def __init__(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def generate_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text


class OllamaClient(BaseLLMClient):
    """Client for Ollama models (Llama, etc.)."""
    
    def __init__(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def generate_with_messages(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]


class LLMClientFactory:
    """Factory for creating LLM clients."""
    
    _clients = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "ollama": OllamaClient,
    }
    
    @classmethod
    def create(cls, provider: str, model: str, **kwargs) -> BaseLLMClient:
        """
        Create an LLM client.
        
        Args:
            provider: Provider name (openai, anthropic, ollama)
            model: Model name
            **kwargs: Additional parameters
            
        Returns:
            LLM client instance
        """
        client_class = cls._clients.get(provider.lower())
        if not client_class:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls._clients.keys())}")
        
        return client_class(model=model, **kwargs)
    
    @classmethod
    def register_client(cls, provider: str, client_class: type):
        """
        Register a new LLM client.
        
        Args:
            provider: Provider name
            client_class: Client class
        """
        cls._clients[provider.lower()] = client_class


__all__ = [
    "BaseLLMClient",
    "OpenAIClient",
    "AnthropicClient",
    "OllamaClient",
    "LLMClientFactory",
]
