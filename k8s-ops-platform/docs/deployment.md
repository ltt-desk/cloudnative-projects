# K8s Ops Platform 部署指南

## 快速开始

### 1. 本地开发环境

```bash
# 克隆项目
git clone <your-repo-url>
cd k8s-ops-platform

# 启动后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# 新终端启动前端
cd ../frontend
npm install
npm run dev

# 访问 http://localhost:5173
```

### 2. Kubernetes 部署

#### 前置条件

- Kubernetes 集群 (1.28+)
- kubectl 已配置
- Docker 镜像仓库账号

#### 部署步骤

```bash
# 1. 设置环境变量
export DOCKER_REGISTRY=docker.io/yourusername
export IMAGE_TAG=latest

# 2. 构建镜像
make build

# 3. 推送镜像
make push

# 4. 部署到 K8s
make deploy

# 5. 查看状态
kubectl get pods -n k8s-ops
kubectl get svc -n k8s-ops

# 6. 端口转发访问
kubectl port-forward svc/k8s-ops-backend -n k8s-ops 8080:80
```

### 3. 配置 Kubeconfig

后端服务需要访问 Kubernetes 集群：

```bash
# 方式一：使用 ServiceAccount (推荐生产环境)
# deployment.yaml 中已配置 RBAC

# 方式二：挂载 kubeconfig (开发环境)
kubectl create secret generic kubeconfig-secret \
  --from-file=kubeconfig=$HOME/.kube/config \
  -n k8s-ops

# 在 deployment 中添加 volumeMount
```

## 功能演示

### API 测试

```bash
# 健康检查
curl http://localhost:8080/health

# 获取所有命名空间
curl http://localhost:8080/api/v1/namespaces

# 获取 Pod 列表
curl http://localhost:8080/api/v1/namespaces/default/pods

# 获取 Deployment 列表
curl http://localhost:8080/api/v1/namespaces/default/deployments

# 扩缩容 Deployment
curl -X POST "http://localhost:8080/api/v1/namespaces/default/deployments/my-app/scale?replicas=3"

# 创建 HPA
curl -X POST http://localhost:8080/api/v1/hpas \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-app-hpa",
    "namespace": "default",
    "target_deployment": "my-app",
    "min_replicas": 2,
    "max_replicas": 10,
    "target_cpu_utilization": 70
  }'

# 获取成本估算
curl http://localhost:8080/api/v1/cost/namespace/default
curl http://localhost:8080/api/v1/cost/cluster

# 创建告警规则
curl -X POST http://localhost:8080/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "high-cpu",
    "namespace": "default",
    "metric": "cpu_utilization",
    "threshold": 80,
    "comparison": "gt",
    "action": "email"
  }'
```

## 监控配置

### Prometheus 集成

```yaml
# 添加 ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: k8s-ops-backend
  namespace: k8s-ops
spec:
  selector:
    matchLabels:
      app: k8s-ops-backend
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Grafana Dashboard

导入 Dashboard ID: 15200 (FastAPI Dashboard)

## 故障排查

### 后端无法连接 K8s

```bash
# 检查 ServiceAccount
kubectl get sa k8s-ops-sa -n k8s-ops

# 检查 RBAC 权限
kubectl auth can-i list pods --as=system:serviceaccount:k8s-ops:k8s-ops-sa

# 查看日志
kubectl logs -l app=k8s-ops-backend -n k8s-ops
```

### 前端无法连接后端

```bash
# 检查服务
kubectl get svc -n k8s-ops

# 测试连通性
kubectl run test --rm -it --image=curlimages/curl --restart=Never -- \
  curl http://k8s-ops-backend.k8s-ops.svc.cluster.local/health
```

## 安全加固

### 1. 启用认证

```python
# 添加 JWT 认证
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # 验证 token
    pass
```

### 2. 限制 RBAC 权限

```yaml
# 只读权限
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
```

### 3. 网络策略

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: k8s-ops-policy
  namespace: k8s-ops
spec:
  podSelector:
    matchLabels:
      app: k8s-ops-backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: k8s-ops-frontend
    ports:
    - protocol: TCP
      port: 8080
```

## 性能优化

### 1. 启用缓存

```python
# Redis 缓存
@cache.cached(timeout=60)
async def get_pods(namespace: str):
    # ...
```

### 2. 异步处理

```python
# 后台任务
async def background_task():
    # 耗时操作
    pass

@app.post("/trigger")
async def trigger(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task)
```

### 3. 连接池

```python
# K8s client 连接池
config.load_incluster_config()
v1 = client.CoreV1Api()
```

## 扩展开发

### 添加新功能模块

1. 在 `backend/main.py` 添加 API 路由
2. 在 `frontend/src/views` 添加前端页面
3. 更新 `k8s/deployment.yaml`
4. 编写测试用例

### 集成其他服务

- **Loki**: 日志聚合
- **Jaeger**: 链路追踪
- **ArgoCD**: GitOps 部署
- **Velero**: 备份恢复
