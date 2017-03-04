init:
	pip install -r requirements.txt

test:
	pytest tests

build:
	python setup.py sdist
	python setup.py bdist_wheel

pypi: clean build
	twine upload dist/* -r testpypi

clean:
	find . -type f -name '*~' -delete
	find . -type f -name '*.o' -delete
	find . -type f -name '*.pyc' -delete
	rm -rf build dist .cache *.egg-info tests/__pycache__

