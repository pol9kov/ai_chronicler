PYTHON := /opt/homebrew/bin/python3.11
VENV   := .venv

.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
