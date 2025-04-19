@echo off
setlocal
if not exist logs mkdir logs
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set timestamp=%%a
set logfile=logs\slicer_log_%timestamp%.txt
echo Running slicer... > %logfile%
call python slice_all_stl.py >> "%logfile%" 2>&1
echo Done. Output logged to %logfile%
pause
