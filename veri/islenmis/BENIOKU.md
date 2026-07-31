# İşlenmiş veri klasörü

Bu klasördeki her dosya bir betikten üretilir. Tamamını silseniz bile
kaybınız olmaz:

```bash
make tumu
```

komutu hepsini yeniden üretir.

## Buraya ne yazılır

- Koordinat sistemi dönüştürülmüş vektör katmanları
- Yeniden projeksiyonlanmış raster dosyaları
- Eğim, bakı, gölgeli kabartma gibi türetilmiş katmanlar
- Süzgeçten geçirilmiş sismik kayıtlar
- Temizlenmiş ve birleştirilmiş tablolar

## Buraya elle dosya koyulmaz

Elle koyduğunuz bir dosya, `make temiz` komutunda silinir ve geri gelmez.
Kaynak veriniz varsa `veri/ham/` klasörüne koyun.

## Neden git'e girmiyor

`.gitignore` dosyası bu klasörün içeriğini git dışında tutar. Nedeni,
bu dosyaların zaten yeniden üretilebilir olmasıdır. Git'e koymak depoyu
gereksiz yere büyütür ve her çalıştırmada anlamsız değişiklik kaydı
oluşturur.
