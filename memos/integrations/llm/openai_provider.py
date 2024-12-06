"""
OpenAI integration for MemOS AI Framework.
"""

import os
from typing import Dict, Any, Optional, List, Union, AsyncGenerator
import aiohttp
import tiktoken

from .base import (
    LLMProvider,
    LLMResponse,
    ModelMessage,
    ModelRole,
    InvalidCredentials,
    ModelNotAvailable,
    TokenLimitExceeded
)

class OpenAIProvider(LLMProvider):
    """OpenAI API provider implementation."""

    API_BASE = "https://api.openai.com/v1"
    AVAILABLE_MODELS = {
        # GPT-4 Models
        "gpt-4-turbo-preview": 128_000,  # GPT-4 Turbo
        "gpt-4": 8_192,                  # Base GPT-4
        "gpt-4-32k": 32_768,             # GPT-4 32k context
        
        # GPT-3.5 Models
        "gpt-3.5-turbo": 4_096,          # ChatGPT
        "gpt-3.5-turbo-16k": 16_384,     # ChatGPT with extended context
        
        # Embedding Models
        "text-embedding-3-small": 8_191,  # Ada 3 Small
        "text-embedding-3-large": 8_191,  # Ada 3 Large
    }

    def __init__(self,
                 api_key: Optional[str] = None,
                 model: str = "gpt-4-turbo-preview",
                 organization: Optional[str] = None,
                 **kwargs):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key.
            model: Model identifier.
            organization: Optional organization ID.
            **kwargs: Additional arguments.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.organization = organization or os.getenv("OPENAI_ORG_ID")
        super().__init__(api_key=self.api_key, model=model, **kwargs)

    def _validate_credentials(self) -> None:
        """Validate OpenAI credentials."""
        if not self.api_key:
            raise InvalidCredentials("OpenAI API key not provided")
        if not self.validate_model(self.model):
            raise ModelNotAvailable(f"Invalid model: {self.model}")

    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if self.organization:
            headers["OpenAI-Organization"] = self.organization
        return headers

    async def generate(self,
                      prompt: str,
                      *,
                      max_tokens: Optional[int] = None,
                      temperature: float = 0.7,
                      stop_sequences: Optional[List[str]] = None,
                      **kwargs) -> LLMResponse:
        """Generate text using OpenAI API."""
        messages = [
            {"role": "user", "content": prompt}
        ]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.API_BASE}/chat/completions",
                headers=self._get_headers(),
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stop": stop_sequences,
                    **kwargs
                }
            ) as response:
                result = await response.json()

                if "error" in result:
                    raise Exception(result["error"]["message"])

                return LLMResponse(
                    content=result["choices"][0]["message"]["content"],
                    raw_response=result,
                    metadata={
                        "finish_reason": result["choices"][0]["finish_reason"]
                    },
                    usage=result["usage"],
                    model=self.model,
                    provider="openai"
                )

    async def chat(self,
                  messages: List[ModelMessage],
                  *,
                  max_tokens: Optional[int] = None,
                  temperature: float = 0.7,
                  functions: Optional[List[Dict[str, Any]]] = None,
                  **kwargs) -> LLMResponse:
        """Chat completion using OpenAI API."""
        formatted_messages = [
            {
                "role": msg.role.value,
                "content": msg.content,
                **({"name": msg.name} if msg.name else {})
            }
            for msg in messages
        ]

        request_data = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        if functions:
            request_data["functions"] = functions

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.API_BASE}/chat/completions",
                headers=self._get_headers(),
                json=request_data
            ) as response:
                result = await response.json()

                if "error" in result:
                    raise Exception(result["error"]["message"])

                return LLMResponse(
                    content=result["choices"][0]["message"]["content"],
                    raw_response=result,
                    metadata={
                        "finish_reason": result["choices"][0]["finish_reason"],
                        "function_call": result["choices"][0]["message"].get("function_call")
                    },
                    usage=result["usage"],
                    model=self.model,
                    provider="openai"
                )

    async def embed(self,
                   text: Union[str, List[str]],
                   **kwargs) -> Union[List[float], List[List[float]]]:
        """Generate embeddings using OpenAI API."""
        if isinstance(text, str):
            text = [text]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.API_BASE}/embeddings",
                headers=self._get_headers(),
                json={
                    "model": "text-embedding-3-large",
                    "input": text,
                    **kwargs
                }
            ) as response:
                result = await response.json()

                if "error" in result:
                    raise Exception(result["error"]["message"])

                embeddings = [data["embedding"] for data in result["data"]]
                return embeddings[0] if len(embeddings) == 1 else embeddings

    def get_token_count(self, text: str) -> int:
        """Get token count using tiktoken."""
        try:
            encoding = tiktoken.encoding_for_model(self.model)
            return len(encoding.encode(text))
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))

    async def stream_generate(self,
                            prompt: str,
                            *,
                            max_tokens: Optional[int] = None,
                            temperature: float = 0.7,
                            **kwargs) -> AsyncGenerator[str, None]:
        """Stream generated text from OpenAI API."""
        messages = [
            {"role": "user", "content": prompt}
        ]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.API_BASE}/chat/completions",
                headers=self._get_headers(),
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                    **kwargs
                }
            ) as response:
                async for line in response.content:
                    if line:
                        chunk = line.decode().strip()
                        if chunk.startswith("data: ") and chunk != "data: [DONE]":
                            content = chunk[6:]
                            yield content

    async def stream_chat(self,
                         messages: List[ModelMessage],
                         *,
                         max_tokens: Optional[int] = None,
                         temperature: float = 0.7,
                         **kwargs) -> AsyncGenerator[str, None]:
        """Stream chat completion from OpenAI API."""
        formatted_messages = [
            {
                "role": msg.role.value,
                "content": msg.content,
                **({"name": msg.name} if msg.name else {})
            }
            for msg in messages
        ]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.API_BASE}/chat/completions",
                headers=self._get_headers(),
                json={
                    "model": self.model,
                    "messages": formatted_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": True,
                    **kwargs
                }
            ) as response:
                async for line in response.content:
                    if line:
                        chunk = line.decode().strip()
                        if chunk.startswith("data: ") and chunk != "data: [DONE]":
                            content = chunk[6:]
                            yield content

    def get_available_models(self) -> List[str]:
        """Get list of available OpenAI models."""
        return list(self.AVAILABLE_MODELS.keys())

    def validate_model(self, model: str) -> bool:
        """Validate if model is available in OpenAI."""
        return model in self.AVAILABLE_MODELS 