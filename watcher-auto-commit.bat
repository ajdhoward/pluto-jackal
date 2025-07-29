@echo off
title Pluto-Jackal Auto Commit Watcher
echo ===========================================
echo  🚀 Pluto-Jackal Auto Commit Watcher Started
echo ===========================================
echo Watching for new or changed files in: C:\ajdhoward\pluto-jackal
echo Press CTRL+C to stop.
echo.

:loop
cd /d C:\ajdhoward\pluto-jackal

for /f "tokens=*" %%A in ('git status --porcelain') do (
    git add .
    git commit -m "Auto-commit from watcher: %%A"
    git push origin main
    powershell -command "New-BurntToastNotification -Text 'Pluto-Jackal Synced', 'Committed: %%A'"
)

timeout /t 30 >nul
goto loop
