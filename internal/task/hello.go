// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package task

import (
	"context"
	"fmt"
	"time"

	kitconfig "github.com/fsyyft-go/kit/config"
	kitlog "github.com/fsyyft-go/kit/log"

	// 模板：下面这条导入，应用时需要修改。
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
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
		logger kitlog.Logger
		// cfg 存储应用配置信息。
		cfg *appconf.Config
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
func NewHello(logger kitlog.Logger, cfg *appconf.Config) (Hello, error) {
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
	fmt.Print(kitconfig.CurrentVersion.Description())
	ticker := time.NewTicker(time.Minute)
FOR:
	for {
		select {
		case <-ctx.Done():
			break FOR
		case <-ticker.C:
			h.logger.Info("Hello World!")
		}
	}

	return ctx.Err()
}
