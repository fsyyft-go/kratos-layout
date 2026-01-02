# 跨平台服务安装与卸载调研与实现方案

> 适用对象：本仓库中的服务（入口 `cmd/web` 和 `cmd/task` / 逻辑 `internal/app/web` 和 `internal/app/task`）。目标：在不新增独立 CLI 的前提下，于现有可执行文件中增加 `install` / `uninstall` 等子命令，支持 macOS、Linux、Windows 下以"系统服务"方式长期运行，遵循最小权限、可观测、可运维、可扩展的行业标准实践。

---
## 1. 三大桌面/服务器操作系统服务机制原理概述

### 1.1 Linux systemd
- **角色**：PID 1 初始化系统 + 服务管理器。以“Unit”描述资源，其中最常用的是 `service` 单元（`.service` 文件）。
- **关键流程**：
  1. Unit 文件放在 `/etc/systemd/system/<name>.service`（本地自定义）或 `/usr/lib/systemd/system`（发行版包）
  2. `systemctl daemon-reload` 重新加载
  3. `systemctl enable <name>` 生成 wants/symlink 以便开机自启
  4. `systemctl start <name>` 运行，systemd 负责进程生命周期、重启策略、日志（journald）
- **类型**：`Type=simple`（默认，执行即认为启动成功），`notify`（配合 sd_notify）、`forking`（守护进程化旧式）、`oneshot`（短任务）、`idle` 等。
- **日志**：默认写 journald -> `journalctl -u <name>`。
- **用户**：推荐设置 `User=` + `Group=` 指定非 root 账号；配合 `CapabilityBoundingSet=` 等限制特权。
- **最小权限**：通过 `ProtectSystem=`, `ProtectHome=`, `NoNewPrivileges=`, `AmbientCapabilities`, `ReadWritePaths` 等进行沙箱化。
- **配置热更新**：
  - 应用层支持 SIGHUP / 配置文件轮询
  - systemd 支持 `ExecReload=` 定义热重载命令

### 1.2 macOS launchd
- **角色**：统一的服务与任务启动管理（`launchd`）。使用 `.plist`（XML）描述 job。
- **放置位置**：
  - 用户级：`~/Library/LaunchAgents/`（无需 sudo，用户登录后启动）
  - 系统级：`/Library/LaunchDaemons/`（多用户可见，需 root）
- **操作流程**：历史上使用 `launchctl load/unload`，但 **自 macOS 10.10+ 起官方推荐使用显式域 (domain) 语义的 `launchctl bootstrap / bootout`**。旧命令已被视为兼容层，不再建议在新脚本和自动化中使用。
- **关键字段**：`Label`、`Program` / `ProgramArguments`、`RunAtLoad`、`KeepAlive`、`StandardOutPath`、`StandardErrorPath`、`EnvironmentVariables`、`UserName`。
- **日志**：旧版本系统控制台 Console.app，现代 macOS 推荐将 stdout/stderr 重定向到文件或统一到 ASL / unified logging（复杂）。本方案采用文件输出。
- **最小权限**：优先放置用户级（不需 root），若需系统级守护（后台无用户登录运行）则放 `/Library/LaunchDaemons` 并指定 `UserName`（除非需要 root）。

#### 1.2.1 `bootstrap` / `bootout` 与旧 `load` / `unload` 区别

| 维度 | bootstrap / bootout | load / unload (旧) | 说明 |
|------|---------------------|--------------------|------|
| 域 (domain) 指定 | 必须显式：`system` / `user/<uid>` / `gui/<uid>` | 隐式推断 | 新模型更明确、可预期 |
| 行为 | 注册(加载)+启动 / 停止+移除 | 加载+启动 / 停止+卸载 | 语义类似但旧接口不鼓励使用 |
| 并发 & 校验 | 更严格（重复、Label 冲突检测） | 较宽松 | 减少“幽灵”残留 |
| 与 enable/disable 协同 | 设计一致 | 部分情形语义模糊 | 组合运维更清晰 |
| 调试工具支持 | `launchctl print <domain>/<label>` | 仅 list | 新接口提供更丰富状态树 |
| 官方未来支持 | 推荐 | 兼容层，可能限制 | 需迁移 |

常见 domain 示例：
| Domain 示例 | 含义 |
|-------------|------|
| `system` | 系统级守护（`/Library/LaunchDaemons`）|
| `gui/501` | 图形会话 UID=501（桌面登录） |
| `user/501` | 用户会话（Shell 登录） |

> `bootstrap system /Library/LaunchDaemons/xxx.plist` 等价“加载 + 启动”，`bootout system /Library/LaunchDaemons/xxx.plist` 等价“停止 + 卸载”。

#### 1.2.2 推荐的日常命令

| 目的 | 推荐命令 | 说明 |
|------|----------|------|
| 安装并启动 | `sudo launchctl bootstrap system /Library/LaunchDaemons/kratos-layout-web.plist` | 读取 plist 中的 Label 注册 job |
| 停止并卸载 | `sudo launchctl bootout system /Library/LaunchDaemons/kratos-layout-web.plist` | 亦可用 `system/<label>` 形式 |
| 重启 | `sudo launchctl kickstart -k system/kratos-layout-web` | 不修改 plist 文件，仅重新拉起进程 |
| 查看状态 | `sudo launchctl print system/kratos-layout-web` | 比 `list` 更详细（环境、退出码、PID 等） |
| 快速列表 | `launchctl list | grep kratos-layout-web` | 简要行（PID / 上次退出码 / Label） |

#### 1.2.3 迁移建议
如果你已有脚本使用：
```bash
sudo launchctl load /Library/LaunchDaemons/kratos-layout-web.plist
```
请迁移为：
```bash
sudo launchctl bootstrap system /Library/LaunchDaemons/kratos-layout-web.plist
```
卸载对应迁移为：
```bash
sudo launchctl bootout system /Library/LaunchDaemons/kratos-layout-web.plist
```
重启无需“先 bootout 再 bootstrap”，优先使用：
```bash
sudo launchctl kickstart -k system/kratos-layout-web
```

#### 1.2.4 常见问题
- 看到 `- 0 label`：表示已加载且退出码 0，当前可能未常驻（或瞬时任务）。
- 反复 `bootstrap` 报错 *Service already loaded*：说明已存在，先 `bootout` 或直接 `kickstart`。
- 需要切换到用户级（非 root）守护：放置到 `~/Library/LaunchAgents/`，并使用 `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/xxx.plist`。
- **plist 文件权限要求**：系统级 plist 文件必须是 `root:wheel` 所有者，权限 644 (`-rw-r--r--`)，否则 launchd 会拒绝加载。
- **launchctl load 不启动进程**：当使用 no-op service（只注册不运行业务逻辑）时，`launchctl load` 只会注册服务但不启动进程，这是预期行为。如需启动实际业务，需要实现真正的 service.Interface。


### 1.3 Windows Service Control Manager (SCM)
- **角色**：Windows 服务控制管理器管理后台服务。服务信息存储在注册表 `HKLM\SYSTEM\CurrentControlSet\Services`。
- **安装**：
  - 命令行：`sc create` 或 PowerShell `New-Service`
  - 编程：Win32 API `CreateService` / 使用 Go 封装库
- **运行方式**：二进制需实现服务入口（处理 `Start`, `Stop`, `Shutdown` 控制码），否则只会被当作普通进程。第三方库（如 `kardianos/service`）抽象这些细节。
- **日志**：无统一 stdout 捕获（直接打印会消失），需写文件或使用 Windows 事件日志。`kardianos/service` 可辅助。
- **权限**：通过指定 `obj=`, `LocalService` / 自定义低权限用户；目录权限 (ACL) 控制最小访问。
- **自动重启**：`sc failure` 配置或新版使用 `Restart-Service` 策略 / Recovery 选项。

---
## 2. 方案候选及对比

| 方案 | 跨平台性 | 侵入性 | 自定义扩展 | 典型工作量 | 适配最小权限 | 备注 |
|------|----------|--------|------------|------------|--------------|------|
| 各平台分别生成 systemd/launchd/SCM 脚本 | 低 | 低 | 高（任意脚本） | 中高（维护三套脚本） | 好 | 需自行封装 install/uninstall 逻辑 |
| 使用 `kardianos/service` | 高 | 低 | 中（钩子有限，但可扩展 wrapper） | 低 | 支持（User/Group） | 社区常用、稳定，推荐 |
| 使用 `daemon`/`go-daemon` + 各平台脚本 | 中 | 中 | 高 | 中 | 需自行脚本 | 仍要写脚本，不如直接上第一种 |
| 使用容器（systemd 不直接管理） | 高（只需 Docker/K8s） | 中 | 高（Compose/K8s manifest） | 中 | 由容器 runtime 控制 | 场景不同（偏云原生） |

结论：**首选 `kardianos/service`**，可快速提供 install/uninstall/start/stop/status 支持，统一代码路径。

---
## 3. 推荐总体设计

### 3.1 功能目标
- 新增子命令（统一通过现有 `web` 或 `task` 可执行文件）：
  - `web run` / `task run`（默认，与现有 `Run()` 等价）
  - `web install` / `task install`（安装为系统服务）
  - `web uninstall` / `task uninstall`（卸载）
  - 可选扩展：`start` / `stop` / `restart` / `status`
- 支持 flags：`--config`、`--user`（Linux/macOS 指定运行用户）、`--service-name`、`--service-desc`、`--log-dir`。
- 非 root 情况下：
  - Linux：提示需 sudo（安装阶段），运行时由 systemd 以指定 `User=` 启动
  - macOS：若指定 `--user` 且为当前用户，可以安装到用户 LaunchAgents；若为 root + 需要常驻，则写 LaunchDaemons。
  - Windows：默认 LocalService / 自定义用户（需凭据）
- 允许通过环境变量覆盖：`KRATOS_SVC_NAME`, `KRATOS_CONFIG`, `KRATOS_LOG_DIR`。

### 3.2 目录与文件约定
- 可执行目标为 `web` 和 `task`。
- 默认安装后：
  - Linux：日志 `/var/log/<service>/app.log` （或保留项目本地相对路径如 `/opt/<service>/logs`）
  - macOS：用户级 `~/Library/Logs/<service>/*.log` 或系统级 `/var/log/<service>`
  - Windows：`C:\ProgramData\<service>\logs\app.log`
- 配置文件复制（可选）：若用户未指定，安装时写入 `/etc/<service>/config.yaml`（Linux）、`/Library/Application Support/<service>/config.yaml`（macOS）、`C:\ProgramData\<service>\config.yaml`（Windows）。支持软链接（Linux）。

### 3.3 运行用户与最小权限
- 安装时：
  - Linux systemd unit: `User=<user>` `Group=<group>`，并设置：
    - `NoNewPrivileges=yes`
    - `ProtectSystem=full`（如需写配置可使用 `ReadWritePaths=` 指定）
    - `PrivateTmp=yes`、`ProtectHome=true`、`RestrictAddressFamilies=AF_INET AF_UNIX`（按需裁剪）
  - macOS LaunchDaemons：设置 `UserName`；若走 LaunchAgents 则默认当前用户即可。
  - Windows：`kardianos/service` 可配置 `ServiceConfig` 中的 `UserName`（本地账户）与密码；若未设置就用 LocalService（低权限）。

### 3.4 升级与回滚策略（简版）
- **二进制替换**：先 `web stop`，替换文件，`web start`。
- **原地滚动（无停机）**：部署两个实例 + 反向代理（Nginx / LB）；本地单机服务模式通常不需要。
- **版本追踪**：在 `--version` 子命令输出 Git commit / build time，systemd unit 加 `Environment=VERSION=...`；日志首行输出版本。
- **回滚**：保留上一个二进制命名 `<service>-<timestamp>`，失败后切换链接。脚本可附加在文档中。

### 3.5 配置热更新
- 当前代码未实现热重载。建议：
  1. 捕获 `SIGHUP`（Linux/macOS）重新 `LoadConfig` 并更新依赖（需要抽象 Config Provider）
  2. Windows：可通过 `kardianos/service` 的 `Reload`（如无则自定义 `net stop/start` 或在控制通道上触发）
  3. 后续可接入 fsnotify 观察配置变化

### 3.6 日志策略
- 维持现有单文件输出（`logs/app.log`），安装模式可根据 `--log-dir` 重定向。
- Linux systemd 可考虑不写文件，仅 stdout -> journald（简化）——可加 `--journald` 开关。
- Windows：强制写文件 + 可选事件日志（将关键错误写入 Win 事件日志 API，后续扩展）。

### 3.7 监控与健康检查（扩展点）
- 提供 `GET /healthz`（当前可在 `webServer` 启动后添加路由）
- systemd 配置 `Restart=on-failure` + `StartLimitIntervalSec` / `StartLimitBurst` 防止崩溃循环。
- Windows Recovery 选项配置自动重启。

### 3.8 安装卸载行为定义
| 操作 | 行为 | 幂等性 | 失败回滚 |
|------|------|--------|----------|
| install | 检查已存在->跳过/提示; 生成服务描述; 写配置（可选复制）| 需要 | 删除已生成文件 |
| uninstall | 停止服务；移除描述文件 / 注册表项 | 需要 | 如部分失败提示手动清理 |
| start | systemd/launchd/SCM start | 幂等 | - |
| stop | systemd/launchd/SCM stop | 幂等 | - |
| restart | stop + start 或直接 restart | 幂等 | - |
| status | 读取服务状态并统一输出 JSON | - | - |

统一输出结构示例：
```json
{ "service": "kratos-layout-web", "status": "running", "pid": 1234, "uptime": "5m23s" }
```

---
## 4. 使用 `kardianos/service` 的具体实现思路

### 4.1 引入依赖
```bash
go get github.com/kardianos/service@latest
```

### 4.2 抽象 Service Wrapper
新增文件示例：`internal/app/web/service_wrapper.go`：
- 封装 `service.Interface`，其 `Start(s service.Service)` 内启动一个 goroutine 调用现有 `Run()` 中的核心逻辑（需将 `Run()` 拆为可复用函数，如 `NewWebApp(cfg)` + `Start(ctx)`）。
- `Stop(s service.Service)` 发取消信号（context cancel）并等待。

### 4.3 改造现有 `Run()`
当前 `Run()` 同时做：解析 flags + 加载配置 + 信号监听 + 启动服务。为了支持服务管理：
1. 拆分：
   - `LoadConfigFromFlags()` 返回 `*Config`
   - `BuildWebServer(cfg)`（由 wire 生成）返回 `WebServer`
   - `Serve(ctx, webServer)` 负责阻塞运行
2. 普通前台模式：保持现有逻辑
3. 服务模式：`Install` 时不启动，只注册；`Start` 时由 SCM 调用 `Start` -> 构建 + 运行

### 4.4 命令行解析
使用标准库 `flag` 或引入 `spf13/cobra`（若想保持零依赖，继续用 `flag` + 手写子命令解析）。示例结构：
```
web <subcommand> [--flags]
subcommand ∈ { run | install | uninstall | start | stop | restart | status }
默认（无子命令）等价于 run
```

### 4.5 Service Config 生成
```go
svcConfig := &service.Config{
    Name: serviceName,            // kratos-layout-web
    DisplayName: "Kratos Layout Web",
    Description: serviceDesc,
    Arguments: []string{"run", "--config", absConfigPath},
    UserName: targetUser, // Windows 或留空
    Option: map[string]interface{}{
        "RunAtLoad": true,          // macOS
        "KeepAlive": true,          // macOS
        "Restart": "on-failure",   // systemd
        "RestartSec": 3,            // systemd
        "UserService": isUserMode,  // macOS 用户级
    },
}
```
> 不同平台 Option 支持键会被忽略或使用，`kardianos/service` 会筛选。

### 4.6 最小权限
- 如果未指定 `--user`：
  - Linux：创建/提示使用系统用户 `kratos`（可选：`useradd --system --no-create-home kratos`）——由安装文档提示，程序只做校验。
  - macOS 用户级默认当前用户；系统级需要 root。
  - Windows 默认 LocalService（无需明文密码）。
- 对于需要写日志目录：预先创建并 `chown` / 设置 ACL。

### 4.7 状态查询
`service.Status()` 返回：
- `StatusRunning` / `StatusStopped` / `StatusUnknown`
补充 PID：Linux/macOS 可通过 `pidfile`（Option）或解析 systemd/launchctl；简化方案：运行时写一个 pid 文件 `<logDir>/<service>.pid`。

### 4.8 卸载注意点
- 停止服务
- 调用 `s.Uninstall()`
- 可选：询问是否删除日志与配置（交互 / `--purge` flag）

### 4.9 No-op Service 设计模式
实际项目中发现一种设计模式：**服务只负责 install/uninstall，不处理应用程序的真实逻辑**。所有业务逻辑只在前台 `run` 模式启动。

**优势：**
- 服务管理与业务逻辑完全解耦
- 简化服务调试（前台运行时行为一致）
- 避免服务模式下的复杂状态管理

**实现方式：**
```go
type noopProgram struct{}
func (n *noopProgram) Start(s service.Service) error { return nil }
func (n *noopProgram) Stop(s service.Service) error  { return nil }
```

**注意事项：**
- 使用此模式时，`launchctl load` 不会启动实际进程
- 系统服务只起到注册占位作用
- 真正的应用启动需要其他机制（如手动运行或外部调度）

---
## 5. 平台具体生成示例

### 5.1 systemd Unit（仅供参考，使用库时无需手写）
```ini
[Unit]
Description=Kratos Layout Web Service
After=network.target

[Service]
Type=simple
User=kratos
Group=kratos
WorkingDirectory=/opt/kratos-layout
ExecStart=/opt/kratos-layout/web run --config /etc/kratos-layout/config.yaml --log-dir /var/log/kratos-layout
Restart=on-failure
RestartSec=3
NoNewPrivileges=yes
ProtectSystem=full
ProtectHome=true
ReadWritePaths=/var/log/kratos-layout

[Install]
WantedBy=multi-user.target
```

### 5.2 macOS LaunchDaemon plist（参考）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.kratos.layout.web</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/web</string>
    <string>run</string>
    <string>--config</string>
    <string>/Library/Application Support/kratos-layout/config.yaml</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/var/log/kratos-layout/app.out.log</string>
  <key>StandardErrorPath</key><string>/var/log/kratos-layout/app.err.log</string>
  <key>UserName</key><string>kratos</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>KRATOS_ENV</key><string>prod</string>
  </dict>
</dict>
</plist>
```

### 5.3 Windows PowerShell 注册（参考）
```powershell
New-Service -Name "KratosLayoutWeb" -BinaryPathName "C:\Program Files\KratosLayout\web.exe run --config C:\ProgramData\KratosLayout\config.yaml" -DisplayName "Kratos Layout Web" -Description "Kratos Layout Web Service" -StartupType Automatic
```

---
## 6. 子命令行为（拟定）
| 子命令 | 说明 | 关键动作 |
|--------|------|----------|
| run | 前台运行（开发/容器用） | 解析配置 -> wire -> Start -> 阻塞 |
| install | 安装为系统服务 | 构造 service.Config -> s.Install() |
| uninstall | 卸载 | s.Stop() -> s.Uninstall() |
| help | 显示帮助信息 | 输出使用说明 |

**注意**：当前实现采用 no-op service 模式，因此不提供 start/stop/restart/status 子命令，这些操作需要通过系统原生命令完成（如 `systemctl`、`launchctl` 等）。

退出码约定：
- 0 成功
- 1 一般错误（参数 / 未安装）
- 2 权限不足
- 3 配置加载失败

---
## 7. 未来扩展
| 方向 | 描述 | 备注 |
|------|------|------|
| 热重载 | SIGHUP / API 触发 `ReloadConfig()` | 需抽象 config provider |
| Metrics | Prometheus `/metrics` | 结合 gin route |
| Tracing | OpenTelemetry | 链路注入中间件 |
| 安全 | systemd sandbox keys | 默认模板生成 |
| 日志 | 支持 JSON / 结构化 + 日志切割 | 依赖 kitlog 或 logrus hook |
| 多实例 | `--instance` 前缀隔离日志、端口 | Unit 名后缀 |
| 租户隔离 | 运行多个配置集 | 配合多进程或 goroutine pool |

## 7.1 实际开发经验补充
### 7.1.1 代码结构最佳实践
- **统一参数解析**：将 `parseConfigFlag` 设计为支持所有子命令（run/install/uninstall/status），避免重复代码
- **分离业务逻辑**：所有实际业务代码放在 `run()` 函数中，服务管理函数只处理系统集成
- **错误处理一致性**：install/uninstall 失败时使用 `os.Exit(1)`，确保 shell 脚本能正确检测状态

### 7.1.2 多模块支持
对于包含多个可执行文件的项目（如 web + task），建议：
- 每个模块独立实现 services.go
- 使用不同的服务名称避免冲突（如 `kratos-layout-web` vs `kratos-layout-task`）
- 复用相同的设计模式和代码结构
- 注意服务间端口不冲突（web 通常需要 HTTP 端口，task 可能不需要）

---
## 8. 实施步骤（开发任务清单）
1. ✅ 引入依赖：`kardianos/service`
2. ✅ 拆分 `web.Run()` 和 `task.Run()` 为：子命令解析 + `run()` 前台运行
3. ✅ 新增 `internal/app/web/services.go` 和 `internal/app/task/services.go` 实现服务管理
4. ✅ 在各 app.go 中增加子命令解析逻辑
5. ✅ 实现 no-op service 模式（服务只负责 install/uninstall）
6. 📋 文档更新 README：使用示例、权限说明
7. 📋 可选：添加最小单元测试（install dry-run 等）

---
## 9. 风险与缓解
| 风险 | 场景 | 缓解措施 |
|------|------|----------|
| 权限不足安装失败 | 非 root 安装 systemd | 捕获错误提示 sudo 指令 |
| 用户不存在 | 指定 `--user` | 预检并给出创建用户命令建议 |
| 配置路径不可读 | 错误权限 / SELinux | 安装前校验 + 失败友好提示 |
| Windows 防病毒阻止 | 写日志或运行 | 记录文档白名单指引 |
| 杂散进程无法停止 | 未正确记录 pid | 使用库的内部跟踪；再加 pidfile 双保险 |
| 日志过大 | 长期运行 | 建议接入 logrotate / Windows 计划任务清理 |
| macOS plist 权限问题 | plist 文件所有者/权限不正确 | 确保系统级 plist 为 root:wheel 644 权限 |
| 服务注册但不启动 | no-op service 设计 | 明确告知用户这是设计行为，需单独启动业务逻辑 |

## 9.1 调试指南
### 9.1.1 macOS launchd 调试步骤
1. **检查 plist 语法**：`plutil -lint /Library/LaunchDaemons/xxx.plist`
2. **检查文件权限**：`ls -l /Library/LaunchDaemons/ | grep xxx`
3. **查看详细状态**：`sudo launchctl print system/xxx`
4. **检查日志文件**：`sudo tail -f /var/log/xxx.out.log /var/log/xxx.err.log`
5. **手动测试命令**：直接运行 plist 中的 ProgramArguments 验证参数正确性

### 9.1.2 常见错误码含义
- `runs=0`：服务已注册但从未启动过
- `last exit code: 0`：服务正常退出（可能是 no-op 或一次性任务）
- `Permission denied`：plist 文件权限问题或目标用户权限不足

---
## 10. 与容器/K8s 的关系
本方案专注“裸机 / VM” 部署。如果未来走容器：
- 直接以 `web run` 前台模式作为容器 ENTRYPOINT
- 健康探针：`/healthz`
- 配置注入：ConfigMap/Secret -> 挂载到 `/app/configs/config.yaml`
- 进程不再需要 install/uninstall；由 orchestrator 管理生命周期

---
## 11. 最终推荐
采用 `kardianos/service` + 子命令模式，提供统一跨平台体验，最少维护成本。逐步在后续迭代中补充：
1. 拆分运行逻辑
2. 实现子命令
3. 加入最小权限校验
4. 增强可观测（health/metrics）
5. 实现热重载（SIGHUP + fsnotify）

---
## 12. 附：伪代码示例
```go
func main() {
    if len(os.Args) < 2 || os.Args[1] == "run" { 
        run(); // 前台运行业务逻辑
        return 
    }
    sub := os.Args[1]
    switch sub {
    case "install": 
        configPath := parseConfigFlag()
        sm, _ := NewServiceManager(configPath)
        err = sm.Install()
    case "uninstall": 
        configPath := parseConfigFlag()
        sm, _ := NewServiceManager(configPath)
        err = sm.Uninstall()
    case "help", "--help", "-h":
        printUsage()
    default: 
        fmt.Printf("未知命令: %s\n", sub)
        printUsage()
    }
    if err != nil { os.Exit(1) }
}
```

---