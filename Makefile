init:
	pip install -r requirements.txt

test:
	pytest tests

build:
	bash make-readme-toc.sh
	python setup.py sdist
	python setup.py bdist_wheel

pypi: clean build
	twine upload dist/* -r testpypi

pypi-real: clean build
	@read -r -p "Are you sure? " INPUT; \
	if [ "$$INPUT" != "y" ] ; then exit 1 ; fi
	twine upload dist/*

clean:
	find . -type f -name '*~' -delete
	find . -type f -name '*.o' -delete
	find . -type f -name '*.pyc' -delete
	rm -rf build dist .cache *.egg-info tests/__pycache__

