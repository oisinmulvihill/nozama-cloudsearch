# nozama-cloudsearch developer, build and release helpers
#
# Oisin mulvihill
# 2019-06-22
#
GIT_COMMIT?=$(shell git rev-parse HEAD)
DOCKER_NAME=nozama-cloudsearch
DOCKER_IMAGE=${DOCKER_NAME}:${GIT_COMMIT}
DOCKER_REPO=oisinmulvihill/${DOCKER_NAME}

clean:
	rm -rf dist/ build/
	find . -iname '*.pyc' -exec rm {} \; -print

install:
	pip install -r requirements.txt
	python setup.py develop

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

tail:
	docker-compose --project-name ${DOCKER_NAME} logs -f

down:
	docker-compose --project-name ${DOCKER_NAME} logs -t
	docker-compose --project-name ${DOCKER_NAME} down --remove-orphans

docker_test: docker_build
	# Hostnames for mongo and elastic search are set in the "docker-compose.yaml".
	# The test container joins the docker compose created network so that the
	# hostnames
	docker run \
		-u 0 \
		--rm \
		-e MONGO_HOST=mongo \
	  -e ELASTICSEARCH_HOST=elasticsearch \
		--network=${DOCKER_NAME}_default \
		${DOCKER_IMAGE}-test \
		make test

lint:
	flake8 nozama

test: test_install lint
	coverage run -m py.test -s --cov=nozama-cloudsearch --junitxml=tests/report.xml tests

run:
	pserve development.ini

test_pypi_release:
	pip install twine
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release_to_pypi:
	twine upload dist/*

docker_release:
	# Push the latest container version which is tagged with the git commit. Then
	# Tag the latest build and push this as well.
	docker login
	docker tag ${DOCKER_IMAGE} ${DOCKER_REPO}:${GIT_COMMIT}
	docker push ${DOCKER_REPO}:${GIT_COMMIT}
	docker tag ${DOCKER_IMAGE} ${DOCKER_REPO}:latest
	docker push ${DOCKER_REPO}:latest
