// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package log

import (
	"github.com/google/wire"
)

var (
	// ProviderSet 是日志模块的依赖注入提供者集合。
	ProviderSet = wire.NewSet(
		NewLogger,
	)
)
