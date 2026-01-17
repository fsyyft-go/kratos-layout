#!/bin/bash
set -e

# Docker CLI 安装脚本
# 本脚本仅安装 Docker CLI 客户端（docker-ce-cli、docker-buildx-plugin、docker-compose-plugin），
# 不包含 Docker daemon。
#
# 使用说明：
# 安装完成后，需要在容器启动时挂载宿主机的 Docker socket 才能使用 Docker 能力。
#
# 1. docker run 使用方式：
#    docker run -v /var/run/docker.sock:/var/run/docker.sock ...
#
# 2. docker-compose.yml 使用方式：
#    services:
#      your-service:
#        volumes:
#          - /var/run/docker.sock:/var/run/docker.sock
#
# 通过挂载 Docker socket，容器内的 docker 命令将直接操作宿主机的 Docker daemon，
# 可以查看和管理宿主机的所有容器、镜像、网络等资源。

echo "=== 开始安装 Docker CLI ==="

# 添加 Docker 官方 GPG 密钥。
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "✓ GPG 密钥已添加"

# 添加 Docker APT 源。
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
echo "✓ Docker APT 源已添加"

# 更新 APT 并安装 Docker CLI（仅客户端，不包含 daemon）。
apt-get -y update
echo "✓ APT 更新完成"

apt-get install -y \
    docker-ce-cli \
    docker-buildx-plugin \
    docker-compose-plugin
echo "✓ Docker CLI 安装完成"

# 显示安装的版本。
echo ""
echo "=== 安装的组件版本 ==="
docker --version
docker buildx version
docker compose version

echo ""
echo "=== Docker CLI 安装成功 ==="
