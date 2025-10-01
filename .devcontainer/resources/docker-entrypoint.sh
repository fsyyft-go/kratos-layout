#!/bin/bash
set -e

# 显示容器 IP 信息。
echo "Container IP information:"
ip addr show | grep -E "inet " | grep -v "127.0.0.1" | awk "{print \$2}" | cut -d/ -f1 | sed 's/^/  /'
echo

# 调用版本检查脚本。
/usr/bin/check.version.sh

# 调用显示挂载信息脚本。
/usr/bin/check.mount.sh

# SSH 服务信息。
echo "SSH Service Information:"
echo "  - SSH server is running on port 22"
echo "  - Connect using: ssh root@localhost -p <port>"

echo "Starting SSH daemon..."
echo 
exec /usr/sbin/sshd -D "$@"