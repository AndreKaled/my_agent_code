import inspect
from pydantic import TypeAdapter

AVAILABLE_TOOLS = {}
TOOLS_SCHEMA = []

def register_tool(func):
    """Decorador que registra a função e gera o TOOLS_SCHEMA automaticamente"""
    # pegando docstring da funcao pra descricao da tool
    description = func.__doc__.strip() if func.__doc__ else f"Executa {func.__name__}"

    # pegando os parametros da funcao
    sig = inspect.signature(func)
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        param_type = "string" if param.annotation == inspect.Parameter.empty else TypeAdapter(param.annotation).json_schema().get("type", "string")
        properties[name] = {
            "type": param_type,
            "description": f"Parâmetro {name}"
        }
        if param.default == inspect.Parameter.empty:
            required.append(name)
    schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

    AVAILABLE_TOOLS[func.__name__] = func
    TOOLS_SCHEMA.append(schema)
    return func