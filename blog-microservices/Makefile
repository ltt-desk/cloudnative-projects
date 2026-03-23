.PHONY: help start-cluster deploy-all build deploy clean open-app logs

DOCKER_REGISTRY ?= docker.io/yourusername
IMAGE_TAG ?= latest
NAMESPACE = blog

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

start-cluster: ## Start local Kubernetes cluster with kind
	@echo "Starting kind cluster..."
	kind create cluster --name blog-cluster --config=- <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
	@echo "Installing NGINX Ingress..."
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	@echo "Installing Istio..."
	istioctl install --set profile=demo -y
	@echo "Cluster ready!"

build: ## Build all Docker images
	@echo "Building user-service..."
	docker build -t $(DOCKER_REGISTRY)/user-service:$(IMAGE_TAG) src/user-service
	@echo "Building post-service..."
	docker build -t $(DOCKER_REGISTRY)/post-service:$(IMAGE_TAG) src/post-service
	@echo "Building comment-service..."
	docker build -t $(DOCKER_REGISTRY)/comment-service:$(IMAGE_TAG) src/comment-service

push: ## Push Docker images to registry
	docker push $(DOCKER_REGISTRY)/user-service:$(IMAGE_TAG)
	docker push $(DOCKER_REGISTRY)/post-service:$(IMAGE_TAG)
	docker push $(DOCKER_REGISTRY)/comment-service:$(IMAGE_TAG)

deploy-infra: ## Deploy infrastructure (MySQL, Redis)
	@echo "Deploying infrastructure..."
	kubectl apply -f k8s/infrastructure.yaml
	@echo "Waiting for infrastructure to be ready..."
	kubectl wait --for=condition=ready pod -l app=mysql -n $(NAMESPACE) --timeout=120s
	kubectl wait --for=condition=ready pod -l app=redis -n $(NAMESPACE) --timeout=120s

deploy-services: ## Deploy all microservices
	@echo "Deploying services..."
	export DOCKER_REGISTRY=$(DOCKER_REGISTRY) && export IMAGE_TAG=$(IMAGE_TAG) && \
	envsubst < k8s/user-service.yaml | kubectl apply -f -
	export DOCKER_REGISTRY=$(DOCKER_REGISTRY) && export IMAGE_TAG=$(IMAGE_TAG) && \
	envsubst < k8s/post-service.yaml | kubectl apply -f -
	export DOCKER_REGISTRY=$(DOCKER_REGISTRY) && export IMAGE_TAG=$(IMAGE_TAG) && \
	envsubst < k8s/comment-service.yaml | kubectl apply -f -
	kubectl apply -f k8s/ingress.yaml

deploy-all: deploy-infra deploy-services ## Deploy everything
	@echo "All services deployed!"
	@echo "Check status with: kubectl get pods -n $(NAMESPACE)"

deploy: deploy-all ## Alias for deploy-all

clean: ## Clean up all resources
	@echo "Deleting namespace $(NAMESPACE)..."
	kubectl delete namespace $(NAMESPACE) --ignore-not-found
	@echo "Cleanup complete!"

open-app: ## Open application in browser
	@echo "Opening http://blog.local"
	@xdg-open http://blog.local 2>/dev/null || open http://blog.local 2>/dev/null || echo "Visit: http://blog.local"

logs: ## Show logs from all services
	kubectl logs -l app=user-service -n $(NAMESPACE) -f
	kubectl logs -l app=post-service -n $(NAMESPACE) -f
	kubectl logs -l app=comment-service -n $(NAMESPACE) -f

status: ## Show deployment status
	kubectl get pods -n $(NAMESPACE)
	kubectl get svc -n $(NAMESPACE)
	kubectl get hpa -n $(NAMESPACE)

test: ## Run tests
	@echo "Running tests..."
	go test ./src/user-service/...
	cd src/post-service && pytest
