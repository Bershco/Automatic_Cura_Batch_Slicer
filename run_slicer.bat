@echo off
setlocal

set /p input_folder=Enter input STL folder path: 
set /p output_folder=Enter output folder path: 

if not exist logs mkdir logs

:: Generate timestamped log name automatically
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set timestamp=%%a
set logfile=logs\slicer_log_%timestamp%.txt

python slice_all_stl.py -i "%input_folder%" -o "%output_folder%" --log "%logfile%"

pause
