// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package web 提供 Web 应用的启动和管理功能。
//
// 本包包含 Web 应用的入口函数、配置解析、系统服务管理等功能。
// 支持前台运行、系统服务安装卸载等多种运行模式。
//
// 主要功能：
//   - Web 服务启动与配置加载
//   - 优雅关闭与信号处理
//   - 系统服务安装卸载
//   - 命令行参数解析
//
// 使用示例：
//
//	// 启动 Web 应用
//	web.Run()
//
//	// 安装为系统服务
//	web.Run()  // 使用 install 子命令
//
//	// 指定配置文件
//	web.Run()  // 使用 --config 参数
package web
