#!/usr/bin/env python3
"""
FOTOĞRAF İNDİRİCİ — rehber yazılarının açılış görsellerini Pexels'ten indirir.

Neden indiriyoruz, bağlamıyoruz?
  Sitenin mahremiyet mimarisi gereği sayfa **hiçbir dış istek yapmaz**.
  Görsel uzaktan bağlanırsa okuyucunun IP'si üçüncü tarafa gider. Bu yüzden
  görseller bir kez indirilir, küçültülür ve depoya işlenir.

Lisans: Pexels lisansı ücretsiz kullanıma izin verir ve atıf zorunlu değildir;
yine de her görselin altına fotoğrafçı künyesi konur (şeffaflık + nezaket).

Kullanım:
    export PEXELS_ANAHTAR="..."          # anahtar repoya yazılmaz
    python3 scripts/foto-indir.py        # eksik olanları indir
    python3 scripts/foto-indir.py --yenile <slug> [<slug> ...]

Çıktı:
    docs/blog/gorseller/<slug>.jpg       1200x627, yazı açılışı ve og:image
    docs/blog/gorseller/kucuk/<slug>.jpg 360 piksel, rehber dizinindeki kartlar
    scripts/foto-kunye.json              fotoğrafçı/kaynak künyeleri (repoda)

Bağımlılık: yok (standart kütüphane + macOS `sips`).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
GORSEL_DIZIN = KOK / "docs" / "blog" / "gorseller"
KUNYE_DOSYA = Path(__file__).resolve().parent / "foto-kunye.json"

# Yazı başına arama sorgusu ve Türkçe alt metin (alt).
# Sorgu İngilizcedir; Pexels'in dizini böyle çalışıyor.
ARAMALAR = {
    "deprem-sonrasi-ilk-30-gun": (
        "earthquake destroyed building rubble",
        "Depremde yıkılmış bir binanın enkazı"),
    "hasar-tespitine-itiraz": (
        "cracked concrete wall damage",
        "Betonarme bir duvarda oluşmuş derin çatlak"),
    "dask-hasar-ihbari": (
        "damaged house insurance inspection",
        "Hasar görmüş bir konutta yapılan sigorta incelemesi"),
    "hasarli-binadan-esya-alma": (
        "packed cardboard boxes empty room",
        "Boşaltılmış bir odada üst üste dizilmiş karton kolilar"),
    "olum-karinesi-ve-miras": (
        "old documents archive folders",
        "Arşivde sıralanmış resmî belge klasörleri"),
    "dask-neleri-karsilamaz": (
        "living room furniture home interior",
        "Ev eşyalarıyla döşenmiş bir oturma odası"),
    "dask-yeterli-mi": (
        "calculator financial documents desk",
        "Hesap makinesi ve üzerinde çalışılan mali belgeler"),
    "daskim-yoksa-ne-olur": (
        "residential apartment buildings city",
        "Şehirde yan yana sıralanmış konut blokları"),
    "eksper-raporuna-itiraz": (
        "engineer inspecting building clipboard",
        "Elinde raporla bina inceleyen bir mühendis"),
    "sigorta-uyusmazligi-tahkim-mahkeme": (
        "courthouse justice law columns",
        "Sütunlu bir adliye binasının cephesi"),
    "kiraci-deprem-haklari": (
        "apartment door key hand tenant",
        "Bir konutun kapısında anahtar tutan el"),
    "kira-sozlesmesi-deprem": (
        "rental contract keys signing",
        "İmzalanan kira sözleşmesi ve ev anahtarları"),
    "hak-sahipligi-basvurusu": (
        "government office building application",
        "Resmî bir kurum binası ve başvuru bankosu"),
    "arsa-payi-ve-kat-mulkiyeti": (
        "architecture blueprint plan drawing",
        "Masaya serilmiş mimari proje çizimleri"),
    "deprem-vergi-ve-emlak-vergisi": (
        "tax documents paperwork calculator",
        "Vergi belgeleri, hesap makinesi ve kalem"),
    "muteahhit-sorumlulugu": (
        "construction site rebar concrete column",
        "İnşaat hâlindeki betonarme kolon ve donatı demirleri"),
    "idare-ve-yapi-denetimi-sorumlulugu": (
        "construction inspection safety helmet site",
        "Şantiyede denetim yapan baretli görevliler"),
    "riskli-yapi-tespiti": (
        "engineer measuring building structure",
        "Bina taşıyıcı sistemini ölçen bir mühendis"),
    "imar-barisi-yapi-kayit-belgesi": (
        "unfinished concrete building city",
        "Tamamlanmamış betonarme bir yapı"),
    "bina-yasi-ve-deprem-yonetmelikleri": (
        "old apartment buildings street",
        "Sokakta sıralanmış eski apartmanlar"),
}


def api(anahtar: str, sorgu: str, sayfa: int = 1) -> dict:
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode({
        "query": sorgu, "per_page": "5", "page": str(sayfa),
        "orientation": "landscape", "size": "large",
    })
    istek = urllib.request.Request(url, headers={
        "Authorization": anahtar,
        # HTTP başlıkları latin-1 ile kodlanır; ASCII dışına çıkmayın.
        "User-Agent": "DepremHaklarim/0.1 (nonprofit info platform)",
    })
    with urllib.request.urlopen(istek, timeout=30) as f:
        return json.load(f)


def indir(url: str, hedef: Path) -> None:
    istek = urllib.request.Request(url, headers={"User-Agent": "DepremHaklarim/0.1"})
    with urllib.request.urlopen(istek, timeout=60) as f:
        hedef.write_bytes(f.read())


AZAMI_BAYT = 160 * 1024


def kucult(yol: Path) -> None:
    """1200 piksel genişlik, düşük dosya boyutu. Hedef kitle 2G'de olabilir.

    Detaylı fotoğraflar (enkaz, doku) ilk geçişte büyük kalıyor; sınırı aşan
    dosyalar daha düşük kalitede yeniden sıkıştırılır."""
    for kalite in ("58", "42"):
        subprocess.run(["sips", "-s", "format", "jpeg",
                        "-s", "formatOptions", kalite,
                        "--resampleWidth", "1200", str(yol), "--out", str(yol)],
                       check=True, capture_output=True)
        if yol.stat().st_size <= AZAMI_BAYT:
            return


def kucuk_uret(yol: Path) -> None:
    """Rehber dizinindeki kartlar için küçük kopya (~15 kB)."""
    hedef = yol.parent / "kucuk" / yol.name
    hedef.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "45",
                    "--resampleWidth", "360", str(yol), "--out", str(hedef)],
                   check=True, capture_output=True)


def main() -> int:
    anahtar = os.environ.get("PEXELS_ANAHTAR", "").strip()
    if not anahtar:
        print("PEXELS_ANAHTAR ortam değişkeni gerekli "
              "(pexels.com/api adresinden ücretsiz alınır).", file=sys.stderr)
        return 1

    yenile = set(sys.argv[2:]) if "--yenile" in sys.argv else set()
    GORSEL_DIZIN.mkdir(parents=True, exist_ok=True)
    kunye = json.loads(KUNYE_DOSYA.read_text(encoding="utf-8")) \
        if KUNYE_DOSYA.exists() else {}

    for slug, (sorgu, alt) in ARAMALAR.items():
        hedef = GORSEL_DIZIN / f"{slug}.jpg"
        if hedef.exists() and slug not in yenile:
            print(f"  atlandı (var): {slug}")
            continue

        sonuc = api(anahtar, sorgu)
        secenekler = sonuc.get("photos", [])
        if not secenekler:
            print(f"  ✗ sonuç yok: {slug} ({sorgu})", file=sys.stderr)
            continue
        # --yenile ile aynı slug tekrar istendiğinde sıradaki adayı seç
        sira = kunye.get(slug, {}).get("sira", -1) + 1 if slug in yenile else 0
        foto = secenekler[sira % len(secenekler)]

        indir(foto["src"]["landscape"], hedef)
        kucult(hedef)
        kucuk_uret(hedef)
        kunye[slug] = {
            "kaynak": "Pexels",
            "fotografci": foto.get("photographer", ""),
            "fotografci_adres": foto.get("photographer_url", ""),
            "sayfa": foto.get("url", ""),
            "kimlik": foto.get("id"),
            "sorgu": sorgu,
            "alt": alt,
            "sira": sira,
            "genislik": 1200,
            "yukseklik": 627,
        }
        print(f"  ✓ {slug}: {foto.get('photographer','?')} · "
              f"{hedef.stat().st_size // 1024} kB")

    KUNYE_DOSYA.write_text(
        json.dumps(kunye, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n{len(kunye)} künye yazıldı: {KUNYE_DOSYA.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
