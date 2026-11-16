@echo off
title Installer Image Converter Pro - Windows
color 0B

echo ========================================================
echo      INSTALLER IMAGE CONVERTER PRO (KHUSUS WINDOWS)
echo ========================================================
echo.

:: Pindah ke direktori tempat file setup.bat ini berada
cd /d "%~dp0"

:: Cek apakah Python sudah terinstal
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python tidak ditemukan di komputer ini!
    echo Silakan unduh dan instal Python dari https://www.python.org/downloads/
    echo PENTING: Centang opsi "Add Python to PATH" saat proses instalasi.
    echo.
    pause
    exit /b
)

echo [1/3] Memperbarui pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Mengunduh dan menginstal library (Pillow, customtkinter, tkinterdnd2)...
python -m pip install Pillow customtkinter tkinterdnd2

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERROR] Gagal menginstal library. Periksa koneksi internet Anda.
    pause
    exit /b
)

echo.
echo [3/3] Membuat pintasan (Shortcut) di Desktop...

set "SCRIPT_PATH=%~dp0app_konverter-v2.py"
set "DESKTOP_PATH=%USERPROFILE%\Desktop\Image Converter Pro.lnk"

:: Cari lokasi pythonw.exe agar aplikasi berjalan tanpa jendela hitam CMD
for /f "delims=" %%i in ('where pythonw.exe 2^>nul') do (
    set "PYTHONW_PATH=%%i"
    goto :create_shortcut
)
set "PYTHONW_PATH=pythonw.exe"

:create_shortcut
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws = New-Object -ComObject WScript.Shell; ^
    $s = $ws.CreateShortcut('%DESKTOP_PATH%'); ^
    $s.TargetPath = '%PYTHONW_PATH%'; ^
    $s.Arguments = '"%SCRIPT_PATH%"'; ^
    $s.WorkingDirectory = '%~dp0'; ^
    $s.Description = 'Image Converter Pro - Pengonversi Ukuran dan Format Gambar'; ^
    $s.Save()"

echo.
echo ========================================================
echo    INSTALASI SELESAI!
echo    Pintasan "Image Converter Pro" telah dibuat di Desktop.
echo ========================================================
echo.
pause
