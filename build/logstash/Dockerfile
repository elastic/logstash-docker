FROM ubuntu:16.04
MAINTAINER Elastic Docker Team <docker@elastic.co>

ARG ELASTIC_VERSION
ARG LOGSTASH_DOWNLOAD_URL
ARG LOGSTASH_PACK_URL

# Install curl for downloading, Java for running Logstash/JRuby, and netbase
# to resolve a warning from JRuby (https://github.com/jruby/jruby/issues/3955).
RUN apt-get -qq update && \
    apt-get -qq install -y curl netbase openjdk-8-jdk-headless locales && \
    apt-get -qq clean

# Provide a non-root user to run the process.
RUN addgroup --gid 1000 logstash && \
    adduser --disabled-password --gecos=logstash --uid=1000 --gid=1000 \
            --home /usr/share/logstash --no-create-home logstash

# Add Logstash itself.
RUN curl -Lso - ${LOGSTASH_DOWNLOAD_URL} | \
    tar zxf - -C /usr/share && \
    mv /usr/share/logstash-${ELASTIC_VERSION} /usr/share/logstash && \
    chown --recursive logstash:logstash /usr/share/logstash/ && \
    ln -s /usr/share/logstash /opt/logstash
ENV PATH=/usr/share/logstash/bin:$PATH

# Provide a minimal configuration, so that simple invocations will provide
# a good experience.
ADD config/logstash.yml config/log4j2.properties /usr/share/logstash/config/
ADD pipeline/default.conf /usr/share/logstash/pipeline/logstash.conf
RUN chown --recursive logstash:logstash /usr/share/logstash/config/ /usr/share/logstash/pipeline/

# Ensure Logstash has a UTF-8 locale available.
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# Place the startup wrapper script.
ADD bin/docker-entrypoint /usr/local/bin/
RUN chmod 0755 /usr/local/bin/docker-entrypoint

USER logstash

RUN cd /usr/share/logstash && LOGSTASH_PACK_URL=${LOGSTASH_PACK_URL} logstash-plugin install x-pack

ADD env2yaml/env2yaml /usr/local/bin/

EXPOSE 9600 5044

ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
CMD ["-f", "/usr/share/logstash/pipeline/"]
