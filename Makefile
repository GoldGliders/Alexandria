arg = bot

up:
	docker-compose up -d
build:
	docker-compose build
stop:
	docker-compose stop
restart:
	docker-compose restart ${arg}
ps:
	docker-compose ps
bash:
	docker-compose exec ${arg} bash
proxy-alog:
	docker-compose exec reverse-proxy tail -f /var/log/nginx/access.log
proxy-elog:
	docker-compose exec reverse-proxy tail -f /var/log/nginx/error.log
bot-log:
	docker-compose exec bot tail -f /var/log/flask/access.log
api-log:
	docker-compose logs -f --tail=30 api
liff-log:
	docker-compose logs -f --tail=30 liff
