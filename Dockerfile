FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dkg_api ./dkg_api

EXPOSE 8000

CMD ["uvicorn", "dkg_api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
