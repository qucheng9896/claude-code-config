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

# Create .claude directory if not exists
mkdir -p "$CLAUDE_DIR"

# Backup existing settings
if [ -f "$SETTINGS_FILE" ]; then
    BACKUP="$SETTINGS_FILE.bak.$(date +%Y%m%d%H%M%S)"
    cp "$SETTINGS_FILE" "$BACKUP"
    echo -e "${YELLOW}[备份]${NC} 已备份现有配置到: $BACKUP"
fi

# Check if jq is available for merging
if command -v jq &> /dev/null; then
    if [ -f "$SETTINGS_FILE" ]; then
        echo -e "${GREEN}[合并]${NC} 与现有配置合并中..."

        # Read the package settings and merge into existing
        # Preserve: env, permissions, and any user-specific settings
        # Add/override: plugins, language, spinner, statusLine
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
        echo -e "${GREEN}[安装]${NC} 写入配置..."
        cp "$PACKAGE_SETTINGS" "$SETTINGS_FILE"
    fi
else
    echo -e "${YELLOW}[提示]${NC} 未安装 jq，将直接覆盖 settings.json"
    echo -e "${YELLOW}[提示]${NC} 如需保留原有配置，请先安装 jq 再重新运行"
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
echo -e "${YELLOW}提示: 如果使用代理，请在 ~/.claude/settings.json 的 env 中配置 ANTHROPIC_BASE_URL${NC}"
