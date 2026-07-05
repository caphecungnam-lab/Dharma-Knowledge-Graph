FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dkg_api ./dkg_api
COPY scripts ./scripts

RUN adduser --disabled-password --gecos "" dkg
USER dkg

EXPOSE 8000

CMD ["uvicorn", "dkg_api.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
