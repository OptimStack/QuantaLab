from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict
import httpx
from config import settings
import json

class AIProvider(ABC):
    @abstractmethod
    async def stream_completion(self, messages: List[Dict[str, str]], system_prompt: str) -> AsyncGenerator[str, None]:
        pass

class AnthropicProvider(AIProvider):
    async def stream_completion(self, messages: List[Dict[str, str]], system_prompt: str) -> AsyncGenerator[str, None]:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": settings.ai_provider_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": settings.ai_provider_model or "claude-3-haiku-20240307",
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": messages,
            "stream": True
        }
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=data) as response:
                response.raise_for_status()
                async for chunk in response.aiter_text():
                    if chunk.startswith("data: "):
                        try:
                            parsed = json.loads(chunk[6:])
                            if parsed.get("type") == "content_block_delta":
                                yield parsed["delta"]["text"]
                        except:
                            pass

class OpenAIProvider(AIProvider):
    async def stream_completion(self, messages: List[Dict[str, str]], system_prompt: str) -> AsyncGenerator[str, None]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.ai_provider_api_key}",
            "Content-Type": "application/json"
        }
        
        api_messages = [{"role": "system", "content": system_prompt}] + messages
        
        data = {
            "model": settings.ai_provider_model or "gpt-3.5-turbo",
            "messages": api_messages,
            "stream": True
        }
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=data) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            parsed = json.loads(line[6:])
                            content = parsed["choices"][0]["delta"].get("content", "")
                            if content:
                                yield content
                        except:
                            pass

def get_provider() -> AIProvider:
    if settings.ai_provider.lower() == "anthropic":
        return AnthropicProvider()
    elif settings.ai_provider.lower() == "openai":
        return OpenAIProvider()
    else:
        # Default or fallback
        return AnthropicProvider()
