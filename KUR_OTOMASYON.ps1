# =============================================================================
#  KUR_OTOMASYON.ps1
#
#  Bu betiği bir kez çalıştırırsınız, iki şey kurar:
#
#    1. Masaüstünüze "Jeobilim Arastirma" kısayolu koyar.
#       Çift tıklayınca menü açılır, komut ezberlemeniz gerekmez.
#
#    2. Her akşam 18:00'de çalışan otomatik yedekleme görevi oluşturur.
#       Değişiklikleriniz kendiliğinden GitHub'a gönderilir.
#
#  ÇALIŞTIRMA (tek satır, hangi klasörde olduğunuz fark etmez):
#      powershell -ExecutionPolicy Bypass -File "$HOME\Documents\jeobilim-arastirma-iskeleti\KUR_OTOMASYON.ps1"
#
#  KALDIRMA:
#      powershell -ExecutionPolicy Bypass -File "$HOME\Documents\jeobilim-arastirma-iskeleti\KUR_OTOMASYON.ps1" -Kaldir
# =============================================================================

param([switch]$Kaldir)

# Katı hata modu bilerek kullanılmıyor. Windows'un yerleşik komutları
# beklenen durumlarda da hata kanalına yazabiliyor; her adımı tek tek
# kontrol etmek daha güvenilir.

$ProjeKlasoru = Split-Path -Parent $MyInvocation.MyCommand.Path
$MasaustuYolu = [Environment]::GetFolderPath("Desktop")
$KisayolYolu  = Join-Path $MasaustuYolu "Jeobilim Arastirma.lnk"
$GorevAdi     = "Jeobilim Arastirma - Gece Yedegi"
$YedekBetigi  = Join-Path $ProjeKlasoru "gece_yedegi.bat"
$MenuBetigi   = Join-Path $ProjeKlasoru "BASLAT.bat"

function Baslik($metin) {
    Write-Host ""
    Write-Host "================================================================"
    Write-Host "  $metin"
    Write-Host "================================================================"
    Write-Host ""
}

function Gorev-Var {
    $g = Get-ScheduledTask -TaskName $GorevAdi -ErrorAction SilentlyContinue
    return ($null -ne $g)
}

# -----------------------------------------------------------------------------
# Kaldirma
# -----------------------------------------------------------------------------
if ($Kaldir) {
    Baslik "OTOMASYON KALDIRILIYOR"

    if (Test-Path $KisayolYolu) {
        Remove-Item $KisayolYolu -Force
        Write-Host "  Masaustu kisayolu silindi."
    } else {
        Write-Host "  Masaustu kisayolu zaten yoktu."
    }

    if (Gorev-Var) {
        Unregister-ScheduledTask -TaskName $GorevAdi -Confirm:$false
        Write-Host "  Zamanlanmis gorev silindi."
    } else {
        Write-Host "  Zamanlanmis gorev zaten yoktu."
    }

    Write-Host ""
    Write-Host "Kaldirma tamamlandi. Proje dosyalariniza dokunulmadi."
    Write-Host ""
    exit 0
}

# -----------------------------------------------------------------------------
# On kontrol
# -----------------------------------------------------------------------------
Baslik "OTOMASYON KURULUMU"

Write-Host "  Proje klasoru : $ProjeKlasoru"
Write-Host "  Masaustu      : $MasaustuYolu"
Write-Host ""

$eksik = @()
if (-not (Test-Path $MenuBetigi))  { $eksik += "BASLAT.bat" }
if (-not (Test-Path $YedekBetigi)) { $eksik += "gece_yedegi.bat" }

if ($eksik.Count -gt 0) {
    Write-Host "HATA: Su dosyalar bulunamadi: $($eksik -join ', ')" -ForegroundColor Red
    Write-Host "Betigin proje klasorunun icinde durdugundan emin olun."
    exit 1
}

# -----------------------------------------------------------------------------
# 1. Masaustu kisayolu
# -----------------------------------------------------------------------------
Write-Host "1. Masaustu kisayolu olusturuluyor..."

try {
    $kabuk = New-Object -ComObject WScript.Shell
    $kisayol = $kabuk.CreateShortcut($KisayolYolu)
    $kisayol.TargetPath       = $MenuBetigi
    $kisayol.WorkingDirectory = $ProjeKlasoru
    $kisayol.Description      = "Jeobilim arastirma iskeleti menusu"
    $kisayol.IconLocation     = "shell32.dll,21"
    $kisayol.Save()
    Write-Host "   TAMAM: $KisayolYolu" -ForegroundColor Green
} catch {
    Write-Host "   HATA: Kisayol olusturulamadi. $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# -----------------------------------------------------------------------------
# 2. Zamanlanmis gorev
# -----------------------------------------------------------------------------
Write-Host "2. Her aksam 18:00 icin otomatik yedek gorevi olusturuluyor..."

try {
    if (Gorev-Var) {
        Unregister-ScheduledTask -TaskName $GorevAdi -Confirm:$false
        Write-Host "   Eski gorev kaldirildi."
    }

    $eylem = New-ScheduledTaskAction `
        -Execute $YedekBetigi `
        -WorkingDirectory $ProjeKlasoru

    $tetikleyici = New-ScheduledTaskTrigger -Daily -At "18:00"

    # StartWhenAvailable: bilgisayar o saatte kapaliysa acilinca calisir
    $ayarlar = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

    Register-ScheduledTask `
        -TaskName $GorevAdi `
        -Action $eylem `
        -Trigger $tetikleyici `
        -Settings $ayarlar `
        -Description "Jeobilim arastirma iskeleti: her aksam degisiklikleri GitHub'a gonderir." `
        -Force | Out-Null

    if (Gorev-Var) {
        Write-Host "   TAMAM: Gorev olusturuldu." -ForegroundColor Green
        $bilgi = Get-ScheduledTaskInfo -TaskName $GorevAdi
        Write-Host "   Sonraki calisma: $($bilgi.NextRunTime)"
    } else {
        Write-Host "   HATA: Gorev dogrulanamadi." -ForegroundColor Red
    }

} catch {
    Write-Host "   HATA: Gorev olusturulamadi." -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)"
    Write-Host ""
    Write-Host "   Otomatik yedek olmasa da menu calisir."
    Write-Host "   Gonderme islemini menuden 5 numarayla yapabilirsiniz."
}

# -----------------------------------------------------------------------------
# Ozet
# -----------------------------------------------------------------------------
Baslik "KURULUM TAMAMLANDI"

Write-Host "  Masaustunuzde 'Jeobilim Arastirma' kisayolu var."
Write-Host "  Cift tiklayin, menu acilir. Baska komut gerekmez."
Write-Host ""
Write-Host "  Her aksam 18:00'de degisiklikleriniz GitHub'a gonderilir."
Write-Host "  Bilgisayar o saatte kapaliysa acildiginda calisir."
Write-Host ""
Write-Host "  Yedekleme gunlugu: ciktilar\yedek_gunlugu.txt"
Write-Host ""
Write-Host "  Otomatik yedegi hemen denemek icin:"
Write-Host "      Start-ScheduledTask -TaskName `"$GorevAdi`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Otomasyonu kaldirmak icin bu betigi -Kaldir ekiyle calistirin."
Write-Host ""
