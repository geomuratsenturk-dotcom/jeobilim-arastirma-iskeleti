# Kurulum

İki yol var. Mekânsal analiz yapacaksanız birinci yolu seçin.

---

## Yol 1: Conda (önerilen)

Mekânsal paketler (GeoPandas, Rasterio) arka planda GDAL, PROJ ve GEOS
adlı C kütüphanelerine dayanır. Conda bunları uyumlu sürümlerle birlikte
kurar. pip ile kurduğunuzda sürümler çakışabilir ve hata mesajları
anlaşılmaz olur.

### Miniforge kurulumu

Anaconda yerine Miniforge önerilir. Daha küçüktür ve varsayılan olarak
conda-forge kanalını kullanır.

İndirme adresi: <https://github.com/conda-forge/miniforge>

- Windows: `Miniforge3-Windows-x86_64.exe`
- macOS (Apple Silicon): `Miniforge3-MacOSX-arm64.sh`
- macOS (Intel): `Miniforge3-MacOSX-x86_64.sh`
- Linux: `Miniforge3-Linux-x86_64.sh`

### Ortamı oluşturma

```bash
conda env create -f ortam.yml
conda activate jeobilim
```

İlk kurulum birkaç dakika sürebilir. Kurulum bittikten sonra kontrol edin:

```bash
make kontrol
```

Ya da make kurulu değilse:

```bash
python -c "import geopandas, rasterio, obspy; print('kurulum tamam')"
```

---

## Yol 2: pip ve sanal ortam

Yalnızca sismoloji veya tablo analizi yapacaksanız bu yol yeterlidir.

```bash
python -m venv .venv

# Linux ve macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows cmd
.venv\Scripts\activate.bat

pip install --upgrade pip
pip install -r gereksinimler.txt
```

### Windows'ta rasterio kurulmuyorsa

Windows'ta pip ile GDAL bağımlılığı sorun çıkarabilir. İki seçenek:

1. Conda yoluna geçin (yukarıdaki Yol 1).
2. Christoph Gohlke'nin derlenmiş paketlerini kullanın:
   <https://github.com/cgohlke/geospatial-wheels>

---

## Quarto (makale derlemek için)

Quarto, analiz kodu ile metni tek belgede birleştiren yayın sistemidir.
Analizler onsuz da çalışır; yalnızca `makale/makale.qmd` dosyasını
derlemek için gerekir.

İndirme adresi: <https://quarto.org/docs/get-started/>

PDF çıktısı almak için ayrıca bir LaTeX dağıtımı gerekir. En kolay yol:

```bash
quarto install tinytex
```

Kurulumu doğrulayın:

```bash
quarto check
```

---

## Zotero ve kaynakça bağlantısı

Makale kaynakçasını elle yazmak yerine Zotero'ya bağlayın.

1. Zotero'yu kurun: <https://www.zotero.org/download/>
2. Better BibTeX eklentisini kurun:
   <https://retorque.re/zotero-better-bibtex/>
3. Zotero'da bu proje için bir koleksiyon oluşturun.
4. Koleksiyona sağ tıklayın, `Export Collection` seçin.
5. Biçim olarak `Better BibLaTeX` seçin, `Keep updated` kutusunu işaretleyin.
6. Dosyayı `makale/kaynaklar.bib` olarak kaydedin.

Artık Zotero'ya eklediğiniz her kaynak bu dosyada otomatik belirir.
Makalede `[@atifanahtari]` yazarak kullanırsınız.

### Atıf stili

Derginizin istediği stil dosyasını indirip `makale/` klasörüne koyun ve
`makale.qmd` dosyasının başındaki `csl:` satırını açın.

Stil arşivi: <https://www.zotero.org/styles>

---

## Sık karşılaşılan sorunlar

**`ModuleNotFoundError: No module named 'kod'`**

Betiği proje kökünden çalıştırmadınız. Şöyle çalıştırın:

```bash
cd /projenin/bulundugu/klasor
python analizler/01_vektor_saha_verisi.py
```

`analizler/` klasörünün içine girip `python 01_...py` şeklinde
çalıştırırsanız bu hata çıkar.

**`FileNotFoundError: ... saha_noktalari.csv bulunamadi`**

Örnek veriyi henüz üretmediniz:

```bash
python analizler/00_ornek_veri_uret.py
```

**`CRSError` veya koordinat dönüşümü hatası**

PROJ veri dosyaları eksik olabilir. Conda ortamında:

```bash
conda install -c conda-forge proj-data
```

**Şekillerde Türkçe karakterler kutu olarak görünüyor**

Matplotlib'in varsayılan yazı tipi bazı sistemlerde Türkçe karakterleri
göstermez. `kod/ayarlar.py` dosyasına şunu ekleyin:

```python
import matplotlib
matplotlib.rcParams["font.family"] = "DejaVu Sans"
```

**Bellek hatası (büyük raster işlerken)**

Rasterio ile büyük dosyaları parça parça okuyun:

```python
with rasterio.open(yol) as kaynak:
    for _, pencere in kaynak.block_windows(1):
        parca = kaynak.read(1, window=pencere)
        # parcayi isle
```
