# Kilo Code 配置指南

**重要**: Kilo Code 只支持 `uvx` 命令，不支持本地 Python 路径。

## 🎯 两种使用方式

### 方式 1️⃣: 使用已发布的包 (推荐)

一旦包发布到 PyPI，配置非常简单：

#### 配置文件

编辑 `mcp_settings.json`:
```
c:\Users\bluezer\AppData\Roaming\Code\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json
```

#### 配置内容

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill"
      ],
      "alwaysAllow": [
        "load_skill"
      ],
      "disabled": false
    }
  }
}
```

#### 使用自定义技能目录

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill",
        "--skills-dir",
        "c:/your/custom/skill/directory"
      ],
      "alwaysAllow": [
        "load_skill"
      ],
      "disabled": false
    }
  }
}
```

#### 使用步骤

1. 等待包发布到 PyPI
2. 添加上述配置到 `mcp_settings.json`
3. 重启 Kilo Code
4. 询问: "有哪些可用的技能?"

---

### 方式 2️⃣: 本地开发测试 (限制较多)

**局限**: Kilo Code 不支持本地 Python 路径，所以需要：

#### 选项 A: 发布到 Test PyPI

```bash
# 1. 构建包
cd c:\userfolder\DevFolder\杂项\Open-ClaudeSkill_3
python -m build

# 2. 上传到 Test PyPI
python -m twine upload --repository testpypi dist/*

# 3. 配置 Kilo Code 使用 Test PyPI
```

配置:
```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "--index-url",
        "https://test.pypi.org/simple/",
        "mcp-server-skill"
      ],
      "alwaysAllow": [
        "load_skill"
      ],
      "disabled": false
    }
  }
}
```

#### 选项 B: 本地安装后使用 uvx

```bash
# 1. 本地构建
cd c:\userfolder\DevFolder\杂项\Open-ClaudeSkill_3
python -m build

# 2. 使用 uv 本地安装
uv tool install dist/mcp_server_skill-0.1.0-py3-none-any.whl

# 3. 验证
uvx mcp-server-skill --help
```

配置保持不变:
```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill"
      ],
      "alwaysAllow": [
        "load_skill"
      ],
      "disabled": false
    }
  }
}
```

---

## 📋 完整配置示例

### 基础配置 (使用默认 .skill/ 目录)

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "alwaysAllow": ["fetch"],
      "disabled": false
    },
    "skill": {
      "command": "uvx",
      "args": ["mcp-server-skill"],
      "alwaysAllow": ["load_skill"],
      "disabled": false
    }
  }
}
```

### 高级配置 (自定义技能目录)

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "alwaysAllow": ["fetch"],
      "disabled": false
    },
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill",
        "--skills-dir",
        "~/my-skills"
      ],
      "alwaysAllow": ["load_skill"],
      "disabled": false
    }
  }
}
```

---

## 🧪 测试

### 1. 检查 uvx 是否可用

```bash
uvx --version
```

如果没有安装 uv:
```bash
pip install uv
```

### 2. 测试包安装

```bash
# 测试能否通过 uvx 运行
uvx mcp-server-skill --help
```

### 3. 在 Kilo Code 中测试

1. 重启 Kilo Code
2. 询问: "你有哪些工具?"
3. 应该看到 `load_skill` 工具
4. 询问: "有哪些可用的技能?"

---

## 🐛 故障排除

### 问题 1: "uvx: command not found"

**解决**:
```bash
pip install uv
```

### 问题 2: "Package 'mcp-server-skill' not found"

**原因**: 包还未发布到 PyPI

**解决**:
1. 等待包发布，或
2. 使用 Test PyPI 测试，或
3. 本地构建并用 `uv tool install` 安装

### 问题 3: Kilo Code 不识别配置

**检查**:
- JSON 语法正确
- 路径使用正斜杠 `/`
- `disabled: false`
- 完全重启 Kilo Code

### 问题 4: 技能未加载

**检查**:
- 技能目录存在
- SKILL.md 格式正确
- 权限正确

---

## 📦 发布流程

### 准备发布到 PyPI

详见 [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md)

快速流程:

```bash
# 1. 构建
cd c:\userfolder\DevFolder\杂项\Open-ClaudeSkill_3
python -m build

# 2. 上传 (需要 PyPI 账号和 token)
python -m twine upload dist/*

# 3. 验证
uvx mcp-server-skill --help
```

发布后更新 Kilo Code 配置使用正式版本。

---

## 🎯 推荐工作流

### 开发阶段

```bash
# 本地测试 (不通过 Kilo Code)
python -m mcp_server_skill.server
```

### 集成测试

```bash
# 1. 构建本地包
python -m build

# 2. 用 uv 安装
uv tool install dist/mcp_server_skill-0.1.0-py3-none-any.whl --force

# 3. 测试
uvx mcp-server-skill --help

# 4. 在 Kilo Code 中测试 (使用 uvx 配置)
```

### 生产使用

```bash
# 1. 发布到 PyPI
python -m twine upload dist/*

# 2. Kilo Code 配置使用 uvx

# 3. 用户直接安装使用
```

---

## ✅ 配置清单

使用 Kilo Code 前确认:

- [ ] 已发布到 PyPI 或 Test PyPI
- [ ] 或使用 `uv tool install` 本地安装
- [ ] mcp_settings.json 配置正确
- [ ] 使用 `uvx` 命令 (不是 python)
- [ ] 技能目录存在且有 SKILL.md
- [ ] Kilo Code 已重启

---

## 📚 相关文档

- **发布指南**: [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md)
- **本地测试**: [LOCAL_TESTING.md](LOCAL_TESTING.md) (仅用于开发)
- **MCP 配置**: [MCP_CONFIG.md](MCP_CONFIG.md)
- **快速开始**: [QUICKSTART.md](QUICKSTART.md)

---

**Kilo Code + uvx 是最佳组合! 🚀**
