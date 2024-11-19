default: fmt fix

# Startup commands
up *params:
    docker compose -f compose.yaml up {{params}}

serve host="127.0.0.1" port="8000":
    uv run uvicorn app.main:app --host {{host}} --port {{port}} --reload

# Code quality commands
fmt:
    uv run ruff format

check-fmt:
    uv run ruff format --check

lint:
    uv run ruff check

fix:
    uv run ruff check --fix

# Migrations management commands
revise msg:
    uv run alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    uv run alembic upgrade {{target}}

revert target="-1":
    uv run alembic downgrade {{target}}
