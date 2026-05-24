run:
	python -m app.main

lint:
	ruff check .

format:
	ruff format .

test:
	pytest

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

test-e2e:
	pytest tests/e2e