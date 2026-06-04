# Claude Code 中文增强配置包

一键配置 Claude Code：中文语言 + 超强插件 + 炫酷状态栏 + 200+ 个中文加载动画

## 一键安装

```bash
curl -sL https://raw.githubusercontent.com/qucheng9896/claude-code-config/main/setup.sh | bash
```

## 包含内容

| 功能 | 说明 |
|------|------|
| 语言 | 中文界面 |
| 插件 | [superpowers](https://github.com/obra/superpowers-marketplace) — 超强能力技能包（TDD、调试、代码审查等） |
| 插件 | [claude-hud](https://github.com/jarrodwatts/claude-hud) — 状态栏 HUD |
| 状态栏 | 自定义 HUD 状态栏，显示在输入框下方 |
| Spinner | 200+ 个中文加载动画（烹饪、武术、太空、烹饪、舞蹈……） |
| 提示 | 40+ 条中文使用技巧，替代默认英文提示 |

## 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/qucheng9896/claude-code-config.git

# 2. 运行安装脚本
cd claude-code-config
bash setup.sh
```

## 配置代理（可选）

如果你使用代理访问 Claude API，在 `~/.claude/settings.json` 中添加：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://你的代理地址:端口",
    "ANTHROPIC_AUTH_TOKEN": "PROXY_MANAGED"
  }
}
```

## 卸载

```bash
# 删除 settings.json 中的相关配置，或直接还原：
cp ~/.claude/settings.json.bak ~/.claude/settings.json
```

## 仓库内其他项目

### [AutoClicker — 多步骤宏工具](src/)

Windows 桌面自动化点击工具，支持多步骤宏编排、录制回放、图片识别定位与游戏级底层输入模拟。

详见 [src/README.md](src/README.md)

## License

MIT
