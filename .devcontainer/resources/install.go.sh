#!/bin/bash
set -e

# 安装 Go 常用工具。
echo "Installing Go development tools..."
go env -w GOPROXY=https://goproxy.cn,https://mirrors.aliyun.com/goproxy/,direct
go env GOPROXY

# 安装 Kratos 命令行工具（使用伪版本号，对应 v2.9.0）。
# 获取伪版本：go list -m github.com/go-kratos/kratos/cmd/kratos/v2@latest
go install github.com/go-kratos/kratos/cmd/kratos/v2@v2.0.0-20251015020953-cdff24709025

# 安装 Kratos HTTP 服务代码生成器（使用伪版本号，对应 v2.9.0）。
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@v2.0.0-20251015020953-cdff24709025

# 安装 Kratos 错误代码生成器（使用伪版本号，对应 v2.9.0）。
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-errors/v2@v2.0.0-20251015020953-cdff24709025

# 安装 Protocol Buffers 的 Go 语言代码生成器。
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.36.10

# 安装 gRPC 的 Go 语言代码生成器。
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.5.1

# 安装 Protocol Buffers 验证代码生成器。
go install github.com/envoyproxy/protoc-gen-validate@v1.2.1

# 安装 OpenAPI（Swagger）文档生成器。
go install github.com/google/gnostic/cmd/protoc-gen-openapi@v0.7.0

# 安装漏洞检查工具。
go install golang.org/x/vuln/cmd/govulncheck@v1.1.4

# 安装 Go 语言代码质量检查工具。
go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.64.8

# 安装依赖注入代码生成工具。
go install github.com/google/wire/cmd/wire@v0.7.0

echo "Go tools installation completed."