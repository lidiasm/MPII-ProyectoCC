install:
	pipenv install --three
	pipenv run pip install -r requirements.txt
	
test:
	pipenv run python -m pytest tests/test_mascotas.py
	pipenv run python -m pytest --cov=mascotas tests/