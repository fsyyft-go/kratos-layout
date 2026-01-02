#!/usr/bin/env python3
"""
依赖安装器

安装 requirements.txt 中的依赖到虚拟环境。

用法：
    python3 install_deps.py
"""

import sys
import platform
import subprocess
from pathlib import Path


def install_deps():
    """
    安装依赖到虚拟环境

    返回:
        bool: 成功返回 True，失败返回 False
    """
    # 1. 检查虚拟环境是否存在
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        print("❌ 错误：虚拟环境不存在：.venv")
        print("   请先运行：python3 create_venv.py")
        return False

    # 2. 检查 requirements.txt 是否存在
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ 错误：requirements.txt 不存在")
        print("   请先运行：python3 generate_requirements.py")
        return False

    # 3. 确定 pip 路径（跨平台）
    if platform.system() == "Windows":
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        pip_exe = venv_dir / "bin" / "pip"

    if not pip_exe.exists():
        print(f"❌ 错误：找不到 pip：{pip_exe}")
        print("   虚拟环境可能损坏")
        return False

    # 4. 升级 pip
    print("🔄 正在升级 pip...")
    try:
        result = subprocess.run(
            [str(pip_exe), "install", "--upgrade", "pip"],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print("✅ pip 升级成功")
        else:
            print("⚠️  pip 升级失败（将继续安装依赖）")

    except subprocess.TimeoutExpired:
        print("⚠️  pip 升级超时（将继续安装依赖）")
    except Exception as e:
        print(f"⚠️  pip 升级失败：{e}（将继续安装依赖）")

    # 5. 安装依赖
    print("📦 正在安装依赖...")
    print("   这可能需要几分钟时间...")

    try:
        result = subprocess.run(
            [str(pip_exe), "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            timeout=600  # 10 分钟超时
        )

        if result.returncode != 0:
            print("❌ 安装失败，部分包可能未安装")
            print("\n错误输出：")
            print(result.stderr)
            return False

        print("✅ 依赖安装成功")

    except subprocess.TimeoutExpired:
        print("❌ 安装超时（超过 10 分钟）")
        print("   请检查网络连接或尝试手动安装：")
        print(f"   {pip_exe} install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ 安装失败：{e}")
        return False

    # 6. 显示已安装的包列表
    print("\n📋 已安装的包：")
    try:
        result = subprocess.run(
            [str(pip_exe), "list"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            # 只显示包名和版本，格式化输出
            lines = result.stdout.strip().split('\n')
            for line in lines[2:]:  # 跳过前两行标题
                print(f"   {line}")

    except Exception as e:
        print(f"   ⚠️  无法获取包列表：{e}")

    return True


def main():
    """主函数"""
    success = install_deps()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
