#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 模块重命名类型分析器
=========================

功能：
  - 比较新旧模块名
  - 判断全量或部分重命名
  - 生成替换规则列表

输出格式：
  {
    "type": "full" | "partial",
    "old_module": "github.com/fsyyft-go/kratos-layout",
    "new_module": "github.com/new-org/new-project",
    "old_project": "kratos-layout",
    "new_project": "new-project",
    "replacements": {
      "full_replace": [...],
      "partial_replace": [...]
    }
  }

返回值：
  0 - 成功
  1 - 参数错误
  2 - 模块名格式无效

自动化程度：100% 脚本自动化，无需大模型介入
"""

import sys
import json
import platform
from pathlib import Path


def ensure_python_env():
    """
    确保在正确的 Python 环境中运行

    策略：
    1. 检查 .venv 是否存在
    2. 如果存在，使用虚拟环境中的 Python
    3. 如果不存在，返回当前 Python（由调用方决定是否创建）

    返回：
        当前使用的 Python 解释器路径
    """
    venv_python = None

    # 检查虚拟环境
    if Path(".venv").exists():
        if platform.system() == "Windows":
            venv_python = Path(".venv/Scripts/python.exe")
        else:
            venv_python = Path(".venv/bin/python")

        if venv_python.exists():
            print("✅ 使用虚拟环境：.venv", file=sys.stderr)
            return str(venv_python)

    # 虚拟环境不存在或不可用
    print("ℹ️  虚拟环境未检测到，使用当前 Python", file=sys.stderr)
    return sys.executable


def validate_module_name(module_name):
    """
    验证模块名格式

    Go 模块名格式：domain/username/project
    至少包含两个斜杠分隔的部分

    Args:
        module_name: 模块名字符串

    Returns:
        bool: 有效返回 True，否则返回 False
    """
    if not module_name or not isinstance(module_name, str):
        return False

    parts = module_name.split('/')
    if len(parts) < 3:
        return False

    # 简单的域名格式检查
    if '.' not in parts[0]:
        return False

    return True


def analyze_rename_type(old_module, new_module):
    """
    分析重命名类型

    判断逻辑：
    - 比较模块名路径的前两个部分（域名、用户名）
    - 如果前两部分相同 → 部分重命名（仅项目名变化）
    - 如果前两部分不同 → 全量重命名（域名或用户名变化）

    Args:
        old_module: 旧模块名
        new_module: 新模块名

    Returns:
        dict: 包含重命名类型和替换规则的字典
    """
    old_parts = old_module.split('/')
    new_parts = new_module.split('/')

    # 检查前两部分是否相同
    if old_parts[:2] == new_parts[:2]:
        rename_type = "partial"  # 部分重命名
    else:
        rename_type = "full"  # 全量重命名

    old_project = old_parts[-1]
    new_project = new_parts[-1]

    # 生成替换规则
    replacements = generate_replacement_rules(
        rename_type, old_module, new_module, old_project, new_project
    )

    return {
        "type": rename_type,
        "old_module": old_module,
        "new_module": new_module,
        "old_project": old_project,
        "new_project": new_project,
        "replacements": replacements
    }


def generate_replacement_rules(rename_type, old_module, new_module, old_project, new_project):
    """
    生成替换规则列表

    Args:
        rename_type: 重命名类型（"full" 或 "partial"）
        old_module: 旧模块名
        new_module: 新模块名
        old_project: 旧项目名
        new_project: 新项目名

    Returns:
        dict: 包含 full_replace 和 partial_replace 规则的字典
    """
    rules = {
        "full_replace": [],
        "partial_replace": []
    }

    if rename_type == "full":
        # 全量替换规则：替换完整的模块路径
        rules["full_replace"] = [
            {
                "file_pattern": "go.mod",
                "search_pattern": f"module {old_module}",
                "replace_pattern": f"module {new_module}",
                "description": "模块声明"
            },
            {
                "file_pattern": "*.go",
                "search_pattern": f'"{old_module}/',
                "replace_pattern": f'"{new_module}/',
                "description": "导入路径"
            },
            {
                "file_pattern": "*.proto",
                "search_pattern": f'option go_package = "{old_module}/',
                "replace_pattern": f'option go_package = "{new_module}/',
                "description": "Proto go_package"
            },
        ]

        # 全量重命名时，也要替换项目名
        rules["partial_replace"] = [
            {
                "file_pattern": "Makefile",
                "search_pattern": old_project,
                "replace_pattern": new_project,
                "description": "Docker 镜像名"
            },
            {
                "file_pattern": "OWNERS",
                "search_pattern": old_project,
                "replace_pattern": new_project,
                "description": "项目所有者"
            },
            {
                "file_pattern": "*.md",
                "search_pattern": old_project,
                "replace_pattern": new_project,
                "description": "文档引用"
            },
        ]
    else:
        # 部分替换规则：仅替换项目名
        rules["partial_replace"] = [
            {
                "file_pattern": "Makefile",
                "search_pattern": old_project,
                "replace_pattern": new_project,
                "description": "Docker 镜像名"
            },
            {
                "file_pattern": "OWNERS",
                "search_pattern": old_project,
                "replace_pattern": new_project,
                "description": "项目所有者"
            },
            {
                "file_pattern": "*.md",
                "search_pattern": old_project,
                "replace_pattern": new_project,
                "description": "文档引用"
            },
            {
                "file_pattern": "config.proto",
                "search_pattern": old_project,
                "replace_pattern": new_project,
                "description": "配置文件"
            },
        ]

    return rules


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 检查命令行参数
    if len(sys.argv) != 3:
        print("用法：python3 analyze_rename_type.py <旧模块名> <新模块名>", file=sys.stderr)
        print("示例：python3 analyze_rename_type.py github.com/fsyyft-go/kratos-layout github.com/new-org/new-project", file=sys.stderr)
        sys.exit(1)

    old_module = sys.argv[1]
    new_module = sys.argv[2]

    # 验证模块名格式
    if not validate_module_name(old_module):
        print(f"错误：旧模块名格式无效：{old_module}", file=sys.stderr)
        print("模块名格式应为：domain/username/project", file=sys.stderr)
        sys.exit(2)

    if not validate_module_name(new_module):
        print(f"错误：新模块名格式无效：{new_module}", file=sys.stderr)
        print("模块名格式应为：domain/username/project", file=sys.stderr)
        sys.exit(2)

    # 分析重命名类型
    result = analyze_rename_type(old_module, new_module)

    # 输出 JSON 结果
    print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(0)


if __name__ == "__main__":
    main()
