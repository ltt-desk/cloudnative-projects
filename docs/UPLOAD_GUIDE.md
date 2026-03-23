# 📤 GitHub 上传指南

## 方法一：使用 Personal Access Token（推荐）

### 1. 创建 Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写说明（如：cloudnative-projects-upload）
4. 勾选权限：`repo`（全选）
5. 点击 "Generate token"
6. **复制并保存 Token**（只显示一次！）

### 2. 推送代码

```bash
cd /home/admin/.openclaw/workspace/cloudnative-projects

# 设置 Token（替换 YOUR_TOKEN_HERE）
export GITHUB_TOKEN=your_token_here

# 运行推送脚本
./push-to-github.sh
```

或者手动推送：

```bash
# 使用 Token 推送
git remote set-url origin https://YOUR_TOKEN@github.com/ltt-desk/cloudnative-projects.git
git push -u origin main
```

---

## 方法二：使用 SSH

### 1. 生成 SSH Key（如果没有）

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. 添加 SSH Key 到 GitHub

1. 复制公钥内容：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 访问 https://github.com/settings/keys
3. 点击 "New SSH key"
4. 粘贴公钥内容，保存

### 3. 推送代码

```bash
cd /home/admin/.openclaw/workspace/cloudnative-projects

# 切换到 SSH 地址
git remote set-url origin git@github.com:ltt-desk/cloudnative-projects.git

# 推送
git push -u origin main
```

---

## 方法三：使用 GitHub CLI

### 1. 安装 gh

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. 登录并推送

```bash
cd /home/admin/.openclaw/workspace/cloudnative-projects

# 登录
gh auth login

# 推送
git push -u origin main
```

---

## 验证推送

推送完成后，访问：
https://github.com/ltt-desk/cloudnative-projects

检查文件是否完整：
- ✅ README.md（主文档）
- ✅ LICENSE（许可证）
- ✅ blog-microservices/（博客项目）
- ✅ k8s-ops-platform/（运维平台项目）
- ✅ INTERVIEW_GUIDE.md（面试指南）
- ✅ start.sh（启动脚本）

---

## 后续更新

```bash
# 提交更改
git add .
git commit -m "描述你的更改"

# 推送到 GitHub
git push
```

---

## 常见问题

### Q: 提示 "Permission denied"
**A:** 检查 Token 是否有 repo 权限，或 SSH Key 是否正确配置

### Q: 提示 "remote: Repository not found"
**A:** 确认仓库地址正确，或先创建空仓库

### Q: 推送太慢
**A:** 使用 `git push --quiet` 减少输出，或检查网络连接

---

## 下一步

上传完成后：

1. ✅ 完善 GitHub 仓库描述
2. ✅ 添加 Topics（kubernetes, cloud-native, microservices 等）
3. ✅ 设置 GitHub Pages（可选）
4. ✅ 添加 CI/CD Badge 到 README
5. ✅ 分享给朋友/同学获取反馈

祝你好运！🎉
