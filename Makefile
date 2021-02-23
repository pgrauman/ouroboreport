

env-install:
	test -d .venv || poetry install

clean:
	find . | grep -E "(__pycache__)" | xargs rm -rf

test: env-install
	poetry run pytest tests

teardown: clean
	rm poetry.lock
	rm -rf .venv