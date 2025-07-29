@echo off
REM === One-click script to run final-check.sh ===

REM Change directory to your project folder
cd /d C:\ajdhoward\pluto-jackal

REM Launch Git Bash and run the final-check.sh script
"C:\Program Files\Git\bin\bash.exe" --login -i -c "source venv/Scripts/activate && ./final-check.sh"

pause
