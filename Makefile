_isort_check:
	uv run isort --check .

_black_check:
	uv run black --check .

_mypy:
	uv run mypy .

lint:
	make -j _isort_check _black_check _mypy

_isort_apply:
	uv run isort .

_black_apply:
	uv run black .

fmt:
	make _isort_apply _black_apply

test:
	pytest