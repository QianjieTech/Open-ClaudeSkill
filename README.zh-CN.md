# Open-ClaudeSkill: 通用技能系统（基于MCP）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

**Open-ClaudeSkill** 是一个开源实现,将 Claude 强大的技能系统带给任何支持 MCP 的 AI Agent。它通过**渐进式披露**机制,让 Agent 能够按需访问专业知识和能力。

[English](README.md) | 简体中文

## 🎯 这是什么?

Claude Code 有一个原生的"技能"系统,使用渐进式披露机制:
- 技能在系统提示词中仅列出简要信息(名称+描述)
- 只有在调用时才加载完整的技能内容
- 这样既节省了 token,又提供了专业能力

**本项目将这种能力带给任何支持 MCP 的 Agent**,使用标准接口而非专有的函数调用。

## ✨ 核心特性

- **🔌 通用兼容**: 支持任何 MCP 兼容的 Agent (Kilo Code、Claude Desktop、Cline、Continue.dev、自定义 Agent)
- **📁 标准格式**: 100% 兼容官方 Claude Skill 格式
- **🔥 热重载**: 自动检测技能变化,无需重启
- **💾 节省上下文**: 渐进式披露只在需要时加载内容
- **🛠️ 简单配置**: 支持 `uvx` 零配置部署
- **🔒 安全**: 技能在本地环境运行

## 🚀 快速开始

### Kilo Code 用户

1. **安装 MCP 服务器**(一次性):
   ```bash
   pip install mcp-server-skill
   # 或直接使用 uvx (无需安装)
   ```

2. **配置 MCP**,编辑 `mcp_settings.json`:
   ```json
   {
     "mcpServers": {
       "skill": {
         "command": "uvx",
         "args": ["mcp-server-skill"],
         "alwaysAllow": ["load_skill"],
         "disabled": false
       }
     }
   }
   ```

3. **创建技能目录**:
   ```bash
   mkdir -p .skill/my-first-skill
   ```

4. **添加技能** (`.skill/my-first-skill/SKILL.md`):
   ```markdown
   ---
   name: my-first-skill
   description: 一个简单的示例技能用于测试
   ---

   # 我的第一个技能

   这个技能演示了系统的使用方法。

   ## 使用说明
   当用户询问测试相关问题时,解释这个技能系统!
   ```

5. **测试**:
   - 重启 Kilo Code
   - 询问: "有哪些可用的技能?"
   - 尝试: "使用 my-first-skill 技能"

### 其他平台

查看 [MCP_CONFIG.md](MCP_CONFIG.md) 获取详细配置说明:
- Claude Desktop
- Cline (VSCode)
- Continue.dev
- 自定义 MCP 客户端

## 📖 工作原理

### 架构图

```
┌─────────────────────────────────────────────────┐
│         支持 MCP 的 Agent                        │
│      (Kilo Code, Claude Desktop 等)             │
└─────────────────┬───────────────────────────────┘
                  │ MCP 协议
                  │
┌─────────────────▼───────────────────────────────┐
│       mcp-server-skill (本项目)                  │
│  ┌────────────────────────────────────────┐     │
│  │  1. 扫描 .skill/ 文件夹                │     │
│  │  2. 解析 SKILL.md 文件                 │     │
│  │  3. 生成 available_skills XML          │     │
│  │  4. 监控变化 (热重载)                  │     │
│  └────────────────────────────────────────┘     │
└─────────────────┬───────────────────────────────┘
                  │
                  │ 文件系统访问
                  │
┌─────────────────▼───────────────────────────────┐
│            .skill/ 目录                          │
│  ├── calculator/                                 │
│  │   └── SKILL.md                               │
│  ├── code-reviewer/                              │
│  │   └── SKILL.md                               │
│  └── custom-skill/                               │
│      └── SKILL.md                                │
└──────────────────────────────────────────────────┘
```

### 渐进式披露流程

1. **初始状态**: Agent 只看到技能名称和描述(嵌入在工具描述中)
2. **用户请求**: 用户的请求匹配某个技能描述
3. **Agent 决策**: Agent 识别匹配并调用 `load_skill` 工具
4. **内容加载**: 服务器返回完整的技能内容(markdown 指令)
5. **Agent 执行**: Agent 遵循详细的技能指令

这样节省了上下文,因为完整的技能内容只在需要时才加载!

## 📁 技能格式

技能遵循 [Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md):

```markdown
---
name: skill-name
description: 描述技能的作用和使用时机
license: MIT  # 可选
allowed-tools:  # 可选
  - Read
  - Write
metadata:  # 可选
  author: "你的名字"
  version: "1.0"
---

# 技能标题

Markdown 格式的技能说明...

## 章节

- 可以包含任何 markdown 内容
- 代码示例
- 最佳实践
- 工作流程
```

### 必需字段
- `name`: 技能标识符(必须与文件夹名匹配)
- `description`: Agent 何时/如何使用此技能

### 可选字段
- `license`: 许可证信息
- `allowed-tools`: 预批准的工具(用于 Claude Code)
- `metadata`: 自定义键值对

## 🎓 创建技能

### 简单示例

```markdown
---
name: greeting-expert
description: 擅长创作多语言专业问候语。当用户需要正式或文化问候时使用。
---

# 问候语专家技能

## 能力
- 正式商务问候
- 文化敏感性考虑
- 多语言问候
- 情境适当的称呼

## 指南
1. 询问情境(商务、休闲、文化背景)
2. 提供 2-3 个选项
3. 解释文化细微差别
4. 如果是非中文则包含发音
```

### 复杂示例

查看 [.skill/code-reviewer/SKILL.md](.skill/code-reviewer/SKILL.md) 获取包含以下内容的综合示例:
- 安全检查清单
- 多维度审查框架
- 特定语言指南
- 示例输出

## 🔧 配置

### 默认配置

默认从当前工作目录的 `.skill/` 加载技能。

### 自定义技能目录

```bash
mcp-server-skill --skills-dir /path/to/your/skills
```

在 MCP 配置中:
```json
{
  "command": "uvx",
  "args": ["mcp-server-skill", "--skills-dir", "/custom/path"]
}
```

### 多个技能源

为不同技能集运行多个实例:

```json
{
  "mcpServers": {
    "skill-work": {
      "command": "uvx",
      "args": ["mcp-server-skill", "--skills-dir", "~/work-skills"]
    },
    "skill-personal": {
      "command": "uvx",
      "args": ["mcp-server-skill", "--skills-dir", "~/personal-skills"]
    }
  }
}
```

## 🧪 测试

### 手动测试

1. **启动服务器**:
   ```bash
   mcp-server-skill
   ```

2. **创建测试技能** 在 `.skill/test/SKILL.md`

3. **测试发现**: 服务器应记录 "Loaded X skills"

4. **测试热重载**: 修改 SKILL.md 并查看重载消息

### 集成测试

使用提供的示例:

```bash
# 创建示例技能
mkdir -p .skill
cp -r examples/calculator .skill/
cp -r examples/code-reviewer .skill/

# 使用你的 Agent 测试
# 询问: "你有哪些技能?"
# 尝试: "使用 calculator 技能计算 123 * 456"
```

## 🎯 使用场景

### 软件开发
- **code-reviewer**: 全面的代码审查,注重安全性
- **test-generator**: 生成单元测试
- **documentation-writer**: 技术文档最佳实践
- **refactoring-guide**: 代码改进策略

### 内容创作
- **technical-writer**: 技术写作指南
- **blog-optimizer**: SEO 和可读性改进
- **social-media**: 平台特定的内容优化

### 数据与分析
- **data-analyst**: 统计分析工作流
- **visualization-expert**: 数据可视化最佳实践
- **sql-optimizer**: 查询优化技术

### 领域特定
- **legal-reviewer**: 法律文档审查清单
- **medical-coder**: 医疗编码辅助
- **financial-analyst**: 财务分析框架

## 🤝 贡献

我们欢迎贡献!

### 添加你的技能

1. 按照格式创建技能
2. 本地测试
3. 在 `examples/` 中提交包含你的技能的 PR

### 改进服务器

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 添加测试
5. 提交 PR

### 技能分享

与社区分享你的技能:
- 使用标签 `#open-claudeskill`
- 包含用例和示例
- 记录任何特殊要求

## 📚 文档

- **[MCP_CONFIG.md](MCP_CONFIG.md)**: 所有平台的详细配置
- **[AGENT_PROMPT.md](AGENT_PROMPT.md)**: Agent 的系统提示词模板
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: 技术架构文档
- **[QUICKSTART.md](QUICKSTART.md)**: 5分钟快速开始指南
- **[Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)**: 官方技能格式规范

## 🔍 故障排除

### 技能未加载

```bash
# 检查目录
ls .skill/

# 检查格式
cat .skill/your-skill/SKILL.md

# 测试服务器
mcp-server-skill --skills-dir .skill
```

### 工具未出现在 Agent 中

1. 重启你的 MCP 客户端
2. 检查 `mcp_settings.json` 语法
3. 验证 `disabled: false`
4. 查看服务器日志

### 热重载不工作

- 验证文件权限
- 检查服务器是否监控正确的目录
- 如需要则重启 MCP 服务器

## 🛣️ 路线图

- [ ] 技能模板生成器
- [ ] 技能验证工具
- [ ] 技能市场/注册表
- [ ] 技能版本管理
- [ ] 技能依赖关系
- [ ] 远程技能仓库
- [ ] 技能分析(使用跟踪)
- [ ] 技能管理 Web UI

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 灵感来自 [Claude Code 的技能系统](https://claude.ai/code)
- 基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- 使用 [Agent Skills Spec](https://github.com/anthropics/skills)

## 🔗 链接

- **文档**: [完整文档](docs/)
- **示例**: [技能示例](examples/)
- **MCP 协议**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **官方技能**: [anthropics/skills](https://github.com/anthropics/skills)

## 💬 社区

- **问题**: [GitHub Issues](https://github.com/your-org/open-claudeskill/issues)
- **讨论**: [GitHub Discussions](https://github.com/your-org/open-claudeskill/discussions)

---

**由 Open-ClaudeSkill 社区 ❤️ 制作**

如果你觉得有用,请给仓库 ⭐ 星标并分享给其他人!
