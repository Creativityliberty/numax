.PHONY: install test lint format run serve

install:
	pip install -e .[dev]

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

run:
	python -m numax.app run --flow $(flow) --prompt "$(prompt)"

serve:
	python -m numax.app serve
