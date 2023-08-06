.PHONY: clean lint format help
.DEFAULT_GOAL := help

PYTHON := python

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@grep '^[^.#]\+:\s\+.*#' Makefile | \
	  sed "s/\(.\+\):\s*\(.*\) #\s*\(.*\)/`printf "\033[93m"`  \1`printf "\033[0m"`	\3 [\2]/" | \
	  expand -35
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

clean: # Remove all builds and Python artifacts
	find wagtailembedpeertube \
	  \( -name '*.py[co]' -o -name '__pycache__' \) -exec rm -rf {} +
	rm -rf build dist .eggs *.egg-info

lint: # Check the Python code syntax and style
	$(PYTHON) -m flake8 wagtailembedpeertube

format: # Fix the Python code syntax and imports order
	$(PYTHON) -m isort wagtailembedpeertube
	$(PYTHON) -m black wagtailembedpeertube

release: dist # Package and upload a release
	twine upload dist/*

dist: clean # Build source and wheel package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist
