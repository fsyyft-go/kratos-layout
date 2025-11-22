// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package data 提供数据访问层的实现。
//
// 本包实现了业务层定义的仓储接口，负责与数据源的交互。
// 当前实现为模拟层，可根据需要扩展为真实数据库访问。
//
// 主要功能：
//   - 实现 GreeterRepo 接口
//   - 数据的 CRUD 操作（保存、更新、查询）
//   - 数据层资源管理
//
// 依赖关系：
//   - 依赖业务层定义的 Greeter 实体和仓储接口
//   - 提供给服务层使用
//
// 扩展建议：
//   - 集成真实数据库驱动（如 MySQL、PostgreSQL）
//   - 实现事务管理
//   - 添加缓存层支持
//
// 使用示例：
//
//	// 创建数据层实例
//	repo := data.NewGreeterRepo(logger, conf, dataLayer)
//
//	// 保存 Greeter 实体
//	greeter, err := repo.Save(ctx, &biz.Greeter{Hello: "Hello"})
package data
