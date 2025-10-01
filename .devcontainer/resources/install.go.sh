#!/bin/bash
set -e

# 安装 Go 常用工具。
echo "Installing Go development tools..."
go env -w GOPROXY=https://goproxy.cn,https://mirrors.aliyun.com/goproxy/,direct
go env GOPROXY

# 安装漏洞检查工具。
go install golang.org/x/vuln/cmd/govulncheck@latest

# 安装 Protocol Buffers 的 Go 语言代码生成器。
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

# 安装 gRPC 的 Go 语言代码生成器。
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# 安装 Kratos 命令行工具。
go install github.com/go-kratos/kratos/cmd/kratos/v2@latest

# 安装 Kratos HTTP 服务代码生成器。
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@latest

# 安装 Protocol Buffers 验证代码生成器。
go install github.com/envoyproxy/protoc-gen-validate@latest

# 安装 Kratos 错误代码生成器。
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-errors/v2@latest

# 安装 OpenAPI（Swagger）文档生成器。
go install github.com/google/gnostic/cmd/protoc-gen-openapi@latest

# 安装 Go 语言代码质量检查工具。
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# 安装依赖注入代码生成工具。
go install github.com/google/wire/cmd/wire@latest

echo "Go tools installation completed."