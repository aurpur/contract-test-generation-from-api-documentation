"""Unified LLM client for interacting with different language models.
Supports OpenAI, Anthropic, Google, Mistral, and Ollama (Llama).

Author: Aurel IKAMA HONEY
"""
import os
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
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


class BaseLLMClient(ABC):
    """Base class for LLM clients."""
    
    def xǁBaseLLMClientǁ__init____mutmut_orig(self, model: str, temperature: float = 0.2, max_tokens: int = 4096):
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
    
    def xǁBaseLLMClientǁ__init____mutmut_1(self, model: str, temperature: float = 1.2, max_tokens: int = 4096):
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
    
    def xǁBaseLLMClientǁ__init____mutmut_2(self, model: str, temperature: float = 0.2, max_tokens: int = 4097):
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
    
    def xǁBaseLLMClientǁ__init____mutmut_3(self, model: str, temperature: float = 0.2, max_tokens: int = 4096):
        """
        Initialize the LLM client.
        
        Args:
            model: Model name/identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.model = None
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def xǁBaseLLMClientǁ__init____mutmut_4(self, model: str, temperature: float = 0.2, max_tokens: int = 4096):
        """
        Initialize the LLM client.
        
        Args:
            model: Model name/identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.model = model
        self.temperature = None
        self.max_tokens = max_tokens
    
    def xǁBaseLLMClientǁ__init____mutmut_5(self, model: str, temperature: float = 0.2, max_tokens: int = 4096):
        """
        Initialize the LLM client.
        
        Args:
            model: Model name/identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = None
    
    xǁBaseLLMClientǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseLLMClientǁ__init____mutmut_1': xǁBaseLLMClientǁ__init____mutmut_1, 
        'xǁBaseLLMClientǁ__init____mutmut_2': xǁBaseLLMClientǁ__init____mutmut_2, 
        'xǁBaseLLMClientǁ__init____mutmut_3': xǁBaseLLMClientǁ__init____mutmut_3, 
        'xǁBaseLLMClientǁ__init____mutmut_4': xǁBaseLLMClientǁ__init____mutmut_4, 
        'xǁBaseLLMClientǁ__init____mutmut_5': xǁBaseLLMClientǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseLLMClientǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBaseLLMClientǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBaseLLMClientǁ__init____mutmut_orig)
    xǁBaseLLMClientǁ__init____mutmut_orig.__name__ = 'xǁBaseLLMClientǁ__init__'
    
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
    
    def xǁOpenAIClientǁ__init____mutmut_orig(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_1(self, model: str = "XXgpt-4-turbo-previewXX", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_2(self, model: str = "GPT-4-TURBO-PREVIEW", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_3(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(None, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_4(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_5(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, )
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_6(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = None
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_7(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv(None)
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_8(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("XXOPENAI_API_KEYXX")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_9(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("openai_api_key")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_10(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_11(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(None)
    
    def xǁOpenAIClientǁ__init____mutmut_12(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("XXOPENAI_API_KEY not found in environment variablesXX")
    
    def xǁOpenAIClientǁ__init____mutmut_13(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("openai_api_key not found in environment variables")
    
    def xǁOpenAIClientǁ__init____mutmut_14(self, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY NOT FOUND IN ENVIRONMENT VARIABLES")
    
    xǁOpenAIClientǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIClientǁ__init____mutmut_1': xǁOpenAIClientǁ__init____mutmut_1, 
        'xǁOpenAIClientǁ__init____mutmut_2': xǁOpenAIClientǁ__init____mutmut_2, 
        'xǁOpenAIClientǁ__init____mutmut_3': xǁOpenAIClientǁ__init____mutmut_3, 
        'xǁOpenAIClientǁ__init____mutmut_4': xǁOpenAIClientǁ__init____mutmut_4, 
        'xǁOpenAIClientǁ__init____mutmut_5': xǁOpenAIClientǁ__init____mutmut_5, 
        'xǁOpenAIClientǁ__init____mutmut_6': xǁOpenAIClientǁ__init____mutmut_6, 
        'xǁOpenAIClientǁ__init____mutmut_7': xǁOpenAIClientǁ__init____mutmut_7, 
        'xǁOpenAIClientǁ__init____mutmut_8': xǁOpenAIClientǁ__init____mutmut_8, 
        'xǁOpenAIClientǁ__init____mutmut_9': xǁOpenAIClientǁ__init____mutmut_9, 
        'xǁOpenAIClientǁ__init____mutmut_10': xǁOpenAIClientǁ__init____mutmut_10, 
        'xǁOpenAIClientǁ__init____mutmut_11': xǁOpenAIClientǁ__init____mutmut_11, 
        'xǁOpenAIClientǁ__init____mutmut_12': xǁOpenAIClientǁ__init____mutmut_12, 
        'xǁOpenAIClientǁ__init____mutmut_13': xǁOpenAIClientǁ__init____mutmut_13, 
        'xǁOpenAIClientǁ__init____mutmut_14': xǁOpenAIClientǁ__init____mutmut_14
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIClientǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOpenAIClientǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOpenAIClientǁ__init____mutmut_orig)
    xǁOpenAIClientǁ__init____mutmut_orig.__name__ = 'xǁOpenAIClientǁ__init__'
    
    def xǁOpenAIClientǁgenerate__mutmut_orig(self, prompt: str, **kwargs) -> str:
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
    
    def xǁOpenAIClientǁgenerate__mutmut_1(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = None
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_2(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=None)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_3(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = None
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_4(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=None,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_5(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=None,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_6(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=None,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_7(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=None,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_8(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_9(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_10(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_11(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_12(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_13(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"XXroleXX": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_14(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"ROLE": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_15(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "XXuserXX", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_16(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "USER", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_17(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "XXcontentXX": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_18(self, prompt: str, **kwargs) -> str:
        """Generate text from OpenAI."""
        # Import here to avoid issues if package not installed
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "CONTENT": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate__mutmut_19(self, prompt: str, **kwargs) -> str:
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
        return response.choices[1].message.content
    
    xǁOpenAIClientǁgenerate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIClientǁgenerate__mutmut_1': xǁOpenAIClientǁgenerate__mutmut_1, 
        'xǁOpenAIClientǁgenerate__mutmut_2': xǁOpenAIClientǁgenerate__mutmut_2, 
        'xǁOpenAIClientǁgenerate__mutmut_3': xǁOpenAIClientǁgenerate__mutmut_3, 
        'xǁOpenAIClientǁgenerate__mutmut_4': xǁOpenAIClientǁgenerate__mutmut_4, 
        'xǁOpenAIClientǁgenerate__mutmut_5': xǁOpenAIClientǁgenerate__mutmut_5, 
        'xǁOpenAIClientǁgenerate__mutmut_6': xǁOpenAIClientǁgenerate__mutmut_6, 
        'xǁOpenAIClientǁgenerate__mutmut_7': xǁOpenAIClientǁgenerate__mutmut_7, 
        'xǁOpenAIClientǁgenerate__mutmut_8': xǁOpenAIClientǁgenerate__mutmut_8, 
        'xǁOpenAIClientǁgenerate__mutmut_9': xǁOpenAIClientǁgenerate__mutmut_9, 
        'xǁOpenAIClientǁgenerate__mutmut_10': xǁOpenAIClientǁgenerate__mutmut_10, 
        'xǁOpenAIClientǁgenerate__mutmut_11': xǁOpenAIClientǁgenerate__mutmut_11, 
        'xǁOpenAIClientǁgenerate__mutmut_12': xǁOpenAIClientǁgenerate__mutmut_12, 
        'xǁOpenAIClientǁgenerate__mutmut_13': xǁOpenAIClientǁgenerate__mutmut_13, 
        'xǁOpenAIClientǁgenerate__mutmut_14': xǁOpenAIClientǁgenerate__mutmut_14, 
        'xǁOpenAIClientǁgenerate__mutmut_15': xǁOpenAIClientǁgenerate__mutmut_15, 
        'xǁOpenAIClientǁgenerate__mutmut_16': xǁOpenAIClientǁgenerate__mutmut_16, 
        'xǁOpenAIClientǁgenerate__mutmut_17': xǁOpenAIClientǁgenerate__mutmut_17, 
        'xǁOpenAIClientǁgenerate__mutmut_18': xǁOpenAIClientǁgenerate__mutmut_18, 
        'xǁOpenAIClientǁgenerate__mutmut_19': xǁOpenAIClientǁgenerate__mutmut_19
    }
    
    def generate(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIClientǁgenerate__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIClientǁgenerate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate.__signature__ = _mutmut_signature(xǁOpenAIClientǁgenerate__mutmut_orig)
    xǁOpenAIClientǁgenerate__mutmut_orig.__name__ = 'xǁOpenAIClientǁgenerate'
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_orig(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_1(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = None
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_2(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=None)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_3(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = None
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_4(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=None,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_5(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=None,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_6(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=None,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_7(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=None,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_8(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_9(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_10(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_11(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            **kwargs
        )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_12(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            )
        return response.choices[0].message.content
    
    def xǁOpenAIClientǁgenerate_with_messages__mutmut_13(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
        return response.choices[1].message.content
    
    xǁOpenAIClientǁgenerate_with_messages__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOpenAIClientǁgenerate_with_messages__mutmut_1': xǁOpenAIClientǁgenerate_with_messages__mutmut_1, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_2': xǁOpenAIClientǁgenerate_with_messages__mutmut_2, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_3': xǁOpenAIClientǁgenerate_with_messages__mutmut_3, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_4': xǁOpenAIClientǁgenerate_with_messages__mutmut_4, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_5': xǁOpenAIClientǁgenerate_with_messages__mutmut_5, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_6': xǁOpenAIClientǁgenerate_with_messages__mutmut_6, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_7': xǁOpenAIClientǁgenerate_with_messages__mutmut_7, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_8': xǁOpenAIClientǁgenerate_with_messages__mutmut_8, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_9': xǁOpenAIClientǁgenerate_with_messages__mutmut_9, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_10': xǁOpenAIClientǁgenerate_with_messages__mutmut_10, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_11': xǁOpenAIClientǁgenerate_with_messages__mutmut_11, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_12': xǁOpenAIClientǁgenerate_with_messages__mutmut_12, 
        'xǁOpenAIClientǁgenerate_with_messages__mutmut_13': xǁOpenAIClientǁgenerate_with_messages__mutmut_13
    }
    
    def generate_with_messages(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOpenAIClientǁgenerate_with_messages__mutmut_orig"), object.__getattribute__(self, "xǁOpenAIClientǁgenerate_with_messages__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate_with_messages.__signature__ = _mutmut_signature(xǁOpenAIClientǁgenerate_with_messages__mutmut_orig)
    xǁOpenAIClientǁgenerate_with_messages__mutmut_orig.__name__ = 'xǁOpenAIClientǁgenerate_with_messages'


class AnthropicClient(BaseLLMClient):
    """Client for Anthropic models (Claude)."""
    
    def xǁAnthropicClientǁ__init____mutmut_orig(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_1(self, model: str = "XXclaude-3-sonnet-20240229XX", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_2(self, model: str = "CLAUDE-3-SONNET-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_3(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(None, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_4(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_5(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, )
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_6(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = None
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_7(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv(None)
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_8(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("XXANTHROPIC_API_KEYXX")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_9(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("anthropic_api_key")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_10(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_11(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(None)
    
    def xǁAnthropicClientǁ__init____mutmut_12(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("XXANTHROPIC_API_KEY not found in environment variablesXX")
    
    def xǁAnthropicClientǁ__init____mutmut_13(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("anthropic_api_key not found in environment variables")
    
    def xǁAnthropicClientǁ__init____mutmut_14(self, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(model, **kwargs)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY NOT FOUND IN ENVIRONMENT VARIABLES")
    
    xǁAnthropicClientǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAnthropicClientǁ__init____mutmut_1': xǁAnthropicClientǁ__init____mutmut_1, 
        'xǁAnthropicClientǁ__init____mutmut_2': xǁAnthropicClientǁ__init____mutmut_2, 
        'xǁAnthropicClientǁ__init____mutmut_3': xǁAnthropicClientǁ__init____mutmut_3, 
        'xǁAnthropicClientǁ__init____mutmut_4': xǁAnthropicClientǁ__init____mutmut_4, 
        'xǁAnthropicClientǁ__init____mutmut_5': xǁAnthropicClientǁ__init____mutmut_5, 
        'xǁAnthropicClientǁ__init____mutmut_6': xǁAnthropicClientǁ__init____mutmut_6, 
        'xǁAnthropicClientǁ__init____mutmut_7': xǁAnthropicClientǁ__init____mutmut_7, 
        'xǁAnthropicClientǁ__init____mutmut_8': xǁAnthropicClientǁ__init____mutmut_8, 
        'xǁAnthropicClientǁ__init____mutmut_9': xǁAnthropicClientǁ__init____mutmut_9, 
        'xǁAnthropicClientǁ__init____mutmut_10': xǁAnthropicClientǁ__init____mutmut_10, 
        'xǁAnthropicClientǁ__init____mutmut_11': xǁAnthropicClientǁ__init____mutmut_11, 
        'xǁAnthropicClientǁ__init____mutmut_12': xǁAnthropicClientǁ__init____mutmut_12, 
        'xǁAnthropicClientǁ__init____mutmut_13': xǁAnthropicClientǁ__init____mutmut_13, 
        'xǁAnthropicClientǁ__init____mutmut_14': xǁAnthropicClientǁ__init____mutmut_14
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAnthropicClientǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAnthropicClientǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAnthropicClientǁ__init____mutmut_orig)
    xǁAnthropicClientǁ__init____mutmut_orig.__name__ = 'xǁAnthropicClientǁ__init__'
    
    def xǁAnthropicClientǁgenerate__mutmut_orig(self, prompt: str, **kwargs) -> str:
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
    
    def xǁAnthropicClientǁgenerate__mutmut_1(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = None
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_2(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=None)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_3(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = None
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_4(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=None,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_5(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=None,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_6(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=None,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_7(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=None,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_8(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_9(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_10(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_11(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_12(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
            )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_13(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"XXroleXX": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_14(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"ROLE": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_15(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "XXuserXX", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_16(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "USER", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_17(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "XXcontentXX": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_18(self, prompt: str, **kwargs) -> str:
        """Generate text from Anthropic."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "CONTENT": prompt}],
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate__mutmut_19(self, prompt: str, **kwargs) -> str:
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
        return response.content[1].text
    
    xǁAnthropicClientǁgenerate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAnthropicClientǁgenerate__mutmut_1': xǁAnthropicClientǁgenerate__mutmut_1, 
        'xǁAnthropicClientǁgenerate__mutmut_2': xǁAnthropicClientǁgenerate__mutmut_2, 
        'xǁAnthropicClientǁgenerate__mutmut_3': xǁAnthropicClientǁgenerate__mutmut_3, 
        'xǁAnthropicClientǁgenerate__mutmut_4': xǁAnthropicClientǁgenerate__mutmut_4, 
        'xǁAnthropicClientǁgenerate__mutmut_5': xǁAnthropicClientǁgenerate__mutmut_5, 
        'xǁAnthropicClientǁgenerate__mutmut_6': xǁAnthropicClientǁgenerate__mutmut_6, 
        'xǁAnthropicClientǁgenerate__mutmut_7': xǁAnthropicClientǁgenerate__mutmut_7, 
        'xǁAnthropicClientǁgenerate__mutmut_8': xǁAnthropicClientǁgenerate__mutmut_8, 
        'xǁAnthropicClientǁgenerate__mutmut_9': xǁAnthropicClientǁgenerate__mutmut_9, 
        'xǁAnthropicClientǁgenerate__mutmut_10': xǁAnthropicClientǁgenerate__mutmut_10, 
        'xǁAnthropicClientǁgenerate__mutmut_11': xǁAnthropicClientǁgenerate__mutmut_11, 
        'xǁAnthropicClientǁgenerate__mutmut_12': xǁAnthropicClientǁgenerate__mutmut_12, 
        'xǁAnthropicClientǁgenerate__mutmut_13': xǁAnthropicClientǁgenerate__mutmut_13, 
        'xǁAnthropicClientǁgenerate__mutmut_14': xǁAnthropicClientǁgenerate__mutmut_14, 
        'xǁAnthropicClientǁgenerate__mutmut_15': xǁAnthropicClientǁgenerate__mutmut_15, 
        'xǁAnthropicClientǁgenerate__mutmut_16': xǁAnthropicClientǁgenerate__mutmut_16, 
        'xǁAnthropicClientǁgenerate__mutmut_17': xǁAnthropicClientǁgenerate__mutmut_17, 
        'xǁAnthropicClientǁgenerate__mutmut_18': xǁAnthropicClientǁgenerate__mutmut_18, 
        'xǁAnthropicClientǁgenerate__mutmut_19': xǁAnthropicClientǁgenerate__mutmut_19
    }
    
    def generate(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAnthropicClientǁgenerate__mutmut_orig"), object.__getattribute__(self, "xǁAnthropicClientǁgenerate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate.__signature__ = _mutmut_signature(xǁAnthropicClientǁgenerate__mutmut_orig)
    xǁAnthropicClientǁgenerate__mutmut_orig.__name__ = 'xǁAnthropicClientǁgenerate'
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_orig(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_1(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = None
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_2(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=None)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_3(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = None
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_4(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=None,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_5(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=None,
            temperature=self.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_6(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=None,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_7(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=None,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_8(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_9(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_10(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_11(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            **kwargs
        )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_12(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            )
        return response.content[0].text
    
    def xǁAnthropicClientǁgenerate_with_messages__mutmut_13(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
        return response.content[1].text
    
    xǁAnthropicClientǁgenerate_with_messages__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAnthropicClientǁgenerate_with_messages__mutmut_1': xǁAnthropicClientǁgenerate_with_messages__mutmut_1, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_2': xǁAnthropicClientǁgenerate_with_messages__mutmut_2, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_3': xǁAnthropicClientǁgenerate_with_messages__mutmut_3, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_4': xǁAnthropicClientǁgenerate_with_messages__mutmut_4, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_5': xǁAnthropicClientǁgenerate_with_messages__mutmut_5, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_6': xǁAnthropicClientǁgenerate_with_messages__mutmut_6, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_7': xǁAnthropicClientǁgenerate_with_messages__mutmut_7, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_8': xǁAnthropicClientǁgenerate_with_messages__mutmut_8, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_9': xǁAnthropicClientǁgenerate_with_messages__mutmut_9, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_10': xǁAnthropicClientǁgenerate_with_messages__mutmut_10, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_11': xǁAnthropicClientǁgenerate_with_messages__mutmut_11, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_12': xǁAnthropicClientǁgenerate_with_messages__mutmut_12, 
        'xǁAnthropicClientǁgenerate_with_messages__mutmut_13': xǁAnthropicClientǁgenerate_with_messages__mutmut_13
    }
    
    def generate_with_messages(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAnthropicClientǁgenerate_with_messages__mutmut_orig"), object.__getattribute__(self, "xǁAnthropicClientǁgenerate_with_messages__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate_with_messages.__signature__ = _mutmut_signature(xǁAnthropicClientǁgenerate_with_messages__mutmut_orig)
    xǁAnthropicClientǁgenerate_with_messages__mutmut_orig.__name__ = 'xǁAnthropicClientǁgenerate_with_messages'


class OllamaClient(BaseLLMClient):
    """Client for Ollama models (Llama, etc.)."""
    
    def xǁOllamaClientǁ__init____mutmut_orig(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_1(self, model: str = "XXllama3.1:70bXX", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_2(self, model: str = "LLAMA3.1:70B", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_3(self, model: str = "llama3.1:70b", base_url: str = "XXhttp://localhost:11434XX", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_4(self, model: str = "llama3.1:70b", base_url: str = "HTTP://LOCALHOST:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_5(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(None, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_6(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_7(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, )
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_8(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = None
    
    def xǁOllamaClientǁ__init____mutmut_9(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url and os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_10(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv(None, "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_11(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", None)
    
    def xǁOllamaClientǁ__init____mutmut_12(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_13(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", )
    
    def xǁOllamaClientǁ__init____mutmut_14(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("XXOLLAMA_BASE_URLXX", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_15(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("ollama_base_url", "http://localhost:11434")
    
    def xǁOllamaClientǁ__init____mutmut_16(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "XXhttp://localhost:11434XX")
    
    def xǁOllamaClientǁ__init____mutmut_17(self, model: str = "llama3.1:70b", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model, **kwargs)
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "HTTP://LOCALHOST:11434")
    
    xǁOllamaClientǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaClientǁ__init____mutmut_1': xǁOllamaClientǁ__init____mutmut_1, 
        'xǁOllamaClientǁ__init____mutmut_2': xǁOllamaClientǁ__init____mutmut_2, 
        'xǁOllamaClientǁ__init____mutmut_3': xǁOllamaClientǁ__init____mutmut_3, 
        'xǁOllamaClientǁ__init____mutmut_4': xǁOllamaClientǁ__init____mutmut_4, 
        'xǁOllamaClientǁ__init____mutmut_5': xǁOllamaClientǁ__init____mutmut_5, 
        'xǁOllamaClientǁ__init____mutmut_6': xǁOllamaClientǁ__init____mutmut_6, 
        'xǁOllamaClientǁ__init____mutmut_7': xǁOllamaClientǁ__init____mutmut_7, 
        'xǁOllamaClientǁ__init____mutmut_8': xǁOllamaClientǁ__init____mutmut_8, 
        'xǁOllamaClientǁ__init____mutmut_9': xǁOllamaClientǁ__init____mutmut_9, 
        'xǁOllamaClientǁ__init____mutmut_10': xǁOllamaClientǁ__init____mutmut_10, 
        'xǁOllamaClientǁ__init____mutmut_11': xǁOllamaClientǁ__init____mutmut_11, 
        'xǁOllamaClientǁ__init____mutmut_12': xǁOllamaClientǁ__init____mutmut_12, 
        'xǁOllamaClientǁ__init____mutmut_13': xǁOllamaClientǁ__init____mutmut_13, 
        'xǁOllamaClientǁ__init____mutmut_14': xǁOllamaClientǁ__init____mutmut_14, 
        'xǁOllamaClientǁ__init____mutmut_15': xǁOllamaClientǁ__init____mutmut_15, 
        'xǁOllamaClientǁ__init____mutmut_16': xǁOllamaClientǁ__init____mutmut_16, 
        'xǁOllamaClientǁ__init____mutmut_17': xǁOllamaClientǁ__init____mutmut_17
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaClientǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOllamaClientǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOllamaClientǁ__init____mutmut_orig)
    xǁOllamaClientǁ__init____mutmut_orig.__name__ = 'xǁOllamaClientǁ__init__'
    
    def xǁOllamaClientǁgenerate__mutmut_orig(self, prompt: str, **kwargs) -> str:
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
    
    def xǁOllamaClientǁgenerate__mutmut_1(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = None
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_2(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=None,
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_3(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=None,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_4(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options=None,
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_5(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_6(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_7(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_8(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_9(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "XXtemperatureXX": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_10(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "TEMPERATURE": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_11(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "XXnum_predictXX": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_12(self, prompt: str, **kwargs) -> str:
        """Generate text from Ollama."""
        import ollama
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "NUM_PREDICT": self.max_tokens,
            },
            **kwargs
        )
        return response["response"]
    
    def xǁOllamaClientǁgenerate__mutmut_13(self, prompt: str, **kwargs) -> str:
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
        return response["XXresponseXX"]
    
    def xǁOllamaClientǁgenerate__mutmut_14(self, prompt: str, **kwargs) -> str:
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
        return response["RESPONSE"]
    
    xǁOllamaClientǁgenerate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaClientǁgenerate__mutmut_1': xǁOllamaClientǁgenerate__mutmut_1, 
        'xǁOllamaClientǁgenerate__mutmut_2': xǁOllamaClientǁgenerate__mutmut_2, 
        'xǁOllamaClientǁgenerate__mutmut_3': xǁOllamaClientǁgenerate__mutmut_3, 
        'xǁOllamaClientǁgenerate__mutmut_4': xǁOllamaClientǁgenerate__mutmut_4, 
        'xǁOllamaClientǁgenerate__mutmut_5': xǁOllamaClientǁgenerate__mutmut_5, 
        'xǁOllamaClientǁgenerate__mutmut_6': xǁOllamaClientǁgenerate__mutmut_6, 
        'xǁOllamaClientǁgenerate__mutmut_7': xǁOllamaClientǁgenerate__mutmut_7, 
        'xǁOllamaClientǁgenerate__mutmut_8': xǁOllamaClientǁgenerate__mutmut_8, 
        'xǁOllamaClientǁgenerate__mutmut_9': xǁOllamaClientǁgenerate__mutmut_9, 
        'xǁOllamaClientǁgenerate__mutmut_10': xǁOllamaClientǁgenerate__mutmut_10, 
        'xǁOllamaClientǁgenerate__mutmut_11': xǁOllamaClientǁgenerate__mutmut_11, 
        'xǁOllamaClientǁgenerate__mutmut_12': xǁOllamaClientǁgenerate__mutmut_12, 
        'xǁOllamaClientǁgenerate__mutmut_13': xǁOllamaClientǁgenerate__mutmut_13, 
        'xǁOllamaClientǁgenerate__mutmut_14': xǁOllamaClientǁgenerate__mutmut_14
    }
    
    def generate(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaClientǁgenerate__mutmut_orig"), object.__getattribute__(self, "xǁOllamaClientǁgenerate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate.__signature__ = _mutmut_signature(xǁOllamaClientǁgenerate__mutmut_orig)
    xǁOllamaClientǁgenerate__mutmut_orig.__name__ = 'xǁOllamaClientǁgenerate'
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_orig(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_1(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = None
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_2(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=None,
            messages=messages,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_3(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=None,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_4(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options=None,
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_5(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            messages=messages,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_6(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_7(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_8(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
            )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_9(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "XXtemperatureXX": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_10(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "TEMPERATURE": self.temperature,
                "num_predict": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_11(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": self.temperature,
                "XXnum_predictXX": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_12(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text with message history."""
        import ollama
        
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": self.temperature,
                "NUM_PREDICT": self.max_tokens,
            },
            **kwargs
        )
        return response["message"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_13(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
        return response["XXmessageXX"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_14(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
        return response["MESSAGE"]["content"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_15(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
        return response["message"]["XXcontentXX"]
    
    def xǁOllamaClientǁgenerate_with_messages__mutmut_16(self, messages: List[Dict[str, str]], **kwargs) -> str:
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
        return response["message"]["CONTENT"]
    
    xǁOllamaClientǁgenerate_with_messages__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOllamaClientǁgenerate_with_messages__mutmut_1': xǁOllamaClientǁgenerate_with_messages__mutmut_1, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_2': xǁOllamaClientǁgenerate_with_messages__mutmut_2, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_3': xǁOllamaClientǁgenerate_with_messages__mutmut_3, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_4': xǁOllamaClientǁgenerate_with_messages__mutmut_4, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_5': xǁOllamaClientǁgenerate_with_messages__mutmut_5, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_6': xǁOllamaClientǁgenerate_with_messages__mutmut_6, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_7': xǁOllamaClientǁgenerate_with_messages__mutmut_7, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_8': xǁOllamaClientǁgenerate_with_messages__mutmut_8, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_9': xǁOllamaClientǁgenerate_with_messages__mutmut_9, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_10': xǁOllamaClientǁgenerate_with_messages__mutmut_10, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_11': xǁOllamaClientǁgenerate_with_messages__mutmut_11, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_12': xǁOllamaClientǁgenerate_with_messages__mutmut_12, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_13': xǁOllamaClientǁgenerate_with_messages__mutmut_13, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_14': xǁOllamaClientǁgenerate_with_messages__mutmut_14, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_15': xǁOllamaClientǁgenerate_with_messages__mutmut_15, 
        'xǁOllamaClientǁgenerate_with_messages__mutmut_16': xǁOllamaClientǁgenerate_with_messages__mutmut_16
    }
    
    def generate_with_messages(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOllamaClientǁgenerate_with_messages__mutmut_orig"), object.__getattribute__(self, "xǁOllamaClientǁgenerate_with_messages__mutmut_mutants"), args, kwargs, self)
        return result 
    
    generate_with_messages.__signature__ = _mutmut_signature(xǁOllamaClientǁgenerate_with_messages__mutmut_orig)
    xǁOllamaClientǁgenerate_with_messages__mutmut_orig.__name__ = 'xǁOllamaClientǁgenerate_with_messages'


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
