@echo off
chcp 65001 >nul
title Bore Connect - 启动

cd /d "%~dp0"

echo ========================================
echo   Bore Connect 启动中...
echo ========================================

:: 检查 MySQL
echo [1/3] 检查 MySQL...
sc query MySQL80 | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo   [WARN] MySQL 未运行，尝试启动...
    net start MySQL80 >nul 2>&1
    if errorlevel 1 (
        echo   [WARN] 无法启动 MySQL，请手动启动
    ) else (
        echo   [OK] MySQL 已启动
    )
) else (
    echo   [OK] MySQL 已运行
)

:: 启动 FastAPI 后端
echo [2/3] 启动 FastAPI 后端...
start "Bore-Connect-Backend" cmd /c "cd /d %~dp0 && .venv\Scripts\python -m app.main"
echo   [OK] 后端已启动 (http://127.0.0.1:8000)

:: 等后端就绪
echo   等待后端就绪...
timeout /t 5 /nobreak >nul

:: 启动 Nginx
echo [3/3] 启动 Nginx...
start "Bore-Connect-Nginx" cmd /c "cd /d %~dp0nginx-portable\nginx-1.26.3 && .\nginx.exe -c %~dp0nginx.conf -p %~dp0nginx-portable\nginx-1.26.3\"
echo   [OK] Nginx 已启动 (http://127.0.0.1:9090)

echo.
echo ========================================
echo   Bore Connect 启动完成!
echo   前端访问: http://127.0.0.1:9090
echo   后端直连: http://127.0.0.1:8000
echo ========================================
echo.
echo 按任意键关闭本窗口 (不影响服务)
pause >nul
