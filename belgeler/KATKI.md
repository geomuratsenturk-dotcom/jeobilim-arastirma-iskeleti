# Katkı ve Çalışma Kuralları

Bu dosya iki işe yarar: birlikte çalıştığınız kişilere kuralları anlatır,
ve kendi kendinize koyduğunuz kuralları hatırlatır. Tek başınıza
çalışıyorsanız bile ikinci işlev değerlidir.

---

## Değişmez kurallar

1. **Ham veriye dokunulmaz.** `veri/ham/` klasöründeki hiçbir dosya elle
   düzenlenmez. Düzeltme gerekiyorsa bir betikle yapılır ve sonuç
   `veri/islenmis/` klasörüne yazılır.

2. **Her çıktı bir betikten üretilir.** `sekiller/` ve `ciktilar/`
   klasörlerine elle dosya koyulmaz. Bu klasörlerin tamamı silinip
   `make tumu` ile yeniden üretilebilmelidir.

3. **Dosya yolu elle yazılmaz.** Bütün yollar `kod/ayarlar.py`
   dosyasından gelir. Bir betikte `C:\Users\...` veya `/home/...`
   görürseniz düzeltin.

4. **Rastgelelik tohumlanır.** Rastgele sayı kullanan her işlemden önce
   `yardimcilar.tohum_sabitle()` çağrılır. Aksi halde sonuç her
   çalıştırmada değişir.

---

## Kod yazım biçimi

- Değişken ve fonksiyon adları Türkçe, küçük harf ve alt çizgi ile:
  `egim_hesapla`, `nokta_sayisi`
- Fonksiyonların ne yaptığı üç açıklama tırnağı içinde yazılır
- Bir fonksiyon tek iş yapar. Elli satırı geçiyorsa bölün
- Aynı kod iki yerde tekrar ediyorsa `kod/yardimcilar.py` dosyasına taşıyın

Biçimi otomatik düzeltmek için:

```bash
pip install ruff
ruff format .
ruff check . --fix
```

---

## Yeni analiz eklerken

Betikleri numaralandırın ve çalışma sırasını numara belirlesin:

```
analizler/04_jeokimya_diyagramlari.py
```

Her betiğin başına şu bilgileri yazın:

```python
"""
04 - Kısa başlık

Ne yapar:
    1. ...
    2. ...

Kullanılan paketler: ...

Girdi:  veri/ham/... , veri/islenmis/...
Çıktı:  sekiller/... , ciktilar/...

Çalıştırma (proje kökünden):
    python analizler/04_jeokimya_diyagramlari.py
"""
```

Girdi ve çıktıyı yazmak, aylar sonra hangi betiğin hangi dosyayı
ürettiğini aramaktan kurtarır.

---

## Değişiklik kaydı

Her anlamlı adımda kayıt oluşturun:

```bash
git add .
git commit -m "Egim hesabinda piksel boyutu duzeltildi"
```

Mesajı Türkçe yazabilirsiniz, ancak Türkçe karakter kullanmayın. Bazı
terminaller ve git araçları bunları bozuk gösterir.

---

## Birden fazla kişi çalışıyorsa

Doğrudan `main` dalına yazmayın. Her iş için bir dal açın:

```bash
git checkout -b jeokimya-analizi
# çalışın, kaydedin
git push -u origin jeokimya-analizi
```

Sonra GitHub üzerinde bir "pull request" açıp diğer kişinin bakmasını
isteyin. İki kişilik bir ekipte bile bu alışkanlık, fark edilmeyen
hataları yakalar.

---

## Yayın öncesi kontrol

Makaleyi göndermeden önce:

- [ ] Depoyu temiz bir klasöre klonlayın
- [ ] Ortamı sıfırdan kurun
- [ ] `make tumu` çalıştırın
- [ ] Üretilen şekillerin makaledekilerle aynı olduğunu doğrulayın
- [ ] `pip freeze > gereksinimler_kilitli.txt` ile sürümleri dondurun
- [ ] Sürüm etiketi oluşturun (`git tag -a v1.0`)
- [ ] Zenodo DOI'sini alın ve `CITATION.cff` dosyasına ekleyin

Birinci madde en önemlisidir. Kendi bilgisayarınızda çalışan bir
analizin başka bir bilgisayarda çalışmamasının en yaygın nedeni,
depoya girmemiş bir dosya veya kurulu olduğunu unuttuğunuz bir
paketdir.
