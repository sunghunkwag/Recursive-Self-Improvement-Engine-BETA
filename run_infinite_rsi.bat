@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title RSI Infinite Loop Monitor (L2 Meta-Logic) - STATUS: CHECKING

cls
echo ==========================================================
echo       RSI SELF-IMPROVEMENT ENGINE LAUNCHER V4
echo ==========================================================
echo.

REM 1. File Check
echo [1/3] Checking for L2_UNIFIED_RSI.py...
if exist "L2_UNIFIED_RSI.py" (
    echo    - OK: File found.
) else (
    color 4f
    title [ERROR] FILE MISSING
    echo.
    echo    [CRITICAL ERROR] FILE MISSING!
    echo    --------------------------------------------------
    echo    Could not find 'L2_UNIFIED_RSI.py' in this folder.
    echo.
    echo    [POSSIBLE CAUSES]
    echo    1. You downloaded the file but Windows added '.txt' extension?
    echo       (Make sure it is NOT 'L2_UNIFIED_RSI.py.txt')
    echo    2. You are running this .bat file from a different folder?
    echo       (Both files must be in the SAME folder)
    echo    --------------------------------------------------
    echo.
    echo    PRESS ANY KEY TO EXIT... (Read above first!)
    pause
    exit /b
)
echo.

REM 2. Python Check & Run
echo [2/3] Searching for Python...
set "PY_CMD="
python --version >nul 2>&1 && set "PY_CMD=python"
if not defined PY_CMD ( py --version >nul 2>&1 && set "PY_CMD=py" )
if not defined PY_CMD ( python3 --version >nul 2>&1 && set "PY_CMD=python3" )

if defined PY_CMD (
    echo    - Found: %PY_CMD%
    echo.
    echo [3/3] Starting Infinite Loop...
    title RSI Infinite Loop - RUNNING
    
    "%PY_CMD%" L2_UNIFIED_RSI.py rsi-loop --generations 500 --rounds 100
    
    if errorlevel 1 (
        color 4f
        title [CRASH] PYTHON SCRIPT FAILED
        echo.
        echo    [EXECUTION FAILED]
        echo    The Python script crashed with an error.
        echo    See the error message above.
        echo.
        echo    PRESS ANY KEY TO EXIT...
        pause
        exit /b
    )
    goto :Success
)

REM 3. Python Failure
color 4f
title [ERROR] PYTHON NOT FOUND
echo.
echo    [CRITICAL ERROR] PYTHON NOT FOUND!
echo    --------------------------------------------------
echo    Detailed Check:
echo    'python' command: NOT FOUND
echo    'py' command:     NOT FOUND
echo    'python3' command: NOT FOUND
echo.
echo    Please install Python from python.org.
echo    (IMPORTANT: Check "Add Python to PATH" during install)
echo    --------------------------------------------------
echo.
echo    PRESS ANY KEY TO EXIT...
pause
exit /b

:Success
echo.
echo    [INFO] Process finished successfully.
pause
