FROM python:3 as base

ENV POETRY_HOME="/poetry"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/poetry/bin:${PATH}"
WORKDIR /code

COPY poetry.toml /code
COPY pyproject.toml /code

FROM base as dev
RUN poetry install
COPY app /code/app
ENTRYPOINT ["python", "app/app.py"]

FROM dev as test
ENTRYPOINT ["poetry", "run", "pytest"]

FROM base as prod
RUN poetry install --no-dev
COPY app /code/app
COPY scripts /code/scripts
ENV PORT=5000
ENTRYPOINT ["/bin/sh", "./scripts/entrypoint.sh"]