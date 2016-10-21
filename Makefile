SHELL=/bin/bash
ifndef LOGSTASH_VERSION
LOGSTASH_VERSION=5.0.0-rc1
endif

ifdef STAGING_BUILD_NUM
VERSION_TAG=$(LOGSTASH_VERSION)-${STAGING_BUILD_NUM}
LOGSTASH_DOWNLOAD_URL=http://staging.elastic.co/$(VERSION_TAG)/downloads/logstash/logstash-${LOGSTASH_VERSION}.tar.gz
else
VERSION_TAG=$(LOGSTASH_VERSION)
LOGSTASH_DOWNLOAD_URL=https://artifacts.elastic.co/downloads/logstash/logstash-${LOGSTASH_VERSION}.tar.gz
endif

REGISTRY=docker.elastic.co
IMAGE=$(REGISTRY)/logstash/logstash
VERSIONED_IMAGE=$(IMAGE):$(VERSION_TAG)
LATEST_IMAGE=$(IMAGE):latest

export LOGSTASH_VERSION
export LOGSTASH_DOWNLOAD_URL
export VERSIONED_IMAGE

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

demo:
	docker-compose --file docker-compose.demo.yml down
	docker-compose --file docker-compose.demo.yml rm --force
	docker-compose --file docker-compose.demo.yml up

push: build test
	docker push $(VERSIONED_IMAGE)

	# Only push latest if not a staging build
	if [ -z $$STAGING_BUILD_NUM ]; then \
	  docker tag $(VERSIONED_IMAGE) $(LATEST_IMAGE); \
	  docker push $(LATEST_IMAGE); \
	fi

.PHONY: build demo push test
