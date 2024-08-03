FROM python:3.12


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY . /app/


RUN pip install --upgrade pip
RUN pip install django gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y redis-server supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV DJANGO_SETTINGS_MODULE=auth_system.settings

RUN python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput
#     gunicorn -b 0.0.0.0:8000

CMD ["gunicorn", "auth_system.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["/usr/bin/supervisord"]