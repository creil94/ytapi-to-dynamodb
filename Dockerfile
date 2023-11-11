FROM public.ecr.aws/lambda/python:3.11 as base

WORKDIR /var/task/functions
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    VENV_PATH="/var/task/functions/.venv"


# prepend poetry and venv to path
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry==1.6.1

# copy project requirement files
# and install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY functions .