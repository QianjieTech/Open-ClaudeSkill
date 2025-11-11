@echo off
REM MCP Skill Server 启动脚本
REM 本地开发测试使用

echo ========================================
echo MCP Skill Server - Local Testing
echo ========================================
echo.

REM 切换到项目目录
cd /d "%~dp0"

echo [1/3] 检查 Python...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python
    echo 请确保 Python 已安装并添加到 PATH
    pause
    exit /b 1
)
echo.

echo [2/3] 检查依赖...
python -c "import mcp, yaml, watchdog" 2>nul
if errorlevel 1 (
    echo 警告: 依赖未安装
    echo 正在安装依赖...
    pip install -e .
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)
echo.

echo [3/3] 启动 MCP Skill Server...
echo 技能目录: %~dp0.skill
echo.
echo 提示: 按 Ctrl+C 停止服务器
echo ========================================
echo.

REM 启动服务器
python -m mcp_server_skill.server --skills-dir "%~dp0.skill"

pause
