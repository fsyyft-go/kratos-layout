// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Code generated by Wire. DO NOT EDIT.

//go:generate go run -mod=mod github.com/google/wire/cmd/wire
//go:build !wireinject
// +build !wireinject

package web

import (
	"github.com/fsyyft-go/kratos-layout/internal/conf"
	"github.com/fsyyft-go/kratos-layout/internal/server"
	"github.com/fsyyft-go/kratos-layout/internal/service"
)

// Injectors from wire.go:

func wireWeb(conf2 *conf.Config) (server.WebServer, func(), error) {
	logLogger, cleanup, err := NewLogger(conf2)
	if err != nil {
		return nil, nil, err
	}
	greeterHTTPServer := service.NewGreeterService(logLogger, conf2)
	webServer, cleanup2, err := server.NewWebServer(logLogger, conf2, greeterHTTPServer)
	if err != nil {
		cleanup()
		return nil, nil, err
	}
	return webServer, func() {
		cleanup2()
		cleanup()
	}, nil
}
