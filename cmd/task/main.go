// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package main 实现了任务执行器的入口程序。
// 该程序负责初始化配置、依赖注入，并启动任务执行器。
package main

import (
	app_task "github.com/fsyyft-go/kratos-layout/internal/app/task"
)

func main() {
	app_task.Run()
}
