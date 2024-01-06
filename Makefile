init:
	pip install -r requirements.txt

test:
	pytest tests

build:
	python3 -m build

pypi:
	python3 -m twine upload --repository testpypi dist/*
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps keyctl

pypi-real: clean init build
	@read -r -p "Are you sure? " INPUT; \
	if [ "$$INPUT" != "y" ] ; then exit 1 ; fi
	twine upload dist/*

clean:
	pip freeze | xargs pip uninstall keyctl -y
	#pip uninstall keyctl
	find . -type f -name '*~' -delete
	find . -type f -name '*.o' -delete
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf build dist .cache *.egg-info .pytest_cache

