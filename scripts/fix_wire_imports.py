#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wire 生成文件导入规范调整脚本

本脚本用于调整 wire_gen.go 文件的 import 部分，使其符合 rule.md 中的规范：
- 所有项目内包必须强制取别名，别名前缀为 app
- import 按字母顺序排序

使用方式:
    python3 scripts/fix_wire_imports.py                    # 处理当前目录下所有 wire_gen.go
    python3 scripts/fix_wire_imports.py /path/to/project   # 处理指定目录下所有 wire_gen.go
    python3 scripts/fix_wire_imports.py --dry-run          # 仅显示修改，不写入文件
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, Tuple, List


class WireImportFixer:
    """Wire 生成文件的 import 规范调整工具"""

    # 项目内包的包名前缀映射
    PACKAGE_ALIAS_MAP = {
        "internal/app/task": "task",
        "internal/app/web": "web",
        "internal/biz": "biz",
        "internal/data": "data",
        "internal/domain": "domain",
        "internal/pkg/conf": "conf",
        "internal/pkg/log": "log",
        "internal/server": "server",
        "internal/service": "service",
        "internal/task": "task",
    }

    def __init__(self, project_root: str = ".", dry_run: bool = False):
        """
        初始化修复工具

        参数：
          - project_root：项目根目录路径
          - dry_run：是否仅显示修改而不写入文件
        """
        self.project_root = project_root
        self.dry_run = dry_run
        self.files_processed = 0
        self.files_modified = 0

    def find_wire_gen_files(self) -> List[str]:
        """查找所有 wire_gen.go 文件"""
        wire_files = []
        for root, dirs, files in os.walk(self.project_root):
            # 跳过 vendor 和 node_modules 目录
            if "vendor" in dirs:
                dirs.remove("vendor")
            if "node_modules" in dirs:
                dirs.remove("node_modules")

            if "wire_gen.go" in files:
                wire_files.append(os.path.join(root, "wire_gen.go"))

        return sorted(wire_files)

    def get_package_alias(self, package_path: str) -> str:
        """
        获取包的别名

        参数：
          - package_path：包的路径，如 'github.com/fsyyft-go/kratos-layout/internal/conf'

        返回：
          - 别名，如 'appconf'；如果不是项目内包则返回空字符串
        """
        for internal_path, pkg_name in self.PACKAGE_ALIAS_MAP.items():
            if package_path.endswith(internal_path):
                return f"app{pkg_name}"
        return ""

    def parse_imports(self, content: str) -> Tuple[str, Dict[str, str]]:
        """
        解析 import 部分

        参数：
          - content：文件内容

        返回：
          - (前缀, import字典)：前缀是 import 前的部分，字典为 {原始导入: 别名}
        """
        # 找到 import ( 和 ) 的位置
        import_pattern = r'(.*?import\s*\()(.*?)(\)\s*(?://|$))'
        match = re.search(import_pattern, content, re.DOTALL)

        if not match:
            return content, {}

        prefix = match.group(1)
        import_block = match.group(2)
        suffix = match.group(3)

        # 解析每一行的导入
        imports_dict = {}
        lines = import_block.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            # 提取包路径
            if '"' in line:
                match = re.search(r'"([^"]+)"', line)
                if match:
                    package_path = match.group(1)
                    imports_dict[package_path] = None

        return content, imports_dict

    def add_copyright_header(self, content: str) -> Tuple[str, bool]:
        """
        添加版权信息到文件开头

        参数：
          - content：文件内容

        返回：
          - (修改后的内容, 是否添加了版权信息)
        """
        copyright_header = (
            "// Copyright 2025 fsyyft-go\n"
            "//\n"
            "// Licensed under the MIT License. See LICENSE file in the project root for full license information.\n"
            "\n"
        )
        
        # 检查是否已有版权信息
        if content.strip().startswith("// Copyright"):
            return content, False
        
        # 添加版权信息到文件开头
        return copyright_header + content, True

    def fix_imports(self, content: str) -> Tuple[str, bool]:
        """
        调整 import 部分使其符合规范

        参数：
          - content：文件内容

        返回：
          - (修改后的内容, 是否发生了修改)
        """
        # 找到 import ( 和 ) 的位置
        import_pattern = r'(.*?import\s*\()(.*?)(\))'
        match = re.search(import_pattern, content, re.DOTALL)

        if not match:
            return content, False

        prefix = match.group(1)
        import_block = match.group(2)
        suffix = match.group(3)

        # 收集需要导入的包
        imports_list = []
        needs_modification = False
        
        for line in import_block.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            if '"' in line:
                match = re.search(r'"([^"]+)"', line)
                if match:
                    package_path = match.group(1)
                    alias = self.get_package_alias(package_path)
                    
                    # 检查该行是否已有别名
                    has_alias = " " in line and not line.startswith('"')
                    
                    if alias:
                        imports_list.append((alias, package_path))
                        # 如果需要别名但当前没有，则需要修改
                        if not has_alias:
                            needs_modification = True
                    else:
                        imports_list.append((None, package_path))

        # 如果没有检测到需要修改的地方，直接返回
        if not needs_modification:
            return content, False

        # 按别名排序（先处理别名包，后处理非别名包）
        aliased_imports = sorted(
            [(alias, pkg) for alias, pkg in imports_list if alias],
            key=lambda x: x[0]
        )
        other_imports = sorted(
            [(None, pkg) for alias, pkg in imports_list if not alias],
            key=lambda x: x[1]
        )

        # 生成新的 import 块
        new_import_lines = []
        for alias, package_path in aliased_imports + other_imports:
            if alias:
                new_import_lines.append(f'\t{alias} "{package_path}"')
            else:
                new_import_lines.append(f'\t"{package_path}"')

        new_import_block = "\n" + "\n".join(new_import_lines) + "\n"

        # 替换 import 块
        new_content = re.sub(
            import_pattern,
            prefix + new_import_block + suffix,
            content,
            count=1,
            flags=re.DOTALL
        )

        # 更新代码中对包的引用
        new_content = self.update_package_references(
            new_content, imports_list
        )

        return new_content, True

    def update_package_references(
        self, content: str, imports_list: List[Tuple[str, str]]
    ) -> str:
        """
        更新代码中对包的引用

        参数：
          - content：文件内容
          - imports_list：[(别名, 包路径), ...]

        返回：
          - 更新后的内容
        """
        # 跳过 import 块
        import_pattern = r'import\s*\(.*?\)'
        match = re.search(import_pattern, content, re.DOTALL)

        if not match:
            return content

        import_end = match.end()
        before_import = content[:import_end]
        after_import = content[import_end:]

        # 在 import 块之后的代码中更新包引用
        for alias, package_path in imports_list:
            if not alias:
                continue

            # 提取包名（最后一个 / 之后的部分）
            original_pkg_name = package_path.split("/")[-1]

            # 替换 package.Function 为 alias.Function
            pattern = rf'\b{original_pkg_name}\.'
            replacement = f"{alias}."

            after_import = re.sub(pattern, replacement, after_import)

        return before_import + after_import

    def process_file(self, filepath: str) -> bool:
        """
        处理单个文件

        参数：
          - filepath：文件路径

        返回：
          - 是否发生了修改
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 添加版权信息
            new_content, copyright_added = self.add_copyright_header(content)
            
            # 调整 import
            new_content, import_modified = self.fix_imports(new_content)
            
            modified = copyright_added or import_modified

            if modified:
                if not self.dry_run:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)

                return True

            return False

        except Exception as e:
            print(f"❌ 处理文件 {filepath} 出错: {e}", file=sys.stderr)
            return False

    def run(self):
        """执行修复操作"""
        wire_files = self.find_wire_gen_files()

        if not wire_files:
            print("ℹ️  未找到任何 wire_gen.go 文件")
            return

        print(f"📝 找到 {len(wire_files)} 个 wire_gen.go 文件\n")

        for filepath in wire_files:
            self.files_processed += 1
            modified = self.process_file(filepath)

            if modified:
                self.files_modified += 1
                status = "✏️  已修改" if not self.dry_run else "✏️  需要修改"
                print(f"{status}: {filepath}")
            else:
                print(f"✅ 已符合规范: {filepath}")

        print(f"\n📊 统计信息:")
        print(f"   处理文件数: {self.files_processed}")
        print(f"   修改文件数: {self.files_modified}")
        if self.dry_run:
            print(f"   ℹ️  此次为演示运行，未实际修改文件")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="调整 wire_gen.go 文件的 import 使其符合 rule.md 规范"
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="项目根目录（默认为当前目录）"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅显示修改，不写入文件"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细输出"
    )

    args = parser.parse_args()

    # 验证项目目录
    project_root = args.project_root
    if not os.path.isdir(project_root):
        print(f"❌ 错误：目录不存在: {project_root}", file=sys.stderr)
        sys.exit(1)

    fixer = WireImportFixer(project_root, args.dry_run)
    fixer.run()


if __name__ == "__main__":
    main()
