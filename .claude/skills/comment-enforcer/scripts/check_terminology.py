#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 代码术语一致性检查器
==========================

功能：
  1. 全局搜索特定类型（如 context.Context）
  2. 提取所有相关注释
  3. 比对注释表述是否一致
  4. 报告不一致的地方

使用方式：
  python3 check_terminology.py [--type 类型] [--standard 标准表述]

返回值：
  0 - 无不一致
  1 - 发现有不一致
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
from collections import defaultdict


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

    # 脚本在 .claude/skills/comment-enforcer/scripts/check_terminology.py
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


# 标准术语映射表（从 .ai/rule.md.bak 提取）
STANDARD_TERMINOLOGY = {
    "context.Context": "请求上下文，用于取消与超时控制。",
    "*Config": "应用配置信息。",
    "Config": "应用配置信息。",
    "Logger": "日志记录器。",
    "*Data": "数据仓储接口。",
    "Data": "数据仓储接口。",
    "*Greeter": "Greeter 实体。",
    "Greeter": "Greeter 实体。",
}


def collect_go_files(base_dir: Path) -> List[Path]:
    """
    收集所有 Go 文件

    Args:
        base_dir: 项目根目录

    Returns:
        Go 文件路径列表
    """
    go_files = []
    for pattern in ["*.go"]:
        go_files.extend([
            f for f in base_dir.rglob(pattern)
            if ".backup" not in str(f) and "vendor" not in str(f)
        ])
    return go_files


def extract_param_comments(file_path: Path) -> List[Dict]:
    """
    提取文件中所有参数的注释

    Args:
        file_path: Go 文件路径

    Returns:
        参数注释列表
        格式：{"file": 文件路径, "line": 行号, "param": 参数名, "type": 类型, "comment": 注释}
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"⚠️  无法读取文件 {file_path}：{e}")
        return []

    param_comments = []

    # 正则模式：匹配函数声明中的参数
    func_param_pattern = re.compile(
        r'(\w+)\s+(' + '|'.join(re.escape(k) for k in STANDARD_TERMINOLOGY.keys()) + r')\b'
    )

    for line_num, line in enumerate(lines, 1):
        # 查找参数声明
        matches = func_param_pattern.finditer(line)

        for match in matches:
            param_name = match.group(1)
            param_type = match.group(2)

            # 向上查找注释
            comment = extract_comment_before(lines, line_num, param_name)

            param_comments.append({
                "file": str(file_path),
                "line": line_num,
                "param": param_name,
                "type": param_type,
                "comment": comment
            })

    return param_comments


def extract_comment_before(lines: List[str], line_num: int, param_name: str) -> str:
    """
    提取参数前的注释

    Args:
        lines: 代码行列表
        line_num: 声明行号（从 1 开始）
        param_name: 参数名

    Returns:
        注释内容（不包含 // 符号）
    """
    if line_num < 2:
        return ""

    comment_lines = []

    # 从参数行向上查找注释（最多 5 行）
    for i in range(line_num - 2, max(0, line_num - 7), -1):
        line = lines[i].strip()

        # 遇到空行，停止
        if not line:
            break

        # 提取注释内容
        if line.startswith('//'):
            # 检查是否包含参数名
            if param_name in line or len(comment_lines) > 0:
                comment_content = line[2:].strip()
                # 移除参数名前缀（如 "ctx："）
                comment_content = re.sub(r'^' + re.escape(param_name) + r'\s*[:：]\s*', '', comment_content)
                comment_lines.insert(0, comment_content)
        else:
            # 遇到非注释、非空行，停止
            break

    return ' '.join(comment_lines) if comment_lines else ""


def check_terminology_consistency(base_dir: Path) -> Dict:
    """
    检查术语一致性

    Args:
        base_dir: 项目根目录

    Returns:
        检查结果字典
    """
    # 收集所有 Go 文件
    go_files = collect_go_files(base_dir)

    # 提取所有参数注释
    all_param_comments = []
    for file_path in go_files:
        param_comments = extract_param_comments(file_path)
        all_param_comments.extend(param_comments)

    # 按类型分组
    by_type = defaultdict(list)
    for pc in all_param_comments:
        by_type[pc["type"]].append(pc)

    # 检查每个类型的一致性
    results = {}

    for type_name, param_list in by_type.items():
        standard = STANDARD_TERMINOLOGY.get(type_name, "")

        # 统计不同的注释
        comment_groups = defaultdict(list)
        for pc in param_list:
            comment = pc["comment"]
            if comment:
                comment_groups[comment].append(pc)

        # 找出不一致的
        if len(comment_groups) > 1:
            # 有不一致
            variations = []

            for comment, pcs in comment_groups.items():
                if comment != standard:
                    variations.append({
                        "text": comment,
                        "count": len(pcs),
                        "files": [
                            f"{Path(pc['file']).relative_to(base_dir)}:{pc['line']}"
                            for pc in pcs[:5]  # 最多显示 5 个
                        ]
                    })

            results[type_name] = {
                "standard": standard,
                "variations": variations,
                "total_inconsistent": sum(v["count"] for v in variations)
            }

    return results


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 获取项目根目录
    base_dir = find_project_root()
    print(f"📁 项目根目录：{base_dir}")
    print("")

    # 解析命令行参数
    check_type = None
    custom_standard = None

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--type" and i + 1 < len(sys.argv):
            check_type = sys.argv[i + 1]
        elif arg == "--standard" and i + 1 < len(sys.argv):
            custom_standard = sys.argv[i + 1]

    if check_type and custom_standard:
        STANDARD_TERMINOLOGY[check_type] = custom_standard

    # 执行检查
    print("🔍 检查术语一致性...")
    print("")

    if check_type:
        print(f"   检查类型：{check_type}")
        if check_type in STANDARD_TERMINOLOGY:
            print(f"   标准表述：{STANDARD_TERMINOLOGY[check_type]}")
    else:
        print("   检查类型：")
        for type_name in STANDARD_TERMINOLOGY.keys():
            print(f"   - {type_name}: {STANDARD_TERMINOLOGY[type_name]}")

    print("")

    results = check_terminology_consistency(base_dir)

    # 输出结果
    if not results:
        print("=" * 50)
        print("✅ 未发现术语不一致！")
        print("=" * 50)
        print("")
        exit_code = 0
    else:
        print("=" * 50)
        print("📋 术语不一致报告")
        print("=" * 50)
        print("")

        total_inconsistent = 0

        for type_name, result in results.items():
            print(f"❌ {type_name}")
            print(f"   标准表述：{result['standard']}")
            print(f"   发现 {len(result['variations'])} 种不同表述：")
            print("")

            for variation in result['variations']:
                print(f"   - \"{variation['text']}\"")
                print(f"     出现 {variation['count']} 次")
                print(f"     位置：")
                for file_ref in variation['files'][:3]:
                    print(f"       • {file_ref}")
                if len(variation['files']) > 3:
                    print(f"       ... 还有 {len(variation['files']) - 3} 处")
                print("")

            total_inconsistent += result['total_inconsistent']

        print("=" * 50)
        print(f"总计：{total_inconsistent} 处不一致")
        print("=" * 50)
        print("")

        exit_code = 1

    # 输出 JSON 结果
    output = {
        "checked_types": list(STANDARD_TERMINOLOGY.keys()) if not check_type else [check_type],
        "results": results,
        "total_inconsistent": sum(r.get("total_inconsistent", 0) for r in results.values())
    }

    output_file = base_dir / ".backup" / "comments" / "terminology_results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ 结果已保存到：{output_file.relative_to(base_dir)}")
    print("")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
