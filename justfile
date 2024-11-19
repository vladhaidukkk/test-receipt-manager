default: fmt fix

# Code quality commands
fmt:
    uv run ruff format

check-fmt:
    uv run ruff format --check

lint:
    uv run ruff check

fix:
    uv run ruff check --fix
