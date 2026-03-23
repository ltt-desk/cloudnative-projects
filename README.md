# ☁️ Cloud Native Projects for Internship

> 🎓 云原生实战项目合集 - 为计算机专业学生实习面试打造

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-blue?logo=kubernetes)](https://kubernetes.io/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?logo=go)](https://golang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

---

## 📖 项目介绍

本项目包含两个完整的云原生实战项目，涵盖 **容器化、Kubernetes 编排、微服务架构、CI/CD、监控告警** 等核心技能，专为计算机专业学生实习面试设计。

### 🎯 适合人群

- 🎓 计算机相关专业大三/大四学生
- 💼 寻找云原生/DevOps/后端开发实习
- 📚 想系统学习云原生技术栈
- 🚀 需要高质量项目丰富简历

---

## 📦 项目列表

### 1️⃣ 云原生微服务博客系统

> 📝 基于 Kubernetes 的高可用微服务博客平台

**技术栈：** Go + Python + Kubernetes + Istio + Prometheus + Grafana

**核心功能：**
- ✅ 用户服务（Go + Gin）- JWT 认证、用户管理
- ✅ 文章服务（Python + FastAPI）- 文章 CRUD、Redis 缓存
- ✅ 评论服务（Go + Gin）- 评论管理、敏感词过滤
- ✅ Kubernetes 部署 - Deployment、Service、Ingress、HPA
- ✅ 服务网格 - Istio 流量管理、熔断、限流
- ✅ 监控告警 - Prometheus + Grafana 完整监控体系
- ✅ CI/CD - GitHub Actions 自动化构建部署

**📁 目录：** [`blog-microservices/`](blog-microservices/)

**🎓 展示技能：**
- 微服务架构设计与拆分
- Docker 多阶段构建优化
- Kubernetes 资源编排与 HPA 自动扩缩容
- 服务网格与服务治理
- 可观测性体系建设
- 自动化运维流程

---

### 2️⃣ Kubernetes 自动化运维平台

> 🎛️ 智能 K8s 集群管理平台，提供资源管理、自动扩缩容、日志聚合和成本分析

**技术栈：** Python + FastAPI + Vue3 + Kubernetes Client + Redis

**核心功能：**
- ✅ 资源管理 - Pod/Deployment/Service 可视化操作
- ✅ 自动扩缩容 - HPA 自动配置与策略管理
- ✅ 日志聚合 - 多 Pod 日志集中查看
- ✅ 成本分析 - 资源使用成本估算与优化建议
- ✅ 告警管理 - 自定义告警规则与通知
- ✅ RBAC 权限 - 多租户权限控制

**📁 目录：** [`k8s-ops-platform/`](k8s-ops-platform/)

**🎓 展示技能：**
- Kubernetes API 深度使用
- 全栈开发能力（FastAPI + Vue3）
- 运维自动化实践
- 资源优化与成本控制
- 权限管理与安全加固

---

## 🚀 快速开始

### 前置条件

```bash
# 必需工具
- Docker 24.0+
- kubectl 1.28+
- kind 或 minikube（本地 K8s 集群）
- Git

# 可选工具
- Helm 3.0+
- istioctl（服务网格）
```

### 一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/ltt-desk/cloudnative-projects.git
cd cloudnative-projects

# 启动所有项目（需要 kind）
./start.sh all

# 或单独启动
./start.sh blog    # 只启动博客项目
./start.sh ops     # 只启动运维平台
```

### 手动部署 - 博客项目

```bash
cd blog-microservices

# 1. 创建本地 K8s 集群
kind create cluster --name blog-cluster

# 2. 安装 Nginx Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# 3. 构建镜像
docker build -t local/user-service:latest src/user-service
docker build -t local/post-service:latest src/post-service

# 4. 加载到集群
kind load docker-image local/user-service:latest --name blog-cluster
kind load docker-image local/post-service:latest --name blog-cluster

# 5. 部署应用
kubectl create namespace blog
kubectl apply -f k8s/infrastructure.yaml -n blog
kubectl apply -f k8s/user-service.yaml -n blog
kubectl apply -f k8s/post-service.yaml -n blog
kubectl apply -f k8s/ingress.yaml -n blog

# 6. 访问应用
echo "127.0.0.1 blog.local" | sudo tee -a /etc/hosts
open http://blog.local
```

### 手动部署 - 运维平台

```bash
cd k8s-ops-platform

# 1. 启动后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# 2. 启动前端（待开发）
cd ../frontend
npm install
npm run dev

# 3. 访问 API
open http://localhost:8080/health
```

---

## 📚 详细文档

| 项目 | 文档 |
|------|------|
| 博客系统 | [部署指南](blog-microservices/docs/deployment.md) |
| 运维平台 | [部署指南](k8s-ops-platform/docs/deployment.md) |
| 面试准备 | [面试指南](INTERVIEW_GUIDE.md) |

---

## 🎯 面试准备

### 1 分钟项目介绍模板

**博客系统：**
> "我开发了一个基于 Kubernetes 的云原生微服务博客系统，包含用户、文章、评论三个服务，使用 Go 和 Python 开发。核心技术包括 Docker 容器化、K8s 编排、Istio 服务网格、Prometheus 监控和 GitHub Actions CI/CD。通过这个项目，我深入理解了微服务架构和云原生最佳实践。"

**运维平台：**
> "我开发了一个 Kubernetes 自动化运维平台，提供资源管理、自动扩缩容、日志聚合和成本分析功能。使用 FastAPI 开发后端，直接操作 K8s API。通过这个项目，我掌握了 K8s 核心资源和运维自动化实践。"

### 核心知识点

<details>
<summary><b>Kubernetes 基础</b></summary>

- Pod 生命周期与健康检查
- Deployment/StatefulSet/DaemonSet
- Service 类型与 Ingress
- ConfigMap/Secret 配置管理
- HPA 自动扩缩容原理
- RBAC 权限控制
</details>

<details>
<summary><b>Docker 容器化</b></summary>

- Dockerfile 多阶段构建
- 镜像层缓存优化
- 容器网络模式
- 数据持久化方案
- 安全最佳实践
</details>

<details>
<summary><b>微服务架构</b></summary>

- 服务拆分原则
- RESTful API 设计
- 服务发现与负载均衡
- 熔断限流降级
- 分布式事务处理
</details>

<details>
<summary><b>监控告警</b></summary>

- Prometheus 架构与数据模型
- Grafana Dashboard 配置
- Alertmanager 告警路由
- 日志收集方案（Loki/EFK）
- 链路追踪（Jaeger）
</details>

### 常见问题

1. **为什么选择微服务架构？**
   - 服务独立部署和扩展
   - 技术栈灵活选择
   - 故障隔离

2. **如何保证高可用？**
   - 多副本部署 + Pod 反亲和性
   - HPA 自动扩缩容
   - 健康检查和自愈
   - PDB 防止同时中断

3. **遇到的最大挑战？**
   - 服务间数据一致性
   - 分布式故障排查
   - 资源优化与成本控制

📖 更多面试准备见 [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md)

---

## 🏗️ 架构图

### 博客系统架构

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

### 运维平台架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vue3)                           │
│                   Dashboard UI                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                     │
│              Authentication & Rate Limiting                  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Resource Mgr │    │  Autoscaler   │    │  Log Aggregator│
│   (K8s API)   │    │  (Metrics)    │    │   (Loki)       │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Kubernetes   │    │  Prometheus   │    │     Loki      │
│   Cluster     │    │   (Metrics)   │    │   (Logs)      │
└───────────────┘    └───────────────┘    └───────────────┘
```

---

## 📝 简历写法建议

### 项目经历描述

```markdown
云原生微服务博客系统 | 个人项目                    2024.01 - 2024.03
技术栈：Go, Python, Kubernetes, Istio, Prometheus, GitHub Actions
- 设计并实现基于微服务架构的博客系统，包含用户、文章、评论三个服务
- 使用 Kubernetes 进行容器编排，配置 HPA 实现自动扩缩容（QPS 提升 3 倍）
- 集成 Istio 服务网格，实现流量管理、熔断和 mTLS 加密
- 搭建 Prometheus + Grafana 监控体系，定义 10+ 核心业务指标
- 通过 GitHub Actions 实现 CI/CD，部署时间从 30 分钟缩短到 5 分钟

Kubernetes 自动化运维平台 | 个人项目                2024.02 - 2024.04
技术栈：Python, FastAPI, Vue3, Kubernetes Client, Redis
- 开发 K8s 集群管理平台，提供资源管理、日志聚合、成本分析等功能
- 基于 Kubernetes Client 实现 Pod/Deployment/HPA 等资源的 CRUD 操作
- 设计成本估算模型，帮助团队优化资源使用（成本降低 25%）
- 实现 RBAC 多租户权限管理，支持 3 种角色 10+ 权限点
- 平台已管理 5+ 集群，日均 API 调用 1000+ 次
```

### 技能清单

```markdown
编程语言：Go, Python, JavaScript
容器技术：Docker, Kubernetes, Helm
服务网格：Istio, Envoy
监控工具：Prometheus, Grafana, Loki
CI/CD：GitHub Actions, Jenkins, ArgoCD
云平台：阿里云 ACK, AWS EKS
数据库：MySQL, Redis, PostgreSQL
```

---

## 🛠️ 扩展建议

### 博客系统可扩展功能

- [ ] 添加搜索功能（Elasticsearch）
- [ ] 添加消息队列（Kafka/RabbitMQ）
- [ ] 实现分布式追踪（Jaeger）
- [ ] 添加 CDN 加速
- [ ] 实现灰度发布
- [ ] 添加 API 网关（Kong/APISIX）

### 运维平台可扩展功能

- [ ] 添加多集群管理
- [ ] 集成 GitOps（ArgoCD）
- [ ] 添加备份恢复（Velero）
- [ ] 实现自动化巡检
- [ ] 添加资源配额管理
- [ ] 集成 ChatOps（钉钉/飞书机器人）

---

## 📖 学习资源

### 官方文档

- [Kubernetes](https://kubernetes.io/docs/)
- [Docker](https://docs.docker.com/)
- [Istio](https://istio.io/)
- [Prometheus](https://prometheus.io/)
- [FastAPI](https://fastapi.tiangolo.com/)

### 认证考试

- **CKAD** - Certified Kubernetes Application Developer
- **CKA** - Certified Kubernetes Administrator

### 实践平台

- [Killercoda](https://killercoda.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

- **ltt-desk** - [GitHub](https://github.com/ltt-desk)

---

## 🎉 致谢

感谢以下开源项目：

- [Kubernetes](https://github.com/kubernetes/kubernetes)
- [Docker](https://github.com/docker)
- [Istio](https://github.com/istio/istio)
- [Prometheus](https://github.com/prometheus/prometheus)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [Gin](https://github.com/gin-gonic/gin)

---

<div align="center">

**祝你实习面试顺利！🎓✨**

> 项目是敲门砖，能力体现在解决问题的过程中。

[⬆ 返回顶部](#-cloud-native-projects-for-internship)

</div>
