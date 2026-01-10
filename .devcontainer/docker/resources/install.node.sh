#!/bin/bash
set -e

CLAUDE_CODE_VERSION="${CLAUDE_CODE_VERSION:-1.x}"

# 安装 Node.js LTS 版本。
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && node --version \
    && npm --version \
    && npm config set registry https://registry.npmmirror.com

# 根据构建参数安装 Claude Code 指定版本。
# 1.0.126 版本，可以使用 -p，2.0.14 1.0.128 测试失败。
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
    fi