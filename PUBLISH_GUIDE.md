# 发布到 PyPI 指南

由于 Kilo Code 只支持 uvx 命令，我们需要将包发布到 PyPI。

## 📋 发布前准备

### 1. 确保本地测试通过

```bash
cd c:\userfolder\DevFolder\杂项\Open-ClaudeSkill_3

# 运行测试
python test_installation.py

# 测试服务器
python -m mcp_server_skill.server
```

### 2. 检查包信息

确认 `pyproject.toml` 中的信息正确：
- 包名: `mcp-server-skill`
- 版本: `0.1.0`
- 依赖项已列出

### 3. 清理旧构建

```bash
# 清理
rm -rf build/ dist/ *.egg-info src/*.egg-info

# 或使用 Makefile
make clean
```

## 🔨 构建包

### 安装构建工具

```bash
pip install --upgrade build twine
```

### 构建分发包

```bash
# 在项目根目录
python -m build
```

这会创建：
- `dist/mcp_server_skill-0.1.0-py3-none-any.whl` (wheel 包)
- `dist/mcp_server_skill-0.1.0.tar.gz` (源码包)

### 检查包

```bash
# 检查包是否正确
twine check dist/*
```

## 🧪 测试包 (本地)

### 在新环境中测试

```bash
# 创建测试环境
python -m venv test_env
test_env\Scripts\activate

# 从 wheel 安装
pip install dist/mcp_server_skill-0.1.0-py3-none-any.whl

# 测试
mcp-server-skill --help
python -c "from mcp_server_skill import __version__; print(__version__)"

# 清理
deactivate
rm -rf test_env
```

## 📤 发布到 PyPI

### 选项 A: 发布到 Test PyPI (推荐先测试)

```bash
# 注册 Test PyPI 账号: https://test.pypi.org/account/register/

# 上传
python -m twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ mcp-server-skill

# 或使用 uvx 测试
uvx --index-url https://test.pypi.org/simple/ mcp-server-skill --help
```

### 选项 B: 发布到正式 PyPI

```bash
# 1. 注册 PyPI 账号: https://pypi.org/account/register/

# 2. 创建 API Token
#    访问: https://pypi.org/manage/account/token/
#    创建一个 token 用于上传

# 3. 配置认证 (可选)
#    创建 ~/.pypirc:
cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
username = __token__
password = pypi-your-test-token-here
EOF

# 4. 上传
python -m twine upload dist/*

# 或手动输入 token
# Username: __token__
# Password: pypi-xxxxx (你的 API token)
```

## ✅ 发布后验证

### 1. 检查 PyPI 页面

访问: https://pypi.org/project/mcp-server-skill/

确认：
- ✅ 包信息正确
- ✅ 版本号正确
- ✅ README 显示正常
- ✅ 依赖项列出

### 2. 测试安装

```bash
# 新环境测试
pip install mcp-server-skill

# 测试命令
mcp-server-skill --help

# 测试 uvx (Kilo Code 使用的方式)
uvx mcp-server-skill --help
```

### 3. 更新 Kilo Code 配置

发布成功后，Kilo Code 配置改回：

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

可选：指定技能目录

```json
{
  "mcpServers": {
    "skill": {
      "command": "uvx",
      "args": [
        "mcp-server-skill",
        "--skills-dir",
        "c:/path/to/your/.skill"
      ],
      "alwaysAllow": [
        "load_skill"
      ],
      "disabled": false
    }
  }
}
```

## 🔐 安全提醒

### API Token 安全

- ❌ 不要将 token 提交到 Git
- ✅ 使用环境变量存储 token
- ✅ 限制 token 的作用域
- ✅ 定期轮换 token

### 使用环境变量

```bash
# 设置环境变量
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here

# 上传 (自动使用环境变量)
python -m twine upload dist/*
```

## 📝 发布检查清单

发布前检查：

- [ ] 所有测试通过
- [ ] 版本号已更新
- [ ] CHANGELOG.md 已更新
- [ ] README.md 完整且准确
- [ ] LICENSE 文件存在
- [ ] 依赖项正确列出
- [ ] 构建成功 (`python -m build`)
- [ ] 包检查通过 (`twine check dist/*`)
- [ ] 本地测试通过
- [ ] Git 已提交所有更改
- [ ] 创建 Git tag

## 🏷️ 版本管理

### 创建版本标签

```bash
# 提交所有更改
git add .
git commit -m "Release v0.1.0"

# 创建标签
git tag -a v0.1.0 -m "Release version 0.1.0"

# 推送
git push origin main
git push origin v0.1.0
```

### 语义化版本

遵循 [SemVer](https://semver.org/)：

- `MAJOR.MINOR.PATCH`
- `0.1.0` → 第一个测试版本
- `0.1.1` → Bug 修复
- `0.2.0` → 新功能
- `1.0.0` → 稳定版本

## 🔄 更新包

发布新版本时：

```bash
# 1. 更新版本号
# 编辑 pyproject.toml 中的 version = "0.1.1"

# 2. 更新 CHANGELOG.md

# 3. 清理旧构建
make clean

# 4. 构建新版本
python -m build

# 5. 上传
python -m twine upload dist/*
```

## 🚀 自动化发布

### 使用 GitHub Actions

已配置自动发布工作流 (`.github/workflows/publish.yml`):

1. 创建 GitHub Release
2. 自动构建并发布到 PyPI

需要配置：
- GitHub Secret: `PYPI_API_TOKEN`

## 📞 需要帮助？

### 常见问题

**Q: 包名已被占用**
A: 修改 `pyproject.toml` 中的包名

**Q: 上传失败**
A: 检查 API token 和网络连接

**Q: uvx 找不到包**
A: 等待几分钟让 PyPI 索引更新

**Q: README 显示不正确**
A: 确保 README.md 是有效的 Markdown

### 相关资源

- [PyPI 官方文档](https://packaging.python.org/)
- [Twine 文档](https://twine.readthedocs.io/)
- [Python 打包指南](https://packaging.python.org/tutorials/packaging-projects/)

---

## 🎯 快速发布命令

```bash
# 完整发布流程 (一次性)
cd c:\userfolder\DevFolder\杂项\Open-ClaudeSkill_3

# 1. 清理和构建
make clean
python -m build

# 2. 检查
twine check dist/*

# 3. 测试 PyPI (可选)
python -m twine upload --repository testpypi dist/*

# 4. 正式发布
python -m twine upload dist/*

# 5. 验证
uvx mcp-server-skill --help
```

---

**准备好发布了吗？ 🚀**

1. 确保本地测试通过
2. 清理和构建: `python -m build`
3. 上传到 PyPI: `twine upload dist/*`
4. 更新 Kilo Code 配置使用 uvx
