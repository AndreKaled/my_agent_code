FROM python:3.11-slim

WORKDIR /workspace
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
COPY app /app/app
ENV PYTHONPATH=/app

CMD ["python", "-m", "app.agent.main"]