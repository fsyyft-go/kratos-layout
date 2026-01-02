#!/bin/bash
set -e

# =====================================================
# Ubuntu Go 安装脚本
# =====================================================

# Go 版本号（需要指定，例如：go1.25.5）
GO_VERSION="${GO_VERSION:-go1.25.5}"

echo "Starting Go installation..."
echo "Go version: $GO_VERSION"

# 1. 从国内镜像下载指定版本的安装包到 /tmp 目录
GO_INSTALLER="${GO_VERSION}.linux-amd64.tar.gz"
DOWNLOAD_URL="https://mirrors.aliyun.com/golang/${GO_INSTALLER}"

echo "Downloading from: $DOWNLOAD_URL"
cd /tmp
curl -LO "$DOWNLOAD_URL"

# 2. 把安装包解压到 /usr/local/下，例如：/usr/local/go1.25.5
echo "Extracting Go to /usr/local/${GO_VERSION}..."
 mkdir -p /usr/local
 tar -C /usr/local -xzf "$GO_INSTALLER"
 mv /usr/local/go "/usr/local/${GO_VERSION}"

# 3. 建立软链接 /usr/local/go 指向到 /usr/local/go1.25.5
echo "Creating symlink /usr/local/go -> /usr/local/${GO_VERSION}..."
 ln -sf "/usr/local/${GO_VERSION}" /usr/local/go

# 4. 建立软链接 /usr/local/bin/go 到 /usr/local/go/bin/go
echo "Creating symlink /usr/local/bin/go -> /usr/local/go/bin/go..."
 ln -sf /usr/local/go/bin/go /usr/local/bin/go
 ln -sf /usr/local/go/bin/gofmt /usr/local/bin/gofmt

# 清理下载的安装包
echo "Cleaning up..."
rm -f "/tmp/${GO_INSTALLER}"

# 验证安装
echo "Verifying installation..."
/usr/local/bin/go version

echo "Go installation completed successfully!"
echo "Go version: $(/usr/local/bin/go version)"
echo "Go installed at: /usr/local/${GO_VERSION}"
echo "Symlink: /usr/local/go -> /usr/local/${GO_VERSION}"

# 安装 Go 常用工具。
echo "Installing Go development tools..."
go env -w GOPROXY=https://goproxy.cn,https://mirrors.aliyun.com/goproxy/,direct
go env GOPROXY

# 禁用 CGO 以避免交叉编译问题
# 大多数 Go 工具不需要 CGO，禁用可以加速编译并避免平台依赖
export CGO_ENABLED=0

# 调试选项（默认禁用以减少输出量，需要时取消注释）
# export GODEBUG=gctrace=0
# 输出编译过程的每个包名，显示执行的每个命令，会占用大量的日志缓冲区，可能出现：output clipped log limit 2Mib reached。
# export GOFLAGS="-v -x"

# =====================================================
# 安装 Go 开发工具
# =====================================================

# 1. 代码格式化和检查工具
echo "==> 安装格式化工具..."
go install golang.org/x/tools/cmd/goimports@v0.40.0
go install mvdan.cc/gofumpt@v0.9.2
go install github.com/mitchellh/gox@v1.0.1

# 2. Lint 和静态分析工具
echo "==> 安装 Lint 工具..."
go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.64.8
go install honnef.co/go/tools/cmd/staticcheck@v0.6.1
go install github.com/kisielk/errcheck@v1.9.0
go install github.com/go-critic/go-critic/cmd/go-critic@v0.14.2

# 3. 测试和覆盖率工具
echo "==> 安装测试工具..."
go install github.com/onsi/ginkgo/v2/ginkgo@v2.27.3
go install gotest.tools/gotestsum@v1.13.0

# 4. 代码生成工具
echo "==> 安装代码生成工具..."
go install github.com/golang/mock/mockgen@v1.6.0
go install github.com/google/wire/cmd/wire@v0.7.0
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.36.11
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.6.0
go install github.com/envoyproxy/protoc-gen-validate@v1.3.0
go install github.com/google/gnostic/cmd/protoc-gen-openapi@v0.7.1

# 5. Kratos 框架工具，不能使用指定版本号的方式安装。
echo "==> 安装 Kratos 工具..."
go install github.com/go-kratos/kratos/cmd/kratos/v2@latest
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@latest
go install github.com/go-kratos/kratos/cmd/protoc-gen-go-errors/v2@latest

# 6. 调试和性能分析工具
echo "==> 安装调试工具..."
go install github.com/go-delve/delve/cmd/dlv@v1.26.0
go install github.com/google/pprof@latest

# 7. 构建和依赖管理工具
echo "==> 安装构建工具..."
# goreleaser 在 Go 1.25.5 上有兼容性问题，暂时移除，待手动处理后再添加。
# go install github.com/goreleaser/goreleaser@latest
go install github.com/pressly/goose/v3/cmd/goose@v3.26.0

# 8. 安全扫描工具
echo "==> 安装安全工具..."
go install golang.org/x/vuln/cmd/govulncheck@v1.1.4
go install github.com/securego/gosec/v2/cmd/gosec@v2.22.11
# 找不到工具，暂时移除，待手动处理后再添加。
# go install github.com/sonatypecommunity/nancy@latest

# 9. API 和文档工具
echo "==> 安装 API 工具..."
go install github.com/swaggo/swag/cmd/swag@v1.16.6
go install github.com/deepmap/oapi-codegen/cmd/oapi-codegen@latest

# 10. CLI 开发工具
echo "==> 安装 CLI 工具..."
go install github.com/spf13/cobra-cli@v1.3.0
# 找不到工具，暂时移除，待手动处理后再添加。
# go install github.com/muesli/termenv/cmd/genaccent@v0.16.0

echo "==> 所有工具安装完成！"

# 修改文件所有者。
chown -R fsyyft /usr/local/go/