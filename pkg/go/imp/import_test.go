// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package imp

import (
	"os"
	"testing"

	kitimp "github.com/fsyyft-go/kit/go/imp"
)

// TestImport 测试导入语句检查功能。
// 该测试函数遍历项目中的所有 Go 文件，检查每个文件的导入语句是否符合规范，
// 包括分组、排序和别名规则。如果发现问题，会记录并输出所有问题。
func TestImport(t *testing.T) {
	root := "../../.."
	_ = os.Chdir(root)
	if pwd, err := os.Getwd(); err == nil {
		t.Logf("根目录 %s", pwd)
	}
	allIssues, err := kitimp.Check(".")
	if nil != err {
		t.Logf("%v\n", err)
		return
	}

	if len(allIssues) == 0 {
		t.Logf("所有文件的导入语句都符合规范！")
	} else {
		t.Logf("发现以下导入问题：")
		for _, issue := range allIssues {
			t.Log(issue)
		}
		t.FailNow()
	}
}
