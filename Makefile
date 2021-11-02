SHELL := /bin/bash

docs:
	widdershins \
		--environment design-docs/widdershins.json \
		design-docs/openapi/tagged-image-manager.yml \
		-o design-docs/openapi/generated-tagged-image-manager.md

	