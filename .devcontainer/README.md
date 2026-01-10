# Kratos Layout DevContainer 配置指南

## 1. 概述

### 1.1 什么是 DevContainer

DevContainer（Development Container）是 VS Code 提供的一项功能，允许开发者使用 Docker 容器作为完整的开发环境。通过 DevContainer，您可以：

- **环境一致性**：所有团队成员使用完全相同的开发环境
- **快速上手**：新成员无需手动安装复杂的开发工具链
- **隔离性**：开发环境与宿主机环境隔离，避免冲突
- **可移植性**：开发环境可以在任何支持 Docker 的平台上运行

### 1.2 本项目提供的两种配置方式

本项目提供了两种 DevContainer 配置方式，分别位于不同的示例目录中：

| 配置方式 | 示例目录 | 配置文件 | 说明 |
|---------|---------|---------|------|
| **Dockerfile 方式** | `.devcontainer/example-dockerfile/` | `devcontainer.json` | 直接基于 Dockerfile 构建容器镜像 |
| **Docker Compose 方式** | `.devcontainer/example-compose/` | `devcontainer.json` + `docker-compose.yml` | 使用本地预构建镜像，通过 Docker Compose 启动 |

### 1.3 两种方式对比

| 特性 | Dockerfile 方式 | Docker Compose 方式 |
|------|----------------|-------------------|
| **启动速度** | 较慢（需要构建） | **快（直接使用镜像）** |
| **首次使用** | 需要联网构建（15-30 分钟） | 需要预构建镜像（一次性） |
| **后续启动** | 2-5 分钟（有缓存） | < 1 分钟 |
| **配置复杂度** | 简单 | 中等 |
| **服务编排** | 不支持 | **支持** |
| **扩展性** | 有限 | **强大** |
| **镜像管理** | 本地构建 | 本地预构建镜像 |
| **适用场景** | 单容器开发 | 多容器协作开发 |

### 1.4 推荐使用场景

#### 选择 Dockerfile 方式
- ✅ 需要 Dockerfile 中的最新配置
- ✅ 不确定是否会频繁使用 DevContainer
- ✅ 希望完全控制构建过程
- ✅ 只需要单容器开发环境

#### 选择 Docker Compose 方式
- ✅ **需要快速启动开发环境（推荐）**
- ✅ 需要多容器协作（如数据库、Redis 等）
- ✅ 团队成员需要统一环境
- ✅ 网络环境不稳定（构建镜像可能失败）

## 2. 快速开始

### 2.1 前置要求

在开始之前，请确保您的系统已安装以下软件：

| 软件 | 版本要求 | 检查命令 | 安装说明 |
|------|---------|---------|---------|
| **Docker** | 最新稳定版 | `docker --version` | [Docker 官网](https://www.docker.com/get-started) |
| **VS Code** | 最新版本 | `code --version` | [VS Code 官网](https://code.visualstudio.com/) |
| **DevContainer 扩展** | 最新版本 | 在 VS Code 扩展中搜索 "Dev Containers" | VS Code 内置扩展 |

### 2.2 首次使用前初始化

在启动 DevContainer 之前，需要先运行以下命令来初始化必要的目录结构和数据持久化目录：

```bash
make devcontainer-init
```

该命令会自动创建以下目录：

| 目录 | 用途 | 容器内路径 |
|------|------|-----------|
| `.devcontainer/data/.venv` | Python 虚拟环境目录 | `/development/.../kratos-layout/.venv` |
| `.devcontainer/data/go/cache` | Go 缓存目录 | `/usr/local/go/cache` |
| `.devcontainer/data/go/path` | Go PATH 目录 | `/usr/local/go/path` |
| `.devcontainer/data/data` | 通用数据目录 | `/data` |

**重要提示**：
- ✅ 所有这些目录都已在 `.gitignore` 中配置，不会被提交到 Git
- ⚠️ Python 虚拟环境需要在容器启动后，在容器内运行 `python -m venv .venv` 进行初始化

### 2.3 选择配置方式

根据您的需求选择合适的配置方式：

#### 场景 1：快速启动（推荐 Docker Compose 方式）
```bash
# 步骤 1：构建镜像（仅需执行一次）
cd .devcontainer/docker
./scripts/build

# 步骤 2：复制配置文件
cp example-compose/devcontainer.json ../devcontainer.json
cp example-compose/docker-compose.yml ../docker-compose.yml

# 步骤 3：启动 DevContainer
# 使用 VS Code 打开项目，选择 "在 DevContainer 中重新打开"
```

#### 场景 2：完全控制（Dockerfile 方式）
```bash
# 步骤 1：复制配置文件
cp example-dockerfile/devcontainer.json devcontainer.json

# 步骤 2：启动 DevContainer
# 使用 VS Code 打开项目，选择 "在 DevContainer 中重新打开"
# VS Code 会自动构建容器镜像（首次需要 15-30 分钟）
```

### 2.4 启动 DevContainer

配置文件准备好后，使用 VS Code 打开项目：

```bash
# 在项目根目录执行
code .
```

然后 VS Code 会弹出提示：
```
"Dev Container: This folder contains a Dev Container configuration. Do you want to reopen the folder in a container?"
```

点击 **"Reopen in Container"** 即可。

## 3. Dockerfile 方式

### 3.1 方式特点

Dockerfile 方式的特点：

- ✅ **配置简单**：只需要一个 `devcontainer.json` 文件
- ✅ **完全控制**：可以修改 Dockerfile 自定义构建过程
- ❌ **首次构建时间长**：需要 15-30 分钟下载和构建
- ❌ **依赖网络**：需要稳定的网络连接下载依赖
- ✅ **自动缓存**：后续构建会使用缓存，只需 2-5 分钟

### 3.2 使用步骤

#### 步骤 1：复制配置文件

将示例配置文件复制到 `.devcontainer/` 目录：

```bash
cd .devcontainer
cp example-dockerfile/devcontainer.json devcontainer.json
```

#### 步骤 2：配置环境变量（可选）

创建或编辑项目根目录的 `.env` 文件：

```bash
# .env 文件示例
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=glm-4.7
```

#### 步骤 3：启动 DevContainer

1. 使用 VS Code 打开项目：`code .`
2. 在弹出的提示中选择 **"在 DevContainer 中重新打开"**
3. 等待容器构建完成（首次需要 15-30 分钟）

### 3.3 构建时间说明

#### 首次构建（无缓存）

- **预计时间**：15-30 分钟（取决于网络速度）
- **网络要求**：需要稳定网络连接
- **下载内容**：
  | 内容 | 大小 | 说明 |
  |------|------|------|
  | 基础镜像 | ~500 MB | Ubuntu 基础镜像 |
  | APT 包 | ~200 MB | 系统工具和库 |
  | Go 安装包 | ~130 MB | Go 1.25.5 |
  | Node.js 包 | ~50 MB | Node.js LTS |
  | Go 工具 | ~100 MB | 开发工具（wire、protoc 等） |
  | AI 工具 | ~100 MB | Claude Code、Gemini CLI 等 |

#### 后续构建（有缓存）

- **预计时间**：2-5 分钟
- **缓存机制**：
  | 缓存类型 | 缓存位置 | 说明 |
  |---------|---------|------|
  | APT 缓存 | `/var/cache/apt`、`/var/lib/apt/lists` | Debian 包缓存 |
  | Go 模块缓存 | `/go/pkg/mod` | Go 依赖包缓存 |
  | NPM 缓存 | `/root/.npm` | Node.js 包缓存 |

- **重新构建条件**：
  - ✅ Dockerfile 被修改
  - ✅ `resources/*.sh` 安装脚本被修改
  - ✅ 构建参数（`ARG`）改变（如 `UBUNTU_VERSION`、`CLAUDE_CODE_VERSION`）

#### 网络优化

本项目已配置国内镜像源以加速下载：

| 源类型 | 镜像地址 | 说明 |
|--------|---------|------|
| APT 源 | 清华大学镜像 | Ubuntu 包管理器 |
| Go 源 | 阿里云镜像 | Go 模块下载 |
| NPM 源 | npmmirror 镜像 | Node.js 包下载 |

### 3.4 配置文件说明

Dockerfile 方式使用的配置文件：

| 文件 | 位置 | 说明 |
|------|------|------|
| `devcontainer.json` | `.devcontainer/devcontainer.json` | DevContainer 主配置文件 |
| `Dockerfile` | `.devcontainer/docker/Dockerfile` | 容器镜像构建文件 |
| `resources/*.sh` | `.devcontainer/docker/resources/` | 安装脚本 |

**重要配置项**：

```json
{
  "name": "Kratos Layout Dev Container",
  "dockerFile": "docker/Dockerfile",  // Dockerfile 路径（相对路径）
  "build": {
    "context": "docker/",              // 构建上下文
    "args": {
      "UBUNTU_VERSION": "ubuntu24.04", // Ubuntu 版本
      "CLAUDE_CODE_VERSION": "1.x"     // Claude Code 版本（1.x 或 2.x）
    }
  }
}
```

### 3.5 适用场景

| 适用场景 | 说明 |
|---------|------|
| ✅ **开发调试** | 需要频繁修改 Dockerfile 测试新配置 |
| ✅ **离线环境** | 首次构建后可离线使用（有缓存） |
| ✅ **自定义构建** | 需要完全控制构建过程 |
| ❌ **快速启动** | 不适合需要快速启动的场景 |
| ❌ **多容器协作** | 不适合需要多个容器的场景 |

## 4. Docker Compose 方式

### 4.1 方式特点

Docker Compose 方式的特点：

- ✅ **启动速度快**：< 1 分钟（使用本地预构建镜像）
- ✅ **服务编排灵活**：可以轻松添加多个服务
- ✅ **配置集中**：所有配置在 `docker-compose.yml` 中
- ⚠️ **需要预构建**：首次使用需要构建镜像（一次性）
- ✅ **版本锁定**：可以使用特定版本的镜像

### 4.2 使用步骤

#### 步骤 1：构建镜像（仅需执行一次）

使用提供的构建脚本构建镜像：

```bash
cd .devcontainer/docker

# 查看构建脚本帮助
./scripts/build --help 2>/dev/null || cat scripts/build | head -20

# 执行构建（使用默认配置）
./scripts/build

# 或指定 Claude Code 版本构建
CLAUDE_CODE_VERSION=2.x ./scripts/build
```

**构建脚本说明**：

| 环境变量 | 说明 | 默认值 | 示例 |
|---------|------|--------|------|
| `CLAUDE_CODE_VERSION` | Claude Code 版本 | `1.x` | `1.x`、`2.x` |
| `UBUNTU_VERSION` | Ubuntu 版本 | `ubuntu24.04` | `ubuntu24.04`、`ubuntu22.04` |
| `IMAGE_REPO` | 镜像仓库地址 | `fsyyft/devcontainer/ubuntu/go` | `myrepo/custom-image` |

**构建产物**：

- **版本标签**：`fsyyft/devcontainer/ubuntu/go:ubuntu24.04.YYMMDDNN`
- **latest 标签**：`fsyyft/devcontainer/ubuntu/go:latest`

#### 步骤 2：复制配置文件

将示例配置文件复制到 `.devcontainer/` 目录：

```bash
cd .devcontainer
cp example-compose/devcontainer.json devcontainer.json
cp example-compose/docker-compose.yml docker-compose.yml
```

#### 步骤 3：配置环境变量（可选）

创建或编辑项目根目录的 `.env` 文件：

```bash
# .env 文件示例
# 镜像配置
IMAGE_REPO=fsyyft/devcontainer/ubuntu/go
IMAGE_TAG=latest

# 容器配置
CONTAINER_NAME=kratos-layout-dev
HOSTNAME=kratos-dev

# Claude Code 配置
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=glm-4.7
```

#### 步骤 4：启动 DevContainer

1. 使用 VS Code 打开项目：`code .`
2. 在弹出的提示中选择 **"在 DevContainer 中重新打开"**
3. 等待容器启动（< 1 分钟）

### 4.3 镜像版本说明

#### 版本标签格式

镜像标签采用以下格式：

```
{IMAGE_REPO}:{UBUNTU_VERSION}.{YYMMDD}{NN}
```

示例：
- `fsyyft/devcontainer/ubuntu/go:ubuntu24.04.26011101`（2026年1月11日第1次构建）
- `fsyyft/devcontainer/ubuntu/go:ubuntu24.04.26011102`（2026年1月11日第2次构建）
- `fsyyft/devcontainer/ubuntu/go:latest`（最新版本）

#### 镜像版本选择

| 使用场景 | 推荐标签 | 说明 |
|---------|---------|------|
| **日常开发** | `latest` | 始终使用最新版本，包含最新工具和安全更新 |
| **版本锁定** | `ubuntu24.04.26011101` | 使用特定版本，避免环境变化 |
| **团队协作** | 固定版本标签 | 确保所有团队成员使用相同版本 |

#### 更新镜像

当需要更新到最新版本时：

```bash
# 重新构建本地镜像
cd .devcontainer/docker
./scripts/build

# 构建脚本会自动：
# 1. 生成新的版本标签（如 ubuntu24.04.26011102）
# 2. 更新 latest 标签
# 3. 显示新镜像的信息
```

**注意**：
- 本项目使用本地构建的镜像，未推送到远程仓库
- 如需在多台机器间共享镜像，可以手动导出/导入镜像
- 或配置镜像仓库并推送镜像（需要用户自行实现）

### 4.4 配置文件说明

Docker Compose 方式使用的配置文件：

| 文件 | 位置 | 说明 |
|------|------|------|
| `devcontainer.json` | `.devcontainer/devcontainer.json` | DevContainer 主配置文件 |
| `docker-compose.yml` | `.devcontainer/docker-compose.yml` | Docker Compose 配置文件 |

**重要配置项**：

```yaml
# docker-compose.yml
services:
  app:
    image: ${IMAGE_REPO:-fsyyft/devcontainer/ubuntu/go}:${IMAGE_TAG:-latest}
    container_name: ${CONTAINER_NAME:-kratos-layout-dev}
    hostname: ${HOSTNAME:-kratos-dev}
```

```json
// devcontainer.json
{
  "name": "Kratos Layout Dev Container With Docker Compose",
  "dockerComposeFile": "docker-compose.yml",  // Docker Compose 文件路径
  "service": "app",                           // 使用的服务名称
  "workspaceFolder": "/development/github.com/fsyyft-go/kratos-layout"
}
```

### 4.5 适用场景

| 适用场景 | 说明 |
|---------|------|
| ✅ **快速启动** | 需要快速启动开发环境 |
| ✅ **多容器协作** | 需要数据库、Redis 等多个服务 |
| ✅ **团队协作** | 团队成员需要统一环境 |
| ✅ **版本管理** | 需要锁定特定版本的环境 |
| ❌ **频繁修改配置** | 不适合需要频繁修改 Dockerfile 的场景 |

## 5. 配置文件使用说明

### 5.1 为什么不直接使用 example- 配置

#### VSCode 识别限制

**重要**：VS Code DevContainer 功能**只能识别两层目录结构**的配置文件：

```
✅ 可识别：
.devcontainer/
  └── devcontainer.json

❌ 不可识别：
.devcontainer/
  └── example-compose/
      └── devcontainer.json
```

**三层目录结构问题**：

VS Code 只会在项目根目录的 `.devcontainer/` 目录中查找 `devcontainer.json` 文件，**不会递归搜索子目录**。因此，将配置文件放在 `example-compose/` 或 `example-dockerfile/` 子目录中，VS Code **无法自动识别**。

**设计说明**：

`example-` 前缀的目录设计为**示例配置**，目的是：
- ✅ 提供多种配置方式供参考
- ✅ 避免直接修改主配置文件
- ✅ 用户可以根据需求复制和自定义

### 5.2 如何复制和修改配置文件

#### 方式 1：使用 Dockerfile 配置

```bash
# 步骤 1：复制配置文件
cd .devcontainer
cp example-dockerfile/devcontainer.json devcontainer.json

# 步骤 2：修改路径配置（必须）
# 根据下一节的说明修改 dockerFile 和 build.context 路径
```

**注意事项**：
- ⚠️ **必须修改**：`dockerFile` 和 `build.context` 路径
- ⚠️ **确保存在**：`.env` 文件（如果使用环境变量）
- ✅ **可选**：修改 `containerEnv` 中的环境变量配置

#### 方式 2：使用 Docker Compose 配置

```bash
# 步骤 1：复制配置文件
cd .devcontainer
cp example-compose/devcontainer.json devcontainer.json
cp example-compose/docker-compose.yml docker-compose.yml

# 步骤 2：检查配置
# 根据下一节的说明检查路径配置
```

**注意事项**：
- ✅ **路径配置**：大部分路径保持不变（使用相对路径）
- ⚠️ **确保存在**：`.env` 文件在项目根目录（如果使用环境变量）
- ⚠️ **确保存在**：数据目录（运行 `make devcontainer-init` 创建）
- ✅ **可选**：修改环境变量或镜像版本

### 5.3 配置文件移动后的路径修改清单

#### Dockerfile 方式修改清单

将 `example-dockerfile/devcontainer.json` 复制到 `.devcontainer/devcontainer.json` 后，需要修改以下路径配置：

| 配置项 | 原路径（example-dockerfile/） | 新路径（.devcontainer/） | 说明 |
|--------|-------------------------------|-------------------------|------|
| `dockerFile` | `"../docker/Dockerfile"` | `"docker/Dockerfile"` | Dockerfile 相对路径 |
| `build.context` | `"../docker/"` | `"docker/"` | 构建上下文路径 |

**修改示例**：

```json
// 原配置（example-dockerfile/devcontainer.json）
{
  "dockerFile": "../docker/Dockerfile",
  "build": {
    "context": "../docker/"
  }
}

// 修改后（.devcontainer/devcontainer.json）
{
  "dockerFile": "docker/Dockerfile",
  "build": {
    "context": "docker/"
  }
}
```

#### Docker Compose 方式修改清单

将 `example-compose/` 中的文件复制到 `.devcontainer/` 后，**大部分路径保持不变**：

| 配置项 | 原路径 | 新路径 | 是否需要修改 | 说明 |
|--------|--------|--------|-------------|------|
| `dockerComposeFile` | `"docker-compose.yml"` | `"docker-compose.yml"` | ❌ 不变 | 同级目录 |
| `service` | `"app"` | `"app"` | ❌ 不变 | 服务名 |
| `env_file` | `"../.env"` | `"../.env"` | ❌ 不变 | 相对路径相同 |
| 卷挂载路径 | `"../../data/*"` | `"../../data/*"` | ❌ 不变 | 相对路径相同 |

**说明**：
- Docker Compose 中的路径使用相对路径，无论配置文件在哪个目录，指向的都是相同的目标
- `../.env`：从 `example-compose/` 或 `.devcontainer/` 到项目根目录的 `.env` 文件，路径都是 `../.env`
- `../../data/*`：从 `example-compose/` 或 `.devcontainer/` 到 `.devcontainer/data/` 目录，路径都是 `../../data/*`

**需要确保的前置条件**：
- ✅ `.env` 文件存在于项目根目录（或创建一个）
- ✅ 数据目录已创建（运行 `make devcontainer-init`）

**无需修改示例**：

```yaml
# example-compose/docker-compose.yml 和 .devcontainer/docker-compose.yml 配置相同
volumes:
  - ../../data/.venv:/development/github.com/fsyyft-go/kratos-layout/.venv
  - ../../data:/data
  - ../../data/go/cache:/usr/local/go/cache
  - ../../data/go/path:/usr/local/go/path
```

## 6. 环境变量配置

### 6.1 完整 .env 文件示例

在项目根目录创建 `.env` 文件（或使用现有的 `.devcontainer/docker/.env`）：

```bash
# ========================================
# Claude Code API 配置（必须配置）
# ========================================
# Anthropic API 密钥（必须配置）
# 获取方式：https://console.anthropic.com/settings/keys
ANTHROPIC_API_KEY=your_api_key_here

# ========================================
# Claude Code API 配置（可选）
# ========================================
# Anthropic API 基础 URL（默认：智谱 AI）
# 可选值：https://api.anthropic.com（官方）
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic

# Anthropic 主要模型（用于复杂任务）
# 可选值：claude-sonnet-4-5-20250929、glm-4.7 等
ANTHROPIC_MODEL=glm-4.7

# Anthropic 快速模型（用于简单任务）
# 可选值：claude-haiku-4-20250521、glm-4.7 等
ANTHROPIC_SMALL_FAST_MODEL=glm-4.7

# Anthropic 认证令牌（可选，用于 Claude Code CLI 认证）
# ANTHROPIC_AUTH_TOKEN=your_auth_token_here

# ========================================
# 时区和语言配置（可选）
# ========================================
# 时区设置
# TZ=Asia/Shanghai

# 语言设置
# LANG=zh_CN.UTF-8
# LC_ALL=zh_CN.UTF-8

# ========================================
# Docker Compose 镜像配置（可选）
# ========================================
# 镜像仓库地址
# IMAGE_REPO=fsyyft/devcontainer/ubuntu/go

# 镜像版本标签
# IMAGE_TAG=latest

# 容器名称
# CONTAINER_NAME=kratos-layout-dev

# 容器主机名
# HOSTNAME=kratos-dev

# Docker Compose 项目名称
# COMPOSE_PROJECT_NAME=kratos-layout-dev

# ========================================
# 构建相关配置（可选）
# ========================================
# Claude Code 版本（1.x 或 2.x）
# CLAUDE_CODE_VERSION=1.x

# Ubuntu 版本（ubuntu24.04 或 ubuntu22.04）
# UBUNTU_VERSION=ubuntu24.04
```

### 6.2 必须配置的环境变量

| 变量名 | 说明 | 获取方式 | 示例值 | 是否必须 |
|--------|------|----------|--------|---------|
| `ANTHROPIC_API_KEY` | Claude Code API 密钥 | 从 [Anthropic Console](https://console.anthropic.com/settings/keys) 或智谱 AI 获取 | `sk-ant-xxx` | ✅ **必须** |

#### 如何获取 API Key

##### 方式 1：使用 Anthropic 官方 API

1. 访问 [Anthropic Console](https://console.anthropic.com/settings/keys)
2. 登录或注册账号
3. 在 "API Keys" 页面点击 "Create Key"
4. 复制生成的 API Key

**配置示例**：
```bash
ANTHROPIC_API_KEY=sk-ant-api123-xxx
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
```

##### 方式 2：使用智谱 AI API（国内推荐）

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 登录或注册账号
3. 在 "API 密钥" 页面创建密钥
4. 复制生成的 API Key

**配置示例**：
```bash
ANTHROPIC_API_KEY=your_zhipu_api_key
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=glm-4.7
```

### 6.3 可选的环境变量

#### Claude Code 相关

| 变量名 | 说明 | 默认值 | 示例值 |
|--------|------|--------|--------|
| `ANTHROPIC_BASE_URL` | API 基础 URL | `https://open.bigmodel.cn/api/anthropic` | `https://api.anthropic.com` |
| `ANTHROPIC_MODEL` | 主要模型（复杂任务） | `glm-4.7` | `claude-sonnet-4-5-20250929` |
| `ANTHROPIC_SMALL_FAST_MODEL` | 快速模型（简单任务） | `glm-4.7` | `claude-haiku-4-20250521` |
| `ANTHROPIC_AUTH_TOKEN` | 认证令牌 | - | `your_token_here` |
| `ANTHROPIC_LOG` | 日志级别（调试用） | - | `debug`、`info`、`warn`、`error` |

**模型选择建议**：

| 使用场景 | 推荐模型 | 说明 |
|---------|---------|------|
| **国内用户** | `glm-4.7` | 智谱 AI 模型，访问速度快 |
| **国际用户** | `claude-sonnet-4-5-20250929` | Anthropic 官方模型，功能强大 |
| **快速任务** | `claude-haiku-4-20250521` | 响应速度快，适合简单任务 |

#### 时区和语言

| 变量名 | 说明 | 默认值 | 可选值 |
|--------|------|--------|--------|
| `TZ` | 时区 | `Asia/Shanghai` | `Asia/Hong_Kong`、`UTC` 等 |
| `LANG` | 语言 | `zh_CN.UTF-8` | `en_US.UTF-8` 等 |
| `LC_ALL` | 本地化 | `zh_CN.UTF-8` | `en_US.UTF-8` 等 |

#### Docker Compose 相关

| 变量名 | 说明 | 默认值 | 示例值 |
|--------|------|--------|--------|
| `IMAGE_REPO` | 镜像仓库地址 | `fsyyft/devcontainer/ubuntu/go` | `myrepo/custom-image` |
| `IMAGE_TAG` | 镜像版本标签 | `latest` | `ubuntu24.04.26011101` |
| `CONTAINER_NAME` | 容器名称 | `kratos-layout-dev` | `my-dev-container` |
| `HOSTNAME` | 容器主机名 | `kratos-dev` | `my-kratos-dev` |
| `COMPOSE_PROJECT_NAME` | Docker Compose 项目名称 | `kratos-layout-dev` | `my-project` |

#### 构建相关

| 变量名 | 说明 | 默认值 | 可选值 |
|--------|------|--------|--------|
| `CLAUDE_CODE_VERSION` | Claude Code 版本 | `1.x` | `1.x`、`2.x` |
| `UBUNTU_VERSION` | Ubuntu 版本 | `ubuntu24.04` | `ubuntu24.04`、`ubuntu22.04` |

**Claude Code 版本说明**：

| 版本 | 说明 | 推荐场景 |
|------|------|---------|
| `1.x` | 稳定版本，功能完整 | 生产环境、稳定使用 |
| `2.x` | 新版本，可能有新功能 | 开发测试、体验新功能 |

## 7. 验证和测试

### 7.1 检查容器状态

容器启动后，可以使用以下命令检查状态：

```bash
# 在容器内的终端执行

# 检查容器是否正常运行
uname -a
# 输出示例：Linux kratos-dev 6.x.x-x-generic xxx

# 检查用户
whoami
# 输出应为：fsyyft

# 检查工作目录
pwd
# 输出应为：/development/github.com/fsyyft-go/kratos-layout
```

### 7.2 检查环境变量

```bash
# 在容器内的终端执行

# 检查 Claude Code 相关环境变量
echo $ANTHROPIC_API_KEY
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_MODEL

# 检查时区和语言
echo $TZ
echo $LANG

# 检查所有环境变量
env | grep ANTHROPIC
```

**预期输出**：

```bash
$ echo $ANTHROPIC_BASE_URL
https://open.bigmodel.cn/api/anthropic

$ echo $ANTHROPIC_MODEL
glm-4.7

$ echo $TZ
Asia/Shanghai
```

### 7.3 检查开发工具

```bash
# 在容器内的终端执行

# 检查 Go 版本
go version
# 预期输出：go version go1.25.5 linux/amd64

# 检查 Node.js 版本
node --version
# 预期输出：v22.x.x（LTS 版本）

# 检查 Claude Code 版本
claude --version
# 预期输出：Claude Code version 1.0.126 或 2.x.x

# 检查 Kratos 工具
kratos --version
# 预期输出：kratos version v2.x.x

# 检查 Wire 工具
wire --version
# 预期输出：wire version v0.7.0
```

**已安装的主要开发工具**：

| 类别 | 工具 | 说明 |
|------|------|------|
| **Go** | go 1.25.5 | Go 语言环境 |
| **Node.js** | Node.js LTS | JavaScript 运行时 |
| **Kratos** | kratos v2 | Go 微服务框架 |
| **Wire** | wire v0.7.0 | 依赖注入代码生成 |
| **Protocol Buffers** | protoc | 接口定义语言编译器 |
| **Claude Code** | 1.x / 2.x | AI 代码助手 |
| **golangci-lint** | v1.64.8 | Go 代码质量检查 |
| **Delve** | dlv v1.26.0 | Go 调试器 |

## 8. 常见问题

### 8.1 VSCode 无法识别配置

**问题**：VS Code 没有弹出 "在 DevContainer 中重新打开" 的提示。

**原因**：
- ❌ 配置文件不在 `.devcontainer/` 目录
- ❌ 配置文件在三层子目录中（如 `.devcontainer/example-compose/devcontainer.json`）
- ❌ 配置文件名不是 `devcontainer.json`

**解决方案**：

```bash
# 检查配置文件位置
ls -la .devcontainer/devcontainer.json

# 如果文件不存在，复制示例配置
cp .devcontainer/example-compose/devcontainer.json .devcontainer/devcontainer.json

# 重新加载 VS Code 窗口
# 在 VS Code 中按 F1 或 Ctrl+Shift+P，输入 "Reload Window"
```

### 8.2 容器启动失败

**问题**：VS Code 提示容器启动失败。

**排查步骤**：

1. **检查 Docker 是否运行**：
   ```bash
   docker ps
   ```

2. **查看容器日志**：
   ```bash
   # 查看最近创建的容器日志
   docker logs $(docker ps -a | grep -E 'kratos|dev' | head -1 | awk '{print $1}')
   ```

3. **检查端口占用**：
   ```bash
   # 检查 8000、8001、9000 端口是否被占用
   lsof -i :8000
   lsof -i :8001
   lsof -i :9000
   ```

4. **检查磁盘空间**：
   ```bash
   df -h
   ```

**常见错误及解决方案**：

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `Cannot connect to the Docker daemon` | Docker 未运行 | 启动 Docker Desktop |
| `port is already allocated` | 端口被占用 | 停止占用端口的进程或修改端口映射 |
| `no space left on device` | 磁盘空间不足 | 清理 Docker 镜像和容器 |
| `network xxx not found` | Docker 网络问题 | 重新创建 Docker 网络 |

### 8.3 构建时间过长

**问题**：Dockerfile 方式首次构建时间过长（超过 30 分钟）。

**优化建议**：

1. **检查网络连接**：
   ```bash
   # 测试下载速度
   curl -o /dev/null https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/dists/
   ```

2. **使用 Docker Compose 方式**（推荐）：
   ```bash
   # 使用本地预构建镜像，启动时间 < 1 分钟
   cd .devcontainer/docker
   ./scripts/build
   ```

3. **配置 Docker 代理**（如果在国内）：
   ```json
   // ~/.docker/daemon.json
   {
     "registry-mirrors": [
       "https://docker.mirrors.ustc.edu.cn",
       "https://hub-mirror.c.163.com"
     ]
   }
   ```

4. **检查构建缓存**：
   ```bash
   # 查看构建缓存
   docker system df

   # 清理缓存（谨慎使用）
   docker builder prune
   ```

### 8.4 环境变量未生效

**问题**：配置的环境变量在容器内无效。

**排查步骤**：

1. **检查 .env 文件位置**：
   ```bash
   # .env 文件应该在项目根目录
   ls -la .env
   ```

2. **检查环境变量语法**：
   ```bash
   # 确保没有多余的空格或引号
   cat .env
   ```

3. **检查容器内环境变量**：
   ```bash
   # 在容器内执行
   env | grep ANTHROPIC
   ```

4. **重启容器**：
   ```bash
   # 在 VS Code 中，按 F1 或 Ctrl+Shift+P
   # 输入 "Dev Containers: Rebuild Container"
   ```

**注意事项**：

- ⚠️ 环境变量修改后需要**重建容器**才能生效
- ⚠️ `.env` 文件中的注释以 `#` 开头
- ⚠️ 环境值不要使用引号（除非值中包含空格）

### 8.5 端口冲突问题

**问题**：容器启动失败，提示端口已被占用。

**解决方案**：

**方案 1：停止占用端口的进程**

```bash
# 查找占用端口的进程
lsof -i :8000
lsof -i :8001
lsof -i :9000

# 停止进程（替换 PID）
kill -9 <PID>
```

**方案 2：修改端口映射**

编辑 `devcontainer.json` 或 `docker-compose.yml`，修改端口映射：

```json
// devcontainer.json
"forwardPorts": [8080, 8081, 9090]  // 修改为其他端口
```

```yaml
# docker-compose.yml
ports:
  - "0:8080"  # Web 服务
  - "0:8081"  # Task 服务
  - "0:9090"  # gRPC 服务
```

**方案 3：使用自动分配端口**（推荐）

Docker Compose 方式默认使用 `"0:22"`、`"0:8000"` 等自动分配模式，Docker 会自动分配可用端口。

## 9. 附录

### 9.1 目录结构说明

```
.devcontainer/
├── README.md                           # 本文档
├── devcontainer.json                    # 主配置文件（Dockerfile 方式）
├── docker/                              # Docker 相关文件
│   ├── Dockerfile                      # 容器镜像构建文件
│   ├── resources/                      # 资源文件
│   │   ├── *.sh                        # 安装脚本
│   │   ├── .vimrc                     # Vim 配置
│   │   └── go.env                     # Go 环境配置
│   └── scripts/                        # 脚本文件
│       └── build                       # 镜像构建脚本
├── example-compose/                    # Docker Compose 示例配置
│   ├── devcontainer.json              # Docker Compose 版配置
│   └── docker-compose.yml             # Docker Compose 文件
├── example-dockerfile/                 # Dockerfile 示例配置
│   └── devcontainer.json              # Dockerfile 版配置
└── data/                               # 数据持久化目录（git忽略）
    ├── .venv/                         # Python 虚拟环境
    ├── go/                            # Go 相关目录
    │   ├── cache/                     # Go 缓存
    │   └── path/                      # Go PATH
    └── data/                          # 通用数据目录
```

### 9.2 端口映射说明

容器内的服务端口映射：

| 服务 | 容器端口 | 主机端口（Dockerfile 方式） | 主机端口（Compose 方式） | 说明 |
|------|----------|---------------------------|------------------------|------|
| SSH | 22 | 自动分配 | 自动分配 | SSH 服务 |
| Web | 8000 | 自动分配 | 自动分配 | HTTP API 服务 |
| Task | 8001 | 自动分配 | 自动分配 | 后台任务服务 |
| gRPC | 9000 | 自动分配 | 自动分配 | gRPC 服务 |

**查看实际分配的端口**：

```bash
# 方式 1：使用 docker port 命令
docker port <container_name>

# 方式 2：使用 docker ps 命令
docker ps | grep kratos

# 方式 3：在 VS Code 的"端口"选项卡中查看
```

### 9.3 卷挂载说明

数据持久化目录挂载：

| 宿主机路径 | 容器路径 | 说明 |
|-----------|----------|------|
| `/var/run/docker.sock` | `/var/run/docker.sock` | Docker Socket（Docker-in-Docker） |
| `${localWorkspaceFolder}` | `/development/github.com/fsyyft-go/kratos-layout` | 项目工作目录 |
| `.devcontainer/data/.venv` | `/development/.../kratos-layout/.venv` | Python 虚拟环境 |
| `.devcontainer/data/data` | `/data` | 通用数据目录 |
| `.devcontainer/data/go/cache` | `/usr/local/go/cache` | Go 缓存目录 |
| `.devcontainer/data/go/path` | `/usr/local/go/path` | Go GOPATH 目录 |

**卷挂载的好处**：

- ✅ **持久化数据**：容器删除后数据不丢失
- ✅ **共享数据**：宿主机和容器可以共享文件
- ✅ **加速构建**：Go 模块缓存、NPM 缓存等可以重用

### 9.4 已安装的开发工具清单

容器中已预安装的开发工具：

#### Go 工具

| 工具 | 版本 | 说明 |
|------|------|------|
| Go | 1.25.5 | Go 语言环境 |
| golangci-lint | v1.64.8 | Go 代码质量检查 |
| staticcheck | v0.6.1 | Go 静态分析 |
| errcheck | v1.9.0 | Go 错误检查 |
| go-critic | v0.14.2 | Go 代码建议 |
| goimports | v0.40.0 | Go 导入排序 |
| gofumpt | v0.9.2 | Go 代码格式化 |
| ginkgo | v2.27.3 | Go 测试框架 |
| gotestsum | v1.13.0 | Go 测试运行器 |
| mockgen | v1.6.0 | Go mock 生成 |
| wire | v0.7.0 | Go 依赖注入 |
| protoc-gen-go | v1.36.11 | Protocol Buffers Go 代码生成 |
| protoc-gen-go-grpc | v1.6.0 | gRPC Go 代码生成 |
| protoc-gen-go-http | latest | Kratos HTTP 代码生成 |
| protoc-gen-go-errors | latest | Kratos 错误代码生成 |
| protoc-gen-validate | v1.3.0 | Protocol Buffers 验证 |
| protoc-gen-openapi | v0.7.1 | OpenAPI 文档生成 |
| kratos | v2 | Kratos 框架工具 |
| dlv | v1.26.0 | Go 调试器 |
| pprof | latest | Go 性能分析 |
| govvulcheck | v1.1.4 | Go 漏洞扫描 |
| gosec | v2.22.11 | Go 安全扫描 |
| swag | v1.16.6 | Swagger 文档生成 |
| oapi-codegen | latest | OpenAPI 代码生成 |
| cobra-cli | v1.3.0 | CLI 开发工具 |
| goose | v3.26.0 | 数据库迁移工具 |

#### Node.js 工具

| 工具 | 版本 | 说明 |
|------|------|------|
| Node.js | LTS | JavaScript 运行时 |
| npm | 最新 | Node.js 包管理器 |
| @google/gemini-cli | latest | Gemini AI 工具 |
| @qwen-code/qwen-code | latest | 通义千问代码助手 |
| @anthropic-ai/claude-code | 1.x / 2.x | Claude Code CLI |
| opencode | latest | OpenCode 工具 |

#### 系统工具

| 工具 | 说明 |
|------|------|
| git | 版本控制 |
| vim | 文本编辑器 |
| zsh + Oh My Zsh | 增强型 Shell |
| tmux | 终端复用器 |
| make | 构建工具 |
| curl、wget | 网络下载工具 |
| nmap、tcpdump | 网络调试工具 |
| openssh-server | SSH 服务器 |

## 相关资源

- [VS Code DevContainer 官方文档](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 官方文档](https://docs.docker.com/compose/)
- [Go Kratos 框架文档](https://go-kratos.dev/)
- [项目 CLAUDE.md](../CLAUDE.md) - 项目开发指南
