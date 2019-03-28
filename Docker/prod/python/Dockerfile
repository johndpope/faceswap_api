FROM python:3.6-slim AS python_base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Workaround for https://github.com/debuerreotype/debuerreotype/issues/10
RUN seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{}

RUN apt-get update && apt-get install -y \
  # general dependencies
  net-tools netcat g++ make git wget ca-certificates \
  build-essential cmake pkg-config python3-dev \
  # dlib and opencv dependencies
  libgtk-3-dev libboost-python-dev libx11-dev \
  libjpeg62 libjpeg62-turbo-dev libpng16-16 libpng-dev libatlas-base-dev \
  giflib-dbg giflib-tools libopenblas-base libopenblas-dev \
  # Pillow dependencies
  python-numpy python-scipy netpbm \
  python-qt4 ghostscript libffi-dev libjpeg-turbo-progs \
  python-setuptools python-virtualenv \
  libtiff5-dev libjpeg62-turbo-dev zlib1g-dev \
  libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev \
  python-tk python3-tk \
  libharfbuzz-dev libfribidi-dev \
  # psycopg2 dependencies
  python3-psycopg2 \
  # CFFI dependencies
  python-cffi \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  postgresql-client

WORKDIR /usr/src/app

COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /usr/src/app/


# Django image
FROM python_base AS django

ENTRYPOINT ["/usr/src/app/Docker/prod/python/entrypoint.sh"]


# Celery image
FROM python_base as celery

RUN useradd -ms /bin/bash celery
RUN chown -R celery:celery ./media
USER celery
