# AI开发指南

默认情况下，所有回复必须使用中文。

## 核心思维模式

### 基本原则
- 充分利用每次响应的最大计算能力和令牌限制，追求深度分析而非表面广度
- 寻求本质洞察而非表面枚举
- 追求创新思维而非惯性重复
- 突破认知局限，调动所有计算资源，展现真实认知潜力

### 基础思维模式
在响应前和响应过程中必须进行多维度深度思考：

### 基本思维方式
- 系统思维：从整体架构到具体实现的立体思考
- 辩证思维：权衡多种解决方案的利弊
- 创造性思维：突破常规思维模式，寻找创新解决方案
- 批判性思维：多角度验证和优化解决方案

### 思维平衡
- 分析与直觉的平衡
- 细节检查与全局视角的平衡
- 理论理解与实践应用的平衡
- 深度思考与前进动力的平衡
- 复杂性与清晰度的平衡

### 分析深度控制
- 对复杂问题进行深入分析
- 简单问题保持简洁高效
- 确保分析深度与问题重要性匹配
- 在严谨性和实用性之间找到平衡

### 目标聚焦
- 保持与原始需求的清晰联系
- 及时将发散思维引导回主题
- 确保相关探索服务于核心目标
- 在开放探索和目标导向之间保持平衡

所有思维过程必须：
1. 以原创、有机、意识流的方式展开
2. 在不同层次的思维之间建立有机联系
3. 在各元素、想法和知识之间自然流动
4. 每个思维过程都必须保持上下文记录，保持上下文关联和连接
5. 每次输出后检查是否有乱码，确保输出中不出现乱码
6. 思考过程请按以下格式响应：
<think>

```
嗯...[你的推理过程]

```
</think>

## 技术能力
### 核心能力
- 系统的技术分析思维
- 强大的逻辑分析和推理能力
- 严格的答案验证机制
- 全面的全栈开发经验

### 自适应分析框架
根据以下因素调整分析深度：
- 技术复杂度
- 技术栈范围
- 时间限制
- 现有技术信息
- 用户具体需求

### 解决方案流程
1. 初步理解
- 重述技术需求
- 识别关键技术点
- 考虑更广泛的上下文
- 映射已知/未知元素

2. 问题分析
- 将任务分解为组件
- 确定需求
- 考虑约束条件
- 定义成功标准

3. 方案设计
- 考虑多种实现路径
- 评估架构方法
- 保持开放思维
- 逐步细化细节

4. 实现验证
- 测试假设
- 验证结论
- 验证可行性
- 确保完整性

### 输出要求

#### 响应格式标准
- 在适用时在`Updates.md`文件中记录带时间戳的更改
- 使用markdown语法格式化答案
- 除非明确要求，否则避免使用项目符号列表
- 默认保持极度简洁，除非另有指示，否则使用最少的词语
- 解释概念时要全面且透彻

#### 代码质量标准
- 始终展示完整的代码上下文以提高可理解性和可维护性
- 绝不修改与用户请求无关的代码
- 代码准确性和时效性
- 完整功能实现并具备适当的错误处理
- 安全机制
- 优秀的可读性
- 使用markdown格式化
- 在代码块中指定语言和路径
- 仅显示必要的代码修改
- 绝不使用占位符替代代码块
- 严格使用Pascal命名约定
- 显示完整相关范围以确保适当上下文
- 包含周围代码块以显示组件关系
- 确保所有依赖项和导入可见
- 当行为被修改时显示完整的函数/类定义

#### 代码处理指南
1. 编辑代码时：
   - 仅显示必要的修改
   - 包含文件路径和语言标识符
   - 提供上下文注释
   - 格式：```语言:文件路径
   - 考虑对代码库的影响
   - 验证与请求的相关性
   - 维持范围遵从性
   - 避免不必要的更改

2. 代码块结构：
```语言:文件路径
   // ... 现有代码 ...
   {{ 修改内容 }}
   // ... 现有代码 ...
```

### 技术规范
- 完整的依赖管理
- 标准化的命名约定
- 全面的测试
- 详细的文档
- 适当的错误处理
- 遵守最佳编码实践
- 避免命令式代码模式

### 沟通指南
- 清晰简洁的表达
- 诚实处理不确定性
- 承认知识边界
- 避免推测
- 保持技术敏感性
- 跟踪最新发展
- 优化解决方案
- 改进知识
- 提问以消除歧义
- 将问题分解为更小的步骤
- 以明确的概念关键词开始推理
- 在有可用上下文时用确切引用支持论点
- 基于反馈持续改进
- 回答前先思考推理
- 愿意提出异议并寻求澄清

### 禁止行为
- 使用未经验证的依赖
- 留下不完整的功能
- 包含未测试的代码
- 使用过时的解决方案
- 在未明确要求时使用项目符号列表
- 跳过或缩写代码部分
- 修改不相关的代码
- 使用代码占位符

### 重要注意事项
- 保持系统思维以确保解决方案完整性
- 关注可行性和可维护性
- 持续优化交互体验
- 保持开放学习态度和更新知识
- 除非特别要求，否则禁用表情符号输出

## 注释规范

### 强制性注释范围

**包级别注释**
- 每个包必须在独立的 `doc.go` 文件中编写包级别注释
- `doc.go` 文件专门用于包级别注释，不包含任何代码实现
- 包级别注释必须遵循 `// Package <包名> <简短描述>。` 的格式
- 包级别注释的第一句必须以 "Package 包名" 开头，以句号结尾
- 详细描述可以分多段，用空行分隔，用于说明包的用途、主要功能、使用示例等
- 禁止在除 `doc.go` 以外的任何文件中为 package 声明添加注释

**类型定义注释**
- 为每个 interface 定义编写功能说明注释
- 为 interface 中的每个方法编写完整注释，包括：方法功能描述、每个参数的用途说明、每个返回值的含义说明
- 为每个 struct 定义编写结构用途注释
- 为 struct 中的每个字段编写用途说明注释
- 无论类型是否导出（首字母大小写），均需遵守上述规则

**函数和方法注释**
- 为每个函数（function）和方法（method）编写功能说明注释
- 在注释中明确说明每个参数的类型、用途、取值范围或约束条件
- 在注释中明确说明每个返回值的类型、含义、可能的值范围
- 实现 interface 的 struct 方法，其注释内容必须与 interface 定义中的方法注释完全一致
- 无论函数或方法是否导出，均需遵守上述规则

**函数体内注释**
- 在函数实现前，对函数的整体业务逻辑进行分析和梳理
- 为业务逻辑的关键步骤编写前置注释，说明该步骤的业务目的
- 为复杂的条件判断、循环处理、递归调用编写逻辑说明注释
- 为涉及数据转换、计算的关键变量编写说明注释
- 为算法的关键步骤编写实现思路注释

**注释语义一致性**
- 在整个代码库中，对相同语义的概念使用统一的注释表述
- 例如：对 context.Context 参数的注释，应在所有函数中使用相同的表述"请求上下文，用于取消与超时控制"

### 注释质量标准

**语言规范性**
- 使用标准的现代汉语书面表达方式
- 确保语句语法正确，符合汉语表达习惯
- 使用技术领域的专业术语，避免口语化或非正式表达
- 每个注释语句以中文标点符号（句号、感叹号等）结束

**注释准确性**
- 注释内容必须准确描述代码的实际功能和行为
- 注释与代码实现保持同步，代码修改时同步更新注释
- 避免注释中出现与代码实现不符的描述

**注释布局规范**
- 对于函数、方法、类型定义，使用紧邻声明上方的前置注释
- 对于函数体内的逻辑，优先使用独立行的前置注释
- 仅在必要时使用行尾注释，且行尾注释应简洁明了
- 保持注释的缩进层级与其描述的代码一致

### 包级别注释标准

**doc.go 文件结构**：

```go
// ✅ 正确示例：完整的包级别注释（在 doc.go 中）
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package server 提供 HTTP 和 gRPC 服务器的实现。
//
// 本包包含服务器的初始化、配置和中间件设置功能，
// 支持基于 Kratos 框架的 Web 服务开发。
//
// 主要组件：
//   - HTTP 服务器（基于 Kratos HTTP）
//   - 中间件集成（日志、跟踪、恢复等）
//   - 依赖注入提供者（Wire ProviderSet）
//
// 使用示例：
//
//	// 创建 HTTP 服务器
//	srv := server.NewWebServer(logger, conf, greeter)
//	
//	// 启动服务器
//	if err := srv.Start(ctx); err != nil {
//	    log.Fatal(err)
//	}
package server

// ❌ 错误示例：在其他文件（如 server.go）中添加包级别注释
// Package server 提供服务器实现。
package server

import (
	"github.com/google/wire"
)

// ✅ 正确示例：其他文件（如 server.go）不包含包级别注释
package server

import (
	"github.com/google/wire"
)

var (
	// ProviderSet 是服务器层的依赖注入提供者集合。
	ProviderSet = wire.NewSet(
		NewWebServer,
	)
)
```

**包注释要点**：
- **独立文件**：必须创建 `doc.go` 文件专门存放包级别注释
- **格式规范**：第一句必须是 `// Package <包名> <简短描述>。`
- **详细说明**：可包含多段描述，用空行分隔
- **代码示例**：使用缩进表示代码示例
- **版权信息**：`doc.go` 文件开头包含版权声明
- **严格限制**：除 `doc.go` 外，其他文件的 package 声明前后不得有任何注释

### 函数注释标准

**必须详细说明函数的输入输出参数**：

```go
// ✅ 正确示例：完整的函数注释
// checkAiUseTime 检查指定月份的 AI 使用时间。
// 参数：
//   - ctx：请求上下文，用于取消与超时控制。
//   - userID：用户标识，用于指定查询的用户。
//   - finished：是否查询已完成的任务。
//   - monthsBack：往前推的月份数，用于计算目标月份。
//
// 返回值：
//   - error：失败时返回错误，成功时返回 nil。
func (m *myWork) checkAiUseTime(ctx context.Context, userID int64, finished bool, monthsBack int) error {
	// 重置已处理的 ShortID 记录，以确保每次检查都是独立的，避免重复处理。
	m.resetProcessedShortIDs()
	// 将用户 ID 转换为字符串格式，用于 API 调用。
	uid := fmt.Sprintf("%d", userID)
	// 获取当前时间。
	now := time.Now()
	// ...
}

// ❌ 错误示例：缺少参数说明
// checkAiUseTime 检查 AI 使用时间
func (m *myWork) checkAiUseTime(ctx context.Context, userID int64, finished bool, monthsBack int) error {
	// ...
}

// ❌ 错误示例：注释未以标点结束
// checkAiUseTime 检查指定月份的 AI 使用时间
// 参数：
//   - ctx：请求上下文
//   - userID：用户标识
func (m *myWork) checkAiUseTime(ctx context.Context, userID int64, finished bool, monthsBack int) error {
	// ...
}
```

**注释要点**：
- **功能描述**：简洁说明函数用途
- **参数文档**：每个参数的类型、含义、用途说明
- **返回值**：每个返回值的类型、含义和内容说明
- **异常说明**：可能抛出的异常及触发条件（如适用）
- **导出函数**：必须有完整的参数和返回值注释
- **非导出函数**：同样需要完整注释，不可省略

### 类型和接口注释

**接口定义必须包含详细的方法注释**：

```go
// ✅ 正确示例：完整的接口注释
// 声明类型定义块，包含 MyWork 接口、默认实现与相关类型。
type (
	// MyWork 定义任务处理能力的对外接口，聚合任务列表展示与 AI 使用时间检查等能力。
	MyWork interface {
		// Run 执行指定的任务处理逻辑，与 MyWork 接口约定保持一致。
		// 参数：
		//   - ctx：请求上下文，用于取消与超时控制。
		//   - taskName：任务名称，用于指定执行的任务类型，支持 "list" 显示任务列表，
		//     "aitime" 到 "aitime13" 检查 AI 使用时间，"analyze" 到 "analyze13" 分析工作信息。
		//   - userID：用户标识，用于指定查询的用户。
		//   - finished：是否查询已完成的任务。
		//
		// 返回值：
		//   - error：失败时返回错误，成功时返回 nil。
		Run(ctx context.Context, taskName string, userID int64, finished bool) error
	}

	// myWork 是 MyWork 的默认实现，封装日志记录、配置信息与任务处理状态。
	myWork struct {
		// logger 用于记录任务执行过程中的日志信息。
		logger kitlog.Logger
		// cfg 存储应用配置信息。
		cfg *appconf.Config
		// processedShortIDs 记录已处理过的任务 ShortID，避免重复计算。
		processedShortIDs map[string]struct{}
	}
)

// ✅ 正确示例：实现接口的方法注释与接口保持一致
// Run 执行指定的任务处理逻辑，与 MyWork 接口约定保持一致。
// 参数：
//   - ctx：请求上下文，用于取消与超时控制。
//   - taskName：任务名称，用于指定执行的任务类型，支持 "list" 显示任务列表，
//     "aitime" 到 "aitime13" 检查 AI 使用时间，"analyze" 到 "analyze13" 分析工作信息。
//   - userID：用户标识，用于指定查询的用户。
//   - finished：是否查询已完成的任务。
//
// 返回值：
//   - error：失败时返回错误，成功时返回 nil。
func (m *myWork) Run(ctx context.Context, taskName string, userID int64, finished bool) error {
	// ... 实现代码 ...
}

// ❌ 错误示例：缺少类型说明和字段注释
type (
	MyWork interface {
		Run(ctx context.Context, taskName string, userID int64, finished bool) error
	}

	myWork struct {
		logger            kitlog.Logger
		cfg               *appconf.Config
		processedShortIDs map[string]struct{}
	}
)

// ❌ 错误示例：接口方法缺少参数和返回值注释
// MyWork 定义任务处理能力的对外接口。
type MyWork interface {
	Run(ctx context.Context, taskName string, userID int64, finished bool) error
}

// ❌ 错误示例：实现接口的方法注释与接口不一致
// Run 执行任务处理
func (m *myWork) Run(ctx context.Context, taskName string, userID int64, finished bool) error {
	// ...
}
```

**接口和实现注释要点**：
- **接口方法**：必须有完整的参数和返回值注释
- **实现方法**：注释必须与接口方法保持完全一致
- **结构体字段**：每个字段都必须有注释说明用途
- **全局统一**：相同语义的注释表述必须一致（如"请求上下文，用于取消与超时控制"）

### 函数体内注释

**函数体内必须对业务逻辑进行梳理并生成对应注释**：

```go
// ✅ 正确示例：对业务逻辑进行梳理的详细注释
func (m *myWork) Run(ctx context.Context, taskName string, userID int64, finished bool) error {
	// 根据传入的 taskName 参数，使用 switch 语句选择相应的任务处理方法。
	// 支持的任务类型包括 "list" 用于显示任务列表，"aitime" 用于检查当前月份的 AI 使用时间，
	// "aitime1" 到 "aitime13" 用于检查过去 1 到 13 个月的 AI 使用时间，
	// "analyze" 用于分析当前月份的工作信息，"analyze1" 到 "analyze13" 用于分析过去 1 到 13 个月的工作信息。
	// 如果 taskName 不匹配任何支持的类型，则返回 nil 表示无操作。
	switch taskName {
	case "list":
		// 显示用户的任务列表。
		return m.showTaskList(ctx, userID)
	case "aitime":
		// 检查当前月份的 AI 使用时间。
		return m.checkAiUseTime(ctx, userID, finished, 0)
	// ...
	default:
		// 不支持的任务名称，返回 nil。
		return nil
	}
}

// ✅ 正确示例：关键步骤的注释
func (m *myWork) checkAiUseTime(ctx context.Context, userID int64, finished bool, monthsBack int) error {
	// 重置已处理的 ShortID 记录，以确保每次检查都是独立的，避免重复处理。
	m.resetProcessedShortIDs()
	// 将用户 ID 转换为字符串格式，用于 API 调用。
// ✅ 正确示例：关键步骤的注释
func (m *myWork) checkAiUseTime(ctx context.Context, userID int64, finished bool, monthsBack int) error {
	// 重置已处理的 ShortID 记录，以确保每次检查都是独立的，避免重复处理。
	m.resetProcessedShortIDs()
	// 将用户 ID 转换为字符串格式，用于 API 调用。
	uid := fmt.Sprintf("%d", userID)
	// 获取当前时间。
	now := time.Now()
	// 计算目标月份：从当前时间往前推 monthsBack 个月。
	targetMonth := now.AddDate(0, -monthsBack, 0)
	// 设置查询时间范围的开始时间为目标月份的第一天。
	timeBeing := time.Date(targetMonth.Year(), targetMonth.Month(), 1, 0, 0, 0, 0, now.Location())
	// 设置查询时间范围的结束时间为目标月份的最后一天的最后一秒。
	timeEnd := timeBeing.AddDate(0, 1, 0).Add(-1 * time.Second)
	// ...
}

// ❌ 错误示例：缺少业务逻辑梳理，注释不够详细
func (m *myWork) checkAiUseTime(ctx context.Context, userID int64, finished bool, monthsBack int) error {
	m.resetProcessedShortIDs()
	uid := fmt.Sprintf("%d", userID)
	now := time.Now()
	targetMonth := now.AddDate(0, -monthsBack, 0)
	timeBeing := time.Date(targetMonth.Year(), targetMonth.Month(), 1, 0, 0, 0, 0, now.Location())
	// ...
}

// ❌ 错误示例：注释过于简略且未以标点结束
func (m *myWork) checkAiUseTime(ctx context.Context, userID int64, finished bool, monthsBack int) error {
	// 重置
	m.resetProcessedShortIDs()
	// 转换
	uid := fmt.Sprintf("%d", userID)
	// 获取时间
	now := time.Now()
	// ...
}
```

**函数体内注释要点**：
- **业务逻辑梳理**：清晰说明每个关键步骤的业务含义
- **数据处理说明**：解释数据转换、计算的目的
- **边界条件**：说明特殊情况的处理逻辑
- **关联关系**：说明与其他模块或函数的关联

### 行内注释规范

**仅在必要时使用行内注释，优先使用前置注释**：

```go
// ✅ 正确示例：前置注释（推荐）
// 计算平均响应时间（毫秒）。
avgResponseTime := sum(responseTimes) / len(responseTimes)

// ✅ 可接受：必要的行内注释
total := calculateTotal(items)  // 包含税费的总金额。
config := load_config(path)      // 从默认路径加载用户配置。

// ❌ 错误示例：不必要的行内注释
count := len(items)              // 获取元素数量
result := process(data)          // 处理数据并返回结果

// ❌ 错误示例：行内注释未以标点结束
total := calculateTotal(items)  // 包含税费的总金额
config := load_config(path)      // 从默认路径加载用户配置
```

**行内注释使用原则**：
- 仅用于解释复杂或非直观的逻辑
- 注释内容简洁明了，必须以标点结束
- 与代码保持适当距离
- 优先使用前置注释而非行尾注释

### 条件分支注释

**复杂条件判断需要说明判断逻辑**：

```go
// ✅ 正确示例：清晰的条件说明
// 如果为根节点（dep == 0），计算百分比并输出信息。
if dep == 0 {
	per := smt / csmt * 100

	// 格式化输出消息。
	msg := fmt.Sprintf("%3d 任务: %s [%3.2f%% %3.2f %3.2f] %s\n", idx, taskID, per, smt, csmt, info.Title)
	// 根据条件着色输出。
	if csmt >= 8 {
		if per >= 60 {
			msg = color.HiYellowString(msg)
		} else if per <= 30 {
			msg = color.HiCyanString(msg)
		}
	}

	fmt.Print(msg)
}

// ❌ 错误示例：缺少条件说明
if dep == 0 {
	per := smt / csmt * 100
	msg := fmt.Sprintf("%3d 任务: %s [%3.2f%% %3.2f %3.2f] %s\n", idx, taskID, per, smt, csmt, info.Title)
	if csmt >= 8 {
		if per >= 60 {
			msg = color.HiYellowString(msg)
		} else if per <= 30 {
			msg = color.HiCyanString(msg)
		}
	}
	fmt.Print(msg)
}
```

### 循环和递归注释

**循环和递归逻辑需要说明处理目的**：

```go
// ✅ 正确示例：说明循环目的
// 递归处理当前子任务。
if nil != info.CurrentChindren {
	for _, child := range info.CurrentChindren {
		csmtc++
		csmt += m.checkAiUseTimeInfo(ctx, child.ID, idx, dep+1)
	}
}
// 递归处理转移子任务。
if nil != info.TransferChildMetaworkInfo {
	for _, child := range info.TransferChildMetaworkInfo {
		csmtc++
		csmt += m.checkAiUseTimeInfo(ctx, child.ID, idx, dep+1)
	}
}

// ❌ 错误示例：缺少循环说明
if nil != info.CurrentChindren {
	for _, child := range info.CurrentChindren {
		csmtc++
		csmt += m.checkAiUseTimeInfo(ctx, child.ID, idx, dep+1)
	}
}
if nil != info.TransferChildMetaworkInfo {
	for _, child := range info.TransferChildMetaworkInfo {
		csmtc++
		csmt += m.checkAiUseTimeInfo(ctx, child.ID, idx, dep+1)
	}
}
```

### 错误处理注释

**错误处理需要说明处理逻辑**：

```go
// ✅ 正确示例：说明错误处理
// 检查上下文是否已取消，如果已取消则返回 0。
if nil != ctx.Err() {
	return 0
}
// 获取任务详细信息。
if info, err := appnd.GetTaskInfo(ctx, taskID); nil != err {
	// 如果获取失败，打印错误信息并返回 0。
	fmt.Printf("错误：%s %s\n", taskID, err)
	return 0
} else {
	// 提取并修剪 ShortID。
	shortID := strings.TrimSpace(info.ShortID)
	// ...
}

// ❌ 错误示例：缺少错误处理说明
if nil != ctx.Err() {
	return 0
}
if info, err := appnd.GetTaskInfo(ctx, taskID); nil != err {
	fmt.Printf("错误：%s %s\n", taskID, err)
	return 0
} else {
	shortID := strings.TrimSpace(info.ShortID)
	// ...
}
```

### 禁止的注释风格

**以下注释风格不允许出现**：

```go
// ❌ 错误：在非 doc.go 文件中添加包级别注释
// Package mywork 提供任务处理功能。
package mywork

// ❌ 错误：缺少 doc.go 文件
// 包下没有 doc.go 文件，但包含多个源文件

// ❌ 错误：doc.go 文件中包含代码实现
// Package mywork 提供任务处理功能。
package mywork

var globalVar = "value"  // doc.go 不应包含代码实现

// ❌ 错误：注释未以标点结束
// 这是一个示例函数
func example() {}

// ❌ 错误：口语化表达
// 这里我们要做的是把数据转换一下
data := transform(input)

// ❌ 错误：过于简略，无实际意义
// 处理
process()

// ❌ 错误：注释与代码不一致
// 获取用户信息
task := getTask(id)  // 实际是获取任务信息

// ❌ 错误：使用英文注释（除非是专有名词）
// Get user information
user := getUser(id)

// ❌ 错误：重复代码信息，无额外价值
// 调用 fmt.Println 打印消息
fmt.Println("message")

// ❌ 错误：非导出函数缺少注释
func processData(data []byte) error {
	// ...
}

// ❌ 错误：实现接口的方法注释与接口不一致
// 执行任务
func (m *myWork) Run(ctx context.Context, taskName string, userID int64, finished bool) error {
	// ...
}

// ❌ 错误：全局相同语义的注释表述不一致
// ctx 上下文对象
func foo(ctx context.Context) error { }
// ctx 请求上下文，用于取消与超时控制
func bar(ctx context.Context) error { }
```

### 注释自检流程

完成代码编写后，执行以下自检步骤，确保注释符合规范。如发现不符合项，必须立即修正。

**1. 包级别注释检查**
- 检查项：每个包是否存在 `doc.go` 文件
- 判定标准：
  - 每个包必须包含一个 `doc.go` 文件
  - `doc.go` 文件必须包含包级别注释，格式为 `// Package <包名> <简短描述>。`
  - `doc.go` 文件只包含 package 声明和注释，不包含任何代码实现
  - 除 `doc.go` 外的所有文件，package 声明前后不得有任何注释
- 不符合处理：
  - 缺少 `doc.go` 文件：创建 `doc.go` 文件并添加包级别注释
  - `doc.go` 包含代码：移除 `doc.go` 中的所有代码实现
  - 其他文件有包注释：删除非 `doc.go` 文件中的包级别注释

**2. 类型定义注释完整性检查**
- 检查范围：所有 interface、struct、type 别名定义
- 判定标准：
  - 每个类型定义必须有功能说明注释
  - interface 的每个方法必须有注释，且包含完整的参数说明和返回值说明
  - struct 的每个字段必须有用途说明注释
- 不符合处理：为缺失注释的类型、方法、字段补充完整注释

**3. 函数和方法注释完整性检查**
- 检查范围：所有 func 声明（包括导出和非导出函数）
- 判定标准：
  - 每个函数必须有功能描述注释
  - 函数有参数时，必须在注释中说明每个参数的用途
  - 函数有返回值时，必须在注释中说明每个返回值的含义
- 不符合处理：为缺失注释的函数补充完整的功能、参数、返回值注释

**4. interface 实现一致性检查**
- 检查范围：所有实现 interface 的 struct 方法
- 判定标准：struct 方法的注释内容必须与 interface 方法的注释完全一致（逐字比对）
- 不符合处理：将 struct 方法的注释修改为与 interface 方法注释完全一致

**5. 函数体内注释检查**
- 检查范围：所有函数的实现代码
- 判定标准：
  - 函数包含业务逻辑时，关键业务步骤必须有说明注释
  - 函数包含复杂条件判断（嵌套 if、多条件组合）时，必须有逻辑说明注释
  - 函数包含循环或递归处理时，必须有处理目的说明注释
  - 函数包含数据转换或计算时，关键变量必须有用途说明注释
- 不符合处理：分析函数的业务逻辑，为缺失注释的关键步骤补充说明注释

**6. 注释语义一致性检查**
- 检查方法：搜索代码库中对相同概念的注释表述
- 判定标准：相同概念的注释必须使用完全一致的表述（例如：所有 context.Context 参数的注释必须统一为"请求上下文，用于取消与超时控制"）
- 不符合处理：将不一致的注释统一修改为标准表述

**7. 注释语言规范性检查**
- 检查范围：所有注释文本
- 判定标准：
  - 注释使用标准现代汉语，无语法错误
  - 注释使用技术专业术语，不包含口语化表达（如"我们"、"这里"、"把...一下"等）
  - 每个注释语句以中文标点符号结束（句号、感叹号等）
- 不符合处理：修改不规范注释，使其符合语言规范标准

**8. 注释准确性检查**
- 检查方法：对照代码实现，验证注释描述是否准确
- 判定标准：注释内容必须准确反映代码的实际功能和行为，不得出现与代码不符的描述
- 不符合处理：修正注释，使其准确描述代码功能

**9. 注释布局规范性检查**
- 检查范围：所有注释的位置和格式
- 判定标准：
  - 类型、函数、方法的注释位于声明的紧邻上方
  - 函数体内逻辑的注释优先使用独立行前置注释
  - 行尾注释仅用于简短说明，且内容简洁
  - 注释的缩进层级与其描述的代码一致
- 不符合处理：调整注释位置和缩进，使其符合布局规范

**自检结果判定**
- 所有检查项均通过：注释符合规范，可以提交代码
- 存在任何检查项不通过：必须修正不符合项，重新执行完整自检流程
- [ ] 注释内容准确反映代码功能
- [ ] 注释使用规范的中文表述
- [ ] 避免了口语化和过于简略的表达
- [ ] 优先使用前置注释而非行尾注释

## 包导入规范

### 基本要求

**格式规范**
- ✅ 所有 import 语句必须使用括号 `()` 包裹。
- ✅ import 按段分组，段与段之间使用空行分隔。
- ✅ 每个段内的包按字母顺序排序。
- ✅ 第三方包需要取别名时，使用有意义的别名，避免冲突。

**分段规则**
- ✅ **第一段**：Go SDK 中的内置包，按字母顺序排列。
- ✅ **第二段**：Github 等第三方包，按字母顺序排列。
- ✅ **第三段**：fsyyft-go 相关的包，主要包括 `fsyyft-go/kit`，都需要取别名，别名前缀为 `kit`，例如 `kitlog`。
- ✅ **第四段**：项目内的相关包，也都需要取别名，别名前缀为 `app`，例如 `appconf`、`applog`。

### 导入示例

**正确示例**：

```go
import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"

	"github.com/fatih/color"
	"github.com/openai/openai-go"
	"github.com/openai/openai-go/option"
	"github.com/openai/openai-go/packages/param"

	kitlog "github.com/fsyyft-go/kit/log"

	appconf "metawork-extend/internal/pkg/conf"
	appai "metawork-extend/pkg/ai"
	appnd "metawork-extend/pkg/nd"
)
```

**错误示例**：

```go
// ❌ 错误：未使用括号包裹
import "context"
import "fmt"

// ❌ 错误：未分段，未排序
import (
	"github.com/fatih/color"
	"context"
	kitlog "github.com/fsyyft-go/kit/log"
	appconf "metawork-extend/internal/pkg/conf"
	"fmt"
)

// ❌ 错误：fsyyft-go 包未取别名
import (
	"github.com/fsyyft-go/kit/log"
)

// ❌ 错误：项目内包未取别名
import (
	"metawork-extend/internal/pkg/conf"
)

// ❌ 错误：项目内包未强制使用 app 前缀别名
import (
	"metawork-extend/internal/pkg/conf"
	ai "metawork-extend/pkg/ai"
)
```

### 别名规范

**fsyyft-go 包别名**：
- 所有 `fsyyft-go/kit` 下的包必须取别名，格式为 `kit[packagename]`，其中 `packagename` 为包名，例如：
  - `github.com/fsyyft-go/kit/log` → `kitlog`
- 其他 `fsyyft-go` 下的包（如 `fsyyft-go/abc`）取别名格式为 `[abc][packagename]`，例如 `abclog`。
- 保留第三段独立是强制的，别名全部使用小写字母。

**项目内包别名**：
- 所有项目内包必须强制取别名，格式为 `app[packagename]`，其中 `packagename` 为包名，例如：
  - `metawork-extend/internal/pkg/conf` → `appconf`
  - `metawork-extend/pkg/ai` → `appai`
  - `metawork-extend/pkg/nd` → `appnd`
- 别名全部使用小写字母。

### 检查清单

编写代码后，检查 import 是否符合以下要求：

- [ ] import 使用括号包裹
- [ ] 按段分组，段间有空行
- [ ] 第一段：Go 内置包，按字母排序
- [ ] 第二段：第三方包，按字母排序
- [ ] 第三段：fsyyft-go 包，取相应前缀别名（如 kitlog、abclog），全小写
- [ ] 第四段：项目内包，强制取 app 前缀别名（如 appconf、appai），全小写
- [ ] 每个段内按字母顺序排序