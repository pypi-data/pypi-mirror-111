.PHONY: package
package:
	@./setup.py sdist

.PHONY: clean
clean:
	rm -rf MANIFEST
	rm -rf dist
	py3clean .

.PHONY: publish
publish: clean package
	twine upload dist/*
