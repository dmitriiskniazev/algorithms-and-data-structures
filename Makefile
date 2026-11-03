.PHONY: help setup setup-python test test-python docs clean format lint typecheck check

help:
	@printf '%s\n' 'setup          Set up Python dependencies through uv' \
	  'test           Run Python tests' \
	  'test-python    Run pytest through uv' \
	  'lint           Check Python lint and formatting' \
	  'typecheck      Check all source types with Pyright' \
	  'format         Format Python sources and tests' \
	  'check          Run lint, types, tests, and HTML build' \
	  'docs           Build HTML documentation' \
	  'clean          Remove generated output and caches; keep the Python environment'

setup: setup-python

setup-python:
	uv sync --all-groups --locked

test: test-python

test-python:
	@if test -d tests && test -n "$$(find tests -type f -name 'test_*.py' -print -quit)"; then uv run --locked python -m pytest; else printf '%s\n' 'No Python tests yet.'; fi

docs:
	uv run --locked --group docs sphinx-build -W --keep-going -b html docs docs/_build/html

format:
	uv run --locked ruff format src tests

lint:
	uv run --locked ruff check src tests/typing
	uv run --locked ruff format --check src tests

typecheck:
	uv run --locked pyright

check: lint typecheck test docs

clean:
	rm -rf -- docs/_build dist .cache .pytest_cache .ruff_cache
	find src tests -type d -name __pycache__ -prune -exec rm -rf -- {} +
