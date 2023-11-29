MAKEFLAGS += --silent

clean:
	python -B -m scripts.clean

lint:
	python -m flake8
