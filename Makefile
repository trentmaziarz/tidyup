.PHONY: test install clean

test:
	python3 -m pytest -q tests

install:
	pip3 install --user -e .

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -name __pycache__ | xargs rm -rf
