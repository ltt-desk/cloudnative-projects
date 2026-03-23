#!/bin/bash

# 云原生项目快速启动脚本
# 用于本地开发和演示

set -e

echo "🚀 云原生项目快速启动"
echo "====================="
echo ""

# 检查必要工具
check_requirements() {
    echo "📋 检查必要工具..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl 未安装，请先安装 kubectl"
        exit 1
    fi
    
    if ! command -v kind &> /dev/null; then
        echo "⚠️  kind 未安装，建议使用 kind 创建本地集群"
        echo "   安装命令：go install sigs.k8s.io/kind@latest"
    fi
    
    echo "✅ 必要工具检查完成"
    echo ""
}

# 启动博客微服务项目
start_blog_project() {
    echo "📝 启动博客微服务项目..."
    cd blog-microservices
    
    # 创建本地集群
    echo "🔧 创建 Kubernetes 集群..."
    kind create cluster --name blog-cluster --config=- <<EOF 2>/dev/null || true
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
    
    # 安装 Nginx Ingress
    echo "🌐 安装 Nginx Ingress..."
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml 2>/dev/null || true
    
    # 等待 Ingress 就绪
    echo "⏳ 等待 Ingress 就绪..."
    kubectl wait --namespace ingress-nginx \
      --for=condition=ready pod \
      --selector=app.kubernetes.io/component=controller \
      --timeout=90s 2>/dev/null || true
    
    # 创建命名空间
    echo "📦 创建命名空间..."
    kubectl create namespace blog --dry-run=client -o yaml | kubectl apply -f -
    
    # 部署基础设施
    echo "🗄️  部署基础设施（MySQL, Redis）..."
    kubectl apply -f k8s/infrastructure.yaml -n blog
    
    # 等待基础设施就绪
    echo "⏳ 等待基础设施就绪..."
    sleep 10
    
    # 构建并加载镜像
    echo "🐳 构建 Docker 镜像..."
    export DOCKER_REGISTRY=local
    export IMAGE_TAG=latest
    
    docker build -t local/user-service:latest src/user-service 2>/dev/null || echo "⚠️  user-service 构建跳过"
    docker build -t local/post-service:latest src/post-service 2>/dev/null || echo "⚠️  post-service 构建跳过"
    
    # 加载到 kind
    echo "📥 加载镜像到集群..."
    kind load docker-image local/user-service:latest --name blog-cluster 2>/dev/null || true
    kind load docker-image local/post-service:latest --name blog-cluster 2>/dev/null || true
    
    # 部署服务
    echo "🚀 部署微服务..."
    export DOCKER_REGISTRY=local
    export IMAGE_TAG=latest
    envsubst < k8s/user-service.yaml | kubectl apply -f - 2>/dev/null || true
    envsubst < k8s/post-service.yaml | kubectl apply -f - 2>/dev/null || true
    kubectl apply -f k8s/ingress.yaml -n blog 2>/dev/null || true
    
    # 显示访问信息
    echo ""
    echo "✅ 博客微服务项目启动完成！"
    echo ""
    echo "📊 查看服务状态:"
    echo "   kubectl get pods -n blog"
    echo "   kubectl get svc -n blog"
    echo ""
    echo "🌐 访问应用:"
    echo "   添加 hosts: echo '127.0.0.1 blog.local' | sudo tee -a /etc/hosts"
    echo "   访问地址：http://blog.local"
    echo ""
    echo "🔍 查看日志:"
    echo "   kubectl logs -l app=user-service -n blog -f"
    echo "   kubectl logs -l app=post-service -n blog -f"
    echo ""
    
    cd ..
}

# 启动 K8s 运维平台项目
start_k8s_ops_project() {
    echo "🎛️  启动 K8s 运维平台项目..."
    cd k8s-ops-platform
    
    # 创建命名空间
    echo "📦 创建命名空间..."
    kubectl create namespace k8s-ops --dry-run=client -o yaml | kubectl apply -f -
    
    # 部署应用
    echo "🚀 部署应用..."
    export DOCKER_REGISTRY=local
    export IMAGE_TAG=latest
    
    # 构建镜像
    docker build -t local/k8s-ops-backend:latest backend 2>/dev/null || echo "⚠️  backend 构建跳过"
    kind load docker-image local/k8s-ops-backend:latest --name blog-cluster 2>/dev/null || true
    
    # 部署
    envsubst < k8s/deployment.yaml | kubectl apply -f - 2>/dev/null || true
    
    # 显示访问信息
    echo ""
    echo "✅ K8s 运维平台项目启动完成！"
    echo ""
    echo "📊 查看服务状态:"
    echo "   kubectl get pods -n k8s-ops"
    echo "   kubectl get svc -n k8s-ops"
    echo ""
    echo "🌐 访问应用:"
    echo "   kubectl port-forward svc/k8s-ops-backend -n k8s-ops 8080:80"
    echo "   访问地址：http://localhost:8080"
    echo ""
    echo "📖 API 测试:"
    echo "   curl http://localhost:8080/health"
    echo "   curl http://localhost:8080/api/v1/namespaces"
    echo ""
    
    cd ..
}

# 显示帮助信息
show_help() {
    echo "使用方法:"
    echo "  ./start.sh              - 启动所有项目"
    echo "  ./start.sh blog         - 只启动博客项目"
    echo "  ./start.sh ops          - 只启动运维平台项目"
    echo "  ./start.sh clean        - 清理所有资源"
    echo "  ./start.sh help         - 显示帮助信息"
    echo ""
}

# 清理资源
clean_resources() {
    echo "🧹 清理资源..."
    kubectl delete namespace blog --ignore-not-found
    kubectl delete namespace k8s-ops --ignore-not-found
    kind delete cluster --name blog-cluster 2>/dev/null || true
    echo "✅ 清理完成!"
}

# 主程序
main() {
    case "${1:-all}" in
        blog)
            check_requirements
            start_blog_project
            ;;
        ops)
            check_requirements
            start_k8s_ops_project
            ;;
        all)
            check_requirements
            start_blog_project
            start_k8s_ops_project
            ;;
        clean)
            clean_resources
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "❌ 未知参数：$1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
