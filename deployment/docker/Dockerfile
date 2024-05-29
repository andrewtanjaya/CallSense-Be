ARG ARCH
FROM ${ARCH}python:3.10-slim-buster
ARG TOKEN
ARG TOKEN_NAME

ENV POETRY_HOME="$HOME/.poetry" \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry
RUN apt-get update && apt-get install git -y

WORKDIR /hackathon-bi-service
COPY poetry.lock pyproject.toml /hackathon-bi-service/

RUN poetry install --no-dev

COPY ./common /hackathon-bi-service/common
COPY ./src /hackathon-bi-service/src
COPY __init__.py app.py /hackathon-bi-service/

CMD poetry run uvicorn app:app --workers 1 --host 0.0.0.0 --port 5000
