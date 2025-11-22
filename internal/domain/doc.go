// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package domain 提供领域模型和业务实体定义。
//
// 本包定义了系统中的核心领域模型，包括实体、值对象和
// 业务逻辑相关的辅助类型。这些定义是系统业务逻辑的基础。
//
// 主要内容：
//   - Token：JWT token 的定义和操作
//   - TokenClaims：Token 中包含的声明信息
//   - 相关常量与配置
//
// 设计原则：
//   - 领域模型独立于框架和数据库
//   - 包含业务逻辑的实现（如 token 生成、签名）
//   - 与其他层解耦
//
// 使用示例：
//
//	// 创建 token
//	token, err := domain.NewToken(secret, userID, expiration)
//
//	// Token 中包含的标准声明
//	claims := token.Claims
package domain
