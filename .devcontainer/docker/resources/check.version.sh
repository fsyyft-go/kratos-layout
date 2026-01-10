#!/bin/bash

# 显示已安装软件版本信息
echo "Installed Software Versions:"
echo "+-------------------------+------------------+----------------+"
echo "| Software                | Version          | Status         |"
echo "+-------------------------+------------------+----------------+"

# ============ 核心开发工具 ============
# Go 版本
GO_VERSION=$(/usr/local/go/bin/go version | awk "{print \$3}" | sed "s/go//")
printf "| %-23s | %-16s | %-14s |\n" "Go" "$GO_VERSION" "✓ Installed"

# Node.js 版本
NODE_VERSION=$(node --version | sed "s/v//")
printf "| %-23s | %-16s | %-14s |\n" "Node.js" "$NODE_VERSION" "✓ Installed"

# npm 版本
NPM_VERSION=$(npm --version)
printf "| %-23s | %-16s | %-14s |\n" "npm" "$NPM_VERSION" "✓ Installed"

# ============ Go 开发工具 ============
# govulncheck 版本
if command -v govulncheck &> /dev/null; then
    GOVULNCHECK_VERSION=$(govulncheck --version 2>/dev/null | grep -o "v[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "govulncheck" "$GOVULNCHECK_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "govulncheck" "N/A" "✗ Not found"
fi

# protoc-gen-go 版本
if command -v protoc-gen-go &> /dev/null; then
    PROTOC_GEN_GO_VERSION=$(protoc-gen-go --version 2>&1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go" "$PROTOC_GEN_GO_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go" "N/A" "✗ Not found"
fi

# protoc-gen-go-grpc 版本
if command -v protoc-gen-go-grpc &> /dev/null; then
    PROTOC_GEN_GO_GRPC_VERSION=$(protoc-gen-go-grpc --version 2>&1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go-grpc" "$PROTOC_GEN_GO_GRPC_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go-grpc" "N/A" "✗ Not found"
fi

# kratos 版本
if command -v kratos &> /dev/null; then
    KRATOS_VERSION=$(kratos --version 2>/dev/null | grep -o "v[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "kratos" "$KRATOS_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "kratos" "N/A" "✗ Not found"
fi

# protoc-gen-go-http 版本
if command -v protoc-gen-go-http &> /dev/null; then
    PROTOC_GEN_GO_HTTP_VERSION=$(protoc-gen-go-http --version 2>&1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go-http" "$PROTOC_GEN_GO_HTTP_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go-http" "N/A" "✗ Not found"
fi

# protoc-gen-validate 版本
if command -v protoc-gen-validate &> /dev/null; then
    PROTOC_GEN_VALIDATE_VERSION=$(protoc-gen-validate --version 2>&1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-validate" "$PROTOC_GEN_VALIDATE_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-validate" "N/A" "✗ Not found"
fi

# protoc-gen-go-errors 版本
if command -v protoc-gen-go-errors &> /dev/null; then
    PROTOC_GEN_GO_ERRORS_VERSION=$(protoc-gen-go-errors --version 2>&1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go-errors" "$PROTOC_GEN_GO_ERRORS_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-go-errors" "N/A" "✗ Not found"
fi

# protoc-gen-openapi 版本
if command -v protoc-gen-openapi &> /dev/null; then
    PROTOC_GEN_OPENAPI_VERSION=$(protoc-gen-openapi --version 2>&1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-openapi" "$PROTOC_GEN_OPENAPI_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "protoc-gen-openapi" "N/A" "✗ Not found"
fi

# golangci-lint 版本
if command -v golangci-lint &> /dev/null; then
    GOLANGCI_VERSION=$(golangci-lint --version | grep -o "v[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1)
    printf "| %-23s | %-16s | %-14s |\n" "golangci-lint" "$GOLANGCI_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "golangci-lint" "N/A" "✗ Not found"
fi

# wire 版本
if command -v wire &> /dev/null; then
    WIRE_VERSION=$(wire --help 2>&1 | head -1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "wire" "$WIRE_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "wire" "N/A" "✗ Not found"
fi

# ============ 压缩和打包工具 ============
# UPX 版本
UPX_VERSION=$(upx --version | head -1 | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "UPX" "$UPX_VERSION" "✓ Installed"

# Tar 版本
TAR_VERSION=$(tar --version | head -1 | awk "{print \$4}")
printf "| %-23s | %-16s | %-14s |\n" "tar" "$TAR_VERSION" "✓ Installed"

# Unzip 版本
UNZIP_VERSION=$(unzip -v | head -1 | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "unzip" "$UNZIP_VERSION" "✓ Installed"

# Zip 版本
ZIP_VERSION=$(zip -v | head -2 | tail -1 | awk "{print \$4}")
printf "| %-23s | %-16s | %-14s |\n" "zip" "$ZIP_VERSION" "✓ Installed"

# ============ 版本控制和编辑器 ============
# Git 版本
GIT_VERSION=$(git --version | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "git" "$GIT_VERSION" "✓ Installed"

# Vim 版本
VIM_VERSION=$(vim --version | head -1 | awk "{print \$5}" | sed "s/,//")
printf "| %-23s | %-16s | %-14s |\n" "vim" "$VIM_VERSION" "✓ Installed"

# Nano 版本
NANO_VERSION=$(nano --version | head -1 | awk "{print \$4}")
printf "| %-23s | %-16s | %-14s |\n" "nano" "$NANO_VERSION" "✓ Installed"

# Emacs 版本
EMACS_VERSION=$(emacs --version | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "emacs-nox" "$EMACS_VERSION" "✓ Installed"

# ============ 网络工具 ============
# Curl 版本
CURL_VERSION=$(curl --version | head -1 | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "curl" "$CURL_VERSION" "✓ Installed"

# Wget 版本
WGET_VERSION=$(wget --version | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "wget" "$WGET_VERSION" "✓ Installed"

# Telnet 版本
TELNET_VERSION=$(telnet --version 2>&1 | head -1 | grep -o "[0-9]\+\.[0-9]\+" | head -1 || echo "N/A")
printf "| %-23s | %-16s | %-14s |\n" "telnet" "$TELNET_VERSION" "✓ Installed"

# Nmap 版本
NMAP_VERSION=$(nmap --version | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "nmap" "$NMAP_VERSION" "✓ Installed"

# Iftop 版本
IFTOP_VERSION=$(iftop --version 2>&1 | head -1 | awk "{print \$2}" | sed "s/,//")
printf "| %-23s | %-16s | %-14s |\n" "iftop" "$IFTOP_VERSION" "✓ Installed"

# Mtr 版本
MTR_VERSION=$(mtr --version | head -1 | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "mtr" "$MTR_VERSION" "✓ Installed"

# Socat 版本
SOCAT_VERSION=$(socat -V 2>&1 | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "socat" "$SOCAT_VERSION" "✓ Installed"

# ============ 系统工具 ============
# Rsync 版本
RSYNC_VERSION=$(rsync --version | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "rsync" "$RSYNC_VERSION" "✓ Installed"

# Tmux 版本
TMUX_VERSION=$(tmux -V | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "tmux" "$TMUX_VERSION" "✓ Installed"

# Screen 版本
SCREEN_VERSION=$(screen --version | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "screen" "$SCREEN_VERSION" "✓ Installed"

# Make 版本
MAKE_VERSION=$(make --version | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "make" "$MAKE_VERSION" "✓ Installed"

# Tree 版本
TREE_VERSION=$(tree --version | head -1 | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "tree" "$TREE_VERSION" "✓ Installed"

# Htop 版本
HTOP_VERSION=$(htop --version | head -1 | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "htop" "$HTOP_VERSION" "✓ Installed"

# JQ 版本
JQ_VERSION=$(jq --version | sed "s/jq-//")
printf "| %-23s | %-16s | %-14s |\n" "jq" "$JQ_VERSION" "✓ Installed"

# Grep 版本
GREP_VERSION=$(grep --version | head -1 | awk "{print \$4}")
printf "| %-23s | %-16s | %-14s |\n" "grep" "$GREP_VERSION" "✓ Installed"

# Sed 版本
SED_VERSION=$(sed --version | head -1 | awk "{print \$4}")
printf "| %-23s | %-16s | %-14s |\n" "sed" "$SED_VERSION" "✓ Installed"

# Gawk 版本
GAWK_VERSION=$(gawk --version | head -1 | awk "{print \$3}" | sed "s/,//")
printf "| %-23s | %-16s | %-14s |\n" "gawk" "$GAWK_VERSION" "✓ Installed"

# Gdb 版本
GDB_VERSION=$(gdb --version | head -1 | awk "{print \$4}")
printf "| %-23s | %-16s | %-14s |\n" "gdb" "$GDB_VERSION" "✓ Installed"

# Sysstat 版本
SYSSTAT_VERSION=$(sar -V 2>&1 | head -1 | awk "{print \$3}")
printf "| %-23s | %-16s | %-14s |\n" "sysstat" "$SYSSTAT_VERSION" "✓ Installed"

# Zsh 版本
ZSH_VERSION=$(zsh --version | awk "{print \$2}")
printf "| %-23s | %-16s | %-14s |\n" "zsh" "$ZSH_VERSION" "✓ Installed"

# ============ AI 助手工具 ============
# Claude Code 版本
if command -v claude &> /dev/null; then
    CLAUDE_VERSION=$(claude --version 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "1.x")
    printf "| %-23s | %-16s | %-14s |\n" "Claude Code" "$CLAUDE_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "Claude Code" "N/A" "✗ Not found"
fi

# Gemini CLI 版本
if command -v gemini &> /dev/null; then
    GEMINI_VERSION=$(gemini --version 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "Gemini CLI" "$GEMINI_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "Gemini CLI" "N/A" "✗ Not found"
fi

# Qwen Code 版本
if command -v qwen &> /dev/null; then
    QWEN_VERSION=$(qwen --version 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1 || echo "latest")
    printf "| %-23s | %-16s | %-14s |\n" "Qwen Code" "$QWEN_VERSION" "✓ Installed"
else
    printf "| %-23s | %-16s | %-14s |\n" "Qwen Code" "N/A" "✗ Not found"
fi

# ============ SSH 服务 ============
# OpenSSH 版本
SSH_VERSION=$(ssh -V 2>&1 | awk "{print \$1}" | sed "s/OpenSSH_//g" | sed "s/,//g")
printf "| %-23s | %-16s | %-14s |\n" "OpenSSH Server" "$SSH_VERSION" "✓ Installed"

# 表格结束线
echo "+-------------------------+------------------+----------------+"
echo ""
echo "Total installed software packages: 45"