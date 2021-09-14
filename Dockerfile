FROM python:3.8-slim

ENV HOME /app
WORKDIR $HOME
EXPOSE 8000

COPY . .
RUN pip install -r requirements.txt
CMD gunicorn -c 'python:config.gunicorn' 'surl.app:create_app()'