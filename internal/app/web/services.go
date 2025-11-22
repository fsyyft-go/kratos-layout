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

// serviceManager 管理系统服务的安装、卸载、状态查询等操作。
//
// 该结构体封装了 kardianos/service 的 service.Service，
// 提供跨平台的服务管理能力，支持 Linux(systemd)、macOS(launchd)、Windows(Service)。
type serviceManager struct {
	configPath string
	service    service.Service
}

// noopProgram 实现 service.Interface，但不直接启动业务。
//
// 该类型用于注册系统服务时占位，所有业务逻辑仅在前台 runForeground 启动。
type noopProgram struct{}

func (n *noopProgram) Start(s service.Service) error { return nil }
func (n *noopProgram) Stop(s service.Service) error  { return nil }

// NewServiceManager 创建服务管理器。
//
// 参数：
//   - configPath：配置文件路径。
//
// 返回：
//   - *serviceManager：服务管理器实例。
//   - error：初始化过程中可能发生的错误。
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

// Install 安装系统服务。
//
// 检查服务是否已安装，未安装则注册为系统服务。
// 安装成功后输出启动/状态命令提示。
//
// 返回：
//   - error：安装过程中可能发生的错误。
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

// Uninstall 卸载系统服务。
//
// 若服务正在运行则先尝试停止，再卸载服务。
// 返回：
//   - error：卸载过程中可能发生的错误。
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

// Start 实现 service.Interface
// 之前的运行逻辑已移除：业务仅通过 runForeground 启动。

// handleInstallCommand 处理 install 子命令。
//
// 解析配置参数，创建服务管理器并执行安装。
// 安装失败时直接退出进程。
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

// handleUninstallCommand 处理 uninstall 子命令。
//
// 解析配置参数，创建服务管理器并执行卸载。
// 卸载失败时直接退出进程。
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

// parseConfigFlag 解析配置文件路径参数。
//
// 支持 run/install/uninstall/status/无子命令等多种用法，
// 自动跳过子命令参数，兼容所有入口。
// 返回：
//   - string：配置文件路径。
func parseConfigFlag() string {
	var configPath string

	// 根据命令行参数的结构，提取配置相关的参数。
	// 支持多种调用方式：run 子命令、无子命令、install/uninstall/status 子命令。
	var args []string
	if len(os.Args) > 1 && os.Args[1] == "run" {
		// 处理 "app run --config path" 格式，跳过 "run" 参数。
		args = os.Args[2:]
	} else if len(os.Args) > 1 && (os.Args[1] == "install" || os.Args[1] == "uninstall" || os.Args[1] == "status") {
		// 处理 "app install --config path" 格式，跳过子命令参数。
		args = os.Args[2:]
	} else {
		// 处理 "app --config path" 或无参数格式，从第一个参数开始解析。
		args = os.Args[1:]
	}

	// 创建一个新的 FlagSet 来避免与全局 flag 冲突，确保参数解析的独立性。
	fs := flag.NewFlagSet(os.Args[0], flag.ExitOnError)
	fs.StringVar(&configPath, "config", "configs/config.yaml", "配置文件路径")
	_ = fs.Parse(args)

	return configPath
}

// printUsage 打印命令行使用帮助。
//
// 输出所有支持的子命令和参数说明。
func printUsage() {
	fmt.Printf("Kratos Layout Web Service\n\n")
	fmt.Printf("使用方法:\n")
	fmt.Printf("  %s [命令] [选项]\n\n", os.Args[0])
	fmt.Printf("可用命令:\n")
	fmt.Printf("  run          前台运行服务 (默认)\n")
	fmt.Printf("  install      安装为系统服务\n")
	fmt.Printf("  uninstall    卸载系统服务\n")
	fmt.Printf("  help         显示此帮助信息\n\n")
	fmt.Printf("选项:\n")
	fmt.Printf("  --config <path>    指定配置文件路径 (默认: configs/config.yaml)\n\n")
	fmt.Printf("示例:\n")
	fmt.Printf("  %s --config /etc/web/config.yaml\n", os.Args[0])
	fmt.Printf("  %s install --config /etc/web/config.yaml\n", os.Args[0])
	fmt.Printf("  %s uninstall --config /etc/web/config.yaml\n", os.Args[0])
}
