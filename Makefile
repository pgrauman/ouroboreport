

env-install:
	test -d .venv || poetry install

lint: env-install
	poetry run pylint ouroboreport

test: env-install
	poetry run pytest tests

clean:
	find . | grep -E "(__pycache__)" | xargs rm -rf
	find . | grep -E "(pytest_cache)" | xargs rm -rf

teardown: clean
	touch poetry.lock && rm poetry.lock
	rm -rf .venv