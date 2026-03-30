@echo off
REM Flash-IDPS Docker Setup Script for Windows
REM Automates the setup and running of the Flash-IDPS Jupyter notebook environment

setlocal enabledelayedexpansion

REM Colors (Windows 10+)
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
  set "COLOR_BLUE=%%b[34m"
  set "COLOR_GREEN=%%b[32m"
  set "COLOR_YELLOW=%%b[33m"
  set "COLOR_RED=%%b[31m"
  set "COLOR_RESET=%%b[0m"
)

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

:menu
echo %COLOR_BLUE%========================================%COLOR_RESET%
echo %COLOR_BLUE%   Flash-IDPS Docker Setup (Windows)%COLOR_RESET%
echo %COLOR_BLUE%========================================%COLOR_RESET%
echo.
echo 1. Full Setup (Build and Start)
echo 2. Build Docker Image (CPU)
echo 3. Build Docker Image (GPU)
echo 4. Start Container
echo 5. Stop Container
echo 6. Restart Container
echo 7. Show Status
echo 8. Clean Up (Remove Images)
echo 9. Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto build_cpu
if "%choice%"=="3" goto build_gpu
if "%choice%"=="4" goto start
if "%choice%"=="5" goto stop
if "%choice%"=="6" goto restart
if "%choice%"=="7" goto status
if "%choice%"=="8" goto clean
if "%choice%"=="9" goto end
goto menu

:setup
echo.
echo %COLOR_BLUE%Checking prerequisites...%COLOR_RESET%
docker --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_RED%Error: Docker is not installed. Please install Docker Desktop first.%COLOR_RESET%
    pause
    goto menu
)
echo %COLOR_GREEN%✓ Docker is installed%COLOR_RESET%

echo.
echo %COLOR_BLUE%Creating directories...%COLOR_RESET%
if not exist "data" mkdir data
if not exist "models" mkdir models
if not exist "output" mkdir output
if not exist "notebooks" mkdir notebooks
echo %COLOR_GREEN%✓ Directories created%COLOR_RESET%

echo.
echo %COLOR_BLUE%Building Docker image...%COLOR_RESET%
docker build -t flash-idps:latest --target final .
if errorlevel 1 (
    echo %COLOR_RED%Error: Docker build failed%COLOR_RESET%
    pause
    goto menu
)
echo %COLOR_GREEN%✓ Docker image built%COLOR_RESET%

echo.
echo %COLOR_BLUE%Starting container...%COLOR_RESET%
docker run -d ^
    --name flash-idps-notebook ^
    -p 8888:8888 ^
    -v "%SCRIPT_DIR%":/app ^
    -v "%SCRIPT_DIR%data":/app/data ^
    -v "%SCRIPT_DIR%models":/app/models ^
    -v "%SCRIPT_DIR%output":/app/output ^
    flash-idps:latest

echo.
echo %COLOR_GREEN%========================================%COLOR_RESET%
echo %COLOR_GREEN%   Setup Complete!%COLOR_RESET%
echo %COLOR_GREEN%========================================%COLOR_RESET%
echo.
echo Access the notebook at: %COLOR_BLUE%http://localhost:8888%COLOR_RESET%
echo.
echo To stop: %COLOR_YELLOW%Option 5%COLOR_RESET%
echo To view logs: %COLOR_YELLOW%docker logs -f flash-idps-notebook%COLOR_RESET%
echo.
pause
goto menu

:build_cpu
echo.
echo %COLOR_BLUE%Building CPU-only Docker image...%COLOR_RESET%
docker build -t flash-idps:latest --target final .
if errorlevel 1 (
    echo %COLOR_RED%Error: Docker build failed%COLOR_RESET%
) else (
    echo %COLOR_GREEN%✓ Docker image built successfully%COLOR_RESET%
)
pause
goto menu

:build_gpu
echo.
echo %COLOR_BLUE%Building GPU-enabled Docker image...%COLOR_RESET%
echo %COLOR_YELLOW%Note: GPU build requires NVIDIA Docker runtime%COLOR_RESET%
docker build -f Dockerfile.gpu -t flash-idps:gpu --target final .
if errorlevel 1 (
    echo %COLOR_RED%Error: Docker build failed%COLOR_RESET%
    echo %COLOR_YELLOW%Ensure you have NVIDIA Docker runtime installed%COLOR_RESET%
) else (
    echo %COLOR_GREEN%✓ GPU Docker image built successfully%COLOR_RESET%
)
pause
goto menu

:start
echo.
echo %COLOR_BLUE%Starting container...%COLOR_RESET%
docker start flash-idps-notebook 2>nul
if errorlevel 1 (
    docker run -d ^
        --name flash-idps-notebook ^
        -p 8888:8888 ^
        -v "%SCRIPT_DIR%":/app ^
        -v "%SCRIPT_DIR%data":/app/data ^
        -v "%SCRIPT_DIR%models":/app/models ^
        -v "%SCRIPT_DIR%output":/app/output ^
        flash-idps:latest
)
echo.
echo %COLOR_GREEN%Container started%COLOR_RESET%
echo Access: %COLOR_BLUE%http://localhost:8888%COLOR_RESET%
pause
goto menu

:stop
echo.
echo %COLOR_BLUE%Stopping container...%COLOR_RESET%
docker stop flash-idps-notebook 2>nul
docker rm flash-idps-notebook 2>nul
docker compose down 2>nul
echo %COLOR_GREEN%Container stopped%COLOR_RESET%
pause
goto menu

:restart
echo.
echo %COLOR_BLUE%Restarting container...%COLOR_RESET%
call :stop
timeout /t 2 /nobreak >nul
call :start
goto menu

:status
echo.
echo %COLOR_BLUE%Container Status:%COLOR_RESET%
docker ps --filter "name=flash-idps" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.
echo %COLOR_BLUE%Docker Images:%COLOR_RESET%
docker images flash-idps --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
echo.
pause
goto menu

:clean
echo.
echo %COLOR_BLUE%Cleaning up Docker images...%COLOR_RESET%
docker rmi flash-idps:latest 2>nul
docker rmi flash-idps:gpu 2>nul
echo %COLOR_GREEN%Images removed%COLOR_RESET%
pause
goto menu

:end
echo.
echo %COLOR_GREEN%Goodbye!%COLOR_RESET%
exit /b 0
