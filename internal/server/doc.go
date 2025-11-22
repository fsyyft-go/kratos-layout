// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package server 提供 HTTP 和 gRPC 服务器的实现。
//
// 本包包含服务器的初始化、配置、中间件设置等功能。
// 基于 Kratos 框架实现，支持灵活的路由和中间件扩展。
//
// 主要组件：
//   - WebServer：HTTP 服务器实现
//   - 中间件链：恢复、验证、日志等
//   - 依赖注入提供者（Wire ProviderSet）
//
// 中间件功能：
//   - Recovery：捕获 panic 并返回错误响应
//   - Validator：请求参数验证
//   - 自定义验证回调
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
//
//	// 停止服务器
//	srv.Stop(ctx)
package server
