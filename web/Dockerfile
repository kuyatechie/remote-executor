FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN apk update && \
    apk add postgresql-dev musl-dev gcc && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT [ "python3", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]
