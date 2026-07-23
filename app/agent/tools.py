import subprocess
import os

def execute_bash(command: str) -> str:
    """Executa um comando de terminal no diretório atual de trabalho."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/workspace"
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        return output if output else "Comando executado sem retorno visual."
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

def read_file(filepath: str) -> str:
    """Lê o conteúdo de um arquivo em /workspace."""
    full_path = os.path.join("/workspace", filepath)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    """Escreve conteúdo em um arquivo em /workspace."""
    full_path = os.path.join("/workspace", filepath)
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Arquivo '{filepath}' salvo com sucesso."
    except Exception as e:
        return f"Erro ao salvar arquivo: {str(e)}"