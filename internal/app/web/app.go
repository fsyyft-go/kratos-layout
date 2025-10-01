// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package web 提供了 Web 应用程序的入口点和运行时管理，包括配置加载、服务启动和信号处理。
package web

import (
	"context"
	"flag"
	"fmt"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/google/wire"

	// 模板：下面这条导入，应用时需要修改。
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
	applog "github.com/fsyyft-go/kratos-layout/internal/pkg/log"
)

// ProviderSet 是 wire 的依赖注入提供者集合。
// 包含了创建应用实例所需的所有依赖。
var ProviderSet = wire.NewSet(
	applog.NewLogger,
)

// Run 启动并运行Web服务器。
// 该函数负责：
//   - 解析命令行参数
//   - 加载配置文件
//   - 设置信号处理
//   - 初始化并启动服务
func Run() {
	// 检查是否有子命令。
	if len(os.Args) > 1 {
		subCommand := os.Args[1]
		switch subCommand {
		case "install":
			handleInstallCommand()
			return
		case "uninstall":
			handleUninstallCommand()
			return
		case "status":
			handleStatusCommand()
			return
		case "run":
			// 显式运行命令，继续执行下面的逻辑。
		case "--help", "-h", "help":
			printUsage()
			return
		default:
			// 如果是未知命令但不是以 - 开头的 flag，显示帮助。
			if !strings.HasPrefix(subCommand, "-") {
				fmt.Printf("未知命令: %s\n\n", subCommand)
				printUsage()
				return
			}
			// 否则当作普通的 flag 处理，继续执行。
		}
	}

	// 原有的前台运行逻辑。
	run()
}

// run 前台运行 Web 服务（开发模式或容器模式）。
func run() {
	// 解析配置文件路径参数（兼容原有命令行参数）。
	configPath := parseConfigFlagForRun()

	// 从指定路径加载配置文件。
	cfg, err := appconf.LoadConfig(configPath)
	if nil != err {
		fmt.Printf("加载配置文件失败：%v", err)
		return
	}

	// 增加监听操作系统信号，以优雅地关闭服务器。
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 创建信号通道。
	signalChan := make(chan os.Signal, 1)
	// 监听 SIGINT 和 SIGTERM 信号。
	signal.Notify(signalChan, syscall.SIGINT, syscall.SIGTERM)

	// 在单独的 goroutine 中处理信号。
	go func() {
		sig := <-signalChan
		fmt.Printf("接收到系统信号: %v\n", sig)
		cancel() // 取消上下文。
	}()

	// 通过 Wire 框架生成的 wireServer 函数初始化服务。
	// 该函数会自动注入所有依赖项并返回配置好的 Web 服务器实例。
	if task, cleanup, err := wireWeb(cfg); nil != err {
		fmt.Printf("初始化失败：%v", err)
		// 调用清理函数释放已分配的资源。
		cleanup()
	} else {
		// 启动 Web 服务器。
		_ = task.Start(ctx)
	}
}

// parseConfigFlagForRun 解析用于 run 命令的配置文件路径参数（向后兼容原有用法）
func parseConfigFlagForRun() string {
	var configPath string

	// 如果第一个参数是子命令 "run"，则跳过它
	var args []string
	if len(os.Args) > 1 && os.Args[1] == "run" {
		args = os.Args[2:]
	} else {
		// 向后兼容：如果没有子命令，直接解析所有参数
		args = os.Args[1:]
	}

	// 创建一个新的 FlagSet
	fs := flag.NewFlagSet(os.Args[0], flag.ExitOnError)
	fs.StringVar(&configPath, "config", "configs/config.yaml", "配置文件路径")
	fs.Parse(args)

	return configPath
}
