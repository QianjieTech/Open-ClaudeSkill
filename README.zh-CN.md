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

> **⚠️ 当前状态**: 本项目暂未发布到 PyPI，目前无法通过 `uvx mcp-server-skill` 的方式直接使用。我们会尽快打包上传到 PyPI，届时您可以像使用其他 MCP 工具一样通过简单的配置启用 AgentSkill 能力。目前请按照下面的安装指南体验。

**项目地址**: https://github.com/QianjieTech/Open-ClaudeSkill

### 第一步：克隆项目

```bash
git clone https://github.com/QianjieTech/Open-ClaudeSkill.git
cd Open-ClaudeSkill
```

### 第二步：安装依赖

**方式 A：使用系统 Python**

```bash
pip install -e .
```

这会将 `mcp-server-skill` 命令安装到系统 Python 的 Scripts 目录，通常在 PATH 中。

**方式 B：使用 uv（推荐开发者）**

如果使用 uv，命令不会自动加入 PATH，需要通过 `uv run` 调用：

```bash
uv venv
uv pip install -e .
```

**验证安装：**

```bash
# 方式 A 安装后
mcp-server-skill --help

# 方式 B 安装后（需要使用 uv run）
uv run mcp-server-skill --help

# 如果安装成功会看到以下输出
usage: mcp-server-skill [-h] [--skills-dir SKILLS_DIR] [--log-level {DEBUG,INFO,WARNING,ERROR}]

MCP Server for Claude Skills with progressive disclosure

options:
  -h, --help            show this help message and exit
  --skills-dir SKILLS_DIR
                        Directory containing skill folders (default: auto-detect)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging level (default: INFO)
```

### 第三步：配置 MCP 客户端

根据你使用的 Agent 应用和安装方式选择对应配置：

#### Kilo Code（推荐，已验证实测）

**如果使用方式 A（系统 Python）：**

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

**如果使用方式 B（uv）：**

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

**需要指定 `--skills-dir` 的情况：**

- mcp服务启动目录不在项目目录

**如果agent可以指定项目级别的mcp配置，那么以项目级别配置本mcp工具，会自动加载读取当前目录下 `.skill/` 目录下的skill包**，否则，需要通过 `--skills-dir` 参数指定skill包所在的目录，才能正确读取到相应的skill。

💡 **提示**：如果kilocode配置了项目级别的mcp但没有成功加载相应的skill，请手动点击"刷新MCP服务器按钮"或重启vscode再尝试

#### QwenCode

编辑配置文件：`C:\Users\替换为你的user名\.qwen\settings.json`（Windows）

在该配置文件中加入以下部分（Qwencode好像只支持全局的mcp设置，因此需要手动指定skill目录）

**系统 Python 安装：**

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

### 第四步：加载Skill

在项目根目录或全局目录创建 `.skill` 文件夹：

```bash
# 在当前项目创建（推荐）
在项目根目录下创建 .skill/

# 或在全局创建
mkdir ~/.skill/                     # Linux/Mac
mkdir C:\Users\YourName\.skill     # Windows
```

然后在此目录下放入相应的Skill包——直接复制Skill文件夹粘贴到 `.skill/` 文件夹下即可。项目的 `./examples` 目录下放了若干Anthropic官方提供的Skill包，足够完成第五步的测试。

```bash
# 一个简单的迁移skill的例子
examples/canvas-design -复制到-> .skill/
examples/brand-guidelines -复制到-> .skill/
```

最终是这种形式：**`.skill/canvas-design/`**

### 第五步：测试体验

重启你的 Agent 应用，然后在对话中输入：

```
帮我制作一份1920*1080的宣传海报, 风格使用Anthropic品牌风格, 主题为: "未来属于人工智能?\n人工智能只是手段, 而非目标"
```

如果一切正常，Agent 会：
1. 识别到你有`canvas-design`和`brand-guidelines`这2个 Skill
2. 自动调用 `load_skill` 工具
3. 按照 Skill 中的指导为你创建一个海报

*当然也可能只调用其中的skill之一，这取决于大模型对于任务的理解，具有一定的随机性，在我的测试里，至少会调用这2个skill之一*

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
