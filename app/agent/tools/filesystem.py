from app.agent.utils import register_tool, tool_result
import os

WORKSPACE_ROOT = "/workspace"

def _safe_path(filepath: str) -> str:
    """Resolve filepath dentro de WORKSPACE_ROOT e bloqueia path que viola 
    o espaço do container (ex: '../../etc')"""
    full_path = os.path.normpath(os.path.join(WORKSPACE_ROOT, filepath))
    if not (full_path == WORKSPACE_ROOT or full_path.startswith(WORKSPACE_ROOT + os.sep)):
        raise ValueError(f"Caminho '{filepath}' tenta acessar fora do workspace, bloquado.")
    return full_path

@register_tool
def read_file(filepath: str) -> str:
    """Lê o conteúdo de um arquivo dentro do workspace."""
    full_path = _safe_path(filepath)
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()
            return tool_result(
                True,
                "read_file",
                "Arquivo lido",
                path=filepath,
                content=content,
            )
    except Exception as e:
        return tool_result(
            False,
            "read_file",
            "Erro lendo arquivo",
            error=str(e),
        )

@register_tool
def write_file(filepath: str, content: str) -> str:
    """Escreve conteúdo em um arquivo dentro do workspace."""
    try:
        full_path = _safe_path(filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return tool_result(
            True,
            "write_file",
            "Arquivo salvo",
            path=filepath,
        )
    except Exception as e:
        return tool_result(
            False,
            "write_file",
            "Erro salvando arquivo",
            error=str(e),
        )

@register_tool
def edit_file(filepath: str, old_str: str, new_str: str) -> str:
    """
    Substitui um trecho exato de um arquivo por outro, sem reescrever o arquivo inteiro.
    old_str precisa ser copiado exatamente como está no arquivo (recomendo usar read_file antes)
    e precisa aparecer exatamente uma vez. Se aparecer mais de uma vez, inclua mais
    linhas de contexto ao redor do trecho para torná-lo único.
    """
    try:
        full_path = _safe_path(filepath)
 
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
 
        occurrences = content.count(old_str)
 
        if occurrences == 0:
            return tool_result(
                False,
                "edit_file",
                "old_str não encontrado no arquivo. Confira espaços, indentação e "
                "quebras de linha, copie o trecho exatamente como aparece no read_file.",
                path=filepath,
            )
 
        if occurrences > 1:
            return tool_result(
                False,
                "edit_file",
                f"old_str aparece {occurrences} vezes no arquivo e precisa ser único. "
                "Inclua mais linhas de contexto ao redor do trecho para diferenciá-lo.",
                path=filepath,
                occurrences=occurrences,
            )
 
        new_content = content.replace(old_str, new_str, 1)
 
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
 
        return tool_result(
            True,
            "edit_file",
            "Trecho substituído com sucesso",
            path=filepath,
        )
 
    except Exception as e:
        return tool_result(
            False,
            "edit_file",
            "Erro editando arquivo",
            error=str(e),
        )

@register_tool
def create_directory(filepath: str) -> str:
    """
    Cria uma pasta dentro do workspace.
    Nunca utilize caminhos absolutos iniciados por '/'.
    """
    try:
        full_path = _safe_path(filepath)

        os.makedirs(full_path, exist_ok=True)
        return tool_result(
            True,
            "create_directory",
            "Pasta criada",
            path=filepath,
        )
    except Exception as e:
        return tool_result(
            False,
            "create_directory",
            "Erro criando pasta",
            error=str(e),
        )

@register_tool
def list_directory(filepath=".") -> str:
    """Lista arquivos e pastas dentro de um diretório do workspace."""
    try:
        full_path = _safe_path(filepath)
        if not os.path.isdir(full_path):
            return tool_result(
                False,
                "list_directory",
                "Caminho não é um diretório",
                path=filepath,
            )
        entries = []

        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)

            entries.append(
                {
                    "name": entry,
                    "type": "directory" if os.path.isdir(entry_path) else "file",
                }
            )
        return tool_result(
            True,
            "list_directory",
            "Diretório listado",
            path=filepath,
            entries=entries,
        )
    except Exception as e:
        return tool_result(
            False,
            "list_directory",
            "Erro listando diretório",
            error=str(e),
        )

@register_tool
def file_exists(filepath: str) -> str:
    """Verifica se um arquivo ou diretório existe dentro do workspace."""
    try:
        full_path = _safe_path(filepath)

        exists = os.path.exists(full_path)

        return tool_result(
            True,
            "file_exists",
            "Verificação concluída",
            path=filepath,
            exists=exists,
        )

    except Exception as e:
        return tool_result(
            False,
            "file_exists",
            "Erro verificando arquivo",
            error=str(e),
        )


@register_tool
def delete_file(filepath: str) -> str:
    """Remove um arquivo dentro do workspace."""
    try:
        full_path = _safe_path(filepath)

        if not os.path.isfile(full_path):
            return tool_result(
                False,
                "delete_file",
                "Arquivo não encontrado",
                path=filepath,
            )

        os.remove(full_path)

        return tool_result(
            True,
            "delete_file",
            "Arquivo removido",
            path=filepath,
        )

    except Exception as e:
        return tool_result(
            False,
            "delete_file",
            "Erro removendo arquivo",
            error=str(e),
        )


@register_tool
def delete_directory(filepath: str) -> str:
    """Remove um diretório vazio dentro do workspace."""
    try:
        full_path = _safe_path(filepath)

        if not os.path.isdir(full_path):
            return tool_result(
                False,
                "delete_directory",
                "Diretório não encontrado",
                path=filepath,
            )

        os.rmdir(full_path)

        return tool_result(
            True,
            "delete_directory",
            "Diretório removido",
            path=filepath,
        )

    except OSError as e:
        return tool_result(
            False,
            "delete_directory",
            "Diretório não está vazio ou não pode ser removido",
            error=str(e),
        )

    except Exception as e:
        return tool_result(
            False,
            "delete_directory",
            "Erro removendo diretório",
            error=str(e),
        )

@register_tool
def get_file_info(filepath: str) -> str:
    """Retorna informações sobre um arquivo ou diretório dentro do workspace."""
    try:
        full_path = _safe_path(filepath)

        if not os.path.exists(full_path):
            return tool_result(
                False,
                "get_file_info",
                "Arquivo ou diretório não encontrado",
                path=filepath,
            )

        stat = os.stat(full_path)

        is_directory = os.path.isdir(full_path)

        return tool_result(
            True,
            "get_file_info",
            "Informações obtidas",
            path=filepath,
            type="directory" if is_directory else "file",
            size=stat.st_size,
            created_at=stat.st_ctime,
            modified_at=stat.st_mtime,
            extension=(
                os.path.splitext(filepath)[1]
                if not is_directory
                else None
            ),
        )

    except Exception as e:
        return tool_result(
            False,
            "get_file_info",
            "Erro obtendo informações",
            error=str(e),
        )