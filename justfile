fmt:
  uv run ruff check --fix --select I . --exclude packages tests
  uv run ruff format . --exclude packages