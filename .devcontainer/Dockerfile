# Dev Container 专用 Dockerfile

# 使用官方 Go 开发容器镜像作为基础
FROM mcr.microsoft.com/devcontainers/go:1.25

# 设置内部环境变量（系统配置）。
ENV TZ=Asia/Shanghai
ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8
# ENV GOPROXY=https://goproxy.cn,https://mirrors.aliyun.com/goproxy/,direct

COPY resources/.vimrc /home/vscode/.vimrc
COPY resources/go.env /home/vscode/.config/go/env
COPY resources/check.mount.sh /usr/bin/check.mount.sh
COPY resources/check.version.sh /usr/bin/check.version.sh
COPY resources/clean.system.sh /usr/bin/clean.system.sh
COPY resources/install.apt.sh /usr/bin/install.apt.sh
COPY resources/install.go.sh /usr/bin/install.go.sh

RUN chmod +x /usr/bin/check.mount.sh /usr/bin/check.version.sh

# 配置 Bash 别名。
RUN cd /home/vscode && \
    echo 'alias ll="clear;ls -aihl --color=tty --time-style=long-iso"' >> .bashrc && \
    echo '' >> .bashrc && \
    echo 'PATH=/go/bin/:/usr/local/go/bin/:$PATH' >> .bashrc && \
    echo 'alias cp="cp -i"' >> .zshrc && \
    echo 'alias mv="mv -i"' >> .zshrc && \
    echo 'alias ll="clear;ls -aihl --color=tty --time-style=long-iso"' >> .zshrc && \
    echo 'alias rm="/bin/rm -i"' >> .zshrc && \
    echo 'alias sudo="sudo "' >> .zshrc && \
    echo '' >> .zshrc && \
    cd -

# 执行 Go 工具安装，使用 BuildKit 缓存。
RUN --mount=type=cache,target=/go/pkg/mod,id=go-mod-cache \
    chmod +x /usr/bin/install.go.sh && \
    /usr/bin/install.go.sh && \
    rm -rfv /usr/bin/install.go.sh && \
    du -sh /go/pkg/mod | xargs echo "Go module cache size:"

# 配置 APT 源为清华大学镜像，加速包下载。
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources

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

# 创建并设置工作目录。
RUN mkdir -p /workspace
WORKDIR /workspace

# 复制容器入口脚本。
COPY resources/docker-entrypoint.sh /docker-entrypoint.sh

# 设置脚本执行权限。
RUN chmod +x /docker-entrypoint.sh

# 设置外部环境变量（Claude Code 相关）。
ENV ANTHROPIC_BASE_URL=https://q.quuvv.cn
ENV CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# 设置构建参数：Claude Code 版本选择（默认为 1.x，可选 2.x）。
ARG CLAUDE_CODE_VERSION=1.x

# 安装 Node.js LTS 版本。
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && node --version \
    && npm --version \
    && npm config set registry https://registry.npmmirror.com

# 根据构建参数安装 Claude Code 指定版本。
# 1.0.126 版本，可以使用 -p，2.0.14 1.0.128 测试失败。
RUN --mount=type=cache,target=/root/.npm,id=npm-cache \
    echo "Installing Gemini..." && \
    npm install -g @google/gemini-cli && \
    echo "Installing Qwen Code..." && \
    npm install -g @qwen-code/qwen-code && \
    echo "Installing Claude Code..." && \
    if [ "$CLAUDE_CODE_VERSION" = "2.x" ]; then \
        echo "Installing Claude Code 2.x version..." && \
        npm install -g @anthropic-ai/claude-code@^2.0.0; \
    else \
        echo "Installing Claude Code 1.x version..." && \
        npm install -g @anthropic-ai/claude-code@1.0.126; \
    fi && \
    du -sh /root/.npm 2>/dev/null | xargs echo "NPM cache size:"

# 执行清理操作。
RUN chmod +x /usr/bin/clean.system.sh && \
    /usr/bin/clean.system.sh && \
    sudo chown vscode -R /go

USER vscode