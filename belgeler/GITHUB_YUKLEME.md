# Depoyu GitHub'a Yükleme

Bu kılavuz, hesabınızda henüz depo olmadığı varsayımıyla yazılmıştır.
Adımları sırayla izleyin.

---

## 1. Git kurulumu ve kimlik ayarı

Git kurulu değilse: <https://git-scm.com/downloads>

Kurulumdan sonra kimliğinizi bir kez ayarlayın. Bu bilgi her katkı
kaydına işlenir.

```bash
git config --global user.name "Adiniz Soyadiniz"
git config --global user.email "eposta@kurum.edu.tr"
```

GitHub hesabınızdaki e-posta adresiyle aynı olmasına dikkat edin.
Farklı olursa katkılarınız profilinizde görünmez.

---

## 2. GitHub'da boş bir depo oluşturun

1. <https://github.com/new> adresine gidin.
2. **Repository name**: proje adınızı yazın. Küçük harf ve tire kullanın,
   boşluk kullanmayın. Örnek: `menderes-grabeni-analiz`
3. **Description**: bir cümlelik açıklama yazın.
4. **Public** veya **Private** seçin. Makale yayımlanana kadar Private
   tutup sonra Public yapmak yaygın bir yaklaşımdır.
5. **Önemli**: "Add a README file", "Add .gitignore" ve "Choose a license"
   kutularının hiçbirini işaretlemeyin. Bu dosyalar zaten iskelette var.
   İşaretlerseniz çakışma çıkar.
6. **Create repository** düğmesine basın.

Açılan sayfada size bir adres gösterilir. Şuna benzer:

```
https://github.com/kullanici-adiniz/menderes-grabeni-analiz.git
```

Bu adresi kopyalayın.

---

## 3. Yerel klasörü depoya bağlayın

Proje klasörünüzün içinde terminal açın ve sırayla çalıştırın:

```bash
# Git deposunu başlat
git init

# Bütün dosyaları hazırlığa al
git add .

# Neyin ekleneceğini kontrol edin
git status
```

`git status` çıktısında `veri/ham/` içindeki büyük dosyaları
**görmemelisiniz**. Görüyorsanız `.gitignore` dosyası devreye girmemiş
demektir. Devam etmeden önce kontrol edin.

```bash
# İlk katkı kaydını oluştur
git commit -m "İlk sürüm: analiz iskeleti ve örnek veri"

# Ana dalın adını main yap
git branch -M main

# Uzak depoyu bağla (adresi kendi adresinizle değiştirin)
git remote add origin https://github.com/kullanici-adiniz/menderes-grabeni-analiz.git

# Gönder
git push -u origin main
```

İlk `push` sırasında GitHub kimlik doğrulaması ister. Parola yerine
kişisel erişim jetonu (personal access token) kullanmanız gerekir.

---

## 4. Kişisel erişim jetonu oluşturma

GitHub 2021'den beri parola ile git erişimini kabul etmiyor.

1. <https://github.com/settings/tokens> adresine gidin.
2. **Generate new token** > **Generate new token (classic)** seçin.
3. **Note** alanına tanımlayıcı bir ad yazın: "dizustu bilgisayar"
4. **Expiration** için 90 gün veya daha uzun seçin.
5. **Select scopes** bölümünde yalnızca **repo** kutusunu işaretleyin.
6. **Generate token** düğmesine basın.
7. Çıkan jetonu kopyalayın. **Bu jeton bir daha gösterilmez.**

`git push` sırasında kullanıcı adı sorulduğunda GitHub kullanıcı adınızı,
parola sorulduğunda bu jetonu yapıştırın.

Jetonu her seferinde yazmamak için kaydedin:

```bash
# macOS
git config --global credential.helper osxkeychain

# Windows
git config --global credential.helper manager

# Linux
git config --global credential.helper store
```

Alternatif olarak GitHub CLI kullanabilirsiniz; kimlik doğrulamayı
kendisi halleder: <https://cli.github.com/>

---

## 5. Günlük kullanım

Çalışmaya devam ederken üç komut yeterlidir:

```bash
git add .
git commit -m "Ne yaptığınızı bir cümleyle yazın"
git push
```

### İyi katkı mesajı nasıl yazılır

Kötü: `guncelleme`, `duzeltme`, `asdf`

İyi:

- `Egim hesabinda piksel boyutu duzeltildi`
- `Sekil 2'ye golgeli kabartma paneli eklendi`
- `Litoloji ozet tablosuna standart sapma eklendi`

Ölçüt şu: altı ay sonra bu satırı okuyunca ne yaptığınızı anlamalısınız.

### Ne sıklıkla kaydetmeli

Bir işi bitirdiğinizde. Günde bir kez değil, mantıklı bir birim
tamamlandığında. "Şekil 2 artık doğru çalışıyor" bir birimdir.

---

## 6. Sürüm etiketleme

Makaleyi dergiye gönderdiğiniz anda o hali etiketleyin:

```bash
git tag -a v1.0 -m "Dergiye gonderilen surum"
git push origin v1.0
```

Hakem düzeltmesi geldiğinde o hale geri dönebilirsiniz. Bu, "hakem
şekil 3'ü soruyor ama ben o zamandan beri kodu değiştirdim" durumunun
çözümüdür.

---

## 7. Zenodo bağlantısı ve DOI

Depoya kalıcı bir DOI vermek, makalede kaynak gösterebilmenizi sağlar.

1. <https://zenodo.org> adresinde GitHub hesabınızla giriş yapın.
2. Üst menüden hesap ayarlarına, oradan **GitHub** bölümüne gidin.
3. Listeden deponuzu bulun ve anahtarı **On** konumuna getirin.
4. GitHub'a dönün, deponuzda **Releases** bölümüne gidin.
5. **Create a new release** ile bir sürüm yayımlayın (örneğin `v1.0`).
6. Zenodo bu sürümü otomatik arşivler ve bir DOI verir.
7. DOI'yi `CITATION.cff` ve `README.md` dosyalarına ekleyin.

Bu adımı makale gönderiminden **önce** yapın. Hakem sürecinde "kod
nerede" sorusuna hazır bir cevabınız olur.

---

## Kontrol listesi

Depoyu ilk kez yüklemeden önce:

- [ ] `.gitignore` çalışıyor, büyük veri dosyaları listede görünmüyor
- [ ] `LICENSE` dosyasındaki isim alanı dolduruldu
- [ ] `CITATION.cff` dosyasındaki köşeli parantezli alanlar dolduruldu
- [ ] `README.md` dosyası kendi projenizi anlatıyor
- [ ] Şifre, API anahtarı veya kişisel veri içeren dosya yok
- [ ] `make tumu` komutu temiz bir klondan sorunsuz çalışıyor

Son madde en önemlisidir. Depoyu başka bir klasöre klonlayıp analizleri
baştan çalıştırın. Çalışmıyorsa eksik bir dosya veya bağımlılık var
demektir; başkası da çalıştıramaz.
