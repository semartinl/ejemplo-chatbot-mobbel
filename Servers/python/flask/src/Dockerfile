
FROM python:3.9-slim

# RUN curl -fsSL https://ollama.com/install.sh | bash

WORKDIR /app

COPY requirements.txt ./
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "app.py"]



