@echo off
REM 本地开发环境快速设置脚本

echo ========================================
echo Open-ClaudeSkill 本地开发设置
echo ========================================
echo.

REM 切换到项目目录
cd /d "%~dp0"

echo [步骤 1/4] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python
    echo 请安装 Python 3.10 或更高版本
    pause
    exit /b 1
)
echo ✓ Python 已安装
echo.

echo [步骤 2/4] 安装依赖包...
pip install -e .
if errorlevel 1 (
    echo 错误: 安装失败
    pause
    exit /b 1
)
echo ✓ 依赖包已安装
echo.

echo [步骤 3/4] 运行安装测试...
python test_installation.py
if errorlevel 1 (
    echo 警告: 部分测试未通过
    echo 这可能是正常的,继续配置...
)
echo.

echo [步骤 4/4] 创建 Kilo Code 配置...
echo.
echo 请将以下配置添加到 Kilo Code 的 mcp_settings.json:
echo.
echo 文件位置:
echo c:\Users\bluezer\AppData\Roaming\Code\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json
echo.
echo ----------------------------------------
type mcp_settings.local.json
echo ----------------------------------------
echo.

echo ========================================
echo 设置完成!
echo ========================================
echo.
echo 下一步:
echo 1. 复制上面的配置到 Kilo Code 的 mcp_settings.json
echo 2. 重启 Kilo Code
echo 3. 测试: 询问 "有哪些可用的技能?"
echo.
echo 或者运行 run_skill_server.bat 来手动测试服务器
echo.

pause
