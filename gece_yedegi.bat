@echo off
chcp 65001 > nul
REM ===========================================================================
REM  gece_yedegi.bat - Otomatik GitHub yedegi
REM
REM  Bu dosyayi elle calistirmaniz gerekmez. Windows Gorev Zamanlayicisi
REM  her aksam saat 18:00'de kendiliginden calistirir.
REM
REM  Ne yapar:
REM    - Degisiklik varsa hepsini kaydeder ve GitHub'a gonderir
REM    - Degisiklik yoksa hicbir sey yapmaz
REM    - Ne yaptigini gunluk dosyasina yazar
REM
REM  Gunluk dosyasi: ciktilar\yedek_gunlugu.txt
REM ===========================================================================

cd /d "%~dp0"

set GUNLUK=ciktilar\yedek_gunlugu.txt
if not exist ciktilar mkdir ciktilar

echo. >> "%GUNLUK%"
echo ---------------------------------------------------------------- >> "%GUNLUK%"
echo %DATE% %TIME% >> "%GUNLUK%"

REM Git deposu mu, kontrol et
git rev-parse --is-inside-work-tree > nul 2>&1
if errorlevel 1 (
    echo HATA: Bu klasor bir git deposu degil. >> "%GUNLUK%"
    exit /b 1
)

REM Degisiklik var mi
git status --porcelain > "%TEMP%\yedek_durum.txt"
for %%A in ("%TEMP%\yedek_durum.txt") do set BOYUT=%%~zA
del "%TEMP%\yedek_durum.txt" > nul 2>&1

if "%BOYUT%"=="0" (
    echo Degisiklik yok, yedek gerekmedi. >> "%GUNLUK%"
    exit /b 0
)

echo Degisiklikler bulundu, gonderiliyor... >> "%GUNLUK%"
git status --short >> "%GUNLUK%" 2>&1

git add -A >> "%GUNLUK%" 2>&1
if errorlevel 1 (
    echo HATA: git add basarisiz. >> "%GUNLUK%"
    exit /b 1
)

git commit -m "Otomatik gece yedegi" >> "%GUNLUK%" 2>&1
if errorlevel 1 (
    echo HATA: git commit basarisiz. >> "%GUNLUK%"
    exit /b 1
)

git push >> "%GUNLUK%" 2>&1
if errorlevel 1 (
    echo HATA: git push basarisiz. Kimlik dogrulamasi gerekebilir. >> "%GUNLUK%"
    echo Menuden 5 numarayi secip elle gonderin. >> "%GUNLUK%"
    exit /b 1
)

echo Yedek basariyla gonderildi. >> "%GUNLUK%"
exit /b 0
