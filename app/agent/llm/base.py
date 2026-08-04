from abc import ABC, abstractmethod
import json
import uuid

class LLMProvider(ABC):

    @abstractmethod
    def chat(self, messages: list, tools: list | None = None) -> dict:
        """Executa uma conversa e retorna uma resposta no formato interno do agente"""
        pass

    def _normalize_tool_calls(self, raw_tool_calls: list) -> list:
        """Método comum para normalizar argumentos de string JSON para dicionário"""
        normalized = []
        if not raw_tool_calls:
            return normalized

        for tc in raw_tool_calls:
            # funciona se for um dicionario ou objeto SDK da openai
            if isinstance(tc, dict):
                call_id = tc.get("id") or f"call_{uuid.uuid4().hex[:8]}"
                func = tc.get("function", {})
                name = func.get("name")
                args = func.get("arguments", {})
            else:
                call_id = getattr(tc, "id", None) or f"call_{uuid.uuid4().hex[:8]}"
                name = tc.function.name
                args = tc.function.arguments

            # converte string json para dict
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}

            if name:
                normalized.append({
                    "id": call_id,
                    "function": {
                        "name": name,
                        "arguments": args
                    }
                })
        return normalized