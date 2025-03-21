.PHONY: develop format run sim test lint clean

develop:
	uv venv
	uv pip install -e ".[dev,test]"

format:
	uv run ruff format .

lint:
	uv run ruff check
	uv run pyright

test:
	uv run pytest

run:
	uv run python -m controller

sim:
	uv run python -m controller simulate

clean:
	rm -rf .venv *.egg-info .pytest_cache .coverage .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +