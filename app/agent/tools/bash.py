import subprocess
import os
import json
from app.agent.utils import register_tool
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
        return json.dumps(
            {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            },
            ensure_ascii=False
        )

    except subprocess.TimeoutExpired:
        return json.dumps(
            {
                "success": False,
                "exit_code": None,
                "stdout": "",
                "stderr": "Timeout excedido (30 segundos)"
            },
            ensure_ascii=False
        )

    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "exit_code": None,
                "stdout": "",
                "stderr": str(e)
            },
            ensure_ascii=False
        )