# Claude Code 中文增强配置包

一键配置 Claude Code：中文语言 + 超强插件 + 炫酷状态栏 + 200+ 个中文加载动画

## 前置条件

| 依赖 | 是否必须 | 说明 |
|------|---------|------|
| [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) | 必须 | 本脚本的配置对象 |
| [Node.js](https://nodejs.org/) | 可选 | 状态栏 HUD 需要，不装也不影响其他功能 |
| [jq](https://jqlang.github.io/jq/) | 可选 | 用于智能合并配置（不装则安全跳过，不会覆盖你的原有配置） |

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
| Spinner | 200+ 个中文加载动画（烹饪、武术、太空、舞蹈……） |
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
    "ANTHROPIC_BASE_URL": "http://你的代理地址:端口"
  }
}
```

## 故障排除

### Claude Code 打不开 / 报错

1. **检查 settings.json 语法**：确保 JSON 格式正确，没有多余逗号
   ```bash
   cat ~/.claude/settings.json | python3 -m json.tool
   ```

2. **还原备份**：安装脚本会自动备份原配置，可直接还原
   ```bash
   ls ~/.claude/settings.json.bak.*   # 查看备份
   cp ~/.claude/settings.json.bak.最新时间戳 ~/.claude/settings.json
   ```

3. **全新重装**：删除配置后重新运行安装脚本
   ```bash
   rm ~/.claude/settings.json
   bash setup.sh
   ```

### 状态栏不显示

- 确认已安装 Node.js：`node --version`
- 确认 claude-hud 插件已下载：`ls ~/.claude/plugins/cache/`
- 可手动运行状态栏命令测试：
  ```bash
  plugin_dir=$(ls -1d ~/.claude/plugins/cache/*/claude-hud/*/ 2>/dev/null | sort -V | tail -1)
  node "${plugin_dir}dist/index.js"
  ```

### 插件安装失败

- 检查网络连接，确保能访问 GitHub
- 首次运行 `claude` 时会自动下载插件，需要等待片刻
- 如果网络受限，可尝试配置代理（见上方「配置代理」）

## 卸载

```bash
# 还原备份
cp ~/.claude/settings.json.bak.* ~/.claude/settings.json

# 或手动删除配置中不需要的字段
```

## 仓库内其他项目

### [AutoClicker — 多步骤宏工具](src/)

Windows 桌面自动化点击工具，支持多步骤宏编排、录制回放、图片识别定位与游戏级底层输入模拟。

详见 [src/README.md](src/README.md)

## License

MIT
