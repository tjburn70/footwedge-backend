ENV_NAME ?= dev
SERVICE_NAME = footwedge-backend

AWS_ACCOUNT_ID = 753710783959
REGION = us-east-2
SYNTH_OUT ?= cdk_stack

build: build-cdk

build-cdk:
	yarn run build
	yarn run lint

deploy:
	yarn run cdk -- deploy $(ENV_NAME)-$(SERVICE_NAME) \
	--output=$(SYNTH_OUT) \
	--context ENV_NAME=$(ENV_NAME) \
	--context SERVICE_NAME=$(SERVICE_NAME) \
	--context REGION=$(REGION) \
	--context ACCOUNT=$(AWS_ACCOUNT_ID) \
	--context ALGOLIA_FOOTWEDGE_APP_ID=$(ALGOLIA_FOOTWEDGE_APP_ID) \
	--context ALGOLIA_API_KEY=$(ALGOLIA_API_KEY)

buildDeploy: build deploy
