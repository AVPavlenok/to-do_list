FROM python:3.9.9-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "src.routers:app", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8080"]