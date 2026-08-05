import subprocess
import os
import json
from app.agent.utils import register_tool, tool_result
from app.agent.tools.filesystem import WORKSPACE_ROOT

@register_tool
def execute_bash(command: str) -> str:
    """Executa um comando de terminal no diretório atual de trabalho."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=WORKSPACE_ROOT
        )
        return tool_result(
            success=result.returncode == 0,
            operation="execute_bash",
            message="Comando executado",
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    except subprocess.TimeoutExpired:
        return tool_result(
            success=False,
            operation="execute_bash",
            message="Timeout excedido",
            exit_code=None,
            stdout="",
            stderr="Timeout de 30 segundos",
        )

    except Exception as e:
        return tool_result(
            success=False,
            operation="execute_bash",
            message="Erro executando comando",
            error=str(e),
        )