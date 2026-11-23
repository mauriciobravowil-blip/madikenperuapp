@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=C:\Users\minios\Python313\python.exe
if not exist "%PY%" set PY=python
echo Iniciando MADIKEN PERU...
start "" http://127.0.0.1:8000
"%PY%" run.py
pause
