# Yer Bilimleri Araştırma Deposu İskeleti

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21722688.svg)](https://doi.org/10.5281/zenodo.21722688)
[![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

Saha verisinden makaleye giden yolu tek bir klasörde toplayan, yeniden
üretilebilir bir araştırma deposu şablonu.

Bu bir kütüphane değil, bir başlangıç noktasıdır. Kopyalayın, adını
değiştirin, kendi verinizi koyun ve çalışmaya başlayın.

---

## Neden böyle bir yapı

Bir araştırmayı bitirdikten altı ay sonra hakem düzeltmesi gelir. O anda
sorulacak sorular hep aynıdır:

- Şekil 3'ü hangi kodla ürettim?
- O tabloda kullandığım veri hangi sürümüydü?
- Analizi hangi paket sürümleriyle çalıştırmıştım?

Bu iskelet, o üç soruyu cevaplamak için tasarlanmıştır. Ana kural şudur:
**ham veriye asla dokunulmaz, her çıktı bir betikten üretilir.** Elle
düzenlenmiş hiçbir ara dosya bulunmaz. Böylece analizi baştan
çalıştırdığınızda aynı şekiller ve aynı tablolar yeniden üretilir.

---

## Klasör yapısı

```
.
├── veri/
│   ├── ham/          Kaynak veri. Buraya bir kez yazılır, bir daha değiştirilmez.
│   └── islenmis/     Betiklerin ürettiği ara çıktılar. Silinip yeniden üretilebilir.
├── kod/              Analizlerin ortak kullandığı ayarlar ve yardımcı fonksiyonlar.
├── analizler/        Numaralandırılmış analiz betikleri. Sırayla çalışır.
├── sekiller/         Makaleye girecek görseller. Betikler üretir.
├── ciktilar/         Tablolar ve özet dosyaları. Betikler üretir.
├── makale/           Quarto makale taslağı ve kaynakça.
└── belgeler/         Kurulum, katkı ve GitHub yükleme kılavuzları.
```

Üç kural:

1. `veri/ham/` klasörüne elle dosya koyulur, betikler oraya asla yazmaz.
2. `sekiller/`, `ciktilar/` ve `veri/islenmis/` klasörlerinin tamamı
   silinebilir olmalıdır. Betikleri baştan çalıştırdığınızda hepsi geri gelir.
3. Hiçbir betikte elle yazılmış dosya yolu bulunmaz. Bütün yollar
   `kod/ayarlar.py` dosyasından gelir.

---

## Hızlı başlangıç

```bash
# 1. Ortamı kurun (conda kullanıyorsanız)
conda env create -f ortam.yml
conda activate jeobilim

# pip kullanıyorsanız
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r gereksinimler.txt

# 2. Örnek veriyi üretin
python analizler/00_ornek_veri_uret.py

# 3. Analizleri sırayla çalıştırın
python analizler/01_vektor_saha_verisi.py
python analizler/02_raster_uydu_goruntusu.py
python analizler/03_sismoloji_zaman_serisi.py
```

Hepsini tek komutla çalıştırmak için:

```bash
make tumu
```

Ayrıntılı kurulum adımları için `belgeler/KURULUM.md` dosyasına bakın.

---

## İçindeki üç örnek analiz

Her biri bağımsız çalışır ve kendi şeklini üretir. Kendi çalışmanıza
uymayanı silin, uyanı temel alarak genişletin.

### 01 - Vektör saha verisi

Arazi ölçüm noktalarını CSV'den okur, koordinat sistemini dönüştürür,
litolojiye göre özet çıkarır, en yakın komşu mesafelerini hesaplar ve
konum haritası çizer.

Kullanılan paketler: geopandas, shapely, pandas

Ürettiği çıktılar:

- `sekiller/sekil_01_nokta_dagilimi.png`
- `ciktilar/tablo_01_litoloji_ozeti.csv`
- `veri/islenmis/saha_noktalari.gpkg`

### 02 - Raster ve uydu görüntüsü

Sayısal yükseklik modelini okur, metrik sisteme projeksiyonlar, eğim ve
bakı hesaplar, gölgeli kabartma üretir ve saha noktalarının altındaki
piksel değerlerini okuyup arazi ölçümüyle karşılaştırır.

Kullanılan paketler: rasterio, numpy, geopandas

Ürettiği çıktılar:

- `sekiller/sekil_02_arazi_degiskenleri.png`
- `ciktilar/tablo_02_nokta_yukseklik_karsilastirma.csv`
- `veri/islenmis/egim.tif`, `bakis.tif`, `golge.tif`

Betiğin sonunda, çok bantlı uydu görüntüsünden NDVI hesaplamayı gösteren
yorumlanmış bir bölüm bulunur.

### 03 - Sismoloji zaman serisi

Üç bileşenli bir sismogram okur, ön işleme uygular, bant geçirgen süzgeç
uygular, genlik spektrumu ve spektrogram üretir.

Kullanılan paketler: obspy, numpy

Ürettiği çıktılar:

- `sekiller/sekil_03_dalga_formu.png`
- `sekiller/sekil_04_spektrogram.png`
- `veri/islenmis/sismogram_suzulmus.mseed`

Varsayılan olarak obspy ile gelen örnek kaydı kullanır, yani internet
bağlantısı olmadan çalışır. Gerçek veri çekmek için:

```bash
python analizler/03_sismoloji_zaman_serisi.py --cevrimici
```

---

## Makale taslağı

`makale/makale.qmd` dosyası, analizlerin ürettiği şekilleri doğrudan
kullanan bir Quarto belgesidir. Şekiller `sekiller/` klasöründen okunur,
kaynakça `makale/kaynaklar.bib` dosyasından gelir.

Derlemek için:

```bash
quarto render makale/makale.qmd --to pdf
quarto render makale/makale.qmd --to docx
```

Quarto kurulu değilse Pandoc da iş görür:

```bash
pandoc makale/makale.qmd -o makale/makale.docx --citeproc \
  --bibliography=makale/kaynaklar.bib
```

Not: Pandoc, Quarto'nun çapraz gönderme biçimini (`@fig-noktalar` gibi)
tanımaz ve bunları çözülemeyen kaynak olarak uyarır. Şekil ve tablo
numaralarının otomatik çalışması için Quarto kullanın.

Bunun faydası şudur: analizi yeniden çalıştırdığınızda şekiller güncellenir
ve makaleyi yeniden derlediğinizde yeni şekiller otomatik olarak yerine
geçer. Şekli elle Word'e yapıştırmak zorunda kalmazsınız.

---

## Kendi projenize uyarlama

1. `kod/ayarlar.py` dosyasında `CRS_METRIK` değerini çalışma alanınızın
   UTM dilimine göre değiştirin. Türkiye için 35N, 36N veya 37N.
2. `analizler/00_ornek_veri_uret.py` betiğini silin.
3. Kendi verinizi `veri/ham/` klasörüne koyun.
4. `veri/VERI_SOZLUGU.md` dosyasını kendi sütunlarınızla doldurun.
5. İhtiyacınız olmayan analiz betiklerini silin.
6. `CITATION.cff` dosyasındaki isim, kurum ve ORCID alanlarını doldurun.
7. `README.md` dosyasının bu bölümünü silip yerine kendi projenizin
   açıklamasını yazın.

---

## Veri ve kod lisansı ayrımı

Kod ve veri farklı lisanslar ister. Bu depoda:

- **Kod**: MIT Lisansı (`LICENSE` dosyası). İzin verici, kullanımı kolay.
- **Veri**: Kendi verinizi paylaşacaksanız CC BY 4.0 gibi bir veri lisansı
  seçip `veri/LISANS.md` dosyasında belirtin. Kod lisansı veriyi kapsamaz.

Kurumunuzun veya proje fonunuzun veri paylaşımına dair kuralları varsa
onlar önceliklidir. Paylaşmadan önce kontrol edin.

---

## Veriyi depoya koymayın

`.gitignore` dosyası, büyük veri dosyalarını git dışında tutacak şekilde
ayarlanmıştır. Bunun nedeni git'in ikili dosyalarda kötü çalışmasıdır:
100 MB'lık bir GeoTIFF'i beş kez güncellerseniz depo 500 MB olur ve
küçültmenin kolay yolu yoktur.

Veriyi nerede tutmalı:

| Veri boyutu | Nerede tutulur |
|---|---|
| 10 MB altı | Doğrudan depoda tutulabilir |
| 10 MB - 100 MB | Git LFS veya harici bağlantı |
| 100 MB üstü | Zenodo, Figshare veya kurumsal veri deposu; depoda sadece indirme betiği |

Zenodo'ya yüklenen veri kalıcı bir DOI alır ve makalede kaynak olarak
gösterilebilir. GitHub deposunu Zenodo'ya bağlarsanız her sürüm otomatik
olarak arşivlenir.

---

## Alıntı

Bu depo Zenodo'da arşivlenmiştir ve kalıcı bir DOI numarası taşır.

**Önerilen alıntı:**

> Şentürk, M. (2026). *Yer Bilimleri Araştırma Deposu İskeleti* (sürüm 1.0.0)
> [Yazılım]. Zenodo. https://doi.org/10.5281/zenodo.21722688

### İki DOI arasındaki fark

Zenodo her depoya iki numara verir. Hangisini kullanacağınız amacınıza bağlıdır.

| DOI | Neyi gösterir | Ne zaman kullanılır |
|---|---|---|
| `10.5281/zenodo.21722688` | Bütün sürümler | Genel atıf. Her zaman en son sürüme yönlendirir. |
| `10.5281/zenodo.21722689` | Yalnızca sürüm 1.0.0 | Tam olarak hangi sürümü kullandığınızı belirtmeniz gerektiğinde. |

Makalenizde hangi sürümü kullandığınız sonucu etkiliyorsa ikinci numarayı
verin. Bu, hakemin sizin çalıştırdığınız kodun aynısına erişmesini sağlar.

GitHub, `CITATION.cff` dosyasını okuyup depo sayfasında "Cite this repository"
düğmesi gösterir. Oradan APA ve BibTeX biçimlerini hazır alabilirsiniz.

---

## Sonraki adımlar

Depo çalışır hale geldikten sonra sırasıyla şunlar önerilir:

1. **Sürüm etiketleme.** Makaleyi gönderdiğiniz andaki hali için bir
   sürüm etiketi oluşturun (`git tag v1.0`). Hakem düzeltmesi geldiğinde
   o hale geri dönebilirsiniz.
2. **Zenodo bağlantısı.** Depoyu Zenodo'ya bağlayın, kalıcı DOI alın ve
   makalede kaynak gösterin.
3. **Ortam dosyasını dondurun.** Makale gönderiminden hemen önce
   `pip freeze > gereksinimler_kilitli.txt` çalıştırıp tam sürümleri
   kaydedin.
4. **Test ekleyin.** Kritik fonksiyonlar için basit testler yazın. Bir
   koordinat dönüşümünün doğru çalıştığını doğrulayan üç satırlık bir test
   bile, aylar sonra fark edilmeyecek bir hatayı yakalar.
