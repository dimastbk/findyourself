install:
	poetry install --no-root

freeze:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

lint:
	flake8 --config=setup.cfg
	black --check .
	isort --check

test:
	coverage run --source='.' --omit='*/migrations/*' manage.py test
	coverage report -m
