"""
00 - Ornek veri uretimi

Bu betik, iskeletin kutudan cikar cikmaz calismasi icin yapay ornek veri
uretir. Gercek projenizde bu betigi silin ve kendi verinizi veri/ham/
klasorune koyun.

Uretilen dosyalar:
    veri/ham/saha_noktalari.csv   - 60 adet yapay arazi olcum noktasi
    veri/ham/sayisal_yukseklik.tif - 1 km cozunurlukte yapay yukseklik modeli

Calistirma:
    python analizler/00_ornek_veri_uret.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_origin

from kod import ayarlar, yardimcilar

# Calisma alani: Bati Anadolu'da yapay bir dikdortgen alan.
# Kendi alaniniz icin bu dort sayiyi degistirmeniz yeterli.
BOYLAM_MIN, BOYLAM_MAK = 28.90, 29.40
ENLEM_MIN, ENLEM_MAK = 37.60, 38.00

LITOLOJILER = ["kirectasi", "kumtasi", "marn", "andezit", "alüvyon"]
NOKTA_SAYISI = 60


def saha_noktalari_uret() -> Path:
    """Arazi olcum noktalarini bir CSV dosyasi olarak yazar."""
    yardimcilar.tohum_sabitle(42)

    boylam = np.random.uniform(BOYLAM_MIN, BOYLAM_MAK, NOKTA_SAYISI)
    enlem = np.random.uniform(ENLEM_MIN, ENLEM_MAK, NOKTA_SAYISI)

    # Yuksekligi konuma bagli yapay bir egilimle uretiyoruz ki
    # sayisal yukseklik modeliyle tutarli gorunsun.
    yukseklik = (
        400
        + 900 * np.exp(-(((boylam - 29.15) ** 2 + (enlem - 37.80) ** 2) / 0.02))
        + np.random.normal(0, 40, NOKTA_SAYISI)
    )

    tablo = pd.DataFrame(
        {
            "nokta_no": [f"N-{i:03d}" for i in range(1, NOKTA_SAYISI + 1)],
            "boylam": np.round(boylam, 6),
            "enlem": np.round(enlem, 6),
            "yukseklik_m": np.round(yukseklik, 1),
            "litoloji": np.random.choice(LITOLOJILER, NOKTA_SAYISI),
            "tabaka_dogrultu_derece": np.random.randint(0, 360, NOKTA_SAYISI),
            "tabaka_egim_derece": np.random.randint(5, 85, NOKTA_SAYISI),
            "ornek_alindi": np.random.choice([True, False], NOKTA_SAYISI, p=[0.4, 0.6]),
        }
    )

    ayarlar.HAM_VERI.mkdir(parents=True, exist_ok=True)
    yol = ayarlar.HAM_VERI / "saha_noktalari.csv"
    tablo.to_csv(yol, index=False, encoding="utf-8")
    yardimcilar.duyur(f"{len(tablo)} nokta yazildi: {yol.name}")
    return yol


def yukseklik_modeli_uret() -> Path:
    """Calisma alanini kapsayan yapay bir sayisal yukseklik modeli yazar."""
    yardimcilar.tohum_sabitle(42)

    satir, sutun = 400, 500
    piksel_derece = (BOYLAM_MAK - BOYLAM_MIN) / sutun

    x = np.linspace(BOYLAM_MIN, BOYLAM_MAK, sutun)
    y = np.linspace(ENLEM_MAK, ENLEM_MIN, satir)
    xx, yy = np.meshgrid(x, y)

    # Uc tepe ve bir vadi: gercek araziye benzer bir yuzey olusturur.
    yuzey = (
        900 * np.exp(-(((xx - 29.15) ** 2 + (yy - 37.80) ** 2) / 0.010))
        + 500 * np.exp(-(((xx - 29.05) ** 2 + (yy - 37.92) ** 2) / 0.004))
        + 350 * np.exp(-(((xx - 29.30) ** 2 + (yy - 37.68) ** 2) / 0.003))
        - 200 * np.exp(-(((xx - 29.20) ** 2 + (yy - 37.90) ** 2) / 0.002))
        + 400
    )
    # Ince olcekli arazi puruzlulugu.
    # Gurultuyu once kaba bir izgarada uretip sonra buyutuyoruz. Boylece
    # piksel piksel zipzip degil, gercek arazi gibi surekli bir yuzey cikar.
    # Piksel olcegindeki beyaz gurultu, egim hesabini anlamsiz hale getirir.
    from scipy.ndimage import zoom

    kaba = np.random.normal(0, 55, (satir // 25 + 1, sutun // 25 + 1))
    puruzluluk = zoom(kaba, (satir / kaba.shape[0], sutun / kaba.shape[1]), order=3)
    yuzey += puruzluluk[:satir, :sutun]
    yuzey = yuzey.astype("float32")

    donusum = from_origin(BOYLAM_MIN, ENLEM_MAK, piksel_derece, piksel_derece)

    ayarlar.HAM_VERI.mkdir(parents=True, exist_ok=True)
    yol = ayarlar.HAM_VERI / "sayisal_yukseklik.tif"

    with rasterio.open(
        yol,
        "w",
        driver="GTiff",
        height=satir,
        width=sutun,
        count=1,
        dtype="float32",
        crs=ayarlar.CRS_COGRAFI,
        transform=donusum,
        nodata=-9999.0,
        compress="deflate",
    ) as kaynak:
        kaynak.write(yuzey, 1)
        kaynak.set_band_description(1, "yukseklik_metre")

    yardimcilar.duyur(f"Yukseklik modeli yazildi: {yol.name} ({satir}x{sutun})")
    return yol


def main() -> None:
    ayarlar.klasorleri_hazirla()
    yardimcilar.duyur("Ornek veri uretimi basliyor")
    saha_noktalari_uret()
    yukseklik_modeli_uret()
    yardimcilar.duyur("Ornek veri hazir. Gercek projede bu betigi silin.")


if __name__ == "__main__":
    main()
