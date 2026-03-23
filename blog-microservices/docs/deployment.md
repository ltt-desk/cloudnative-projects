# 部署指南

## 本地开发环境部署

### 1. 前置条件

确保安装以下工具：

```bash
# Docker Desktop (包含 kubectl)
https://www.docker.com/products/docker-desktop

# 或使用 minikube
brew install minikube  # macOS
choco install minikube  # Windows

# kind (轻量级 K8s)
go install sigs.k8s.io/kind@latest

# Helm
brew install helm  # macOS
choco install helm  # Windows

# Istio
curl -L https://istio.io/downloadIstio | sh -
export PATH=$PWD/bin:$PATH

# kubectl
brew install kubectl  # macOS
choco install kubectl  # Windows
```

### 2. 启动集群

```bash
cd blog-microservices

# 使用 kind 启动本地集群
make start-cluster

# 或使用 minikube
minikube start --memory=4096 --cpus=2
minikube addons enable ingress
minikube addons enable metrics-server
```

### 3. 构建镜像

```bash
# 设置你的 Docker 用户名
export DOCKER_REGISTRY=docker.io/yourusername
export IMAGE_TAG=latest

# 构建所有镜像
make build

# 推送到镜像仓库（可选，本地开发可跳过）
make push

# 本地 kind 集群加载镜像
kind load docker-image $(DOCKER_REGISTRY)/user-service:$(IMAGE_TAG)
kind load docker-image $(DOCKER_REGISTRY)/post-service:$(IMAGE_TAG)
```

### 4. 部署应用

```bash
# 一键部署所有组件
make deploy-all

# 或分步部署
make deploy-infra   # 部署 MySQL, Redis
make deploy-services # 部署微服务
```

### 5. 验证部署

```bash
# 查看 Pod 状态
kubectl get pods -n blog

# 查看服务
kubectl get svc -n blog

# 查看 HPA
kubectl get hpa -n blog

# 测试健康检查
kubectl port-forward svc/user-service 8001:80 -n blog &
curl http://localhost:8001/health

kubectl port-forward svc/post-service 8002:80 -n blog &
curl http://localhost:8002/health
```

### 6. 访问应用

```bash
# 添加 hosts 条目 (需要 sudo)
echo "127.0.0.1 blog.local" | sudo tee -a /etc/hosts  # Linux/Mac
echo "127.0.0.1 blog.local" >> C:\Windows\System32\drivers\etc\hosts  # Windows

# 打开应用
make open-app

# 或手动访问
# http://blog.local
```

## 云环境部署

### AWS EKS

```bash
# 创建 EKS 集群
eksctl create cluster --name blog-cluster --region us-west-2 --nodes 2

# 配置 kubectl
aws eks update-kubeconfig --name blog-cluster --region us-west-2

# 安装 Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/aws/deploy.yaml

# 部署应用
make deploy-all
```

### 阿里云 ACK

```bash
# 创建 ACK 集群（通过控制台或 CLI）
aliyun cs CreateCluster --name blog-cluster --region cn-hangzhou

# 部署应用
make deploy-all

# 配置负载均衡
kubectl apply -f k8s/ingress-aliyun.yaml
```

## 监控与日志

### 部署 Prometheus + Grafana

```bash
# 添加 Helm 仓库
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 安装 kube-prometheus-stack
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# 访问 Grafana
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
# 用户名：admin, 密码：prom-operator
```

### 查看监控面板

1. 访问 http://localhost:3000
2. 导入 Dashboard ID: 315 (Kubernetes Cluster)
3. 导入 Dashboard ID: 10280 (JVM Micrometer)

## 故障排查

### Pod 无法启动

```bash
# 查看 Pod 状态
kubectl describe pod <pod-name> -n blog

# 查看日志
kubectl logs <pod-name> -n blog

# 进入容器调试
kubectl exec -it <pod-name> -n blog -- /bin/sh
```

### 服务无法访问

```bash
# 检查 Service
kubectl get svc -n blog

# 测试服务连通性
kubectl run test --rm -it --image=busybox --restart=Never -- wget -qO- http://user-service.blog.svc.cluster.local/health
```

### 数据库连接失败

```bash
# 检查 MySQL Pod
kubectl get pods -l app=mysql -n blog

# 查看 MySQL 日志
kubectl logs -l app=mysql -n blog

# 测试数据库连接
kubectl run mysql-test --rm -it --image=mysql:8.0 --restart=Never -- \
  mysql -h mysql.blog.svc.cluster.local -uroot -pblogpassword123
```

## 性能测试

```bash
# 安装 hey
go install github.com/rakyll/hey@latest

# 压测用户服务
hey -n 1000 -c 10 http://blog.local/api/v1/users

# 压测文章服务
hey -n 1000 -c 10 http://blog.local/api/v1/posts
```

## 清理资源

```bash
# 删除所有资源
make clean

# 删除 kind 集群
kind delete cluster --name blog-cluster

# 或删除 minikube
minikube delete
```
