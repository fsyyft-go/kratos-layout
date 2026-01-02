#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 代码注释检查报告生成器
==========================

功能：
  1. 整合所有检查结果
  2. 生成结构化的 Markdown 报告
  3. 提供符合规范的解决方案
  4. 汇总统计信息

使用方式：
  python3 generate_report.py [--output 报告文件]

返回值：
  0 - 成功
  1 - 失败

自动化程度：100% 脚本自动化
"""

import sys
import os
import json
import platform
from pathlib import Path
from datetime import datetime


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

    # 脚本在 .claude/skills/comment-enforcer/scripts/generate_report.py
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


def load_json_results(base_dir: Path) -> Dict:
    """
    加载所有检查结果

    Args:
        base_dir: 项目根目录

    Returns:
        检查结果字典
    """
    backup_dir = base_dir / ".backup" / "comments"

    results = {
        "format": None,
        "terminology": None,
        "pkg": None,
        "llm": None
    }

    # 加载格式检查结果
    format_file = backup_dir / "format_results.json"
    if format_file.exists():
        try:
            with open(format_file, 'r', encoding='utf-8') as f:
                results["format"] = json.load(f)
        except Exception as e:
            print(f"⚠️  无法加载格式检查结果：{e}")

    # 加载术语检查结果
    terminology_file = backup_dir / "terminology_results.json"
    if terminology_file.exists():
        try:
            with open(terminology_file, 'r', encoding='utf-8') as f:
                results["terminology"] = json.load(f)
        except Exception as e:
            print(f"⚠️  无法加载术语检查结果：{e}")

    # 加载包级别注释检查结果
    pkg_file = backup_dir / "pkg_results.json"
    if pkg_file.exists():
        try:
            with open(pkg_file, 'r', encoding='utf-8') as f:
                results["pkg"] = json.load(f)
        except Exception as e:
            print(f"⚠️  无法加载包注释检查结果：{e}")

    # 加载大模型分析结果
    llm_file = backup_dir / "llm_results.json"
    if llm_file.exists():
        try:
            with open(llm_file, 'r', encoding='utf-8') as f:
                results["llm"] = json.load(f)
        except Exception as e:
            print(f"⚠️  无法加载大模型分析结果：{e}")

    return results


def generate_markdown_report(results: Dict, base_dir: Path) -> str:
    """
    生成 Markdown 格式的报告

    Args:
        results: 检查结果字典
        base_dir: 项目根目录

    Returns:
        Markdown 报告字符串
    """
    report_lines = []

    # 标题
    report_lines.append("# 注释规范检查报告")
    report_lines.append("")
    report_lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"项目根目录：{base_dir}")
    report_lines.append("")

    # 总览
    report_lines.append("## 📊 总览")
    report_lines.append("")

    format_results = results.get("format", {})
    terminology_results = results.get("terminology", {})
    pkg_results = results.get("pkg", {})
    llm_results = results.get("llm", {})

    total_files = format_results.get("total_files", 0) if format_results else 0
    files_with_issues = format_results.get("files_with_issues", 0) if format_results else 0

    format_issues_count = len(format_results.get("issues", [])) if format_results else 0
    terminology_inconsistent_count = terminology_results.get("total_inconsistent", 0) if terminology_results else 0
    pkg_missing_count = len(pkg_results.get("packages_missing_doc", [])) if pkg_results else 0
    pkg_files_with_comment_count = len(pkg_results.get("files_with_pkg_comment", [])) if pkg_results else 0
    semantic_issues_count = len(llm_results.get("semantic_issues", [])) if llm_results else 0
    interface_mismatches_count = len(llm_results.get("interface_mismatches", [])) if llm_results else 0
    missing_comments_count = len(llm_results.get("missing_comments", [])) if llm_results else 0

    total_issues = (
        format_issues_count +
        terminology_inconsistent_count +
        pkg_missing_count +
        pkg_files_with_comment_count +
        semantic_issues_count +
        interface_mismatches_count +
        missing_comments_count
    )

    report_lines.append(f"- 检查文件数：{total_files}")
    report_lines.append(f"- 发现问题：{total_issues} 个")
    report_lines.append(f"  - 格式问题：{format_issues_count} 个")
    report_lines.append(f"  - 术语一致性问题：{terminology_inconsistent_count} 个")
    report_lines.append(f"  - 包注释问题：{pkg_missing_count + pkg_files_with_comment_count} 个")
    report_lines.append(f"  - 语义问题：{semantic_issues_count} 个")
    report_lines.append(f"  - Interface 不一致：{interface_mismatches_count} 个")
    report_lines.append(f"  - 缺失注释：{missing_comments_count} 个")
    report_lines.append("")

    # 格式问题
    if format_results and format_results.get("issues"):
        report_lines.append("## 1️⃣ 格式问题（脚本检查 - 可自动修复）")
        report_lines.append("")

        # 按类型分组
        format_issues_by_type = {}
        for issue in format_results["issues"]:
            issue_type = issue["type"]
            if issue_type not in format_issues_by_type:
                format_issues_by_type[issue_type] = []
            format_issues_by_type[issue_type].append(issue)

        for issue_type, issues in format_issues_by_type.items():
            if issue_type == "missing_punctuation":
                report_lines.append("### 1.1 注释未以标点结束")
                report_lines.append("")

                for issue in issues[:10]:
                    report_lines.append(f"- [ ] {issue['file']}:{issue['line']}")
                    report_lines.append(f"  当前：{issue['current']}")
                    report_lines.append(f"  建议：{issue['suggested']}")
                    report_lines.append("")

                if len(issues) > 10:
                    report_lines.append(f"... 还有 {len(issues) - 10} 个格式问题")
                    report_lines.append("")

            elif issue_type == "missing_comment":
                report_lines.append("### 1.2 缺少注释")
                report_lines.append("")

                for issue in issues[:10]:
                    report_lines.append(f"- [ ] {issue['file']}:{issue['line']}")
                    report_lines.append(f"  缺少 {issue['item']} 的注释")
                    report_lines.append("")

                if len(issues) > 10:
                    report_lines.append(f"... 还有 {len(issues) - 10} 个缺失注释")
                    report_lines.append("")

    # 术语一致性问题
    if terminology_results and terminology_results.get("results"):
        report_lines.append("## 2️⃣ 术语一致性问题（脚本检查 - 需手动确认）")
        report_lines.append("")

        for type_name, result in terminology_results["results"].items():
            report_lines.append(f"### 2.{type_name.replace('.', '-')} {type_name} 注释不一致")
            report_lines.append("")

            report_lines.append(f"标准表述：{result['standard']}")
            report_lines.append("")

            for variation in result['variations']:
                report_lines.append(f"- [ ] 出现 {variation['count']} 次：\"{variation['text']}\"")
                report_lines.append(f"  影响：")
                for file_ref in variation['files'][:3]:
                    report_lines.append(f"    • {file_ref}")
                if len(variation['files']) > 3:
                    report_lines.append(f"    ... 还有 {len(variation['files']) - 3} 处")
                report_lines.append("")

    # 包级别注释问题
    if pkg_results:
        report_lines.append("## 3️⃣ 包级别注释问题（脚本检查）")
        report_lines.append("")

        if pkg_results.get("packages_missing_doc"):
            report_lines.append("### 3.1 缺少 doc.go 文件")
            report_lines.append("")

            for pkg in pkg_results["packages_missing_doc"][:10]:
                pkg_name = Path(pkg['package']).name
                report_lines.append(f"- [ ] {pkg['package']}")
                report_lines.append(f"  建议：创建 {pkg['suggestion']}")
                report_lines.append("")
                report_lines.append("  ```go")
                report_lines.append("  // Copyright 2025 fsyyft-go")
                report_lines.append("  //")
                report_lines.append("  // Licensed under the MIT License.")
                report_lines.append("  //")
                report_lines.append(f"  // Package {pkg_name} 提供功能实现。")
                report_lines.append(f"  package {pkg_name}")
                report_lines.append("  ```")
                report_lines.append("")

            if len(pkg_results["packages_missing_doc"]) > 10:
                report_lines.append(f"... 还有 {len(pkg_results['packages_missing_doc']) - 10} 个包缺少 doc.go")
                report_lines.append("")

        if pkg_results.get("files_with_pkg_comment"):
            report_lines.append("### 3.2 包级别注释在非 doc.go 文件中")
            report_lines.append("")

            for file_info in pkg_results["files_with_pkg_comment"][:10]:
                report_lines.append(f"- [ ] {file_info['file']}:{file_info['line']}")
                report_lines.append(f"  注释：{file_info['comment']}")
                report_lines.append(f"  建议：移动到 doc.go 文件")
                report_lines.append("")

            if len(pkg_results["files_with_pkg_comment"]) > 10:
                report_lines.append(f"... 还有 {len(pkg_results['files_with_pkg_comment']) - 10} 个文件")
                report_lines.append("")

    # 语义问题
    if llm_results and llm_results.get("semantic_issues"):
        report_lines.append("## 4️⃣ 语义问题（大模型分析 - 需专业判断）")
        report_lines.append("")

        for issue in llm_results["semantic_issues"][:10]:
            report_lines.append(f"- [ ] {issue['file']}:{issue.get('line', '?')}")
            report_lines.append(f"  当前注释：{issue.get('current', '无')}")
            report_lines.append(f"  问题：{issue.get('issue', '未知')}")
            report_lines.append(f"  建议：{issue.get('suggested', '无')}")
            if 'reason' in issue:
                report_lines.append(f"  理由：{issue['reason']}")
            report_lines.append("")

        if len(llm_results["semantic_issues"]) > 10:
            report_lines.append(f"... 还有 {len(llm_results['semantic_issues']) - 10} 个语义问题")
            report_lines.append("")

    # Interface 不一致
    if llm_results and llm_results.get("interface_mismatches"):
        report_lines.append("## 5️⃣ Interface 不一致（大模型分析 - 需专业判断）")
        report_lines.append("")

        for mismatch in llm_results["interface_mismatches"][:10]:
            report_lines.append(f"- [ ] {mismatch['file']}:{mismatch.get('line', '?')}")
            report_lines.append(f"  接口定义：{mismatch.get('interface_def', '无')}")
            report_lines.append(f"  实现：{mismatch.get('implementation', '无')}")
            report_lines.append(f"  建议：{mismatch.get('suggested', '无')}")
            report_lines.append("")

        if len(llm_results["interface_mismatches"]) > 10:
            report_lines.append(f"... 还有 {len(llm_results['interface_mismatches']) - 10} 个不一致")
            report_lines.append("")

    # 缺失注释
    if llm_results and llm_results.get("missing_comments"):
        report_lines.append("## 6️⃣ 缺失注释（大模型生成 - 需确认）")
        report_lines.append("")

        for missing in llm_results["missing_comments"][:10]:
            report_lines.append(f"- [ ] {missing['file']}:{missing.get('line', '?')}")
            report_lines.append(f"  {missing.get('type', '未知')}: {missing.get('name', '')}")
            report_lines.append(f"  建议：{missing.get('suggested', '无')}")
            report_lines.append("")

        if len(llm_results["missing_comments"]) > 10:
            report_lines.append(f"... 还有 {len(llm_results['missing_comments']) - 10} 个缺失注释")
            report_lines.append("")

    # 下一步操作
    report_lines.append("## ✅ 下一步操作")
    report_lines.append("")

    auto_fixable = format_issues_count
    need_confirm = (
        terminology_inconsistent_count +
        pkg_missing_count +
        pkg_files_with_comment_count +
        semantic_issues_count +
        interface_mismatches_count +
        missing_comments_count
    )

    if auto_fixable > 0:
        report_lines.append(f"### 自动修复（脚本）")
        report_lines.append(f"- 格式问题：{auto_fixable} 个可自动修复")
        report_lines.append("")

    if need_confirm > 0:
        report_lines.append(f"### 需要确认（列出清单）")
        report_lines.append(f"- 术语一致性问题：{terminology_inconsistent_count} 个")
        report_lines.append(f"- 包注释问题：{pkg_missing_count + pkg_files_with_comment_count} 个")
        report_lines.append(f"- 语义问题：{semantic_issues_count} 个")
        report_lines.append(f"- Interface 不一致：{interface_mismatches_count} 个")
        report_lines.append(f"- 缺失注释：{missing_comments_count} 个")
        report_lines.append("")

    report_lines.append("请勾选需要修复的问题后，运行：")
    report_lines.append("```bash")
    report_lines.append("python3 .claude/skills/comment-enforcer/scripts/fix_comment.py report.md")
    report_lines.append("```")
    report_lines.append("")

    return '\n'.join(report_lines)


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 获取项目根目录
    base_dir = find_project_root()
    print(f"📁 项目根目录：{base_dir}")
    print("")

    # 解析命令行参数
    output_file = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]

    # 加载检查结果
    print("🔍 加载检查结果...")
    results = load_json_results(base_dir)

    loaded_count = sum(1 for r in results.values() if r is not None)
    print(f"   加载了 {loaded_count} 个结果文件")
    print("")

    if loaded_count == 0:
        print("❌ 未找到任何检查结果，请先运行检查脚本")
        print("   建议：")
        print("   1. python3 .claude/skills/comment-enforcer/scripts/check_format.py")
        print("   2. python3 .claude/skills/comment-enforcer/scripts/check_terminology.py")
        print("   3. python3 .claude/skills/comment-enforcer/scripts/check_pkg_doc.py")
        print("   4. python3 .claude/skills/comment-enforcer/scripts/analyze_with_llm.py")
        sys.exit(1)

    # 生成报告
    print("📝 生成报告...")
    report_content = generate_markdown_report(results, base_dir)

    # 保存报告
    if not output_file:
        output_file = base_dir / "comment-report.md"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"✅ 报告已生成：{output_path.relative_to(base_dir) if output_path.is_relative_to(base_dir) else output_path}")
    print("")

    sys.exit(0)


if __name__ == "__main__":
    main()
