.PHONY: docs

init:
	pip install -r requirements.txt

publish:
	python setup.py register
	python setup.py bdist_wheel upload
	python setup.py sdist upload

publish-test:
	python setup.py register -r https://testpypi.python.org/pypi
	python setup.py sdist upload -r https://testpypi.python.org/pypi
	python setup.py bdist_wheel upload -r https://testpypi.python.org/pypi

docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make html

clean:
	rm -rf dist build
	rm -rf Tahoma.egg-info
	cd docs && make clean
	python setup.py clean
