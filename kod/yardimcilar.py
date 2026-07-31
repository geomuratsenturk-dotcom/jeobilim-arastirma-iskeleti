"""
Butun analizlerde tekrar eden kucuk isler.

Buraya koydugunuz her fonksiyon, uc analiz betiginde de aynen calisir.
Kopyala yapistir yerine buraya yazip cagirin.
"""

from __future__ import annotations

import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt

from kod import ayarlar


def duyur(mesaj: str) -> None:
    """Ekrana zaman damgali bir ilerleme satiri yazar."""
    saat = datetime.now().strftime("%H:%M:%S")
    print(f"[{saat}] {mesaj}", flush=True)


def sekil_kaydet(sekil: plt.Figure, dosya_adi: str, aciklama: str = "") -> Path:
    """
    Sekli sekiller/ klasorune dergi cozunurlugunde kaydeder.

    dosya_adi uzantisiz verilir. Uzanti ayarlar.SEKIL_BICIMI degerinden gelir.
    """
    ayarlar.SEKILLER.mkdir(parents=True, exist_ok=True)
    yol = ayarlar.SEKILLER / f"{dosya_adi}.{ayarlar.SEKIL_BICIMI}"
    sekil.savefig(yol, dpi=ayarlar.SEKIL_COZUNURLUK, bbox_inches="tight")
    plt.close(sekil)
    duyur(f"Sekil kaydedildi: {yol.name} {aciklama}".strip())
    return yol


def ortam_bilgisi_yaz(dosya_adi: str = "ortam_bilgisi.txt") -> Path:
    """
    Analizin hangi ortamda calistigini kayit altina alir.

    Bunu her calistirmada uretmek, aylar sonra "bende neden farkli sonuc
    cikti" sorusunu cevaplamanin en ucuz yoludur.
    """
    ayarlar.CIKTILAR.mkdir(parents=True, exist_ok=True)
    yol = ayarlar.CIKTILAR / dosya_adi

    satirlar = [
        f"Calistirma zamani (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Isletim sistemi        : {platform.platform()}",
        f"Python                 : {sys.version.split()[0]}",
        "",
        "Paket surumleri:",
    ]

    for paket in ("numpy", "pandas", "geopandas", "rasterio", "pyproj",
                  "shapely", "obspy", "matplotlib"):
        try:
            modul = __import__(paket)
            satirlar.append(f"  {paket:<12} {getattr(modul, '__version__', 'bilinmiyor')}")
        except ImportError:
            satirlar.append(f"  {paket:<12} kurulu degil")

    yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    duyur(f"Ortam bilgisi yazildi: {yol.name}")
    return yol


def tohum_sabitle(tohum: int = 42) -> None:
    """
    Rastgelelik iceren islemleri tekrarlanabilir hale getirir.

    Ornek veri uretimi, bootstrap, egitim ve test ayrimi gibi her yerde
    cagirin. Cagirmadiginiz her rastgele islem, sonucunuzu yeniden
    uretilemez yapar.
    """
    import random

    import numpy as np

    random.seed(tohum)
    np.random.seed(tohum)
