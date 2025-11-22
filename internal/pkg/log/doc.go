// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package log 提供日志系统的初始化和管理。
//
// 本包使用 fsyyft-go/kit 库提供统一的日志接口，支持多种日志输出
// 格式和日志级别的动态配置。使用单例模式确保全局日志记录器的唯一性。
//
// 主要功能：
//   - 日志记录器的初始化
//   - 日志级别的配置
//   - 日志输出格式的配置
//   - 全局日志记录器管理
//
// 支持的日志类型：
//   - logrus：基于 logrus 的日志实现
//   - 可扩展支持其他日志库
//
// 支持的日志级别：
//   - debug：调试信息
//   - info：普通信息
//   - warn：警告信息
//   - error：错误信息
//
// 使用示例：
//
//	// 创建日志记录器
//	logger, cleanup, err := log.NewLogger(conf)
//	defer cleanup()
//
//	// 记录日志
//	logger.Info("Server started")
//	logger.Error("Connection failed", err)
package log
