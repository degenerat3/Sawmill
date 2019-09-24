ARG ELK_VERSION
ARG ELK_FLAVOUR

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch${ELK_FLAVOUR}:${ELK_VERSION}

COPY config/sg/ config/sg/
COPY bin/ bin/


# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
