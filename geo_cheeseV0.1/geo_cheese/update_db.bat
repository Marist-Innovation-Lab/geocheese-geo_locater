@echo off
cls
:update_db
python update_db.py
echo Initiating Database Update in:
timeout /t 86400 /nobreak
goto update_db