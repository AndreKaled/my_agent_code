# Uso rápido

### 1. Iniciar a infraestrutura
Suba os containers necessários no seu computador:
```bash
docker compose up -d
```

### 2. Configurar o Modelo (Google Colab)
1. Abra o [Google Colab](https://colab.research.google.com).
2. Carregue o arquivo [`teste_agente.ipynb`](teste_agente.ipynb) disponível neste repositório.
3. Execute todas as células do notebook.
4. Copie a **URL pública** gerada pelo túnel da Cloudflare.

### 3. Vincular o Host do Ollama
Abra o arquivo [`docker-compose.yml`](docker-compose.yml) e cole a URL copiada diretamente na variável de ambiente correspondente:
```yaml
OLLAMA_HOST=sua_url_da_cloudflare_aqui
```

> [!NOTE]
> O modelo permanecerá ativo apenas enquanto o notebook do Google Colab estiver em execução.

> [!IMPORTANT]
> Você pode alterar o modelo livremente, basta se lembrar de alterar o model em [main.py](app/agent/main.py) e baixar e carregar o modelo desejado no [Google colab](https://colab.research.google.com).
---

## Executando o agente

Para iniciar o agente e enviar prompts, execute:
```bash
docker compose run --rm agent
```
> Escreva seu prompt e seja feliz! *(Ou triste, caso o modelo decida ficar completamente louco e nao conseguir fazer nada legal).*

Você também pode passar o prompt diretamente como argumento final do comando:
```bash
docker compose run --rm agent "crie uma pasta chamada coisas_legais_divertidas_para_nerds_felizes_lalalalala"
```

---

> [!WARNING]
> **Permissões do Agente**
> O agente possui acesso limitado ao ambiente. Ele pode utilizar apenas ferramentas básicas de sistema por enquanto, como:
> - `execute_bash`
> - `read_file`
> - `write_file`