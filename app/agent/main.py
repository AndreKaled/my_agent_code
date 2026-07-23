import sys
sys.path.append("/content")

import os
import ollama
import json
import re
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools import execute_bash, read_file, write_file

ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = ollama.Client(host=ollama_host)

AVAILABLE_TOOLS = {
    "execute_bash": execute_bash,
    "read_file": read_file,
    "write_file": write_file
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "execute_bash",
            "description": "Executa um comando bash no terminal dentro do workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "O comando bash a ser executado."
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lê o conteúdo de um arquivo no workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Caminho relativo do arquivo."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Cria ou sobrescreve um arquivo no workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Caminho relativo do arquivo."
                    },
                    "content": {
                        "type": "string",
                        "description": "Conteúdo de texto a ser gravado no arquivo."
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    }
]

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
                calls.append({"function": data})
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
            response = client.chat(
                model="qwen2.5-coder:7b-instruct-q4_K_M",
                messages=state.get_history(),
                tools=TOOLS_SCHEMA
            )
            
            message = response["message"]
            content = message.get("content", "")
            state.add_message("assistant", content)

            tool_calls = message.get("tool_calls") or extract_json_tools(content)

            if tool_calls:
                for tool_call in tool_calls:
                    func_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]

                    if func_name in AVAILABLE_TOOLS:
                        print(f"Executando: {func_name}({arguments})", flush=True)
                        tool_output = AVAILABLE_TOOLS[func_name](**arguments)
                        print(f"Retorno: {tool_output}\n", flush=True)
                        
                        state.messages.append({
                            "role": "tool",
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