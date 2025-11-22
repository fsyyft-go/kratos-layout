// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package conf 提供应用配置管理功能。
//
// 本包负责应用配置的加载、解析和验证。支持 YAML 和 Protobuf
// 格式的配置文件，并实现配置的安全验证（如路径遍历防护）。
//
// 主要功能：
//   - 配置文件加载与解析
//   - 路径安全性验证
//   - 配置结构定义（通过 Protobuf）
//
// 配置结构：
//   - Log：日志系统配置
//   - Server：服务器配置（HTTP、gRPC）
//   - 扩展：可根据需要添加更多配置项
//
// 支持的格式：
//   - YAML（config.yaml）
//   - Protobuf（config.proto）
//
// 使用示例：
//
//	// 加载配置文件
//	cfg, err := conf.LoadConfig("configs/config.yaml")
//	if err != nil {
//	    log.Fatal(err)
//	}
//
//	// 访问配置项
//	serverAddr := cfg.GetServer().GetHttp().GetAddr()
package conf
