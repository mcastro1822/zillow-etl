FROM prefecthq/prefect:2-python3.12

COPY uv.lock .

COPY pyproject.toml .

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/prefect/.venv

RUN uv sync --no-dev --frozen && uv pip install pip

ENV PATH="/opt/prefect/.venv/bin:${PATH}"