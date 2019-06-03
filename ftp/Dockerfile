FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /app && mkdir /homedir && chmod 755 /homedir && chown ftp:ftp /homedir
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "ftp.py" ]