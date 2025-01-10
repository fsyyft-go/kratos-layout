#!/bin/bash
set -e

# 清理 Go 临时文件和缓存。
# 这个清理过程，没有挂载缓存，就是清理目标容器内的。
echo "Cleaning up Go caches and temporary files..." && \
    go clean -modcache && \
    go clean -cache && \
    go clean -testcache && \
    rm -rf /tmp/* && \
    echo "Cleanup completed."

# 清理 npm 缓存。
echo "Cleaning up npm cache..." && \
    npm cache clean --force && \
    rm -rf /root/.npm && \
    rm -rf /tmp/* && \
    echo "npm cleanup completed."

# 清理 APT 缓存和临时文件。
echo "Cleaning up APT caches and temporary files..." && \
    apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/* && \
    echo "APT cleanup completed."

# 最终清理系统临时文件。
echo "Final system cleanup..." && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/* && \
    rm -rf /root/.cache && \
    find /var/log -type f -name "*.log" -delete && \
    echo "Final cleanup completed."