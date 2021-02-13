FROM python:3 as base

ENV POETRY_HOME="/poetry"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/poetry/bin:${PATH}"
WORKDIR /code

COPY pyproject.toml poetry.lock /code/

FROM base as dev
RUN poetry install
COPY app /code/app
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0"]

FROM dev as test
COPY app /code/app
COPY tests /code/tests
COPY conftest.py pytest.ini /code/
ENTRYPOINT ["poetry", "run", "pytest"]

FROM base as prod
RUN poetry install --no-dev
COPY app /code/app
COPY scripts /code/scripts
ENV PORT=5000
ENTRYPOINT ["/bin/sh", "./scripts/entrypoint.sh"]