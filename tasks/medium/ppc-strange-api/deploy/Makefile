COMPOSE=docker compose -p strange-api

.PHONY: deploy
deploy:
	@$(COMPOSE) up --build -d

.PHONY: logs
logs:
	@$(COMPOSE) logs

.PHONY: up
up:
	@$(COMPOSE) up --build

.PHONY: down
down:
	@$(COMPOSE) down --rmi all -v