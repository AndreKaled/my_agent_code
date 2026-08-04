import sys
sys.path.append("/content")

import json
import re
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.llm.factory import get_provider
import app.agent.tools
from app.agent.utils import (
    AVAILABLE_TOOLS,
    TOOLS_SCHEMA
)

provider = get_provider()


def extract_json_tools(text: str):
    """Extrai múltiplos objetos JSON sequenciais do texto da LLM."""
    calls = []
    cleaned = re.sub(r'```(?:json)?', '', text).strip()
    
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(cleaned):
        idx = cleaned.find('{', idx)
        if idx == -1:
            break
        try:
            data, end_idx = decoder.raw_decode(cleaned, idx)
            if isinstance(data, dict) and "name" in data and "arguments" in data:
                inner = data.get("function", data) if isinstance(data.get("function"), dict) else data
                name = inner.get("name") or inner.get("function_name") or inner.get("tool")
                arguments = inner.get("arguments") or inner.get("parameters") or inner.get("args")
                if name and isinstance(arguments, dict):
                    calls.append({"function": {"name": name, "arguments": arguments}})
            idx = end_idx
        except json.JSONDecodeError:
            idx += 1
    return calls

def run_agent(user_prompt: str):
    state = AgentState()
    state.add_message("system", SYSTEM_PROMPT)
    state.add_message("user", user_prompt)

    print(f"Tarefa recebida: {user_prompt}\n", flush=True)

    while True:
        try:
            print("Pensando...", flush=True)
            response = provider.chat(
                messages=state.get_history(),
                tools=TOOLS_SCHEMA
            )
            
            message = response["message"]
            content = message.get("content", "")
            native_tool_calls = message.get("tool_calls")
            state.add_message("assistant", content, tool_calls=native_tool_calls)

            tool_calls = native_tool_calls or extract_json_tools(content)

            if tool_calls:
                for tool_call in tool_calls:
                    call_id = tool_call.get("id", "call_default")
                    func_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]

                    if func_name in AVAILABLE_TOOLS:
                        print(f"Executando: {func_name}({arguments})", flush=True)
                        tool_output = AVAILABLE_TOOLS[func_name](**arguments)
                        print(f"Retorno: {tool_output}\n", flush=True)
                        
                        state.messages.append({
                            "role": "tool",
                            "tool_call_id": call_id,
                            "name": func_name,
                            "content": tool_output
                        })
                    else:
                        print(f"Ferramenta '{func_name}' não encontrada.\n", flush=True)
            else:
                print("\n[Resposta Final da LLM]:", flush=True)
                print(content, flush=True)
                break

        except Exception as e:
            print(f"Erro de execução: {e}", flush=True)
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # se passou o comando direto no terminal
        prompt = " ".join(sys.argv[1:])
    else:
        # se rodou so 'docker compose run --rm agent', ele pergunta ao user oq quer fazer
        prompt = input("O que vamos construir hoje? > ")

    if prompt.strip():
        run_agent(prompt)
    else:
        print("Nenhuma instrução fornecida. Encerrando.")