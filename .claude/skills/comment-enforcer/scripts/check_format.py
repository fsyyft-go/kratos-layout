#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 代码注释格式检查器
==========================

功能：
  1. 检查注释是否存在
  2. 检查注释是否以中文标点结束
  3. 检查注释位置是否正确（在声明上方）
  4. 统计缺失注释的数量

使用方式：
  python3 check_format.py [路径]

返回值：
  0 - 无问题或仅有可自动修复的问题
  1 - 有缺失注释
  2 - 检查失败

自动化程度：100% 脚本自动化
"""

import sys
import os
import json
import re
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

    Returns:
        Path: 项目根目录的绝对路径
    """
    # 获取脚本自身的绝对路径
    script_path = Path(__file__).resolve()

    # 脚本在 .claude/skills/comment-enforcer/scripts/check_format.py
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


def collect_go_files(base_dir: Path, target_path: str = None) -> List[Path]:
    """
    收集需要检查的 Go 文件

    Args:
        base_dir: 项目根目录
        target_path: 目标路径（可选）

    Returns:
        Go 文件路径列表
    """
    if target_path:
        # 检查特定路径
        path = base_dir / target_path
        if path.is_file() and path.suffix == ".go":
            return [path]
        elif path.is_dir():
            return list(path.rglob("*.go"))
        else:
            print(f"⚠️  警告：路径不存在或不是 Go 文件：{target_path}")
            return []
    else:
        # 检查整个项目（排除 vendor 和 .backup）
        go_files = []
        for pattern in ["*.go"]:
            go_files.extend([
                f for f in base_dir.rglob(pattern)
                if ".backup" not in str(f) and "vendor" not in str(f)
            ])
        return go_files


def parse_go_file(file_path: Path) -> Tuple[List[str], List[Tuple[int, str, str]]]:
    """
    解析 Go 文件，提取声明和注释

    Args:
        file_path: Go 文件路径

    Returns:
        (代码行列表, 声明列表)
        声明列表格式：(行号, 类型, 名称)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"⚠️  无法读取文件 {file_path}：{e}")
        return [], []

    declarations = []

    # 正则模式
    patterns = {
        'type': r'^type\s+(\w+)\s+(struct|interface)\s*{?',
        'func': r'^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(',
        'var': r'^var\s+(\w+)',
        'const': r'^const\s+(\w+)',
    }

    for line_num, line in enumerate(lines, 1):
        # 跳过注释行
        if line.strip().startswith('//'):
            continue

        # 检查各种声明
        for decl_type, pattern in patterns.items():
            match = re.match(pattern, line.strip())
            if match:
                name = match.group(1)
                declarations.append((line_num, decl_type, name))
                break

    return lines, declarations


def extract_comment_before(lines: List[str], line_num: int) -> str:
    """
    提取声明前的注释

    Args:
        lines: 代码行列表
        line_num: 声明行号（从 1 开始）

    Returns:
        注释内容（不包含 // 符号）
    """
    if line_num < 2:
        return ""

    comment_lines = []

    # 从声明行向上查找注释
    for i in range(line_num - 2, -1, -1):
        line = lines[i].strip()

        # 遇到空行，停止
        if not line:
            break

        # 提取注释内容
        if line.startswith('//'):
            comment_content = line[2:].strip()
            comment_lines.insert(0, comment_content)
        else:
            # 遇到非注释、非空行，停止
            break

    return ' '.join(comment_lines) if comment_lines else ""


def check_comment_ending(comment: str) -> bool:
    """
    检查注释是否以中文标点结束

    Args:
        comment: 注释内容

    Returns:
        是否以中文标点结束
    """
    if not comment:
        return False

    # 中文标点符号
    chinese_punctuations = ['。', '！', '？', '；', '：', '，']

    # 检查最后一个字符
    return comment[-1] in chinese_punctuations


def check_file(file_path: Path, base_dir: Path) -> Dict:
    """
    检查单个文件的注释格式

    Args:
        file_path: 文件路径
        base_dir: 项目根目录

    Returns:
        检查结果字典
    """
    result = {
        "file": str(file_path.relative_to(base_dir)),
        "issues": []
    }

    # 解析文件
    lines, declarations = parse_go_file(file_path)

    if not lines:
        return result

    # 检查每个声明
    for line_num, decl_type, name in declarations:
        # 提取注释
        comment = extract_comment_before(lines, line_num)

        # 检查注释是否存在
        if not comment:
            result["issues"].append({
                "file": str(file_path.relative_to(base_dir)),
                "line": line_num,
                "type": "missing_comment",
                "item": f"{decl_type} {name}",
                "severity": "error",
                "auto_fixable": False
            })
            continue

        # 检查注释是否以中文标点结束
        if not check_comment_ending(comment):
            result["issues"].append({
                "file": str(file_path.relative_to(base_dir)),
                "line": line_num - 1,  # 注释行
                "type": "missing_punctuation",
                "item": f"{decl_type} {name}",
                "current": f"// {comment}",
                "suggested": f"// {comment}。",
                "severity": "warning",
                "auto_fixable": True
            })

    return result


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

    # 收集 Go 文件
    print("🔍 收集 Go 文件...")
    if target_path:
        print(f"   目标路径：{target_path}")

    go_files = collect_go_files(base_dir, target_path)
    print(f"   找到 {len(go_files)} 个 Go 文件")
    print("")

    # 检查每个文件
    print("📋 检查注释格式...")
    all_results = []
    total_files = len(go_files)
    files_with_issues = 0

    for i, file_path in enumerate(go_files, 1):
        # 显示进度
        rel_path = file_path.relative_to(base_dir)
        print(f"   [{i}/{total_files}] {rel_path}", end='\r')

        # 检查文件
        result = check_file(file_path, base_dir)
        if result["issues"]:
            files_with_issues += 1
            all_results.append(result)

    print("")  # 换行

    # 统计
    total_issues = sum(len(r["issues"]) for r in all_results)
    missing_comments = sum(
        sum(1 for issue in r["issues"] if issue["type"] == "missing_comment")
        for r in all_results
    )
    format_issues = sum(
        sum(1 for issue in r["issues"] if issue["type"] == "missing_punctuation")
        for r in all_results
    )

    # 输出结果
    print("")
    print("=" * 50)
    print("📊 检查结果统计")
    print("=" * 50)
    print(f"总文件数：{total_files}")
    print(f"有问题的文件：{files_with_issues}")
    print(f"总问题数：{total_issues}")
    print(f"  - 缺失注释：{missing_comments}")
    print(f"  - 格式问题：{format_issues}")
    print("")

    # 显示有问题的文件
    if all_results:
        print("=" * 50)
        print("📋 问题详情")
        print("=" * 50)
        print("")

        for result in all_results[:10]:  # 只显示前 10 个文件
            print(f"📄 {result['file']}")
            for issue in result['issues'][:3]:  # 每个文件只显示前 3 个问题
                if issue['type'] == 'missing_comment':
                    print(f"   ❌ 行 {issue['line']}：缺少 {issue['item']} 的注释")
                elif issue['type'] == 'missing_punctuation':
                    print(f"   ⚠️  行 {issue['line']}：{issue['item']} 注释未以标点结束")
                    print(f"      当前：{issue['current']}")
                    print(f"      建议：{issue['suggested']}")

            if len(result['issues']) > 3:
                print(f"   ... 还有 {len(result['issues']) - 3} 个问题")
            print("")

        if len(all_results) > 10:
            print(f"... 还有 {len(all_results) - 10} 个文件有问题")
            print("")

    # 输出 JSON 结果
    output = {
        "total_files": total_files,
        "files_with_issues": files_with_issues,
        "issues": [
            issue for result in all_results for issue in result["issues"]
        ]
    }

    output_file = base_dir / ".backup" / "comments" / "format_results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("=" * 50)
    print(f"✅ 结果已保存到：{output_file.relative_to(base_dir)}")
    print("")

    # 返回值
    if missing_comments > 0:
        sys.exit(1)  # 有缺失注释
    else:
        sys.exit(0)  # 无问题或仅有可自动修复的问题


if __name__ == "__main__":
    main()
