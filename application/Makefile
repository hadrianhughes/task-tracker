test:
	python -m pytest lambdas/_tests/ -v

remove-stack:
	aws cloudformation delete-stack --stack-name task-tracker-application

build:
	sam build --use-container

start:
	sam local start-api
