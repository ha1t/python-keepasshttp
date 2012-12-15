all:
	-rm -rf build dist
	python setup.py py2app
clean:
	-rm -rf build dist
