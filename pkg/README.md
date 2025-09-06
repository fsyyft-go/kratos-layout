# `pkg`

`pkg` 目录用于存放可被外部项目复用的通用库或工具包。这里的包设计为对外暴露，其他项目可以通过 import 路径直接引用，适合通用性强、可共享的代码模块。

与 [`internal/pkg`](../internal/pkg/) 目录不同：
- `pkg`：可被外部项目复用，设计为通用库，允许其他项目 import。
- [`internal/pkg`](../internal/pkg/)：仅本项目内部可用，外部无法 import，适合项目专用的工具包。

**建议**：如果你的包希望对外复用，放在 `pkg`；如果只服务于当前项目且不希望被外部依赖，放在 [`internal/pkg`](../internal/pkg/)。

