#!/bin/bash

set -e

# 容器挂载信息查看脚本
# 使用 findmnt 命令获取所有挂载信息并分类显示

echo "Container Mount Information"
echo "========================"

echo ""
echo "Explicit Mounts (User-defined volumes)"
echo "----------------------------------------"

# 获取显式挂载（用户定义的volumes）
# 使用 findmnt --pairs 输出，然后解析
findmnt --pairs -o TARGET,SOURCE,FSTYPE,OPTIONS 2>/dev/null | while read -r line; do
    # 解析 --pairs 格式: TARGET="/home/workspace" SOURCE="/dev/vdb1[...]" FSTYPE="ext4" OPTIONS="rw,relatime"
    target=$(echo "$line" | sed -n 's/.*TARGET="\([^"]*\)".*/\1/p')
    source=$(echo "$line" | sed -n 's/.*SOURCE="\([^"]*\)".*/\1/p')
    fstype=$(echo "$line" | sed -n 's/.*FSTYPE="\([^"]*\)".*/\1/p')
    options=$(echo "$line" | sed -n 's/.*OPTIONS="\([^"]*\)".*/\1/p')

    # 过滤显式挂载 - 使用POSIX兼容语法
    explicit_mount=0
    case "$target" in
        /home/*|/workspace/*|/go/*|/app/*|/data/*) explicit_mount=1 ;;
    esac
    if [ "$fstype" = "virtiofs" ] || [ "$fstype" = "fuse" ]; then
        explicit_mount=1
    fi

    if [ "$explicit_mount" -eq 1 ]; then
        # 提取权限信息
        if echo "$options" | grep -q "rw"; then
            perms="Read-Write"
        else
            perms="Read-Only"
        fi

        # 确定源类型
        if echo "$source" | grep -q "^/"; then
            source_type="Host Path"
        elif [ "$fstype" = "virtiofs" ]; then
            source_type="VirtioFS"
        elif [ "$fstype" = "fuse" ]; then
            source_type="Fuse"
        else
            source_type="Volume"
        fi

        printf "  %-18s %-12s %-10s %s\n" "$target" "$perms" "$source_type" "$source"
    fi
done

echo ""
echo "Implicit Mounts (Docker internal)"
echo "-----------------------------------"

# 获取隐式挂载（Docker内部管理的文件）
findmnt --pairs -o TARGET,SOURCE,FSTYPE,OPTIONS 2>/dev/null | while read -r line; do
    # 解析 --pairs 格式
    target=$(echo "$line" | sed -n 's/.*TARGET="\([^"]*\)".*/\1/p')
    source=$(echo "$line" | sed -n 's/.*SOURCE="\([^"]*\)".*/\1/p')
    fstype=$(echo "$line" | sed -n 's/.*FSTYPE="\([^"]*\)".*/\1/p')
    options=$(echo "$line" | sed -n 's/.*OPTIONS="\([^"]*\)".*/\1/p')

    # 过滤隐式挂载（Docker内部管理的配置文件）- 使用POSIX兼容语法
    if echo "$source" | grep -q "\[.*docker/containers.*\]"; then
        # 提取权限信息
        if echo "$options" | grep -q "rw"; then
            perms="Read-Write"
        else
            perms="Read-Only"
        fi

        printf "  %-18s %-12s %-10s %s\n" "$target" "$perms" "Internal" "$source"
    fi
done

echo ""
echo "Legend:"
echo "   • Explicit Mounts: User-defined volumes in docker-compose.yml"
echo "   • Implicit Mounts: Docker-managed container configuration files"
echo "   • Host Path: Direct mount from host filesystem"
echo "   • VirtioFS/Fuse: Docker Desktop optimized mounts"
echo "   • Internal: Docker container runtime mounts"