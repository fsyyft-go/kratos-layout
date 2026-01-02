#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Go 模块重命名执行器（核心）
==========================

功能：
  1. 创建备份
  2. 执行文本替换（根据类型选择策略）
  3. 清理模板注释
  4. 生成操作报告

使用方式：
  python3 perform_rename.py <旧模块名> <新模块名> [--type=full|partial] [--dry-run]

返回值：
  0 - 成功
  1 - 参数错误
  2 - 备份失败
  3 - 替换失败

自动化程度：90% 脚本自动化 + 10% 大模型介入
"""

import sys
import os
import json
import shutil
import re
import argparse
import platform
from pathlib import Path
from datetime import datetime


def find_project_root():
    """
    自动定位项目根目录（包含 go.mod 的目录）

    策略：
    1. 从脚本自身位置向上查找
    2. 如果脚本在 .claude/skills/go-module-renamer/scripts/，向上 5 级
    3. 验证 go.mod 是否存在
    4. 如果不存在，尝试当前工作目录

    Returns:
        Path: 项目根目录的绝对路径
    """
    # 获取脚本自身的绝对路径
    script_path = Path(__file__).resolve()

    # 脚本在 .claude/skills/go-module-renamer/scripts/perform_rename.py
    # 需要向上 5 级到达项目根目录
    project_root = script_path.parents[4]  # 向上 5 级（从 scripts 开始数：scripts -> go-module-renamer -> skills -> .claude -> project）

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

    # 实在找不到，返回当前工作目录（可能会失败，但至少有明确的错误信息）
    print("⚠️  警告：无法找到项目根目录（go.mod），使用当前工作目录")
    return cwd


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


class ModuleRenamer:
    """Go 模块重命名器"""

    def __init__(self, old_module, new_module, rename_type="auto"):
        """
        初始化重命名器

        Args:
            old_module: 旧模块名
            new_module: 新模块名
            rename_type: 重命名类型（"auto", "full", "partial"）
        """
        self.old_module = old_module
        self.new_module = new_module
        self.backup_dir = Path(".backup")
        self.modified_files = []
        self.dry_run = False
        # 使用智能项目根目录定位
        self.base_dir = find_project_root()
        print(f"📁 项目根目录：{self.base_dir}")

        # 解析项目名
        self.old_project = old_module.split('/')[-1]
        self.new_project = new_module.split('/')[-1]

        # 自动检测重命名类型
        if rename_type == "auto":
            old_parts = old_module.split('/')
            new_parts = new_module.split('/')
            if old_parts[:2] == new_parts[:2]:
                self.rename_type = "partial"
            else:
                self.rename_type = "full"
        else:
            self.rename_type = rename_type

        # 替换规则
        self.replacements = self._build_replacements()

    def _build_replacements(self):
        """构建替换规则列表"""
        replacements = []

        if self.rename_type == "full":
            # 全量替换规则
            replacements = [
                {
                    "pattern": "go.mod",
                    "type": "full",
                    "search": f"module {self.old_module}",
                    "replace": f"module {self.new_module}"
                },
                {
                    "pattern": "*.go",
                    "type": "full",
                    "search": f'"{self.old_module}/',
                    "replace": f'"{self.new_module}/'
                },
                {
                    "pattern": "*.proto",
                    "type": "full",
                    "search": f'option go_package = "{self.old_module}/',
                    "replace": f'option go_package = "{self.new_module}/'
                },
                {
                    "pattern": "Makefile",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
                {
                    "pattern": "OWNERS",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
                {
                    "pattern": "*.md",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
                {
                    "pattern": "internal/conf/config.proto",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
            ]
        else:
            # 部分替换规则
            replacements = [
                {
                    "pattern": "Makefile",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
                {
                    "pattern": "OWNERS",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
                {
                    "pattern": "*.md",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
                {
                    "pattern": "internal/conf/config.proto",
                    "type": "partial",
                    "search": self.old_project,
                    "replace": self.new_project
                },
            ]

        return replacements

    def create_backup(self):
        """创建备份"""
        print(f"📦 创建备份到 {self.backup_dir}")

        try:
            # 如果备份目录已存在，先删除
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)

            self.backup_dir.mkdir(parents=True, exist_ok=True)

            # 收集需要备份的文件
            files_to_backup = self._collect_files_to_backup()

            # 复制文件到备份目录
            for file_path in files_to_backup:
                if file_path.exists():
                    # 保持目录结构
                    relative_path = file_path.relative_to(self.base_dir)
                    backup_path = self.backup_dir / relative_path
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, backup_path)

            print(f"✅ 备份完成：{len(files_to_backup)} 个文件")
            return True

        except Exception as e:
            print(f"❌ 备份失败：{e}")
            return False

    def _collect_files_to_backup(self):
        """收集需要备份的文件"""
        files = set()

        # 添加特定文件
        specific_files = [
            "go.mod",
            "Makefile",
            "OWNERS",
        ]
        for file_name in specific_files:
            file_path = self.base_dir / file_name  # 使用绝对路径
            if file_path.exists():
                files.add(file_path)

        # 添加匹配模式的文件
        for pattern in ["*.go", "*.proto", "*.md"]:
            files.update(self.base_dir.rglob(pattern))

        return list(files)

    def perform_rename(self, dry_run=False):
        """
        执行重命名

        Args:
            dry_run: 是否为试运行（不实际修改文件）

        Returns:
            bool: 成功返回 True，否则返回 False
        """
        self.dry_run = dry_run

        if dry_run:
            print("🔍 试运行模式：不会实际修改文件")
        else:
            print(f"🚀 开始重命名：{self.old_module} → {self.new_module}")
            print(f"   类型：{'全量替换' if self.rename_type == 'full' else '部分替换'}")

        # 创建备份
        if not dry_run:
            if not self.create_backup():
                return False

        # 执行替换
        modified_count = 0
        for replacement in self.replacements:
            pattern = replacement["pattern"]
            search = replacement["search"]
            replace = replacement["replace"]

            # 查找匹配的文件
            if "*" in pattern:
                # 使用 glob 模式
                matching_files = list(self.base_dir.rglob(pattern))
            else:
                # 特定文件
                matching_files = [self.base_dir / pattern]

            # 对每个文件执行替换
            for file_path in matching_files:
                if file_path.is_file():
                    if self._replace_in_file(file_path, search, replace):
                        modified_count += 1
                        if file_path not in self.modified_files:
                            self.modified_files.append(file_path)

        # 清理模板注释
        if not dry_run:
            self._clean_template_comments()

        print(f"✅ 替换完成：{modified_count} 处修改")

        return True

    def _replace_in_file(self, file_path, search, replace):
        """
        在文件中执行替换

        Args:
            file_path: 文件路径
            search: 搜索字符串
            replace: 替换字符串

        Returns:
            bool: 如果文件被修改返回 True，否则返回 False
        """
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否包含搜索字符串
            if search not in content:
                return False

            # 执行替换
            new_content = content.replace(search, replace)

            # 如果内容有变化，写入文件
            if new_content != content:
                if not self.dry_run:
                    # 写入临时文件，然后原子性替换
                    temp_path = file_path.with_suffix(file_path.suffix + '.tmp')
                    with open(temp_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    # 原子性替换
                    temp_path.replace(file_path)

                print(f"   ✓ {file_path.relative_to(self.base_dir)}")
                return True

            return False

        except Exception as e:
            print(f"   ⚠️  {file_path.relative_to(self.base_dir)}: {e}")
            return False

    def _clean_template_comments(self):
        """清理模板注释（删除包含 "// 模板：" 的行）"""
        print("🧹 清理模板注释...")

        for file_path in self.base_dir.rglob("*.go"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # 过滤掉包含模板注释的行
                new_lines = [line for line in lines if "// 模板：" not in line]

                # 如果有变化，写回文件
                if len(new_lines) != len(lines):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"   ✓ {file_path.relative_to(self.base_dir)} (清理模板注释)")

            except Exception as e:
                print(f"   ⚠️  {file_path.relative_to(self.base_dir)}: {e}")

    def rollback(self):
        """回滚所有修改"""
        print("🔄 回滚操作...")

        if not self.backup_dir.exists():
            print("❌ 备份目录不存在，无法回滚")
            return False

        try:
            # 恢复备份的文件
            for backup_file in self.backup_dir.rglob("*"):
                if backup_file.is_file():
                    # 计算原始文件路径
                    relative_path = backup_file.relative_to(self.backup_dir)
                    original_path = self.base_dir / relative_path

                    # 恢复文件
                    shutil.copy2(backup_file, original_path)

            print("✅ 回滚完成")
            return True

        except Exception as e:
            print(f"❌ 回滚失败：{e}")
            return False

    def generate_report(self):
        """生成操作报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "rename_type": self.rename_type,
            "old_module": self.old_module,
            "new_module": self.new_module,
            "old_project": self.old_project,
            "new_project": self.new_project,
            "modified_files": [str(f.relative_to(self.base_dir)) for f in self.modified_files],
            "modified_count": len(self.modified_files),
        }

        return report


def main():
    """主函数"""
    # 确保在正确的 Python 环境中运行
    python_bin = ensure_python_env()

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Go 模块重命名工具')
    parser.add_argument('old_module', help='旧模块名')
    parser.add_argument('new_module', help='新模块名')
    parser.add_argument('--type', choices=['auto', 'full', 'partial'], default='auto',
                        help='重命名类型（默认：auto）')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式（不实际修改文件）')

    args = parser.parse_args()

    # 创建重命名器
    renamer = ModuleRenamer(args.old_module, args.new_module, args.type)

    # 执行重命名
    if not renamer.perform_rename(dry_run=args.dry_run):
        sys.exit(2)

    # 生成报告
    report = renamer.generate_report()
    print("\n📊 操作报告：")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    sys.exit(0)


if __name__ == "__main__":
    main()
