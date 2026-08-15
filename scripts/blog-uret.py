#!/usr/bin/env python3
"""
BLOG ÜRETECİ — docs/blog/ altındaki tüm HTML dosyalarını üretir.

Neden üreteç var?
  20 yazının her birinde ~60 satırlık SEO başlığı (canonical, Open Graph,
  Twitter, JSON-LD, kırıntı yolu, içindekiler) elle yazılırsa tutarlılık
  ilk güncellemede bozulur. Kaynak metin `scripts/yazilar/*.py` içinde;
  bu betik SEO iskeletini tek yerden basar.

Çıktı, bağımlılığı olmayan düz HTML'dir — sitenin "derleme adımı yok"
ilkesi bozulmaz: üretilen dosyalar depoya işlenir, tarayıcı hiçbir şey
derlemez.

Kullanım:
    python3 scripts/blog-uret.py          # üret
    python3 scripts/blog-uret.py --kontrol # üretilen dosya güncel mi?

Bağımlılık: yok (yalnızca standart kütüphane).
"""

from __future__ import annotations

import html
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gorseller                                    # noqa: E402  (SVG şemaları)
from sekiller import SEKILLER                       # noqa: E402


def _ana_site():
    """Ana site üretecini (scripts/site-uret.py) yükler.

    Başlık, gezinme ve alt bilgi tek yerden gelsin diye rehber sayfaları da
    aynı `Site` sınıfını kullanır; aksi hâlde blog bölümü sitenin geri
    kalanından farklı görünürdü. Dosya adında tire olduğu için normal
    `import` çalışmaz."""
    yol = Path(__file__).resolve().parent / "site-uret.py"
    ayar = importlib.util.spec_from_file_location("site_uret", yol)
    modul = importlib.util.module_from_spec(ayar)
    ayar.loader.exec_module(modul)
    return modul.Site(json.loads(
        (Path(__file__).resolve().parent.parent / "icerik" / "site.json")
        .read_text(encoding="utf-8")))

KOK = Path(__file__).resolve().parent.parent
DOCS = KOK / "docs"
BLOG = DOCS / "blog"
YAZILAR_DIZIN = Path(__file__).resolve().parent / "yazilar"
KUNYE_DOSYA = Path(__file__).resolve().parent / "foto-kunye.json"

# Fotoğraf künyeleri `scripts/foto-indir.py` tarafından üretilir.
FOTOGRAFLAR = (json.loads(KUNYE_DOSYA.read_text(encoding="utf-8"))
               if KUNYE_DOSYA.exists() else {})

ANA = _ana_site()          # ortak başlık/gezinme/alt bilgi kaynağı

# --- Site sabitleri ---------------------------------------------------------
SITE = "https://saidsurucu.github.io/claude-impact-lab-1-t8-hasar-tespiti/"
SITE_ADI = "Deprem Haklarım"
KURULUS = "T8 Hasar Tespiti · Claude Impact Lab"
OG_GORSEL = SITE + "assets/og.png"
OG_ALT = "Deprem Haklarım — haklarınız var ama süreleri işliyor"
BLOG_ADI = "Deprem Hakları Rehberi"
BLOG_ACIKLAMA = (
    "Deprem öncesi ve sonrasındaki haklar, süreler ve başvuru yolları; "
    "her biri dayandığı kanun maddesiyle birlikte."
)

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

# Kategori sırası — blog dizininde ve yazı listelerinde bu sıra kullanılır.
KATEGORILER = [
    ("Deprem sonrası ilk günler",
     "Deprem olduktan sonraki ilk haftalarda süresi işleyen haklar."),
    ("DASK ve sigorta",
     "Zorunlu deprem sigortasının kapsamı, muafiyeti ve uyuşmazlık yolları."),
    ("Kiracı hakları",
     "Sistem mülkiyet üzerine kurulu; kiracının elinde kalan haklar."),
    ("Devlet desteği ve mülkiyet",
     "Hak sahipliği, afet konutu, vergi ve yeniden inşa süreci."),
    ("Dava yolları",
     "Müteahhit, yapı denetim kuruluşu ve idare karşısındaki sorumluluk."),
    ("Deprem öncesi",
     "Deprem olmadan önce kullanılabilecek, en az bilinen haklar."),
]

# --- Yardımcılar ------------------------------------------------------------
def tarih_yaz(iso: str) -> str:
    """2026-08-15 -> 15 Ağustos 2026"""
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} {AYLAR[d.month - 1]} {d.year}"

def rfc822(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")

def k(metin: str) -> str:
    """HTML öznitelik/metin kaçışı."""
    return html.escape(metin, quote=True)

def metne_cevir(parca_html: str) -> str:
    metin = re.sub(r"<[^>]+>", " ", parca_html)
    return html.unescape(re.sub(r"\s+", " ", metin)).strip()

def kelime_say(parca_html: str) -> int:
    return len([s for s in metne_cevir(parca_html).split(" ") if s])

def okuma_suresi(kelime: int) -> int:
    return max(2, round(kelime / 190))


# --- Yazıların yüklenmesi ---------------------------------------------------
def yazilari_yukle() -> list[dict]:
    yazilar = []
    for yol in sorted(YAZILAR_DIZIN.glob("*.py")):
        if yol.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(yol.stem, yol)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
        yazi = modul.YAZI
        yazi["dosya"] = yol.name
        yazilar.append(yazi)
    return yazilar


def dogrula(yazilar: list[dict]) -> None:
    """SEO kuralları üretim anında zorlanır; hata varsa dosya yazılmaz."""
    hatalar = []
    slugler = set()
    for y in yazilar:
        s = y["slug"]
        if s in slugler:
            hatalar.append(f"{s}: yinelenen slug")
        slugler.add(s)
        if not re.fullmatch(r"[a-z0-9-]+", s):
            hatalar.append(f"{s}: slug yalnızca a-z, 0-9 ve tire içerebilir")
        if len(y["seoBaslik"]) > 60:
            hatalar.append(f"{s}: <title> {len(y['seoBaslik'])} karakter (>60)")
        if len(y["seoBaslik"]) < 25:
            hatalar.append(f"{s}: <title> çok kısa ({len(y['seoBaslik'])})")
        if not 120 <= len(y["aciklama"]) <= 158:
            hatalar.append(
                f"{s}: meta description {len(y['aciklama'])} karakter "
                "(120-158 olmalı)")
        if y["kategori"] not in [ad for ad, _ in KATEGORILER]:
            hatalar.append(f"{s}: bilinmeyen kategori {y['kategori']!r}")
        if len(y.get("sss", [])) < 3:
            hatalar.append(f"{s}: en az 3 sık sorulan soru gerekir")
        if len(y.get("anahtar", [])) < 3:
            hatalar.append(f"{s}: en az 3 anahtar kelime gerekir")
        if not y.get("ilgili"):
            hatalar.append(f"{s}: en az bir ilgili yazı gerekir")
        for i in y.get("ilgili", []):
            if i not in slugler and i not in [z["slug"] for z in yazilar]:
                hatalar.append(f"{s}: ilgili yazı bulunamadı: {i}")
            if i == s:
                hatalar.append(f"{s}: kendine ilgili yazı veremez")
        for h2 in re.findall(r"<h2([^>]*)>", y["govde"]):
            if "id=" not in h2:
                hatalar.append(f"{s}: id'siz <h2> var (içindekiler bozulur)")
        # Türkçe eklemeli bir dil: aynı içerik İngilizceden ~%25 daha az
        # kelimeyle ifade edilir. Eşikler buna göre seçildi.
        govde = kelime_say(y["govde"])
        toplam = govde + sum(kelime_say(x["s"]) + kelime_say(x["c"])
                             for x in y["sss"])
        if govde < 550:
            hatalar.append(f"{s}: gövde {govde} kelime (<550)")
        if toplam < 750:
            hatalar.append(f"{s}: toplam {toplam} kelime (<750)")
    if hatalar:
        print("SEO doğrulaması başarısız:", file=sys.stderr)
        for h in hatalar:
            print("  ✗ " + h, file=sys.stderr)
        sys.exit(1)


# --- HTML parçaları ---------------------------------------------------------
def bas(*, baslik, aciklama, canonical, kok, anahtar=None, tur="website",
        yayin=None, guncelleme=None, bolum=None, etiketler=None,
        jsonld=None, rss=True, gorsel=None, gorsel_alt=None,
        gorsel_en=1200, gorsel_boy=630) -> str:
    gorsel = gorsel or OG_GORSEL
    gorsel_alt = gorsel_alt or OG_ALT
    p = [
        '<!doctype html>',
        '<html lang="tr">',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<title>{k(baslik)}</title>',
        f'<meta name="description" content="{k(aciklama)}">',
    ]
    if anahtar:
        p.append(f'<meta name="keywords" content="{k(", ".join(anahtar))}">')
    p += [
        f'<meta name="author" content="{k(SITE_ADI)} — {k(KURULUS)}">',
        '<meta name="robots" content="index, follow, max-snippet:-1, '
        'max-image-preview:large, max-video-preview:-1">',
        f'<link rel="canonical" href="{k(canonical)}">',
        '<meta name="color-scheme" content="light dark">',
        '<meta name="theme-color" content="#0B6B5B">',
        f'<meta property="og:type" content="{tur}">',
        f'<meta property="og:site_name" content="{k(SITE_ADI)}">',
        '<meta property="og:locale" content="tr_TR">',
        f'<meta property="og:title" content="{k(baslik)}">',
        f'<meta property="og:description" content="{k(aciklama)}">',
        f'<meta property="og:url" content="{k(canonical)}">',
        f'<meta property="og:image" content="{k(gorsel)}">',
        f'<meta property="og:image:width" content="{gorsel_en}">',
        f'<meta property="og:image:height" content="{gorsel_boy}">',
        f'<meta property="og:image:alt" content="{k(gorsel_alt)}">',
    ]
    if tur == "article":
        p += [
            f'<meta property="article:published_time" content="{yayin}T08:00:00+03:00">',
            f'<meta property="article:modified_time" content="{guncelleme}T08:00:00+03:00">',
            f'<meta property="article:section" content="{k(bolum)}">',
            f'<meta property="article:author" content="{k(KURULUS)}">',
        ]
        for e in etiketler or []:
            p.append(f'<meta property="article:tag" content="{k(e)}">')
    p += [
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{k(baslik)}">',
        f'<meta name="twitter:description" content="{k(aciklama)}">',
        f'<meta name="twitter:image" content="{k(gorsel)}">',
        f'<meta name="twitter:image:alt" content="{k(gorsel_alt)}">',
        f'<link rel="icon" href="{kok}favicon.svg" type="image/svg+xml">',
    ]
    if rss:
        p.append(f'<link rel="alternate" type="application/rss+xml" '
                 f'title="{k(BLOG_ADI)}" href="{kok}blog/feed.xml">')
    p.append(f'<link rel="stylesheet" href="{kok}assets/tasarim.css">')
    # Rehbere özgü bileşenler ayrı dosyada: ana tasarım sistemi dosyası
    # (assets/tasarim.css) rehber için değiştirilmez.
    p.append('<link rel="stylesheet" href="./rehber.css">')
    if jsonld:
        p.append('<script type="application/ld+json">')
        p.append(json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")))
        p.append('</script>')
    p.append('</head>')
    return "\n".join(p)


def kurulus_dugumleri() -> list[dict]:
    return [
        {
            "@type": "Organization",
            "@id": SITE + "#kurulus",
            "name": SITE_ADI,
            "alternateName": KURULUS,
            "url": SITE,
            "logo": {
                "@type": "ImageObject",
                "@id": SITE + "#logo",
                "url": SITE + "favicon.svg",
                "contentUrl": SITE + "favicon.svg",
                "width": 32, "height": 32,
                "caption": SITE_ADI,
            },
            "description": (
                "Deprem öncesi ve sonrasındaki hakları, dayandığı kanun "
                "maddesiyle birlikte ve süresi geçmeden önce anlatan, kâr "
                "amacı gütmeyen ücretsiz bilgi platformu."),
            "knowsLanguage": "tr-TR",
            "nonprofitStatus": "NonprofitType",
        },
        {
            "@type": "WebSite",
            "@id": SITE + "#site",
            "url": SITE,
            "name": SITE_ADI,
            "description": BLOG_ACIKLAMA,
            "publisher": {"@id": SITE + "#kurulus"},
            "inLanguage": "tr-TR",
        },
    ]


def kirinti_html(ogeler: list[tuple[str, str | None]]) -> str:
    """[(ad, href|None)] — son öge geçerli sayfadır."""
    satir = ['<nav class="kirinti" aria-label="Kırıntı yolu">', "<ol>"]
    for ad, href in ogeler:
        if href:
            satir.append(f'<li><a href="{k(href)}">{k(ad)}</a></li>')
        else:
            satir.append(f'<li><span aria-current="page">{k(ad)}</span></li>')
    satir += ["</ol>", "</nav>"]
    return "\n".join(satir)


def kirinti_jsonld(kimlik: str, ogeler: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": kimlik,
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": ad, "item": url}
            for i, (ad, url) in enumerate(ogeler)
        ],
    }


# --- Yazı sayfası -----------------------------------------------------------
def yazi_uret(y: dict, hepsi: dict[str, dict]) -> str:
    url = SITE + "blog/" + y["slug"] + ".html"
    foto = FOTOGRAFLAR.get(y["slug"])
    foto_url = (SITE + "blog/gorseller/" + y["slug"] + ".jpg") if foto else None
    kelime = kelime_say(y["govde"]) + sum(
        kelime_say(s["c"]) for s in y["sss"])
    dakika = okuma_suresi(kelime)

    basliklar = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', y["govde"], re.S)
    icindekiler = [(kid, metne_cevir(ad)) for kid, ad in basliklar]
    icindekiler.append(("sik-sorulan-sorular", "Sık sorulan sorular"))
    if y.get("dayanaklar"):
        icindekiler.append(("dayanaklar", "Hangi kanuna dayanıyor?"))

    kirinti = [
        (SITE_ADI, SITE),
        (BLOG_ADI, SITE + "blog/"),
        (y["baslik"], url),
    ]

    graf = kurulus_dugumleri() + [
        {
            "@type": "WebPage",
            "@id": url,
            "url": url,
            "name": y["seoBaslik"],
            "description": y["aciklama"],
            "isPartOf": {"@id": SITE + "#site"},
            "breadcrumb": {"@id": url + "#kirinti"},
            "inLanguage": "tr-TR",
            "datePublished": y["yayin"],
            "dateModified": y["guncelleme"],
            "primaryImageOfPage": {"@id": url + "#gorsel"},
        },
        {
            "@type": "ImageObject",
            "@id": url + "#gorsel",
            "url": foto_url or OG_GORSEL,
            "contentUrl": foto_url or OG_GORSEL,
            "width": foto["genislik"] if foto else 1200,
            "height": foto["yukseklik"] if foto else 630,
            "caption": foto["alt"] if foto else OG_ALT,
            "creditText": (f"{foto['fotografci']} · Pexels") if foto else SITE_ADI,
            "license": "https://www.pexels.com/license/" if foto else SITE,
        },
        {
            "@type": "Article",
            "@id": url + "#makale",
            "isPartOf": {"@id": url},
            "mainEntityOfPage": {"@id": url},
            "headline": y["baslik"][:110],
            "name": y["baslik"],
            "description": y["aciklama"],
            "articleSection": y["kategori"],
            "keywords": y["anahtar"],
            "inLanguage": "tr-TR",
            "datePublished": y["yayin"],
            "dateModified": y["guncelleme"],
            "author": {"@id": SITE + "#kurulus"},
            "publisher": {"@id": SITE + "#kurulus"},
            "image": {"@id": url + "#gorsel"},
            "wordCount": kelime,
            "timeRequired": f"PT{dakika}M",
            "isAccessibleForFree": True,
            "license": SITE,
            "about": [{"@type": "Thing", "name": a} for a in y["anahtar"][:6]],
            "citation": [
                {"@type": "CreativeWork", "name": d} for d in y.get("dayanaklar", [])
            ],
        },
        kirinti_jsonld(url + "#kirinti", kirinti),
        {
            "@type": "FAQPage",
            "@id": url + "#sss",
            "isPartOf": {"@id": url},
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": s["s"],
                    "acceptedAnswer": {"@type": "Answer", "text": s["c"]},
                }
                for s in y["sss"]
            ],
        },
    ]

    p = [bas(baslik=y["seoBaslik"], aciklama=y["aciklama"], canonical=url,
             kok="../", anahtar=y["anahtar"], tur="article", yayin=y["yayin"],
             guncelleme=y["guncelleme"], bolum=y["kategori"],
             etiketler=y["anahtar"],
             gorsel=foto_url, gorsel_alt=foto["alt"] if foto else None,
             gorsel_en=foto["genislik"] if foto else 1200,
             gorsel_boy=foto["yukseklik"] if foto else 630,
             jsonld={"@context": "https://schema.org", "@graph": graf}),
         '<body>',
         '<a class="atla" href="#ana">İçeriğe atla</a>',
         ANA.ust_html(1, None),
         '<main id="ana" class="kap">',
         kirinti_html([(SITE_ADI, "../index.html"),
                       (BLOG_ADI, "./index.html"),
                       (y["baslik"], None)]),
         '<article class="yazi">',
         '<header>',
         f'<p class="etiket">{k(y["kategori"])}</p>',
         f'<h1>{y["baslik"]}</h1>',
         f'<p class="giris">{y["ozet"]}</p>',
         '<p class="yazi-bilgi">',
         f'<time datetime="{y["yayin"]}">{tarih_yaz(y["yayin"])}</time>',
         (f' · <span>Güncelleme: <time datetime="{y["guncelleme"]}">'
          f'{tarih_yaz(y["guncelleme"])}</time></span>'
          if y["guncelleme"] != y["yayin"] else ""),
         f' · <span>~{dakika} dakika okuma</span>',
         f' · <span>{KURULUS}</span>',
         '</p>',
         '</header>']

    if foto:
        p += ['<figure class="foto">',
              f'<img src="./gorseller/{y["slug"]}.jpg" '
              f'alt="{k(foto["alt"])}" width="{foto["genislik"]}" '
              f'height="{foto["yukseklik"]}" decoding="async" '
              f'fetchpriority="high">',
              '<figcaption>Fotoğraf: '
              f'<a href="{k(foto["fotografci_adres"])}" rel="nofollow noopener" '
              f'target="_blank">{k(foto["fotografci"])}</a> · '
              f'<a href="{k(foto["sayfa"])}" rel="nofollow noopener" '
              f'target="_blank">Pexels</a></figcaption>',
              '</figure>']

    if y.get("sure"):
        p += ['<div class="kart tehlikeli">',
              '<span class="etiket">Süre</span>',
              f'<p style="margin-bottom:0"><strong>{y["sure"]}</strong></p>',
              '</div>']

    p += ['<nav class="icindekiler" aria-label="İçindekiler">',
          '<p class="etiket">İçindekiler</p>', '<ol>']
    for kid, ad in icindekiler:
        p.append(f'<li><a href="#{kid}">{k(ad)}</a></li>')
    p += ['</ol>', '</nav>']

    sekil = SEKILLER.get(y["slug"])
    if sekil:
        p += ['<figure class="sekil">',
              gorseller.ciz(y["slug"], sekil),
              f'<figcaption>{k(sekil["altyazi"])}</figcaption>',
              '</figure>']

    p.append(yollari_guncelle(y["govde"].strip()))

    p += ['<h2 id="sik-sorulan-sorular">Sık sorulan sorular</h2>',
          '<div class="sss">']
    for s in y["sss"]:
        p += [f'<h3>{k(s["s"])}</h3>', f'<p>{k(s["c"])}</p>']
    p.append('</div>')

    if y.get("dayanaklar"):
        p += ['<h2 id="dayanaklar">Hangi kanuna dayanıyor?</h2>',
              '<p>Bu yazıdaki bilgilerin dayandığı düzenlemeler:</p>',
              '<ul class="dayanak-liste">']
        for d in y["dayanaklar"]:
            p.append(f'<li>{k(d)}</li>')
        p.append('</ul>')
        p += ['<div class="serit">',
              '<strong>Doğrulama durumu: kaynak metinden teyit bekliyor.</strong>',
              'Bu yazıdaki kanun maddeleri birden fazla bağımsız ikincil '
              'kaynaktan derlendi; Resmî Gazete ve mevzuat.gov.tr metinleriyle '
              'birebir karşılaştırma sürüyor. Kesin bilgi ve somut olayınıza '
              'uygulanması için avukata veya barosunun '
              '<strong>adli yardım</strong> birimine danışın.',
              '</div>']

    if y.get("araclar"):
        p += ['<div class="kart vurgulu">',
              '<span class="etiket">Bu sayfadan devam edin</span>',
              '<ul style="margin:0">']
        for href, ad, aciklama in y["araclar"]:
            p.append(f'<li><a href="{k(yollari_guncelle(href))}">'
                     f'<strong>{k(ad)}</strong></a> — {k(aciklama)}</li>')
        p += ['</ul>', '</div>']

    p += ['<footer class="yazi-alt">',
          '<h2 id="ilgili-yazilar">İlgili yazılar</h2>',
          '<ul class="ilgili-liste">']
    for slug in y["ilgili"]:
        i = hepsi[slug]
        p.append(f'<li><a href="./{i["slug"]}.html">{i["baslik"]}</a><br>'
                 f'<small>{k(i["ozet"] if len(i["ozet"]) < 130 else i["ozet"][:127] + "…")}</small></li>')
    p += ['</ul>',
          '<p class="etiketler">Etiketler: ' +
          ", ".join(k(a) for a in y["anahtar"]) + '</p>',
          f'<p class="etiketler"><a href="./index.html">← Tüm rehber yazıları</a></p>',
          '</footer>',
          '</article>',
          '</main>',
          ANA.alt_html(1),
          '<script type="module">',
          '  import { temaBaslat, temaBagla } from "../assets/app.js";',
          '  temaBaslat(); temaBagla();',
          '</script>',
          '</body>',
          '</html>', '']
    return "\n".join(x for x in p if x != "")


# --- Blog dizini ------------------------------------------------------------
def dizin_uret(yazilar: list[dict]) -> str:
    url = SITE + "blog/"
    baslik = "Deprem hakları rehberi: haklar, süreler ve başvuru yolları"
    seo_baslik = "Deprem Hakları Rehberi: Süreler ve Başvuru Yolları"
    aciklama = (
        "Deprem öncesi ve sonrasındaki haklarınız: hasar tespitine itiraz, "
        "DASK, kiracı hakları, hak sahipliği ve dava yolları. Her yazı kanun "
        "maddesiyle birlikte.")

    kirinti = [(SITE_ADI, SITE), (BLOG_ADI, url)]
    graf = kurulus_dugumleri() + [
        {
            "@type": "CollectionPage",
            "@id": url,
            "url": url,
            "name": seo_baslik,
            "description": aciklama,
            "isPartOf": {"@id": SITE + "#site"},
            "breadcrumb": {"@id": url + "#kirinti"},
            "inLanguage": "tr-TR",
        },
        {
            "@type": "Blog",
            "@id": url + "#blog",
            "url": url,
            "name": BLOG_ADI,
            "description": BLOG_ACIKLAMA,
            "inLanguage": "tr-TR",
            "publisher": {"@id": SITE + "#kurulus"},
            "blogPost": [
                {
                    "@type": "BlogPosting",
                    "@id": SITE + "blog/" + y["slug"] + ".html#makale",
                    "headline": y["baslik"][:110],
                    "url": SITE + "blog/" + y["slug"] + ".html",
                    "datePublished": y["yayin"],
                    "dateModified": y["guncelleme"],
                    "author": {"@id": SITE + "#kurulus"},
                }
                for y in yazilar
            ],
        },
        {
            "@type": "ItemList",
            "@id": url + "#liste",
            "name": BLOG_ADI,
            "numberOfItems": len(yazilar),
            "itemListOrder": "https://schema.org/ItemListOrderAscending",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": y["baslik"],
                 "url": SITE + "blog/" + y["slug"] + ".html"}
                for i, y in enumerate(yazilar)
            ],
        },
        kirinti_jsonld(url + "#kirinti", kirinti),
    ]

    p = [bas(baslik=seo_baslik, aciklama=aciklama, canonical=url, kok="../",
             anahtar=["deprem hakları", "deprem hukuku", "hasar tespiti itiraz",
                      "DASK", "kiracı hakları", "hak sahipliği"],
             jsonld={"@context": "https://schema.org", "@graph": graf}),
         '<body>',
         '<a class="atla" href="#ana">İçeriğe atla</a>',
         ANA.ust_html(1, None),
         '<main id="ana" class="kap">',
         kirinti_html([(SITE_ADI, "../index.html"), (BLOG_ADI, None)]),
         '<p class="etiket">Rehber</p>',
         f'<h1>{baslik}</h1>',
         '<p class="giris">Her yazı tek bir soruya cevap verir: hakkınız ne, '
         'süresi kaç gün, nereye başvuracaksınız ve hangi kanuna dayanıyor. '
         'Ücretsiz, reklamsız, kayıt gerektirmez.</p>',
         '<div class="serit">',
         '<strong>Bu yazılar hukuki tavsiye değildir.</strong>',
         'Genel bilgilendirme amaçlıdır ve avukatlık hizmetinin yerine geçmez. '
         'Bilgiler resmî kaynaklardan doğrulanana kadar taslak sayılmalıdır.',
         '</div>']

    for kategori, kat_aciklama in KATEGORILER:
        kat_yazilar = [y for y in yazilar if y["kategori"] == kategori]
        if not kat_yazilar:
            continue
        kimlik = re.sub(r"[^a-z0-9]+", "-",
                        kategori.lower()
                        .replace("ı", "i").replace("ş", "s").replace("ç", "c")
                        .replace("ö", "o").replace("ü", "u").replace("ğ", "g")
                        ).strip("-")
        p += [f'<h2 id="{kimlik}">{k(kategori)}</h2>',
              f'<p>{k(kat_aciklama)}</p>']
        for y in kat_yazilar:
            foto = FOTOGRAFLAR.get(y["slug"])
            p.append(f'<a class="secim{" gorselli" if foto else ""}" '
                     f'href="./{y["slug"]}.html">')
            if foto:
                # Kart görseli bilgi taşımaz; başlık zaten bağlantı metnidir,
                # bu yüzden alt boş bırakılır (ekran okuyucu tekrar etmesin).
                p.append(f'<img src="./gorseller/kucuk/{y["slug"]}.jpg" alt="" '
                         f'width="360" height="188" loading="lazy" '
                         f'decoding="async">')
            p += [f'<b>{y["baslik"]}</b>',
                  f'<span>{y["ozet"]}</span>',
                  '</a>']

    p += ['<h2 id="araclar">Hesaplayan araçlar</h2>',
          '<p>Yazılar bilgiyi anlatır; araçlar sizin durumunuza uygular.</p>',
          '<a class="secim" href="../arac/sureler.html"><b>Süre takvimi</b>'
          '<span>Tarihlerinizi girin, hangi hakkınızın kaç günü kaldığını '
          'görün.</span></a>',
          '<a class="secim" href="../arac/haklarim.html"><b>Haklarım</b>'
          '<span>Üç soru cevaplayın, durumunuza uyan hakları listeleyelim.'
          '</span></a>',
          '<a class="secim" href="../arac/teminat.html"><b>Sigorta açığı hesabı</b>'
          '<span>DASK ne kadarını karşılıyor, ne kadarı size kalıyor?</span></a>',
          '<a class="secim" href="../arac/dilekce.html"><b>Dilekçe hazırla</b>'
          '<span>Hazır şablonu doldurun, nereye göndereceğinizi öğrenin.'
          '</span></a>',
          '<p class="etiketler"><a href="./feed.xml">RSS akışı</a> · '
          f'{len(yazilar)} yazı · Son güncelleme: '
          f'{tarih_yaz(max(y["guncelleme"] for y in yazilar))}</p>',
          '<p class="etiketler">Fotoğraflar: '
          '<a href="https://www.pexels.com/" rel="nofollow noopener" '
          'target="_blank">Pexels</a> (her yazının altında fotoğrafçı künyesi '
          'vardır) · Şemalar: Deprem Haklarım. Görseller siteye indirilmiştir; '
          'sayfa hiçbir dış istek yapmaz.</p>',
          '</main>',
          ANA.alt_html(1),
          '<script type="module">',
          '  import { temaBaslat, temaBagla } from "../assets/app.js";',
          '  temaBaslat(); temaBagla();',
          '</script>',
          '</body>',
          '</html>', '']
    return "\n".join(p)


# --- Site haritası, RSS, robots, 404 ---------------------------------------
def sitemap_uret(yazilar: list[dict]) -> str:
    """Yalnızca rehber bölümünü kapsar; sitenin geri kalanına dokunmaz."""
    tarih = max(y["guncelleme"] for y in yazilar)
    girisler = [(SITE + "blog/", tarih, "weekly", "1.0")]
    girisler += [(SITE + "blog/" + y["slug"] + ".html", y["guncelleme"],
                  "monthly", "0.8") for y in yazilar]

    p = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, freq, oncelik in girisler:
        p += ['  <url>', f'    <loc>{loc}</loc>',
              f'    <lastmod>{lastmod}</lastmod>',
              f'    <changefreq>{freq}</changefreq>',
              f'    <priority>{oncelik}</priority>', '  </url>']
    p += ['</urlset>', '']
    return "\n".join(p)


def rss_uret(yazilar: list[dict]) -> str:
    p = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
         '  <channel>',
         f'    <title>{k(BLOG_ADI)}</title>',
         f'    <link>{SITE}blog/</link>',
         f'    <description>{k(BLOG_ACIKLAMA)}</description>',
         '    <language>tr</language>',
         f'    <lastBuildDate>{rfc822(max(y["guncelleme"] for y in yazilar))}</lastBuildDate>',
         f'    <atom:link href="{SITE}blog/feed.xml" rel="self" type="application/rss+xml"/>']
    for y in yazilar:
        url = SITE + "blog/" + y["slug"] + ".html"
        p += ['    <item>',
              f'      <title>{k(y["baslik"])}</title>',
              f'      <link>{url}</link>',
              f'      <guid isPermaLink="true">{url}</guid>',
              f'      <description>{k(metne_cevir(y["ozet"]))}</description>',
              f'      <category>{k(y["kategori"])}</category>',
              f'      <pubDate>{rfc822(y["yayin"])}</pubDate>',
              '    </item>']
    p += ['  </channel>', '</rss>', '']
    return "\n".join(p)


# --- Ana akış ---------------------------------------------------------------
ARAC_TASINDI = {           # ana dal araçları docs/arac/ altına taşıdı
    "../sureler.html": "../arac/sureler.html",
    "../haklarim.html": "../arac/haklarim.html",
    "../teminat.html": "../arac/teminat.html",
    "../dilekce.html": "../arac/dilekce.html",
}


def yollari_guncelle(metin: str) -> str:
    for eski, yeni in ARAC_TASINDI.items():
        metin = metin.replace(eski, yeni)
    return metin


def main() -> int:
    kontrol = "--kontrol" in sys.argv
    yazilar = yazilari_yukle()
    if not yazilar:
        print("scripts/yazilar/ boş — üretilecek yazı yok.", file=sys.stderr)
        return 1
    dogrula(yazilar)

    # Kategori sırası + kategori içinde dosya adı sırası
    sira = {ad: i for i, (ad, _) in enumerate(KATEGORILER)}
    yazilar.sort(key=lambda y: (sira[y["kategori"]], y["dosya"]))
    hepsi = {y["slug"]: y for y in yazilar}

    BLOG.mkdir(parents=True, exist_ok=True)
    dosyalar = {BLOG / "index.html": dizin_uret(yazilar),
                BLOG / "feed.xml": rss_uret(yazilar),
                BLOG / "sitemap.xml": sitemap_uret(yazilar)}
    for y in yazilar:
        dosyalar[BLOG / (y["slug"] + ".html")] = yazi_uret(y, hepsi)

    farkli = []
    for yol, icerik in dosyalar.items():
        eski = yol.read_text(encoding="utf-8") if yol.exists() else None
        if eski != icerik:
            farkli.append(yol)
            if not kontrol:
                yol.write_text(icerik, encoding="utf-8")

    if kontrol:
        if farkli:
            print("Üretilen dosyalar güncel değil:", file=sys.stderr)
            for yol in farkli:
                print("  ✗ " + str(yol.relative_to(KOK)), file=sys.stderr)
            print("  → python3 scripts/blog-uret.py", file=sys.stderr)
            return 1
        print(f"✓ {len(dosyalar)} dosya güncel.")
        return 0

    toplam = 0
    for y in yazilar:
        kelime = kelime_say(y["govde"]) + sum(kelime_say(s["c"]) for s in y["sss"])
        toplam += kelime
        print(f"  {y['slug']:<38} {kelime:>5} kelime  "
              f"başlık {len(y['seoBaslik']):>2}  açıklama {len(y['aciklama']):>3}")
    print(f"\n✓ {len(yazilar)} yazı, {toplam} kelime, {len(dosyalar)} dosya yazıldı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
