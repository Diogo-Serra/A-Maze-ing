# A-Maze-ing Makefile
SHELL :=  $(shell echo $$SHELL)


PY := python3
ENV := -m venv .venv
SRC_ENV := source .venv/bin/activate
INSTALL_REQ := pip install -r requirements.txt
LINT_STRICT := flake8 . --exclude=.venv && mypy . --strict
CLEAN_ENV_CACHE := rm -rf .venv **/__pycache__ **/.mypy_cache
BUILD := config.txt main.py Makefile README.md requirements.txt src/
LINT := flake8 . --exclude=.venv && mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

install:
	$(PY) $(ENV) && $(SRC_ENV) && $(INSTALL_REQ)

build:
	tar -cf A-Maze-ing.tar $(BUILD)

run :
	$(PY) a-maze-ing.py config.txt

clean:
	$(CLEAN_ENV_CACHE)

lint-strict:
	$(LINT_STRICT)

lint:
	$(LINT)
