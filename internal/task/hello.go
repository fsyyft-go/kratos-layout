// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package task

import (
	"context"
	"fmt"

	"github.com/fsyyft-go/kit/log"

	// 模板：下面这条导入，应用时需要修改。
	"github.com/fsyyft-go/kratos-layout/internal/config"
)

type (
	// Hello 定义了 Hello 任务的接口。
	Hello interface {
		// Run 执行 Hello 任务。
		Run(ctx context.Context) error
	}

	// hello 实现了 Hello 接口。
	hello struct {
		// logger 用于记录任务执行过程中的日志信息。
		logger log.Logger
		// cfg 存储应用配置信息。
		cfg *config.Config
	}
)

// NewHello 创建一个新的 Hello 实例。
//
// 参数:
//   - logger: 用于记录日志的 logger 实例。
//   - cfg: 应用配置信息。
//
// 返回值:
//   - Hello: 一个新的 Hello 实例。
//   - error: 创建实例过程中可能发生的错误。
func NewHello(logger log.Logger, cfg *config.Config) (Hello, error) {
	return &hello{logger: logger, cfg: cfg}, nil
}

// Run 执行 Hello 任务。
//
// 参数:
//   - ctx: 上下文。
//
// 返回值:
//   - error: 执行过程中可能发生的错误。
func (h *hello) Run(ctx context.Context) error {
	fmt.Println("Hello Run")
	return nil
}
