.DEFAULT_GOAL=help

VENVPATH=venv
PYTHON=$(VENVPATH)/bin/python3

.PHONY: venv
venv: $(VENVPATH)/bin/activate
$(VENVPATH)/bin/activate: requirements.txt
	test -d $(VENVPATH) || virtualenv -p python3 $(VENVPATH); \
	. $(VENVPATH)/bin/activate; \
	pip install -r requirements.txt; \
	touch $(VENVPATH)/bin/activate;

##install-deps: setup your dev environment
.PHONY: install-deps
install-deps: venv

##run: run the message scraper
.PHONY: run
run: install-deps
	$(PYTHON) main.py

.PHONY: lint
lint: venv
	$(PYTHON) -m flake8 . --show-source --statistics

##test: test your code
.PHONY: test
test: install-deps lint
	$(PYTHON) -m pytest

.PHONY: clean
clean:
	rm -rf $(VENVPATH)

##help: show help
.PHONY: help
help : Makefile
	@sed -n 's/^##//p' $<
