// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package web

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/kardianos/service"
)

const (
	serviceName        = "kratos-layout-web"
	serviceDisplayName = "Kratos Layout Web Service"
	serviceDescription = "Kratos Layout Web HTTP服务，基于Go Kratos框架"
)

// serviceManager 管理系统服务的安装、卸载等操作
type serviceManager struct {
	configPath string
	service    service.Service
}

// noopProgram 实现 service.Interface，但不直接启动业务；
// 真正业务逻辑只在前台 `runForeground` 中运行。
type noopProgram struct{}

func (n *noopProgram) Start(s service.Service) error { return nil }
func (n *noopProgram) Stop(s service.Service) error  { return nil }

// NewServiceManager 创建服务管理器
func NewServiceManager(configPath string) (*serviceManager, error) {
	// 获取配置文件的绝对路径。
	absConfigPath, err := filepath.Abs(configPath)
	if err != nil {
		return nil, fmt.Errorf("获取配置文件绝对路径失败: %v", err)
	}

	// 检查配置文件是否存在。
	if _, err := os.Stat(absConfigPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("配置文件不存在: %s", absConfigPath)
	}

	// 使用可执行目录作为 WorkingDirectory（方便后续若扩展需要）。
	exePath, exeErr := os.Executable()
	workingDir := ""
	if exeErr == nil {
		workingDir = filepath.Dir(exePath)
	} else if cwd, errCwd := os.Getwd(); errCwd == nil {
		workingDir = cwd
	} else {
		workingDir = "/tmp"
	}

	// 构建服务配置（不自动启动业务，仅占位 install/uninstall 逻辑）。
	svcConfig := &service.Config{
		Name:             serviceName,
		DisplayName:      serviceDisplayName,
		Description:      serviceDescription,
		WorkingDirectory: workingDir,
		// 提示: 真正业务需人工以 foreground 或其它机制运行。
		Arguments: []string{"run", "--config", absConfigPath},
		Option: service.KeyValue{
			"RunAtLoad": true,
			"KeepAlive": true,
		},
	}

	// 使用 no-op program
	prog := &noopProgram{}
	svc, err := service.New(prog, svcConfig)
	if err != nil {
		return nil, fmt.Errorf("创建服务实例失败: %v", err)
	}

	return &serviceManager{
		configPath: absConfigPath,
		service:    svc,
	}, nil
}

// Install 安装系统服务
func (sm *serviceManager) Install() error {
	// 检查服务是否已经安装
	status, err := sm.service.Status()
	if err == nil {
		switch status {
		case service.StatusRunning:
			return fmt.Errorf("服务 %s 已安装并正在运行", serviceName)
		case service.StatusStopped:
			return fmt.Errorf("服务 %s 已安装但未运行", serviceName)
		}
	}

	// 执行安装。
	if err := sm.service.Install(); err != nil {
		// 检查是否是权限问题。
		if strings.Contains(err.Error(), "permission denied") {
			fmt.Printf("❌ 安装服务失败: 权限不足\n")
			fmt.Printf("💡 请使用管理员权限运行:\n")
			fmt.Printf("   Linux:   sudo %s install --config %s\n", os.Args[0], sm.configPath)
			fmt.Printf("   macOS:   sudo %s install --config %s\n", os.Args[0], sm.configPath)
			fmt.Printf("   Windows: 以管理员身份运行命令提示符，然后执行安装命令\n")
			return fmt.Errorf("权限不足")
		}
		return fmt.Errorf("安装服务失败: %v", err)
	}

	fmt.Printf("✅ 服务 %s 安装成功\n", serviceName)
	fmt.Printf("📄 配置文件: %s\n", sm.configPath)
	fmt.Println("\n🚀 启动服务:")
	fmt.Printf("   Linux:   sudo systemctl start %s\n", serviceName)
	fmt.Printf("   macOS:   sudo launchctl load /Library/LaunchDaemons/com.%s.plist\n", serviceName)
	fmt.Printf("   Windows: net start %s\n", serviceName)
	fmt.Println("\n📊 查看状态:")
	fmt.Printf("   Linux:   sudo systemctl status %s\n", serviceName)
	fmt.Printf("   macOS:   sudo launchctl list | grep %s\n", serviceName)
	fmt.Printf("   Windows: sc query %s\n", serviceName)

	return nil
}

// Uninstall 卸载系统服务
func (sm *serviceManager) Uninstall() error {
	// 首先尝试停止服务
	status, err := sm.service.Status()
	if err == nil && status == service.StatusRunning {
		fmt.Printf("⏹️  正在停止服务 %s...\n", serviceName)
		if err := sm.service.Stop(); err != nil {
			fmt.Printf("⚠️  停止服务失败: %v\n", err)
			fmt.Println("请手动停止服务后再次运行卸载命令")
			return err
		}
		// 等待服务完全停止
		time.Sleep(2 * time.Second)
	}

	// 执行卸载
	if err := sm.service.Uninstall(); err != nil {
		return fmt.Errorf("卸载服务失败: %v", err)
	}

	fmt.Printf("✅ 服务 %s 卸载成功\n", serviceName)
	return nil
}

// Status 查询服务状态
func (sm *serviceManager) Status() error {
	status, err := sm.service.Status()
	if err != nil {
		fmt.Printf("❌ 查询服务状态失败: %v\n", err)
		return err
	}

	statusText := "未知"
	statusEmoji := "❓"
	switch status {
	case service.StatusRunning:
		statusText = "运行中"
		statusEmoji = "✅"
	case service.StatusStopped:
		statusText = "已停止"
		statusEmoji = "⏹️"
	case service.StatusUnknown:
		statusText = "未知"
		statusEmoji = "❓"
	}

	fmt.Printf("%s 服务 %s 状态: %s\n", statusEmoji, serviceName, statusText)
	return nil
}

// Start 实现 service.Interface
// 之前的运行逻辑已移除：业务仅通过 runForeground 启动。

// handleInstallCommand 处理安装命令
func handleInstallCommand() {
	configPath := parseConfigFlag()
	sm, err := NewServiceManager(configPath)
	if err != nil {
		fmt.Printf("❌ 创建服务管理器失败: %v\n", err)
		os.Exit(1)
	}

	if err := sm.Install(); err != nil {
		fmt.Printf("❌ %v\n", err)
		os.Exit(1)
	}
}

// handleUninstallCommand 处理卸载命令
func handleUninstallCommand() {
	configPath := parseConfigFlag()
	sm, err := NewServiceManager(configPath)
	if err != nil {
		fmt.Printf("❌ 创建服务管理器失败: %v\n", err)
		os.Exit(1)
	}

	if err := sm.Uninstall(); err != nil {
		fmt.Printf("❌ %v\n", err)
		os.Exit(1)
	}
}

// handleStatusCommand 处理状态查询命令
func handleStatusCommand() {
	configPath := parseConfigFlag()
	sm, err := NewServiceManager(configPath)
	if err != nil {
		fmt.Printf("❌ 创建服务管理器失败: %v\n", err)
		os.Exit(1)
	}

	if err := sm.Status(); err != nil {
		os.Exit(1)
	}
}

// parseConfigFlag 解析配置文件路径参数
func parseConfigFlag() string {
	var configPath string

	// 创建一个新的 FlagSet 来避免与全局 flag 冲突
	fs := flag.NewFlagSet(os.Args[0], flag.ExitOnError)
	fs.StringVar(&configPath, "config", "configs/config.yaml", "配置文件路径")

	// 解析除第一个子命令外的其他参数
	args := os.Args[2:]
	fs.Parse(args)

	return configPath
}

// printUsage 打印使用帮助
func printUsage() {
	fmt.Printf("Kratos Layout Web Service\n\n")
	fmt.Printf("使用方法:\n")
	fmt.Printf("  %s [命令] [选项]\n\n", os.Args[0])
	fmt.Printf("可用命令:\n")
	fmt.Printf("  run          前台运行服务 (默认)\n")
	fmt.Printf("  install      安装为系统服务\n")
	fmt.Printf("  uninstall    卸载系统服务\n")
	fmt.Printf("  status       查看服务状态\n")
	fmt.Printf("  help         显示此帮助信息\n\n")
	fmt.Printf("选项:\n")
	fmt.Printf("  --config <path>    指定配置文件路径 (默认: configs/config.yaml)\n\n")
	fmt.Printf("示例:\n")
	fmt.Printf("  %s run --config /etc/kratos/config.yaml\n", os.Args[0])
	fmt.Printf("  %s install --config /etc/kratos/config.yaml\n", os.Args[0])
	fmt.Printf("  %s uninstall\n", os.Args[0])
}
