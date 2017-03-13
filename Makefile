SHELL=/bin/bash
ifndef ELASTIC_VERSION
export ELASTIC_VERSION := $(shell cat version.txt)
endif

ifdef STAGING_BUILD_NUM
VERSION_TAG=$(ELASTIC_VERSION)-${STAGING_BUILD_NUM}
LOGSTASH_DOWNLOAD_URL=http://staging.elastic.co/$(VERSION_TAG)/downloads/logstash/logstash-${ELASTIC_VERSION}.tar.gz
LOGSTASH_PACK_URL=https://staging.elastic.co/$(VERSION_TAG)/downloads/logstash-plugins
else
VERSION_TAG=$(ELASTIC_VERSION)
LOGSTASH_DOWNLOAD_URL=https://artifacts.elastic.co/downloads/logstash/logstash-${ELASTIC_VERSION}.tar.gz
LOGSTASH_PACK_URL=https://artifacts.elastic.co/downloads/logstash-plugins
endif

REGISTRY=docker.elastic.co
IMAGE=$(REGISTRY)/logstash/logstash
VERSIONED_IMAGE=$(IMAGE):$(VERSION_TAG)
LATEST_IMAGE=$(IMAGE):latest

export ELASTIC_VERSION
export LOGSTASH_DOWNLOAD_URL
export LOGSTASH_PACK_URL
export VERSIONED_IMAGE
export VERSION_TAG

export PATH := ./bin:./venv/bin:$(PATH)

test: venv build
	bin/testinfra test/

build: env2yaml
	echo $(LOGSTASH_DOWNLOAD_URL)
	docker-compose build --pull

demo: clean-demo
	docker-compose --file docker-compose.demo.yml up

push: build test
	docker push $(VERSIONED_IMAGE)

venv: requirements.txt
	test -d venv || virtualenv --python=python3.5 venv
	pip install -r requirements.txtd
	touch venv

# Make a Golang container that can compile our env2yaml tool.
golang:
	docker build -t golang:env2yaml build/golang

env2yaml: golang
	docker run --rm -it \
	  -v ${PWD}/build/logstash/env2yaml:/usr/local/src/env2yaml \
	golang:env2yaml go build

clean: clean-demo
	docker-compose down
	docker-compose rm --force

clean-demo:
	docker-compose --file docker-compose.demo.yml down
	docker-compose --file docker-compose.demo.yml rm --force

.PHONY: build clean clean-demo demo push test
