// Code generated by Wire. DO NOT EDIT.

//go:generate go run -mod=mod github.com/google/wire/cmd/wire
//go:build !wireinject
// +build !wireinject

package task

import (
	app_conf "github.com/fsyyft-go/kratos-layout/internal/conf"
	app_task "github.com/fsyyft-go/kratos-layout/internal/task"
)

// Injectors from wire.go:

func wireTask(cfg *app_conf.Config) (app_task.Hello, func(), error) {
	logLogger, cleanup, err := NewLogger(cfg)
	if err != nil {
		return nil, nil, err
	}
	hello, err := app_task.NewHello(logLogger, cfg)
	if err != nil {
		cleanup()
		return nil, nil, err
	}
	return hello, func() {
		cleanup()
	}, nil
}
