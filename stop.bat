@echo off
chcp 65001 >nul
title Bore Connect - 停止

echo ========================================
echo   Bore Connect 停止中...
echo ========================================

:: 停止 Nginx
echo [1/2] 停止 Nginx...
taskkill /f /im nginx.exe >nul 2>&1
echo   [OK] Nginx 已停止

:: 停止 FastAPI 后端
echo [2/2] 停止 FastAPI 后端...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING" 2^>nul') do taskkill /f /pid %%a >nul 2>&1
echo   [OK] 后端已停止

echo.
echo   Bore Connect 已停止
pause >nul
