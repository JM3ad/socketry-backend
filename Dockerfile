FROM python:3

ENV POETRY_HOME="/poetry"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/poetry/bin:${PATH}"
WORKDIR /code

COPY poetry.toml /code
COPY pyproject.toml /code
COPY scripts /code/scripts

RUN poetry install

COPY app /code/app

ENTRYPOINT ["/bin/sh", "./scripts/entrypoint.sh"]