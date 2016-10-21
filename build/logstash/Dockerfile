FROM ubuntu:16.04
MAINTAINER Elastic Docker Team <docker@elastic.co>

ARG LOGSTASH_VERSION
ARG LOGSTASH_DOWNLOAD_URL

# Install curl for downloading, Java for running Logstash/JRuby, and netbase
# to resolve a warning from JRuby (https://github.com/jruby/jruby/issues/3955).
RUN apt-get update && \
    apt-get install -y curl netbase openjdk-8-jdk-headless && \
    apt-get clean

# Add Logstash itself.
RUN curl -Lso - ${LOGSTASH_DOWNLOAD_URL} | \
    tar zxf - -C /usr/share && \
    mv /usr/share/logstash-${LOGSTASH_VERSION} /usr/share/logstash && \
    ln -s /usr/share/logstash /opt/logstash
ENV PATH=/usr/share/logstash/bin:$PATH

# Provide a minimal configuration, so that a simple incocations will provide
# a good experience.
ADD config/logstash.yml /usr/share/logstash/config/
ADD config/log4j2.properties /usr/share/logstash/config/
ADD pipeline/default.conf /usr/share/logstash/pipeline/logstash.conf

# Ensure Logstash has a UTF-8 locale available.
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LC_ALL='en_US.UTF-8'

# Provide a non-root user to run the process.
RUN chown --recursive 1000:1000 /usr/share/logstash && \
    addgroup --gid 1000 logstash && \
    adduser --disabled-password --gecos=logstash --uid=1000 --gid=1000 --home /usr/share/logstash logstash
USER logstash

CMD ["logstash", "-f", "/usr/share/logstash/pipeline/"]
