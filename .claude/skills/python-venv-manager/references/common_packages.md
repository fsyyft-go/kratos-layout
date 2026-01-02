# 常用 Python 包清单

## 开发工具

### 代码质量

- **black** - Python 代码格式化工具
  ```bash
  pip install black
  ```

- **isort** - import 语句排序工具
  ```bash
  pip install isort
  ```

- **flake8** - 代码风格检查
  ```bash
  pip install flake8
  ```

- **pylint** - 代码质量分析
  ```bash
  pip install pylint
  ```

- **mypy** - 静态类型检查
  ```bash
  pip install mypy
  ```

### 测试工具

- **pytest** - 测试框架
  ```bash
  pip install pytest
  ```

- **pytest-cov** - pytest 的覆盖率插件
  ```bash
  pip install pytest-cov
  ```

- **unittest-xml-reporting** - XML 测试报告
  ```bash
  pip install unittest-xml-reporting
  ```

- **tox** - 多环境测试工具
  ```bash
  pip install tox
  ```

## Web 框架

### 全栈框架

- **Django** - 全功能 Web 框架
  ```bash
  pip install django
  ```

- **Flask** - 轻量级 Web 框架
  ```bash
  pip install flask
  ```

- **FastAPI** - 现代、快速的 Web 框架
  ```bash
  pip install fastapi uvicorn
  ```

### 异步框架

- **aiohttp** - 异步 HTTP 客户端/服务器
  ```bash
  pip install aiohttp
  ```

- **tornado** - 异步 Web 框架
  ```bash
  pip install tornado
  ```

## 数据科学

### 核心库

- **numpy** - 数值计算库
  ```bash
  pip install numpy
  ```

- **pandas** - 数据分析库
  ```bash
  pip install pandas
  ```

- **scipy** - 科学计算库
  ```bash
  pip install scipy
  ```

### 可视化

- **matplotlib** - 绘图库
  ```bash
  pip install matplotlib
  ```

- **seaborn** - 统计可视化
  ```bash
  pip install seaborn
  ```

- **plotly** - 交互式可视化
  ```bash
  pip install plotly
  ```

### 机器学习

- **scikit-learn** - 机器学习库
  ```bash
  pip install scikit-learn
  ```

- **tensorflow** - 深度学习框架
  ```bash
  pip install tensorflow
  ```

- **torch** - PyTorch 深度学习框架
  ```bash
  pip install torch
  ```

## 数据处理

### 数据格式

- **pyyaml** - YAML 解析器
  ```bash
  pip install pyyaml
  ```

  **注意**：import 时使用 `import yaml`

- **toml** - TOML 解析器
  ```bash
  pip install toml
  ```

- **tomli** - 快速 TOML 解析器（Python 3.11+ 内置）
  ```bash
  pip install tomli
  ```

### 数据库

- **SQLAlchemy** - SQL 工具包和 ORM
  ```bash
  pip install sqlalchemy
  ```

- **psycopg2-binary** - PostgreSQL 适配器
  ```bash
  pip install psycopg2-binary
  ```

- **pymongo** - MongoDB 驱动
  ```bash
  pip install pymongo
  ```

- **redis** - Redis 客户端
  ```bash
  pip install redis
  ```

## 网络

### HTTP 客户端

- **requests** - 人性化 HTTP 库
  ```bash
  pip install requests
  ```

- **httpx** - 现代 HTTP 客户端（支持异步）
  ```bash
  pip install httpx
  ```

- **urllib3** - HTTP 客户端（requests 的依赖）
  ```bash
  pip install urllib3
  ```

### 网页爬虫

- **beautifulsoup4** - HTML/XML 解析库
  ```bash
  pip install beautifulsoup4
  ```

  **注意**：import 时使用 `from bs4 import BeautifulSoup`

- **lxml** - 高性能 XML/HTML 处理
  ```bash
  pip install lxml
  ```

- **scrapy** - 爬虫框架
  ```bash
  pip install scrapy
  ```

## 图像处理

- **Pillow** - 图像处理库
  ```bash
  pip install pillow
  ```

  **注意**：import 时使用 `from PIL import Image`

- **opencv-python** - 计算机视觉库
  ```bash
  pip install opencv-python
  ```

  **注意**：import 时使用 `import cv2`

## 命令行工具

- **click** - 命令行界面创建工具
  ```bash
  pip install click
  ```

- **typer** - 现代 CLI 工具（基于类型提示）
  ```bash
  pip install typer
  ```

- **argparse** - 命令行解析（标准库，无需安装）
  ```python
  import argparse
  ```

## 任务调度

- **celery** - 分布式任务队列
  ```bash
  pip install celery
  ```

- **APScheduler** - 轻量级任务调度
  ```bash
  pip install apscheduler
  ```

- **schedule** - 简单的任务调度
  ```bash
  pip install schedule
  ```

## 配置管理

- **python-dotenv** - 从 .env 文件读取配置
  ```bash
  pip install python-dotenv
  ```

- **pydantic** - 数据验证和设置管理
  ```bash
  pip install pydantic
  ```

## 日志

- **loguru** - 简化的日志库
  ```bash
  pip install loguru
  ```

- **structlog** - 结构化日志
  ```bash
  pip install structlog
  ```

## 监控和性能

- **prometheus-client** - Prometheus 监控
  ```bash
  pip install prometheus-client
  ```

- **pyperformance** - Python 性能基准测试
  ```bash
  pip install pyperformance
  ```

## 安全

- **cryptography** - 加密库
  ```bash
  pip install cryptography
  ```

- **pyjwt** - JWT 令牌处理
  ```bash
  pip install pyjwt
  ```

- **passlib** - 密码哈希
  ```bash
  pip install passlib
  ```

## 工具脚本

### 文件操作

- **watchdog** - 文件系统事件监控
  ```bash
  pip install watchdog
  ```

- **pathlib** - 面向对象文件系统路径（标准库）
  ```python
  from pathlib import Path
  ```

### 进度条

- **tqdm** - 进度条
  ```bash
  pip install tqdm
  ```

- **rich** - 丰富的终端输出
  ```bash
  pip install rich
  ```

## 包别名映射表

| import 名称 | PyPI 包名 | 说明 |
|-----------|----------|------|
| `yaml` | `pyyaml` | YAML 处理 |
| `bs4` | `beautifulsoup4` | HTML 解析 |
| `PIL` | `pillow` | 图像处理 |
| `cv2` | `opencv-python` | 计算机视觉 |
| `sklearn` | `scikit-learn` | 机器学习 |
| `tf` | `tensorflow` | 深度学习 |

## 版本建议

### 稳定版本（生产环境）

```txt
numpy>=1.20.0,<2.0.0
pandas>=2.0.0,<3.0.0
requests>=2.28.0,<3.0.0
```

### 最新版本（开发环境）

```txt
numpy
pandas
requests
```

## 相关资源

- [PyPI - Python Package Index](https://pypi.org/)
- [Awesome Python](https://awesome-python.com/)
- [Python Package Index (PyPI)](https://pypi.org/)
