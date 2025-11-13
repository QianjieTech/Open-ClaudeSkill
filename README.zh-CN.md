# AgentSkill MCP

**让任何 MCP 兼容的 Agent 都能使用 Claude Agent Skills**

一个通用的 MCP 服务器，让**任何**支持 MCP 的 Agent 应用都能使用 Anthropic 官方的 [Claude Agent Skills](https://github.com/anthropics/skills)，并实现**渐进式披露** - 减少上下文开销的同时最大化能力。

**包名**: `agentskill-mcp` | **PyPI**: [agentskill-mcp](https://pypi.org/project/agentskill-mcp/)

[English](README.md) | 简体中文

## 为什么需要 AgentSkill MCP?

Claude Agent Skills 设计精妙，但被锁定在 Claude 生态内。本项目打破这一限制：

- ✅ **通用兼容**：适配任何 MCP 兼容的 agent（Kilo Code、Cursor、Roo Code、Codex 等）
- ✅ **100% Claude Skill 兼容**：使用 Anthropic 官方 Skill 格式 - 无需任何修改
- ✅ **渐进式披露**：实现与 Claude Code 相同的智能上下文加载
- ✅ **零锁定**：标准 MCP 协议意味着永不被单一平台锁定

### Skills 解决的问题

传统 MCP 工具会一次性加载所有文档，在你开始工作前就消耗 大量 tokens。加载 15+ 工具后，agent 还没做事就已经上下文告急。

**Skills 通过渐进式披露解决这个问题**：agent 初始只看到轻量级的 skill 列表，仅在需要时才加载完整内容。本项目将同样的效率带给所有 MCP 兼容的 agent。

## 特性

- 🚀 **一行安装**：`pip install agentskill-mcp` 或 `uvx agentskill-mcp`
- 🔌 **通用 MCP 兼容(待逐步测试适配)**：适配 Kilo Code、Cursor、Roo Code、Codex、Cherry Studio 及任何 MCP 兼容 agent
- 📦 **官方 Skill 格式**：完全兼容 [Anthropic 的 Claude Skills](https://github.com/anthropics/skills)
- 🎯 **渐进式披露**：智能上下文加载 - 在需要 skills 之前几乎零开销
- 🔄 **热重载(暂未实现)**：实时检测文件变化并更新（协议支持时）
- 🗂️ **智能路径发现**：自动检测 `.claude/skills/`、`.skill/` 或自定义目录
- 🌍 **环境感知**：项目级和全局 skill 目录，自动检测
- 🎨 **ClaudeCode 兼容**：同时支持 `.claude/skills/`（ClaudeCode 格式）和 `.skill/`（本项目定义的路径格式）

## 项目状态

⚠️ **早期开发阶段** - 本项目目前处于早期开发阶段，目前仅在 Windows 上进行了测试。

**已测试平台：**
- ✅ **Kilo Code**（AI 编码助手）- Windows
- ✅ **Roo Code**（AI 编码助手）- Windows
- ✅ **Cline**（AI 编码助手）- Windows

**下一步计划：**
- 🔄 在更多 MCP 兼容的 agent 上测试（Codex、Cursor、QwenCode 等）
- 🔄 跨平台测试（macOS、Linux）
- 🔄 更广泛的兼容性验证
- 🔄 热重载可行性的测试(基于mcp的​List Changed Notification)具体参见
https://modelcontextprotocol.io/specification/2025-06-18/server/tools#list-changed-notification

**理论上**：任何实现了 [Model Context Protocol](https://modelcontextprotocol.io) 的 agent 都应该能工作，但我们正在积极测试以确认。

## 快速开始

### 配置

⚠️ **当前推荐使用方式**：通过 `--skills-dir` 参数指定 skills 目录

在你的 MCP 客户端配置文件中添加。查看你的 agent 文档找到 MCP 配置位置：
- **Kilo Code**：工作区的 `.kilocode/mcp.json`
- **Roo Code**：查看 agent 文档
- **Cursor**：工作区的 `.cursor/mcp.json`
- **其他 agent**：参考 agent 特定的 MCP 配置指南

**推荐配置（Windows）：**

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "C:\\Users\\YourName\\path\\to\\skills"
      ]
    }
  }
}
```

**macOS/Linux：**

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "/Users/YourName/path/to/skills"
      ]
    }
  }
}
```

**使用 pip 安装版本：**

将 `"command": "uvx"` 替换为 `"command": "agentskill-mcp"`，并从 args 中移除：

```json
{
  "mcpServers": {
    "skills": {
      "command": "agentskill-mcp",
      "args": [
        "--skills-dir",
        "C:\\Users\\YourName\\path\\to\\skills"
      ]
    }
  }
}
```

💡 **提示**：
- 在 `--skills-dir` 中使用绝对路径以避免歧义
- 配置修改后，重启你的 agent 应用或重新加载 MCP 服务器
- 先使用 `examples/` 目录测试，然后再创建自定义 skills

### 加载 Skills

创建 skills 目录并添加 skill 包：

**格式 1：ClaudeCode 格式（推荐给 ClaudeCode 用户）**

```bash
# 在当前项目创建（推荐）
在项目根目录下创建 .claude/skills/

# 或在全局创建
mkdir -p ~/.claude/skills    # Linux/Mac
mkdir C:\Users\YourName\.claude\skills  # Windows
```

**格式 2：本项目自定义格式（兼容其他 agent）**

```bash
# 在当前项目创建
在项目根目录下创建 .skill/

# 或在全局创建
mkdir ~/.skill         # Linux/Mac
mkdir C:\Users\YourName\.skill  # Windows
```

然后在此目录下放入相应的 Skill 包——直接复制 Skill 文件夹粘贴到 skills 目录下即可。项目的 `./examples` 目录下放了若干 Anthropic 官方提供的 Skill 包，足够完成测试。

```bash
# 示例：迁移 skills（ClaudeCode 格式）
复制 examples/canvas-design -> .claude/skills/
复制 examples/brand-guidelines -> .claude/skills/

# 或（本项目自定义格式）
复制 examples/canvas-design -> .skill/
复制 examples/brand-guidelines -> .skill/
```

最终结构：
- ClaudeCode 格式：**`.claude/skills/canvas-design/`**
- 本项目自定义格式：**`.skill/canvas-design/`**

### 试用

重启你的 Agent 应用并测试：

```
帮我制作一份1920x1080的宣传海报，使用 Anthropic 品牌风格。
主题："未来属于人工智能？人工智能只是手段，而非目标"
```

**会发生什么：**
1. Agent 在 `load_skill` 工具描述中看到可用的 skills
2. Agent 识别相关的 skills（`canvas-design`、`brand-guidelines`）
3. Agent 调用 `load_skill` 获取完整的 skill 详情
4. Agent 按照 skill 指导创建海报

**注意**：Agent 可能根据任务理解只调用其中一个 skill。这是正常的 - AI agent 在工具选择上存在固有的随机性。

## Skill 格式

Skills 遵循官方 Claude Skill 格式：

### 前置元数据（YAML）

```yaml
---
name: skill-name          # 必需：需与文件夹名称一致
description: |            # 必需：详细描述，用于 Agent 匹配
  描述这个 skill 的功能和使用场景。
  包含 Agent 应该匹配的关键词。
license: MIT              # 可选：许可证信息
---
```

### Skill 内容

在前置元数据之后，提供详细的 Markdown 指令：

- 清晰、可执行的指导
- 示例和最佳实践
- 辅助资源的引用

### 辅助资源

Skills 可以包含模板、字体、脚本等资源：

```
.skill/
├── algorithmic-art/
│   ├── SKILL.md
│   └── templates/
│       ├── viewer.html
│       └── generator.js
```

在 skill 中引用资源：

```markdown
使用 Read 工具读取 `templates/viewer.html`
```

## 路径发现

服务器按以下优先级自动查找 skills：

1. **命令行参数**：`--skills-dir /path/to/skills` ⭐ **推荐**
2. **环境变量**：`MCP_SKILLS_DIR=/path/to/skills`
3. **项目级别**：项目根目录的 `.claude/skills/` 或 `.skill/`（检测 `.git`、`.claude/`、`package.json` 等）
4. **全局回退**：`~/.skill`

**注意**：项目级别的发现优先选择 `.claude/skills/`（ClaudeCode 格式）而不是 `.skill/`（本项目自定义格式），当两者都存在时。

**当前推荐**：始终使用 `--skills-dir` 参数以获得最佳兼容性。

## 使用示例

### 示例 1：使用绝对路径（推荐）

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "C:\\userfolder\\DevFolder\\my-skills"
      ]
    }
  }
}
```

### 示例 2：使用项目示例

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": [
        "agentskill-mcp",
        "--skills-dir",
        "C:\\path\\to\\Open-ClaudeSkill\\examples"
      ]
    }
  }
}
```

## 提供的工具

### `load_skill`

按名称加载并激活一个 skill。

**参数：**
- `skill`（字符串）：要加载的 skill 名称

**示例：**
```python
load_skill(skill="code-reviewer")
```

## 高级配置

### 环境变量

- `MCP_SKILLS_DIR`：覆盖默认 skills 目录

### 命令行参数

```bash
agentskill-mcp --skills-dir /custom/path --log-level DEBUG
```

### 日志记录

设置调试日志级别：

```bash
agentskill-mcp --log-level DEBUG
```

级别：`DEBUG`、`INFO`、`WARNING`、`ERROR`

## 示例

查看 `examples/` 目录中的示例 skills：

- **algorithmic-art**：使用 p5.js 创建生成艺术
- **canvas-design**：设计视觉艺术和海报
- **brand-guidelines**：应用 Anthropic 品牌样式
- **code-reviewer**：全面的代码审查框架
- **calculator**：数学计算

### 安装

**方式 1：使用 pip（推荐）**

```bash
pip install agentskill-mcp
```

**方式 2：使用 uvx（无需安装即可试用）**

```bash
# 直接运行，无需安装
uvx agentskill-mcp --help
```

**方式 3：使用 uv**

```bash
uv pip install agentskill-mcp
```

**验证安装：**

```bash
agentskill-mcp --help

# 预期输出:
# usage: agentskill-mcp [-h] [--skills-dir SKILLS_DIR]
#                       [--log-level {DEBUG,INFO,WARNING,ERROR}]
#
# AgentSkill MCP - MCP Server for Claude Skills with progressive disclosure
```

**开发模式**（如果需要修改代码）：

```bash
git clone https://github.com/QianjieTech/Open-ClaudeSkill.git
cd Open-ClaudeSkill
pip install -e .
```

## 开发

### 从源码运行

```bash
# 安装开发依赖
uv pip install -e .

# 运行服务器
uv run agentskill-mcp

# 使用调试日志运行
uv run agentskill-mcp --log-level DEBUG
```

### 创建自定义 Skills

1. 复制示例 skill 作为模板
2. 修改前置元数据（name、description）
3. 更新指令内容
4. 添加任何辅助资源
5. 使用你的 Agent 测试

## 架构

### 核心组件

- **ServerState**：管理运行时状态和路径发现
- **SkillLoader**：发现和解析 skill 文件
- **SkillFileHandler**：使用防抖监控文件变化
- **SkillMCPServer**：主 MCP 服务器实现

### 渐进式披露

Skills 通过单个 `load_skill` 工具暴露，该工具在描述中列出所有可用的 skills。这样可以最小化初始 token 使用，同时提供完整的发现功能。

### 热重载

通过 watchdog 检测文件变化并触发 skill 重新加载。变化对下一个 Agent 请求立即生效。

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

### 贡献者

感谢所有贡献者的付出！

## 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE) 文件。

## 资源

- **文档**：[官方文档](https://github.com/your-org/open-claudeskill)
- **Agent Skills 规范**：[Anthropic 规范](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- **MCP 协议**：[Model Context Protocol](https://modelcontextprotocol.io)
- **问题反馈**：[GitHub Issues](https://github.com/your-org/open-claudeskill/issues)

## 致谢

本项目基于以下开源项目：

- [MCP (Model Context Protocol)](https://modelcontextprotocol.io) - Anthropic
- [Claude Skills](https://www.anthropic.com/news/claude-code-skills) - Anthropic
- [watchdog](https://github.com/gorakhargosh/watchdog) - 文件系统监控
- [PyYAML](https://pyyaml.org/) - YAML 解析

## 联系方式

Q群: 1065081197

---
