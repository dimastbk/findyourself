install:
	poetry install --no-dev --no-root

freeze:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

lint:
	flake8 --config=setup.cfg

test:
	poetry install --no-root
	coverage run --source='.' --omit='*/migrations/*' manage.py test user
	coverage report
