#!/bin/bash
# ====================================================================
# 版本发布脚本
# 用法: ./versions/release.sh <版本号> <版本描述>
# 示例: ./versions/release.sh v0.2.0 "前后端真实连通"
# ====================================================================

VERSION=$1
DESC=$2

if [ -z "$VERSION" ] || [ -z "$DESC" ]; then
    echo "用法: ./versions/release.sh <版本号> <版本描述>"
    echo "示例: ./versions/release.sh v0.2.0 '前后端真实连通'"
    exit 1
fi

echo "========================================="
echo "  准备发布版本: $VERSION"
echo "  描述: $DESC"
echo "========================================="

# 1. 获取 diff 摘要
echo ""
echo "📊 代码变更摘要:"
git diff --stat HEAD~1 HEAD 2>/dev/null || git diff --stat

# 2. 获取当前 commit hash
COMMIT=$(git rev-parse HEAD)
echo ""
echo "🔗 当前 Commit: $COMMIT"

# 3. 创建版本目录
mkdir -p "versions/$VERSION"

# 4. 生成版本记录
cat > "versions/$VERSION/RELEASE.md" << EOF
# 版本 $VERSION — $DESC

> 日期: $(date +%Y-%m-%d)  
> Commit: $COMMIT

---

## 📋 变更摘要

\`\`\`diff
$(git diff --stat HEAD~1 HEAD 2>/dev/null || git diff --stat)
\`\`\`

---

## ✅ 详细变更

### 新增功能


### Bug 修复


### 重构优化


---

## 📊 代码 Diff

\`\`\`diff
$(git diff HEAD~1 HEAD 2>/dev/null | head -200)
\`\`\`

---

## 📁 受影响文件列表

\`\`\`
$(git diff --name-only HEAD~1 HEAD 2>/dev/null)
\`\`\`

---

## 🧪 测试结果

| 测试项 | 结果 | 备注 |
|--------|------|------|
| 编译 | ⬜ | ... |
| 功能测试 | ⬜ | ... |
| 前后端联调 | ⬜ | ... |

---

## 📝 遗留问题


EOF

echo ""
echo "✅ 版本记录已生成: versions/$VERSION/RELEASE.md"
echo ""

# 5. 创建 git tag
git tag -a "$VERSION" -m "$DESC"
echo "✅ Git Tag 已创建: $VERSION"
echo ""
echo "========================================="
echo "  版本发布完成!"
echo "========================================="
