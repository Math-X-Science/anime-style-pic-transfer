fmt:
  uv run ruff check --fix --select I . --exclude packages tests
  uv run ruff format . --exclude packages

start:
  uv lock
  uv sync
  uv run streamlit run src/converter/animegan_converter.py