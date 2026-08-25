@echo off
setlocal
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 "%~dp0demo_gui.py"
) else (
  python "%~dp0demo_gui.py"
)
