import sys

from app.agent.agent import Agent
from app.agent.llm.factory import get_provider
from app.agent.utils import load_tools

load_tools()

provider = get_provider()
agent = Agent(provider)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # se passou o comando direto no terminal
        prompt = " ".join(sys.argv[1:])
    else:
        # se rodou so 'docker compose run --rm agent', ele pergunta ao user oq quer fazer
        prompt = input("O que vamos construir hoje? > ")

    if prompt.strip():
        try:
            agent.run(prompt)
        except Exception as e:
            print(f"Erro de execução: {e}")
            
    else:
        print("Nenhuma instrução fornecida. Encerrando.")