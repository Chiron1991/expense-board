FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=expenseboard.settings.prod

WORKDIR /app

EXPOSE 80/tcp

# install requirements without invalidating the Docker cache layer on successive builds
COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# set entrypoint script
COPY scripts/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["scripts/entrypoint.sh"]

COPY . .

RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get autoremove -y --purge &&\
    apt-get clean &&\
    python manage.py collectstatic --clear --no-input
