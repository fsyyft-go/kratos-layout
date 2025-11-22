// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package task 提供具体的任务实现。
//
// 本包包含系统中所有后台任务的具体实现。任务通过定时器周期性执行，
// 支持上下文取消和优雅关闭。
//
// 主要任务类型：
//   - Hello：定时问候任务示例
//   - 其他任务：可根据需要扩展
//
// 任务执行特点：
//   - 基于 time.Ticker 的周期性执行
//   - 支持 context 取消机制
//   - 记录详细的执行日志
//
// 使用示例：
//
//	// 创建任务实例
//	helloTask := task.NewHello(logger)
//
//	// 运行任务
//	err := helloTask.Run(ctx)
package task
