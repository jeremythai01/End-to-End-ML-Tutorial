include .env

setup:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	export PYTHONPATH=$(PYTHONPATH):./src

lint:
	pylint src/

typehint:
	mypy --ignore-missing-imports src/

format:
	black --line-length 79 *.py

test:
	pytest tests/

build:
	docker-compose build

push:
	docker-compose push

deploy: 
	aws lambda update-function-code --function-name ScrapePushReddit --image-uri $(AWS_ECR)/data_scrape_pipeline:latest
	aws lambda update-function-code --function-name TransformLoadDB --image-uri $(AWS_ECR)/data_prep_pipeline:latest
	aws lambda update-function-code --function-name PredictSentimentML --image-uri $(AWS_ECR)/ml_predict:latest


ci: lint typehint format test build
cd: push deploy