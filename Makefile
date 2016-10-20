SHELL=/bin/bash
ifndef LOGSTASH_VERSION
LOGSTASH_VERSION=5.0.0-rc1
endif

export LOGSTASH_VERSION

REGISTRY=docker.elastic.co
IMAGE=$(REGISTRY)/logstash/logstash
VERSION_TAG=$(IMAGE):$(LOGSTASH_VERSION)
LATEST_TAG=$(IMAGE):latest

test:
	test -d venv || virtualenv --python=python3.5 venv
	( \
	  source venv/bin/activate; \
	  pip install -r test/requirements.txt; \
	  py.test test/ \
	)

build:
	docker-compose build --pull

demo: clean-docker build
	docker-compose up

push: build test
	docker tag $(VERSION_TAG) $(LATEST_TAG)

	docker push $(VERSION_TAG)
	docker push $(LATEST_TAG)

clean-docker:
	docker-compose down
	docker-compose rm --force

.PHONY: build push test
