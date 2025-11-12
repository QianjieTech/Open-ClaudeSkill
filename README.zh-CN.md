# Open-ClaudeSkill

**支持渐进式披露的 Claude Skills MCP 服务器**

将任何兼容 MCP 的 Agent 应用转变为 Claude Skills 强大平台。本服务器支持环境感知、热重载的技能管理，适用于所有 MCP 客户端。

[English](README.md) | 简体中文

## 特性

- **零配置体验**：Skill 文件自动发现和加载
- **实时热重载**：文件修改立即生效（取决于协议特性支持）
- **环境感知**：自动检测项目环境，支持全局/项目级配置
- **跨平台兼容**：标准 MCP 协议，适配所有 Agent 应用
- **优雅降级**：根据客户端能力自动适配

## 快速开始

### 安装

```bash
# 使用 uv 安装（推荐）
uv pip install mcp-server-skill

# 或从源码安装
git clone https://github.com/your-org/open-claudeskill
cd open-claudeskill
uv pip install -e .
```

### 配置

在 MCP 客户端配置中添加：

```json
{
  "mcpServers": {
    "skills": {
      "command": "uv",
      "args": ["run", "mcp-server-skill"]
    }
  }
}
```

### 创建 Skills

1. 在项目中创建 `.skill` 目录
2. 添加包含 `SKILL.md` 文件的 skill 文件夹：

```
.skill/
├── my-skill/
│   ├── SKILL.md          # Skill 定义文件
│   └── templates/        # 可选资源
```

3. 在 `SKILL.md` 中定义你的 skill：

```markdown
---
name: my-skill
description: 这个 skill 的功能和使用场景
license: MIT
---

# Skill 指令

为 Agent 提供的详细指令...
```

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

1. **命令行参数**：`--skills-dir /path/to/.skill`
2. **环境变量**：`MCP_SKILLS_DIR=/path/to/.skill`
3. **动态设置**：通过 `set_skills_directory` 工具
4. **项目级别**：项目根目录的 `.skill/`（检测 `.git`、`package.json` 等）
5. **全局回退**：`~/.skill`

## 使用方法

### Type B 客户端（具有本地 Agent 能力）

Agent 可以动态设置 skills 目录：

```
Agent 检测到：用户在 /path/to/project
Agent 调用：set_skills_directory(path="/path/to/project")
服务器响应：发现 5 个 skills：code-reviewer、calculator...
```

### Type A 客户端（无本地 Agent 能力）

使用全局配置：

```bash
mkdir ~/.skill
cp -r examples/code-reviewer ~/.skill/
```

## 提供的工具

### `set_skills_directory`

设置当前会话的 skills 目录。

**参数：**
- `path`（字符串）：项目或 `.skill` 目录的绝对或相对路径

**示例：**
```python
set_skills_directory(path="/path/to/project")
```

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
mcp-server-skill --skills-dir /custom/path --log-level DEBUG
```

### 日志记录

设置调试日志级别：

```bash
mcp-server-skill --log-level DEBUG
```

级别：`DEBUG`、`INFO`、`WARNING`、`ERROR`

## 示例

查看 `examples/` 目录中的示例 skills：

- **algorithmic-art**：使用 p5.js 创建生成艺术
- **canvas-design**：设计视觉艺术和海报
- **brand-guidelines**：应用 Anthropic 品牌样式
- **code-reviewer**：全面的代码审查框架
- **calculator**：数学计算

## 开发

### 从源码运行

```bash
# 安装开发依赖
uv pip install -e .

# 运行服务器
uv run mcp-server-skill

# 使用调试日志运行
uv run mcp-server-skill --log-level DEBUG
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

## 打包与发布

### 构建分发包

```bash
# 构建 Wheel 和源码包
uv build

# 生成文件在 dist/ 目录
# - mcp_server_skill-0.1.1-py3-none-any.whl
# - mcp_server_skill-0.1.1.tar.gz
```

### 安装方式

**方式 1：从 Wheel 包安装**（推荐）
```bash
pip install dist/mcp_server_skill-0.1.1-py3-none-any.whl
```

**方式 2：从 Git 仓库安装**
```bash
pip install git+https://github.com/your-org/open-claudeskill.git
```

**方式 3：从 PyPI 安装**（公开发布后）
```bash
pip install mcp-server-skill
```

详细打包指南请参考：[PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)

## 配置示例

### Cherry Studio

配置文件位置：`%APPDATA%\Cherry Studio\config.json`

```json
{
  "mcpServers": {
    "skills": {
      "command": "mcp-server-skill",
      "args": []
    }
  }
}
```

### Claude Desktop

**Windows**：`%APPDATA%\Claude\claude_desktop_config.json`
**macOS**：`~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**：`~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "skills": {
      "command": "mcp-server-skill",
      "args": ["--skills-dir", "C:\\Users\\YourName\\.skill"]
    }
  }
}
```

### Kilo Code

配置文件位置：`~/.kilo/mcp_config.json`

```json
{
  "mcpServers": {
    "skills": {
      "command": "uv",
      "args": ["run", "mcp-server-skill", "--log-level", "INFO"],
      "env": {
        "MCP_SKILLS_DIR": "/path/to/your/.skill"
      }
    }
  }
}
```

## 项目结构

```
open-claudeskill/
├── src/
│   └── mcp_server_skill/
│       ├── __init__.py
│       ├── server.py           # MCP 服务器实现
│       ├── skill_loader.py     # Skill 发现和解析
│       └── state.py            # 状态管理
├── examples/                   # 示例 skills
│   ├── algorithmic-art/
│   ├── canvas-design/
│   ├── brand-guidelines/
│   ├── code-reviewer/
│   └── calculator/
├── .skill/                     # 本地 skills（不提交到 Git）
├── dist/                       # 构建输出
├── pyproject.toml             # 项目配置
├── README.md                  # 英文文档
├── README.zh-CN.md            # 中文文档
├── PACKAGING_GUIDE.md         # 打包指南
└── REFACTORING_SUMMARY.md     # 重构说明
```

## 常见问题

### Q: 如何创建一个新的 skill？

1. 在 `.skill/` 目录创建新文件夹
2. 创建 `SKILL.md` 文件，包含 YAML 前置元数据和 Markdown 内容
3. 可选：添加辅助资源（templates/、fonts/ 等）

### Q: Skills 目录没有自动检测到怎么办？

使用 `set_skills_directory` 工具手动设置：
```python
set_skills_directory(path="/path/to/your/project")
```

### Q: 如何调试 skill 加载问题？

使用 DEBUG 日志级别运行：
```bash
mcp-server-skill --log-level DEBUG --skills-dir ./.skill
```

### Q: 可以在多个项目间共享 skills 吗？

可以！使用以下方式之一：
- 全局 skills：放在 `~/.skill`
- 环境变量：`export MCP_SKILLS_DIR=/path/to/shared/skills`
- 符号链接：`ln -s /path/to/shared/skills .skill`

### Q: 如何更新已安装的包？

```bash
# 如果从 Wheel 安装
pip install --upgrade --force-reinstall dist/mcp_server_skill-0.1.1-py3-none-any.whl

# 如果从 Git 安装
pip install --upgrade git+https://your-repo/open-claudeskill.git

# 如果从 PyPI 安装
pip install --upgrade mcp-server-skill
```

## 版本历史

### v0.1.1（当前）

**新功能：**
- ✅ 环境感知的路径发现（5 级优先级）
- ✅ `set_skills_directory` 工具
- ✅ 项目根目录自动检测
- ✅ 防抖文件监控（300ms）
- ✅ 辅助资源路径解析
- ✅ 结构化日志系统

**改进：**
- ✅ 移除非官方前置元数据字段（`allowed-tools`、`metadata`）
- ✅ 100% 兼容官方 Claude Skill 规范
- ✅ 更好的错误处理和隔离
- ✅ 优化的构建配置

**修复：**
- 🐛 修复技能名称与文件夹不匹配的警告
- 🐛 改进 Windows 路径处理
- 🐛 修复热重载时的竞态条件

### v0.1.0

- 🎉 初始版本
- 基础 MCP 服务器实现
- 渐进式披露支持
- 基础文件监控

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

- **问题反馈**：[GitHub Issues](https://github.com/your-org/open-claudeskill/issues)
- **讨论**：[GitHub Discussions](https://github.com/your-org/open-claudeskill/discussions)
- **邮件**：your-email@example.com

---

**用 ❤️ 由 Open-ClaudeSkill 社区创建**
