// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package task

import (
	"context"
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

// Run 是 Task 应用的主入口。
//
// 主要流程：
//  1. 解析命令行参数，识别并分发子命令（install、uninstall、run、help 等）。
//  2. 若为 install/uninstall，调用对应处理函数后退出。
//  3. 若为 run 或无子命令，则进入前台运行模式，调用 run() 启动服务。
//
// 该函数确保所有业务逻辑只在前台模式下启动，服务管理命令与业务解耦。
func Run() {
	if len(os.Args) > 1 {
		subCommand := os.Args[1]
		switch subCommand {
		case "install":
			handleInstallCommand()
			return
		case "uninstall":
			handleUninstallCommand()
			return
		case "run":
			// 显式运行命令，继续执行下面的逻辑。
		case "--help", "-h", "help":
			printUsage()
			return
		default:
			if !strings.HasPrefix(subCommand, "-") {
				fmt.Printf("未知命令: %s\n\n", subCommand)
				printUsage()
				return
			}
			// 否则当作普通的 flag 处理，继续执行。
		}
	}

	run()
}

// run 以前台模式启动 Task 服务。
//
// 主要流程：
//  1. 解析配置文件路径参数（支持 run/无子命令等多种用法）。
//  2. 加载配置文件，失败则直接退出。
//  3. 创建 context 并监听 SIGINT/SIGTERM，实现优雅关闭。
//  4. 通过 wireTask 初始化 Task 实例。
//  5. 启动 Task，主 goroutine 阻塞直到收到信号。
func run() {
	configPath := parseConfigFlag()

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
	if task, cleanup, err := wireTask(cfg); nil != err {
		fmt.Printf("初始化失败：%v", err)
		// 调用清理函数释放已分配的资源。
		cleanup()
	} else {
		// 启动 Web 服务器。
		_ = task.Run(ctx)
	}
}
