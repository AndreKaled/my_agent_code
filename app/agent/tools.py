import subprocess
import os
import json
from app.agent.utils import register_tool

WORKSPACE_ROOT = "/workspace"

def _safe_path(filepath: str) -> str:
    """Resolve filepath dentro de WORKSPACE_ROOT e bloqueia path que viola 
    o espaço do container (ex: '../../etc')"""
    full_path = os.path.normpath(os.path.join(WORKSPACE_ROOT, filepath))
    if not (full_path == WORKSPACE_ROOT or full_path.startswith(WORKSPACE_ROOT + os.sep)):
        raise ValueError(f"Caminho '{filepath}' tenta acessar fora do workspace, bloquado.")
    return full_path

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

@register_tool
def read_file(filepath: str) -> str:
    """Lê o conteúdo de um arquivo em /workspace."""
    full_path = _safe_path(filepath)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

@register_tool
def write_file(filepath: str, content: str) -> str:
    """Escreve conteúdo em um arquivo em /workspace."""
    full_path = _safe_path(filepath)
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Arquivo '{filepath}' salvo com sucesso."
    except Exception as e:
        return f"Erro ao salvar arquivo: {str(e)}"