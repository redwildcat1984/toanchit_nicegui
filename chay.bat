@echo off
setlocal

cls
title Python Virtual Environment Launcher

:: Tên thư mục môi trường ảo
set "VENV_DIR=.venv"

:SETUP_VENV
:: 2. Khởi tạo môi trường ảo nếu chưa tồn tại
if not exist "%VENV_DIR%" (
    echo [+] Ban chua tao moi truong ao, day la file chay nhanh, ban hay tao app va moi truong ao bang file tao_app.bat...
)

:: 3. Kích hoạt môi trường ảo
echo [+] Dang kich hoat moi truong ao...
call %VENV_DIR%\Scripts\activate

py app.py

:: Khi tắt app, thoát khỏi venv
call deactivate
pause
