@echo off
setlocal

REM ===========================================================================
REM  calistir.bat - Butun analizleri sirayla calistirir
REM
REM  Bu dosya, Linux ve macOS'taki "make tumu" komutunun Windows karsiligidir.
REM  Windows'ta make araci bulunmadigi icin ayni isi bu betik yapar.
REM
REM  KULLANIM
REM    Proje klasorunde PowerShell veya komut isteminde:
REM        .\calistir.bat            Butun analizleri calistirir
REM        .\calistir.bat temiz      Uretilen butun ciktilari siler
REM
REM    Ya da dosyaya cift tiklayabilirsiniz.
REM ===========================================================================

set PYTHON=.venv\Scripts\python.exe

if not exist "%PYTHON%" (
    echo.
    echo HATA: Sanal ortam bulunamadi.
    echo.
    echo Once su iki komutu sirayla calistirin:
    echo     py -3.12 -m venv .venv
    echo     .venv\Scripts\python.exe -m pip install -r gereksinimler.txt
    echo.
    goto bitir
)

if /i "%1"=="temiz" goto temizle

echo.
echo ================================================================
echo   00 - Ornek veri uretimi
echo ================================================================
"%PYTHON%" analizler\00_ornek_veri_uret.py || goto hata

echo.
echo ================================================================
echo   01 - Vektor saha verisi
echo ================================================================
"%PYTHON%" analizler\01_vektor_saha_verisi.py || goto hata

echo.
echo ================================================================
echo   02 - Raster ve uydu goruntusu
echo ================================================================
"%PYTHON%" analizler\02_raster_uydu_goruntusu.py || goto hata

echo.
echo ================================================================
echo   03 - Sismoloji zaman serisi
echo ================================================================
"%PYTHON%" analizler\03_sismoloji_zaman_serisi.py || goto hata

echo.
echo ================================================================
echo   Butun analizler tamamlandi.
echo     Sekiller : sekiller\
echo     Tablolar : ciktilar\
echo ================================================================
goto bitir

:temizle
echo.
echo Uretilen ciktilar siliniyor...
if exist sekiller\*.png del /q sekiller\*.png
if exist ciktilar\*.csv del /q ciktilar\*.csv
if exist ciktilar\*.txt del /q ciktilar\*.txt
if exist veri\ham\*.csv del /q veri\ham\*.csv
if exist veri\ham\*.tif del /q veri\ham\*.tif
if exist veri\islenmis\*.tif del /q veri\islenmis\*.tif
if exist veri\islenmis\*.gpkg del /q veri\islenmis\*.gpkg
if exist veri\islenmis\*.mseed del /q veri\islenmis\*.mseed
echo Silindi. calistir.bat ile hepsini yeniden uretebilirsiniz.
echo BENIOKU.md dosyalari korundu.
goto bitir

:hata
echo.
echo ================================================================
echo   HATA: Bir betik hata verdi.
echo   Yukaridaki mesaji okuyun, sorun genellikle orada yazili.
echo ================================================================

:bitir
echo.
pause
endlocal
