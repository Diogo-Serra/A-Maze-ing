# A-Maze-ing Makefile
SHELL :=  $(shell echo $$SHELL)

PY := python3

PIP := .venv/bin/pip
MYPY := .venv/bin/mypy
CLEAN_ENV := rm -rf .venv
FLAKE8 := .venv/bin/flake8
ENV_PY := .venv/bin/python3
BUILD := tar -cf A-Maze-ing.tar $(SRC)
SRC := config.txt main.py Makefile README.md requirements.txt src/
FLAGS_MYPY := --ignore-missing-imports --disallow-untyped-defs \
			  --warn-return-any --warn-unused-ignores \
		  	  --check-untyped-defs

install:
	@echo Preparing environment and installing requirements...
	$(PY) -m venv .venv
	$(ENV_PY) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

run :
	@echo Starting ...
	$(ENV_PY) a-maze-ing.py config.txt

build:
	@echo Building ...
	tar -cf A-Maze-ing.tar $(BUILD)

debug:
	@echo Debugging ...
	$(ENV_PY) -m pdb a-maze-ing.py config.txt

lint:
	@echo Testing lint
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . $(FLAGS_MYPY)

lint-strict:
	@echo Testing lint-strict
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . --strict

clean:
	@echo Cleaning all
	$(CLEAN_ENV) $$(find . -name __pycache__ -o -name .mypy_cache)
