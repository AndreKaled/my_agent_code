class ToolExecutor:
    """Executa ferramentas disponíveis e registradas pelo agente"""

    def __init__(self, tools: dict):
        self.tools = tools

    def execute(self, tool_call: dict) -> dict:
        call_id = tool_call.get("id", "call_default")

        function = tool_call["function"]
        name = function["name"]
        arguments = function["arguments"]

        if name not in self.tools:
            raise ValueError(f"Ferramenta '{name}' não encontrada.")

        print(f"Executando: {name}({arguments})", flush=True)

        result = self.tools[name](**arguments)

        print(f"Retorno: {result}\n", flush=True)
        return {
            "role": "tool",
            "tool_call_id": call_id,
            "name": name,
            "content": result
        }
