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
proxy-alog:
	docker-compose exec reverse-proxy tail -f /var/log/nginx/access.log
proxy-elog:
	docker-compose exec reverse-proxy tail -f /var/log/nginx/error.log
bot-:
	docker-compose exec bot bash
bot-log:
	docker-compose exec bot tail -f /var/log/flask/access.log
api-:
	docker-compose exec api bash
api-log:
	docker-compose exec api tail -f /var/log/flask/access.log
