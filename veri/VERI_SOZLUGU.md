# Veri Sözlüğü

Bu dosya, `veri/ham/` klasöründeki her dosyanın ne olduğunu ve her sütunun
ne anlama geldiğini tanımlar.

Neden gerekli: altı ay sonra `egim_2` sütununun derece mi yüzde mi olduğunu
hatırlamazsınız. Hakem de sormaz, ama siz kendinize sorarsınız. Bu dosyayı
veriyi topladığınız gün doldurun, sonraya bırakmayın.

Aşağıdaki içerik örnek veriye aittir. Kendi verinizle değiştirin.

---

## saha_noktalari.csv

**Ne içerir:** Arazi ölçüm noktalarının konumu ve yapısal ölçümleri.

**Nasıl toplandı:** [Örnek veridir, yapay olarak üretilmiştir. Gerçek
projede burayı doldurun: hangi tarihlerde, hangi cihazla, kaç kişiyle,
hangi yöntemle toplandı.]

**Kayıt sayısı:** 60

**Koordinat sistemi:** EPSG:4326 (WGS 84, coğrafi koordinatlar)

| Sütun | Tip | Birim | Açıklama |
|---|---|---|---|
| `nokta_no` | metin | yok | Nokta kimliği. N-001 biçiminde, tekrar etmez. |
| `boylam` | ondalık | derece | Doğu boylamı. Pozitif değer doğuyu gösterir. |
| `enlem` | ondalık | derece | Kuzey enlemi. Pozitif değer kuzeyi gösterir. |
| `yukseklik_m` | ondalık | metre | Arazide GPS ile ölçülen deniz seviyesinden yükseklik. |
| `litoloji` | metin | yok | Gözlenen kaya türü. Kabul edilen değerler aşağıda. |
| `tabaka_dogrultu_derece` | tam sayı | derece | Tabaka doğrultusu, kuzeyden saat yönünde. 0-359 arası. |
| `tabaka_egim_derece` | tam sayı | derece | Tabaka eğimi, yataydan ölçülür. 0-90 arası. |
| `ornek_alindi` | mantıksal | yok | Bu noktadan laboratuvar örneği alındı mı. |

**`litoloji` sütununun alabileceği değerler:**

- `kirectasi` - Kireçtaşı
- `kumtasi` - Kumtaşı
- `marn` - Marn
- `andezit` - Andezit
- `alüvyon` - Alüvyon

**Bilinen sınırlar:**

- [Örnek veri yapay olduğu için jeolojik olarak tutarlı değildir.]
- [Gerçek projede burayı doldurun: eksik ölçümler, şüpheli değerler,
  ölçüm belirsizliği, erişilemeyen alanlar.]

---

## sayisal_yukseklik.tif

**Ne içerir:** Çalışma alanını kapsayan sayısal yükseklik modeli.

**Kaynak:** [Örnek veridir, yapay olarak üretilmiştir. Gerçek projede
burayı doldurun: SRTM, ASTER GDEM, Copernicus DEM, HGM verisi veya
kendi ürettiğiniz model. İndirme tarihi ve sürümü de yazın.]

**Koordinat sistemi:** EPSG:4326 (WGS 84)

**Boyut:** 400 satır x 500 sütun

**Piksel boyutu:** 0.001 derece (ekvatorda yaklaşık 111 m, bu enlemde
doğu batı yönünde yaklaşık 88 m)

**Bant:**

| Bant | Ad | Birim | Açıklama |
|---|---|---|---|
| 1 | `yukseklik_metre` | metre | Deniz seviyesinden yükseklik |

**Boşluk değeri:** -9999.0

**Bilinen sınırlar:**

- [Gerçek projede burayı doldurun: dikey doğruluk, bulut maskesi,
  boşluk doldurma yöntemi, kaynak verinin tarihi.]

---

## Yeni veri eklerken

Her yeni dosya için aynı başlıkları doldurun:

1. Ne içerir
2. Nasıl toplandı veya nereden indirildi (tarih ve sürüm dahil)
3. Kayıt veya piksel sayısı
4. Koordinat sistemi
5. Sütun veya bant tablosu (ad, tip, birim, açıklama)
6. Kategorik sütunların alabileceği değerler
7. Bilinen sınırlar ve eksikler

Yedinci madde en çok atlanan ama en değerli olanıdır. Verinizin
zayıf yanlarını yazmak, hakem sürecinde savunma yazmaktan kolaydır.
