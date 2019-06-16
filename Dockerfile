FROM python:3-slim as build
WORKDIR /app
RUN apt-get update && apt-get install -y make
ADD requirements.txt .
ADD test-requirements.txt .
ADD development.ini .
ADD setup.py .
ADD Makefile .
RUN make install
ADD . .

FROM build as test
RUN make test_install
CMD ["make", "test"]

FROM build as service
EXPOSE 15808

ENV MONGO_DBNAME nozama-cloudsearch
ENV MONGO_HOST localhost
ENV MONGO_PORT 27017
ENV ELASTICSEARCH_HOST localhost
ENV ELASTICSEARCH_PORT 9200

CMD ["paster", "development.ini"]
