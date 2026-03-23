.PHONY: help build push deploy clean dev backend frontend

DOCKER_REGISTRY ?= docker.io/yourusername
IMAGE_TAG ?= latest

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development environment
	@echo "Starting backend..."
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py &
	@echo "Starting frontend..."
	cd frontend && npm install && npm run dev

backend: ## Run backend locally
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py

frontend: ## Run frontend locally
	cd frontend && npm install && npm run dev

build: ## Build Docker images
	@echo "Building backend..."
	docker build -t $(DOCKER_REGISTRY)/k8s-ops-backend:$(IMAGE_TAG) backend
	@echo "Building frontend..."
	docker build -t $(DOCKER_REGISTRY)/k8s-ops-frontend:$(IMAGE_TAG) frontend

push: ## Push Docker images
	docker push $(DOCKER_REGISTRY)/k8s-ops-backend:$(IMAGE_TAG)
	docker push $(DOCKER_REGISTRY)/k8s-ops-frontend:$(IMAGE_TAG)

deploy: ## Deploy to Kubernetes
	@echo "Deploying to Kubernetes..."
	export DOCKER_REGISTRY=$(DOCKER_REGISTRY) && export IMAGE_TAG=$(IMAGE_TAG) && \
	envsubst < k8s/deployment.yaml | kubectl apply -f -
	kubectl apply -f k8s/ingress.yaml
	@echo "Deployment complete!"

deploy-local: ## Deploy to local cluster
	@echo "Loading images to kind..."
	kind load docker-image $(DOCKER_REGISTRY)/k8s-ops-backend:$(IMAGE_TAG)
	kind load docker-image $(DOCKER_REGISTRY)/k8s-ops-frontend:$(IMAGE_TAG)
	@echo "Deploying..."
	export DOCKER_REGISTRY=$(DOCKER_REGISTRY) && export IMAGE_TAG=$(IMAGE_TAG) && \
	envsubst < k8s/deployment.yaml | kubectl apply -f -

clean: ## Clean up all resources
	@echo "Deleting namespace k8s-ops..."
	kubectl delete namespace k8s-ops --ignore-not-found
	@echo "Cleanup complete!"

logs: ## Show logs
	kubectl logs -l app=k8s-ops-backend -n k8s-ops -f

status: ## Show deployment status
	kubectl get pods -n k8s-ops
	kubectl get svc -n k8s-ops

test: ## Run tests
	@echo "Running backend tests..."
	cd backend && pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

docs: ## Generate API docs
	cd backend && python -m fastapi dev main.py --docs
