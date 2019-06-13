FROM python:3-slim as build
WORKDIR /app
RUN apt-get update && apt-get install -y make
ADD requirements.txt .
ADD development.ini .
ADD Makefile .
RUN make install
ADD . .

FROM build as test
RUN make test_install
ADD test-requirements.txt .
CMD ["make", "test"]

FROM build as service
EXPOSE 15808
CMD ["python", "service.py"]
