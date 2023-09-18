run:
	python main.py

style:
	isort *.py --profile black
	black .