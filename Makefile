build:
	docker build -t recruiting .
run:
	docker run -it -p 9000:80 recruiting
