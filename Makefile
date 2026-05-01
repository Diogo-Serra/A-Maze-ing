# A-Maze-ing Makefile
SHELL :=  $(shell echo $$SHELL)


PY := python3
ENV := -m venv .venv
SRC_ENV := source .venv/bin/activate
CLEAN_ENV := rm -rf .venv
INSTALL_REQ := pip install -r requirements.txt
BUILD := config.txt main.py Makefile README.md requirements.txt src/
LINT_STRICT := flake8 . --exclude=.venv && mypy . --strict
LINT := flake8 . --exclude=.venv && mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

install:
	$(PY) $(ENV) && $(SRC_ENV) && $(INSTALL_REQ)

run :
	$(PY) main.py config.txt

build:
	tar -cf A-Maze-ing.tar $(BUILD)

clean:
	$(CLEAN_ENV)

lint:
	$(LINT)

lint-strict:
	$(LINT_STRICT)
