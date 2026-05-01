# A-Maze-ing Makefile

PY := python3
ENV := -m venv .venv
SRC_ENV := source .venv/bin/activate
CLEAN_ENV := rm -rf .venv
INSTALL_REQ := pip install -r requirements.txt
BUILD := config.txt main.py Makefile README.md requirements.txt src/
LINT := flake8 . && \
		mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

install:
	$(PY) $(ENV) && $(SRC_ENV) && $(INSTALL_REQ)

lint:
	$(PY) $(LINT)

run :
	python main.py config.txt

build:
	tar -cf A-Maze-ing.tar $(BUILD)

clean:
	$(CLEAN_ENV)
