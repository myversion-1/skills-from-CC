@echo off
chcp 65001 >nul
cd /d D:\Personal\skills
python sync_skills.py --check-only
if %errorlevel% neq 0 (
    echo.
    echo [!] 发现新版本，正在同步...
    python sync_skills.py
) else (
    echo.
    echo [OK] Skills 已是最新
)
pause