.DEFAULT_GOAL := help

run: ## Run the application using uvicorn with provided args or defaults
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file $(ENV_FILE)
	##poetry run gunicorn app.main:app -c gunicorn.conf.py

install: ## Install dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?##"}; {printf " %-20s %s\n", $$1, $$2}'
