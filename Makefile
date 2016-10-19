SHELL=/bin/bash
ifndef LOGSTASH_VERSION
LOGSTASH_VERSION=5.0.0-rc1
endif

export LOGSTASH_VERSION

REGISTRY=docker.elastic.co
REMOTE_IMAGE=$(REGISTRY)/logstash/logstash
VERSION_TAG=$(REMOTE_IMAGE):$(LOGSTASH_VERSION)
LATEST_TAG=$(REMOTE_IMAGE):latest

build:
	docker-compose build --pull

demo: build
	docker-compose up

push: build
	docker tag logstash:$(LOGSTASH_VERSION) $(VERSION_TAG)
	docker tag $(VERSION_TAG) $(LATEST_TAG)

	docker push $(VERSION_TAG)
	docker push $(LATEST_TAG)

clean-docker:
	docker-compose down
	docker-compose rm --force

.PHONY: build push
