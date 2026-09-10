FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/apps/api
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
