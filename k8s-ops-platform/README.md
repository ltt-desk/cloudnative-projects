# 🎛️ Kubernetes 自动化运维平台

基于 Kubernetes 的智能运维管理平台，提供资源管理、自动扩缩容、日志聚合和成本分析功能。

## 📋 项目亮点

- ✅ **资源管理** - 可视化查看和管理 K8s 资源
- ✅ **自动扩缩容** - 基于指标的 HPA 自动配置
- ✅ **日志聚合** - 集中式日志查看与分析
- ✅ **成本分析** - 资源使用成本估算与优化建议
- ✅ **告警管理** - 自定义告警规则与通知
- ✅ **API 优先** - RESTful API + WebSocket 实时推送
- ✅ **权限控制** - RBAC 多租户支持

## 🏗️ 架构设计

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

## 🛠️ 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.104+ |
| 前端框架 | Vue3 + Element Plus | 3.3+ |
| K8s 客户端 | kubernetes-python | 28.0+ |
| 消息队列 | Redis | 7.2+ |
| 指标存储 | Prometheus | 2.47+ |
| 日志存储 | Loki | 2.9+ |
| 数据库 | PostgreSQL | 15+ |

## 📦 核心功能

### 1. 资源管理模块
- Pod/Deployment/Service 管理
- 资源使用率监控
- 配置管理 (ConfigMap/Secret)

### 2. 自动扩缩容模块
- 基于 CPU/内存的 HPA
- 自定义指标扩缩容
- 扩缩容策略配置

### 3. 日志聚合模块
- 多集群日志收集
- 日志搜索与过滤
- 日志告警

### 4. 成本分析模块
- 资源成本估算
- 优化建议
- 成本趋势分析

## 🚀 快速开始

### 前置条件

```bash
- Python 3.11+
- Node.js 18+
- Kubernetes 集群 (1.28+)
- Docker
```

### 一键部署

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd k8s-ops-platform

# 2. 启动后端
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# 3. 启动前端
cd ../frontend
npm install
npm run dev

# 4. 访问平台
# http://localhost:5173
```

## 📖 详细文档

- [部署指南](docs/deployment.md)
- [API 文档](docs/api.md)
- [用户手册](docs/user-guide.md)
- [开发指南](docs/development.md)

## 🎯 面试考点

通过这个项目展示：

1. **K8s API 熟练度** - 资源操作、事件处理
2. **后端开发能力** - API 设计、异步编程
3. **前端开发能力** - 响应式 UI、数据可视化
4. **可观测性理解** - 指标、日志、告警
5. **成本意识** - 资源优化、成本控制
6. **全栈能力** - 端到端系统设计与实现

## 📝 License

MIT
