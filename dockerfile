FROM python:3.11-slim

WORKDIR /workspace
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY app /app/app
ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-m", "app.agent.main"]