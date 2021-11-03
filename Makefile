SHELL := /bin/bash
STAGE ?= dev
STACK_PREFIX = tagged-image
SERVICE_STACK_NAME = $(STACK_PREFIX)-$(STAGE)-service
INFRA_STACK_NAME = $(STACK_PREFIX)-$(STAGE)-infra

ifeq ($(USE_AWS_VAULT), true)
  AWS = aws-vault exec $(PROFILE) --no-session -- aws
  CHALICE = aws-vault exec $(PROFILE) -- poetry run chalice
  POETRY = aws-vault exec $(PROFILE) -- poetry
  PYTHON = aws-vault exec $(PROFILE) -- python
else
  AWS = aws
  CHALICE = poetry run chalice
  POETRY = poetry
  PYTHON = python
endif

deploy-infra: cloudformation/infra.yaml
	$(AWS) cloudformation deploy \
		--template-file $< \
		--stack-name $(INFRA_STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides \
			Stage=$(STAGE)

# Deploy uploaded stack to CloudFormation
deploy: packaged/packaged.yaml
	@$(AWS) cloudformation deploy \
		--template-file $< \
		--stack-name $(SERVICE_STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides \
			CognitoPoolArn=$(COGNITO_POOL_ARN) \
			DBUrl=$(DB_URL) \
			Stage=$(STAGE) \
			InfraStack=$(INFRA_STACK_NAME)

docs:
	widdershins \
		--environment design-docs/.widdershins.json \
		design-docs/openapi/tagged-image-manager.yml \
		-o design-docs/openapi/generated-tagged-image-manager.md

fix:
	poetry run isort app.py chalicelib/
	poetry run black app.py chalicelib/

lint:
	poetry run black app.py chalicelib/

requirements.txt: ./poetry.lock
	poetry export --without-hashes | grep -v ' @ ' > $@

run:
	$(POETRY) run chalice local

# Upload the package to S3
packaged/packaged.yaml: packaged/sam.yaml
	$(eval S3_BUCKET = $(shell $(AWS) cloudformation describe-stacks \
		--stack-name $(INFRA_STACK_NAME) \
		--query "Stacks[].Outputs[?OutputKey=='CodeBucketName'][] | [0].OutputValue" \
	))
	@echo "Uploading to $(S3_BUCKET)"
	$(AWS) cloudformation package \
		--template-file $< \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file $@

# Package the app locally
packaged/sam.yaml: requirements.txt
	-rm -rf .chalice/deployments
	STAGE=$(or $(STAGE),dev) $(CHALICE) package \
		$(dir $@) \
		--stage $(or $(STAGE),dev) \
		--template-format yaml \
		--merge-template cloudformation/chalice.yaml


smoketest:
	poetry run pytest -svv tests/smoke --durations=0

tables:
	python -m scripts.make_tables

tests: lint unittests

unittests:
	poetry run pytest -vv --cov-report term-missing --cov="chalicelib" tests/unit

update-snapshots:
	poetry run pytest tests/unit -v --snapshot-update --allow-snapshot-deletion


.PHONY: deploy-service docs packaged/sam.yaml lint unittests smoketest tests update-snapshots