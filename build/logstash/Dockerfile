FROM docker.elastic.co/elasticsearch/elasticsearch-alpine-base:latest
MAINTAINER Elastic Docker Team <docker@elastic.co>

ARG LOGSTASH_VERSION

ENV PATH=/opt/logstash/bin:$PATH \
    JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk

RUN mkdir /opt && \
    chmod 0755 /opt && \
    wget -qO - https://artifacts.elastic.co/downloads/logstash/logstash-${LOGSTASH_VERSION}.tar.gz | \
    tar zxf - -C /opt && \
    mv /opt/logstash-${LOGSTASH_VERSION} /opt/logstash

RUN deluser elasticsearch 2>/dev/null || true; \
    adduser -D -u 1000 -h /opt/logstash logstash && \
    chown -R logstash /opt/logstash

ADD config/stdin-stdout-rubydebug.conf /opt/logstash/conf.d/

USER logstash
CMD logstash -f /opt/logstash/conf.d/
