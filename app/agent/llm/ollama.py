import os
import ollama

from .base import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(self):
        self.client = ollama.Client(
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "qwen2.5-coder:7b-instruct-q4_K_M"
        )

    def chat(self, messages: list, tools: list | None = None) -> dict:
        args = {"model": self.model, "messages": messages}
        if tools:
            args["tools"] = tools

        response = self.client.chat(**args)
        message = response.get("message", {})

        tool_calls = self._normalize_tool_calls(message.get("tool_calls"))
        
        return {
            "message": {
                "content": message.get("content", ""),
                "tool_calls": tool_calls
            }
        }