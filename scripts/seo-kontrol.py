#!/usr/bin/env python3
"""
SEO DENETİMİ — docs/blog/ altındaki rehber sayfalarını kurallara karşı sınar.

Kapsam yalnızca rehber bölümüdür; sitenin elle yazılmış sayfalarına
(index.html, sureler.html, ...) dokunulmaz ve onlar denetlenmez.

Denetlenen kurallar (arama motoru puanlamalarında ölçülen kalemler):

  Teknik      lang, charset, viewport, tek <h1>, başlık hiyerarşisi,
              title uzunluğu, meta description uzunluğu, canonical,
              robots, theme-color
  Paylaşım    Open Graph ve Twitter kartı alanları, görsel boyutu
  Yapısal     JSON-LD ayrıştırılabilirliği ve zorunlu alanlar
  Bağlantı    site içi bağlantı hedeflerinin var olması, boş href
  Erişim      img alt/genişlik/yükseklik, satır içi SVG'de role ve
              aria-labelledby, tablolarda caption, anlamlı bağlantı metni
  Kapsam      blog/sitemap.xml ile sayfa kümesinin örtüşmesi, RSS ve
              paylaşım görselinin varlığı

Kullanım:
    python3 scripts/seo-kontrol.py           # rapor + hata varsa çıkış 1
    python3 scripts/seo-kontrol.py --sessiz  # yalnızca hatalar

Bağımlılık: yok (yalnızca standart kütüphane).
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag

KOK = Path(__file__).resolve().parent.parent
DOCS = KOK / "docs"
BLOG = DOCS / "blog"
SITE = "https://saidsurucu.github.io/claude-impact-lab-1-t8-hasar-tespiti/"

BASLIK_AZAMI = 60
BASLIK_ASGARI = 25
ACIKLAMA_ARALIK = (120, 158)


class Sayfa(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.link: dict[str, str] = {}
        self.baslik = ""
        self._baslikta = False
        self._basta = False
        self._jsonlda = False
        self.jsonld: list[str] = []
        self.hler: list[tuple[int, str]] = []
        self._h = 0
        self._h_metin = ""
        self.gorseller: list[dict] = []
        self.svgler: list[dict] = []
        self.baglantilar: list[tuple[str, str]] = []
        self._a_href: str | None = None
        self._a_metin = ""
        self.html_dil = ""
        self.tablolar = 0
        self.captionlar = 0

    def handle_starttag(self, etiket, oz):
        d = dict(oz)
        if etiket == "html":
            self.html_dil = d.get("lang", "")
        elif etiket == "head":
            self._basta = True
        elif etiket == "title" and self._basta:
            self._baslikta = True
        elif etiket == "meta":
            ad = d.get("name") or d.get("property") or d.get("charset") and "charset"
            if d.get("charset"):
                self.meta["charset"] = d["charset"]
            elif ad:
                self.meta[ad] = d.get("content", "")
        elif etiket == "link":
            for r in (d.get("rel") or "").split():
                self.link[r] = d.get("href", "")
        elif etiket == "script" and d.get("type") == "application/ld+json":
            self._jsonlda = True
            self.jsonld.append("")
        elif etiket in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = int(etiket[1])
            self._h_metin = ""
        elif etiket == "img":
            self.gorseller.append(d)
        elif etiket == "svg":
            self.svgler.append(d)
        elif etiket == "a":
            self._a_href = d.get("href")
            self._a_metin = ""
        elif etiket == "table":
            self.tablolar += 1
        elif etiket == "caption":
            self.captionlar += 1

    def handle_endtag(self, etiket):
        if etiket == "head":
            self._basta = False
        elif etiket == "title":
            self._baslikta = False
        elif etiket == "script":
            self._jsonlda = False
        elif etiket in ("h1", "h2", "h3", "h4", "h5", "h6") and self._h:
            self.hler.append((self._h, self._h_metin.strip()))
            self._h = 0
        elif etiket == "a" and self._a_href is not None:
            self.baglantilar.append((self._a_href, self._a_metin.strip()))
            self._a_href = None

    def handle_data(self, veri):
        if self._baslikta:
            self.baslik += veri
        if self._jsonlda and self.jsonld:
            self.jsonld[-1] += veri
        if self._h:
            self._h_metin += veri
        if self._a_href is not None:
            self._a_metin += veri


def denetle(yol: Path) -> list[str]:
    ham = yol.read_text(encoding="utf-8")
    s = Sayfa()
    s.feed(ham)
    h = []
    noindex = "noindex" in s.meta.get("robots", "")

    # --- Teknik ---
    if s.html_dil != "tr":
        h.append('html lang="tr" yok')
    if s.meta.get("charset", "").lower() != "utf-8":
        h.append("meta charset utf-8 yok")
    if "width=device-width" not in s.meta.get("viewport", ""):
        h.append("viewport eksik")
    baslik = s.baslik.strip()
    if not baslik:
        h.append("<title> yok")
    elif len(baslik) > BASLIK_AZAMI:
        h.append(f"title {len(baslik)} karakter (>{BASLIK_AZAMI})")
    elif len(baslik) < BASLIK_ASGARI:
        h.append(f"title {len(baslik)} karakter (<{BASLIK_ASGARI})")
    aciklama = s.meta.get("description", "").strip()
    if not aciklama:
        h.append("meta description yok")
    elif not noindex and not (ACIKLAMA_ARALIK[0] <= len(aciklama) <= ACIKLAMA_ARALIK[1]):
        h.append(f"meta description {len(aciklama)} karakter "
                 f"({ACIKLAMA_ARALIK[0]}-{ACIKLAMA_ARALIK[1]} olmalı)")
    if not s.link.get("canonical"):
        h.append("canonical yok")
    elif not s.link["canonical"].startswith(SITE):
        h.append("canonical site köküyle başlamıyor")
    if not s.meta.get("robots"):
        h.append("meta robots yok")
    if not s.meta.get("theme-color"):
        h.append("theme-color yok")
    if not s.link.get("icon"):
        h.append("favicon bağlantısı yok")
    if not s.link.get("stylesheet"):
        h.append("stylesheet bağlantısı yok")

    # --- Başlık hiyerarşisi ---
    h1ler = [m for d, m in s.hler if d == 1]
    if len(h1ler) != 1:
        h.append(f"{len(h1ler)} adet <h1> var (1 olmalı)")
    onceki = 0
    for derece, _ in s.hler:
        if onceki and derece > onceki + 1:
            h.append(f"başlık atlaması: h{onceki} → h{derece}")
            break
        onceki = derece
    for derece, metin in s.hler:
        if not metin:
            h.append(f"boş h{derece} başlığı")
            break

    # --- Paylaşım etiketleri ---
    for etiket in ("og:title", "og:description", "og:url", "og:image",
                   "og:type", "og:site_name", "og:locale"):
        if not s.meta.get(etiket):
            h.append(f"{etiket} yok")
    for etiket in ("twitter:card", "twitter:title", "twitter:description",
                   "twitter:image"):
        if not s.meta.get(etiket):
            h.append(f"{etiket} yok")
    if s.meta.get("og:image") and not s.meta.get("og:image:alt"):
        h.append("og:image:alt yok")
    if s.meta.get("og:url") and s.link.get("canonical") and \
            s.meta["og:url"] != s.link["canonical"]:
        h.append("og:url ile canonical farklı")

    # --- JSON-LD ---
    if not s.jsonld:
        h.append("JSON-LD yok")
    for blok in s.jsonld:
        try:
            veri = json.loads(blok)
        except json.JSONDecodeError as e:
            h.append(f"JSON-LD ayrıştırılamadı: {e}")
            continue
        if "@context" not in veri:
            h.append("JSON-LD @context yok")
        dugumler = veri.get("@graph", [veri])
        turler = {d.get("@type") for d in dugumler if isinstance(d, dict)}
        if "Organization" not in turler:
            h.append("JSON-LD Organization düğümü yok")
        for d in dugumler:
            if not isinstance(d, dict):
                continue
            if d.get("@type") in ("Article", "BlogPosting"):
                for alan in ("headline", "datePublished", "dateModified",
                             "author", "publisher", "image", "inLanguage"):
                    if alan not in d:
                        h.append(f"JSON-LD Article.{alan} yok")
                if len(d.get("headline", "")) > 110:
                    h.append("JSON-LD headline 110 karakteri aşıyor")
            if d.get("@type") == "FAQPage":
                for soru in d.get("mainEntity", []):
                    if not soru.get("acceptedAnswer", {}).get("text"):
                        h.append("FAQPage: cevapsız soru var")
                        break

    # --- Erişilebilirlik ve içerik ---
    for g in s.gorseller:
        kaynak = g.get("src", "?")
        if "alt" not in g:
            h.append(f"alt'sız görsel: {kaynak}")
        # Genişlik/yükseklik olmadan görsel yüklenirken sayfa zıplar (CLS).
        if not (g.get("width") and g.get("height")):
            h.append(f"görselde width/height yok: {kaynak}")
        if kaynak.startswith(("http://", "https://")):
            h.append(f"dış kaynaklı görsel: {kaynak}")
        yol_g = (yol.parent / kaynak.split("?")[0]).resolve()
        if not kaynak.startswith("http") and not yol_g.exists():
            h.append(f"görsel dosyası yok: {kaynak}")
    for sv in s.svgler:
        if sv.get("role") != "img":
            h.append("satır içi SVG'de role=\"img\" yok")
        if not sv.get("aria-labelledby"):
            h.append("satır içi SVG'de aria-labelledby yok")
    if s.tablolar and s.captionlar < s.tablolar:
        h.append(f"{s.tablolar} tablo, {s.captionlar} caption (her tabloya caption)")
    for href, metin in s.baglantilar:
        if not href.strip():
            h.append("boş href")
        if metin.lower() in ("buraya", "tıkla", "tıklayın", "buraya tıklayın",
                             "devamı", "link"):
            h.append(f"anlamsız bağlantı metni: {metin!r}")

    # --- Site içi bağlantı hedefleri ---
    for href, _ in s.baglantilar:
        if not href or href.startswith(("http://", "https://", "mailto:",
                                        "tel:", "#")):
            continue
        hedef_yol = urldefrag(href)[0].split("?")[0]
        if not hedef_yol:
            continue
        hedef = (yol.parent / hedef_yol).resolve()
        if not hedef.exists():
            h.append(f"kırık bağlantı: {href}")

    return h


def main() -> int:
    sessiz = "--sessiz" in sys.argv
    sayfalar = sorted(BLOG.rglob("*.html"))
    toplam_hata = 0
    for yol in sayfalar:
        hatalar = denetle(yol)
        toplam_hata += len(hatalar)
        ad = yol.relative_to(BLOG).as_posix()
        if hatalar:
            print(f"✗ {ad}")
            for x in hatalar:
                print(f"    {x}")
        elif not sessiz:
            print(f"✓ {ad}")

    # --- Site geneli ---
    genel = []
    harita = BLOG / "sitemap.xml"
    if not harita.exists():
        genel.append("blog/sitemap.xml yok")
    else:
        icerik = harita.read_text(encoding="utf-8")
        urller = set(re.findall(r"<loc>([^<]+)</loc>", icerik))
        for yol in sayfalar:
            ad = yol.relative_to(DOCS).as_posix()
            bekleniyor = SITE + "blog/" if ad == "blog/index.html" else SITE + ad
            if bekleniyor not in urller:
                genel.append(f"site haritasında yok: {ad}")
        for u in urller:
            if not u.startswith(SITE):
                genel.append(f"site haritasında yabancı URL: {u}")
    if not (DOCS / "assets" / "og.png").exists():
        genel.append("assets/og.png yok (paylaşım görseli)")
    if not (BLOG / "feed.xml").exists():
        genel.append("blog/feed.xml yok")
    if not (BLOG / "rehber.css").exists():
        genel.append("blog/rehber.css yok")

    if genel:
        print("✗ site geneli")
        for x in genel:
            print(f"    {x}")
    toplam_hata += len(genel)

    print(f"\n{len(sayfalar)} rehber sayfası denetlendi · {toplam_hata} bulgu")
    return 1 if toplam_hata else 0


if __name__ == "__main__":
    sys.exit(main())
