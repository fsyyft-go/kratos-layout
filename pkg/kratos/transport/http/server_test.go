// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package http

import (
	"testing"
)

// TestParsePath 测试 Mux 路由到 Gin 路由的转换。
func TestParsePath(t *testing.T) {
	// 定义测试用例。
	tests := []struct {
		name     string // 测试用例名称
		input    string // 输入的 Mux 路由
		expected string // 期望的 Gin 路由
	}{
		// 基本路径测试
		{
			name:     "空路径",
			input:    "",
			expected: "/",
		},
		{
			name:     "根路径",
			input:    "/",
			expected: "/",
		},
		{
			name:     "简单路径",
			input:    "/users",
			expected: "/users",
		},
		{
			name:     "不带前导斜杠的路径",
			input:    "users",
			expected: "/users",
		},

		// 参数路径测试
		{
			name:     "单个参数路径",
			input:    "/users/{id}",
			expected: "/users/:id",
		},
		{
			name:     "多个参数路径",
			input:    "/users/{id}/posts/{postId}",
			expected: "/users/:id/posts/:postId",
		},
		{
			name:     "简单正则参数",
			input:    "/users/{name:[a-z]+}",
			expected: "/users/:name",
		},
		{
			name:     "多层嵌套路径",
			input:    "/api/v1/users/{userId}/posts/{postId}",
			expected: "/api/v1/users/:userId/posts/:postId",
		},

		// 特殊情况测试
		{
			name:     "多个连续斜杠",
			input:    "///users///{id}///",
			expected: "/users/:id/",
		},
		{
			name:     "点号路径",
			input:    "/api/{version}/files/{filename}.{ext}",
			expected: "/api/:version/files/:filename.:ext",
		},
		{
			name:     "带下划线和连字符的参数",
			input:    "/users/{user_id}/{user-name}",
			expected: "/users/:user_id/:user-name",
		},
	}

	// 执行测试用例。
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// 获取实际结果。
			got := parsePath(tt.input)

			// 比较实际结果和期望结果。
			if got != tt.expected {
				t.Errorf("parsePath() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestParsePathBenchmark 基准测试。
func BenchmarkParsePath(b *testing.B) {
	paths := []string{
		"/users/{id}",
		"/api/v1/users/{userId}/posts/{postId}",
		"/users/{name:[a-z]+}",
		"/api/{version}/files/{filename}.{ext}",
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		for _, path := range paths {
			parsePath(path)
		}
	}
}
