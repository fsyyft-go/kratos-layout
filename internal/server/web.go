// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package server

import (
	"context"

	"github.com/gin-gonic/gin"
	kratoserrors "github.com/go-kratos/kratos/v2/errors"
	kratoslog "github.com/go-kratos/kratos/v2/log"
	kratoslogging "github.com/go-kratos/kratos/v2/middleware/logging"
	kratosmetrics "github.com/go-kratos/kratos/v2/middleware/metrics"
	kratosratelimit "github.com/go-kratos/kratos/v2/middleware/ratelimit"
	kratosrecovery "github.com/go-kratos/kratos/v2/middleware/recovery"
	kratoshttp "github.com/go-kratos/kratos/v2/transport/http"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.opentelemetry.io/otel"

	kitkratosmiddlewarevalidate "github.com/fsyyft-go/kit/kratos/middleware/validate"
	kitlog "github.com/fsyyft-go/kit/log"
	kitruntime "github.com/fsyyft-go/kit/runtime"

	apphelloworldv1 "github.com/fsyyft-go/kratos-layout/api/helloworld/v1"
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
)

var (
	_ WebServer = (*webServer)(nil)
)

type (
	// WebServer 定义了 Web 服务器的接口。
	WebServer interface {
		kitruntime.Runner // 继承 Runner 接口，提供 Start 和 Stop 方法。
	}

	// webServer 实现了 WebServer 接口，提供 Web 服务器功能。
	webServer struct {
		// 日志记录器。
		logger kitlog.Logger
		// 应用配置。
		conf *appconf.Config
		// Kratos 日志记录器。
		kratosLogger kratoslog.Logger
		// 服务器实例。
		server *kratoshttp.Server
	}
)

// NewWebServer 创建并配置一个新的 Web 服务器实例。
//
// 参数：
//   - logger：日志记录器，用于服务日志记录。
//   - kratosLogger：Kratos 日志记录器，用于记录应用生命周期事件。
//   - conf：服务配置信息。
//   - greeter：问候服务的 HTTP 处理器。
//
// 返回：
//   - WebServer：配置好的 Web 服务器实例。
//   - func()：清理函数。
//   - error：初始化过程中可能发生的错误。
func NewWebServer(logger kitlog.Logger, kratosLogger kratoslog.Logger, conf *appconf.Config,
	greeter apphelloworldv1.GreeterHTTPServer,
) (WebServer, func(), error) {
	var err error

	// 创建带有领域驱动设计和模块标记的日志记录器。
	l := logger.WithField("ddd", "server").WithField("module", "web")

	webServer := &webServer{
		logger:       l,
		kratosLogger: kratosLogger,
		conf:         conf,
	}

	meter := otel.Meter("app")
	metricRequests, err := kratosmetrics.DefaultRequestsCounter(meter, kratosmetrics.DefaultServerRequestsCounterName)
	if err != nil {
		panic(err)
	}
	metricSeconds, err := kratosmetrics.DefaultSecondsHistogram(meter, kratosmetrics.DefaultServerSecondsHistogramName)
	if err != nil {
		panic(err)
	}

	webServer.server = kratoshttp.NewServer(
		kratoshttp.Address(conf.GetServer().GetHttp().GetAddr()),
		kratoshttp.Logger(kratosLogger),
		kratoshttp.Middleware(
			kratosrecovery.Recovery(),          // 异常恢复：https://www.bookstack.cn/read/kratos-2.8-zh/b9e826c7bec1a4cb.md。
			kratoslogging.Server(kratosLogger), // 日志记录：https://www.bookstack.cn/read/kratos-2.8-zh/14155bca8afb4099.md。
			kratosmetrics.Server( // 指标蹭件：https://github.com/go-kratos/examples/blob/main/metrics/main.go，怎么输出？
				kratosmetrics.WithSeconds(metricSeconds),
				kratosmetrics.WithRequests(metricRequests),
			),
			kratosratelimit.Server(), // 限流：https://www.bookstack.cn/read/kratos-2.8-zh/2659b3542a9e7bd3.md。
			kitkratosmiddlewarevalidate.Validator(kitkratosmiddlewarevalidate.WithValidateCallback(webServer.validateCallback)), // 参数检验：https://www.bookstack.cn/read/kratos-2.8-zh/cc41b2328fb6d9e5.md。
		),
	)

	// 注册 HTTP 处理器。
	apphelloworldv1.RegisterGreeterHTTPServer(webServer.server, greeter)
	// 注册 Gin 处理器。
	webServer.registerGinHandler()

	var cleanup = func() {}

	return webServer, cleanup, err
}

func (s *webServer) registerGinHandler() {
	// 创建 Gin 引擎。
	engine := gin.Default()
	// 注册 Gin 处理的 Handler 到 Kratos HTTP 服务器。
	s.server.HandlePrefix("/", engine)

	engine.GET("/metrics", func(c *gin.Context) {
		promhttp.Handler().ServeHTTP(c.Writer, c.Request)
	})
}

// Start 实现启动 Web 服务器的功能。
// 使用 Gin 引擎监听指定端口。
//
// 参数：
//   - ctx：上下文信息（当前未使用）。
//
// 返回值：
//   - error：启动过程中可能发生的错误。
func (s *webServer) Start(ctx context.Context) error {
	return s.server.Start(ctx)
}

// Stop 实现停止 Web 服务器的功能。
//
// 参数：
//   - ctx：上下文信息（当前未使用）。
//
// 返回值：
//   - error：停止过程中可能发生的错误。
func (s *webServer) Stop(ctx context.Context) error {
	return s.server.Stop(ctx)
}

// validateCallback 处理请求验证失败的回调函数。
// 记录请求和验证错误，并返回标准化的错误响应。
//
// 参数：
//   - ctx：上下文信息（当前未使用）。
//   - req：原始请求。
//   - errValidate：验证过程中产生的错误。
//
// 返回值：
//   - interface{}：处理后的请求（本实现中返回 nil）。
//   - error：格式化后的错误信息。
func (s *webServer) validateCallback(_ context.Context, req interface{}, errValidate error) (interface{}, error) {
	// 记录请求和验证错误信息。
	s.logger.WithField("req", req).WithField("errValidate", errValidate).Info("validateCallback")
	// 返回标准化的错误响应。
	return nil, kratoserrors.BadRequest("VALIDATOR", "请求参数错误，详见日志")
}
