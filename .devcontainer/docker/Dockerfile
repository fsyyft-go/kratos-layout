# Ubuntu 版本号，允许通过外部传入：--build-arg UBUNTU_VERSION="$UBUNTU_VERSION" 。
ARG UBUNTU_VERSION=ubuntu24.04
FROM mcr.microsoft.com/devcontainers/base:${UBUNTU_VERSION}

# 设置内部环境变量（系统配置）。
ENV TZ=Asia/Shanghai
ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8

# 避免交互式安装。
ENV DEBIAN_FRONTEND=noninteractive

# 创建用户 fsyyft，并将用户加入到 sudo 组。
RUN useradd -u 327 -g 0 -d /home/fsyyft -s /bin/bash -m fsyyft && \
    usermod -aG sudo fsyyft

COPY resources/.vimrc /root/.vimrc
COPY resources/go.env /root/.config/go/env

COPY resources/.vimrc /home/fsyyft/.vimrc
COPY resources/go.env /home/fsyyft/.config/go/env

# 配置 Bash 别名，为 fsyyft 用户下的文件个性所有者。
RUN echo 'alias ll="clear;ls -aihl --color=tty --time-style=long-iso"' >> /root/.bashrc && \
    echo '' >> /root/.bashrc && \
    echo 'PATH=/go/bin/:/usr/local/go/bin/:$PATH' >> /root/.bashrc  && \
    echo 'alias ll="clear;ls -aihl --color=tty --time-style=long-iso"' >> /home/fsyyft/.bashrc && \
    echo '' >> /home/fsyyft/.bashrc && \
    echo 'PATH=/go/bin/:/usr/local/go/bin/:$PATH' >> /home/fsyyft/.bashrc && \
    chown fsyyft -R /home/fsyyft

COPY resources/clean.system.sh /usr/bin/clean.system.sh
COPY resources/install.apt.sh /usr/bin/install.apt.sh
COPY resources/install.docker.cli.sh /usr/bin/install.docker.cli.sh
COPY resources/install.zsh.sh /usr/bin/install.zsh.sh

# 配置 APT 源为清华大学镜像，加速包下载。
RUN sed -i 's|http://ports.ubuntu.com/ubuntu-ports/|http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/|g' /etc/apt/sources.list.d/ubuntu.sources

# 安装基础工具、网络工具和开发工具。
RUN --mount=type=cache,target=/var/cache/apt,id=apt-cache \
    --mount=type=cache,target=/var/lib/apt/lists,id=apt-lists \
    chmod +x /usr/bin/install.apt.sh && \
    /usr/bin/install.apt.sh && \
    rm -rfv /usr/bin/install.apt.sh && \
    chmod +x /usr/bin/install.docker.cli.sh && \
    /usr/bin/install.docker.cli.sh && \
    rm -rfv /usr/bin/install.docker.cli.sh && \
    du -sh /var/cache/apt /var/lib/apt/lists 2>/dev/null | xargs echo "APT cache sizes:"

# 配置系统语言环境。
RUN echo "Configuring system locale..." && \
    sed -i '/zh_CN.UTF-8/s/^# //' /etc/locale.gen && \
    locale-gen zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 && \
    echo "Locale configuration completed."

# 安装配置 zsh，两个用户都需要配置。
RUN chmod +x /usr/bin/install.zsh.sh && \
    su - fsyyft -c /usr/bin/install.zsh.sh && \
    rm -rfv /usr/bin/install.zsh.sh

# 定义 Go 版本，允许通过外部传入：--build-arg GO_VERSION="$GO_VERSION"，查询最新版本：curl -s https://go.dev/VERSION\?m\=text。
ARG GO_VERSION=1.25
COPY resources/install.go.sh /usr/bin/install.go.sh

# 执行 Go 工具安装，使用 BuildKit 缓存。
RUN --mount=type=cache,target=/go/pkg/mod,id=go-mod-cache \
    chmod +x /usr/bin/install.go.sh && \
    /usr/bin/install.go.sh && \
    rm -rfv /usr/bin/install.go.sh && \
    du -sh /go/pkg/mod | xargs echo "Go module cache size:"

# 添加 Go 版本标签。
LABEL net.ppno.app.go.version="${GO_VERSION}"

# 配置 SSH 服务。
RUN mkdir -p /var/run/sshd \
    && mkdir -p /root/.ssh \
    && ROOT_PASSWORD=$(openssl rand -base64 12) \
    && echo "root:$ROOT_PASSWORD" | chpasswd \
    && echo "$ROOT_PASSWORD" > /root/.ssh/root_password.txt \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config \
    && ssh-keygen -A

# 暴露 SSH 端口。
EXPOSE 22

COPY resources/install.node.sh /usr/bin/install.node.sh

# 设置构建参数：Claude Code 版本（默认为 latest）。
# 可使用具体版本号（如 2.1.0、1.0.126）或 latest。
# 查看最新版本：npm view @anthropic-ai/claude-code versions。
ARG CLAUDE_CODE_VERSION=latest

# 设置构建参数：Gemini CLI 版本（默认为 latest）。
# 可使用具体版本号（如 0.9.0、0.10.0）或 latest。
# 查看最新版本：npm view @google/gemini-cli versions。
ARG GEMINI_VERSION=latest

# 设置构建参数：Qwen Code 版本（默认为 latest）。
# 可使用具体版本号（如 0.0.15、0.1.0）或 latest。
# 查看最新版本：npm view @qwen-code/qwen-code versions。
ARG QWEN_VERSION=latest

# 设置构建参数：OpenAI CodeX 版本（默认为 latest）。
# 可使用具体版本号或 latest。
# 查看最新版本：npm view @openai/codex versions。
ARG CODEX_VERSION=latest

# 设置构建参数：OpenSpec 版本（默认为 latest）。
# 可使用具体版本号或 latest。
# 查看最新版本：npm view @fission-ai/openspec versions。
ARG OPENSPEC_VERSION=latest

# 设置构建参数：Tencent CodeBuddy 版本（默认为 latest）。
# 可使用具体版本号或 latest。
# 查看最新版本：npm view @tencent-ai/codebuddy-code versions。
ARG CODEBUDDY_VERSION=latest

# 设置外部环境变量（Claude Code 相关）。
ENV CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
ENV ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ENV ANTHROPIC_MODEL=glm-4.7
ENV ANTHROPIC_SMALL_FAST_MODEL=glm-4.7

# 安装 Node.js 以及 Cli 工具。
RUN --mount=type=cache,target=/root/.npm,id=npm-cache \
    chmod +x /usr/bin/install.node.sh && \
    /usr/bin/install.node.sh && \
    rm -rfv /usr/bin/install.node.sh && \
    du -sh /root/.npm 2>/dev/null | xargs echo "NPM cache size:"

LABEL net.ppno.app.claude-code.version="${CLAUDE_CODE_VERSION}"
LABEL net.ppno.app.gemini.version="${GEMINI_VERSION}"
LABEL net.ppno.app.qwen.version="${QWEN_VERSION}"
LABEL net.ppno.app.codex.version="${CODEX_VERSION}"
LABEL net.ppno.app.openspec.version="${OPENSPEC_VERSION}"
LABEL net.ppno.app.codebuddy.version="${CODEBUDDY_VERSION}"

# 安装 OpenCode 工具。
RUN curl -fsSL https://opencode.ai/install | bash && \
    mv /root/.opencode/bin/opencode /usr/local/bin

# 创建并设置工作目录。
RUN mkdir -p /home/workspace
WORKDIR /home/workspace

# 复制容器入口脚本。
COPY resources/check.mount.sh /usr/bin/check.mount.sh
COPY resources/check.version.sh /usr/bin/check.version.sh
COPY resources/docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

# 设置脚本执行权限。
RUN chmod +x /usr/bin/check.mount.sh /usr/bin/check.version.sh && \
    chmod +x /usr/bin/docker-entrypoint.sh

# 设置容器入口点。
ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]

# 执行清理操作。
RUN chmod +x /usr/bin/clean.system.sh && \
    /usr/bin/clean.system.sh