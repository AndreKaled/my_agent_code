import os
from openai import OpenAI
from .base import LLMProvider
import json


class GroqProvider(LLMProvider):
    def __init__(self):
        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

    def _prepare_messages_for_api(self, messages: list) -> list:
        """Garante que todas as mensagens com tool_calls enviem arguments como string JSON para a API do Groq"""
        sanitized_messages = []
        for msg in messages:
            msg_copy = dict(msg)
            if "tool_calls" in msg_copy and msg_copy["tool_calls"]:
                formatted_calls = []
                for tc in msg_copy["tool_calls"]:
                    func = tc.get("function", {})
                    args = func.get("arguments", {})
                    
                    # converte dict em string JSON para satisfazer a API do Groq/OpenAI
                    if isinstance(args, dict):
                        args = json.dumps(args, ensure_ascii=False)

                    formatted_calls.append({
                        "id": tc.get("id", "call_default"),  
                        "type": "function",
                        "function": {
                            "name": func.get("name"),
                            "arguments": args
                        }
                    })
                msg_copy["tool_calls"] = formatted_calls
            sanitized_messages.append(msg_copy)
        return sanitized_messages

    def chat(self, messages: list, tools: list | None = None) -> dict:
        api_messages = self._prepare_messages_for_api(messages)
        args = {"model": self.model, "messages": api_messages}
        if tools:
            args["tools"] = tools
            
        response = self.client.chat.completions.create(**args)
        choice = response.choices[0].message

        tool_calls = self._normalize_tool_calls(choice.tool_calls or [])

        return {
            "message":{
                "content": choice.content or "",
                "tool_calls": tool_calls
            }
        }