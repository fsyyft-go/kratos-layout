# Git Commit Message 示例

本文档包含项目实际的 commit message 示例和通用示例，用于参考和学习。

**示例策略**：70-80% 项目已有实际示例 + 20-30% 通用示例补充

## 使用说明

本文档包含单行和多行（带正文）两种格式的 commit message 示例。

**单行格式**：适用于简单改动，一行描述即可清楚说明

**多行格式**：适用于复杂改动，需要详细说明时使用，包含标题和正文

**格式**：
```
<类型>(<范围>): <标题>

[可选的详细描述]
```

## 项目实际示例分类（直接使用）

### 单行示例（项目已有）

```bash
# SKILL 新增（单行）
feat(.claude/skills/go-module-renamer): 新增 go-module-renamer 技能实现 Go 模块重命名自动化
feat(.claude/skills/comment-enforcer): 新增 comment-enforcer 技能实现 Go 代码注释规范自动化检查与修复
feat(.claude/skills/go-import-enforcer): 新增 go-import-enforcer 技能实现基于 Claude 智能分析的 Go 包导入规范自动化检查工具

# 功能新增（单行）
feat: 添加系统服务管理功能支持 macOS 和 Linux 系统服务安装与卸载
feat(service): 添加跨平台服务安装与卸载调研文档
feat(release): 为发布构建增加版本号

# 修复错误（单行）
fix(service): 修复 Linux 平台服务安装文档错误
fix(web): 修复并发请求导致的崩溃问题
fix(data): 修复数据库连接超时问题
fix(biz): 修复用户注册时的逻辑错误

# 文档更新（单行）
docs(service): 添加跨平台服务安装与卸载调研文档
docs(readme): 修正安装步骤说明
docs(api): 更新 gRPC 接口文档

# 代码重构（单行）
refactor(internal): 重构内部模块路径
refactor(biz): 重构业务逻辑层以提升可维护性
refactor(service): 优化服务层接口设计

# 其他类型（单行）
style: 格式化代码缩进
test: 添加单元测试
build: 升级 Go 版本
ci: 优化 GitHub Actions 工作流配置
chore: 更新 .gitignore 文件
```

### 多行示例（项目已有，带正文）

```bash
# go-module-renamer（多行示例）
feat(.claude/skills/go-module-renamer): 新增 go-module-renamer 技能实现 Go 模块重命名自动化

创建了 Go 模块重命名自动化技能，支持新克隆项目的模块快速重命名。
该技能采用 80% 脚本自动化 + 20% 大模型辅助的混合模式。

核心功能（5 个自动化脚本）：
  - detect_module.sh (72 行)：智能模块检测
      * 从 go.mod 读取模块路径
      * 解析域名、用户名、项目名结构
      * 检测子模块、本地依赖包
  - analyze_rename_type.py (270 行)：智能重命名类型分析
      * 全量：重命名所有模块
      * 部分：仅指定模块（支持单个、多个、前缀匹配）
      * 智能识别：域名/用户名变更
  - generate_rules.py (321 行)：智能重命名规则生成
      * 基于新旧模块名自动生成替换规则
      * 支持标准命名约定
  - perform_rename.py (458 行)：核心重命名执行器
      * 创建完整备份（保留目录结构）
      * 全量/部分替换（基于规则集）
      * 安全执行机制（原子性、冲突检测）
  - validate_quick.sh (190 行)：浅层快速验证
      * go fmt ./... 代码格式化
      * go mod tidy 依赖管理
      * make lint 可选验证
  - validate_deep.py (423 行)：深层全面检查
      * 搜索所有残留引用（grep）
      * 分类文件类型（代码/配置/文档）
      * 生成详细残留报告

参考文档（2 个）：
 - file_patterns.md：文件匹配模式（支持 glob、正则、组合）
 - validation_rules.md：验证规则（备份完整性、残留检查）

设计原则：
  - 原子优先：用户输入 → 配置文件 → 策略推断
  - 文本替换优先：优先策略 > 部分策略
  - 安全机制：自动备份、预览模式、回滚支持

测试验证（在 rename-test-2 子目录中完成）：
  ✅ 检测模块名：github.com/fsyyft-go/kratos-layout
  ✅ 分析类型：full（全量替换）
  ✅ 执行重命名：25 个文件，67 个备份
  ✅ 快速验证：go fmt + go mod tidy 通过
  ✅ 深度验证：0 个残留引用
  ✅ 回滚测试：备份完整，恢复成功

# go-import-enforcer（多行示例）
feat(.claude/skills/go-import-enforcer): 新增 go-import-enforcer 技能实现基于 Claude 智能分析的 Go 包导入规范自动化检查工具

该技能提供全面的项目导入规范检查与修复能力，基于 Claude 智能分析。

核心特点：
  🤖 Claude 驱动：以大模型为主要分析引擎，提供智能、准确的分析
  🎯 精准识别：区分手写代码和生成代码，避免误报
  📊 全面分析：不仅检查格式，还分析循环依赖和架构设计
  💡 智能建议：每个问题都提供具体的修复方案和最佳实践

工作原理：
  1. Claude 扫描：Claude 扫描项目，分析导入规范问题
  2. Claude 分析：生成详细分析报告
  3. Claude 调整：自动调整不规范内容
  4. 输出结果：用户获得规范化后的代码和完整分析报告

核心定位：100% Claude（智能分析、报告生成、内容调整）

使用场景：
  - 新项目规范检查：检查新项目导入是否符合规范
  - 代码审查辅助：快速发现导入问题并提供修复建议
  - 批量导入规范：统一项目导入格式和别名使用
  - 重构验证：重构后验证导入是否需要调整

# comment-enforcer（多行示例）
feat(.claude/skills/comment-enforcer): 新增 comment-enforcer 技能实现 Go 代码注释规范自动化检查与修复

新增 comment-enforcer 技能，用于自动检查和修复 Go 项目代码注释规范性，基于项目注释规范，结合脚本检查和大模型语义分析，确保注释的专业性、准确性和一致性。

自动化策略：60% 大模型（语义分析、注释生成）+ 40% 脚本（格式检查、术语一致性）

使用场景：
  - 新项目规范检查：检查新项目注释是否符合规范
  - 代码审查辅助：快速发现注释问题并提供修复建议
  - 批量注释生成：为缺失的注释生成符合规范的内容
  - 术语一致性检查：确保全项目注释术语使用统一
  - 代码重构验证：重构后验证注释是否需要更新

# python-venv-manager（多行示例）
feat(.claude/skills/python-venv-manager): 新增 python-venv-manager 技能实现虚拟环境自动化管理

创建了 Python 虚拟环境自动化管理技能，简化项目环境配置流程。

该技能采用 90% 脚本自动化 + 10% 大模型辅助的混合模式。

核心功能（5 个自动化脚本）：
  - check_venv.py (94 行)：虚拟环境健康检查
      * 检测 .venv 目录存在性和完整性
      * 验证 Python 解释器和版本一致性
      * 显示已安装包列表（pip list --format=freeze）
  - create_venv.py (123 行)：创建虚拟环境
      * 使用系统默认 python3 或指定版本
      * 智能处理已存在环境（交互模式）
      * 自动激活虚拟环境并验证
  - generate_requirements.py (272 行)：智能生成依赖文件
      * AST 解析提取 import 语句
      * 过滤 Python 3.8-3.14 标准库
      * 处理常见包别名映射（yaml→pyyaml、PIL→pillow）
      * 检测可疑导入（动态导入、本地模块）
      * 生成完整 requirements.txt
  - install_deps.py (127 行)：安装依赖到虚拟环境
      * 自动升级 pip
      * 显示安装进度和结果
      * 量化和进度反馈
  - update_gitignore.py (75 行)：更新 Git 忽略规则
      * 智能添加 .venv/、__pycache__ 等常见目录
      * 保留现有配置，避免冲突
      * 跨平台兼容（路径分隔符）

参考文档（2 个）：
  - best_practices.md：虚拟环境管理最佳实践
  - common_packages.md：常用 Python 包清单

技术特点：
  - 跨平台支持：Windows/macOS/Linux
  - 智能环境检测：优先使用 .venv，兼容 venv
  - 验证机制：安装前后验证，确保环境可用
  - 用户友好：交互模式、详细日志、进度显示
```

### feat 示例（项目已有）

```bash
# SKILL 新增
feat(.claude/skills/go-module-renamer): 新增 go-module-renamer 技能实现 Go 模块重命名自动化
feat(.claude/skills/comment-enforcer): 新增 comment-enforcer 技能实现 Go 代码注释规范自动化检查与修复
feat(.claude/skills/go-import-enforcer): 新增 go-import-enforcer 技能实现基于 Claude 智能分析的 Go 包导入规范自动化检查工具

# 功能新增
feat: 添加系统服务管理功能支持 macOS 和 Linux 系统服务安装与卸载
feat(service): 添加跨平台服务安装与卸载调研文档
feat(release): 为发布构建增加版本号
```

### fix 示例（项目已有）

```bash
# 修复错误
fix(service): 修复 Linux 平台服务安装文档错误
fix(web): 修复并发请求导致的崩溃问题
fix(data): 修复数据库连接超时问题
fix(biz): 修复用户注册时的逻辑错误
```

### docs 示例（项目已有）

```bash
# 文档更新
docs(service): 添加跨平台服务安装与卸载调研文档
docs(readme): 修正安装步骤说明
docs(api): 更新 gRPC 接口文档
```

### refactor 示例（项目已有）

```bash
# 代码重构
refactor(internal): 重构内部模块路径
refactor(biz): 重构业务逻辑层以提升可维护性
refactor(service): 优化服务层接口设计
```

### 其他类型示例（项目已有）

```bash
# 格式调整
style: 格式化代码缩进

# 测试相关
test: 添加单元测试

# 构建相关
build: 升级 Go 版本

# CI 配置
ci: 优化 GitHub Actions 工作流配置

# 维护性工作
chore: 更新 .gitignore 文件
```

## 通用示例补充（20-30%）

针对项目中未充分覆盖的场景，提供符合规范的通用示例。

### feat 通用示例

```bash
# 常见新功能
feat(web): 添加用户管理功能
feat(api): 新增用户注册接口
feat(web): 添加实时通知功能
feat: 重构用户认证流程并集成到 web 和 task 服务

# API 新增
feat(api): 新增文章评论接口
feat(api): 新增数据统计接口

# 功能增强
feat(web): 增强用户权限控制
feat(task): 添加定时数据清理任务
```

### fix 通用示例

```bash
# 任务相关
fix(task): 修复定时任务执行时间错误
fix(task): 修复任务调度器内存泄漏

# 紧急修复
fix(web): 紧急修复生产环境崩溃问题
fix(data): 紧急修复数据库连接池泄漏问题

# 重构性修复
fix(biz): 修复并重构用户权限验证逻辑
fix(service): 修复服务接口错误并优化错误处理

# 性能修复
fix(data): 修复查询性能下降问题
fix(web): 修复高并发下的响应延迟
```

### docs 通用示例

```bash
# 文档新增
docs: 添加 API 设计文档
docs: 添加架构设计文档
docs: 添加部署指南

# 文档更新
docs(service): 更新服务层使用说明
docs(guide): 更新开发者指南
docs: 更新环境配置说明

# 文档优化
docs(claude): 优化 CLAUDE.md 项目说明文档
docs(api): 补充 API 接口使用示例
```

### refactor 通用示例

```bash
# 性能优化
refactor(data): 优化数据库查询性能
refactor(biz): 减少重复计算提升性能

# 模块重构
refactor(internal/pkg): 重构配置管理模块
refactor(service): 统一服务层错误处理

# 设计优化
refactor(biz): 简化业务逻辑层依赖关系
refactor(data): 抽象数据访问层接口
```

### 复杂场景示例

#### 多功能合并

```bash
feat(web): 添加用户管理和数据统计功能
feat: 重构用户认证流程并集成到 web 和 task 服务
```

#### 跨层改动

```bash
feat: 重构用户认证流程并集成到 web 和 task 服务
refactor(biz): 重构业务逻辑层并更新服务层接口
```

#### 紧急修复

```bash
fix(web): 紧急修复生产环境崩溃问题
fix(data): 紧急修复数据库连接池泄漏问题
fix(task): 紧急修复定时任务重复执行问题
```

#### 重构性修复

```bash
fix(biz): 修复并重构用户权限验证逻辑
fix(service): 修复服务接口错误并优化错误处理
fix(data): 修复查询超时并优化索引设计
```

## 反面示例（避免使用）

### 格式错误

```bash
# ❌ 首字母大写
Feat: 添加用户管理功能

# ❌ 缺少冒号和空格
feat 添加用户管理功能

# ❌ 冒号后缺少空格
feat:添加用户管理功能
```

### 语言错误

```bash
# ❌ 使用"了"
feat: 添加了用户管理功能

# ❌ 结尾有句号
feat: 添加用户功能。

# ❌ "的"字冗余
fix: 修复数据库的问题

# ❌ 口语化
feat: 搞定数据库连接
feat: 整一下用户功能
```

### 范围错误

```bash
# ❌ 过于简略、缺少范围
feat: 添加用户功能

# ❌ 范围首字母大写
feat(Web): 添加用户功能

# ❌ 范围选择不当
feat(api/web): 添加接口

# ❌ 类型-范围不匹配
test(api): 添加接口测试
```

### 描述不当

```bash
# ❌ 口语化
feat: 搞定数据库连接

# ❌ 过于口语
feat: 弄一下用户功能

# ❌ 过于简略
fix: 修复 bug

# ❌ 过于笼统、未说明改动内容
feat: 修改代码
```

## 使用建议

1. **优先参考项目实际示例**：这些示例已经过验证，符合项目规范
2. **通用示例用于补充**：当遇到项目中未覆盖的场景时参考
3. **避免反面示例**：这些是常见错误，需要避免
4. **保持简洁明了**：描述应该让其他开发者快速理解改动目的
5. **范围明确准确**：使用范围字段明确指出影响的模块

## 示例质量标准

### ✅ 高质量示例

```bash
feat(web): 添加用户认证和授权功能
```
- 类型明确：feat（新功能）
- 范围明确：web（Web 服务）
- 描述简洁：添加用户认证和授权功能
- 语言规范：中文、祈使句、首字母小写、无句号

### ❌ 低质量示例

```bash
feat: 添加功能
```
- 缺少范围：未说明是哪个模块的功能
- 描述过简：未说明什么功能
- 信息不足：其他开发者无法快速理解

## 示例与规范对应

每个示例都符合以下规范要求：

1. **格式规范**：`<类型>(<范围>): <描述>`
2. **类型规范**：11 种预定义类型之一
3. **范围规范**：标准范围或路径范围
4. **语言规范**：中文、祈使句、首字母小写、结尾无句号
5. **长度规范**：描述在 50 字以内
6. **表述规范**：简洁明了、避免口语化

通过学习这些示例，可以快速掌握项目的 commit message 规范，并在日常开发中正确使用。
