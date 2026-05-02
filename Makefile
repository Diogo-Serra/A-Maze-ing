# A-Maze-ing Makefile
SHELL :=  $(shell echo $$SHELL)


PY := python3
ENV := -m venv .venv
SRC_ENV := source .venv/bin/activate
INSTALL_REQ := pip install -r requirements.txt
LINT_STRICT := flake8 . --exclude=.venv && mypy . --strict
BUILD := config.txt main.py Makefile README.md requirements.txt src/
CLEAN_ENV_CACHE := rm -rf .venv $$(find . -name __pycache__ -o -name .mypy_cache)
LINT := flake8 . --exclude=.venv && mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

install:
	$(PY) $(ENV) && $(SRC_ENV) && $(INSTALL_REQ)

run :
	$(SRC_ENV) && $(PY) a-maze-ing.py config.txt

build:
	tar -cf A-Maze-ing.tar $(BUILD)

lint-strict:
	$(SRC_ENV) $(LINT_STRICT)

lint:
	$(SRC_ENV) $(LINT)

clean:
	$(CLEAN_ENV_CACHE)
