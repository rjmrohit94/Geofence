
dependencies:
	@echo "=============Build Geo fence API Dependencies :local============="
	docker-compose up -d

down:
	docker-compose down

clean: down
	@echo "=============Clean Up: Geo fence API Images============="
	docker system prune -f
	docker volume prune -f