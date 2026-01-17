#!/bin/bash
set -e

# 初始化函数：仅在 SSH 模式下执行（无用户命令时）
initialize_ssh_environment() {
    # 设置用户密码（如果提供了 USER_PASSWORD 环境变量）。
    if [ -n "$USER_PASSWORD" ]; then
        echo "Setting passwords for root, fsyyft, and ubuntu users..."
        echo "root:$USER_PASSWORD" | chpasswd
        echo "fsyyft:$USER_PASSWORD" | chpasswd
        echo "ubuntu:$USER_PASSWORD" | chpasswd
        unset USER_PASSWORD  # 使用后立即清除环境变量
        echo "Passwords set successfully."
        echo
    fi

    # 调用版本检查脚本。
    /usr/bin/check.version.sh

    # 调用显示挂载信息脚本。
    /usr/bin/check.mount.sh

    # 显示容器 IP 信息。
    echo "Container IP information:"
    ip addr show | grep -E "inet " | grep -v "127.0.0.1" | awk "{print \$2}" | cut -d/ -f1 | sed 's/^/  /'
    echo

    # SSH 服务信息。
    echo "SSH Service Information:"
    echo "  - SSH server is running on port 22"
    echo "  - Connect using: ssh root@localhost -p <port>"
}

# 更新 OpenCode 配置的函数。
# 可以使用 opencode -m zhipuai-coding-plan/glm-4.7 使用。
update_opencode_auth_json() {
    # 检查 ANTHROPIC_BASE_URL 是否等于预期值。
    if [ "$ANTHROPIC_BASE_URL" != "https://open.bigmodel.cn/api/anthropic" ]; then
        return
    fi

    # 直接创建 auth.json 文件。
    local AUTH_FILE="$HOME/.local/share/opencode/auth.json"
    local AUTH_DIR="$HOME/.local/share/opencode"

    # 确保目录存在。
    mkdir -p "$AUTH_DIR"

    # 使用环境变量创建新的 auth.json 文件。
    jq -n --arg key "$ANTHROPIC_API_KEY" \
       '{"zhipuai-coding-plan": {"type": "api", "key": $key}}' \
       > "$AUTH_FILE"
}

update_opencode_auth_json

# 根据参数和环境变量决定启动模式。
if [ "$START_SSH" != "no" ] && [ $# -eq 0 ]; then
    # 默认：只启动 SSH（前台模式）。
    initialize_ssh_environment
    echo "Starting SSH daemon in foreground..."
    echo
    exec /usr/sbin/sshd -D
elif [ "$START_SSH" != "no" ]; then
    # 有命令参数且 START_SSH 未设置为 no：SSH 后台 + 用户命令。
    # 为避免输出干扰信息，SSH 服务启动在后台，并且不输出任何信息。
    /usr/sbin/sshd
    exec "$@"
else
    # START_SSH=no：只执行用户命令，不启动 SSH。
    echo "SSH disabled by START_SSH environment variable."
    echo "Executing: $*"
    echo
    exec "$@"
fi