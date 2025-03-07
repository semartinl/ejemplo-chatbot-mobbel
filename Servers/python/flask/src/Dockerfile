# FROM ollama/ollama

# RUN ollama pull llama3.2

# CMD ["ollama", "run", "llama3.2"]

FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | bash

WORKDIR /app

COPY requirements.txt ./
COPY . .

RUN pip install -r requirements.txt
RUN systemctl enable ollama && systemctl start ollama

CMD ["python", "app.py"]

