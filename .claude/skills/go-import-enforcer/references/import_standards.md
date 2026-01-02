# Go 包导入规范

## 规范来源

本文档从 `.ai/rule.md.bak` 第 880-1000 行提取，定义了项目的包导入规范性要求。

---

## 导入格式强制要求

### 三项强制规则

1. **括号包裹**：所有 `import` 语句必须使用 `()` 包裹
2. **段落分组**：按段落分组，段与段之间使用空行分隔
3. **字母排序**：每个段内的包按字母顺序排序

---

## 四段分组规则

### 分段定义

| 段落 | 内容 | 别名要求 | 示例 |
|------|------|---------|------|
| **第一段** | Go 标准库 | 无需别名 | `context`, `fmt`, `strings`, `time` |
| **第二段** | 第三方包（github.com 等） | 建议取别名 | `kratoshttp "github.com/go-kratos/..."` |
| **第三段** | fsyyft-go 相关包 | **强制**使用 `kit` 前缀别名 | `kitlog "github.com/fsyyft-go/kit/log"` |
| **第四段** | 项目内部包 | **强制**使用 `app` 前缀别名 | `appconf "github.com/.../internal/pkg/conf"` |

### 分组判断逻辑

```python
def classify_package(import_path):
    """分类包类型

    返回: "standard", "third_party", "fsyyft", "project"
    """
    if import_path.startswith("github.com/fsyyft-go/kratos-layout"):
        return "project"  # 项目内部包
    elif import_path.startswith("github.com/fsyyft-go"):
        return "fsyyft"  # fsyyft-go 包
    elif "/" not in import_path or import_path in STANDARD_LIBRARY:
        return "standard"  # Go 标准库
    else:
        return "third_party"  # 第三方包
```

### 分组顺序要求

导入块必须严格按照以下顺序出现：

```
1. Go 标准库（standard）
2. 第三方包（third_party）
3. fsyyft-go 相关包（fsyyft）
4. 项目内部包（project）
```

任何违反此顺序的导入都属于分组错误。

---

## 别名规范

### fsyyft-go 包别名（强制使用 kit 前缀）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kit/log` | `kitlog` | 日志组件 |
| `github.com/fsyyft-go/kit/runtime` | `kitruntime` | 运行时组件 |
| `github.com/fsyyft-go/kit/kratos/middleware/validate` | `kitkratosmiddlewarevalidate` | 验证中间件 |

**命名规则**：
- 基础包名（如 log, runtime）直接加 `kit` 前缀
- 复杂路径（如 kit/kratos/middleware/validate）拼接所有路径段，加 `kit` 前缀

### 项目内部包别名（强制使用 app 前缀）

| 包路径 | 强制别名 | 说明 |
|-------|---------|------|
| `github.com/fsyyft-go/kratos-layout/api/helloworld/v1` | `apphelloworldv1` | HelloWorld API v1 |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/conf` | `appconf` | 配置包 |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/log` | `applog` | 日志包 |

**命名规则**：
- 去除 `github.com/fsyyft-go/kratos-layout/` 前缀
- 将剩余路径段拼接，加 `app` 前缀
- 示例：`api/helloworld/v1` → `apphelloworldv1`

### 第三方包别名（建议取别名）

对于第三方包，建议使用有意义的别名以增强代码可读性：

| 包路径 | 建议别名 | 理由 |
|-------|---------|------|
| `github.com/go-kratos/kratos/v2/transport/http` | `kratoshttp` | 明确 Kratos HTTP 传输层 |
| `github.com/go-kratos/kratos/v2/errors` | `kratoserrors` | 明确 Kratos 错误处理 |
| `github.com/gin-gonic/gin` | `gingin` 或无别名 | Gin 框架本身已经很明确 |

---

## 正确示例

### 完整规范的导入块

```go
import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-kratos/kratos/v2/errors"
	kratoshttp "github.com/go-kratos/kratos/v2/transport/http"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	kitlog "github.com/fsyyft-go/kit/log"
	kitruntime "github.com/fsyyft-go/kit/runtime"

	apphelloworldv1 "github.com/fsyyft-go/kratos-layout/api/helloworld/v1"
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
)
```

**符合的规范**：
- ✅ 使用括号包裹
- ✅ 四段分组，段与段之间有空行
- ✅ 每段内按字母排序
- ✅ fsyyft-go 包使用 kit 前缀
- ✅ 项目内部包使用 app 前缀

---

## 错误示例

### 错误 1：未使用括号包裹

```go
// ❌ 错误：未使用括号包裹
import "context"
import "fmt"
```

**修复**：
```go
// ✅ 正确：使用括号包裹
import (
	"context"
	"fmt"
)
```

---

### 错误 2：未分段，未排序

```go
// ❌ 错误：未分段，未排序
import (
	"github.com/go-kratos/kratos/v2/errors"
	"context"
	kitlog "github.com/fsyyft-go/kit/log"
	"fmt"
)
```

**问题**：
- 标准库和第三方包混在一起
- 未按字母排序
- 缺少段落分隔空行

**修复**：
```go
// ✅ 正确：四段分组，排序
import (
	"context"
	"fmt"

	"github.com/go-kratos/kratos/v2/errors"

	kitlog "github.com/fsyyft-go/kit/log"
)
```

---

### 错误 3：fsyyft-go 包未取别名

```go
// ❌ 错误：fsyyft-go 包未取别名
import (
	"github.com/fsyyft-go/kit/log"
)
```

**修复**：
```go
// ✅ 正确：使用 kit 前缀别名
import (
	kitlog "github.com/fsyyft-go/kit/log"
)
```

---

### 错误 4：项目内部包未使用 app 前缀别名

```go
// ❌ 错误：项目内包未使用 app 前缀别名
import (
	conf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
)
```

**修复**：
```go
// ✅ 正确：使用 app 前缀别名
import (
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
)
```

---

## 检查规则

### 格式检查规则

1. **括号检查**：`import` 语句必须紧跟 `(`，同一行或下一行均可
2. **段落分隔检查**：不同类型的包之间必须有空行
3. **排序检查**：每个段内的包路径必须按字母排序

### 分组检查规则

1. **第一段（标准库）**：路径不包含 `/` 或属于 Go 标准库列表
2. **第二段（第三方）**：路径包含域名，不属于 fsyyft-go 或项目内部
3. **第三段（fsyyft-go）**：路径以 `github.com/fsyyft-go` 开头，但不是项目内部
4. **第四段（项目内部）**：路径以 `github.com/fsyyft-go/kratos-layout` 开头

### 别名检查规则

1. **fsyyft-go 包**：别名必须以 `kit` 开头，与标准映射表匹配
2. **项目内部包**：别名必须以 `app` 开头，与标准映射表匹配
3. **第三方包**：如果取别名，别名应有明确意义

---

## 常见问题

### Q1：为什么必须使用括号包裹？

**答**：
- Go 官方推荐的导入格式
- 便于段落分组和排序
- 统一代码风格

### Q2：为什么必须按四段分组？

**答**：
- **可读性**：清晰区分标准库、第三方、框架包、项目包
- **维护性**：易于识别和管理依赖
- **规范性**：符合项目统一标准

### Q3：别名前缀（kit、app）的作用？

**答**：
- **避免冲突**：防止包名重复（如多个 log 包）
- **明确来源**：一眼看出包的归属
- **统一规范**：团队协作时代码风格一致

### Q4：第三方包的别名是强制的吗？

**答**：
- 不是强制的，但**建议**取有意义的别名
- 目的：提高代码可读性
- 示例：`kratoshttp` 比 `http` 更明确

### Q5：如何处理未在标准表中的包？

**答**：
- **fsyyft-go 新包**：使用 `kit` 前缀，拼接路径段
- **项目内部新包**：使用 `app` 前缀，拼接路径段
- **第三方包**：根据需要决定是否取别名

---

## 工具支持

### 自动化检查

使用 import-enforcer 技能自动检查导入规范性：

```bash
# 检查整个项目
python3 .claude/skills/import-enforcer/scripts/check_imports.py

# 检查特定目录
python3 .claude/skills/import-enforcer/scripts/check_imports.py internal/
```

### 自动修复

检查报告生成后，可以自动修复部分问题：

```bash
# 预览修复（不实际修改）
python3 .claude/skills/import-enforcer/scripts/fix_imports.py \
  report.md --dry-run

# 执行修复
python3 .claude/skills/import-enforcer/scripts/fix_imports.py report.md
```

### 配合 Go 工具

```bash
# 使用 goimports 快速格式化（不处理分组和别名）
goimports -w main.go

# 使用 import-enforcer 深度检查（处理分组和别名）
python3 .claude/skills/import-enforcer/scripts/check_imports.py
```

---

## 参考资料

### 官方文档

- [Effective Go - Imports](https://golang.org/doc/effective_go.html#imports)
- [Go Code Review Comments - Imports](https://github.com/golang/go/wiki/CodeReviewComments#imports)

### 项目规范

- `.ai/rule.md.bak` - 项目完整规范（第 880-1000 行）
- `alias_mapping.md` - 标准别名映射表

### 相关工具

- `goimports` - Go 官方导入格式化工具
- `golangci-lint` - Go 代码检查工具（包含导入检查）
- `import-enforcer` - 项目定制化导入规范检查工具
