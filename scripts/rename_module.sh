#!/bin/bash

# 检查是否提供了新的模块名
if [ $# -ne 1 ]; then
    echo "错误：请提供新的模块名"
    echo "用法：$0 <新模块名>"
    echo "示例：$0 github.com/your-username/your-project"
    exit 1
fi

NEW_MODULE_NAME=$1
# 获取当前模块名
CURRENT_MODULE_NAME=$(grep "^module" go.mod | awk '{print $2}')

if [ -z "$CURRENT_MODULE_NAME" ]; then
    echo "错误：无法从 go.mod 获取当前模块名"
    exit 1
fi

echo "当前模块名：$CURRENT_MODULE_NAME"
echo "新模块名：$NEW_MODULE_NAME"
echo "开始重命名模块..."

# 修改 go.mod 文件
sed -i '' "s|module $CURRENT_MODULE_NAME|module $NEW_MODULE_NAME|" go.mod

# 更新所有 .go 文件中的导入路径
find . -name "*.go" -type f -exec sed -i '' "s|\"$CURRENT_MODULE_NAME/|\"$NEW_MODULE_NAME/|g" {} \;

# 运行 go mod tidy 更新依赖
go mod tidy

echo "模块重命名完成！"
echo "请检查更改并提交到版本控制系统。" 