install:
	pipenv install --three
	pipenv run pip install -r requirements.txt
	
test:
	pipenv run python -m pytest tests/test_mascotas.py tests/test_mascotas_rest.py 
	pipenv run python -m pytest --cov=mascotas --cov=mascotas_rest tests/