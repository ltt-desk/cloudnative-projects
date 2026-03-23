# 🎨 GitHub 仓库完善指南

## 方法一：使用 GitHub CLI（推荐）

### 1. 安装 gh

```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. 登录 GitHub

```bash
gh auth login
```

选择：
- GitHub.com
- HTTPS
- Login with a web browser
- 复制代码，在浏览器中打开 https://github.com/login/device
- 粘贴代码并授权

### 3. 更新仓库信息

```bash
cd /home/admin/.openclaw/workspace/cloudnative-projects

# 更新仓库描述
gh repo edit --description "🎓 云原生实战项目合集 - 为计算机专业学生实习面试打造 | Kubernetes + Microservices + DevOps"

# 添加 Topics
gh repo edit --add-topics "kubernetes,cloud-native,microservices,devops,docker,k8s,golang,python,fastapi,istio,prometheus,cicd,internship,backend"

# 启用 Issues
gh repo edit --enable-issues

# 启用 Wiki
gh repo edit --enable-wiki

# 设置默认分支
gh repo edit --default-branch main
```

---

## 方法二：手动在网页上操作

### 1. 添加仓库描述

1. 访问：https://github.com/ltt-desk/cloudnative-projects
2. 点击右上角 **⚙️ Settings**
3. 在 **"About"** 区域点击编辑
4. 填写描述：
   ```
   🎓 云原生实战项目合集 - 为计算机专业学生实习面试打造
   ```
5. 添加网站（可选）：`https://github.com/ltt-desk`

### 2. 添加 Topics

1. 在仓库首页右侧 **"About"** 下方
2. 点击 **⚙️** 编辑按钮
3. 添加以下 Topics（用空格分隔）：
   ```
   kubernetes cloud-native microservices devops docker k8s golang python fastapi istio prometheus cicd internship backend
   ```
4. 点击 **Save changes**

### 3. 完善 README 徽章

在 README.md 顶部添加以下徽章（已包含在现有 README 中）：

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-blue?logo=kubernetes)](https://kubernetes.io/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?logo=go)](https://golang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Stars](https://img.shields.io/github/stars/ltt-desk/cloudnative-projects?style=social)](https://github.com/ltt-desk/cloudnative-projects/stargazers)
[![Forks](https://img.shields.io/github/forks/ltt-desk/cloudnative-projects?style=social)](https://github.com/ltt-desk/cloudnative-projects/network/members)
```

---

## 方法三：使用 API 脚本

创建 `update-github-info.sh` 脚本：

```bash
#!/bin/bash

# GitHub 仓库信息更新脚本

GITHUB_TOKEN="your_github_token_here"
REPO="ltt-desk/cloudnative-projects"

# 更新仓库描述
curl -X PATCH \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  https://api.github.com/repos/${REPO} \
  -d '{
    "description": "🎓 云原生实战项目合集 - 为计算机专业学生实习面试打造 | Kubernetes + Microservices + DevOps",
    "homepage": "https://github.com/ltt-desk",
    "has_issues": true,
    "has_wiki": true,
    "has_projects": false,
    "default_branch": "main"
  }'

# 添加 Topics
curl -X PUT \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  https://api.github.com/repos/${REPO}/topics \
  -d '{
    "names": [
      "kubernetes",
      "cloud-native",
      "microservices",
      "devops",
      "docker",
      "k8s",
      "golang",
      "python",
      "fastapi",
      "istio",
      "prometheus",
      "cicd",
      "internship",
      "backend"
    ]
  }'

echo "✅ 仓库信息更新完成！"
```

---

## 📋 完整的仓库信息建议

### 仓库名称
`cloudnative-projects`

### 描述
```
🎓 云原生实战项目合集 - 为计算机专业学生实习面试打造

包含两个完整项目：
1️⃣ 微服务博客系统 (Go + Python + K8s + Istio)
2️⃣ K8s 运维平台 (Python + FastAPI + Vue3)

涵盖：容器化、Kubernetes 编排、微服务架构、CI/CD、监控告警
```

### Topics
```
kubernetes cloud-native microservices devops docker k8s golang python fastapi istio prometheus cicd internship backend
```

### 分类
- **Primary category**: Software
- **Category**: Developer Tools / DevOps

### 许可证
✅ MIT License（已添加）

### 功能开关
- ✅ Issues: 启用
- ✅ Projects: 可选启用
- ✅ Wiki: 启用
- ✅ Discussions: 可选启用

---

## 🎨 添加徽章到 README

### 现有徽章（已包含）

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-blue?logo=kubernetes)](https://kubernetes.io/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?logo=go)](https://golang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
```

### 可选添加的徽章

```markdown
[![Stars](https://img.shields.io/github/stars/ltt-desk/cloudnative-projects?style=social)](https://github.com/ltt-desk/cloudnative-projects/stargazers)
[![Forks](https://img.shields.io/github/forks/ltt-desk/cloudnative-projects?style=social)](https://github.com/ltt-desk/cloudnative-projects/network/members)
[![Issues](https://img.shields.io/github/issues/ltt-desk/cloudnative-projects)](https://github.com/ltt-desk/cloudnative-projects/issues)
[![Last Commit](https://img.shields.io/github/last-commit/ltt-desk/cloudnative-projects)](https://github.com/ltt-desk/cloudnative-projects/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/ltt-desk/cloudnative-projects)](https://github.com/ltt-desk/cloudnative-projects)
```

---

## 📸 添加仓库封面（可选）

1. 访问：https://github.com/ltt-desk/cloudnative-projects
2. 点击 **README.md** 下方的编辑按钮
3. 在顶部添加仓库封面图片：

```markdown
<div align="center">
  <img src="https://socialify.git.ci/ltt-desk/cloudnative-projects/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Auto" alt="cloudnative-projects">
</div>
```

---

## ✅ 检查清单

完成以下操作：

- [ ] 添加仓库描述
- [ ] 添加 Topics（至少 5 个）
- [ ] 启用 Issues
- [ ] 启用 Wiki
- [ ] 添加徽章到 README
- [ ] 添加仓库封面（可选）
- [ ] 固定仓库到个人主页（可选）

---

## 🎯 固定仓库到个人主页

1. 访问：https://github.com/ltt-desk
2. 在 **"Pinned"** 区域点击 **Customize pins**
3. 勾选 `cloudnative-projects`
4. 点击 **Save pins**

---

## 🔗 分享仓库

仓库链接：https://github.com/ltt-desk/cloudnative-projects

可以分享到：
- 简历
- LinkedIn
- 技术博客
- 社交媒体

---

**完成这些设置后，你的 GitHub 仓库会更加专业和吸引人！🎉**
