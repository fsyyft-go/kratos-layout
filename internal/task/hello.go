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
	// 输出当前版本信息，作为任务启动的标识。
	fmt.Print(kitconfig.CurrentVersion.Description())
	// 创建一个每分钟触发一次的定时器，用于周期性执行任务。
	ticker := time.NewTicker(time.Minute)
FOR:
	// 进入无限循环，等待定时器触发或上下文取消。
	for {
		select {
		// 监听上下文取消信号，当收到取消信号时退出循环。
		case <-ctx.Done():
			break FOR
		// 监听定时器通道，每分钟执行一次日志输出。
		case <-ticker.C:
			h.logger.Info("Hello World!")
		}
	}

	// 返回上下文的错误信息，通常是上下文取消的原因。
	return ctx.Err()
}
