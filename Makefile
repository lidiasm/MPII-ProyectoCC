install:
	pipenv install --three
	pipenv run pip install pytest
	pipenv run pip install pytest-cov

test:
	pipenv run python -m pytest tests/test_mascotas.py
	pipenv run python -m pytest --cov=mascotas tests/