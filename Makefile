format-all: ## run black and isort ignoring
	poetry run black --extend-exclude="database/" . && poetry run isort --extend-skip-glob="database/*" .

check-all: ## run check for black and isort and prospector
	poetry run black --extend-exclude="database/" --check . && poetry run isort --extend-skip-glob="database/*" --check-only .\
	&& poetry run prospector -P .prospector.yaml -S .

upgrade-db: ## run alembic upgrade scripts
	poetry run alembic upgrade head

downgrade-db: ## downgrade last migration
	poetry run alembic downgrade -1

start-app:
	poetry run uvicorn app:app --reload --port=8000

clean: ## clean project from cache files
	poetry run poe clean

vulture: ## view unused (dead) codes
	poetry run vulture . --exclude .venv

generate-migration: ## view unused (dead) codes
	poetry run alembic revision --autogenerate -m "init"

help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'
