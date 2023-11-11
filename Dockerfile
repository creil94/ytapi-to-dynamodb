FROM public.ecr.aws/lambda/python:3.11 as base

WORKDIR /var/task/functions
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    VENV_PATH="/var/task/functions/.venv" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN curl -sSL https://install.python-poetry.org | python3 -


# copy project requirement files
# and install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY functions .

# ENTRYPOINT ["tail", "-f", "/dev/null"]