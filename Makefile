ENV_RUN := conda run -n admix
PIP_RUN := ${cr} pip

.PHONY: help \
		setup \
		create_env \
		install_hooks \
		install_requirements \
		lint_staged \
		lint_all \
		clean \
		test

help:
	@echo
	@echo "Admixture Makefile"
	@echo
	@echo "Usage:"
	@echo
	@echo "ENVIRONMENT MANAGEMENT"
	@echo
	@echo "\t setup		    creates and sets up the conda environment: "\
							 "installs packages from environment.yml, "\
							 "requirements.txt and installs git commit hooks."
	@echo
	@echo "\t clean  		  Cleans autogenerated files like cache"
	@echo
	@echo "LINTING"
	@echo
	@echo "\t lint_staged	 lints files staged for commit"
	@echo
	@echo "\t lint_all		 lints all files"
	@echo
	@echo "TESTING"
	@echo
	@echo "\t test	       run all the tests"
	@echo

## MANAGING THE ENVIRONMENT
setup:
	@echo Setting up the repo
	$(MAKE) create_env
	${ENV_RUN} $(MAKE) install_requirements
	${ENV_RUN} $(MAKE) install_hooks

create_env:
	@echo Creating environment from environment.yml
	@conda env create -f environment.yml

install_hooks:
	@echo Installing precommit hooks...
	@pre-commit install
	@pre-commit install --hook-type commit-msg

install_requirements:
	@echo Installing from requirements.txt...
	@pip install -r requirements.txt
	@pip install -e .

clean:
	@echo Cleaning files...
	@rm -rf .mypy_cache *.egg_info

## LINTERS
lint_staged:
	@echo Running hook with staged files
	@pre-commit run

lint_all:
	@echo Running hook on all files
	@pre-commit run --all-files

## TESTS
test:
	@python3 -m pytest -vvs tests