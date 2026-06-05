#!/bin/bash
set -e

# Claude Code 中文增强配置 - 一键安装脚本

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_SETTINGS="$SCRIPT_DIR/.claude/settings.json"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Claude Code 中文增强配置 - 安装程序${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}错误: 未检测到 Claude Code CLI${NC}"
    echo "请先安装: https://docs.anthropic.com/en/docs/claude-code"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Claude Code 已安装"

# Check optional dependencies
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}[提示]${NC} 未检测到 Node.js — 状态栏 HUD 功能将不可用（不影响核心功能）"
fi

HAS_JQ=false
if command -v jq &> /dev/null; then
    HAS_JQ=true
    echo -e "${GREEN}[OK]${NC} jq 已安装（支持配置合并）"
else
    echo -e "${YELLOW}[提示]${NC} 未安装 jq — 将使用安全合并模式"
fi

# Create .claude directory if not exists
mkdir -p "$CLAUDE_DIR"

# Backup existing settings
if [ -f "$SETTINGS_FILE" ]; then
    BACKUP="$SETTINGS_FILE.bak.$(date +%Y%m%d%H%M%S)"
    cp "$SETTINGS_FILE" "$BACKUP"
    echo -e "${YELLOW}[备份]${NC} 已备份现有配置到: $BACKUP"
fi

if [ -f "$SETTINGS_FILE" ]; then
    if [ "$HAS_JQ" = true ]; then
        echo -e "${GREEN}[合并]${NC} 与现有配置合并中..."
        jq -s '
            .[0] as $existing |
            .[1] as $package |
            $existing * {
                extraKnownMarketplaces: ($package.extraKnownMarketplaces // .[0].extraKnownMarketplaces),
                enabledPlugins: ($package.enabledPlugins // .[0].enabledPlugins),
                statusLine: ($package.statusLine // .[0].statusLine),
                language: ($package.language // .[0].language),
                spinnerTipsEnabled: ($package.spinnerTipsEnabled // .[0].spinnerTipsEnabled),
                spinnerVerbs: ($package.spinnerVerbs // .[0].spinnerVerbs),
                spinnerTipsOverride: ($package.spinnerTipsOverride // .[0].spinnerTipsOverride)
            }
        ' "$SETTINGS_FILE" "$PACKAGE_SETTINGS" > "$SETTINGS_FILE.tmp"
        mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
    else
        echo -e "${GREEN}[合并]${NC} 安全合并配置（保留你的 env、permissions 等个人设置）..."
        # Without jq: only append missing keys from package settings, never overwrite existing ones
        python3 -c "
import json, sys
with open('$SETTINGS_FILE') as f:
    existing = json.load(f)
with open('$PACKAGE_SETTINGS') as f:
    package = json.load(f)
# Only add keys that don't already exist in the user's settings
for key, value in package.items():
    if key not in existing:
        existing[key] = value
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('  安全合并完成')
" 2>/dev/null || {
            echo -e "${YELLOW}[警告]${NC} 无法安全合并（缺少 jq 和 python3），跳过覆盖以保护你的现有配置"
            echo -e "${YELLOW}[建议]${NC} 请安装 jq 后重试: brew install jq / apt install jq / choco install jq"
            echo ""
            echo -e "或者手动将以下内容添加到 $SETTINGS_FILE 中:"
            cat "$PACKAGE_SETTINGS"
            exit 1
        }
    fi
else
    echo -e "${GREEN}[安装]${NC} 写入配置..."
    cp "$PACKAGE_SETTINGS" "$SETTINGS_FILE"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  安装完成!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "已配置:"
echo -e "  - 中文语言"
echo -e "  - superpowers 插件 (超强能力技能包)"
echo -e "  - claude-hud 插件 (状态栏)"
echo -e "  - 200+ 个中文加载动画"
echo -e "  - 40+ 条中文使用技巧"
echo ""
echo -e "运行 ${GREEN}claude${NC} 启动体验"
echo ""
echo -e "${YELLOW}提示: 如果使用代理，请在 ~/.claude/settings.json 的 env 中配置:${NC}"
echo -e '  "env": { "ANTHROPIC_BASE_URL": "http://你的代理地址:端口" }'
