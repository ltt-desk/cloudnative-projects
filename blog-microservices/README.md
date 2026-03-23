# 🚀 云原生微服务博客系统

基于 Kubernetes 的高可用微服务博客平台，展示云原生核心技术能力。

## 📋 项目亮点

- ✅ **微服务架构** - 用户服务、文章服务、评论服务独立部署
- ✅ **容器化** - Docker 多阶段构建，镜像优化
- ✅ **Kubernetes 部署** - Deployment、Service、Ingress、HPA
- ✅ **服务网格** - Istio 流量管理、熔断、限流
- ✅ **可观测性** - Prometheus + Grafana 监控告警
- ✅ **CI/CD** - GitHub Actions 自动化构建部署
- ✅ **配置管理** - ConfigMap + Secret 配置分离
- ✅ **持久化** - MySQL + Redis 数据存储

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                         Ingress                              │
│                    (Nginx Controller)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Istio Service Mesh                      │
│              (Traffic Management & Security)                 │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  User Service │    │ Post Service  │    │Comment Service│
│     (Go)      │    │   (Python)    │    │    (Go)       │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│     Redis     │    │     MySQL     │    │     Redis     │
│   (Cache)     │    │   (Storage)   │    │   (Cache)     │
└───────────────┘    └───────────────┘    └───────────────┘
```

## 🛠️ 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 容器运行时 | Docker | 24.0+ |
| 编排平台 | Kubernetes | 1.28+ |
| 服务网格 | Istio | 1.19+ |
| API 网关 | Nginx Ingress | 1.9+ |
| 监控 | Prometheus + Grafana | 2.47+ |
| 日志 | Loki + Promtail | 2.9+ |
| 数据库 | MySQL | 8.0+ |
| 缓存 | Redis | 7.2+ |
| CI/CD | GitHub Actions | - |

## 📦 服务说明

### 1. 用户服务 (user-service)
- Go + Gin 框架
- JWT 认证
- 用户注册/登录/信息管理
- 端口：8001

### 2. 文章服务 (post-service)
- Python + FastAPI
- 文章 CRUD 操作
- Markdown 渲染
- 端口：8002

### 3. 评论服务 (comment-service)
- Go + Gin 框架
- 评论管理
- 敏感词过滤
- 端口：8003

## 🚀 快速开始

### 前置条件

```bash
# 本地开发环境
- Docker Desktop / minikube / kind
- kubectl
- helm
- istioctl
```

### 一键部署

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd blog-microservices

# 2. 启动本地 Kubernetes 集群
make start-cluster

# 3. 部署所有服务
make deploy-all

# 4. 查看服务状态
kubectl get pods -n blog
kubectl get svc -n blog

# 5. 访问应用
make open-app
# http://blog.local
```

## 📖 详细文档

- [部署指南](docs/deployment.md)
- [开发指南](docs/development.md)
- [监控配置](docs/monitoring.md)
- [故障排查](docs/troubleshooting.md)

## 🎯 面试考点

通过这个项目，你可以展示以下技能：

1. **容器化能力** - Dockerfile 编写、镜像优化
2. **K8s 掌握程度** - 资源定义、服务发现、配置管理
3. **微服务理解** - 服务拆分、API 设计、数据一致性
4. **可观测性** - 监控指标、日志收集、链路追踪
5. **自动化运维** - CI/CD 流程、GitOps 实践
6. **问题解决能力** - 故障排查、性能优化

## 📝 License

MIT
