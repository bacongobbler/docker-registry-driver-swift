test:
	python setup.py nosetests
	flake8
	bash contrib/validate-commits.sh
