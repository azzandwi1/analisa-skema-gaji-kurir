@echo off
title Push ke GitHub - Analisa Skema Gaji Kurir
echo ========================================================
echo   MELAKUKAN PUSH KE REPOSITORY GITHUB
echo   https://github.com/azzandwi1/analisa-skema-gaji-kurir
echo ========================================================
echo.

cd /d "%~dp0"
echo Lokasi folder saat ini: %CD%
echo.

echo Menjalankan git push...
"C:\Users\Dell E5300 i5\AppData\Local\Programs\Git\cmd\git.exe" push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   BERHASIL! Semua perubahan telah ter-push ke GitHub.
    echo ========================================================
) else (
    echo ========================================================
    echo   GAGAL atau Memerlukan Login Akun GitHub Anda.
    echo ========================================================
)
echo.
pause
