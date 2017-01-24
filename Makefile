SHELL=/bin/bash
ifndef ELASTIC_VERSION
ELASTIC_VERSION=5.2.0
endif

ifdef STAGING_BUILD_NUM
VERSION_TAG=$(ELASTIC_VERSION)-${STAGING_BUILD_NUM}
LOGSTASH_DOWNLOAD_URL=http://staging.elastic.co/$(VERSION_TAG)/downloads/logstash/logstash-${ELASTIC_VERSION}.tar.gz
else
VERSION_TAG=$(ELASTIC_VERSION)
LOGSTASH_DOWNLOAD_URL=https://artifacts.elastic.co/downloads/logstash/logstash-${ELASTIC_VERSION}.tar.gz
endif

REGISTRY=docker.elastic.co
IMAGE=$(REGISTRY)/logstash/logstash
VERSIONED_IMAGE=$(IMAGE):$(VERSION_TAG)
LATEST_IMAGE=$(IMAGE):latest

export ELASTIC_VERSION
export LOGSTASH_DOWNLOAD_URL
export VERSIONED_IMAGE
export VERSION_TAG

test: build
	test -d venv || virtualenv --python=python3.5 venv
	( \
	  source venv/bin/activate; \
	  pip install -r test/requirements.txt; \
	  py.test test/ \
	)

build:
	echo $(LOGSTASH_DOWNLOAD_URL)
	docker-compose build --pull

demo: clean-demo
	docker-compose --file docker-compose.demo.yml up

push: build test
	docker push $(VERSIONED_IMAGE)

clean: clean-demo
	docker-compose down
	docker-compose rm --force

clean-demo:
	docker-compose --file docker-compose.demo.yml down
	docker-compose --file docker-compose.demo.yml rm --force

.PHONY: build clean clean-demo demo push test
