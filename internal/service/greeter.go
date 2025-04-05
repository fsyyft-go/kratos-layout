// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package service

import (
	"context"

	kit_log "github.com/fsyyft-go/kit/log"

	app_helloworld_v1 "github.com/fsyyft-go/kratos-layout/api/helloworld/v1"
	app_biz "github.com/fsyyft-go/kratos-layout/internal/biz"
	app_conf "github.com/fsyyft-go/kratos-layout/internal/conf"
)

type (
	greeterService struct {
		logger kit_log.Logger
		conf   *app_conf.Config
		uc     app_biz.GreeterUsecase
	}
)

func NewGreeterService(logger kit_log.Logger, conf *app_conf.Config, uc app_biz.GreeterUsecase) app_helloworld_v1.GreeterHTTPServer {
	return &greeterService{
		logger: logger,
		conf:   conf,
		uc:     uc,
	}
}

func (s *greeterService) SayHello(ctx context.Context, in *app_helloworld_v1.HelloRequest) (*app_helloworld_v1.HelloReply, error) {
	return nil, nil
}
