ARG PYTHON_VER=3.11

FROM python:${PYTHON_VER} AS base

WORKDIR /backend

ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ../pyproject.toml ../poetry.lock* /backend/

RUN poetry install --no-root

COPY ../src/bot /backend/src/bot

FROM python:3.11-slim

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get -y install libgomp1 && \
    apt-get -y install libc-dev && \
    apt-get -y install build-essential

WORKDIR /backend

COPY --from=base /backend/src /backend/src
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

CMD python /backend/src/bot/main.py