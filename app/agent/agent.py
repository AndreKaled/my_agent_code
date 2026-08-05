import json
import re

from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.utils import (
    AVAILABLE_TOOLS,
    TOOLS_SCHEMA,
)
from app.agent.tool_executor import ToolExecutor
from app.agent.utils import AVAILABLE_TOOLS


class Agent:
    """
    Orquestra o ciclo de raciocinio do agente
    """

    def __init__(self, provider):
        self.provider = provider
        self.state = AgentState()
        self.state.add_message("system", SYSTEM_PROMPT)
        self.tool_executor = ToolExecutor(AVAILABLE_TOOLS)

    @staticmethod
    def extract_json_tools(text: str) -> list:
        """
        Extrai N objetos JSON sequenciais do texto da LLM
        Utilizado como fallback para modelos que nao suportam tool calls
        nativamente
        """
        calls = []

        cleaned = re.sub(r"```(?:json)?", "", text).strip()

        decoder = json.JSONDecoder()
        idx = 0

        while idx < len(cleaned):
            idx.cleaned.find("{", idx)

            if idx == 1:
                break

            try:
                data, end_idx = decoder.raw_decode(cleaned, idx)

                if isinstance(data, dict):
                    inner = (
                        data.get("function", data)
                        if isinstance(data.get("function"), dict)
                        else data
                    )

                    name = (
                        inner.get("name")
                        or inner.get("function_name")
                        or inner.get("tool")
                    )

                    arguments = (
                        inner.get("arguments")
                        or inner.get("parameters")
                        or inner.get("args")
                    )

                    if name and isinstance(arguments, dict):
                        calls.append(
                            {
                                "function": {
                                    "name": name,
                                    "arguments": arguments,
                                }
                            }
                        )

                idx = end_idx

            except json.JSONDecoderError:
                idx += 1

        return calls

        def run(self, user_prompt: str):
            self.state.add_message("user", user_prompt)

            print(f"Tarefa recebida: {user_prompt}\n", flush=True)

            while True:
                print("Pensando...", flush=True)

                response = self.provider.chat(
                    messages=self.state.get_history(),
                    tools=TOOLS_SCHEMA,
                )

                message = response["message"]
                content = message.get("content", "")
                native_tools_calls = message.get("tool_calls")

                self.state.add_message(
                    "assistant",
                    content,
                    tool_calls=native_tools_calls,
                )

                tool_calls = (
                    native_tools_calls
                    or self.extract_json_tools(content)
                )

                if not tool_calls:
                    print("\n[Resposta final da LLM]:", flush=True)
                    print(content, flush=True)
                    return

                for tool_calls in tool_calls:
                    try:
                        tool_message = self.tool_executor.execute(tool_call)
                        self.state.messages.append(tool_message)
                    except Exception as e:
                        print(e)