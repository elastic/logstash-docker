SHELL=/bin/bash
ifndef LOGSTASH_VERSION
LOGSTASH_VERSION=5.0.0-rc1
endif

export LOGSTASH_VERSION

REGISTRY=docker.elastic.co
IMAGE=$(REGISTRY)/logstash/logstash
VERSION_TAG=$(IMAGE):$(LOGSTASH_VERSION)
LATEST_TAG=$(IMAGE):latest

test: build
	test -d venv || virtualenv --python=python3.5 venv
	( \
	  source venv/bin/activate; \
	  pip install -r test/requirements.txt; \
	  py.test test/ \
	)

build:
	docker-compose build --pull

demo:
	docker-compose --file docker-compose.demo.yml down
	docker-compose --file docker-compose.demo.yml rm --force
	docker-compose --file docker-compose.demo.yml up

push: build test
	docker tag $(VERSION_TAG) $(LATEST_TAG)

	docker push $(VERSION_TAG)
	docker push $(LATEST_TAG)

.PHONY: build push test
