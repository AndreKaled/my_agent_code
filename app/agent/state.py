from typing import List, Dict, Any

class AgentState:
    """Gerencia o quadro de estado (Blackboard) da conversa e execuções."""
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str, tool_calls=None):
        message = {"role": role, "content": content}
        if tool_calls:
            message["tool_calls"] = tool_calls
        self.messages.append(message)

    def get_history(self) -> List[Dict[str, Any]]:
        return self.messages