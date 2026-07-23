from typing import List, Dict, Any

class AgentState:
    """Gerencia o quadro de estado (Blackboard) da conversa e execuções."""
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, Any]]:
        return self.messages