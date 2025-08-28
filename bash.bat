@echo off
setlocal enabledelayedexpansion

:: Folder
set "dir=%~1"
if "%dir%"=="" set "dir=%USERPROFILE%"

:: Extension
set "ext=%~2"
if "%ext%"=="" set "ext=.bat"

:: Log file path
set "logfile=%dir%\file_log.txt"

:: Get date and time
for /f "tokens=1-3 delims=/ " %%A in ('date /t') do set "date=%%C-%%A-%%B"
for /f "tokens=1-2 delims=: " %%A in ('time /t') do set "time=%%A:%%B"

:: Write date and time to log
echo %date% > "%logfile%"
echo %time% >> "%logfile%"

:: Collect files and write to log
for /r "%dir%" %%F in (*%ext%) do (
    echo %%~nxF >> "%logfile%"
    echo %%~fF >> "%logfile%"
)

:: Open log file in Notepad
start notepad "%logfile%"
pause

:: Close Notepad and delete log file
taskkill /f /im notepad.exe
if exist "%logfile%" del "%logfile%"

endlocal
exit /b
