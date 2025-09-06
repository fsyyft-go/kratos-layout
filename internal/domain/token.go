// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package domain 实现了系统的核心领域模型。
// 该包包含了业务实体、值对象和领域服务的定义，用于实现系统的核心业务逻辑。
package domain

import (
	"time"

	"github.com/golang-jwt/jwt"
)

// Token 是一个值对象，用于表示系统中的认证令牌。
// 包含访问令牌、刷新令牌和过期时间等基本信息。
type Token struct {
	// 访问令牌，用于用户身份验证和授权。
	AccessToken string
	// 刷新令牌，用于在访问令牌过期时获取新的访问令牌。
	RefreshToken string
	// 过期时间，表示访问令牌的有效期限。
	ExpiresAt time.Time
}

// TokenClaims 定义了 JWT token 的声明结构。
// 继承自 jwt.StandardClaims，添加了用户相关的自定义字段。
type TokenClaims struct {
	// 用户唯一标识。
	UserID string `json:"user_id"`
	// 用户名称。
	Username string `json:"username"`
	jwt.StandardClaims
}

// NewToken 创建一个新的 Token 实例。
// 参数：
//   - userID: 用户唯一标识
//   - username: 用户名称
//   - secret: 用于签名的密钥
//   - expiration: token 的有效期时长
//
// 返回：
//   - *Token: 生成的 token 实例
//   - error: 错误信息，如果有的话
func NewToken(userID, username string, secret string, expiration time.Duration) (*Token, error) {
	// 创建包含用户信息的 JWT Claims。
	claims := TokenClaims{
		UserID:   userID,
		Username: username,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(expiration).Unix(),
			IssuedAt:  time.Now().Unix(),
		},
	}

	// 使用 HS256 算法创建新的 JWT token。
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	// 使用密钥对 token 进行签名。
	accessToken, err := token.SignedString([]byte(secret))
	if err != nil {
		return nil, err
	}

	// 生成用于刷新的令牌。
	refreshToken, err := generateRefreshToken()
	if err != nil {
		return nil, err
	}

	// 返回完整的 Token 实例。
	return &Token{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
		ExpiresAt:    time.Now().Add(expiration),
	}, nil
}

// generateRefreshToken 生成刷新令牌。
// 返回：
//   - string: 生成的刷新令牌
//   - error: 错误信息，如果有的话
func generateRefreshToken() (string, error) {
	// TODO：实现刷新令牌生成逻辑。
	return "refresh_token", nil
}
