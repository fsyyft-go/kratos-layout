// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package log

import (
	kratoslog "github.com/go-kratos/kratos/v2/log"

	kitlog "github.com/fsyyft-go/kit/log"
)

type (
	// kratosLogger 是 kratoslog.Logger 的实现，封装了 kitlog.Logger 以适配 Kratos 日志接口。
	kratosLogger struct {
		// logger 封装的底层日志记录器，用于实际的日志输出。
		logger kitlog.Logger
	}
)

// NewKratosLogger 创建一个新的 Kratos 日志记录器实例。
// 参数：
//   - logger：底层日志记录器，用于实际的日志输出。
//
// 返回值：
//   - kratoslog.Logger：适配 Kratos 日志接口的日志记录器实例。
func NewKratosLogger(logger kitlog.Logger) kratoslog.Logger {
	return &kratosLogger{logger: logger.WithField("kratos", "")}
}

// Log 根据指定的日志级别记录日志消息。
// 参数：
//   - level：日志级别，确定消息的严重程度。
//   - keyvals：键值对形式的日志数据，支持任意数量的参数。
//
// 返回值：
//   - error：记录过程中发生的错误，成功时返回 nil。
func (l *kratosLogger) Log(level kratoslog.Level, keyvals ...any) error {
	// 根据日志级别调用相应的底层日志记录器方法。
	switch level {
	case kratoslog.LevelDebug:
		l.logger.Debug(keyvals...)
	case kratoslog.LevelInfo:
		l.logger.Info(keyvals...)
	case kratoslog.LevelWarn:
		l.logger.Warn(keyvals...)
	case kratoslog.LevelError:
		l.logger.Error(keyvals...)
	}
	return nil
}
