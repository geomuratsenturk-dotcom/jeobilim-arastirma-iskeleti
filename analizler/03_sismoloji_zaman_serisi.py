"""
03 - Sismoloji zaman serisi analizi

Ne yapar:
    1. Ucbilesenli bir sismogram okur.
    2. Kayit ustverisini raporlar.
    3. On isleme uygular: ortalama cikarma, egilim giderme, pencereleme.
    4. Bant gecirgen suzgec uygular.
    5. Genlik spektrumunu hesaplar.
    6. Spektrogram (zaman - frekans gorunumu) uretir.
    7. Ham ve suzulmus dalga formlarini karsilastiran bir sekil cizer.
    8. Islenmis kaydi MSEED olarak kaydeder.

Varsayilan olarak obspy ile birlikte gelen ornek kaydi kullanir; boylece
internet baglantisi olmadan da calisir. Gercek veri icin:

    python analizler/03_sismoloji_zaman_serisi.py --cevrimici

Bu secenek AFAD, KOERI veya IRIS gibi bir FDSN sunucusundan veri ceker.

Kullanilan paketler: obspy, numpy, matplotlib

Calistirma (proje kokunden):
    python analizler/03_sismoloji_zaman_serisi.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np
import obspy

from kod import ayarlar, yardimcilar

# Suzgec sinirlari. Yerel depremler icin 1-20 Hz alisilmis bir araliktir.
# Uzak (telesismik) kayitlar icin 0.02-0.5 Hz gibi cok daha dusuk degerler kullanilir.
SUZGEC_ALT_HZ = 1.0
SUZGEC_UST_HZ = 20.0


# ---------------------------------------------------------------------------
# 1. Veriyi al
# ---------------------------------------------------------------------------
def cevrimdisi_kayit_oku() -> obspy.Stream:
    """obspy ile gelen ucbilesenli ornek kaydi okur."""
    akis = obspy.read()  # Argumansiz cagri gomulu ornek kaydi dondurur
    yardimcilar.duyur(f"Ornek kayit okundu: {len(akis)} bilesen")
    return akis


def cevrimici_kayit_oku() -> obspy.Stream:
    """
    Bir FDSN sunucusundan gercek kayit ceker.

    Turkiye icin kullanilabilecek sunucular:
        "KOERI"  - Bogazici Universitesi Kandilli Rasathanesi
        "IRIS"   - Kuresel arsiv, Turkiye istasyonlarinin cogunu da icerir
        "ORFEUS" - Avrupa arsivi

    Istasyon ve zaman araligini kendi calismaniza gore degistirin.
    """
    from obspy.clients.fdsn import Client

    istemci = Client("IRIS", timeout=30)
    baslangic = obspy.UTCDateTime("2023-02-06T01:17:35")  # Kahramanmaras depremi
    akis = istemci.get_waveforms(
        network="IU",
        station="ANTO",       # Ankara, kuresel ag istasyonu
        location="00",
        channel="BH?",
        starttime=baslangic,
        endtime=baslangic + 600,
        attach_response=True,
    )
    yardimcilar.duyur(f"Cevrimici kayit alindi: {len(akis)} bilesen")
    return akis


# ---------------------------------------------------------------------------
# 2. Ustveri
# ---------------------------------------------------------------------------
def ustveriyi_raporla(akis: obspy.Stream) -> None:
    yardimcilar.duyur("Kayit ustverisi:")
    for iz in akis:
        istatistik = iz.stats
        print(
            f"    {istatistik.network}.{istatistik.station}."
            f"{istatistik.location}.{istatistik.channel}  "
            f"ornekleme {istatistik.sampling_rate:.0f} Hz  "
            f"sure {istatistik.npts / istatistik.sampling_rate:.1f} s  "
            f"baslangic {istatistik.starttime}"
        )


# ---------------------------------------------------------------------------
# 3. On isleme ve suzgec
# ---------------------------------------------------------------------------
def on_isle_ve_suz(akis: obspy.Stream) -> obspy.Stream:
    """
    Suzgec uygulamadan once bu uc adim standarttir. Atlanirsa suzgec
    kayit kenarlarinda yapay salinimlar uretir.
    """
    islenmis = akis.copy()
    islenmis.detrend("demean")   # Ortalamayi sifira cek
    islenmis.detrend("linear")   # Dogrusal egilimi gider
    islenmis.taper(max_percentage=0.05, type="hann")  # Kenarlari yumusat

    nyquist = islenmis[0].stats.sampling_rate / 2.0
    ust_sinir = min(SUZGEC_UST_HZ, nyquist * 0.9)

    islenmis.filter(
        "bandpass",
        freqmin=SUZGEC_ALT_HZ,
        freqmax=ust_sinir,
        corners=4,
        zerophase=True,  # Faz kaymasini onler, varis zamani olcumu icin onemli
    )
    yardimcilar.duyur(
        f"Bant gecirgen suzgec uygulandi: {SUZGEC_ALT_HZ} - {ust_sinir:.1f} Hz"
    )
    return islenmis


# ---------------------------------------------------------------------------
# 4. Genlik spektrumu
# ---------------------------------------------------------------------------
def genlik_spektrumu(iz: obspy.Trace):
    """Tek bir bilesenin genlik spektrumunu dondurur."""
    veri = iz.data - np.mean(iz.data)
    ornekleme = iz.stats.sampling_rate

    spektrum = np.abs(np.fft.rfft(veri))
    frekans = np.fft.rfftfreq(len(veri), d=1.0 / ornekleme)
    return frekans, spektrum


# ---------------------------------------------------------------------------
# 5. Sekil
# ---------------------------------------------------------------------------
def karsilastirma_sekli(ham: obspy.Stream, suzulmus: obspy.Stream) -> Path:
    bilesen_sayisi = min(len(ham), 3)
    sekil, eksenler = plt.subplots(
        bilesen_sayisi + 1,
        1,
        figsize=(ayarlar.SEKIL_GENISLIK_CIFT_SUTUN, 2.0 * (bilesen_sayisi + 1)),
    )

    for sira in range(bilesen_sayisi):
        iz_ham = ham[sira]
        iz_suz = suzulmus[sira]
        zaman = np.arange(iz_ham.stats.npts) / iz_ham.stats.sampling_rate

        eksen = eksenler[sira]
        eksen.plot(zaman, iz_ham.data, linewidth=0.5, color="0.6", label="ham")
        eksen.plot(zaman, iz_suz.data, linewidth=0.6, color="firebrick", label="suzulmus")
        eksen.set_ylabel(iz_ham.stats.channel, fontsize=9)
        eksen.legend(fontsize=7, loc="upper right")
        eksen.grid(alpha=0.2, linestyle=":")
        if sira < bilesen_sayisi - 1:
            eksen.set_xticklabels([])

    eksenler[bilesen_sayisi - 1].set_xlabel("Zaman (s)", fontsize=9)

    # Son panel: genlik spektrumu
    eksen_spektrum = eksenler[-1]
    for iz in suzulmus[:bilesen_sayisi]:
        frekans, spektrum = genlik_spektrumu(iz)
        eksen_spektrum.loglog(
            frekans[1:], spektrum[1:], linewidth=0.7, label=iz.stats.channel
        )
    eksen_spektrum.set_xlabel("Frekans (Hz)", fontsize=9)
    eksen_spektrum.set_ylabel("Genlik", fontsize=9)
    eksen_spektrum.legend(fontsize=7)
    eksen_spektrum.grid(alpha=0.2, which="both", linestyle=":")

    istasyon = suzulmus[0].stats.station
    sekil.suptitle(
        f"{istasyon} istasyonu: ham ve suzulmus dalga formlari ile genlik spektrumu",
        fontsize=10,
    )
    sekil.tight_layout()

    return yardimcilar.sekil_kaydet(sekil, "sekil_03_dalga_formu")


def spektrogram_sekli(iz: obspy.Trace) -> Path:
    sekil, eksen = plt.subplots(
        figsize=(ayarlar.SEKIL_GENISLIK_CIFT_SUTUN, 3.2)
    )
    eksen.specgram(
        iz.data,
        Fs=iz.stats.sampling_rate,
        NFFT=256,
        noverlap=192,
        cmap="viridis",
    )
    eksen.set_xlabel("Zaman (s)", fontsize=9)
    eksen.set_ylabel("Frekans (Hz)", fontsize=9)
    eksen.set_title(
        f"{iz.stats.station}.{iz.stats.channel} bileseninin spektrogrami", fontsize=10
    )
    sekil.tight_layout()
    return yardimcilar.sekil_kaydet(sekil, "sekil_04_spektrogram")


# ---------------------------------------------------------------------------
# Akis
# ---------------------------------------------------------------------------
def main() -> None:
    ayrıstirici = argparse.ArgumentParser(description="Sismoloji zaman serisi analizi")
    ayrıstirici.add_argument(
        "--cevrimici",
        action="store_true",
        help="Gercek veriyi FDSN sunucusundan cek (internet baglantisi gerekir)",
    )
    argumanlar = ayrıstirici.parse_args()

    ayarlar.klasorleri_hazirla()
    yardimcilar.duyur("03 - Sismoloji analizi basliyor")

    if argumanlar.cevrimici:
        try:
            akis = cevrimici_kayit_oku()
        except Exception as hata:
            yardimcilar.duyur(f"Cevrimici erisim basarisiz oldu: {hata}")
            yardimcilar.duyur("Ornek kayda geciliyor.")
            akis = cevrimdisi_kayit_oku()
    else:
        akis = cevrimdisi_kayit_oku()

    ustveriyi_raporla(akis)

    suzulmus = on_isle_ve_suz(akis)

    for iz in suzulmus:
        yardimcilar.duyur(
            f"{iz.stats.channel}: en buyuk genlik {np.abs(iz.data).max():.1f}, "
            f"etkin deger {np.sqrt(np.mean(iz.data.astype(float) ** 2)):.1f}"
        )

    karsilastirma_sekli(akis, suzulmus)
    spektrogram_sekli(suzulmus[0])

    cikti = ayarlar.ISLENMIS_VERI / "sismogram_suzulmus.mseed"
    suzulmus.write(str(cikti), format="MSEED")
    yardimcilar.duyur(f"Islenmis kayit yazildi: {cikti.name}")

    yardimcilar.duyur("03 tamamlandi.")


if __name__ == "__main__":
    main()
