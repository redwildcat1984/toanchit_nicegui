@echo off
setlocal

cls
title Python Virtual Environment Launcher

:: Tên thư mục môi trường ảo
set "VENV_DIR=.venv"

:: 1. Kiểm tra Python đã cài chưa
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python khong tim thay. Dang chuan bi tai xuong...
    goto :INSTALL_PYTHON
) else (
    echo [OK] Python da co san.
    goto :SETUP_VENV
)

:INSTALL_PYTHON
set "py_url=https://www.python.org/ftp/python/3.14.6/python-3.10.11-amd64.exe"
set "py_exe=%temp%\python_installer.exe"

echo [+] Dang tai Python 3.14 tu python.org...
powershell -Command "Invoke-WebRequest -Uri '%py_url%' -OutFile '%py_exe%'"

echo [+] Dang cai dat Python (vui long cho trong giay lat)...
start /wait %py_exe% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
set "PATH=%PATH%;%ProgramFiles%\Python314\;%ProgramFiles%\Python314s\Scripts\"

if %errorlevel% neq 0 (
    echo [!] Cai dat Python that bai.
    pause
    exit
)
echo [OK] Cai dat Python thanh cong.

:SETUP_VENV
:: 2. Khởi tạo môi trường ảo nếu chưa tồn tại
if not exist "%VENV_DIR%" (
    echo [+] Dang tao moi truong ao venv...
    python -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo [!] Khong the tao venv.
        pause
        exit
    )
    echo [OK] Da tao xong venv.
)

:: 3. Kích hoạt môi trường ảo
echo [+] Dang kich hoat moi truong ao...
call %VENV_DIR%\Scripts\activate

:: 4. Cài đặt thư viện bên trong venv
:: Sử dụng file requirements.txt nếu có, hoặc cài thủ công
echo [+] Dang kiem tra va cap nhat thu vien trong venv...
python -m pip install --upgrade pip
@REM pip install pandas streamlit docxtpl comtypes openpyxl python-calamine python-docx pypdf unidecode pywin32
pip install nicegui

:: 5. Chạy ứng dụng Streamlit
cls
echo [OK] Moi truong ao da san sang!
echo [+] Dang khoi chay ung dung...
py app.py

:: Khi tắt app, thoát khỏi venv
call deactivate
pause
