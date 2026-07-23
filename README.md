# Uso rápido

suba os containers:
```bash
docker compose up -d
```

Baixar o modelo dentro do container do Ollama (apenas uma vez):
```bash
docker exec -it ollama_service ollama run qwen2.5-coder:7b-instruct-q4_K_M
```

Outro modelo mais leve:
```bash
docker exec -it ollama_service ollama run qwen2.5-coder:3b
```

Rodando o agente:
```bash
docker compose run --rm agent
```