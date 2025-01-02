# 包导入别名映射表

## 说明

本文档定义了项目中所有包的标准别名映射。别名映射表用于：
1. 自动检查导入别名是否符合规范
2. 自动生成正确的别名
3. 保持代码一致性和可读性

---

## 映射表结构

### 优先级规则

1. **项目内部包**（第四段） - 最高优先级
2. **fsyyft-go 包**（第三段） - 次高优先级
3. **第三方包**（第二段） - 建议性别名
4. **Go 标准库**（第一段） - 不需要别名

---

## 第一段：Go 标准库

### 无别名要求

以下包**不应**取别名，直接使用包名：

| 包名 | 用途 |
|------|------|
| `context` | 请求上下文，用于取消与超时控制 |
| `fmt` | 格式化 I/O |
| `strings` | 字符串操作 |
| `time` | 时间和日期 |
| `errors` | 错误处理 |
| `io` | 原始 I/O 操作 |
| `os` | 操作系统接口 |
| `path` | 路径操作（斜杠分隔） |
| `path/filepath` | 路径操作（系统分隔） |
| `sync` | 基本同步原语 |
| `http` | HTTP 客户端和服务端 |
| `net/http` | HTTP 客户端和服务端 |
| `encoding/json` | JSON 编码和解码 |
| `database/sql` | 数据库通用接口 |

**规则**：
- 标准库包**永远不**取别名
- 直接使用包名调用函数

---

## 第二段：第三方包

### 建议性别名（非强制）

| 包路径 | 建议别名 | 理由 | 优先级 |
|-------|---------|------|-------|
| `github.com/go-kratos/kratos/v2` | `kratos` | 核心框架包 | 高 |
| `github.com/go-kratos/kratos/v2/errors` | `kratoserrors` | 错误处理包 | 高 |
| `github.com/go-kratos/kratos/v2/log` | `kratoslog` | 日志包 | 中 |
| `github.com/go-kratos/kratos/v2/middleware` | `kratosmiddleware` | 中间件包 | 中 |
| `github.com/go-kratos/kratos/v2/transport/http` | `kratoshttp` | HTTP 传输层 | 高 |
| `github.com/go-kratos/kratos/v2/transport/grpc` | `kratosgrpc` | gRPC 传输层 | 高 |
| `github.com/go-kratos/kratos/v2/config` | `kratosconfig` | 配置管理 | 中 |
| `github.com/gin-gonic/gin` | `gingin` 或无 | Web 框架 | 低 |
| `github.com/golang/protobuf/proto` | `proto` | Protocol Buffers | 高 |
| `github.com/google/wire` | `wire` | 依赖注入 | 高 |
| `google.golang.org/grpc` | `grpc` | gRPC 框架 | 高 |
| `google.golang.org/protobuf/proto` | `proto` | Protobuf API | 高 |
| `github.com/prometheus/client_golang/prometheus` | `prometheus` | 监控指标 | 中 |
| `github.com/prometheus/client_golang/prometheus/promhttp` | `promhttp` | Prometheus HTTP | 中 |
| `go.uber.org/zap` | `zaplog` 或 `zap` | 日志库 | 低 |
| `github.com/spf13/viper` | `viper` | 配置管理 | 中 |
| `github.com/go-sql-driver/mysql` | - | MySQL 驱动，通常使用 `_` 别名 | 低 |
| `github.com/lib/pq` | - | PostgreSQL 驱动，通常使用 `_` 别名 | 低 |

**规则**：
- 第三方包别名是**建议性**的，不是强制的
- 目的：提高代码可读性
- 如果包名本身已经很明确（如 `gin`, `wire`），可以不取别名
- 数据库驱动通常使用 `_` 别名（仅导入副作用）

---

## 第三段：fsyyft-go 包

### 强制别名（kit 前缀）

所有来自 `github.com/fsyyft-go` 的包**必须**使用 `kit` 前缀别名。

#### kit 核心包

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kit/log` | `kitlog` | 日志组件 |
| `github.com/fsyyft-go/kit/runtime` | `kitruntime` | 运行时管理 |
| `github.com/fsyyft-go/kit/config` | `kitconfig` | 配置管理 |

#### kit Kratos 集成包

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kit/kratos` | `kitkratos` | Kratos 集成核心 |
| `github.com/fsyyft-go/kit/kratos/middleware` | `kitkratosmiddleware` | Kratos 中间件 |
| `github.com/fsyyft-go/kit/kratos/middleware/logging` | `kitkratosmiddlewarelogging` | 日志中间件 |
| `github.com/fsyyft-go/kit/kratos/middleware/validate` | `kitkratosmiddlewarevalidate` | 验证中间件 |
| `github.com/fsyyft-go/kit/kratos/middleware/recovery` | `kitkratosmiddlewarerecovery` | 恢复中间件 |

#### kit 数据包

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kit/data` | `kitdata` | 数据访问层 |
| `github.com/fsyyft-go/kit/data/ent` | `kitdataent` | Ent ORM 集成 |
| `github.com/fsyyft-go/kit/data/redis` | `kitdataredis` | Redis 客户端 |
| `github.com/fsyyft-go/kit/data/mongo` | `kitdatamongo` | MongoDB 客户端 |

#### kit 工具包

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kit/util` | `kitutil` | 通用工具 |
| `github.com/fsyyft-go/kit/util/collection` | `kitutilcollection` | 集合工具 |
| `github.com/fsyyft-go/kit/util/time` | `kittutiltime` | 时间工具 |

**命名规则**：
1. 基础规则：`kit` + 去除前缀后的路径段拼接
2. 示例：
   - `kit/log` → `kit` + `log` = `kitlog`
   - `kit/kratos/middleware` → `kit` + `kratos` + `middleware` = `kitkratosmiddleware`
   - `kit/runtime` → `kit` + `runtime` = `kitruntime`

**特殊情况**：
- 如果包路径的最后一段与前面的段重复，可以简化
- 示例：`kit/kratos/kratos` → `kitkratos`（而非 `kitkratoskratos`）

---

## 第四段：项目内部包

### 强制别名（app 前缀）

所有来自 `github.com/fsyyft-go/kratos-layout` 的包**必须**使用 `app` 前缀别名。

#### API 包（api/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/api/helloworld/v1` | `apphelloworldv1` | HelloWorld API v1 |
| `github.com/fsyyft-go/kratos-layout/api/user/v1` | `appuserv1` | User API v1 |
| `github.com/fsyyft-go/kratos-layout/api/order/v1` | `apporderv1` | Order API v1 |
| `github.com/fsyyft-go/kratos-layout/api/product/v1` | `appproductv1` | Product API v1 |

**命名规则**：
- `app` + API 名称 + 版本号
- 示例：`api/helloworld/v1` → `apphelloworldv1`

#### 内部包（internal/）

##### 业务逻辑层（biz/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/internal/biz` | `appbiz` | 业务逻辑层核心 |
| `github.com/fsyyft-go/kratos-layout/internal/biz/greeter` | `appbizgreeter` | Greeter 业务逻辑 |
| `github.com/fsyyft-go/kratos-layout/internal/biz/user` | `appbizuser` | User 业务逻辑 |
| `github.com/fsyyft-go/kratos-layout/internal/biz/order` | `appbizorder` | Order 业务逻辑 |

**命名规则**：
- `app` + `biz` + 业务领域名
- 示例：`internal/biz/greeter` → `appbizgreeter`

##### 数据访问层（data/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/internal/data` | `appdata` | 数据访问层核心 |
| `github.com/fsyyft-go/kratos-layout/internal/data/greeter` | `appdatagreeter` | Greeter 数据访问 |
| `github.com/fsyyft-go/kratos-layout/internal/data/user` | `appdatauser` | User 数据访问 |
| `github.com/fsyyft-go/kratos-layout/internal/data/order` | `appdataorder` | Order 数据访问 |

**命名规则**：
- `app` + `data` + 数据领域名
- 示例：`internal/data/greeter` → `appdatagreeter`

##### 服务层（service/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/internal/service` | `appservice` | 服务层核心 |
| `github.com/fsyyft-go/kratos-layout/internal/service/greeter` | `appservicegreeter` | Greeter 服务 |
| `github.com/fsyyft-go/kratos-layout/internal/service/user` | `appserviceuser` | User 服务 |
| `github.com/fsyyft-go/kratos-layout/internal/service/order` | `appserviceorder` | Order 服务 |

**命名规则**：
- `app` + `service` + 服务领域名
- 示例：`internal/service/greeter` → `appservicegreeter`

##### 服务器层（server/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/internal/server` | `appserver` | 服务器核心 |
| `github.com/fsyyft-go/kratos-layout/internal/server/http` | `appserverhttp` | HTTP 服务器 |
| `github.com/fsyyft-go/kratos-layout/internal/server/grpc` | `appservergrpc` | gRPC 服务器 |

**命名规则**：
- `app` + `server` + 服务器类型
- 示例：`internal/server/http` → `appserverhttp`

##### 领域模型（domain/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/internal/domain` | `appdomain` | 领域模型核心 |
| `github.com/fsyyft-go/kratos-layout/internal/domain/greeter` | `appdomaingreeter` | Greeter 领域模型 |
| `github.com/fsyyft-go/kratos-layout/internal/domain/user` | `appdomainuser` | User 领域模型 |
| `github.com/fsyyft-go/kratos-layout/internal/domain/order` | `appdomainorder` | Order 领域模型 |

**命名规则**：
- `app` + `domain` + 领域名
- 示例：`internal/domain/greeter` → `appdomaingreeter`

#### 公共包（pkg/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/internal/pkg/conf` | `appconf` | 配置管理 |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/log` | `applog` | 日志工具 |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/util` | `apputil` | 通用工具 |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/middleware` | `appmiddleware` | 公共中间件 |

**命名规则**：
- `app` + 包名（去除 pkg 前缀）
- 示例：`internal/pkg/conf` → `appconf`

#### 命令行工具（cmd/）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/cmd` | `appcmd` | 命令行工具核心 |
| `github.com/fsyyft-go/kratos-layout/cmd/web` | `appcmdweb` | Web 服务命令 |
| `github.com/fsyyft-go/kratos-layout/cmd/worker` | `appcmdworker` | Worker 命令 |

**命名规则**：
- `app` + `cmd` + 命令名
- 示例：`cmd/web` → `appcmdweb`

---

## 别名生成算法

### 自动生成规则

```python
def generate_alias(import_path):
    """生成标准别名

    规则：
    1. 项目内部包：app + 路径段拼接
    2. fsyyft-go 包：kit + 路径段拼接
    3. 第三方包：根据建议表或自定义
    4. 标准库：无别名
    """

    # 项目内部包
    if import_path.startswith("github.com/fsyyft-go/kratos-layout"):
        # 去除前缀
        relative_path = import_path.replace("github.com/fsyyft-go/kratos-layout/", "")
        # 拼接路径段
        segments = relative_path.split("/")
        alias = "app" + "".join(seg.capitalize() for seg in segments)
        return alias

    # fsyyft-go 包
    elif import_path.startswith("github.com/fsyyft-go"):
        # 去除前缀
        relative_path = import_path.replace("github.com/fsyyft-go/", "")
        # 拼接路径段
        segments = relative_path.split("/")
        alias = "kit" + "".join(seg.lower() for seg in segments)
        return alias

    # 标准库和第三方包
    else:
        return None  # 不需要或自定义别名
```

### 示例

| 输入路径 | 生成别名 | 类型 |
|---------|---------|------|
| `internal/biz/greeter` | `appbizgreeter` | 项目内部 |
| `internal/data/user` | `appdatauser` | 项目内部 |
| `github.com/fsyyft-go/kit/log` | `kitlog` | fsyyft-go |
| `github.com/fsyyft-go/kit/kratos/middleware` | `kitkratosmiddleware` | fsyyft-go |
| `context` | `None` | 标准库 |
| `github.com/go-kratos/kratos/v2` | `kratos` | 第三方（建议） |

---

## 检查规则

### 强制检查

以下情况**必须**使用标准别名：

1. ❌ **不使用别名**（fsyyft-go 包和项目内部包）
   ```go
   import "github.com/fsyyft-go/kit/log"  // ❌ 错误
   import "github.com/fsyyft-go/kratos-layout/internal/biz"  // ❌ 错误
   ```

2. ❌ **使用错误的前缀**
   ```go
   import (
       applog "github.com/fsyyft-go/kit/log"  // ❌ 应使用 kit 前缀
       kitbiz "github.com/fsyyft-go/kratos-layout/internal/biz"  // ❌ 应使用 app 前缀
   )
   ```

3. ❌ **使用非标准别名**（已在映射表中的包）
   ```go
   import (
       mylog "github.com/fsyyft-go/kit/log"  // ❌ 应使用 kitlog
       biz "github.com/fsyyft-go/kratos-layout/internal/biz"  // ❌ 应使用 appbiz
   )
   ```

### 建议检查

以下情况建议使用标准别名：

1. ⚠️ **第三方包未取别名**（可能导致歧义）
   ```go
   import "github.com/go-kratos/kratos/v2/transport/http"  // ⚠️ 建议使用 kratoshttp
   ```

2. ⚠️ **第三方包使用了不明确的别名**
   ```go
   import h "github.com/go-kratos/kratos/v2/transport/http"  // ⚠️ 建议使用 kratoshttp
   ```

---

## 维护指南

### 添加新包到映射表

当项目新增包时，按以下步骤更新映射表：

1. **确定包类型**：
   - 项目内部包 → 添加到第四段
   - fsyyft-go 包 → 添加到第三段
   - 第三方包 → 添加到第二段（可选）

2. **生成别名**：
   - 项目内部：`app` + 路径段拼接
   - fsyyft-go：`kit` + 路径段拼接
   - 第三方：根据包特征决定

3. **添加到对应章节**：
   - 更新本映射表
   - 确保别名唯一性

4. **更新 check_imports.py**：
   - 在 `STANDARD_ALIASES` 字典中添加映射
   - 运行测试验证

### 别名冲突处理

如果两个不同的包可能生成相同的别名：

1. **检查冲突**：
   ```python
   aliases = {}
   for import_path in all_imports:
       alias = generate_alias(import_path)
       if alias in aliases:
           print(f"冲突：{alias} <- {aliases[alias]} 和 {import_path}")
       else:
           aliases[alias] = import_path
   ```

2. **解决方法**：
   - **方法 1**：调整别名生成规则，加入更多上下文
   - **方法 2**：手动指定唯一别名
   - **方法 3**：重新组织包结构

---

## 参考资料

### 相关文档

- `import_standards.md` - 完整的导入规范
- `.ai/rule.md.bak` - 项目原始规范（第 880-1000 行）

### 工具支持

- `check_imports.py` - 自动检查别名一致性
- `fix_imports.py` - 自动修复别名问题
- `generate_report.py` - 生成别名问题报告

### 自动化脚本

```bash
# 检查别名一致性
python3 .claude/skills/import-enforcer/scripts/check_imports.py

# 生成别名报告
python3 .claude/skills/import-enforcer/scripts/generate_report.py

# 修复别名问题
python3 .claude/skills/import-enforcer/scripts/fix_imports.py report.md
```
