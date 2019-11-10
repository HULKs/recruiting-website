build:
	docker build -t recruiting -f Dockerfile .
test:
	docker build -t recruiting -f Dockerfile.test .
run:
	docker run -it -p 9000:80 recruiting
