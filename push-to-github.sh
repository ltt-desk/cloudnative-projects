#!/bin/bash

# GitHub 推送脚本
# 使用方法：./push-to-github.sh

set -e

echo "🚀 推送到 GitHub..."
echo ""

# 检查是否有 GitHub Token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  未设置 GITHUB_TOKEN 环境变量"
    echo ""
    echo "请使用以下方法之一推送："
    echo ""
    echo "方法 1: 使用 Personal Access Token"
    echo "  export GITHUB_TOKEN=your_token_here"
    echo "  ./push-to-github.sh"
    echo ""
    echo "方法 2: 使用 SSH"
    echo "  git remote set-url origin git@github.com:ltt-desk/cloudnative-projects.git"
    echo "  git push -u origin main"
    echo ""
    echo "方法 3: 手动推送"
    echo "  cd /home/admin/.openclaw/workspace/cloudnative-projects"
    echo "  git push -u origin main"
    echo ""
    exit 1
fi

# 使用 Token 推送
REPO_URL="https://${GITHUB_TOKEN}@github.com/ltt-desk/cloudnative-projects.git"

git remote set-url origin "${REPO_URL}"
git push -u origin main

echo ""
echo "✅ 推送成功！"
echo "🌐 访问：https://github.com/ltt-desk/cloudnative-projects"
