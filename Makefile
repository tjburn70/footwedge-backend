ENV_NAME ?= dev
SERVICE_NAME = footwedge-backend

AWS_ACCOUNT_ID = 753710783959
REGION = us-east-2
SYNTH_OUT ?= cdk_stack

build: build-cdk build-footwedge-api build-post-confirmation-service build-stream-service build-scrape-golf-clubs

build-cdk:
	yarn run build
	yarn run lint

build-footwedge-api:
	make -C footwedge-api/ build
	make -C footwedge-api/ lint

build-post-confirmation-service:
	make -C post-confirmation-service/ build
	make -C post-confirmation-service/ lint

build-stream-service:
	make -C stream-service/ build
	make -C stream-service/ lint

build-scrape-golf-clubs:
	make -C scrape-golf-clubs/ build
	make -C scrape-golf-clubs/ lint

deploy:
	yarn run cdk -- deploy $(ENV_NAME)-$(SERVICE_NAME) \
	--output=$(SYNTH_OUT) \
	--context ENV_NAME=$(ENV_NAME) \
	--context SERVICE_NAME=$(SERVICE_NAME) \
	--context REGION=$(REGION) \
	--context ACCOUNT=$(AWS_ACCOUNT_ID) \
	--context ALGOLIA_FOOTWEDGE_APP_ID=$(ALGOLIA_FOOTWEDGE_APP_ID) \
	--context ALGOLIA_API_KEY=$(ALGOLIA_API_KEY) \
	--context STREAM_SERVICE_COGNITO_CLIENT_SECRET=$(STREAM_SERVICE_COGNITO_CLIENT_SECRET) \
	--context SCRAPE_SERVICE_COGNITO_CLIENT_SECRET=$(SCRAPE_SERVICE_COGNITO_CLIENT_SECRET)

buildDeploy: build deploy
