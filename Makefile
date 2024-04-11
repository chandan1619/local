# Variables
FRONTEND_DIR = ./client
BACKEND_DIR = ./server
BACKEND_MAIN = main.py
CONDA_ENV_NAME = local_assistant
PORT_FRONTEND = 3000
PORT_BACKEND = 8000

# Default target to start everything
.PHONY: start
start: kill-ports setup-backend-env start-docker-compose
	@($(MAKE) start-backend &) && $(MAKE) start-frontend

# Kill processes running on the frontend and backend ports
.PHONY: kill-ports
kill-ports:
	@echo "Killing processes on ports $(PORT_FRONTEND) and $(PORT_BACKEND)..."
	-@lsof -ti :$(PORT_FRONTEND) | xargs kill -9
	-@lsof -ti :$(PORT_BACKEND) | xargs kill -9

# Setup the backend environment
.PHONY: setup-backend-env
setup-backend-env:
	@echo "Setting up the Conda environment..."
	@if conda info --envs | grep $(CONDA_ENV_NAME) >/dev/null; then \
		echo "Conda environment $(CONDA_ENV_NAME) already exists. Skipping environment creation."; \
	else \
		echo "Creating Conda environment $(CONDA_ENV_NAME)..."; \
		conda create --name $(CONDA_ENV_NAME) python=3.8 -y && \
		echo "Environment $(CONDA_ENV_NAME) created."; \
		echo "Installing requirements..."; \
		conda run --name $(CONDA_ENV_NAME) pip install -r $(BACKEND_DIR)/requirements.txt; \
	fi

# Start Docker Compose services
.PHONY: start-docker-compose
start-docker-compose:
	@echo "Starting Docker Compose services..."
	@cd $(BACKEND_DIR) && docker-compose -f docker-compose.dev.yml up -d

# Start the frontend application
.PHONY: start-frontend
start-frontend:
	@echo "Starting frontend server..."
	@cd $(FRONTEND_DIR) &&  npm install && npm start > frontend.log 2>&1

# Start the backend application and display logs
.PHONY: start-backend
start-backend:
	@echo "Starting backend server..."
	cd $(BACKEND_DIR) && python -u $(BACKEND_MAIN) | tee backend.log
