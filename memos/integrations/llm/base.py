"""
Base classes for LLM integrations in MemOS AI Framework.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum

@dataclass
class LLMResponse:
    """Container for LLM responses."""
    content: str
    raw_response: Dict[str, Any]
    metadata: Dict[str, Any]
    usage: Dict[str, int]
    model: str
    provider: str

class ModelRole(Enum):
    """Roles for model interactions."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

@dataclass
class ModelMessage:
    """Message structure for model interactions."""
    role: ModelRole
    content: str
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class LLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, 
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 **kwargs):
        """
        Initialize LLM provider.

        Args:
            api_key: Optional API key for the provider.
            model: Optional default model to use.
            **kwargs: Additional provider-specific arguments.
        """
        self.api_key = api_key
        self.model = model
        self.kwargs = kwargs
        self._validate_credentials()

    @abstractmethod
    def _validate_credentials(self) -> None:
        """Validate provider credentials."""
        pass

    @abstractmethod
    async def generate(self,
                      prompt: str,
                      *,
                      max_tokens: Optional[int] = None,
                      temperature: float = 0.7,
                      stop_sequences: Optional[List[str]] = None,
                      **kwargs) -> LLMResponse:
        """
        Generate text from prompt.

        Args:
            prompt: Input prompt.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            stop_sequences: Optional stopping sequences.
            **kwargs: Additional provider-specific arguments.

        Returns:
            LLMResponse: Generated response.
        """
        pass

    @abstractmethod
    async def chat(self,
                  messages: List[ModelMessage],
                  *,
                  max_tokens: Optional[int] = None,
                  temperature: float = 0.7,
                  functions: Optional[List[Dict[str, Any]]] = None,
                  **kwargs) -> LLMResponse:
        """
        Chat completion with message history.

        Args:
            messages: List of conversation messages.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            functions: Optional function definitions.
            **kwargs: Additional provider-specific arguments.

        Returns:
            LLMResponse: Generated response.
        """
        pass

    @abstractmethod
    async def embed(self,
                   text: Union[str, List[str]],
                   **kwargs) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text.

        Args:
            text: Input text or list of texts.
            **kwargs: Additional provider-specific arguments.

        Returns:
            Union[List[float], List[List[float]]]: Generated embeddings.
        """
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """
        Get token count for text.

        Args:
            text: Input text.

        Returns:
            int: Number of tokens.
        """
        pass

    @abstractmethod
    async def stream_generate(self,
                            prompt: str,
                            *,
                            max_tokens: Optional[int] = None,
                            temperature: float = 0.7,
                            **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream generated text.

        Args:
            prompt: Input prompt.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            **kwargs: Additional provider-specific arguments.

        Yields:
            str: Generated text chunks.
        """
        pass

    @abstractmethod
    async def stream_chat(self,
                         messages: List[ModelMessage],
                         *,
                         max_tokens: Optional[int] = None,
                         temperature: float = 0.7,
                         **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream chat completion.

        Args:
            messages: List of conversation messages.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            **kwargs: Additional provider-specific arguments.

        Yields:
            str: Generated text chunks.
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List[str]: List of model identifiers.
        """
        pass

    @abstractmethod
    def validate_model(self, model: str) -> bool:
        """
        Validate if model is available.

        Args:
            model: Model identifier.

        Returns:
            bool: True if model is valid.
        """
        pass

class LLMException(Exception):
    """Base exception for LLM-related errors."""
    pass

class ProviderNotAvailable(LLMException):
    """Exception for unavailable providers."""
    pass

class InvalidCredentials(LLMException):
    """Exception for invalid credentials."""
    pass

class ModelNotAvailable(LLMException):
    """Exception for unavailable models."""
    pass

class TokenLimitExceeded(LLMException):
    """Exception for token limit violations."""
    pass 