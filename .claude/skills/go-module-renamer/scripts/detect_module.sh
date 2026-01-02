#!/bin/bash

# =============================================================================
# Go 模块名检测器
# =============================================================================
# 功能：
#   从 go.mod 读取当前模块名
#   解析模块名结构（域名、用户名、项目名）
#   输出 JSON 格式信息
#
# 输出格式：
#   {
#     "full_path": "github.com/fsyyft-go/kratos-layout",
#     "domain": "github.com",
#     "username": "fsyyft-go",
#     "project": "kratos-layout"
#   }
#
# 返回值：
#   0 - 成功
#   1 - go.mod 不存在
#   2 - 无法解析模块名
#
# 自动化程度：100% 脚本自动化，无需大模型介入
# =============================================================================

set -e  # 遇到错误立即退出

# 颜色定义（用于终端输出，不影响 JSON）
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# 检查 go.mod 文件是否存在
if [ ! -f "go.mod" ]; then
    echo -e "${RED}错误：go.mod 文件不存在${NC}" >&2
    echo "请在 Go 项目根目录下运行此脚本" >&2
    exit 1
fi

# 从 go.mod 提取模块名
# 使用 grep 和 awk 提取 "module xxx" 行中的模块名
MODULE_LINE=$(grep "^module " go.mod | head -n 1)

if [ -z "$MODULE_LINE" ]; then
    echo -e "${RED}错误：无法从 go.mod 解析模块名${NC}" >&2
    echo "go.mod 文件格式可能不正确" >&2
    exit 2
fi

# 提取模块路径（去掉 "module " 前缀和空格）
MODULE_PATH=$(echo "$MODULE_LINE" | sed 's/^module //' | sed 's/[[:space:]]*$//')

# 解析模块路径的各个部分
# 格式通常为：domain/username/project 或 domain/username/project/subpackage
IFS='/' read -r -a PARTS <<< "$MODULE_PATH"

DOMAIN="${PARTS[0]}"
USERNAME="${PARTS[1]}"
PROJECT="${PARTS[2]}"

# 输出 JSON 格式结果
cat <<EOF
{
  "full_path": "$MODULE_PATH",
  "domain": "$DOMAIN",
  "username": "$USERNAME",
  "project": "$PROJECT"
}
EOF

exit 0
