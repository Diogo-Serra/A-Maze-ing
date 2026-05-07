# A-Maze-ing Makefile
SHELL :=  $(shell echo $$SHELL)

PY := python3
ENV := -m venv .venv
PIP := .venv/bin/pip
SRC_ENV := source .venv/bin/activate
INSTALL_REQ := $(PIP) install -r requirements.txt
LINT_STRICT := flake8 . --exclude=.venv && mypy . --strict
PIP_UPDATE := .venv/bin/python3 -m pip install --upgrade pip
BUILD := config.txt main.py Makefile README.md requirements.txt src/
CLEAN_ENV_CACHE := rm -rf .venv $$(find . -name __pycache__ -o -name .mypy_cache)

LINT := flake8 . --exclude=.venv && mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

install:
	@echo Installing requirements...
	$(PY) $(ENV)
	$(PIP_UPDATE)
	$(INSTALL_REQ)

run :
	@echo Starting ...
	.venv/bin/python3 a-maze-ing.py config.txt

build:
	@echo Building ...
	tar -cf A-Maze-ing.tar $(BUILD)

lint-strict:
	@echo Testing with lint-strict
	$(SRC_ENV) $(LINT_STRICT)

lint:
	@echo Testing linting
	$(SRC_ENV) $(LINT)

clean:
	#echo Cleaning all
	$(CLEAN_ENV_CACHE)
