FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /app && mkdir /homedir
WORKDIR /app
COPY requirements.txt .
RUN apk update && \
    apk add postgresql-dev musl-dev gcc && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "worker.py" ]
