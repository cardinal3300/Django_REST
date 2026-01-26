FROM python:3.14

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY = $SECRET_KEY
ENV CELERY_BROKER_URL = $REDIS_URL
ENV CELERY_RESULT_BACKEND = $REDIS_URL

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
