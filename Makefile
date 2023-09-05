.PHONY: setup_precommit .cz.toml setup_commitizen commit publish_pytest test lint format

################### 
# PRECOMMIT HOOKS #
###################

setup_precommit:
	@echo "Setting up pre-commit hooks..."
	poetry run pre-commit install
	poetry run pre-commit autoupdate
	@echo "Done."

setup_commitizen:
	@echo "Installing commitizen for convential commits..."
	pip install commitizen
	cz init
	@echo "Done."


commit:
	@echo "Committing with commitizen..."
	poetry run cz commit
	@echo "Done."

publish_pytest:
	@echo "Publishing to Test PyPI..."
	poetry build
	poetry publish -r testpypi
	@echo "Done."

########### 
# Testing #
###########

test:
	@echo "Running tests..."
	poetry run pytest 
	@echo "Done."

##########################
# LINTING AND FORMATTING #
##########################
PYTHON_FILES=.
lint:
	@echo "Running linting..."
	poetry run mypy $(PYTHON_FILES)
	poetry run black $(PYTHON_FILES) --check
	poetry run ruff .
	@echo "Done."

format:
	@echo "Running formatting..."
	poetry run black $(PYTHON_FILES) 
	poetry run ruff --select I --fix $(PYTHON_FILES)
	@echo "Done."
