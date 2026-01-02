#!/usr/bin/env python3
"""
Git 忽略规则更新器

更新 .gitignore 文件，确保 .venv 虚拟环境被忽略。

用法：
    python3 update_gitignore.py
"""

import sys
from pathlib import Path


def update_gitignore():
    """
    更新 .gitignore 文件，添加 .venv 规则

    返回:
        bool: 成功返回 True，失败返回 False
    """
    gitignore_path = Path(".gitignore")

    # .venv 忽略规则
    venv_rule = ".venv/"
    venv_section = "\n# Python 虚拟环境\n.venv/\n"

    # 1. 如果 .gitignore 不存在，创建它
    if not gitignore_path.exists():
        try:
            gitignore_path.write_text(f"# Python 虚拟环境\n{venv_rule}\n", encoding='utf-8')
            print("✅ 已创建 .gitignore 并添加 .venv/")
            return True
        except Exception as e:
            print(f"❌ 创建 .gitignore 失败：{e}")
            return False

    # 2. 读取现有 .gitignore
    try:
        content = gitignore_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ 读取 .gitignore 失败：{e}")
        return False

    # 3. 检查是否已包含 .venv 规则
    if venv_rule in content or ".venv" in content:
        print("ℹ️  .gitignore 已包含 .venv 规则")
        return True

    # 4. 添加 .venv 规则
    try:
        # 确保文件以换行符结尾
        if not content.endswith('\n'):
            content += '\n'

        # 添加 .venv 规则
        content += venv_section

        gitignore_path.write_text(content, encoding='utf-8')
        print("✅ 已更新 .gitignore，添加 .venv/")
        return True

    except Exception as e:
        print(f"❌ 更新 .gitignore 失败：{e}")
        return False


def main():
    """主函数"""
    success = update_gitignore()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
