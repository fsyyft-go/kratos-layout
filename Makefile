INTERNAL_CONF_PROTO_FILES=$(shell find internal/conf -name *.proto)

.PHONY: init
init:
	go install golang.org/x/vuln/cmd/govulncheck@latest
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	go install github.com/go-kratos/kratos/cmd/kratos/v2@latest
	go install github.com/go-kratos/kratos/cmd/protoc-gen-go-http/v2@latest
	go install github.com/envoyproxy/protoc-gen-validate@latest
	go install github.com/go-kratos/kratos/cmd/protoc-gen-go-errors/v2@latest
	go install github.com/google/gnostic/cmd/protoc-gen-openapi@latest
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install github.com/google/wire/cmd/wire@latest

.PHONY: config
config:
	protoc --proto_path=. \
	       --proto_path=./api/third_party \
 	       --go_out=paths=source_relative:. \
	       $(INTERNAL_CONF_PROTO_FILES)

.PHONY: generate
generate:
	go mod tidy
	go generate ./...

# 运行性能测试。
# 使用 -bench 标志运行基准测试。
# 使用 -benchmem 标志显示内存分配统计。

# 运行基本的代码质量检查。
# 使用 golangci-lint 进行静态代码分析。
# 设置 3 分钟超时时间。
.PHONY: lint
lint:
	golangci-lint run --timeout=3m

# 运行严格的代码质量检查。
# 启用所有 linter。
# 增加检查严格程度。
# 设置 5 分钟超时时间。
.PHONY: lint-strict
lint-strict:
	golangci-lint run --timeout=5m --enable-all --exclude-use-default=false

.PHONY: build
build:
	mkdir -p bin/linux_arm64   && CGO_ENABLED=0 GOOS=linux   GOARCH=arm64 go build -o bin/linux_arm64/   ./...
	mkdir -p bin/linux_amd64   && CGO_ENABLED=0 GOOS=linux   GOARCH=amd64 go build -o bin/linux_amd64/   ./...
	mkdir -p bin/darwin_arm64  && CGO_ENABLED=0 GOOS=darwin  GOARCH=arm64 go build -o bin/darwin_arm64/  ./...
	mkdir -p bin/darwin_amd64  && CGO_ENABLED=0 GOOS=darwin  GOARCH=amd64 go build -o bin/darwin_amd64/  ./...
	mkdir -p bin/windows_arm64 && CGO_ENABLED=0 GOOS=windows GOARCH=arm64 go build -o bin/windows_arm64/ ./...
	mkdir -p bin/windows_amd64 && CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o bin/windows_amd64/ ./...
	mkdir -p logs && rm -rf logs/upx.log && for exec in ./bin/linux_*/* ./bin/windows_*/*; do upx -9 $$exec >> logs/upx.log || break ; done