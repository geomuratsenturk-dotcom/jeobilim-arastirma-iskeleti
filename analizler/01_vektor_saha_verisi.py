"""
01 - Vektor saha verisi analizi

Ne yapar:
    1. Arazi olcum noktalarini CSV dosyasindan okur.
    2. Noktalari cografi koordinat sisteminden metrik sisteme donusturur.
    3. Litolojiye gore ozet tablo uretir.
    4. En yakin komsu mesafelerini hesaplar (nokta dagiliminin sikligi).
    5. Litoloji renkli bir konum haritasi cizer.
    6. Sonuclari GeoPackage ve CSV olarak kaydeder.

Kullanilan paketler: geopandas, shapely, pandas, matplotlib

Calistirma (proje kokunden):
    python analizler/01_vektor_saha_verisi.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from kod import ayarlar, yardimcilar

GIRDI = ayarlar.HAM_VERI / "saha_noktalari.csv"


# ---------------------------------------------------------------------------
# 1. Veriyi oku ve mekansal hale getir
# ---------------------------------------------------------------------------
def noktalari_oku() -> gpd.GeoDataFrame:
    if not GIRDI.exists():
        raise FileNotFoundError(
            f"{GIRDI} bulunamadi.\n"
            "Once ornek veriyi uretin: python analizler/00_ornek_veri_uret.py"
        )

    tablo = pd.read_csv(GIRDI)
    yardimcilar.duyur(f"{len(tablo)} satir okundu: {GIRDI.name}")

    # Boylam x eksenine, enlem y eksenine gelir. Sirasi karistirmak
    # bu alandaki en sik hatalardan biridir.
    noktalar = gpd.GeoDataFrame(
        tablo,
        geometry=gpd.points_from_xy(tablo["boylam"], tablo["enlem"]),
        crs=ayarlar.CRS_COGRAFI,
    )
    return noktalar


# ---------------------------------------------------------------------------
# 2. Metrik sisteme donustur
# ---------------------------------------------------------------------------
def metrik_sisteme_donustur(noktalar: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Mesafe ve alan hesabi yapmadan once mutlaka metrik sisteme gecin.
    Derece cinsinden hesaplanan mesafe anlamli bir buyukluk degildir.
    """
    metrik = noktalar.to_crs(ayarlar.CRS_METRIK)
    yardimcilar.duyur(f"Koordinat sistemi donusturuldu: {ayarlar.CRS_METRIK}")
    return metrik


# ---------------------------------------------------------------------------
# 3. Litolojiye gore ozet
# ---------------------------------------------------------------------------
def litoloji_ozeti(noktalar: gpd.GeoDataFrame) -> pd.DataFrame:
    ozet = (
        noktalar.groupby("litoloji")
        .agg(
            nokta_sayisi=("nokta_no", "count"),
            ortalama_yukseklik_m=("yukseklik_m", "mean"),
            en_dusuk_yukseklik_m=("yukseklik_m", "min"),
            en_yuksek_yukseklik_m=("yukseklik_m", "max"),
            ortalama_egim_derece=("tabaka_egim_derece", "mean"),
            ornek_alinan=("ornek_alindi", "sum"),
        )
        .round(1)
        .sort_values("nokta_sayisi", ascending=False)
    )
    return ozet


# ---------------------------------------------------------------------------
# 4. En yakin komsu mesafesi
# ---------------------------------------------------------------------------
def en_yakin_komsu_mesafeleri(noktalar_metrik: gpd.GeoDataFrame) -> pd.Series:
    """
    Her nokta icin kendisi disindaki en yakin noktaya olan mesafe.
    Orneklem sikligini ve bosluklari gormek icin pratik bir olcut.
    """
    birlesim = gpd.sjoin_nearest(
        noktalar_metrik[["nokta_no", "geometry"]],
        noktalar_metrik[["nokta_no", "geometry"]].rename(
            columns={"nokta_no": "komsu_no"}
        ),
        how="left",
        distance_col="mesafe_m",
        exclusive=True,
    )
    # Esit mesafeli birden fazla komsu varsa ilkini al.
    mesafe = birlesim.groupby("nokta_no")["mesafe_m"].min()
    return mesafe.round(1)


# ---------------------------------------------------------------------------
# 5. Harita
# ---------------------------------------------------------------------------
def konum_haritasi_ciz(noktalar: gpd.GeoDataFrame) -> Path:
    sekil, eksen = plt.subplots(
        figsize=(ayarlar.SEKIL_GENISLIK_CIFT_SUTUN, 5.5)
    )

    for litoloji, grup in noktalar.groupby("litoloji"):
        eksen.scatter(
            grup.geometry.x,
            grup.geometry.y,
            s=grup["yukseklik_m"] / 8,
            label=f"{litoloji} (n={len(grup)})",
            alpha=0.75,
            edgecolors="black",
            linewidths=0.4,
        )

    eksen.set_xlabel("Boylam (derece)")
    eksen.set_ylabel("Enlem (derece)")
    eksen.set_title(
        "Arazi olcum noktalarinin litolojiye gore dagilimi\n"
        "(daire buyuklugu yuksekligi gosterir)",
        fontsize=10,
    )
    eksen.legend(fontsize=7, loc="upper right", framealpha=0.9)
    eksen.grid(alpha=0.25, linestyle=":")
    eksen.set_aspect("equal", adjustable="datalim")

    return yardimcilar.sekil_kaydet(sekil, "sekil_01_nokta_dagilimi")


# ---------------------------------------------------------------------------
# Akis
# ---------------------------------------------------------------------------
def main() -> None:
    ayarlar.klasorleri_hazirla()
    yardimcilar.duyur("01 - Vektor saha verisi analizi basliyor")

    noktalar = noktalari_oku()
    noktalar_metrik = metrik_sisteme_donustur(noktalar)

    # Ozet tablo
    ozet = litoloji_ozeti(noktalar)
    ozet_yolu = ayarlar.CIKTILAR / "tablo_01_litoloji_ozeti.csv"
    ozet.to_csv(ozet_yolu, encoding="utf-8")
    yardimcilar.duyur(f"Ozet tablo yazildi: {ozet_yolu.name}")
    print()
    print(ozet.to_string())
    print()

    # En yakin komsu
    mesafeler = en_yakin_komsu_mesafeleri(noktalar_metrik)
    noktalar_metrik = noktalar_metrik.merge(
        mesafeler.rename("en_yakin_komsu_m"), on="nokta_no", how="left"
    )
    yardimcilar.duyur(
        "En yakin komsu mesafesi: "
        f"ortalama {mesafeler.mean():.0f} m, "
        f"en kucuk {mesafeler.min():.0f} m, "
        f"en buyuk {mesafeler.max():.0f} m"
    )

    # Harita
    konum_haritasi_ciz(noktalar)

    # Kalici cikti: GeoPackage tercih edin, shapefile degil.
    # Shapefile alan adlarini 10 karaktere kirpar ve Turkce karakterde sorun cikarir.
    gpkg_yolu = ayarlar.ISLENMIS_VERI / "saha_noktalari.gpkg"
    noktalar_metrik.to_file(gpkg_yolu, layer="saha_noktalari", driver="GPKG")
    yardimcilar.duyur(f"Mekansal cikti yazildi: {gpkg_yolu.name}")

    yardimcilar.ortam_bilgisi_yaz()
    yardimcilar.duyur("01 tamamlandi.")


if __name__ == "__main__":
    main()
