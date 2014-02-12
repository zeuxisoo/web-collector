.PHONY: clean-pyc

all:
	@echo "make install"

server:
	@python manager.py runserver

install:
	@virtualenv-2.7 --no-site-package venv
	@source ./venv/bin/activate && pip install -r requirements.txt

clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
