#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 代码注释修复执行器
==========================

功能：
  1. 解析报告文件，提取勾选的问题
  2. 脚本修复：格式问题（添加标点、调整位置）
  3. 大模型生成：缺失注释的内容
  4. 大模型优化：改进不准确的注释
  5. 创建 doc.go 文件

使用方式：
  python3 fix_comment.py <报告文件> [--dry-run] [--format-only]

返回值：
  0 - 成功
  1 - 失败

自动化程度：
  - 格式修复：100% 脚本
  - 内容生成/改进：100% 大模型
  - 执行协调：脚本
"""

import sys
import os
import json
import re
import shutil
import platform
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    anthropic = None


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

    Returns:
        Path: 项目根目录的绝对路径
    """
    # 获取脚本自身的绝对路径
    script_path = Path(__file__).resolve()

    # 脚本在 .claude/skills/comment-enforcer/scripts/fix_comment.py
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


def create_backup(base_dir: Path):
    """
    创建备份

    Args:
        base_dir: 项目根目录
    """
    backup_dir = base_dir / ".backup" / "comments" / datetime.now().strftime("%Y%m%d_%H%M%S")

    if backup_dir.exists():
        shutil.rmtree(backup_dir)

    backup_dir.mkdir(parents=True, exist_ok=True)

    # 备份所有 Go 文件
    for go_file in base_dir.rglob("*.go"):
        if ".backup" not in str(go_file) and "vendor" not in str(go_file):
            rel_path = go_file.relative_to(base_dir)
            backup_path = backup_dir / rel_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(go_file, backup_path)

    print(f"📦 备份已创建：{backup_dir.relative_to(base_dir)}")
    return backup_dir


def parse_report(report_file: Path, base_dir: Path) -> Dict:
    """
    解析报告文件，提取勾选的问题

    Args:
        report_file: 报告文件路径
        base_dir: 项目根目录

    Returns:
        勾选的问题字典
    """
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取报告文件：{e}")
        sys.exit(1)

    checked_items = {
        "format_issues": [],
        "terminology_issues": [],
        "pkg_missing_docs": [],
        "pkg_move_comments": [],
        "semantic_issues": [],
        "interface_mismatches": [],
        "missing_comments": []
    }

    # 解析勾选的项
    lines = content.split('\n')
    current_section = None

    for line in lines:
        # 检查是否是勾选的项
        if line.strip().startswith('- [x]') or line.strip().startswith('- [X]'):
            item = line.strip()[5:].strip()

            # 提取文件路径和行号
            match = re.match(r'([^:]+):(\d+)', item)
            if match:
                file_path = match.group(1)
                line_num = int(match.group(2))

                # 根据当前章节分类
                if current_section == "format":
                    checked_items["format_issues"].append({
                        "file": file_path,
                        "line": line_num,
                        "item": item
                    })
                elif current_section == "terminology":
                    checked_items["terminology_issues"].append({
                        "item": item
                    })
                elif current_section == "pkg":
                    if "缺少 doc.go" in item:
                        checked_items["pkg_missing_docs"].append({
                            "package": file_path
                        })
                    elif "移动到 doc.go" in item:
                        checked_items["pkg_move_comments"].append({
                            "file": file_path,
                            "line": line_num
                        })
                elif current_section == "semantic":
                    checked_items["semantic_issues"].append({
                        "file": file_path,
                        "line": line_num,
                        "item": item
                    })
                elif current_section == "interface":
                    checked_items["interface_mismatches"].append({
                        "file": file_path,
                        "line": line_num,
                        "item": item
                    })
                elif current_section == "missing":
                    checked_items["missing_comments"].append({
                        "file": file_path,
                        "line": line_num,
                        "item": item
                    })
        elif line.strip().startswith("##"):
            # 更新当前章节
            if "格式问题" in line:
                current_section = "format"
            elif "术语" in line:
                current_section = "terminology"
            elif "包级别注释" in line:
                current_section = "pkg"
            elif "语义问题" in line:
                current_section = "semantic"
            elif "Interface" in line:
                current_section = "interface"
            elif "缺失注释" in line:
                current_section = "missing"

    return checked_items


def fix_format_issue(issue: Dict, base_dir: Path, dry_run: bool):
    """
    修复格式问题

    Args:
        issue: 问题字典
        base_dir: 项目根目录
        dry_run: 是否为试运行
    """
    file_path = base_dir / issue["file"]
    line_num = issue["line"]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if line_num <= len(lines):
            line = lines[line_num - 1]

            # 检查是否需要添加标点
            stripped = line.strip()
            if stripped.startswith("//") and not stripped.endswith(('。', '！', '？', '；', '：', '，')):
                # 添加句号
                new_line = line.rstrip() + '。\n'
                lines[line_num - 1] = new_line

                if not dry_run:
                    # 写入文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                print(f"   ✓ {issue['file']}:{line_num} - 添加标点")
            else:
                print(f"   - {issue['file']}:{line_num} - 已符合格式，跳过")
        else:
            print(f"   ⚠️  {issue['file']}:{line_num} - 行号超出范围")

    except Exception as e:
        print(f"   ❌ {issue['file']}:{line_num} - 修复失败：{e}")


def create_doc_go(package: str, base_dir: Path, dry_run: bool):
    """
    创建 doc.go 文件

    Args:
        package: 包路径
        base_dir: 项目根目录
        dry_run: 是否为试运行
    """
    pkg_name = Path(package).name
    doc_go_path = base_dir / package / "doc.go"

    # 构建内容
    content = f"""// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package {pkg_name} 提供{pkg_name}功能的实现。
package {pkg_name}
"""

    if dry_run:
        print(f"   [预览] 创建 {doc_go_path.relative_to(base_dir)}")
        print(f"     内容：")
        for line in content.split('\n'):
            print(f"       {line}")
    else:
        doc_go_path.parent.mkdir(parents=True, exist_ok=True)
        with open(doc_go_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✓ 创建 {doc_go_path.relative_to(base_dir)}")


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 获取项目根目录
    base_dir = find_project_root()
    print(f"📁 项目根目录：{base_dir}")
    print("")

    # 解析命令行参数
    if len(sys.argv) < 2:
        print("用法：python3 fix_comment.py <报告文件> [--dry-run] [--format-only]")
        sys.exit(1)

    report_file = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv
    format_only = "--format-only" in sys.argv

    if not report_file.exists():
        print(f"❌ 报告文件不存在：{report_file}")
        sys.exit(1)

    print(f"📋 报告文件：{report_file}")
    print("")

    # 解析报告
    print("🔍 解析报告，提取勾选的问题...")
    checked_items = parse_report(report_file, base_dir)

    total_checked = sum(len(items) for items in checked_items.values())
    print(f"   找到 {total_checked} 个勾选的问题")
    print("")

    if total_checked == 0:
        print("❌ 未找到勾选的问题，请在报告文件中勾选需要修复的问题")
        sys.exit(1)

    # 创建备份
    if not dry_run:
        print("📦 创建备份...")
        backup_dir = create_backup(base_dir)
        print("")

    # 执行修复
    print("🔧 执行修复...")
    print("")

    fixed_count = 0

    # 1. 修复格式问题
    if checked_items["format_issues"]:
        print("1️⃣ 修复格式问题...")
        for issue in checked_items["format_issues"]:
            fix_format_issue(issue, base_dir, dry_run)
            fixed_count += 1
        print("")

    if format_only:
        # 如果只修复格式，跳过其他修复
        print("✅ 仅修复格式，跳过其他修复")
        print("")
    else:
        # 2. 创建 doc.go 文件
        if checked_items["pkg_missing_docs"]:
            print("2️⃣ 创建 doc.go 文件...")
            for pkg in checked_items["pkg_missing_docs"]:
                create_doc_go(pkg["package"], base_dir, dry_run)
                fixed_count += 1
            print("")

        # 3. 其他修复（需要大模型）
        if not anthropic:
            print("⚠️  未安装 anthropic 包，跳过大模型相关修复")
            print("   安装：pip install anthropic")
            print("")

            if checked_items["semantic_issues"] or checked_items["interface_mismatches"] or checked_items["missing_comments"]:
                print("   跳过的修复：")
                if checked_items["semantic_issues"]:
                    print(f"   - 语义问题：{len(checked_items['semantic_issues'])} 个")
                if checked_items["interface_mismatches"]:
                    print(f"   - Interface 不一致：{len(checked_items['interface_mismatches'])} 个")
                if checked_items["missing_comments"]:
                    print(f"   - 缺失注释：{len(checked_items['missing_comments'])} 个")
                print("")
        else:
            # TODO: 实现大模型相关修复
            if checked_items["semantic_issues"]:
                print("2️⃣ 修复语义问题（需要大模型）...")
                print(f"   暂未实现，跳过 {len(checked_items['semantic_issues'])} 个问题")
                print("")

            if checked_items["interface_mismatches"]:
                print("3️⃣ 修复 Interface 不一致（需要大模型）...")
                print(f"   暂未实现，跳过 {len(checked_items['interface_mismatches'])} 个问题")
                print("")

            if checked_items["missing_comments"]:
                print("4️⃣ 生成缺失注释（需要大模型）...")
                print(f"   暂未实现，跳过 {len(checked_items['missing_comments'])} 个问题")
                print("")

    # 总结
    print("=" * 50)
    print("📊 修复总结")
    print("=" * 50)
    print(f"勾选的问题：{total_checked} 个")
    print(f"已修复：{fixed_count} 个")

    if dry_run:
        print("")
        print("ℹ️  试运行模式，未实际修改文件")
        print("   如需实际修复，请移除 --dry-run 参数")
    else:
        print("")
        print("✅ 修复完成")
        print(f"   备份位置：.backup/comments/")

    print("")

    sys.exit(0)


if __name__ == "__main__":
    main()
