#!/bin/bash
set -e

# 安装 Node.js LTS 版本。
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && node --version \
    && npm --version \
    && npm config set registry https://registry.npmmirror.com

# 设置 Claude Code 版本（默认为 latest）。
CLAUDE_CODE_VERSION="${CLAUDE_CODE_VERSION:-latest}"

# 设置 Gemini CLI 版本（默认为 latest）。
GEMINI_VERSION="${GEMINI_VERSION:-latest}"

# 设置 Qwen Code 版本（默认为 latest）。
QWEN_VERSION="${QWEN_VERSION:-latest}"

# 设置 OpenAI CodeX 版本（默认为 latest）。
CODEX_VERSION="${CODEX_VERSION:-latest}"

# 设置 OpenSpec 版本（默认为 latest）。
OPENSPEC_VERSION="${OPENSPEC_VERSION:-latest}"

# 设置 Tencent CodeBuddy 版本（默认为 latest）。
CODEBUDDY_VERSION="${CODEBUDDY_VERSION:-latest}"

# 安装 Claude Code 指定版本（如果版本不为 none）。
if [[ "${CLAUDE_CODE_VERSION,,}" != "none" ]]; then
    echo "Installing Claude Code version: $CLAUDE_CODE_VERSION..."
    npm install -g "@anthropic-ai/claude-code@$CLAUDE_CODE_VERSION"
else
    echo "Skipping Claude Code, version set to none"
fi

# 安装 Gemini CLI 指定版本（如果版本不为 none）。
if [[ "${GEMINI_VERSION,,}" != "none" ]]; then
    echo "Installing Gemini CLI version: $GEMINI_VERSION..."
    npm install -g "@google/gemini-cli@$GEMINI_VERSION"
else
    echo "Skipping Gemini CLI, version set to none"
fi

# 安装 Qwen Code 指定版本（如果版本不为 none）。
if [[ "${QWEN_VERSION,,}" != "none" ]]; then
    echo "Installing Qwen Code version: $QWEN_VERSION..."
    npm install -g "@qwen-code/qwen-code@$QWEN_VERSION"
else
    echo "Skipping Qwen Code, version set to none"
fi

# 安装 OpenAI CodeX 指定版本（如果版本不为 none）。
if [[ "${CODEX_VERSION,,}" != "none" ]]; then
    echo "Installing OpenAI CodeX version: $CODEX_VERSION..."
    npm install -g "@openai/codex@$CODEX_VERSION"
else
    echo "Skipping OpenAI CodeX, version set to none"
fi

# 安装 OpenSpec 指定版本（如果版本不为 none）。
if [[ "${OPENSPEC_VERSION,,}" != "none" ]]; then
    echo "Installing OpenSpec version: $OPENSPEC_VERSION..."
    npm install -g "@fission-ai/openspec@$OPENSPEC_VERSION"
else
    echo "Skipping OpenSpec, version set to none"
fi

# 安装 Tencent CodeBuddy 指定版本（如果版本不为 none）。
if [[ "${CODEBUDDY_VERSION,,}" != "none" ]]; then
    echo "Installing Tencent CodeBuddy version: $CODEBUDDY_VERSION..."
    npm install -g "@tencent-ai/codebuddy-code@$CODEBUDDY_VERSION"
else
    echo "Skipping Tencent CodeBuddy, version set to none"
fi
