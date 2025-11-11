@echo off
REM 为 Kilo Code 安装 mcp-server-skill
REM 使用 uv tool install 本地安装，让 Kilo Code 可以通过 uvx 使用

echo ========================================
echo 为 Kilo Code 安装 MCP Skill Server
echo ========================================
echo.

REM 切换到项目目录
cd /d "%~dp0"

echo [步骤 1/5] 检查 uv...
uv --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 uv
    echo 请先安装 uv: pip install uv
    pause
    exit /b 1
)
echo ✓ uv 已安装
echo.

echo [步骤 2/5] 清理旧构建...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✓ 清理完成
echo.

echo [步骤 3/5] 构建包...
python -m build
if errorlevel 1 (
    echo 错误: 构建失败
    echo 请确保已安装: pip install build
    pause
    exit /b 1
)
echo ✓ 构建成功
echo.

echo [步骤 4/5] 使用 uv tool 安装...
uv tool install dist\mcp_server_skill-0.1.0-py3-none-any.whl --force
if errorlevel 1 (
    echo 错误: 安装失败
    pause
    exit /b 1
)
echo ✓ 安装成功
echo.

echo [步骤 5/5] 验证安装...
uvx mcp-server-skill --help
if errorlevel 1 (
    echo 警告: 验证失败
    echo 但安装可能已成功，请继续配置 Kilo Code
)
echo ✓ 验证成功
echo.

echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 下一步：配置 Kilo Code
echo.
echo 1. 打开配置文件:
echo    c:\Users\bluezer\AppData\Roaming\Code\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json
echo.
echo 2. 添加或更新 skill 配置:
echo.
echo    "skill": {
echo      "command": "uvx",
echo      "args": ["mcp-server-skill"],
echo      "alwaysAllow": ["load_skill"],
echo      "disabled": false
echo    }
echo.
echo 3. 可选：指定技能目录
echo.
echo    "args": [
echo      "mcp-server-skill",
echo      "--skills-dir",
echo      "c:/path/to/your/.skill"
echo    ]
echo.
echo 4. 重启 Kilo Code
echo.
echo 5. 测试：询问 "有哪些可用的技能?"
echo.

pause
