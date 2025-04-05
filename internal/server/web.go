// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package server

import (
	"context"

	"github.com/gin-gonic/gin"
	"github.com/go-kratos/kratos/v2/transport/http"

	kit_kratos_transport_http "github.com/fsyyft-go/kit/kratos/transport/http"
	kit_log "github.com/fsyyft-go/kit/log"
	kit_runtime "github.com/fsyyft-go/kit/runtime"

	app_helloworld_v1 "github.com/fsyyft-go/kratos-layout/api/helloworld/v1"
	app_conf "github.com/fsyyft-go/kratos-layout/internal/conf"
)

var (
	_ WebServer = (*webServer)(nil)
)

type (
	// WebServer 定义了 Web 服务器的接口。
	WebServer interface {
		kit_runtime.Runner   // 继承 Runner 接口，提供 Start 和 Stop 方法。
		Engine() *gin.Engine // 返回 Gin 引擎实例，允许外部访问和配置。
	}

	// webServer 实现了 WebServer 接口，提供 Web 服务器功能。
	webServer struct {
		// 日志记录器。
		logger kit_log.Logger
		// 应用配置。
		conf *app_conf.Config
		// Gin 引擎，用于处理 HTTP 请求。
		engine *gin.Engine
	}
)

func NewWebServer(logger kit_log.Logger, conf *app_conf.Config, greeter app_helloworld_v1.GreeterHTTPServer) (WebServer, func(), error) {
	var err error

	// 创建带有领域驱动设计和模块标记的日志记录器。
	l := logger.WithField("ddd", "server").WithField("module", "web")

	webServer := &webServer{
		logger: l,
		conf:   conf,
	}

	server := http.NewServer()

	// 初始化 Gin 引擎，并配置默认中间件。
	webServer.engine = gin.Default()
	// 将 Kratos HTTP 服务解析到 Gin 引擎中。
	kit_kratos_transport_http.Parse(server, webServer.engine)

	var cleanup = func() {}

	return webServer, cleanup, err
}

func (s *webServer) Start(ctx context.Context) error {
	return nil
}

// Stop implements WebServer.
func (s *webServer) Stop(ctx context.Context) error {
	panic("unimplemented")
}

// Engine implements WebServer.
func (s *webServer) Engine() *gin.Engine {
	panic("unimplemented")
}
