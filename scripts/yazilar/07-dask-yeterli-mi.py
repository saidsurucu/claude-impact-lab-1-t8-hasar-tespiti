# -*- coding: utf-8 -*-
YAZI = {
    "slug": "dask-yeterli-mi",
    "kategori": "DASK ve sigorta",
    "yayin": "2026-08-15",
    "guncelleme": "2026-08-15",
    "seoBaslik": "DASK Yeterli mi? Sigorta Bedeli ve Azami Teminat",
    "baslik": "DASK'ım yeterli mi? Sigorta bedeli, azami teminat ve eksik sigorta tuzağı",
    "ozet": "DASK'ın ödeyeceği tutar konutunuzun piyasa değeri değildir. Bedel "
            "metrekareyle hesaplanır, azami teminatla sınırlıdır ve muafiyet düşülür.",
    "aciklama": "DASK ne kadar öder? Sigorta bedeli metrekare üzerinden hesaplanır, "
                "azami teminatla sınırlıdır. Eksik sigorta tuzağı ve teminat açığının "
                "nasıl kapatılacağı.",
    "anahtar": ["DASK ne kadar öder", "DASK azami teminat", "sigorta bedeli hesaplama",
                "eksik sigorta", "DASK yeterli mi", "konut sigortası deprem teminatı"],
    "araclar": [
        ("../teminat.html", "Sigorta açığı hesabı",
         "binanızın bedelini, muafiyeti ve açıkta kalan tutarı hesaplayın"),
        ("../haklarim.html", "Haklarım",
         "profilinize göre hangi haklara sahipsiniz?"),
    ],
    "dayanaklar": [
        "Zorunlu Deprem Sigortası Tarife ve Talimat Tebliği — metrekare bedelleri ve azami teminat",
        "Zorunlu Deprem Sigortası Genel Şartları — muafiyet ve teminat kapsamı",
        "6102 sayılı Türk Ticaret Kanunu — eksik sigorta ve oransal ödeme",
    ],
    "sss": [
        {"s": "DASK'ın ödeyeceği tutar nasıl hesaplanır?",
         "c": "Sigorta bedeli, yapı tarzına göre belirlenen metrekare birim "
              "bedelinin binanın brüt yüzölçümüyle çarpılmasıyla bulunur. "
              "Bulunan tutar azami teminatı aşarsa ödeme azami teminatla "
              "sınırlıdır; ayrıca yüzde iki muafiyet düşülür."},
        {"s": "DASK azami teminat tutarı ne kadar?",
         "c": "Azami teminat tutarı sabit değildir; tarife dönemlerinde "
              "güncellenir. 01.05.2026 tarifesine göre bir mesken için azami "
              "teminat 2.271.283 TL olarak belirtilmiştir. Güncel değeri her "
              "zaman resmî tarifeden teyit edin."},
        {"s": "Eksik sigorta ne demek?",
         "c": "Sigorta bedelinin, malın gerçek değerinden düşük belirlenmesidir. "
              "Bu durumda sigortacı, sigorta bedelinin gerçek değere oranı "
              "ölçüsünde orantılı ödeme yapar; hasarın tamamını ödemez."},
        {"s": "DASK'ın üstünü hangi poliçe kapatır?",
         "c": "Deprem ek teminatlı ihtiyari konut sigortası. Önce DASK limitine "
              "kadar öder, limiti aşan kısım konut paket poliçesinin deprem "
              "teminatından karşılanır."},
    ],
    "ilgili": ["dask-neleri-karsilamaz", "dask-hasar-ihbari",
               "daskim-yoksa-ne-olur", "eksper-raporuna-itiraz"],
    "govde": """
<p>"DASK'ım var" cümlesi, çoğu insan için "evim sigortalı" anlamına geliyor.
Oysa DASK'ın ödeyeceği tutarın konutunuzun piyasa değeriyle ilgisi yoktur.
Ödeme üç filtreden geçer: <strong>sigorta bedeli</strong>,
<strong>azami teminat</strong> ve <strong>muafiyet</strong>.</p>

<h2 id="sigorta-bedeli">1. Sigorta bedeli: metrekare × birim bedel</h2>

<p>Sigorta bedeli, yapı tarzına göre belirlenen metrekare birim bedelinin
binanın brüt yüzölçümüyle çarpılmasıyla bulunur.</p>

<div class="tablo-sar">
<table>
  <caption class="sr">Yapı tarzına göre metrekare birim bedelleri</caption>
  <thead><tr><th>Yapı tarzı</th><th class="sayi">m² bedeli (01.05.2026)</th></tr></thead>
  <tbody>
    <tr><td>Çelik, betonarme karkas</td><td class="sayi">10.714 TL</td></tr>
    <tr><td>Diğer yapılar</td><td class="sayi">7.142 TL</td></tr>
  </tbody>
</table>
</div>

<p><strong>Örnek:</strong> 100 m² betonarme konut →
100 × 10.714 = <strong>1.071.400 TL</strong> sigorta bedeli.</p>

<p>Aynı konutun piyasa değeri 4 milyon TL olabilir. DASK bu farkı kapatmaz;
zaten amacı da bu değildir — DASK, yapıyı yeniden üretme maliyetine dayalı bir
sistemdir.</p>

<h2 id="azami-teminat">2. Azami teminat: üst sınır</h2>

<p>Sigorta bedeli ne çıkarsa çıksın, bir mesken için ödenecek tutar
<strong>azami teminat</strong> ile sınırlıdır. 01.05.2026 tarifesine göre bu
tutar 2.271.283 TL olarak belirtilmiştir.</p>

<div class="kart uyarili">
  <span class="etiket">Tarih damgası</span>
  <p style="margin-bottom:0">Azami teminat tutarı 2026'da <strong>yıl içinde
  birden fazla kez</strong> güncellenmiştir: 2024'te 1.272.000 TL, 2025'te
  1.704.162 TL, 2026 başında 2.095.462 TL, 01.05.2026'da 2.271.283 TL. Bu
  yüzden hiçbir içerik sayfasına sabit rakam yazılmamalı; hesaplama, tarih
  damgalı bir tarifeden yapılmalıdır. <a href="../teminat.html">Sigorta açığı
  aracı</a> hangi tarihli tarifeyle hesap yaptığını size gösterir.</p>
</div>

<h2 id="muafiyet">3. Muafiyet: %2 tenzili muafiyet</h2>

<p>Her hasarda sigorta bedelinin <strong>%2'si oranında tenzili muafiyet</strong>
uygulanır; DASK muafiyeti aşan kısımdan sorumludur. 1.071.400 TL bedelli bir
konutta bu, 21.428 TL demektir. Bu tutarın altındaki hasarlar için ödeme
yapılmaz.</p>

<p>Muafiyet uygulaması bakımından her 72 saatlik dönem tek hasar sayılır —
bu kural sigortalının lehinedir.
<a href="./dask-hasar-ihbari.html">Ayrıntısı burada</a>.</p>

<h2 id="teminat-acigi">Sonuç: teminat açığı</h2>

<p>Üç filtreden sonra ortaya çıkan tabloya <strong>teminat açığı</strong>
diyoruz: konutunuzun gerçek değeri ile sigortanın ödeyeceği tutar arasındaki
fark, artı DASK'ın hiç ödemediği kalemler.</p>

<div class="tablo-sar">
<table>
  <caption class="sr">Örnek teminat açığı hesabı</caption>
  <thead><tr><th>Kalem</th><th class="sayi">Tutar</th></tr></thead>
  <tbody>
    <tr><td>Konutun varsayılan değeri</td><td class="sayi">4.000.000 TL</td></tr>
    <tr><td>DASK sigorta bedeli (100 m² betonarme)</td><td class="sayi">1.071.400 TL</td></tr>
    <tr><td>Muafiyet (%2)</td><td class="sayi">−21.428 TL</td></tr>
    <tr><td><strong>Açıkta kalan</strong></td><td class="sayi"><strong>2.928.600 TL</strong></td></tr>
    <tr><td>Ayrıca kapsam dışı: eşya, enkaz, kira, bedeni zarar</td><td class="sayi">—</td></tr>
  </tbody>
</table>
</div>

<h2 id="eksik-sigorta">Eksik sigorta tuzağı</h2>

<p>İhtiyari konut sigortası yaptıranların en sık düştüğü tuzak budur. Sigorta
bedeli, malın gerçek değerinden düşük belirlenmişse
<strong>eksik sigorta</strong> söz konusu olur ve sigortacı, sigorta bedelinin
gerçek değere oranı ölçüsünde <strong>orantılı</strong> ödeme yapar.</p>

<div class="kart tehlikeli">
  <span class="etiket">Somut örnek</span>
  <p style="margin-bottom:0">Gerçek değeri 4.000.000 TL olan konutu 2.000.000 TL
  üzerinden sigortalatan kişi, 1.000.000 TL'lik hasarda tam ödeme değil,
  oran gereği <strong>500.000 TL</strong> tazminat alır. Poliçesi olduğu için
  kendini güvende sanan kişi, hasarın yarısını üstlenmiş olur.</p>
</div>

<p>Prim düşürmek için bedeli düşük göstermek, hasar anında en pahalı karara
dönüşür.</p>

<h2 id="acigi-kapatmak">Açığı kapatmanın yolları</h2>

<ol>
  <li><strong>Deprem ek teminatlı konut sigortası.</strong> DASK limitini aşan
  bina hasarını, eşyayı, enkaz kaldırmayı ve alternatif konaklamayı poliçeye
  göre karşılar.</li>
  <li><strong>Poliçedeki metrekare ve yapı tarzını düzeltin.</strong> Yanlış
  metrekare doğrudan eksik bedel demektir.</li>
  <li><strong>Ferdi kaza poliçenizde deprem teminatını kontrol edin.</strong>
  Aksi kararlaştırılmadıkça deprem teminat dışıdır.</li>
  <li><strong>Kiracıysanız kendi eşyanızı sigortalayın.</strong> DASK
  yaptıramazsınız ama eşya sigortası yaptırabilirsiniz.</li>
</ol>

<h2 id="policeyi-kontrol">Poliçenizi okurken bakılacak beş şey</h2>

<ul>
  <li>Brüt yüzölçümü doğru mu?</li>
  <li>Yapı tarzı (çelik/betonarme karkas veya diğer) doğru mu?</li>
  <li>Sigorta bedeli ve azami teminat kaç TL yazıyor?</li>
  <li>Poliçe hangi tarihe kadar geçerli? Yenileme yapılmadıysa teminat yoktur.</li>
  <li>Bina, genel şartlardaki kapsam dışı hâllerden birine giriyor mu
  (tamamı ticari kullanım, taşıyıcı sistem tadilatı, metruk yapı)?</li>
</ul>

<p>Poliçeniz hiç yoksa, asıl kayıp cezai yaptırım değildir:
<a href="./daskim-yoksa-ne-olur.html">DASK'ı olmayan devlet konut yardımından
da yararlanamaz.</a></p>

<h2 id="metrekare">En sık yapılan hata: yanlış metrekare</h2>

<p>Sigorta bedeli <strong>brüt yüzölçümü</strong> üzerinden hesaplanır. Poliçede
net alan yazılmışsa veya balkon, ortak alan payı gibi kalemler eksik
hesaplanmışsa, sigorta bedeliniz gerçekte olması gerekenden düşük çıkar ve
hasar anında ödeme de düşük olur.</p>

<ul>
  <li>Tapu ve proje bilgilerinizle poliçedeki metrekareyi karşılaştırın.</li>
  <li>Yapı tarzı alanının doğru olduğundan emin olun: betonarme bir binada
  "diğer" seçilmişse bedel yaklaşık üçte bir oranında düşük hesaplanır.</li>
  <li>Hata varsa poliçeyi düzenleyen şirkete başvurup
  <strong>zeyilname</strong> ile düzeltilmesini isteyin.</li>
</ul>

<h2 id="ne-zaman-yeterli">DASK ne zaman "yeterli" sayılır?</h2>

<p>DASK'ın amacı konutunuzun piyasa değerini korumak değil, yapının yeniden
üretilmesine katkı sağlamaktır. Bu çerçevede DASK şu üç koşulda görece
yeterlidir:</p>

<ol>
  <li>Binanın metrekaresi küçük ve sigorta bedeli, gerçek yapım maliyetine
  yakınsa,</li>
  <li>Eşya, barınma ve bedeni zarar riskleri <strong>ayrı poliçelerle</strong>
  karşılanıyorsa,</li>
  <li>Muafiyet tutarını kendi bütçenizden karşılayabilecek durumdaysanız.</li>
</ol>

<p>Üçü de sağlanmıyorsa, DASK tek başına bir koruma planı değil, planın yalnızca
ilk katmanıdır.</p>
""",
}
