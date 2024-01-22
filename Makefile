init:
	python3 -m pip install -r requirements.txt
	python3 -m pip install -r requirements-dev.txt

test:
	python3 -m pytest tests

build:
	python3 -m build

pypi:
	python3 -m twine upload --repository testpypi dist/*
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps keyctl

pypi-real: clean init test build
	@read -r -p "Are you sure? " INPUT; \
	if [ "$$INPUT" != "y" ] ; then exit 1 ; fi
	twine upload dist/*

clean:
	pip freeze | xargs pip uninstall keyctl -y
	find . -type f -name '*~' -delete
	find . -type f -name '*.o' -delete
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf build dist .cache *.egg-info .pytest_cache tests/.pytest_cache
