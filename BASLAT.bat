@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title Jeobilim Arastirma Iskeleti

REM ===========================================================================
REM  BASLAT.bat - Menu
REM
REM  Bu dosyaya cift tiklayin. Komut ezberlemeniz gerekmez, menuden secersiniz.
REM  Masaustundeki kisayol da bu dosyayi calistirir.
REM ===========================================================================

cd /d "%~dp0"

set PYTHON=.venv\Scripts\python.exe

:menu
cls
echo.
echo ================================================================
echo    JEOBILIM ARASTIRMA ISKELETI
echo    %CD%
echo ================================================================
echo.
echo    1  -  Analizleri calistir          (sekiller ve tablolar uretilir)
echo    2  -  Makaleyi Word olarak derle
echo    3  -  Ikisini birden yap           (once analiz, sonra makale)
echo.
echo    4  -  Neler degisti, goster
echo    5  -  Degisiklikleri GitHub'a gonder
echo    6  -  GitHub'daki guncellemeleri al
echo.
echo    7  -  Uretilen ciktilari sil       (hepsi yeniden uretilebilir)
echo    8  -  Kurulumu kontrol et
echo.
echo    0  -  Cikis
echo.
echo ================================================================
echo.
set /p secim=Numarayi yazip Enter'a basin:

if "%secim%"=="1" goto analiz
if "%secim%"=="2" goto makale
if "%secim%"=="3" goto hepsi
if "%secim%"=="4" goto durum
if "%secim%"=="5" goto gonder
if "%secim%"=="6" goto al
if "%secim%"=="7" goto temizle
if "%secim%"=="8" goto kontrol
if "%secim%"=="0" goto son
echo.
echo Boyle bir secenek yok. Tekrar deneyin.
timeout /t 2 > nul
goto menu

REM ---------------------------------------------------------------------------
:analiz
cls
echo.
echo === ANALIZLER CALISTIRILIYOR ===
echo.
if not exist "%PYTHON%" goto ortam_yok
"%PYTHON%" analizler\00_ornek_veri_uret.py || goto hata
echo.
"%PYTHON%" analizler\01_vektor_saha_verisi.py || goto hata
echo.
"%PYTHON%" analizler\02_raster_uydu_goruntusu.py || goto hata
echo.
"%PYTHON%" analizler\03_sismoloji_zaman_serisi.py || goto hata
echo.
echo ================================================================
echo   Analizler tamamlandi.
echo   Sekiller : sekiller klasorunde
echo   Tablolar : ciktilar klasorunde
echo ================================================================
if "%zincir%"=="1" goto makale_devam
goto bitti

REM ---------------------------------------------------------------------------
:makale
cls
echo.
echo === MAKALE DERLENIYOR ===
echo.
where quarto > nul 2>&1
if errorlevel 1 (
    echo HATA: Quarto bulunamadi.
    echo Kurulum icin: winget install --id Posit.Quarto -e
    goto bitti
)
quarto render makale\makale.qmd --to docx || goto hata
echo.
echo ================================================================
echo   Makale hazir: makale\makale.docx
echo ================================================================
echo.
set /p ac=Word dosyasini simdi acmak ister misiniz? (e/h):
if /i "%ac%"=="e" start "" "makale\makale.docx"
goto bitti

REM ---------------------------------------------------------------------------
:makale_devam
set zincir=
echo.
echo === SIMDI MAKALE DERLENIYOR ===
echo.
where quarto > nul 2>&1
if errorlevel 1 (
    echo Quarto kurulu degil, makale derleme atlandi.
    goto bitti
)
quarto render makale\makale.qmd --to docx || goto hata
echo.
echo ================================================================
echo   Analizler ve makale tamamlandi.
echo   Makale: makale\makale.docx
echo ================================================================
goto bitti

:hepsi
set zincir=1
goto analiz

REM ---------------------------------------------------------------------------
:durum
cls
echo.
echo === SON KAYITTAN BU YANA NELER DEGISTI ===
echo.
git status --short
echo.
echo Yukarida hicbir satir yoksa her sey kayitli demektir.
echo.
echo Isaretlerin anlami:
echo    M  = degistirilmis dosya
echo    ??  = yeni, henuz kaydedilmemis dosya
echo    D  = silinmis dosya
goto bitti

REM ---------------------------------------------------------------------------
:gonder
cls
echo.
echo === GITHUB'A GONDERILIYOR ===
echo.
git status --short
echo.
git diff --quiet && git diff --cached --quiet
if not errorlevel 1 (
    git ls-files --others --exclude-standard > "%TEMP%\yeni_dosyalar.txt"
    for %%A in ("%TEMP%\yeni_dosyalar.txt") do if %%~zA equ 0 (
        echo Gonderilecek bir degisiklik yok, her sey guncel.
        del "%TEMP%\yeni_dosyalar.txt" > nul 2>&1
        goto bitti
    )
    del "%TEMP%\yeni_dosyalar.txt" > nul 2>&1
)
echo.
set /p mesaj=Bu degisiklikleri bir cumleyle anlatin:
if "%mesaj%"=="" set mesaj=Guncelleme
git add -A || goto hata
git commit -m "%mesaj%" || goto hata
git push || goto hata
echo.
echo ================================================================
echo   Gonderildi.
echo ================================================================
goto bitti

REM ---------------------------------------------------------------------------
:al
cls
echo.
echo === GITHUB'DAN GUNCELLEMELER ALINIYOR ===
echo.
git pull || goto hata
echo.
echo Tamamlandi.
goto bitti

REM ---------------------------------------------------------------------------
:temizle
cls
echo.
echo === URETILEN CIKTILAR SILINECEK ===
echo.
echo Silinecekler: sekiller, tablolar, islenmis veri ve ornek ham veri.
echo Hepsi 1 numarali secenekle yeniden uretilebilir.
echo Kodunuz, belgeleriniz ve kaynakcaniz silinmez.
echo.
set /p onay=Emin misiniz? (e/h):
if /i not "%onay%"=="e" goto menu
if exist sekiller\*.png del /q sekiller\*.png
if exist ciktilar\*.csv del /q ciktilar\*.csv
if exist ciktilar\*.txt del /q ciktilar\*.txt
if exist veri\ham\*.csv del /q veri\ham\*.csv
if exist veri\ham\*.tif del /q veri\ham\*.tif
if exist veri\islenmis\*.tif del /q veri\islenmis\*.tif
if exist veri\islenmis\*.gpkg del /q veri\islenmis\*.gpkg
if exist veri\islenmis\*.mseed del /q veri\islenmis\*.mseed
echo.
echo Silindi. 1 numarali secenekle hepsini geri getirebilirsiniz.
goto bitti

REM ---------------------------------------------------------------------------
:kontrol
cls
echo.
echo === KURULUM KONTROLU ===
echo.
if exist "%PYTHON%" (
    echo [ TAMAM ] Python sanal ortami
    "%PYTHON%" -c "import geopandas, rasterio, obspy; print('[ TAMAM ] Mekansal ve sismoloji paketleri')" 2>nul || echo [ EKSIK ] Paketler kurulu degil
) else (
    echo [ EKSIK ] Python sanal ortami bulunamadi
)
where git > nul 2>&1 && echo [ TAMAM ] Git || echo [ EKSIK ] Git
where quarto > nul 2>&1 && echo [ TAMAM ] Quarto || echo [ EKSIK ] Quarto
if exist makale\zotero.bib (echo [ TAMAM ] Zotero kaynakca dosyasi) else (echo [ EKSIK ] makale\zotero.bib yok)
echo.
echo Eksik bir sey varsa belgeler\WINDOWS.md dosyasina bakin.
goto bitti

REM ---------------------------------------------------------------------------
:ortam_yok
echo.
echo HATA: Python sanal ortami bulunamadi.
echo.
echo Su iki komutu sirayla calistirin:
echo     py -3.12 -m venv .venv
echo     .venv\Scripts\python.exe -m pip install -r gereksinimler.txt
goto bitti

:hata
echo.
echo ================================================================
echo   HATA olustu. Yukaridaki mesaji okuyun.
echo ================================================================
goto bitti

:bitti
echo.
pause
goto menu

:son
endlocal
exit /b 0
