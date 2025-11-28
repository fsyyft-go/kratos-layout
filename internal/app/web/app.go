// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.
package web

import (
	"context"
	"fmt"
	"net/url"
	"os"
	"os/signal"
	"strings"
	"syscall"

	kratosnacos "github.com/go-kratos/kratos/contrib/registry/nacos/v2"
	"github.com/go-kratos/kratos/v2"
	kratoslog "github.com/go-kratos/kratos/v2/log"
	"github.com/google/wire"
	kratosnacosclients "github.com/nacos-group/nacos-sdk-go/clients"
	kratosnacosconstant "github.com/nacos-group/nacos-sdk-go/common/constant"
	kratosnacosvo "github.com/nacos-group/nacos-sdk-go/vo"

	kitlog "github.com/fsyyft-go/kit/log"

	// 模板：下面这条导入，应用时需要修改。
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
	applog "github.com/fsyyft-go/kratos-layout/internal/pkg/log"
	appserver "github.com/fsyyft-go/kratos-layout/internal/server"
)

// ProviderSet 是 wire 的依赖注入提供者集合。
// 包含了创建应用实例所需的所有依赖。
var ProviderSet = wire.NewSet(
	applog.NewLogger,
	applog.NewKratosLogger,
	newApp,
)

var (
	// name 存储应用的名称，用于标识当前应用实例。
	name = "kratos-layout"
	// id 存储主机名，用于唯一标识应用实例。
	id, _ = os.Hostname()
)

// newApp 创建并配置 Kratos 应用实例。
// 参数：
//   - ctx：请求上下文，用于取消与超时控制。
//   - logger：日志记录器，用于记录应用生命周期事件。
//   - kratosLogger：Kratos 日志记录器，用于记录应用生命周期事件。
//   - hs：Web 服务器实例，用于处理 HTTP 请求。
//
// 返回值：
func newApp(ctx context.Context, logger kitlog.Logger, kratosLogger kratoslog.Logger, conf *appconf.Config, hs appserver.WebServer) *kratos.App {
	opts := []kratos.Option{
		kratos.Context(ctx),
		kratos.ID(id),
		kratos.Name(name),
		kratos.Logger(kratosLogger),
		kratos.Metadata(make(map[string]string)),
		kratos.Server(
			hs,
		),
		// 配置应用启动前的回调函数，记录启动日志。
		kratos.BeforeStart(func(ctx context.Context) error {
			logger.WithField("app", "web").Info("启动服务")
			return nil
		}),
		// 配置应用启动成功后的回调函数，记录成功日志。
		kratos.AfterStart(func(ctx context.Context) error {
			logger.WithField("app", "web").Info("服务启动成功")
			return nil
		}),
		// 配置应用停止前的回调函数，记录停止日志。
		kratos.BeforeStop(func(ctx context.Context) error {
			logger.WithField("app", "web").Info("停止服务")
			return nil
		}),
		// 配置应用停止成功后的回调函数，记录停止成功日志。
		kratos.AfterStop(func(ctx context.Context) error {
			logger.WithField("app", "web").Info("服务停止成功")
			return nil
		}),
	}

	if *appconf.RegisterType_REGISTER_TYPE_UNSPECIFIED.Enum() != conf.Register.Type {
		// TODO 真实场景需要替换为外部可以访问的正确的地址。
		endpoint, err := url.Parse("http://" + conf.Server.Http.Addr)
		if err != nil {
			panic(err)
		}
		opts = append(opts, kratos.Endpoint(endpoint))
		if *appconf.RegisterType_REGISTER_TYPE_NACOS.Enum() == conf.Register.Type {
			sc := kratosnacosconstant.NewServerConfig(
				conf.Register.Nacos.ServerAddr,
				uint64(conf.Register.Nacos.ServerPort),
			)
			cc := kratosnacosconstant.NewClientConfig(
				kratosnacosconstant.WithNamespaceId(conf.Register.Nacos.Client.NamespaceId),
				kratosnacosconstant.WithCacheDir(conf.Register.Nacos.Client.CacheDir),
				kratosnacosconstant.WithLogDir(conf.Register.Nacos.Client.LogDir),
				kratosnacosconstant.WithLogLevel(conf.Register.Nacos.Client.LogLevel),
				kratosnacosconstant.WithUsername(conf.Register.Nacos.Client.Username),
				kratosnacosconstant.WithPassword(conf.Register.Nacos.Client.Password),
			)
			client, err := kratosnacosclients.NewNamingClient(
				kratosnacosvo.NacosClientParam{
					ServerConfigs: []kratosnacosconstant.ServerConfig{*sc},
					ClientConfig:  cc,
				},
			)

			if err != nil {
				panic(err)
			}

			r := kratosnacos.New(client)
			opts = append(opts, kratos.Registrar(r))
		}
	}

	// 使用 Kratos 框架创建应用实例，配置上下文、ID、名称和服务器。
	a := kratos.New(opts...)
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
	// 检查命令行参数长度，判断是否存在子命令。
	if len(os.Args) > 1 {
		subCommand := os.Args[1]
		// 根据子命令类型执行相应操作。
		switch subCommand {
		case "install":
			// 调用安装命令处理函数。
			handleInstallCommand()
			return
		case "uninstall":
			// 调用卸载命令处理函数。
			handleUninstallCommand()
			return
		case "run":
			// 显式运行命令，继续执行下面的逻辑。
		case "--help", "-h", "help":
			// 显示帮助信息并退出。
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
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 监听系统信号（SIGINT/SIGTERM），用于优雅关闭。
	signalChan := make(chan os.Signal, 1)
	signal.Notify(signalChan, syscall.SIGINT, syscall.SIGTERM)

	// 启动信号处理 goroutine，收到信号后取消 context。
	go func() {
		sig := <-signalChan
		fmt.Printf("接收到系统信号: %v\n", sig)
		cancel()
	}()

	// 通过 Wire 框架生成的 wireWeb 函数初始化服务。
	// 该函数会自动注入所有依赖项并返回配置好的 Web 服务器实例。
	if w, cleanup, err := wireWeb(ctx, cfg); nil != err {
		fmt.Printf("初始化失败：%v", err)
		// 调用清理函数释放已分配的资源。
		cleanup()
	} else if err := w.Run(); err != nil {
		panic(err)
	}
}
