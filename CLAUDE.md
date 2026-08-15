# CLAUDE.md

Bu dosya, depoda çalışan Claude Code oturumları için kılavuzdur.

**Ürün:** Deprem Haklarım — deprem öncesi ve sonrasındaki hakları, dayandığı
kanun maddesiyle birlikte ve **süresi geçmeden önce** anlatan ücretsiz bilgi
platformu. Ekip: T8 Hasar Tespiti · Claude Impact Lab.

---

## 1. En önemli kural: hiçbir hukuki bilgi doğrulanmadı

`DOGRULAMA.md` 71 kalemlik bir doğrulama görev listesidir ve **tamamlanmadı.**
Geliştirme ortamının ağ politikası `mevzuat.gov.tr`, `resmigazete.gov.tr` ve
`dask.gov.tr` erişimini engelledi. Bu yüzden:

- **Hiçbir madde numarasını, süreyi veya tutarı "kesin" diye sunmayın.**
  Metinlerde "belirtilmektedir", "kabul edilmektedir" gibi çekinceli dil
  bilinçlidir; düzeltme değildir.
- Yeni içerik yazarken kaynağın doğrulama durumunu (`resmi` / `coklu` / `tek` /
  `celiskili`) mutlaka taşıyın.
- Parasal değerler **metne gömülmez**; `data/parametreler.json` kanonik
  kaynaktır. DASK azami teminatı 2026'da aylık güncelleniyor — bir sayfaya
  sabit rakam yazmak o sayfayı bir ay içinde yanlış hâle getirir.

## 2. Dokunulmayacak alanlar

Kullanıcı isteği üzerine **site kökündeki elle yazılmış sayfalar rehber
çalışmasının kapsamı dışındadır**:

```
docs/index.html  docs/sureler.html  docs/haklarim.html
docs/teminat.html  docs/dilekce.html  docs/assets/tasarim.css
```

Bunlar rehber (blog) işi sırasında değiştirilmedi ve açık talimat olmadıkça
değiştirilmemeli. Rehbere özgü stiller `docs/blog/rehber.css` içinde durur;
ana tasarım sistemine eklenmez.

`docs/assets/app.js` içindeki tek ekleme geriye dönük uyumludur:
`iskelet({ kok })` — varsayılan `"./"`, rehber sayfaları `"../"` gönderir.
Mevcut sayfaların davranışı değişmedi.

---

## 3. Depo haritası

| Yol | İçerik |
|---|---|
| `docs/` | Yayımlanan statik site (GitHub Pages, derleme adımı yok) |
| `docs/blog/` | **Rehber bölümü** — 20 yazı, dizin, RSS, site haritası, kendi CSS'i |
| `docs/assets/` | `tasarim.css`, `app.js`, `veri.js`, `og.png` (paylaşım görseli) |
| `data/parametreler.json` | Tarih damgalı, sürümlü parametreler (kanonik) |
| `scripts/blog-uret.py` | Rehber üreteci — `docs/blog/*` dosyalarını yazar |
| `scripts/yazilar/*.py` | **Rehber yazılarının kaynağı** (her dosyada bir `YAZI` sözlüğü) |
| `scripts/sekiller.py` | Yazı başına SVG şema tanımı (slug → şema) |
| `scripts/gorseller.py` | Şema çizen SVG kütüphanesi (5 tip) |
| `scripts/foto-indir.py` | Pexels'ten açılış fotoğraflarını indirir/küçültür |
| `scripts/foto-kunye.json` | Fotoğraf künyeleri (üretilir, repoda durur) |
| `scripts/seo-kontrol.py` | Rehber sayfaları için SEO/erişilebilirlik denetimi |
| `scripts/veri-kontrol.py` | `parametreler.json` ↔ `veri.js` tutarlılığı |
| `scripts/og-kaynak.svg` | `docs/assets/og.png` görselinin kaynağı |
| `PROJE-LEGAL.md` | Hukuki altyapı — rehber içeriğinin ana kaynağı |
| `PROJE-AKIS.md` | Kiracının korunması, tek pencere modeli |
| `PROJE-PARAMETRIK.md` | Parametrik kiracı ürünü, DASK protokolü |
| `DOGRULAMA.md` | 🔴 Doğrulama görev listesi |
| `TASARIM.md` | Tasarım sistemi ve kriz UX kararları |

---

## 4. Rehber (blog) nasıl çalışır?

**`docs/blog/*.html` dosyaları üretilmiştir — elle düzenlemeyin.** Kaynak
`scripts/yazilar/` altındadır; değişiklikten sonra üreteci çalıştırın:

```bash
python3 scripts/blog-uret.py            # üret
python3 scripts/blog-uret.py --kontrol  # üretilen dosyalar güncel mi? (CI için)
python3 scripts/seo-kontrol.py          # SEO + erişilebilirlik denetimi
```

Neden üreteç var: 20 yazının her birinde ~60 satırlık SEO başlığı (canonical,
Open Graph, Twitter, JSON-LD, kırıntı yolu, içindekiler) elle yazılırsa
tutarlılık ilk güncellemede bozulur. Üretilen HTML depoya işlenir; tarayıcı
hiçbir şey derlemez, sitenin "derleme adımı yok" ilkesi korunur.

### Yeni yazı eklemek

`scripts/yazilar/NN-slug.py` oluşturun (dosya adındaki numara kategori içi
sırayı belirler) ve `YAZI` sözlüğünü doldurun:

| Alan | Kural |
|---|---|
| `slug` | yalnızca `a-z0-9-`; dosya adı `<slug>.html` olur |
| `seoBaslik` | `<title>` — **25-60 karakter**, anahtar kelime başta |
| `baslik` | sayfadaki `<h1>`, uzun olabilir |
| `aciklama` | meta description — **120-158 karakter** |
| `ozet` | düz metin (HTML yok); listede, RSS'te ve girişte kullanılır |
| `kategori` | `blog-uret.py` içindeki `KATEGORILER` listesinden biri |
| `anahtar` | en az 3; `article:tag` ve JSON-LD `keywords` olur |
| `sss` | en az 3 soru-cevap → görünür bölüm + `FAQPage` işaretlemesi |
| `ilgili` | en az 1 başka yazının slug'ı (iç bağlantı ağı) |
| `dayanaklar` | kanun/madde künyeleri → görünür liste + JSON-LD `citation` |
| `sure` | (isteğe bağlı) sayfa başındaki kırmızı süre kartı |
| `araclar` | (isteğe bağlı) `(href, ad, açıklama)` üçlüleri |
| `govde` | HTML; **her `<h2>` bir `id` taşımalı** (içindekiler ondan üretilir) |

Üreteç bu kuralları **yazma anında zorlar**: kural ihlali varsa dosya
yazılmaz, hata listesi basılır. Ayrıca gövde ≥ 550 ve toplam ≥ 750 kelime
şartı vardır (Türkçe eklemeli bir dil olduğu için eşikler İngilizceye göre
düşüktür).

### Yazı gövdesinde kullanılacak sınıflar

Tasarım sistemi sınıfları (`TASARIM.md` Bölüm 6): `.kart` + `.vurgulu` /
`.uyarili` / `.tehlikeli` / `.bilgili`, `.dayanak`, `.serit`, `.etiket`,
`.tablo-sar` (her `<table>` bunun içinde ve bir `<caption class="sr">` ile),
`.rozet`. Rehbere özgü olanlar `docs/blog/rehber.css` içinde: `.kirinti`,
`.icindekiler`, `.yazi`, `.yazi-bilgi`, `.sss`, `.dayanak-liste`,
`.ilgili-liste`, `.etiketler`.

### Görseller: her yazıda bir fotoğraf + bir şema

**1. Açılış fotoğrafı** (`docs/blog/gorseller/<slug>.jpg`, 1200×627)

Kaynak Pexels'tir; Pexels lisansı ücretsiz kullanıma izin verir ve atıf zorunlu
değildir, yine de her fotoğrafın altında fotoğrafçı künyesi vardır. Fotoğraflar
**uzaktan bağlanmaz, indirilir** — aksi hâlde okuyucunun IP adresi üçüncü tarafa
gider ve sitenin "dış istek yok" ilkesi bozulur.

```bash
export PEXELS_ANAHTAR="..."               # pexels.com/api · repoya YAZILMAZ
python3 scripts/foto-indir.py             # eksikleri indir
python3 scripts/foto-indir.py --yenile <slug>   # beğenilmeyeni değiştir
```

Arama sorguları ve Türkçe `alt` metinleri `scripts/foto-indir.py` içindeki
`ARAMALAR` sözlüğündedir. Fotoğraf 1200 piksele küçültülür ve 160 kB'ı aşarsa
daha düşük kalitede yeniden sıkıştırılır; ayrıca rehber dizini kartları için
360 piksellik kopya üretilir. Her fotoğraf aynı zamanda o yazının
`og:image`'ıdır.

> **Yayımlamadan önce fotoğrafı gözle kontrol edin.** Stok aramaları krize
> uygun olmayan sonuçlar döndürebilir (ör. "taşınma" sorgusunda gülümseyen
> kişi). Ton: sade, kişisiz, sansasyonsuz.

**2. Şema** (satır içi SVG, `scripts/sekiller.py` + `scripts/gorseller.py`)

Şema, yazının içindeki bir bilgiyi görselleştirir — süsleme değildir; aynı
bilgi metinde ve tablolarda da bulunur. Satır içi olmasının nedeni CSS
değişkenlerini miras alması: koyu/açık tema ve kullanıcının tema seçimi çizime
de uygulanır. Beş tip: `sure`, `kapsam`, `akis`, `karsilastirma`, `eksen`.

Yeni şema eklemek için `SEKILLER` sözlüğüne yazının slug'ıyla bir kayıt
ekleyin; anahtarlar doğrudan `gorseller.py` içindeki fonksiyonun
parametreleridir.

### Paylaşım görselini yeniden üretmek

```bash
qlmanage -t -s 1200 -o /tmp scripts/og-kaynak.svg
sips -c 630 1200 /tmp/og-kaynak.svg.png --out docs/assets/og.png
```

Kaynak SVG 1200×1200'dür ve tasarım dikeyde ortalanmıştır; `sips` ortadan
kırptığı için sonuç tam olarak 1200×630 tasarımdır.

---

## 5. SEO kuralları (rehber bölümü)

`scripts/seo-kontrol.py` her sayfada şunları denetler ve ihlalde çıkış kodu 1
döner:

- **Teknik:** `lang="tr"`, charset, viewport, tek `<h1>`, başlık atlaması yok,
  başlık ve açıklama uzunlukları, canonical (site köküyle başlamalı), robots,
  theme-color, favicon, stylesheet.
- **Paylaşım:** tüm Open Graph ve Twitter alanları; `og:url` ile canonical
  aynı olmalı; `og:image:alt` zorunlu.
- **Yapısal veri:** JSON-LD ayrıştırılabilir olmalı; `Organization` düğümü,
  `Article` zorunlu alanları, `headline` ≤ 110 karakter, `FAQPage` cevapları.
- **Erişilebilirlik:** görsellerde `alt` ve `width`/`height` (CLS), satır içi
  SVG'de `role="img"` + `aria-labelledby`, her tabloda `caption`, anlamsız
  bağlantı metni ("buraya tıklayın") yasak.
- **Görsel:** dış kaynaktan bağlanmış görsel hata sayılır; dosya diskte
  bulunmalıdır.
- **Bağlantı:** site içi bağlantıların hedefi diskte var olmalı (kırık
  bağlantı = hata).
- **Kapsam:** `blog/sitemap.xml` tüm rehber sayfalarını içermeli;
  `feed.xml`, `rehber.css` ve `assets/og.png` var olmalı.

Değiştirilmeyen ilkeler: dış istek yok, çerez yok, analitik yok, web fontu yok.
Bir SEO iyileştirmesi bu ilkelerden birini bozuyorsa **yapılmaz**.

`robots.txt` ve site geneli `sitemap.xml` bilerek eklenmedi: ikisi de rehber
bölümünün dışına çıkar. Ayrıca proje tipi GitHub Pages adreslerinde
`robots.txt` yalnızca alan adının kökünde geçerlidir.

---

## 6. Yazım ve ton

- **Jargon yok.** "Zımni ret" değil, "cevap gelmezse".
- **Süre her zaman görünür.** Kaybedilen hakların çoğu süresi kaçtığı için
  kaybediliyor.
- **Yanlış umut vermek, bilgi vermemekten daha zararlıdır.** Dava sonuçları,
  destek programları ve tutarlar gerçekçi anlatılır.
- **Kalıcı hak ile geçmiş uygulama ayrılır.** 2023'e özgü AFAD/KOSGEB/BDDK
  kararları "hakkınız" olarak değil, "geçmiş afette uygulanan emsal" olarak
  sunulur.
- **Kiracı unutulmaz.** Sistem mülkiyet üzerine kuruludur; kiracının en güçlü
  ve en az bilinen hakkı, tazminat davasında mülkiyet şartı aranmamasıdır.
- Her yazı sonunda **baro adli yardım** yönlendirmesi ve "hukuki tavsiye
  değildir" uyarısı bulunur.

---

## 7. Yerelde çalıştırma

```bash
cd docs && python3 -m http.server 8899   # http://localhost:8899
```

Sayfalar ES modülü kullandığı için `file://` ile açılmaz, sunulmaları gerekir.

## 8. Sık kullanılan komutlar

```bash
python3 scripts/blog-uret.py            # rehber sayfalarını üret
python3 scripts/blog-uret.py --kontrol  # üretim çıktısı güncel mi
python3 scripts/seo-kontrol.py          # rehber SEO denetimi
python3 scripts/seo-kontrol.py --sessiz # yalnızca hataları göster
PEXELS_ANAHTAR="..." python3 scripts/foto-indir.py   # eksik fotoğrafları indir
python3 scripts/veri-kontrol.py         # parametre ↔ veri.js tutarlılığı
```

---

## 9. Yapılacaklar (öncelik sırasıyla)

- 🔴 `DOGRULAMA.md` § A'daki 12 kritik maddenin resmî kaynaktan doğrulanması —
  sitedeki ve rehberdeki tüm süreler buna bağlı.
- 🔴 Dilekçe şablonlarının avukat onayı (yayın öncesi zorunlu).
- Rehber yazılarının bir avukat tarafından gözden geçirilip her sayfaya
  "içeriği doğrulayan" künyesinin eklenmesi.
- Çevrimdışı çalışma için service worker.
- Çok dilli içerik (TR, AR, KU) — rehber için `hreflang` altyapısı gerekir.
