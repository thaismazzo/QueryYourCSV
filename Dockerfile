FROM python:3.11-slim

WORKDIR /app

# Copia arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expor a porta do Streamlit
EXPOSE 8501

# Comando para rodar Streamlit acessível de fora do container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
