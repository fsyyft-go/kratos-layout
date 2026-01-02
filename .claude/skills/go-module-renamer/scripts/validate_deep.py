#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 模块重命名 - 深层验证脚本
================================

功能：
  1. 搜索所有包含旧模块名的文件
  2. 分类文件类型（代码/配置/文档）
  3. 对不同类型采取不同策略

分类规则：
  - .go、.proto → 代码文件，不应该有残留，报告错误
  - Makefile、config.yaml → 配置文件，警告
  - README.md → 明显的文档引用，可以自动替换
  - .github/*.md → GitHub 文档，可以自动替换
  - 注释、文档 → 可能是历史说明，信息提示

输出格式：
  {
    "code": [...],      # 代码文件中的残留（错误）
    "config": [...],    # 配置文件中的残留（警告）
    "docs": [...],      # 文档文件中的残留（可自动替换）
    "other": [...]      # 其他文件
  }

返回值：
  0 - 无残留或仅有文档残留
  1 - 代码文件中有残留
  2 - 配置文件中有残留

自动化程度：70% 脚本自动化 + 30% 大模型介入
"""

import sys
import os
import json
import re
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Tuple


def ensure_python_env():
    """确保在正确的 Python 环境中运行"""
    venv_python = None

    if Path(".venv").exists():
        if platform.system() == "Windows":
            venv_python = Path(".venv/Scripts/python.exe")
        else:
            venv_python = Path(".venv/bin/python")

        if venv_python.exists():
            print("✅ 使用虚拟环境：.venv")
            return str(venv_python)

    print("ℹ️  虚拟环境未检测到，使用当前 Python")
    return sys.executable


def find_project_root():
    """
    自动定位项目根目录（包含 go.mod 的目录）

    策略：
    1. 从脚本自身位置向上查找
    2. 如果脚本在 .claude/skills/go-module-renamer/scripts/，向上 5 级
    3. 验证 go.mod 是否存在
    4. 如果不存在，尝试当前工作目录

    Returns:
        Path: 项目根目录的绝对路径
    """
    # 获取脚本自身的绝对路径
    script_path = Path(__file__).resolve()

    # 脚本在 .claude/skills/go-module-renamer/scripts/validate_deep.py
    # 需要向上 5 级到达项目根目录
    project_root = script_path.parents[4]

    # 验证 go.mod 是否存在
    if (project_root / "go.mod").exists():
        return project_root

    # 如果找不到，尝试当前工作目录
    cwd = Path.cwd()
    if (cwd / "go.mod").exists():
        return cwd

    # 如果当前工作目录也没有 go.mod，向上搜索
    for parent in [cwd] + list(cwd.parents):
        if (parent / "go.mod").exists():
            print(f"⚠️  警告：项目根目录定位为 {parent}")
            return parent

    # 实在找不到，返回当前工作目录
    print("⚠️  警告：无法找到项目根目录（go.mod），使用当前工作目录")
    return cwd


def grep_search(patterns: List[str], file_patterns: List[str] = None) -> List[Path]:
    """
    使用 grep 搜索包含指定模式的文件

    Args:
        patterns: 搜索模式列表
        file_patterns: 文件模式列表（如 ["*.go", "*.proto"]）

    Returns:
        包含匹配内容的文件路径列表
    """
    matched_files = set()

    for pattern in patterns:
        try:
            # 构建 grep 命令
            cmd = ["grep", "-r", "-l", pattern, "."]

            # 添加文件类型过滤
            if file_patterns:
                for fp in file_patterns:
                    cmd.extend(["--include", fp])

            # 执行 grep
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                # 解析输出
                for line in result.stdout.strip().split('\n'):
                    if line:
                        file_path = Path(line)
                        if file_path.is_file():
                            # 排除备份目录和虚拟环境
                            if ".backup" not in str(file_path) and ".venv" not in str(file_path):
                                matched_files.add(file_path)

        except Exception as e:
            print(f"⚠️  grep 搜索失败：{e}", file=sys.stderr)

    return list(matched_files)


def categorize_file(file_path: Path) -> str:
    """
    对文件进行分类

    Args:
        file_path: 文件路径

    Returns:
        文件类别：code, config, docs, other
    """
    suffix = file_path.suffix.lower()
    path_str = str(file_path)

    # 代码文件
    if suffix in ['.go', '.proto', '.s', '.c', '.h']:
        return 'code'

    # 配置文件
    if suffix in ['.yaml', '.yml', '.json', '.toml', '.xml', '.conf', '.ini'] or \
       file_path.name in ['Makefile', 'Dockerfile', 'docker-compose.yml', '.gitignore', '.gitattributes']:
        return 'config'

    # 文档文件
    if suffix in ['.md', '.txt', '.rst', '.adoc'] or \
       '.github' in path_str or \
       'docs' in path_str or \
       'README' in file_path.name.upper() or \
       'CHANGELOG' in file_path.name.upper():
        return 'docs'

    # 其他
    return 'other'


def validate_deep(old_module: str, old_project: str) -> Dict[str, List[Dict]]:
    """
    深层验证：搜索并分类残留引用

    Args:
        old_module: 旧模块名
        old_project: 旧项目名

    Returns:
        分类后的文件列表
    """
    # 使用智能项目根目录定位
    base_dir = find_project_root()
    print(f"📁 项目根目录：{base_dir}")
    print(f"🔍 深层验证：搜索残留引用")
    print(f"   搜索模式：")
    print(f"   - {old_module}")
    print(f"   - {old_project}")
    print("")

    # 搜索代码文件
    print("📂 搜索代码文件...")
    code_files = grep_search(
        [old_module, old_project],
        ["*.go", "*.proto"]
    )

    # 搜索配置文件
    print("📂 搜索配置文件...")
    config_files = grep_search(
        [old_project],
        ["Makefile", "*.yaml", "*.yml", "*.json", "*.toml", "Dockerfile", "docker-compose.yml"]
    )

    # 搜索文档文件
    print("📂 搜索文档文件...")
    docs_files = grep_search(
        [old_module, old_project],
        ["*.md", "*.txt", "*.rst"]
    )

    # 搜索其他文件
    print("📂 搜索其他文件...")
    other_files = grep_search(
        [old_module, old_project]
    )

    # 去重和分类
    all_files = set(code_files + config_files + docs_files + other_files)

    categorized = {
        "code": [],
        "config": [],
        "docs": [],
        "other": []
    }

    for file_path in all_files:
        category = categorize_file(file_path)

        # 获取匹配的行
        matches = get_file_matches(file_path, [old_module, old_project])

        # 尝试转换为相对路径，如果失败则使用绝对路径
        try:
            rel_path = str(file_path.relative_to(base_dir))
        except ValueError:
            rel_path = str(file_path)

        file_info = {
            "path": rel_path,
            "matches": matches
        }

        categorized[category].append(file_info)

    # 打印结果
    print_validation_results(categorized)

    return categorized


def get_file_matches(file_path: Path, patterns: List[str]) -> List[Dict]:
    """
    获取文件中匹配的行

    Args:
        file_path: 文件路径
        patterns: 搜索模式列表

    Returns:
        匹配的行信息列表
    """
    matches = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in patterns:
                    if pattern in line:
                        matches.append({
                            "line": line_num,
                            "pattern": pattern,
                            "content": line.strip()[:100]  # 限制长度
                        })

    except Exception as e:
        pass

    return matches


def print_validation_results(categorized: Dict[str, List[Dict]]):
    """打印验证结果"""
    print("")
    print("=" * 50)
    print("📊 深层验证结果")
    print("=" * 50)
    print("")

    # 代码文件
    if categorized["code"]:
        print(f"❌ 代码文件中的残留（{len(categorized['code'])} 个文件）：")
        for file_info in categorized["code"]:
            print(f"   - {file_info['path']}")
            for match in file_info['matches'][:3]:  # 只显示前 3 个匹配
                print(f"     行 {match['line']}: {match['content']}")
            if len(file_info['matches']) > 3:
                print(f"     ... 还有 {len(file_info['matches']) - 3} 个匹配")
        print("")

    # 配置文件
    if categorized["config"]:
        print(f"⚠️  配置文件中的残留（{len(categorized['config'])} 个文件）：")
        for file_info in categorized["config"]:
            print(f"   - {file_info['path']}")
            for match in file_info['matches'][:3]:
                print(f"     行 {match['line']}: {match['content']}")
            if len(file_info['matches']) > 3:
                print(f"     ... 还有 {len(file_info['matches']) - 3} 个匹配")
        print("")

    # 文档文件
    if categorized["docs"]:
        print(f"ℹ️  文档文件中的残留（{len(categorized['docs'])} 个文件）：")
        for file_info in categorized["docs"][:5]:  # 只显示前 5 个文件
            print(f"   - {file_info['path']}")
        if len(categorized["docs"]) > 5:
            print(f"   ... 还有 {len(categorized['docs']) - 5} 个文件")
        print("")

    # 其他文件
    if categorized["other"]:
        print(f"📦 其他文件中的残留（{len(categorized['other'])} 个文件）：")
        for file_info in categorized["other"][:5]:
            print(f"   - {file_info['path']}")
        if len(categorized["other"]) > 5:
            print(f"   ... 还有 {len(categorized['other']) - 5} 个文件")
        print("")

    # 总结
    print("=" * 50)
    print("📋 总结")
    print("=" * 50)
    print(f"代码文件：{len(categorized['code'])} 个")
    print(f"配置文件：{len(categorized['config'])} 个")
    print(f"文档文件：{len(categorized['docs'])} 个")
    print(f"其他文件：{len(categorized['other'])} 个")
    print("")

    # 建议
    if categorized["code"]:
        print("⚠️  发现代码文件中的残留引用，这可能导致编译或运行时错误。")
        print("   建议：手动检查并修复这些文件")
        print("")

    if categorized["config"]:
        print("⚠️  发现配置文件中的残留引用，可能需要手动调整。")
        print("   建议：检查这些配置文件是否需要更新")
        print("")

    if categorized["docs"]:
        print("ℹ️  发现文档文件中的残留引用，这些可以批量替换或手动更新。")
        print("   建议：使用编辑器的批量替换功能更新文档")
        print("")

    if not any([categorized["code"], categorized["config"], categorized["docs"], categorized["other"]]):
        print("✅ 未发现任何残留引用！")
        print("")


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法：python3 validate_deep.py <旧模块名> [--old-project=<旧项目名>]", file=sys.stderr)
        print("示例：python3 validate_deep.py github.com/fsyyft-go/kratos-layout", file=sys.stderr)
        sys.exit(1)

    old_module = sys.argv[1]

    # 解析旧项目名（如果未提供，从模块名提取）
    old_project = None
    if len(sys.argv) >= 3:
        if sys.argv[2].startswith("--old-project="):
            old_project = sys.argv[2].split("=")[1]
        else:
            old_project = sys.argv[2]

    if not old_project:
        old_project = old_module.split('/')[-1]

    # 执行深层验证
    categorized = validate_deep(old_module, old_project)

    # 输出 JSON 结果
    print("=" * 50)
    print("📄 JSON 输出")
    print("=" * 50)
    print(json.dumps(categorized, indent=2, ensure_ascii=False))
    print("")

    # 判断返回值
    if categorized["code"]:
        # 代码文件中有残留，返回 1
        sys.exit(1)
    elif categorized["config"]:
        # 配置文件中有残留，返回 2
        sys.exit(2)
    else:
        # 无残留或仅有文档/其他残留，返回 0
        sys.exit(0)


if __name__ == "__main__":
    main()
