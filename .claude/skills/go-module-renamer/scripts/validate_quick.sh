#!/bin/bash

# =============================================================================
# Go 模块重命名 - 浅层验证脚本
# =============================================================================
# 功能：
#   执行快速验证命令
#   收集验证结果
#   返回通过/失败状态
#
# 验证命令序列：
#   1. go fmt ./...        - 代码格式化
#   2. go mod tidy         - 依赖管理
#   3. make lint           - Lint 检查（可选）
#   4. make build          - 编译验证（可选）
#
# 输出：
#   每个步骤的通过/失败状态
#   失败时的错误摘要
#
# 返回值：
#   0 - 全部通过
#   1 - 有失败
#
# 自动化程度：100% 脚本自动化，无需大模型介入
# =============================================================================

set -e  # 遇到错误立即退出（可被某些命令覆盖）

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 统计变量
TOTAL_STEPS=0
PASSED_STEPS=0
FAILED_STEPS=0

# 日志函数
log_step() {
    echo "======================================"
    echo "步骤 $((TOTAL_STEPS + 1)): $1"
    echo "======================================"
    TOTAL_STEPS=$((TOTAL_STEPS + 1))
}

log_success() {
    echo -e "${GREEN}✓ 通过${NC}: $1"
    PASSED_STEPS=$((PASSED_STEPS + 1))
}

log_failure() {
    echo -e "${RED}✗ 失败${NC}: $1"
    FAILED_STEPS=$((FAILED_STEPS + 1))
}

log_warning() {
    echo -e "${YELLOW}⚠ 警告${NC}: $1"
}

# 检查是否在 Go 项目中
if [ ! -f "go.mod" ]; then
    log_failure "go.mod 文件不存在，请确保在 Go 项目根目录下运行"
    exit 1
fi

# 解析命令行参数
SKIP_LINT=false
SKIP_BUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-lint)
            SKIP_LINT=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        *)
            echo "未知参数：$1"
            echo "用法：$0 [--skip-lint] [--skip-build]"
            exit 1
            ;;
    esac
done

echo "🚀 开始浅层验证..."
echo ""

# =============================================================================
# 步骤 1: 代码格式化
# =============================================================================
log_step "代码格式化 (go fmt)"

if go fmt ./... > /dev/null 2>&1; then
    log_success "代码格式化完成"
else
    log_failure "代码格式化失败"
fi

echo ""

# =============================================================================
# 步骤 2: 依赖管理
# =============================================================================
log_step "依赖管理 (go mod tidy)"

if go mod tidy 2>&1; then
    log_success "依赖管理完成"
else
    log_failure "依赖管理失败"
fi

echo ""

# =============================================================================
# 步骤 3: Lint 检查（可选）
# =============================================================================
if [ "$SKIP_LINT" = false ]; then
    log_step "Lint 检查 (make lint)"

    # 检查 Makefile 中是否有 lint 目标
    if grep -q "^lint:" Makefile 2>/dev/null || grep -q "^\.PHONY:.*lint" Makefile 2>/dev/null; then
        if make lint 2>&1; then
            log_success "Lint 检查通过"
        else
            log_failure "Lint 检查失败"
        fi
    else
        log_warning "Makefile 中未找到 lint 目标，跳过此步骤"
    fi
else
    log_warning "跳过 Lint 检查（--skip-lint）"
fi

echo ""

# =============================================================================
# 步骤 4: 编译验证（可选）
# =============================================================================
if [ "$SKIP_BUILD" = false ]; then
    log_step "编译验证 (make build)"

    # 检查 Makefile 中是否有 build 目标
    if grep -q "^build:" Makefile 2>/dev/null || grep -q "^\.PHONY:.*build" Makefile 2>/dev/null; then
        if make build 2>&1; then
            log_success "编译验证通过"
        else
            log_failure "编译验证失败"
        fi
    else
        log_warning "Makefile 中未找到 build 目标，尝试直接使用 go build"

        if go build ./... 2>&1; then
            log_success "编译验证通过"
        else
            log_failure "编译验证失败"
        fi
    fi
else
    log_warning "跳过编译验证（--skip-build）"
fi

echo ""
echo "======================================"
echo "验证总结"
echo "======================================"
echo -e "总步骤数: $TOTAL_STEPS"
echo -e "${GREEN}通过: $PASSED_STEPS${NC}"
echo -e "${RED}失败: $FAILED_STEPS${NC}"
echo ""

# 判断总体结果
if [ $FAILED_STEPS -eq 0 ]; then
    echo -e "${GREEN}✅ 浅层验证全部通过！${NC}"
    exit 0
else
    echo -e "${RED}❌ 浅层验证失败，请检查错误信息${NC}"
    echo ""
    echo "建议："
    echo "  1. 查看上述错误信息"
    echo "  2. 运行失败的单个命令以获取详细错误"
    echo "  3. 修复问题后重新运行验证"
    echo "  4. 如果需要，可以使用 --rollback 恢复备份"
    exit 1
fi
