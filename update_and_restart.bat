@echo off
REM ComfyUI Update and Restart Script for Windows
REM This script updates ComfyUI, custom nodes, and dependencies, then offers to restart

setlocal enabledelayedexpansion

echo ======================================
echo ComfyUI Update and Restart Utility
echo ======================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Run the Python update script
echo Running update script...
python update_comfyui.py

if %errorlevel% equ 0 (
    echo.
    echo ======================================
    echo Update completed successfully!
    echo ======================================
    echo.
    
    REM Check if ComfyUI is currently running
    tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *main.py*" 2>NUL | find /I /N "python.exe">NUL
    
    if "%errorlevel%"=="0" (
        echo ComfyUI appears to be running.
        echo.
        set /p RESTART="Would you like to restart ComfyUI now? (y/n): "
        
        if /i "!RESTART!"=="y" (
            echo Stopping ComfyUI...
            taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main.py*" 2>NUL
            timeout /t 2 /nobreak >NUL
            
            echo Starting ComfyUI...
            start "ComfyUI" python main.py
            
            echo.
            echo ComfyUI has been restarted!
            echo Check the new window to ensure it started correctly.
        ) else (
            echo Restart cancelled. Please restart ComfyUI manually when ready.
        )
    ) else (
        echo ComfyUI does not appear to be running.
        echo.
        set /p START="Would you like to start ComfyUI now? (y/n): "
        
        if /i "!START!"=="y" (
            echo Starting ComfyUI...
            start "ComfyUI" python main.py
            
            echo.
            echo ComfyUI has been started!
        ) else (
            echo You can start ComfyUI manually by running: python main.py
        )
    )
) else (
    echo.
    echo ======================================
    echo Update failed with errors!
    echo ======================================
    echo Please check the error messages above and resolve any issues.
    pause
    exit /b 1
)

echo.
echo Done!
pause
