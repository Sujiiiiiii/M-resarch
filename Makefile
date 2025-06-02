_isort_check:
	uv run isort --check . --skip .venv

_black_check:
	uv run black --check . --exclude '\.venv'

lint:
	make -j _isort_check _black_check

_isort_apply:
	uv run isort . --skip .venv

_black_apply:
	uv run black . --exclude '\.venv'

fmt:
	make _isort_apply _black_apply

test:
	pytest

clean:
	uv run scripts/clean_results.py