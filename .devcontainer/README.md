# Kratos Layout 开发容器

## 快速开始

### 首次使用前初始化

在启动 DevContainer 之前，需要先运行以下命令来初始化必要的目录结构和 Python 虚拟环境：

```bash
make devcontainer-init
```

该命令会自动创建以下目录和文件：
- `.devcontainer/data/.venv` - Python 虚拟环境（**重要**：需要在容器启动后，在容器内运行 `python -m venv .venv` 进行初始化）
- `.devcontainer/data/go/cache` - Go 缓存目录（挂载到容器内的 `/usr/local/go/cache`）
- `.devcontainer/data/go/path` - Go PATH 目录（挂载到容器内的 `/usr/local/go/path`）
- `.devcontainer/data/data` - 通用数据目录（挂载到容器内的 `/data`）

所有这些目录都已在 `.gitignore` 中配置，不会被提交到 Git。

### 启动 DevContainer

初始化完成后，使用 VS Code 的命令打开项目：

```bash
code .
```

然后选择 "在 DevContainer 中重新打开" 即可。

## TODO

- [x] 在容器内运行 `make init` 卡死，未找到原因
- [x] 添加 DevContainer 初始化命令
- [ ] 使用 Docker Compose
