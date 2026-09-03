@echo off
setlocal
cd /d "%~dp0"
title Eco Pack Analytics

if not exist ".venv\Scripts\python.exe" (
    echo [Eco Pack] Создание виртуального окружения...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Не удалось создать виртуальное окружение.
        pause
        exit /b 1
    )
)

if not exist ".venv\.dependencies_installed" (
    echo [Eco Pack] Установка зависимостей...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Не удалось установить зависимости.
        pause
        exit /b 1
    )
    type nul > ".venv\.dependencies_installed"
)

echo [Eco Pack] Запуск FastAPI: http://localhost:8000
start "Eco Pack API" /D "%~dp0" cmd /k .venv\Scripts\python.exe -m uvicorn api:app --reload --port 8000

echo [Eco Pack] Запуск Streamlit: http://localhost:8501
.venv\Scripts\python.exe -m streamlit run app.py

endlocal
