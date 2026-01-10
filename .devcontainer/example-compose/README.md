# Docker Compose 版 DevContainer 配置

## 概述

此目录包含使用 Docker Compose 的 DevContainer 配置文件，提供了更灵活的服务编排能力。

**重要特性**：使用预构建镜像 `fsyyft/devcontainer/ubuntu/go:latest`，无需现场构建，启动速度更快。

与直接使用 Dockerfile 相比，Docker Compose 方式的优势：

1. **更快的启动速度**：使用预构建镜像，无需等待构建过程
2. **更灵活的服务编排**：可以轻松添加多个服务（如数据库、Redis 等）
3. **更好的配置管理**：所有服务配置集中在一个文件中
4. **更方便的网络配置**：自动创建和管理容器网络
5. **更强大的扩展性**：支持服务依赖、健康检查等高级特性

## 文件说明

- [`docker-compose.yml`](docker-compose.yml) - Docker Compose 配置文件，定义容器服务
- [`devcontainer.json`](devcontainer.json) - VS Code DevContainer 配置文件

## 使用方法

### 方法一：替换现有配置

1. 将 [`devcontainer.json`](devcontainer.json) 复制到项目根目录的 `.devcontainer/` 目录：

```bash
cp .devcontainer/example-compose/devcontainer.json .devcontainer/devcontainer.json
```

2. 将 [`docker-compose.yml`](docker-compose.yml) 也复制到 `.devcontainer/` 目录：

```bash
cp .devcontainer/example-compose/docker-compose.yml .devcontainer/docker-compose.yml
```

3. 使用 VS Code 打开项目：

```bash
code .
```

4. 在弹出的提示中选择 "在 DevContainer 中重新打开"

### 方法二：创建新的 DevContainer 配置

如果想保留现有配置，可以创建多个 DevContainer 配置：

1. 在 `.devcontainer/` 目录下创建子目录，例如 `compose-dev`：

```bash
mkdir -p .devcontainer/compose-dev
```

2. 将配置文件复制到该目录：

```bash
cp .devcontainer/example-compose/devcontainer.json .devcontainer/compose-dev/
cp .devcontainer/example-compose/docker-compose.yml .devcontainer/compose-dev/
```

3. 使用 VS Code 打开项目时，可以选择使用哪个 DevContainer 配置

## 配置说明

### 镜像配置

默认使用预构建镜像 `fsyyft/devcontainer/ubuntu/go:latest`，该镜像包含完整的 Go 开发环境。

镜像配置支持通过环境变量灵活设置，优先级从高到低：

1. **命令行环境变量**（最高优先级）
2. **`.env` 文件**
3. **默认值**（在 docker-compose.yml 中定义）

#### 方式一：使用默认镜像

直接启动，使用默认镜像 `fsyyft/devcontainer/ubuntu/go:latest`：

```bash
docker-compose up
```

#### 方式二：使用环境变量（推荐）

通过环境变量指定镜像版本和容器名称：

```bash
# 指定镜像版本
IMAGE_TAG=ubuntu24.04.26011101 docker-compose up

# 指定完整的镜像仓库和版本
IMAGE_REPO=fsyyft/devcontainer/ubuntu/go IMAGE_TAG=ubuntu24.04.26011101 docker-compose up

# 使用自定义镜像仓库
IMAGE_REPO=myrepo/custom-image IMAGE_TAG=v1.0 docker-compose up

# 自定义容器名称
CONTAINER_NAME=my-dev-container docker-compose up

# 自定义容器主机名
HOSTNAME=my-kratos-dev docker-compose up

# 组合使用多个环境变量
IMAGE_REPO=fsyyft/devcontainer/ubuntu/go IMAGE_TAG=ubuntu24.04.26011101 CONTAINER_NAME=kratos-dev-24 HOSTNAME=my-kratos-dev docker-compose up
```

#### 方式三：在 .env 文件中配置

在项目根目录创建 `.env` 文件（或使用现有的 `.devcontainer/docker/.env`）：

```bash
# .env 文件内容
IMAGE_REPO=fsyyft/devcontainer/ubuntu/go
IMAGE_TAG=ubuntu24.04.26011101
CONTAINER_NAME=kratos-dev-24
HOSTNAME=my-kratos-dev
```

然后正常启动：

```bash
docker-compose up
```

#### 可用镜像版本

| 标签格式 | 示例 | 说明 |
|---------|------|------|
| `latest` | `fsyyft/devcontainer/ubuntu/go:latest` | 最新版本（默认） |
| `ubuntu24.04.YYMMDDNN` | `fsyyft/devcontainer/ubuntu/go:ubuntu24.04.26011101` | Ubuntu 24.04 特定构建 |
| `ubuntu22.04.YYMMDDNN` | `fsyyft/devcontainer/ubuntu/go:ubuntu22.04.26011101` | Ubuntu 22.04 特定构建 |

**提示**：
- 使用 `latest` 标签可以确保使用最新的镜像版本，包含最新的工具和安全更新
- 使用特定版本标签（如 `ubuntu24.04.26011101`）可以锁定环境版本，避免因镜像更新导致的环境变化
- 推荐在开发环境使用 `latest`，在生产环境使用固定版本标签

### 环境变量配置

[`docker-compose.yml`](docker-compose.yml) 支持以下环境变量用于自定义容器配置：

| 环境变量 | 说明 | 默认值 | 示例 |
|---------|------|--------|------|
| `IMAGE_REPO` | 镜像仓库地址 | `fsyyft/devcontainer/ubuntu/go` | `myrepo/custom-image` |
| `IMAGE_TAG` | 镜像版本标签 | `latest` | `ubuntu24.04.26011101` |
| `CONTAINER_NAME` | 容器名称 | `kratos-layout-dev` | `my-dev-container` |
| `HOSTNAME` | 容器主机名 | `kratos-dev` | `my-kratos-dev` |

[`docker-compose.yml`](docker-compose.yml) 中还定义了以下容器内环境变量（用于运行时配置）：

#### 时区和语言

```yaml
TZ: Asia/Shanghai
LANG: zh_CN.UTF-8
LC_ALL: zh_CN.UTF-8
```

#### Claude Code 配置

```yaml
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1"
ANTHROPIC_BASE_URL: ${ANTHROPIC_BASE_URL}
ANTHROPIC_MODEL: ${ANTHROPIC_MODEL}
ANTHROPIC_SMALL_FAST_MODEL: ${ANTHROPIC_SMALL_FAST_MODEL}
ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
ANTHROPIC_AUTH_TOKEN: ${ANTHROPIC_AUTH_TOKEN}
```

这些变量会从宿主机的环境变量中读取。请确保在宿主机上设置了这些变量。

### 端口映射

端口映射配置采用自动分配模式，Docker 会自动分配可用的宿主机端口。

| 服务 | 容器端口 | 主机端口 | 说明 |
|------|----------|----------|------|
| SSH | 22 | 自动分配 | SSH 服务 |
| Web | 8000 | 自动分配 | HTTP API 服务 |
| Task | 8001 | 自动分配 | 后台任务服务 |
| gRPC | 9000 | 自动分配 | gRPC 服务 |

**查看实际分配的端口**：

容器启动后，使用以下命令查看 Docker 实际分配的宿主机端口：

```bash
# 查看所有端口映射
docker port kratos-layout-dev

# 查看特定服务端口
docker port kratos-layout-dev 22    # SSH
docker port kratos-layout-dev 8000  # Web
docker port kratos-layout-dev 8001  # Task
docker port kratos-layout-dev 9000  # gRPC
```

**固定端口映射（可选）**：

如果需要使用固定的端口映射，编辑 [`docker-compose.yml`](docker-compose.yml:117) 中的 `ports` 配置：

```yaml
ports:
  - "44422:22"    # SSH
  - "8000:8000"   # Web
  - "8001:8001"   # Task
  - "9000:9000"   # gRPC
```

**注意**：使用自动分配端口可以避免端口冲突，特别适合同时运行多个容器实例。

### 卷挂载

默认卷挂载：

| 宿主机路径 | 容器路径 | 说明 |
|-----------|----------|------|
| `/var/run/docker.sock` | `/var/run/docker.sock` | Docker Socket（Docker-in-Docker） |
| `../../` | `/development/github.com/fsyyft-go/kratos-layout` | 项目工作目录 |
| `../../data/.venv` | `/development/.../kratos-layout/.venv` | Python 虚拟环境 |
| `../../data` | `/data` | 通用数据目录 |
| `../../data/go/cache` | `/usr/local/go/cache` | Go 缓存目录 |
| `../../data/go/path` | `/usr/local/go/path` | Go GOPATH 目录 |

## 首次使用前初始化

在启动 DevContainer 之前，需要先运行以下命令来初始化必要的目录结构：

```bash
make devcontainer-init
```

该命令会自动创建以下目录：

- `.devcontainer/data/.venv` - Python 虚拟环境目录
- `.devcontainer/data/go/cache` - Go 缓存目录
- `.devcontainer/data/go/path` - Go PATH 目录
- `.devcontainer/data/data` - 通用数据目录

所有这些目录都已在 [`.gitignore`](../../.gitignore) 中配置，不会被提交到 Git。

## 在容器内初始化 Python 虚拟环境

容器启动后，需要在容器内初始化 Python 虚拟环境：

```bash
# 在容器内执行
cd /development/github.com/fsyyft-go/kratos-layout
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # 如果有 requirements.txt
```

## 添加其他服务

如果需要添加其他服务（如数据库、Redis 等），可以在 [`docker-compose.yml`](docker-compose.yml) 中添加新的服务定义。

### 示例：添加 PostgreSQL 数据库

```yaml
services:
  app:
    # ... 现有配置 ...

  # 添加 PostgreSQL 服务
  postgres:
    image: postgres:16-alpine
    container_name: kratos-postgres
    environment:
      POSTGRES_USER: fsyyft
      POSTGRES_PASSWORD: password
      POSTGRES_DB: kratos_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - default

volumes:
  postgres-data:
    driver: local
```

## 故障排查

### 容器无法启动

1. 检查 Docker 是否运行：

```bash
docker ps
```

2. 查看容器日志：

```bash
docker logs kratos-layout-dev
```

3. 检查端口占用：

```bash
lsof -i :8000
lsof -i :44422
```

### 环境变量未生效

1. 确认宿主机环境变量已设置：

```bash
echo $ANTHROPIC_API_KEY
```

2. 检查容器内环境变量：

```bash
docker exec kratos-layout-dev env | grep ANTHROPIC
```

### 卷挂载失败

1. 确认目录存在：

```bash
ls -la .devcontainer/data/
```

2. 如目录不存在，运行初始化命令：

```bash
make devcontainer-init
```

## 与 Dockerfile 版本的对比

| 特性 | Dockerfile 版本 | Docker Compose 版本（预构建镜像） |
|------|----------------|----------------------------------|
| 启动速度 | 较慢（需要构建） | **快（直接使用镜像）** |
| 配置复杂度 | 简单 | 中等 |
| 服务编排 | 不支持 | 支持 |
| 扩展性 | 有限 | 强大 |
| 配置管理 | 分散 | 集中 |
| 镜像管理 | 本地构建 | 使用远程镜像 |
| 学习曲线 | 低 | 中等 |
| 适用场景 | 单容器开发 | 多容器协作开发 |

**推荐**：如果已有预构建镜像，优先使用 Docker Compose 版本以获得更快的启动速度。

## 相关文档

- [DevContainer 官方文档](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker Compose 官方文档](https://docs.docker.com/compose/)
- [项目 README](../../README.md)
