# Windows'ta Kurulum ve Çalıştırma

README'deki komutlar Linux ve macOS içindir. Windows'ta iki fark vardır ve
bu dosya onları anlatır.

---

## İki fark

**1. `make` komutu yoktur.** `make` bir Linux aracıdır. Windows'ta karşılığı
olarak depoda `calistir.bat` dosyası bulunur.

| Linux ve macOS | Windows |
|---|---|
| `make tumu` | `.\calistir.bat` |
| `make temiz` | `.\calistir.bat temiz` |

**2. Sanal ortamı etkinleştirmeye gerek yoktur.** PowerShell varsayılan
olarak betik çalıştırmayı engeller. Bu ayarla uğraşmak yerine sanal
ortamdaki Python'u doğrudan çağırıyoruz:

```
.venv\Scripts\python.exe analizler\01_vektor_saha_verisi.py
```

Bu yol, `Activate.ps1` ile etkinleştirmekle aynı sonucu verir ve hiçbir
sistem ayarına dokunmaz.

---

## Sıfırdan kurulum

PowerShell'i açın ve komutları **tek tek** yapıştırın. Birden fazla satırı
aynı anda yapıştırmak komutların birleşmesine ve hataya yol açar.

### 1. Depoyu indirin

```
cd $HOME\Documents
git clone https://github.com/geomuratsenturk-dotcom/jeobilim-arastirma-iskeleti.git
cd jeobilim-arastirma-iskeleti
```

### 2. Python sürümünü kontrol edin

```
py --list
```

Listede 3.11 veya 3.12 görmelisiniz. Yoksa https://www.python.org/downloads/
adresinden kurun.

### 3. Sanal ortam oluşturun

```
py -3.12 -m venv .venv
```

Bu komut başarılı olduğunda hiçbir şey yazmaz. Sessizlik iyi haberdir.

### 4. Paketleri kurun

```
.venv\Scripts\python.exe -m pip install --upgrade pip
```

```
.venv\Scripts\python.exe -m pip install -r gereksinimler.txt
```

İkincisi birkaç dakika sürer. Sonunda "Successfully installed" satırını
görmelisiniz.

### 5. Analizleri çalıştırın

```
.\calistir.bat
```

Dört betik sırayla çalışır. Sonunda `sekiller\` klasöründe dört PNG,
`ciktilar\` klasöründe iki CSV oluşur.

---

## Sık karşılaşılan sorunlar

**"calistir.bat is not recognized"**

Başına `.\` koymayı unutmuşsunuzdur. PowerShell, bulunduğu klasördeki
dosyaları güvenlik gereği doğrudan çalıştırmaz.

```
.\calistir.bat
```

**"HATA: Sanal ortam bulunamadi"**

3. ve 4. adımları atlamışsınızdır. Sırayla yapın.

**Komutlar birleşiyor ve tuhaf hata veriyor**

Birden fazla satırı aynı anda yapıştırdınız. PowerShell bunları tek komut
sanır. Her satırı ayrı ayrı yapıştırıp Enter'a basın.

**"python is not recognized"**

Python kurulu değil ya da PATH'e eklenmemiş. Kurulum sırasında
"Add Python to PATH" kutusunu işaretlemek gerekir. Kurulumu tekrarlayıp
o kutuyu işaretleyin.

**Türkçe karakterler bozuk görünüyor**

Windows Terminal kullanın, eski komut istemini değil. Windows 11'de
varsayılan olarak Windows Terminal gelir.

**Rasterio veya GeoPandas kurulmuyor**

Nadir bir durumdur, çünkü ikisi de artık GDAL'i içine gömülü Windows
paketleri yayımlıyor. Yine de takılırsanız Miniforge kurup conda yolunu
deneyin: https://github.com/conda-forge/miniforge

```
conda env create -f ortam.yml
conda activate jeobilim
```

---

## Çalıştığını nasıl doğrularsınız

Analizler bittiğinde ekranda şu değerleri görmelisiniz:

```
En yakin komsu mesafesi: ortalama 3244 m, en kucuk 572 m, en buyuk 6738 m
Egim: ortalama 3.1 derece, en yuksek 11.4 derece
Arazi olcumu ile model farki: ortalama +78.1 m, mutlak ortalama 115.6 m
```

Bu sayılar her işletim sisteminde ve her Python sürümünde aynı çıkar.
Farklı çıkarsa bir yerde tohum sabitleme atlanmış demektir.

Bu, iskeletin en önemli özelliğidir. Sonuçlarınızın makineden makineye
değişmemesi, hakem sürecinde "tekrarlayamadım" itirazının önünü keser.
