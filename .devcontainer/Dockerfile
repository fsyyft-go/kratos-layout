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
COPY resources/install.zsh.sh /usr/bin/install.zsh.sh

# 配置 APT 源为清华大学镜像，加速包下载。
RUN sed -i 's|http://ports.ubuntu.com/ubuntu-ports/|http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/|g' /etc/apt/sources.list.d/ubuntu.sources

# 安装基础工具、网络工具和开发工具。
RUN --mount=type=cache,target=/var/cache/apt,id=apt-cache \
    --mount=type=cache,target=/var/lib/apt/lists,id=apt-lists \
    chmod +x /usr/bin/install.apt.sh && \
    /usr/bin/install.apt.sh && \
    rm -rfv /usr/bin/install.apt.sh && \
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

COPY resources/install.go.sh /usr/bin/install.go.sh

# 执行 Go 工具安装，使用 BuildKit 缓存。
RUN --mount=type=cache,target=/go/pkg/mod,id=go-mod-cache \
    chmod +x /usr/bin/install.go.sh && \
    /usr/bin/install.go.sh && \
    rm -rfv /usr/bin/install.go.sh && \
    du -sh /go/pkg/mod | xargs echo "Go module cache size:"

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

# 设置构建参数：Claude Code 版本选择（默认为 1.x，可选 2.x）。
ARG CLAUDE_CODE_VERSION=1.x

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

# 创建并设置工作目录。
RUN mkdir -p /home/workspace
WORKDIR /home/workspace

# 复制容器入口脚本。
COPY resources/check.mount.sh /usr/bin/check.mount.sh
COPY resources/check.version.sh /usr/bin/check.version.sh
COPY resources/docker-entrypoint.sh /docker-entrypoint.sh

# 设置脚本执行权限。
RUN chmod +x /usr/bin/check.mount.sh /usr/bin/check.version.sh && \
    chmod +x /docker-entrypoint.sh

# 设置容器入口点。
ENTRYPOINT ["/docker-entrypoint.sh"]

# 执行清理操作。
RUN chmod +x /usr/bin/clean.system.sh && \
    /usr/bin/clean.system.sh