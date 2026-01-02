#!/usr/bin/env python3
"""
虚拟环境检查器

检查项目根目录是否存在 .venv 虚拟环境，并验证其有效性。

返回值：
    0 - 虚拟环境存在且有效
    1 - 虚拟环境不存在
    2 - 虚拟环境存在但无效（缺少关键文件）

用法：
    python3 check_venv.py
"""

import sys
import platform
import subprocess
from pathlib import Path


def check_venv():
    """
    检查虚拟环境状态

    返回:
        int: 状态码（0=有效, 1=不存在, 2=无效）
    """
    # 1. 检查 .venv 目录是否存在
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        print("ℹ️  虚拟环境不存在：.venv")
        return 1

    # 2. 验证虚拟环境有效性（跨平台）
    if platform.system() == "Windows":
        activate_script = venv_dir / "Scripts" / "activate.bat"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        activate_script = venv_dir / "bin" / "activate"
        python_exe = venv_dir / "bin" / "python"

    # 3. 检查关键文件是否存在
    if not activate_script.exists():
        print(f"❌ 虚拟环境无效：缺少激活脚本 {activate_script}")
        return 2

    if not python_exe.exists():
        print(f"❌ 虚拟环境无效：缺少 Python 解释器 {python_exe}")
        return 2

    # 4. 报告详细信息
    print(f"✅ 虚拟环境存在：.venv")
    print(f"   Python 路径：{python_exe.absolute()}")

    # 5. 尝试获取虚拟环境的 Python 版本
    try:
        result = subprocess.run(
            [str(python_exe), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   Python 版本：{version}")
    except Exception as e:
        print(f"   ⚠️  警告：无法获取 Python 版本：{e}")

    # 6. 检查 pip 是否可用
    try:
        if platform.system() == "Windows":
            pip_exe = venv_dir / "Scripts" / "pip.exe"
        else:
            pip_exe = venv_dir / "bin" / "pip"

        if pip_exe.exists():
            print(f"   Pip 可用：是")
        else:
            print(f"   ⚠️  警告：pip 不可用")
    except Exception:
        pass

    return 0


def main():
    """主函数"""
    status = check_venv()
    sys.exit(status)


if __name__ == "__main__":
    main()
