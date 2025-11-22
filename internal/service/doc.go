// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package service 提供应用服务层的实现。
//
// 本包实现了 gRPC 服务接口，负责将业务用例暴露为 RPC 接口。
// 处理请求的转换、业务逻辑的调用以及响应的格式化。
//
// 主要功能：
//   - gRPC 服务的实现
//   - 业务用例的编排
//   - 请求/响应的转换
//   - 错误处理和转换
//
// 实现的服务：
//   - GreeterService：问候服务的 gRPC 实现
//
// 架构特点：
//   - 依赖业务层的用例接口
//   - 负责 gRPC 协议层的处理
//   - 实现请求的输入输出验证
//
// 使用示例：
//
//	// 创建服务实例
//	svc := service.NewGreeterService(usecase)
//
//	// 服务会自动注册到 gRPC 服务器
//	// 通过 gRPC 调用服务方法
package service
