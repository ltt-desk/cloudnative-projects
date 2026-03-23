# 🌟 云原生实习项目合集

> 为计算机专业学生打造的云原生实战项目，助力实习面试

## 📚 项目列表

### 1. 云原生微服务博客系统 📝

**技术栈：** Go + Python + Kubernetes + Istio + Prometheus

**核心功能：**
- 用户服务（Go + Gin）
- 文章服务（Python + FastAPI）
- 评论服务（Go + Gin）
- JWT 认证
- 自动扩缩容（HPA）
- 服务网格（Istio）
- 监控告警（Prometheus + Grafana）
- CI/CD（GitHub Actions）

**适合展示的技能：**
- 微服务架构设计
- 容器化与编排
- 服务网格
- 可观测性
- 自动化运维

**📁 位置：** `blog-microservices/`

**🚀 快速启动：**
```bash
cd blog-microservices
make start-cluster
make deploy-all
```

---

### 2. Kubernetes 自动化运维平台 🎛️

**技术栈：** Python + FastAPI + Vue3 + Kubernetes Client

**核心功能：**
- 资源管理（Pod/Deployment/Service）
- 自动扩缩容（HPA 配置）
- 日志聚合
- 成本分析
- 告警管理
- RBAC 权限控制

**适合展示的技能：**
- K8s API 操作
- 后端开发（FastAPI）
- 前端开发（Vue3）
- 运维自动化
- 成本控制意识

**📁 位置：** `k8s-ops-platform/`

**🚀 快速启动：**
```bash
cd k8s-ops-platform
make backend  # 启动后端
make frontend # 启动前端
```

---

## 🎯 使用指南

### 面试准备流程

1. **理解项目架构** (1-2 天)
   - 阅读 README.md
   - 理解架构图
   - 了解技术选型原因

2. **本地部署运行** (1 天)
   - 按照部署文档操作
   - 确保能成功运行
   - 记录遇到的问题和解决方案

3. **深入代码细节** (2-3 天)
   - 阅读核心代码
   - 理解关键实现
   - 准备代码讲解

4. **准备面试话术** (1 天)
   - 1 分钟项目介绍
   - 技术难点和解决方案
   - 学到的经验和成长

5. **模拟面试** (1 天)
   - 找同学模拟面试
   - 录制讲解视频
   - 优化表达方式

### 项目演示建议

#### 博客系统演示流程

```
1. 展示架构图（2 分钟）
2. 演示应用访问（2 分钟）
   - 用户注册登录
   - 发布文章
   - 查看评论
3. 展示 Kubernetes 配置（3 分钟）
   - Deployment 配置
   - HPA 自动扩缩容演示
   - Service 和 Ingress
4. 展示监控面板（2 分钟）
   - Grafana Dashboard
   - Prometheus 指标查询
5. 展示 CI/CD 流程（2 分钟）
   - GitHub Actions 配置
   - 自动部署演示
```

#### 运维平台演示流程

```
1. 展示平台功能（2 分钟）
2. 演示资源管理（3 分钟）
   - 查看 Pod/Deployment
   - 扩缩容操作
   - 日志查看
3. 演示 HPA 配置（3 分钟）
   - 创建 HPA
   - 压测触发扩缩容
4. 展示成本分析（2 分钟）
   - 命名空间成本
   - 集群总成本
   - 优化建议
5. 演示告警管理（2 分钟）
   - 创建告警规则
   - 触发告警
```

---

## 📋 面试常见问题准备

### 技术基础

1. **Kubernetes 相关**
   - Pod 的生命周期
   - Service 的类型和区别
   - Deployment 和 StatefulSet 的区别
   - HPA 工作原理
   - ConfigMap 和 Secret 的使用

2. **Docker 相关**
   - Dockerfile 优化
   - 镜像分层原理
   - 容器网络模式
   - 数据持久化方案

3. **微服务相关**
   - 服务拆分原则
   - 服务间通信方式
   - 数据一致性处理
   - 熔断和限流

4. **监控相关**
   - Prometheus 架构
   - 指标类型（Counter/Gauge/Histogram）
   - 告警规则设计
   - 日志收集方案

### 项目相关问题

1. **为什么选择这个技术栈？**
2. **遇到的最大挑战是什么？如何解决的？**
3. **如果重新做，会做哪些改进？**
4. **如何保证系统的高可用？**
5. **如何进行性能优化？**
6. **安全方面做了哪些考虑？**

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
- [Vue3](https://vuejs.org/)

### 认证考试

- **CKAD** - Certified Kubernetes Application Developer
- **CKA** - Certified Kubernetes Administrator
- **DCA** - Docker Certified Associate

### 实践平台

- [Killercoda](https://killercoda.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)
- [阿里云 ACK 免费试用](https://www.aliyun.com/product/kubernetes)

---

## 🎓 简历写法建议

### 项目经历描述

```
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

```
编程语言：Go, Python, JavaScript
容器技术：Docker, Kubernetes, Helm
服务网格：Istio, Envoy
监控工具：Prometheus, Grafana, Loki
CI/CD：GitHub Actions, Jenkins, ArgoCD
云平台：阿里云 ACK, AWS EKS
数据库：MySQL, Redis, PostgreSQL
```

---

## 💡 最后建议

1. **理解胜过记忆** - 理解原理比死记硬背更重要
2. **动手实践** - 多动手部署和调试
3. **记录过程** - 写技术博客记录学习过程
4. **参与社区** - 加入云原生社区，参与讨论
5. **持续学习** - 云原生技术迭代快，保持学习

---

## 📞 支持

如果遇到问题：

1. 查看各项目的 `docs/` 目录
2. 阅读 `INTERVIEW_GUIDE.md`
3. 参考 Kubernetes 官方文档
4. 在 GitHub 提 Issue

---

**祝你实习面试顺利！🎉**

> 记住：项目是敲门砖，真正的能力体现在解决问题的过程中。
