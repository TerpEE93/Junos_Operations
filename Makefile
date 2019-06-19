PROJECT=$(shell python3 setup.py --name)
PROJECT_VERSION=$(shell python3 setup.py --version)
SOURCEDIR=$(subst -,_,$(PROJECT))
SOURCES=$(shell find $(SOURCEDIR) -name '*.py')
APP_SERVER=ea-app

.PHONY: venv build install develop clean test

venv:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv && \
		. .venv/bin/activate && \
		pip3 install -q -U pip && \
		pip3 install -q -r requirements.txt;\
	fi

build: venv
	. .venv/bin/activate && \
	python3 setup.py build

install:
	python3 setup.py install

deploy:
	python3 setup.py sdist bdist_wheel
	scp dist/$(PROJECT)-$(PROJECT_VERSION)-py3-none-any.whl $(APP_SERVER):
	ssh $(APP_SERVER) /usr/local/bin/pip3 install -q -U $(PROJECT)-$(PROJECT_VERSION)-py3-none-any.whl

develop: venv
	. .venv/bin/activate && \
	pip3 install -q -U -r requirements-dev.txt && \
	python3 setup.py develop

clean:
	python3 setup.py clean && \
	pip3 uninstall -q -y $(PROJECT)
	rm -rf *.egg-info/
	rm -rf dist/ build/
	find . -name '*.retry' -print | xargs rm
	find . -name '*.pyc' -print | xargs rm
	find . -name '__pycache__' -print | xargs rmdir

test: venv
	. .venv/bin/activate && \
	python3 -m pytest
