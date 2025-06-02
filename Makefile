_isort_check:
	isort .

_black_check:
	black --check .

_mypy:
	mypy .

lint:
	make -j _isort_check _black_check _mypy

_isort_apply:
	isort .

_black_apply:
	black .

fmt:
	make _isort_apply _black_apply

test:
	pytest