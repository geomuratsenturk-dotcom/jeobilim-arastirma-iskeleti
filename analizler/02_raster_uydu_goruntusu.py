"""
02 - Raster ve uydu goruntusu analizi

Ne yapar:
    1. Sayisal yukseklik modelini okur ve ustverisini raporlar.
    2. Metrik koordinat sistemine yeniden projeksiyonlar.
    3. Egim ve bakisi hesaplar.
    4. Golgeli kabartma (hillshade) uretir.
    5. Saha noktalarinin bulundugu alani kirpar.
    6. Her saha noktasinin altindaki yukseklik degerini okur ve
       arazi olcumuyle karsilastirir.
    7. Uc panelli bir sekil cizer.

NDVI gibi bant indeksleri icin dosyanin sonundaki NDVI_ORNEGI bolumune bakin.

Kullanilan paketler: rasterio, numpy, geopandas, matplotlib

Calistirma (proje kokunden):
    python analizler/02_raster_uydu_goruntusu.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.warp import Resampling, calculate_default_transform, reproject

from kod import ayarlar, yardimcilar

GIRDI = ayarlar.HAM_VERI / "sayisal_yukseklik.tif"
NOKTALAR = ayarlar.HAM_VERI / "saha_noktalari.csv"


# ---------------------------------------------------------------------------
# 1. Oku ve ustveriyi raporla
# ---------------------------------------------------------------------------
def ustveriyi_raporla(yol: Path) -> dict:
    if not yol.exists():
        raise FileNotFoundError(
            f"{yol} bulunamadi.\n"
            "Once ornek veriyi uretin: python analizler/00_ornek_veri_uret.py"
        )

    with rasterio.open(yol) as kaynak:
        bilgi = {
            "boyut": (kaynak.height, kaynak.width),
            "bant_sayisi": kaynak.count,
            "veri_tipi": kaynak.dtypes[0],
            "koordinat_sistemi": str(kaynak.crs),
            "piksel_boyutu": (abs(kaynak.transform.a), abs(kaynak.transform.e)),
            "sinirlar": tuple(round(k, 4) for k in kaynak.bounds),
            "bosluk_degeri": kaynak.nodata,
        }

    yardimcilar.duyur(f"Raster okundu: {yol.name}")
    for anahtar, deger in bilgi.items():
        print(f"    {anahtar:<20} {deger}")
    return bilgi


# ---------------------------------------------------------------------------
# 2. Metrik sisteme yeniden projeksiyon
# ---------------------------------------------------------------------------
def metrik_sisteme_projeksiyonla(girdi: Path) -> Path:
    """
    Egim hesabi icin piksel boyutunun metre cinsinden olmasi sarttir.
    Derece cinsinden bir rasterda hesaplanan egim yanlistir.
    """
    cikti = ayarlar.ISLENMIS_VERI / "yukseklik_utm.tif"
    ayarlar.ISLENMIS_VERI.mkdir(parents=True, exist_ok=True)

    with rasterio.open(girdi) as kaynak:
        donusum, genislik, yukseklik = calculate_default_transform(
            kaynak.crs, ayarlar.CRS_METRIK, kaynak.width, kaynak.height, *kaynak.bounds
        )
        ustveri = kaynak.meta.copy()
        ustveri.update(
            crs=ayarlar.CRS_METRIK,
            transform=donusum,
            width=genislik,
            height=yukseklik,
            compress="deflate",
        )

        with rasterio.open(cikti, "w", **ustveri) as hedef:
            reproject(
                source=rasterio.band(kaynak, 1),
                destination=rasterio.band(hedef, 1),
                src_transform=kaynak.transform,
                src_crs=kaynak.crs,
                dst_transform=donusum,
                dst_crs=ayarlar.CRS_METRIK,
                resampling=Resampling.bilinear,
            )

    yardimcilar.duyur(f"Yeniden projeksiyonlandi: {cikti.name} ({yukseklik}x{genislik})")
    return cikti


# ---------------------------------------------------------------------------
# 3. Egim ve bakis
# ---------------------------------------------------------------------------
def egim_ve_bakis(yukseklik: np.ndarray, piksel_x: float, piksel_y: float):
    """
    Horn yontemiyle egim ve bakis hesabi. Sonuclar derece cinsindendir.

    Bakis, kuzeyden saat yonunde olculur: 0 kuzey, 90 dogu, 180 guney.
    """
    dz_dy, dz_dx = np.gradient(yukseklik, piksel_y, piksel_x)

    egim_radyan = np.arctan(np.hypot(dz_dx, dz_dy))
    egim_derece = np.degrees(egim_radyan)

    bakis_radyan = np.arctan2(-dz_dx, dz_dy)
    bakis_derece = (np.degrees(bakis_radyan) + 360) % 360

    return egim_derece, bakis_derece


def golgeli_kabartma(
    yukseklik: np.ndarray,
    piksel_x: float,
    piksel_y: float,
    azimut: float = 315.0,
    yukselme: float = 45.0,
) -> np.ndarray:
    """
    Golgeli kabartma. Haritalarda araziyi uc boyutlu gostermenin
    standart yoludur. Kuzeybatidan gelen isik (315 derece) alisilmis secimdir.
    """
    egim, bakis = egim_ve_bakis(yukseklik, piksel_x, piksel_y)
    egim_r = np.radians(egim)
    bakis_r = np.radians(bakis)
    azimut_r = np.radians(360.0 - azimut + 90.0)
    yukselme_r = np.radians(yukselme)

    golge = np.sin(yukselme_r) * np.cos(egim_r) + np.cos(yukselme_r) * np.sin(
        egim_r
    ) * np.cos(azimut_r - bakis_r)
    return np.clip(golge, 0, 1)


# ---------------------------------------------------------------------------
# 4. Nokta konumlarindan raster degeri okuma
# ---------------------------------------------------------------------------
def noktalarda_yukseklik_oku(raster_yolu: Path) -> gpd.GeoDataFrame | None:
    """
    Her saha noktasinin altindaki piksel degerini okur.
    Arazide olculen yukseklikle model yuksekligini karsilastirmak,
    veri kalitesi kontrolunun basit ve etkili bir adimidir.
    """
    if not NOKTALAR.exists():
        yardimcilar.duyur("Saha noktalari bulunamadi, bu adim atlaniyor.")
        return None

    import pandas as pd

    tablo = pd.read_csv(NOKTALAR)
    noktalar = gpd.GeoDataFrame(
        tablo,
        geometry=gpd.points_from_xy(tablo["boylam"], tablo["enlem"]),
        crs=ayarlar.CRS_COGRAFI,
    )

    with rasterio.open(raster_yolu) as kaynak:
        noktalar_raster_crs = noktalar.to_crs(kaynak.crs)
        koordinatlar = [
            (nokta.x, nokta.y) for nokta in noktalar_raster_crs.geometry
        ]
        okunan = [deger[0] for deger in kaynak.sample(koordinatlar)]

    noktalar["model_yukseklik_m"] = np.round(okunan, 1)
    noktalar["fark_m"] = np.round(
        noktalar["yukseklik_m"] - noktalar["model_yukseklik_m"], 1
    )

    yardimcilar.duyur(
        "Arazi olcumu ile model farki: "
        f"ortalama {noktalar['fark_m'].mean():+.1f} m, "
        f"mutlak ortalama {noktalar['fark_m'].abs().mean():.1f} m"
    )
    return noktalar


# ---------------------------------------------------------------------------
# 5. Sekil
# ---------------------------------------------------------------------------
def uc_panelli_sekil(
    yukseklik: np.ndarray, egim: np.ndarray, golge: np.ndarray, sinirlar
) -> Path:
    sekil, eksenler = plt.subplots(
        1,
        3,
        figsize=(ayarlar.SEKIL_GENISLIK_CIFT_SUTUN + 2.5, 3.6),
        layout="constrained",
    )

    kapsam = (sinirlar.left, sinirlar.right, sinirlar.bottom, sinirlar.top)

    g1 = eksenler[0].imshow(yukseklik, cmap="terrain", extent=kapsam)
    eksenler[0].set_title("a) Yukseklik", fontsize=10)
    renk_cubugu_1 = sekil.colorbar(g1, ax=eksenler[0], shrink=0.85, pad=0.02)
    # Birim etiketini renk cubugunun ustune koyuyoruz. Yana dik yazildiginda
    # yandaki panelin eksen etiketiyle karistiriliyor.
    renk_cubugu_1.ax.set_title("metre", fontsize=8, pad=4)
    renk_cubugu_1.ax.tick_params(labelsize=7)

    g2 = eksenler[1].imshow(
        egim, cmap="magma", extent=kapsam, vmin=0, vmax=np.nanpercentile(egim, 98)
    )
    eksenler[1].set_title("b) Egim", fontsize=10)
    renk_cubugu_2 = sekil.colorbar(g2, ax=eksenler[1], shrink=0.85, pad=0.02)
    renk_cubugu_2.ax.set_title("derece", fontsize=8, pad=4)
    renk_cubugu_2.ax.tick_params(labelsize=7)

    eksenler[2].imshow(golge, cmap="gray", extent=kapsam)
    eksenler[2].set_title("c) Golgeli kabartma", fontsize=10)

    for eksen in eksenler:
        eksen.set_xlabel("Dogu (km)", fontsize=8)
        eksen.tick_params(labelsize=7)
        # Koordinatlari kilometreye cevirerek eksen etiketlerini sadelestir
        eksen.set_xticks(eksen.get_xticks())
        eksen.set_xticklabels([f"{k / 1000:.0f}" for k in eksen.get_xticks()])
        eksen.set_xlim(sinirlar.left, sinirlar.right)
        eksen.set_aspect("equal")

    eksenler[0].set_ylabel("Kuzey (km)", fontsize=8)
    for eksen in eksenler:
        eksen.set_yticks(eksen.get_yticks())
        eksen.set_yticklabels([f"{k / 1000:.0f}" for k in eksen.get_yticks()])
        eksen.set_ylim(sinirlar.bottom, sinirlar.top)
    for eksen in eksenler[1:]:
        eksen.set_yticklabels([])

    sekil.suptitle(
        "Sayisal yukseklik modelinden turetilen arazi degiskenleri", fontsize=11
    )

    return yardimcilar.sekil_kaydet(sekil, "sekil_02_arazi_degiskenleri")


# ---------------------------------------------------------------------------
# Akis
# ---------------------------------------------------------------------------
def main() -> None:
    ayarlar.klasorleri_hazirla()
    yardimcilar.duyur("02 - Raster analizi basliyor")

    ustveriyi_raporla(GIRDI)
    utm_yolu = metrik_sisteme_projeksiyonla(GIRDI)

    with rasterio.open(utm_yolu) as kaynak:
        yukseklik = kaynak.read(1, masked=True).filled(np.nan)
        piksel_x = abs(kaynak.transform.a)
        piksel_y = abs(kaynak.transform.e)
        sinirlar = kaynak.bounds

    yardimcilar.duyur(f"Piksel boyutu: {piksel_x:.1f} m x {piksel_y:.1f} m")

    egim, bakis = egim_ve_bakis(yukseklik, piksel_x, piksel_y)
    golge = golgeli_kabartma(yukseklik, piksel_x, piksel_y)

    yardimcilar.duyur(
        f"Egim: ortalama {np.nanmean(egim):.1f} derece, "
        f"en yuksek {np.nanmax(egim):.1f} derece"
    )

    # Turetilmis katmanlari kaydet
    with rasterio.open(utm_yolu) as kaynak:
        ustveri = kaynak.meta.copy()
    ustveri.update(dtype="float32", compress="deflate")

    for ad, dizi in (("egim", egim), ("bakis", bakis), ("golge", golge)):
        yol = ayarlar.ISLENMIS_VERI / f"{ad}.tif"
        with rasterio.open(yol, "w", **ustveri) as hedef:
            hedef.write(dizi.astype("float32"), 1)
            hedef.set_band_description(1, ad)
        yardimcilar.duyur(f"Turetilmis katman yazildi: {yol.name}")

    # Nokta bazli kontrol
    noktalar = noktalarda_yukseklik_oku(GIRDI)
    if noktalar is not None:
        yol = ayarlar.CIKTILAR / "tablo_02_nokta_yukseklik_karsilastirma.csv"
        noktalar.drop(columns="geometry").to_csv(yol, index=False, encoding="utf-8")
        yardimcilar.duyur(f"Karsilastirma tablosu yazildi: {yol.name}")

    uc_panelli_sekil(yukseklik, egim, golge, sinirlar)
    yardimcilar.duyur("02 tamamlandi.")


# ---------------------------------------------------------------------------
# NDVI_ORNEGI
# ---------------------------------------------------------------------------
# Cok bantli bir uydu goruntunuz varsa (ornegin Sentinel-2), bitki ortusu
# indeksi NDVI su sekilde hesaplanir. Bant numaralari uyduya gore degisir.
#
#     with rasterio.open("sentinel2_goruntu.tif") as kaynak:
#         kirmizi = kaynak.read(4).astype("float32")   # B04
#         yakin_kizilotesi = kaynak.read(8).astype("float32")  # B08
#         ustveri = kaynak.meta.copy()
#
#     # Sifira bolmeyi engelle
#     paydda = yakin_kizilotesi + kirmizi
#     ndvi = np.where(paydda == 0, np.nan, (yakin_kizilotesi - kirmizi) / paydda)
#
#     ustveri.update(count=1, dtype="float32", nodata=np.nan)
#     with rasterio.open("ndvi.tif", "w", **ustveri) as hedef:
#         hedef.write(ndvi.astype("float32"), 1)
#
# NDVI degerleri -1 ile +1 arasindadir. 0.2'nin altindaki degerler ciplak
# zemin veya kaya, 0.5 ustu degerler yogun bitki ortusu anlamina gelir.
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    main()
