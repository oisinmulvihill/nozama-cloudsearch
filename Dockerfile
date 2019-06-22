# base set for both test and service images:
FROM python:3-slim as build
WORKDIR /app
RUN apt-get update && apt-get install -y make
ADD README.rst .
ADD requirements.txt .
ADD test-requirements.txt .
ADD development.ini .
ADD setup.py .
ADD Makefile .
RUN make install
ADD . .

ENV MONGO_DBNAME nozama-cloudsearch
ENV MONGO_HOST 127.0.0.1
ENV MONGO_PORT 27017
ENV ELASTICSEARCH_HOST 127.0.0.1
ENV ELASTICSEARCH_PORT 9200

# Stuff only for testing:
FROM build as test
RUN make test_install
CMD ["make", "test"]

# Stuff only for production:
FROM build as service
EXPOSE 15808

WORKDIR /app
CMD ["pserve", "development.ini"]
