// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package biz 提供业务逻辑层的用例实现。
//
// 本包定义了业务逻辑的核心接口和实现，包括数据仓储接口、
// 用例接口以及领域模型定义。
//
// 主要组件：
//   - GreeterRepo：Greeter 实体的数据仓储接口
//   - GreeterUsecase：Greeter 业务用例接口
//   - Greeter：领域模型（问候语实体）
//
// 架构特点：
//   - 依赖于仓储层进行数据访问
//   - 提供清晰的业务逻辑抽象
//   - 支持依赖注入框架（Wire）集成
//
// 使用示例：
//
//	// 创建用例实例
//	usecase := biz.NewGreeterUsecase(logger, conf, repo)
//
//	// 执行业务操作
//	greeter, err := usecase.CreateGreeter(ctx, &biz.Greeter{Hello: "Hello"})
package biz
