up:
	docker-compose up -d
build:
	docker-compose build
stop:
	docker-compose stop
restart:
	docker-compose restart
proxy:
	docker-compose exec reverse-proxy bash
proxy-log:
	docker-compose exec reverse-proxy tail -f /var/log/nginx/access.log
bot-:
	docker-compose exec bot bash
bot-log:
	docker-compose exec bot tail -f /var/log/flask/access.log
