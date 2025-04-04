// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package task

import (
	"context"
	"flag"
	"fmt"

	"github.com/google/wire"

	// 模板：下面这条导入，应用时需要修改。
	app_conf "github.com/fsyyft-go/kratos-layout/internal/conf"
)

var (
	ProviderSet = wire.NewSet(
		NewLogger,
	)
)

func Run() {
	// 定义配置文件路径变量，默认为"configs/config.yaml"。
	var configPath string

	// 注册命令行参数，用于指定配置文件路径。
	flag.StringVar(&configPath, "config", "configs/config.yaml", "配置文件路径")
	flag.Parse()

	// 从指定路径加载配置文件。
	cfg, err := app_conf.LoadConfig(configPath)
	if nil != err {
		fmt.Printf("加载配置文件失败：%v", err)
		return
	}

	// 通过 Wire 框架生成的 wireServer 函数初始化服务。
	// 该函数会自动注入所有依赖项并返回配置好的 Web 服务器实例。
	if webServer, cleanup, err := wireServer(cfg); nil != err {
		fmt.Printf("初始化失败：%v", err)
		// 调用清理函数释放已分配的资源。
		cleanup()
	} else {
		// 启动 Web 服务器。
		_ = webServer.Run(context.TODO())
	}
}
