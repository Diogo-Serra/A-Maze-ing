# Makefile

PY := python3
ENV := -m venv .venv
SRC_ENV := source .venv/bin/activate
CLEAN_ENV := rm -rf .venv
INSTALL_REQ := pip install -r requirements.txt


install:
	$(PY) $(ENV) && $(SRC_ENV) && $(INSTALL_REQ)

clean:
	$(CLEAN_ENV)

run :
	python main.py config.txt