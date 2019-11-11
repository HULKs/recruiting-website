run_production: build_production
	docker run -it -p 9000:80 recruiting

build_production:
	docker build -t recruiting -f Dockerfile .

run_tests: build_tests
	docker run -it recruiting

build_tests:
	docker build -t recruiting -f Dockerfile.test .
