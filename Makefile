.ONESHELL:
ENV_PREFIX := $(shell python3 -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
EXTRA_ARGS?=
PYTHON_COMMAND?=python3

.PHONY: help
help: ## Show the help.
	@echo "Usage: make [target] [EXTRA_ARGS=...]"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: show
show: ## Show the environment.
	@echo "Current environment:"
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python --version
	@$(ENV_PREFIX)python -m bifurc2midi --version

.PHONY: install
install: activate ## Install the in dev mode
	@echo "Don't forget to run 'make virtualenv' if you get errors"
	$(ENV_PREFIX)pip install -r requirements.txt

.PHONY: virtualenv
virtualenv: ## Create a virtual environment
	@echo "Creating virtualenv..."
	@rm -rf .venv
	@$(PYTHON_COMMAND) -m venv .venv
	@./.venv/bin/pip install -U pip
	@./.venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "!!! Please run 'source .venv/bin/activate' to activate the virtualenv !!!"

.PHONY: activate
activate: ## Activate the virtual environment
	@echo "Activating virtualenv..."
	. ./$(ENV_PREFIX)activate

.PHONY: run
run: ## Run the project
	$(ENV_PREFIX)python scripts/bifurcation.py $(EXTRA_ARGS)

.PHONY: variables
variables: ## Show interesting variables
	@echo "ENV_PREFIX: $(ENV_PREFIX)"
	@echo "EXTRA_ARGS: $(EXTRA_ARGS)"
