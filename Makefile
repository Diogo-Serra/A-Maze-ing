# A-Maze-ing Makefile
ENV := .venv/bin
PY := /usr/bin/python3

PIP := $(ENV)/pip
MYPY := $(ENV)/mypy
FLAKE8 := $(ENV)/flake8
ENV_PY := $(ENV)/python3
CLEAN_ENV := rm -rf .venv

SRC := config.txt a-maze-ing.py Makefile README.md requirements.txt src/
FLAGS_MYPY := --ignore-missing-imports --disallow-untyped-defs \
			  --warn-return-any --warn-unused-ignores \
		  	  --check-untyped-defs

install:
	@echo Preparing environment and installing requirements...
	$(PY) -m venv .venv
	$(ENV_PY) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

run :
	$(ENV_PY) a-maze-ing.py config.txt

build:
	@echo Building ...
	$(PY) -m build --sdist --outdir .

debug:
	@echo Debugging ...
	$(ENV_PY) -m pdb a-maze-ing.py config.txt

lint:
	@echo Testing lint ...
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . $(FLAGS_MYPY)

lint-strict:
	@echo Testing lint-strict ...
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . --strict

clean:
	@echo Cleaning all cache and venv
	$(CLEAN_ENV) $$(find . -name __pycache__ -o -name .mypy_cache)

create:
	@echo Creating virtual environment ...
	$(PY) -m venv .venv
	$(ENV_PY) -m pip install --upgrade pip

re: clean install