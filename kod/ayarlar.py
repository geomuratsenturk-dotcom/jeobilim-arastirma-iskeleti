"""
Proje genelinde kullanilan yollar, koordinat sistemleri ve sabitler.

Bu dosyanin amaci, hicbir betikte elle yazilmis dosya yolu bulunmamasidir.
Butun betikler yollari buradan cagirir. Boylece projeyi baska bir bilgisayara
tasidiginizda tek bir satir bile degistirmeniz gerekmez.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Yollar
# ---------------------------------------------------------------------------
# Bu dosya kod/ klasorunun icinde. Bir ust klasor proje kokudur.
PROJE_KOK = Path(__file__).resolve().parents[1]

VERI = PROJE_KOK / "veri"
HAM_VERI = VERI / "ham"            # Asla degistirilmeyen kaynak veri
ISLENMIS_VERI = VERI / "islenmis"  # Betiklerin urettigi ara ciktilar
SEKILLER = PROJE_KOK / "sekiller"  # Makaleye girecek gorseller
CIKTILAR = PROJE_KOK / "ciktilar"  # Tablolar, ozet dosyalari
MAKALE = PROJE_KOK / "makale"

# ---------------------------------------------------------------------------
# Koordinat sistemleri
# ---------------------------------------------------------------------------
# Cografi koordinat sistemi: enlem ve boylam, derece cinsinden.
# GPS cihazlari ve cogu acik veri kaynagi bu sistemde veri verir.
CRS_COGRAFI = "EPSG:4326"

# Metrik koordinat sistemi: metre cinsinden, alan ve mesafe hesabi icin.
# UTM 35. dilim, Turkiye'nin orta kesimini kapsar (30-36 dogu boylamlari).
# Calisma alaniniz baska bir dilimdeyse burayi degistirin:
#   UTM 35N: EPSG:32635   (30 - 36 dogu boylami)
#   UTM 36N: EPSG:32636   (36 - 42 dogu boylami)
#   UTM 37N: EPSG:32637   (42 - 48 dogu boylami)
CRS_METRIK = "EPSG:32635"

# ---------------------------------------------------------------------------
# Sekil ayarlari
# ---------------------------------------------------------------------------
# Cogu dergi sekiller icin en az 300 dpi ister. Kontrol edip degistirin.
SEKIL_COZUNURLUK = 300
SEKIL_BICIMI = "png"

# Tek sutun ve cift sutun sekil genislikleri (inc cinsinden).
# Derginin yazim kilavuzundan okuyup guncelleyin.
SEKIL_GENISLIK_TEK_SUTUN = 3.5
SEKIL_GENISLIK_CIFT_SUTUN = 7.2


def klasorleri_hazirla() -> None:
    """Betiklerin yazacagi klasorler yoksa olusturur."""
    for klasor in (HAM_VERI, ISLENMIS_VERI, SEKILLER, CIKTILAR):
        klasor.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    klasorleri_hazirla()
    print("Proje koku:", PROJE_KOK)
    print("Klasorler hazir.")
