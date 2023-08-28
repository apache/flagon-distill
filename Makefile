.PHONY: test lint format

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
