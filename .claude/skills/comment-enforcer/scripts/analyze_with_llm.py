#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 代码注释语义分析器（大模型）
==========================

功能：
  1. 检查 interface 实现方法的注释是否与接口定义一致
  2. 判断注释是否准确反映代码功能
  3. 识别需要改进的注释（过于简略、不准确）
  4. 为缺失的注释生成符合规范的内容

使用方式：
  python3 analyze_with_llm.py [文件路径] [选项]

选项：
  --check-interface-only  只检查 interface 一致性
  --generate-only         只生成缺失注释
  --no-missing            不检查缺失注释

返回值：
  0 - 分析成功
  1 - 分析失败

自动化程度：
  - 代码分析：100% 大模型
  - 报告生成：脚本格式化输出
"""

import sys
import os
import json
import re
import platform
from pathlib import Path
from typing import Dict, List, Optional

try:
    import anthropic
except ImportError:
    print("❌ 缺少 anthropic 包，请安装：pip install anthropic")
    sys.exit(2)


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

    # 脚本在 .claude/skills/comment-enforcer/scripts/analyze_with_llm.py
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
    收集需要分析的 Go 文件

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
        # 检查整个项目
        go_files = []
        for pattern in ["*.go"]:
            go_files.extend([
                f for f in base_dir.rglob(pattern)
                if ".backup" not in str(f) and "vendor" not in str(f)
            ])
        return go_files


def extract_code_snippet(file_path: Path, base_dir: Path) -> str:
    """
    提取代码片段用于大模型分析

    Args:
        file_path: 文件路径
        base_dir: 项目根目录

    Returns:
        代码片段字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"无法读取文件：{e}"

    return content


def analyze_with_llm(code_snippet: str, file_path: str, analysis_type: str = "full") -> Dict:
    """
    使用大模型分析代码注释

    Args:
        code_snippet: 代码片段
        file_path: 文件路径（用于提示）
        analysis_type: 分析类型（full, interface_only, generate_only）

    Returns:
        分析结果字典
    """
    # 获取 API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "error": "未设置 ANTHROPIC_API_KEY 环境变量",
            "suggestion": "请设置环境变量：export ANTHROPIC_API_KEY=your_key"
        }

    # 构建提示词
    if analysis_type == "full":
        prompt = f"""请分析以下 Go 代码文件的注释是否符合规范：

文件路径：{file_path}

代码：
```go
{code_snippet}
```

注释规范：
1. 每个类型（type）必须有功能说明注释
2. 每个函数/方法必须描述功能、参数、返回值
3. 实现接口的方法注释必须与接口定义完全一致
4. 注释必须准确反映代码功能
5. 注释必须以中文标点符号结束
6. 使用标准术语表述

请检查：
1. 是否有缺失的注释？
2. 注释是否准确？
3. interface 实现是否一致？
4. 需要如何改进？

请以 JSON 格式输出结果，格式如下：
{{
  "semantic_issues": [
    {{
      "line": 行号,
      "type": "inaccurate_comment",
      "current": "当前注释",
      "issue": "问题描述",
      "suggested": "建议修改",
      "reason": "理由"
    }}
  ],
  "interface_mismatches": [
    {{
      "line": 行号,
      "interface_def": "接口定义注释",
      "implementation": "实现注释",
      "suggested": "建议统一"
    }}
  ],
  "missing_comments": [
    {{
      "line": 行号,
      "type": "type_definition|function|method|field",
      "name": "名称",
      "suggested": "建议注释"
    }}
  ]
}}

如果没有发现问题，请返回空数组。"""

    elif analysis_type == "interface_only":
        prompt = f"""请检查以下 Go 代码中 interface 实现的注释是否与接口定义一致：

文件路径：{file_path}

代码：
```go
{code_snippet}
```

请以 JSON 格式输出不一致的地方：
{{
  "interface_mismatches": [
    {{
      "line": 行号,
      "interface_def": "接口定义注释",
      "implementation": "实现注释",
      "suggested": "建议统一"
    }}
  ]
}}"""

    elif analysis_type == "generate_only":
        prompt = f"""请为以下 Go 代码中缺失的注释生成符合规范的内容：

文件路径：{file_path}

代码：
```go
{code_snippet}
```

注释规范：
1. 类型注释：描述类型的功能
2. 函数/方法注释：描述功能、参数、返回值
3. 参数注释：使用标准术语表述
4. 以中文标点结束

请以 JSON 格式输出建议的注释：
{{
  "missing_comments": [
    {{
      "line": 行号,
      "type": "type_definition|function|method|field",
      "name": "名称",
      "suggested": "建议注释"
    }}
  ]
}}"""

    # 调用 Anthropic API
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # 提取响应内容
        response_text = message.content[0].text

        # 尝试解析 JSON
        # 移除可能的 markdown 代码块标记
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            # 如果无法解析 JSON，返回原始响应
            return {
                "error": "无法解析大模型响应为 JSON",
                "raw_response": response_text
            }

    except Exception as e:
        return {
            "error": f"调用大模型 API 失败：{e}",
            "suggestion": "请检查 API key 和网络连接"
        }


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 获取项目根目录
    base_dir = find_project_root()
    print(f"📁 项目根目录：{base_dir}")
    print("")

    # 解析命令行参数
    target_path = None
    analysis_type = "full"
    check_missing = True

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--check-interface-only":
            analysis_type = "interface_only"
        elif arg == "--generate-only":
            analysis_type = "generate_only"
        elif arg == "--no-missing":
            check_missing = False
        elif not arg.startswith("--"):
            target_path = arg
        i += 1

    # 收集 Go 文件
    print("🔍 收集 Go 文件...")
    if target_path:
        print(f"   目标路径：{target_path}")

    go_files = collect_go_files(base_dir, target_path)
    print(f"   找到 {len(go_files)} 个 Go 文件")
    print("")

    # 分析每个文件
    print("🤖 使用大模型分析...")
    print("")

    all_results = {
        "analyzed_files": 0,
        "semantic_issues": [],
        "interface_mismatches": [],
        "missing_comments": []
    }

    for i, file_path in enumerate(go_files, 1):
        # 显示进度
        rel_path = file_path.relative_to(base_dir)
        print(f"   [{i}/{len(go_files)}] {rel_path}", end='\r')

        # 提取代码片段
        code_snippet = extract_code_snippet(file_path, base_dir)

        # 限制代码长度（避免超过 API 限制）
        if len(code_snippet) > 10000:  # 限制为 10k 字符
            code_snippet = code_snippet[:10000] + "\n\n... (代码已截断)"

        # 调用大模型分析
        result = analyze_with_llm(code_snippet, str(rel_path), analysis_type)

        if "error" in result:
            print(f"\n⚠️  {rel_path}: {result['error']}")
            continue

        all_results["analyzed_files"] += 1

        # 整合结果
        if "semantic_issues" in result:
            for issue in result["semantic_issues"]:
                issue["file"] = str(rel_path)
                all_results["semantic_issues"].append(issue)

        if "interface_mismatches" in result:
            for mismatch in result["interface_mismatches"]:
                mismatch["file"] = str(rel_path)
                all_results["interface_mismatches"].append(mismatch)

        if check_missing and "missing_comments" in result:
            for missing in result["missing_comments"]:
                missing["file"] = str(rel_path)
                all_results["missing_comments"].append(missing)

    print("")  # 换行

    # 输出结果
    print("")
    print("=" * 50)
    print("📊 分析结果统计")
    print("=" * 50)
    print(f"分析文件数：{all_results['analyzed_files']}")
    print(f"语义问题：{len(all_results['semantic_issues'])} 个")
    print(f"Interface 不一致：{len(all_results['interface_mismatches'])} 个")
    print(f"缺失注释：{len(all_results['missing_comments'])} 个")
    print("")

    # 显示详细问题
    if all_results["semantic_issues"]:
        print("=" * 50)
        print("📋 语义问题")
        print("=" * 50)
        print("")

        for issue in all_results["semantic_issues"][:5]:
            print(f"📄 {issue['file']}:{issue.get('line', '?')}")
            print(f"   当前：{issue.get('current', '无')}")
            print(f"   问题：{issue.get('issue', '未知')}")
            print(f"   建议：{issue.get('suggested', '无')}")
            print("")

        if len(all_results["semantic_issues"]) > 5:
            print(f"... 还有 {len(all_results['semantic_issues']) - 5} 个语义问题")
            print("")

    if all_results["interface_mismatches"]:
        print("=" * 50)
        print("📋 Interface 不一致")
        print("=" * 50)
        print("")

        for mismatch in all_results["interface_mismatches"][:5]:
            print(f"📄 {mismatch['file']}:{mismatch.get('line', '?')}")
            print(f"   接口定义：{mismatch.get('interface_def', '无')}")
            print(f"   实现：{mismatch.get('implementation', '无')}")
            print(f"   建议：{mismatch.get('suggested', '无')}")
            print("")

        if len(all_results["interface_mismatches"]) > 5:
            print(f"... 还有 {len(all_results['interface_mismatches']) - 5} 个不一致")
            print("")

    if check_missing and all_results["missing_comments"]:
        print("=" * 50)
        print("📋 缺失注释")
        print("=" * 50)
        print("")

        for missing in all_results["missing_comments"][:5]:
            print(f"📄 {missing['file']}:{missing.get('line', '?')}")
            print(f"   {missing.get('type', '未知')}: {missing.get('name', '')}")
            print(f"   建议：{missing.get('suggested', '无')}")
            print("")

        if len(all_results["missing_comments"]) > 5:
            print(f"... 还有 {len(all_results['missing_comments']) - 5} 个缺失注释")
            print("")

    # 输出 JSON 结果
    output_file = base_dir / ".backup" / "comments" / "llm_results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("=" * 50)
    print(f"✅ 结果已保存到：{output_file.relative_to(base_dir)}")
    print("")

    sys.exit(0)


if __name__ == "__main__":
    main()
