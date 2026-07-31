# Ham veri klasörü

Bu klasöre bir kez yazılır, bir daha değiştirilmez.

## Kural

Buradaki dosyalara elle dokunmayın. Bir hücreyi düzeltmek, bir satırı
silmek, bir sütun adını değiştirmek gerekiyorsa bunu bir betikle yapın ve
sonucu `veri/islenmis/` klasörüne yazın.

Nedeni şudur: ham veriyi elle düzenlediğinizde, o düzenlemenin kaydı
hiçbir yerde kalmaz. Altı ay sonra sonucunuz farklı çıktığında neyin
değiştiğini bulamazsınız.

## Ne koyulur

- Arazi ölçüm dosyaları
- İndirilen uydu görüntüleri ve yükseklik modelleri
- Laboratuvar analiz sonuçları
- Kurumlardan alınan veri dosyaları

## Ne koyulmaz

- Betiklerin ürettiği ara dosyalar (bunlar `veri/islenmis/` klasörüne gider)
- Elle temizlenmiş veri sürümleri
- Geçici çalışma dosyaları

## Büyük dosyalar

`.gitignore` dosyası bu klasörün içeriğini git dışında tutar. Bu bilinçli
bir tercihtir. Veriniz 10 MB'den büyükse depoya koymayın. Bunun yerine:

1. Veriyi Zenodo veya Figshare'a yükleyin, kalıcı DOI alın.
2. Bu klasöre veriyi indiren kısa bir betik koyun.
3. `veri/VERI_SOZLUGU.md` dosyasına indirme bağlantısını yazın.

Örnek indirme betiği:

```python
# veri/ham/veri_indir.py
import urllib.request
from pathlib import Path

KAYNAKLAR = {
    "yukseklik.tif": "https://zenodo.org/records/0000000/files/yukseklik.tif",
}

for dosya_adi, adres in KAYNAKLAR.items():
    hedef = Path(__file__).parent / dosya_adi
    if hedef.exists():
        print(f"{dosya_adi} zaten var, atlaniyor.")
        continue
    print(f"{dosya_adi} indiriliyor...")
    urllib.request.urlretrieve(adres, hedef)
```

Böylece depoyu klonlayan biri tek komutla veriye ulaşır, deponun boyutu
küçük kalır ve verinizin kalıcı bir kaydı olur.
