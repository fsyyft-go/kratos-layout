// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package conf 提供配置文件的加载和解析功能。
// 支持从 YAML 文件中读取配置，并转换为对应的结构体。
package conf

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

// LoadConfig 从指定路径加载配置文件并解析为 Config 结构体。
//
// 参数：
//   - path string：配置文件的路径。
//
// 返回值：
//   - *Config：解析后的配置对象指针。
//   - error：加载或解析过程中可能发生的错误。
func LoadConfig(path string) (*Config, error) {
	// 验证路径是否为绝对路径。
	if !filepath.IsAbs(path) {
		absPath, err := filepath.Abs(path)
		if err != nil {
			return nil, err
		}
		path = absPath
	}

	// 验证路径是否超出允许的范围。
	cleanPath := filepath.Clean(path)
	if cleanPath != path {
		return nil, fmt.Errorf("invalid path: path contains invalid characters or traversal attempts")
	}

	// 从 yaml 文件中读取配置。
	data, err := os.ReadFile(cleanPath)
	if nil != err {
		return nil, fmt.Errorf("读取配置文件失败：%v", err)
	}

	// 解析 yaml 配置到结构体。
	var cfg Config
	if err = yaml.Unmarshal(data, &cfg); nil != err {
		return nil, fmt.Errorf("解析配置文件失败：%v", err)
	}

	return &cfg, nil
}
