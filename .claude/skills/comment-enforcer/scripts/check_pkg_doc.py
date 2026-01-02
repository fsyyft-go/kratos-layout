#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 代码包级别注释检查器
==========================

功能：
  1. 检查每个包目录是否存在 doc.go 文件
  2. 验证 doc.go 格式是否正确
  3. 检查是否有非 doc.go 文件包含包级别注释

使用方式：
  python3 check_pkg_doc.py [路径]

返回值：
  0 - 符合规范
  1 - 有不符合规范的地方
  2 - 检查失败

自动化程度：100% 脚本自动化
"""

import sys
import os
import json
import re
import platform
from pathlib import Path
from typing import Dict, List, Set


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

    # 脚本在 .claude/skills/comment-enforcer/scripts/check_pkg_doc.py
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


def find_package_dirs(base_dir: Path, target_path: str = None) -> List[Path]:
    """
    查找所有包目录

    Args:
        base_dir: 项目根目录
        target_path: 目标路径（可选）

    Returns:
        包目录路径列表
    """
    package_dirs = set()

    if target_path:
        # 检查特定路径
        path = base_dir / target_path
        if path.is_dir():
            # 检查该目录下是否有 .go 文件
            go_files = list(path.rglob("*.go"))
            for go_file in go_files:
                package_dirs.add(go_file.parent)
        elif path.is_file() and path.suffix == ".go":
            package_dirs.add(path.parent)
    else:
        # 检查整个项目
        go_files = [
            f for f in base_dir.rglob("*.go")
            if ".backup" not in str(f) and "vendor" not in str(f)
        ]
        for go_file in go_files:
            package_dirs.add(go_file.parent)

    return sorted(list(package_dirs))


def check_doc_go(package_dir: Path) -> Dict:
    """
    检查包的 doc.go 文件

    Args:
        package_dir: 包目录路径

    Returns:
        检查结果字典
    """
    doc_go_path = package_dir / "doc.go"

    if not doc_go_path.exists():
        return {
            "exists": False,
            "path": str(package_dir),
            "package_name": package_dir.name
        }

    # 读取 doc.go 内容
    try:
        with open(doc_go_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            "exists": True,
            "error": f"无法读取文件：{e}"
        }

    # 检查格式
    issues = []

    # 检查是否有版权声明
    if not re.search(r'Copyright\s+\d+', content, re.IGNORECASE):
        issues.append("缺少版权声明")

    # 检查是否有 Package 注释
    if not re.search(r'//\s+Package\s+\w+', content):
        issues.append("缺少 Package 级别注释")

    # 检查是否有多余的代码实现
    lines = content.split('\n')
    code_lines = 0
    in_package_decl = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('package '):
            in_package_decl = True
        elif in_package_decl and stripped and not stripped.startswith('//'):
            # package 声明后的非注释行
            code_lines += 1

    if code_lines > 1:  # 允许一个空行
        issues.append("doc.go 包含代码实现（应只有注释和 package 声明）")

    return {
        "exists": True,
        "path": str(package_dir),
        "issues": issues
    }


def check_non_doc_go_files(package_dir: Path) -> List[Dict]:
    """
    检查非 doc.go 文件是否包含包级别注释

    Args:
        package_dir: 包目录路径

    Returns:
        包含包注释的文件列表
    """
    files_with_pkg_comment = []

    # 包注释模式
    pkg_comment_pattern = re.compile(r'^//\s+Package\s+\w+')

    for go_file in package_dir.glob("*.go"):
        # 跳过 doc.go
        if go_file.name == "doc.go":
            continue

        try:
            with open(go_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue

        # 检查文件开头是否有包注释
        for i, line in enumerate(lines[:10], 1):  # 只检查前 10 行
            if pkg_comment_pattern.match(line.strip()):
                files_with_pkg_comment.append({
                    "file": str(go_file),
                    "line": i,
                    "comment": line.strip()
                })
                break

    return files_with_pkg_comment


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 获取项目根目录
    base_dir = find_project_root()
    print(f"📁 项目根目录：{base_dir}")
    print("")

    # 获取目标路径
    target_path = sys.argv[1] if len(sys.argv) > 1 else None

    # 查找所有包目录
    print("🔍 查找包目录...")
    if target_path:
        print(f"   目标路径：{target_path}")

    package_dirs = find_package_dirs(base_dir, target_path)
    print(f"   找到 {len(package_dirs)} 个包目录")
    print("")

    # 检查每个包
    print("📋 检查包级别注释...")
    print("")

    packages_missing_doc = []
    packages_with_doc_issues = []
    files_with_pkg_comment = []

    for i, pkg_dir in enumerate(package_dirs, 1):
        # 显示进度
        rel_path = pkg_dir.relative_to(base_dir)
        print(f"   [{i}/{len(package_dirs)}] {rel_path}", end='\r')

        # 检查 doc.go
        doc_check = check_doc_go(pkg_dir)

        if not doc_check.get("exists"):
            packages_missing_doc.append({
                "package": str(rel_path),
                "path": str(pkg_dir),
                "suggestion": f"创建 {rel_path}/doc.go"
            })
        elif doc_check.get("issues"):
            packages_with_doc_issues.append({
                "package": str(rel_path),
                "path": str(pkg_dir),
                "issues": doc_check["issues"]
            })

        # 检查非 doc.go 文件
        non_doc_issues = check_non_doc_go_files(pkg_dir)
        if non_doc_issues:
            files_with_pkg_comment.extend(non_doc_issues)

    print("")  # 换行

    # 输出结果
    print("")
    print("=" * 50)
    print("📊 检查结果统计")
    print("=" * 50)
    print(f"总包数：{len(package_dirs)}")
    print(f"有 doc.go 的包：{len(package_dirs) - len(packages_missing_doc)}")
    print(f"缺少 doc.go 的包：{len(packages_missing_doc)}")
    print(f"doc.go 有问题的包：{len(packages_with_doc_issues)}")
    print(f"包含包注释的非 doc.go 文件：{len(files_with_pkg_comment)}")
    print("")

    # 显示详细问题
    if packages_missing_doc:
        print("=" * 50)
        print("❌ 缺少 doc.go 的包")
        print("=" * 50)
        print("")

        for pkg in packages_missing_doc[:10]:
            print(f"   📦 {pkg['package']}")
            print(f"      建议：{pkg['suggestion']}")
            print("")

        if len(packages_missing_doc) > 10:
            print(f"   ... 还有 {len(packages_missing_doc) - 10} 个包缺少 doc.go")
            print("")

    if packages_with_doc_issues:
        print("=" * 50)
        print("⚠️  doc.go 有问题的包")
        print("=" * 50)
        print("")

        for pkg in packages_with_doc_issues[:10]:
            print(f"   📦 {pkg['package']}")
            for issue in pkg['issues']:
                print(f"      • {issue}")
            print("")

        if len(packages_with_doc_issues) > 10:
            print(f"   ... 还有 {len(packages_with_doc_issues) - 10} 个包有问题")
            print("")

    if files_with_pkg_comment:
        print("=" * 50)
        print("⚠️  包含包注释的非 doc.go 文件")
        print("=" * 50)
        print("")

        for file_info in files_with_pkg_comment[:10]:
            file_path = Path(file_info['file']).relative_to(base_dir)
            print(f"   📄 {file_info['file']}")
            print(f"      行 {file_info['line']}：{file_info['comment']}")
            print(f"      建议：移动到 doc.go 文件")
            print("")

        if len(files_with_pkg_comment) > 10:
            print(f"   ... 还有 {len(files_with_pkg_comment) - 10} 个文件有问题")
            print("")

    # 输出 JSON 结果
    output = {
        "total_packages": len(package_dirs),
        "packages_with_doc": len(package_dirs) - len(packages_missing_doc),
        "packages_missing_doc": packages_missing_doc,
        "packages_with_doc_issues": packages_with_doc_issues,
        "files_with_pkg_comment": [
            {
                "file": str(Path(f['file']).relative_to(base_dir)),
                "line": f['line'],
                "comment": f['comment']
            }
            for f in files_with_pkg_comment
        ]
    }

    output_file = base_dir / ".backup" / "comments" / "pkg_results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("=" * 50)
    print(f"✅ 结果已保存到：{output_file.relative_to(base_dir)}")
    print("")

    # 返回值
    if packages_missing_doc or packages_with_doc_issues or files_with_pkg_comment:
        sys.exit(1)  # 有不符合规范的地方
    else:
        sys.exit(0)  # 符合规范


if __name__ == "__main__":
    main()
