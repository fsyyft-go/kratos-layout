// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.
package web

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/go-kratos/kratos/v2"
	"github.com/google/wire"

	// 模板：下面这条导入，应用时需要修改。
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
	applog "github.com/fsyyft-go/kratos-layout/internal/pkg/log"
	appserver "github.com/fsyyft-go/kratos-layout/internal/server"
)

// ProviderSet 是 wire 的依赖注入提供者集合。
// 包含了创建应用实例所需的所有依赖。
var ProviderSet = wire.NewSet(
	applog.NewLogger,
	newApp,
)

var (
	name  = "kratos-layout"
	id, _ = os.Hostname()
)

func newApp(hs appserver.WebServer) *kratos.App {
	a := kratos.New(
		kratos.ID(id),
		kratos.Name(name),
		kratos.Server(
			hs,
		),
	)
	return a
}

// Run 是 Web 应用的主入口。
//
// 主要流程：
//  1. 解析命令行参数，识别并分发子命令（install、uninstall、run、help 等）。
//  2. 若为 install/uninstall，调用对应处理函数后退出。
//  3. 若为 run 或无子命令，则进入前台运行模式，调用 run() 启动服务。
//
// 该函数确保所有业务逻辑只在前台模式下启动，服务管理命令与业务解耦。
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

// run 以前台模式启动 Web 服务。
//
// 主要流程：
//  1. 解析配置文件路径参数（支持 run/无子命令等多种用法）。
//  2. 加载配置文件，失败则直接退出。
//  3. 创建 context 并监听 SIGINT/SIGTERM，实现优雅关闭。
//  4. 通过 wireWeb 初始化 WebServer 实例。
//  5. 启动 WebServer，主 goroutine 阻塞直到收到信号。
func run() {
	// 解析配置文件路径参数（兼容 run/无子命令等多种用法）。
	configPath := parseConfigFlag()

	// 加载配置文件。
	cfg, err := appconf.LoadConfig(configPath)
	if nil != err {
		fmt.Printf("加载配置文件失败：%v", err)
		return
	}

	// 创建可取消的 context，用于优雅关闭。
	_, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 监听系统信号（SIGINT/SIGTERM），用于优雅关闭。
	signalChan := make(chan os.Signal, 1)
	signal.Notify(signalChan, syscall.SIGINT, syscall.SIGTERM)

	// 信号处理 goroutine，收到信号后取消 context。
	go func() {
		sig := <-signalChan
		fmt.Printf("接收到系统信号: %v\n", sig)
		cancel()
	}()

	// 通过 Wire 框架生成的 wireWeb 函数初始化服务。
	// 该函数会自动注入所有依赖项并返回配置好的 Web 服务器实例。
	if w, cleanup, err := wireWeb(cfg); nil != err {
		fmt.Printf("初始化失败：%v", err)
		// 调用清理函数释放已分配的资源。
		cleanup()
	} else if err := w.Run(); err != nil {
		panic(err)
	}
}
