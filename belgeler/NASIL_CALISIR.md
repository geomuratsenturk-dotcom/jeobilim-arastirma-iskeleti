# Bu Sistem Nasıl Çalışır

Bu belge, kurduğumuz düzenin ne olduğunu ve nasıl kullanılacağını anlatır.
Komut ezberlemeniz gerekmiyor. Aşağıdaki tabloları okuyup ne yapacağınıza
karar vermeniz yeterli.

---

## Kısa cevap

Araştırmanızın üç parçası vardı ve üçü ayrı yerlerde duruyordu: veri ve
analiz kodu bir klasörde, kaynakça bir programda, makale bir Word
dosyasında. Aralarındaki bağı siz kuruyordunuz. Şekli elle kopyalıyor,
kaynağı elle yazıyor, dosyayı elle yedekliyordunuz.

Şimdi bu bağlar kurulu. Veri değişince şekiller değişiyor, şekiller
değişince makale değişiyor, gün bitince her şey yedekleniyor. Siz sadece
araştırmayı yapıyorsunuz.

---

## Beş parça ve her birinin işi

| Parça | Nerede durur | Ne yapar |
|---|---|---|
| **Proje klasörü** | Bilgisayarınızda, `Belgeler\jeobilim-arastirma-iskeleti` | Veriniz, kodunuz, şekilleriniz ve makaleniz burada durur. Asıl çalışma alanı burasıdır. |
| **Python ortamı** | Proje klasörünün içinde, `.venv` klasörü | Analizleri çalıştıran paketler burada. Sistem Python'unuzdan ayrıdır, bir projedeki paket başka projeyi etkilemez. |
| **Zotero** | Bilgisayarınızda ayrı bir program | Kaynaklarınızı tutar. Better BibTeX eklentisi, her değişiklikte `makale/zotero.bib` dosyasını yeniden yazar. |
| **GitHub** | İnternette, `github.com/geomuratsenturk-dotcom/jeobilim-arastirma-iskeleti` | Kodunuzun ve belgelerinizin yedeği ve geçmişi. Her değişikliğin kaydı burada durur. |
| **Zenodo** | İnternette, `zenodo.org/records/21722689` | Kalıcı arşiv. DOI numarası verir, makalede kaynak gösterebilirsiniz. |

---

## Nerede ne çalışıyor

**Bilgisayarınızda çalışanlar:** analizler, makale derleme, Zotero,
kaynakça dosyasının yazılması, gece yedeği görevi.

**İnternette duranlar:** GitHub deposu ve Zenodo arşivi. Bunlar bir şey
çalıştırmaz, sadece saklar.

Bilgisayarınız internetsizken de analizlerinizi çalıştırıp makale
derleyebilirsiniz. İnternet yalnızca gönderme ve alma adımlarında gerekir.

---

## Günlük kullanım: hangi durumda ne

Masaüstündeki **Jeobilim Arastirma** kısayoluna çift tıklarsınız, menü
açılır. Aşağıdaki tablo hangi durumda hangi numarayı seçeceğinizi gösterir.

| Durumunuz | Menü seçeneği | Ne olur |
|---|---|---|
| Yeni saha verisi ekledim, sonuçları güncellemek istiyorum | **1** | Analizler baştan çalışır, şekiller ve tablolar yenilenir |
| Makalenin son halini Word'de görmek istiyorum | **2** | `makale.docx` üretilir, isterseniz hemen açılır |
| Veriyi de metni de değiştirdim, hepsini yenile | **3** | Önce analizler, sonra makale. En sık kullanacağınız seçenek |
| Son kayıttan bu yana ne değişmiş, merak ediyorum | **4** | Değişen dosyaların listesi çıkar |
| Günü bitirdim, çalışmam yedeklensin | **5** | Değişiklikler GitHub'a gönderilir |
| Başka bir bilgisayarda çalışmıştım, buraya getir | **6** | GitHub'daki güncellemeler indirilir |
| Bir şeyler karıştı, üretilenleri sıfırlamak istiyorum | **7** | Şekil ve tablolar silinir, 1 numarayla geri gelir |
| Bir şey çalışmıyor, neyin eksik olduğunu göreyim | **8** | Python, git, Quarto ve Zotero dosyası kontrol edilir |

Menüden çıkmak için **0**.

---

## Siz hiçbir şey yapmadan olanlar

Üç şey kendiliğinden işler.

**Zotero'ya kaynak eklediğinizde.** Better BibTeX beş saniye içinde
`makale/zotero.bib` dosyasını yeniden yazar. Makalede o kaynağa atıf
yapmak için Zotero'da kaydı seçip sağ paneldeki **Citation Key**
satırındaki metni `[@buraya]` biçiminde yazarsınız.

**Her akşam saat 18:00'de.** Windows, değişiklikleriniz varsa GitHub'a
gönderir. Bilgisayar o saatte kapalıysa açtığınızda çalışır. Ne yaptığını
`ciktilar\yedek_gunlugu.txt` dosyasına yazar. Değişiklik yoksa hiçbir şey
yapmaz.

**Sürüm yayımladığınızda.** GitHub'da yeni bir sürüm (release)
oluşturursanız Zenodo onu arşivleyip yeni bir DOI verir. Bunu makaleyi
dergiye gönderdiğiniz gün yapmanız önerilir; hakem düzeltmesi geldiğinde
tam o hale geri dönebilirsiniz.

---

## Makale yazarken üç kural

**Şekli elle kopyalamayın.** Makale, şekilleri `sekiller/` klasöründen
okur. Analizi yeniden çalıştırdığınızda makale de güncellenir.

**Kaynağı elle yazmayın.** Zotero'ya ekleyin, `[@atifanahtari]` biçiminde
kullanın. Kaynakça listesi kendiliğinden oluşur.

**Ham veriye dokunmayın.** `veri/ham/` klasöründeki dosyalar
değiştirilmez. Düzeltme gerekiyorsa bir betikle yapılır. Bu kural,
aylar sonra "ben bu sayıyı nereden aldım" sorusunu cevaplanabilir kılar.

---

## Kendi verinizle başlarken

Örnek veriden kendi verinize geçerken sırasıyla:

1. `kod/ayarlar.py` dosyasında `CRS_METRIK` değerini çalışma alanınızın
   UTM dilimine göre değiştirin. Isparta çevresi için `EPSG:32636`,
   batıda kalan alanlar için `EPSG:32635`.
2. `analizler/00_ornek_veri_uret.py` betiğini silin. Yapay veri üretiyordu,
   artık gerekmez.
3. Kendi dosyalarınızı `veri/ham/` klasörüne koyun.
4. `veri/VERI_SOZLUGU.md` dosyasını kendi sütunlarınızla doldurun. Bu
   dosyayı veriyi topladığınız gün doldurun, sonraya bırakmayın.
5. Analiz betiklerini kendi verinize göre uyarlayın.

---

## Bir şey ters giderse

**Önce menüden 8'i seçin.** Hangi bileşenin eksik olduğunu söyler.

**Analiz hata verdi.** Ekrandaki mesajı okuyun, sorun genellikle orada
yazılıdır. Anlaşılmıyorsa mesajı olduğu gibi kopyalayın.

**Makale derlenmiyor.** Genellikle `makale.qmd` dosyasının en üstündeki
ayar bloğunda bir yazım hatası vardır. Quarto hangi satırda sorun
olduğunu söyler.

**Gece yedeği çalışmamış.** `ciktilar\yedek_gunlugu.txt` dosyasını açın,
son satırlar ne olduğunu anlatır. Kimlik doğrulaması istendiyse menüden
5'i seçip elle gönderin, bir kez giriş yapınca düzelir.

**Zotero kaynakçası güncellenmiyor.** Zotero'nun açık olduğundan emin
olun. Kapalıyken dosyayı yazamaz.

---

## Yardımcı belgeler

| Dosya | İçerik |
|---|---|
| `README.md` | Deponun genel tanıtımı ve klasör yapısı |
| `belgeler/KURULUM.md` | Sıfırdan kurulum adımları |
| `belgeler/WINDOWS.md` | Windows'a özel farklar ve sorun çözümleri |
| `belgeler/GITHUB_YUKLEME.md` | GitHub'a yükleme ve kimlik doğrulama |
| `belgeler/KATKI.md` | Çalışma kuralları ve yayın öncesi kontrol listesi |
| `veri/VERI_SOZLUGU.md` | Verinizin ne olduğunu anlatan sözlük |
