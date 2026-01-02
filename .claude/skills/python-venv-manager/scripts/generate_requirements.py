#!/usr/bin/env python3
"""
依赖生成器

分析项目中的 Python 代码，生成 requirements.txt 文件。

功能：
    - 扫描所有 .py 文件
    - 提取 import 语句
    - 识别第三方包
    - 过滤标准库和本地模块
    - 生成 requirements.txt

用法：
    python3 generate_requirements.py
"""

import sys
import ast
from pathlib import Path


# Python 3.8-3.14 标准库列表
STDLIB_MODULES = {
    # 常用标准库
    'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore',
    'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins',
    'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs',
    'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser',
    'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt', 'csv',
    'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib',
    'dis', 'distutils', 'doctest', 'email', 'encodings', 'enum', 'errno', 'faulthandler',
    'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib',
    'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'grp',
    'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp',
    'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword',
    'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap',
    'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt',
    'multiprocessing', 'netrc', 'nis', 'nntplib', 'numbers', 'operator', 'optparse',
    'os', 'ossaudiodev', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil',
    'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint', 'profile',
    'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri',
    'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy',
    'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal',
    'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3',
    'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess',
    'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile',
    'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'threading', 'time',
    'timeit', 'tkinter', 'token', 'tokenize', 'tomllib', 'trace', 'traceback',
    'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing', 'typing_extensions',
    'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave',
    'weakref', 'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml',
    'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib',
}

# 常见包别名映射（import 名称 -> PyPI 包名）
PACKAGE_ALIASES = {
    'yaml': 'pyyaml',
    'PIL': 'pillow',
    'cv2': 'opencv-python',
    'bs4': 'beautifulsoup4',
    'sklearn': 'scikit-learn',
    'matplotlib': 'matplotlib',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'scipy': 'scipy',
    'tensorflow': 'tensorflow',
    'torch': 'torch',
    'tf': 'tensorflow',
}


def extract_imports_from_file(file_path):
    """
    从 Python 文件中提取导入的模块

    参数:
        file_path: Python 文件路径

    返回:
        set: 导入的模块集合
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content, filename=str(file_path))
        imports = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # 获取顶层包名
                    module_name = alias.name.split('.')[0]
                    imports.add(module_name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # 获取顶层包名
                    module_name = node.module.split('.')[0]
                    imports.add(module_name)

        return imports

    except SyntaxError as e:
        print(f"⚠️  警告：无法解析 {file_path}（语法错误）：{e}")
        return set()
    except Exception as e:
        print(f"⚠️  警告：无法解析 {file_path}：{e}")
        return set()


def scan_project_files():
    """
    扫描项目中的所有 Python 文件

    返回:
        list: Python 文件路径列表
    """
    # 获取当前目录
    current_dir = Path.cwd()

    # 排除虚拟环境和常见的缓存目录
    exclude_dirs = {
        '.venv', 'venv', 'env', '__pycache__',
        '.git', '.tox', 'dist', 'build', '*.egg-info'
    }

    py_files = []
    for py_file in current_dir.rglob('*.py'):
        # 检查是否在排除目录中
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue

        py_files.append(py_file)

    return py_files


def generate_requirements():
    """
    生成 requirements.txt 文件

    返回:
        tuple: (成功标志, 可疑导入列表)
    """
    print("🔍 正在扫描 Python 文件...")

    # 1. 扫描项目中的所有 .py 文件
    py_files = scan_project_files()

    if not py_files:
        print("❌ 错误：未找到 Python 文件")
        return False, []

    print(f"   找到 {len(py_files)} 个 Python 文件")

    # 2. 提取所有 import 语句
    print("📦 正在提取导入语句...")
    all_imports = set()
    suspicious = []

    for py_file in py_files:
        file_imports = extract_imports_from_file(py_file)
        all_imports.update(file_imports)

    print(f"   提取到 {len(all_imports)} 个导入")

    # 3. 过滤标准库
    print("🔎 正在识别第三方包...")
    third_party = all_imports - STDLIB_MODULES

    # 过滤本地导入（点号开头的）
    third_party = {m for m in third_party if not m.startswith('.')}

    print(f"   识别到 {len(third_party)} 个第三方包")

    # 4. 处理常见包别名映射
    print("🔄 正在规范化包名...")
    normalized_packages = set()
    for package in third_party:
        pypi_name = PACKAGE_ALIASES.get(package, package)
        normalized_packages.add(pypi_name)

    # 5. 检测可疑导入（需要人工检查的情况）
    for file in py_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检测动态导入
            if 'importlib.import_module' in content:
                suspicious.append(f"{file.relative_to(Path.cwd())}: 使用动态导入 importlib.import_module")

            # 检测条件性导入
            if 'try:' in content and 'import' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'try:' in line:
                        # 检查后续几行是否有 import
                        for j in range(i+1, min(i+5, len(lines))):
                            if 'import' in lines[j] and 'except' not in lines[j]:
                                suspicious.append(f"{file.relative_to(Path.cwd())} (行 {i+1}): 可能的条件性导入")
                                break

        except Exception:
            pass

    # 6. 生成 requirements.txt（使用宽松版本要求）
    print("📝 正在生成 requirements.txt...")
    try:
        with open("requirements.txt", "w", encoding='utf-8') as f:
            for package in sorted(normalized_packages):
                f.write(f"{package}>=1.0.0\n")

        print(f"✅ 已生成 requirements.txt，包含 {len(normalized_packages)} 个包")

    except Exception as e:
        print(f"❌ 生成 requirements.txt 失败：{e}")
        return False, []

    # 7. 报告特殊情况（提示用户检查）
    if suspicious:
        print(f"\n⚠️  检测到 {len(suspicious)} 个需要人工检查的情况：")
        for item in suspicious[:10]:  # 最多显示 10 个
            print(f"   - {item}")
        if len(suspicious) > 10:
            print(f"   ... 还有 {len(suspicious) - 10} 个")
        print("\n💡 提示：某些动态导入或条件性依赖可能需要手动添加到 requirements.txt")

    return True, suspicious


def main():
    """主函数"""
    # 检查 requirements.txt 是否已存在
    if Path("requirements.txt").exists():
        print("⚠️  警告：requirements.txt 已存在")
        print("   将覆盖现有文件")

        if sys.stdin.isatty():
            try:
                response = input("是否继续？(y/N): ")
                if response.lower() != 'y':
                    print("❌ 取消操作")
                    sys.exit(1)
            except KeyboardInterrupt:
                print("\n❌ 用户取消操作")
                sys.exit(1)
        else:
            print("   非交互模式，取消操作")
            sys.exit(1)

    print()

    # 生成 requirements.txt
    success, suspicious = generate_requirements()

    if success:
        print("\n✅ 依赖生成完成")
        print("\n💡 后续步骤：")
        print("   1. 检查生成的 requirements.txt")
        print("   2. 根据需要调整版本要求")
        print("   3. 运行：pip install -r requirements.txt")
        sys.exit(0)
    else:
        print("\n❌ 依赖生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
