GIT_COMMIT?=$(shell git rev-parse HEAD)
BRANCH_NAME?=$(shell git rev-parse --abbrev-ref HEAD)

DOCKER_NAME=nozama-cloudsearch
DOCKER_IMAGE=${DOCKER_NAME}:${GIT_COMMIT}

export DB_HOST?=127.0.0.1
export DB_NAME=service
export DB_USER=service
export DB_PASS=service
export DB_PORT=5432

clean:
	rm -rf dist/ build/
	find . -iname '*.pyc' -exec rm {} \; -print

install:
	pip install -r requirements.txt

test_install: install
	pip install -r test-requirements.txt

docker_build: clean
	docker build \
		-t ${DOCKER_IMAGE}-test \
		--target test \
		.
	docker build \
		-t ${DOCKER_IMAGE} \
		--target service \
		.

up:
	docker-compose --project-name ${DOCKER_NAME} up --remove-orphans -d

ps:
	docker-compose --project-name ${DOCKER_NAME} ps

logs:
	docker-compose --project-name ${DOCKER_NAME} logs

down:
	docker-compose --project-name ${DOCKER_NAME} logs -t
	docker-compose --project-name ${DOCKER_NAME} down --remove-orphans

migrate:
	git submodule update
	docker-compose --project-name ${DOCKER_NAME} up --remove-orphans migrate

docker_test:
	docker run \
		-u 0 \
		--rm \
		-e MRDB_SERVICE_URL=http://mrdb-api:8080 \
		-e IRR_SERVICE_URL=http://irr-api:8000 \
		-e LEAD_SERVICE_URL=http://lead-api:8080 \
		-e RENTAL_VALUATIONS_SERVICE_URL=http://rental-valuations-api:8080 \
		-e PROPERTIES_SERVICE_URL=http://properties-api:8080 \
		-e CUSTOMER_SERVICE_URL=http://customer-service:8080 \
		-e DB_HOST=peanut_db \
		-e CUSTOMER_DB_HOST=customer_db \
		-e CUSTOMER_DB_PORT=5432 \
		-e POSTCODES_IO_URL=https://api.postcodes.io \
		--network=${DOCKER_NAME}_default \
		${DOCKER_IMAGE}-test \
		make test

lint:
	flake8 nozama

test: test_install lint
	coverage run -m py.test -s --junitxml=tests/report.xml tests
	coverage report
	coverage html

run:
	python service.py
