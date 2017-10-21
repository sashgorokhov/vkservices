

build:
	docker build -t vkservices .

run:
	docker run -d --name vkservices -p 80:80 --restart always vkservices

stop:
	docker stop vkservices

rm:
	docker rm -fv vkservices

logs:
	docker logs -f vkservices