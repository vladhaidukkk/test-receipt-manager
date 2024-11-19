default: fmt fix

# Startup commands
serve:
    uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Code quality commands
fmt:
    uv run ruff format

check-fmt:
    uv run ruff format --check

lint:
    uv run ruff check

fix:
    uv run ruff check --fix
