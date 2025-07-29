@echo off
echo ===========================================
echo  PLUTO-JACKAL Repo Repair and Re-Sync Tool
echo ===========================================
echo.

REM Step 1: Navigate to parent folder
cd /d C:\ajdhoward

REM Step 2: Kill any processes using repo (VSCode, Python, Node)
taskkill /F /IM code.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

REM Step 3: Remove existing repo
rmdir /s /q pluto-jackal

REM Step 4: Re-clone repo
git clone https://github.com/ajdhoward/pluto-jackal.git

REM Step 5: Checkout main branch
cd pluto-jackal
git checkout main

echo.
echo  ✅ Repo successfully repaired and synced!
pause
