from typing import List, Dict, Any

class AgentState:
    """Gerencia o quadro de estado (Blackboard) da conversa e execuções."""
    
    def __init__(self):
        self._messages: List[Dict[str, Any]] = []

    def add_system(self, content: str) -> None:
        self._messages.append({
            "role": "system",
            "content": content,
        })

    def add_tool_result(self, tool_call_id: str, tool_name: str, content: str,) -> None:
        self._messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": content,
            }
        )

    def add_user(self, content: str) -> None:
        self._messages.append({
            "role": "user",
            "content": content,
        })

    def add_assistant(self, content: str, tool_calls: list | None = None) -> None:
        message = {
            "role": "assistant",
            "content": content,
        }
        if tool_calls:
            message["tool_calls"] = tool_calls
        
        self._messages.append(message)

    def history(self) -> list[dict]:
        return self._messages

    def clear(self) -> None:
        self._messages.clear()
