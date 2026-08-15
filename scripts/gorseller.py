# -*- coding: utf-8 -*-
"""
ŞEKİL KÜTÜPHANESİ — rehber yazılarına gömülen SVG çizimlerini üretir.

Neden satır içi SVG?
  · Dış istek yok — sitenin mahremiyet mimarisi bozulmaz.
  · Sayfa içinde olduğu için CSS değişkenlerini miras alır: koyu/açık tema
    ve kullanıcının tema seçimi çizime de uygulanır (ayrı .svg dosyası
    manuel tema seçimini takip edemezdi).
  · Şema başına ~2 kB; fotoğrafın yüzde biri. Hedef kitle düşük bant
    genişliğinde.

Renkler ve yazı tipleri `docs/blog/rehber.css` içindeki `.sekil` sınıflarıyla
verilir; burada yalnızca geometri ve sınıf adları vardır.

Beş şema tipi:
    sure()          gün/yıl uzunluklarını karşılaştıran yatay çubuklar
    kapsam()        kapsanan / açıkta kalan oranını gösteren yığılı çubuk
    akis()          numaralı adım akışı
    karsilastirma() iki sütunlu karşılaştırma
    eksen()         yıl ekseni üzerinde işaretli noktalar
"""

from __future__ import annotations

import html

G = 720          # tuval genişliği (içerik sütunuyla aynı ölçek)
KENAR = 4        # sol vurgu çubuğu kalınlığı


def _k(m: str) -> str:
    return html.escape(m, quote=True)


def _sar(kimlik: str, baslik: str, aciklama: str, yukseklik: int,
         govde: str) -> str:
    """SVG'yi erişilebilir bir kabuğa sarar."""
    return (
        f'<svg viewBox="0 0 {G} {yukseklik}" role="img" '
        f'aria-labelledby="{kimlik}-b {kimlik}-a" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<title id="{kimlik}-b">{_k(baslik)}</title>'
        f'<desc id="{kimlik}-a">{_k(aciklama)}</desc>'
        f'{govde}</svg>'
    )


def _metin(x, y, metin, sinif="s-metin", boyut=14, agirlik=None, hiza=None):
    ek = f' font-weight="{agirlik}"' if agirlik else ""
    ek += f' text-anchor="{hiza}"' if hiza else ""
    return (f'<text x="{x}" y="{y}" class="{sinif}" font-size="{boyut}"'
            f'{ek}>{_k(metin)}</text>')


# --- 1. Süre çubukları ------------------------------------------------------
def sure(kimlik: str, baslik: str, aciklama: str, kalemler: list[dict],
         birim: str = "gün") -> str:
    """kalemler: [{ad, deger, durum}] — durum: acil | normal | uzun"""
    satir_h = 44
    ust = 8
    yukseklik = ust + len(kalemler) * satir_h + 8
    en_buyuk = max(x["deger"] for x in kalemler)
    etiket_g = 250
    cubuk_g = G - etiket_g - 86

    p = []
    for i, kalem in enumerate(kalemler):
        y = ust + i * satir_h
        oran = kalem["deger"] / en_buyuk
        g = max(6, round(cubuk_g * oran))
        sinif = {"acil": "s-tehlike-dolgu", "normal": "s-uyari-dolgu"}.get(
            kalem.get("durum", "uzun"), "s-vurgu-dolgu")
        p.append(f'<rect x="0" y="{y + 8}" width="{KENAR}" height="24" '
                 f'class="{sinif}"/>')
        p.append(_metin(KENAR + 12, y + 25, kalem["ad"], "s-metin", 14))
        p.append(f'<rect x="{etiket_g}" y="{y + 12}" width="{g}" height="16" '
                 f'class="{sinif}"/>')
        p.append(_metin(etiket_g + g + 10, y + 25,
                        f'{kalem["deger"]} {birim}', "s-mono", 13))
        if i < len(kalemler) - 1:
            p.append(f'<line x1="0" y1="{y + satir_h}" x2="{G}" '
                     f'y2="{y + satir_h}" class="s-cizgi"/>')
    return _sar(kimlik, baslik, aciklama, yukseklik, "".join(p))


# --- 2. Kapsam çubuğu -------------------------------------------------------
def kapsam(kimlik: str, baslik: str, aciklama: str,
           dilimler: list[dict]) -> str:
    """dilimler: [{ad, deger, tur}] — tur: kapsanan | acikta"""
    toplam = sum(d["deger"] for d in dilimler)
    cubuk_y, cubuk_h = 8, 52
    p = []
    x = 0
    for d in dilimler:
        g = round(G * d["deger"] / toplam)
        sinif = "s-vurgu-dolgu" if d["tur"] == "kapsanan" else "s-tehlike-dolgu"
        p.append(f'<rect x="{x}" y="{cubuk_y}" width="{g}" height="{cubuk_h}" '
                 f'class="{sinif}"/>')
        if g > 90:
            p.append(f'<text x="{x + g / 2}" y="{cubuk_y + 32}" '
                     f'class="s-cubuk-yazi" font-size="13" font-weight="700" '
                     f'text-anchor="middle">'
                     f'{_k(str(round(100 * d["deger"] / toplam)))}%</text>')
        x += g

    y = cubuk_y + cubuk_h + 30
    for d in dilimler:
        sinif = "s-vurgu-dolgu" if d["tur"] == "kapsanan" else "s-tehlike-dolgu"
        p.append(f'<rect x="0" y="{y - 11}" width="12" height="12" class="{sinif}"/>')
        p.append(_metin(22, y, d["ad"], "s-metin", 14))
        p.append(_metin(G, y, d.get("yazi", ""), "s-mono", 13, hiza="end"))
        y += 26
    return _sar(kimlik, baslik, aciklama, y, "".join(p))


# --- 3. Adım akışı ----------------------------------------------------------
def akis(kimlik: str, baslik: str, aciklama: str, adimlar: list[dict]) -> str:
    """adimlar: [{ad, not, durum}] — durum: normal | uyari | tehlike"""
    kutu_h, aralik = 62, 18
    p = []
    y = 4
    for i, a in enumerate(adimlar):
        sinif = {"uyari": "s-uyari-dolgu", "tehlike": "s-tehlike-dolgu"}.get(
            a.get("durum", "normal"), "s-vurgu-dolgu")
        p.append(f'<rect x="0" y="{y}" width="{G}" height="{kutu_h}" '
                 f'class="s-kutu"/>')
        p.append(f'<rect x="0" y="{y}" width="{KENAR}" height="{kutu_h}" '
                 f'class="{sinif}"/>')
        p.append(f'<rect x="18" y="{y + 15}" width="26" height="26" '
                 f'class="{sinif}"/>')
        p.append(f'<text x="31" y="{y + 33}" class="s-cubuk-yazi" '
                 f'font-size="14" font-weight="700" text-anchor="middle">'
                 f'{i + 1}</text>')
        p.append(_metin(58, y + 27, a["ad"], "s-metin", 15, agirlik="650"))
        if a.get("not"):
            p.append(_metin(58, y + 47, a["not"], "s-mono", 12))
        if i < len(adimlar) - 1:
            oy = y + kutu_h
            p.append(f'<line x1="31" y1="{oy}" x2="31" y2="{oy + aralik - 5}" '
                     f'class="s-cizgi-kalin"/>')
            p.append(f'<path d="M27 {oy + aralik - 8} L31 {oy + aralik - 2} '
                     f'L35 {oy + aralik - 8} Z" class="s-ok"/>')
        y += kutu_h + aralik
    return _sar(kimlik, baslik, aciklama, y - aralik + 4, "".join(p))


# --- 4. İki sütunlu karşılaştırma -------------------------------------------
def karsilastirma(kimlik: str, baslik: str, aciklama: str, sol: str, sag: str,
                  satirlar: list[dict], sol_tur: str = "vurgu",
                  sag_tur: str = "tehlike") -> str:
    """satirlar: [{sol, sag}] — her satır iki sütunda birer ifade"""
    orta = G / 2
    sutun_g = orta - 12
    baslik_h = 40
    satir_h = 46
    yukseklik = baslik_h + len(satirlar) * satir_h + 6

    s_sinif = f"s-{sol_tur}-dolgu"
    g_sinif = f"s-{sag_tur}-dolgu"
    p = [f'<rect x="0" y="0" width="{sutun_g}" height="26" class="{s_sinif}"/>',
         f'<text x="10" y="18" class="s-cubuk-yazi" font-size="13" '
         f'font-weight="700">{_k(sol)}</text>',
         f'<rect x="{orta + 12}" y="0" width="{sutun_g}" height="26" '
         f'class="{g_sinif}"/>',
         f'<text x="{orta + 22}" y="18" class="s-cubuk-yazi" font-size="13" '
         f'font-weight="700">{_k(sag)}</text>']

    y = baslik_h
    for i, s in enumerate(satirlar):
        p.append(f'<rect x="0" y="{y}" width="{KENAR}" height="30" '
                 f'class="{s_sinif}"/>')
        p.append(_metin(KENAR + 10, y + 20, s["sol"], "s-metin", 13))
        p.append(f'<rect x="{orta + 12}" y="{y}" width="{KENAR}" height="30" '
                 f'class="{g_sinif}"/>')
        p.append(_metin(orta + 12 + KENAR + 10, y + 20, s["sag"], "s-metin", 13))
        if i < len(satirlar) - 1:
            p.append(f'<line x1="0" y1="{y + satir_h - 8}" x2="{G}" '
                     f'y2="{y + satir_h - 8}" class="s-cizgi"/>')
        y += satir_h
    return _sar(kimlik, baslik, aciklama, yukseklik, "".join(p))


# --- 5. Yıl ekseni ----------------------------------------------------------
def eksen(kimlik: str, baslik: str, aciklama: str,
          noktalar: list[dict]) -> str:
    """noktalar: [{yil, ad, not}] — yatay eksende işaretlenir"""
    sol, sag = 20, G - 20
    eksen_y = 96
    yillar = [n["yil"] for n in noktalar]
    en_az, en_cok = min(yillar), max(yillar)
    genislik = max(1, en_cok - en_az)

    p = [f'<line x1="{sol}" y1="{eksen_y}" x2="{sag}" y2="{eksen_y}" '
         f'class="s-cizgi-kalin"/>']
    for i, n in enumerate(noktalar):
        x = sol + (sag - sol) * (n["yil"] - en_az) / genislik
        vurgulu = n.get("vurgulu")
        sinif = "s-vurgu-dolgu" if vurgulu else "s-notr-dolgu"
        p.append(f'<rect x="{x - 5}" y="{eksen_y - 12}" width="10" height="24" '
                 f'class="{sinif}"/>')
        ust = i % 2 == 0
        ty = eksen_y - 28 if ust else eksen_y + 34
        hiza = "middle"
        if i == 0:
            hiza = "start"; x = max(x, sol)
        elif i == len(noktalar) - 1:
            hiza = "end"; x = min(x, sag)
        p.append(f'<text x="{x}" y="{ty}" class="s-mono" font-size="13" '
                 f'font-weight="700" text-anchor="{hiza}">{_k(str(n["yil"]))}</text>')
        p.append(f'<text x="{x}" y="{ty + (-18 if ust else 18)}" class="s-metin" '
                 f'font-size="13" text-anchor="{hiza}">{_k(n["ad"])}</text>')
    return _sar(kimlik, baslik, aciklama, eksen_y + 60, "".join(p))


URETICILER = {
    "sure": sure,
    "kapsam": kapsam,
    "akis": akis,
    "karsilastirma": karsilastirma,
    "eksen": eksen,
}


def ciz(slug: str, tanim: dict) -> str:
    """Şema tanımını SVG'ye çevirir."""
    tip = tanim["tip"]
    uretici = URETICILER[tip]
    veri = {a: d for a, d in tanim.items() if a not in ("tip", "altyazi")}
    return uretici(kimlik="sekil-" + slug, **veri)
