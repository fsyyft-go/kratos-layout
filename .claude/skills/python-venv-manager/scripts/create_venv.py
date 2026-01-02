#!/usr/bin/env python3
"""
虚拟环境创建器

创建 .venv 虚拟环境。

用法：
    python3 create_venv.py [python_path]

参数：
    python_path: 可选的 Python 解释器路径（默认使用系统默认的 python3）

示例：
    python3 create_venv.py
    python3 create_venv.py python3.11
"""

import sys
import shutil
import subprocess
from pathlib import Path


def create_venv(python_path=None):
    """
    创建 Python 虚拟环境

    参数:
        python_path: 可选的 Python 解释器路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    # 1. 确定使用的 Python 解释器
    if python_path is None:
        python_cmd = "python3"
    else:
        python_cmd = python_path

    # 2. 验证 Python 可用性
    try:
        result = subprocess.run(
            [python_cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print(f"❌ 错误：无法找到 Python 解释器：{python_cmd}")
            return False

        print(f"📦 使用 Python：{result.stdout.strip()}")
    except Exception as e:
        print(f"❌ 错误：执行 Python 命令失败：{e}")
        return False

    # 3. 检查是否已存在虚拟环境
    venv_dir = Path(".venv")
    if venv_dir.exists():
        print(f"⚠️  警告：.venv 目录已存在")

        # 检查是否在交互式终端中运行
        if sys.stdin.isatty():
            try:
                response = input("是否删除并重新创建？(y/N): ")
                if response.lower() != 'y':
                    print("❌ 取消创建")
                    return False

                print("🗑️  正在删除旧的虚拟环境...")
                shutil.rmtree(".venv")
            except KeyboardInterrupt:
                print("\n❌ 用户取消操作")
                return False
        else:
            # 非交互式模式，直接返回失败
            print("❌ 虚拟环境已存在，无法创建（非交互模式）")
            return False

    # 4. 创建虚拟环境
    print("🔨 正在创建虚拟环境...")
    try:
        result = subprocess.run(
            [python_cmd, "-m", "venv", ".venv"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"❌ 创建失败：{result.stderr}")
            return False

        print("✅ 虚拟环境创建成功：.venv")

        # 5. 显示激活命令提示
        if sys.platform == "win32":
            print("\n📝 激活虚拟环境：")
            print("   .venv\\Scripts\\activate.bat")
        else:
            print("\n📝 激活虚拟环境：")
            print("   source .venv/bin/activate")

        return True

    except subprocess.TimeoutExpired:
        print("❌ 创建超时（超过 60 秒）")
        return False
    except Exception as e:
        print(f"❌ 创建失败：{e}")
        return False


def main():
    """主函数"""
    python_path = sys.argv[1] if len(sys.argv) > 1 else None

    success = create_venv(python_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
