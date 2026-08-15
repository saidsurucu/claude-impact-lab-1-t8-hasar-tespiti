# -*- coding: utf-8 -*-
"""
YAZI ŞEMALARI — her rehber yazısının açılışına konan çizimin tanımı.

Anahtar: yazının slug'ı. Değer: `scripts/gorseller.py` içindeki şema
üreticilerine gönderilen tanım + `altyazi` (şeklin altındaki açıklama).

Kural: şema, yazının içindeki bir bilgiyi görselleştirir — süsleme değildir.
Aynı bilgi metinde ve tablolarda da bulunur; görsel hiç yüklenmese bile
sayfa eksik kalmaz.
"""

SEKILLER = {

    # --- Deprem sonrası ilk günler -----------------------------------------
    "deprem-sonrasi-ilk-30-gun": {
        "tip": "sure",
        "baslik": "Deprem sonrası hak düşürücü süreler",
        "aciklama": "DASK hasar ihbarı 15 gün, eksper raporuna itiraz 15 gün, "
                    "hasar tespitine itiraz 30 gün, DASK hasar dosyasına itiraz "
                    "30 gün, hak sahipliği başvurusu 60 gün, idari dava 60 gün.",
        "kalemler": [
            {"ad": "DASK hasar ihbarı", "deger": 15, "durum": "acil"},
            {"ad": "Eksper raporuna itiraz", "deger": 15, "durum": "acil"},
            {"ad": "Hasar tespitine itiraz", "deger": 30, "durum": "acil"},
            {"ad": "DASK hasar dosyasına itiraz", "deger": 30, "durum": "normal"},
            {"ad": "Hak sahipliği başvurusu", "deger": 60, "durum": "normal"},
            {"ad": "İdari dava açma", "deger": 60, "durum": "normal"},
        ],
        "altyazi": "Her sürenin başlangıcı farklıdır: ihbarda rizikoyu öğrenme, "
                   "hasar tespitinde mahallî ilan, hak sahipliğinde ilan tarihi "
                   "esas alınır.",
    },

    "hasar-tespitine-itiraz": {
        "tip": "akis",
        "baslik": "Hasar tespitine itiraz süreci",
        "aciklama": "Sonucun ilanı, 30 gün içinde itiraz, yeni teknik heyet "
                    "incelemesi, kesin tespit ve son çare olarak idari yargı.",
        "adimlar": [
            {"ad": "Sonuç mahallinde ilan edilir",
             "not": "30 günlük süre bu tarihte başlar"},
            {"ad": "Yazılı itiraz dilekçesi verilir",
             "not": "30 gün içinde · evrak kaydı alın", "durum": "uyari"},
            {"ad": "Farklı bir teknik heyet yeniden inceler",
             "not": "Fotoğraf ve teknik rapor dosyayı güçlendirir"},
            {"ad": "İkinci tespit KESİNDİR",
             "not": "İdari yolla üçüncü tespit yapılmaz", "durum": "tehlike"},
            {"ad": "Kalan tek yol: idari yargı",
             "not": "Kural olarak 60 gün içinde dava"},
        ],
        "altyazi": "İtiraz üzerine yapılan tespit kesin olduğu için dilekçe, "
                   "tek şans gibi hazırlanmalıdır.",
    },

    "dask-hasar-ihbari": {
        "tip": "sure",
        "baslik": "DASK sürecindeki süreler",
        "aciklama": "Muafiyette 72 saatlik hasar birleştirme penceresi, 15 günlük "
                    "hasar ihbarı, 15 günlük eksper raporuna itiraz ve 30 günlük "
                    "hasar dosyasına itiraz süresi.",
        "kalemler": [
            {"ad": "Hasar birleştirme penceresi", "deger": 3, "durum": "uzun"},
            {"ad": "DASK hasar ihbarı", "deger": 15, "durum": "acil"},
            {"ad": "Eksper raporuna itiraz", "deger": 15, "durum": "acil"},
            {"ad": "Hasar dosyasına itiraz", "deger": 30, "durum": "normal"},
        ],
        "altyazi": "72 saatlik pencere sigortalının lehinedir: kısa aralıklı iki "
                   "deprem tek hasar sayılır, muafiyet bir kez düşülür.",
    },

    "hasarli-binadan-esya-alma": {
        "tip": "karsilastirma",
        "baslik": "Bina durumuna göre eşya alma kuralı",
        "aciklama": "Yıkık ve acil yıktırılacak yapılara girmek yasaktır; ağır "
                    "hasarlı yapılarda eşya alımı uzman raporu ve ekip gözetimiyle "
                    "yapılır.",
        "sol": "YIKIK / ACİL YIKTIRILACAK",
        "sag": "AĞIR HASARLI",
        "sol_tur": "tehlike",
        "sag_tur": "uyari",
        "satirlar": [
            {"sol": "Girmek kesinlikle yasak", "sag": "Uzman raporuyla değerlendirilir"},
            {"sol": "Eşya alınamaz", "sag": "Ekip gözetiminde tahliye"},
            {"sol": "Yıkım süreci işler", "sag": "30 günlük itiraz süresine bağlı"},
        ],
        "altyazi": "Eşyayı hızla almak ile hasar tespitine itiraz etmek pratikte "
                   "çakışır; kararı bilerek verin.",
    },

    "olum-karinesi-ve-miras": {
        "tip": "karsilastirma",
        "baslik": "Ölüm karinesi ile gaiplik farkı",
        "aciklama": "Ölüm karinesi idari kararla işlenir ve süre beklemez; "
                    "gaiplik mahkeme kararı gerektirir ve kanuni süreleri bekler.",
        "sol": "ÖLÜM KARİNESİ · TMK m.31",
        "sag": "GAİPLİK · TMK m.32 vd.",
        "sol_tur": "vurgu",
        "sag_tur": "bilgi",
        "satirlar": [
            {"sol": "Mülkî idare amirinin emri", "sag": "Sulh hukuk mahkemesi kararı"},
            {"sol": "Süre şartı yok", "sag": "Kanuni süreler beklenir"},
            {"sol": "Miras hemen açılır", "sag": "Karardan sonra açılır"},
            {"sol": "Enkaz altında kaybolma", "sag": "Uzun süre haber alınamama"},
        ],
        "altyazi": "Depremde ölümüne kesin gözle bakılan bir kayıp için karine "
                   "yolu daha hızlıdır; mahkeme gerekmez.",
    },

    # --- DASK ve sigorta ----------------------------------------------------
    "dask-neleri-karsilamaz": {
        "tip": "karsilastirma",
        "baslik": "DASK neyi karşılar, neyi karşılamaz?",
        "aciklama": "DASK binayı sigortalar; ev eşyası, enkaz kaldırma, kira "
                    "kaybı, bedeni zararlar ve manevi tazminat teminat dışıdır.",
        "sol": "KARŞILAR",
        "sag": "KARŞILAMAZ",
        "sol_tur": "vurgu",
        "sag_tur": "tehlike",
        "satirlar": [
            {"sol": "Temel, kolon, ana duvarlar", "sag": "Ev eşyası, beyaz eşya"},
            {"sol": "Çatı, merdiven, asansör", "sag": "Enkaz kaldırma masrafı"},
            {"sol": "Depreme bağlı yangın, tsunami", "sag": "Kira kaybı, alternatif konut"},
            {"sol": "Depreme bağlı yer kayması", "sag": "Ölüm ve bedeni zararlar"},
        ],
        "altyazi": "Tek cümlelik özet: DASK binanızı sigortalar, hayatınızı değil.",
    },

    "dask-yeterli-mi": {
        "tip": "kapsam",
        "baslik": "Teminat açığı: 100 m² betonarme konut örneği",
        "aciklama": "Varsayılan 4.000.000 TL değerindeki konutta DASK sigorta "
                    "bedeli 1.071.400 TL, açıkta kalan tutar 2.928.600 TL.",
        "dilimler": [
            {"ad": "DASK sigorta bedeli", "deger": 1071400,
             "tur": "kapsanan", "yazi": "1.071.400 TL"},
            {"ad": "Açıkta kalan", "deger": 2928600,
             "tur": "acikta", "yazi": "2.928.600 TL"},
        ],
        "altyazi": "Üstüne %2 tenzili muafiyet (21.428 TL) düşülür; eşya, enkaz "
                   "ve barınma zaten teminat dışıdır. Değerler 01.05.2026 "
                   "tarifesine göredir.",
    },

    "daskim-yoksa-ne-olur": {
        "tip": "karsilastirma",
        "baslik": "Poliçesi olan ile olmayanın durumu",
        "aciklama": "Zorunlu deprem sigortası bulunmayanlara devlet konut yardımı "
                    "veya kredi ödenmediği belirtilmektedir.",
        "sol": "DASK VAR",
        "sag": "DASK YOK",
        "sol_tur": "vurgu",
        "sag_tur": "tehlike",
        "satirlar": [
            {"sol": "Bina hasarı teminata kadar ödenir", "sag": "Ödeme yapılmaz"},
            {"sol": "Devlet desteği değerlendirilir", "sag": "Konut yardımı/kredi yok"},
            {"sol": "Abonelik ve tapuda sorun yok", "sag": "İşlemlerde poliçe istenir"},
            {"sol": "Eşya ve can kaybı kapsam dışı", "sag": "Eşya ve can kaybı kapsam dışı"},
        ],
        "altyazi": "Asıl yaptırım para cezası değil, afet sonrası devlet desteğine "
                   "erişimin kaybedilmesidir.",
    },

    "eksper-raporuna-itiraz": {
        "tip": "akis",
        "baslik": "Eksper raporuna itiraz basamakları",
        "aciklama": "Rapor tebliği, 15 gün içinde yazılı itiraz, ikinci eksper, "
                    "hakem eksper ve sonucun bildirilmesi.",
        "adimlar": [
            {"ad": "Eksper raporu tebliğ edilir", "not": "Tebliğ tarihini hemen not edin"},
            {"ad": "15 gün içinde yazılı itiraz",
             "not": "Hangi kaleme neden katılmadığınızı yazın", "durum": "uyari"},
            {"ad": "İkinci eksper görevlendirilmesi", "not": "Talep etmeniz gerekir"},
            {"ad": "Raporlar çelişirse hakem eksper", "not": "Kararı nihai kabul edilir"},
            {"ad": "Sonuç: ek ödeme veya ret", "not": "Ret hâlinde yazılı başvuru ve tahkim yolu"},
        ],
        "altyazi": "Bağımsız eksper tutma hakkı da vardır: masrafı size ait olmak "
                   "üzere dilediğiniz eksperden rapor alabilirsiniz.",
    },

    "sigorta-uyusmazligi-tahkim-mahkeme": {
        "tip": "akis",
        "baslik": "Uyuşmazlıkta doğru sıra",
        "aciklama": "Önce sigorta şirketine yazılı başvuru (dava şartı), sonra "
                    "Sigorta Tahkim Komisyonu veya mahkeme; yol seçimi geri "
                    "dönüşsüzdür.",
        "adimlar": [
            {"ad": "Sigorta şirketine YAZILI başvuru",
             "not": "Dava şartı · atlanırsa dosya usulden reddedilir",
             "durum": "tehlike"},
            {"ad": "Şirketin yazılı cevabı", "not": "Gönderim kaydını saklayın"},
            {"ad": "Tahkim VEYA mahkeme",
             "not": "Bir yola gidilince diğeri kapanır", "durum": "uyari"},
            {"ad": "Zamanaşımı: 2 yıl",
             "not": "TTK m.1420 · her hâlde 6 yıl", "durum": "uyari"},
        ],
        "altyazi": "İlk üç basamak (eksper itirazı, ikinci eksper, DASK'a itiraz) "
                   "ücretsizdir ve çoğu dosya orada çözülür.",
    },

    # --- Kiracı hakları -----------------------------------------------------
    "kiraci-deprem-haklari": {
        "tip": "karsilastirma",
        "baslik": "Sistem kimi kapsıyor?",
        "aciklama": "DASK, hak sahipliği ve afet konutu mülkiyet ilişkisi arar; "
                    "tazminat davası aramaz.",
        "sol": "MALİK",
        "sag": "KİRACI",
        "sol_tur": "vurgu",
        "sag_tur": "uyari",
        "satirlar": [
            {"sol": "DASK tazminatı malike ödenir", "sag": "Kapsam dışı"},
            {"sol": "Hak sahipliği (7269)", "sag": "Kapsam dışı"},
            {"sol": "Afet konutu / faizsiz kredi", "sag": "Kapsam dışı"},
            {"sol": "Tazminat davası açabilir", "sag": "Tazminat davası açabilir"},
        ],
        "altyazi": "Son satır kiracının en güçlü ve en az bilinen hakkıdır: "
                   "tazminat davasında mülkiyet şartı yoktur.",
    },

    "kira-sozlesmesi-deprem": {
        "tip": "akis",
        "baslik": "Binanın durumuna göre üç yol",
        "aciklama": "Bina tamamen yıkıldıysa ifa imkânsızlığı, ağır hasarlıysa "
                    "önemli sebeple fesih, kullanılabilir durumdaysa ayıp "
                    "hükümleri devreye girer.",
        "adimlar": [
            {"ad": "Bina tamamen yıkıldı", "not": "İfa imkânsızlığı · TBK m.136 · sözleşme kendiliğinden sona erer"},
            {"ad": "Ağır hasarlı, oturulamaz", "not": "Önemli sebeple fesih · TBK m.331", "durum": "uyari"},
            {"ad": "Hasarlı ama kullanılabilir", "not": "Kira indirimi, onarım talebi · TBK m.305 vd."},
            {"ad": "Anahtar teslimini belgeleyin",
             "not": "Kira borcu fiilî iadeye kadar sürer", "durum": "tehlike"},
        ],
        "altyazi": "Fesih bildirimini yazılı yapın; noter, iadeli taahhütlü posta "
                   "veya imza karşılığı teslim kullanın.",
    },

    # --- Devlet desteği ve mülkiyet ----------------------------------------
    "hak-sahipligi-basvurusu": {
        "tip": "akis",
        "baslik": "Hak sahipliği zinciri",
        "aciklama": "Hasar tespitinin kesinleşmesi, ilan, iki ay içinde yazılı "
                    "talep ve taahhütname, karar ve ret hâlinde 15 günlük itiraz.",
        "adimlar": [
            {"ad": "Hasar tespiti kesinleşir", "not": "İtiraz süresi 30 gün"},
            {"ad": "Hak sahipliği ilanı yapılır", "not": "İki aylık süre bu tarihte başlar"},
            {"ad": "Yazılı talep + taahhütname",
             "not": "2 ay içinde · mahallin en büyük mülkî amirine", "durum": "uyari"},
            {"ad": "Kabul veya ret tebliğ edilir", "not": "Adres kaydınızı güncel tutun"},
            {"ad": "Ret hâlinde 15 gün içinde itiraz",
             "not": "Sonrasında idari yargı yolu", "durum": "tehlike"},
        ],
        "altyazi": "Borçlandırma en az 20, en çok 30 yıl ve faizsizdir; ilk taksit "
                   "genellikle teslimden iki yıl sonra başlar.",
    },

    "arsa-payi-ve-kat-mulkiyeti": {
        "tip": "akis",
        "baslik": "Bina yıkıldıktan sonra mülkiyet",
        "aciklama": "Kat mülkiyeti sona erer, arsa payı oranında paylı mülkiyet "
                    "kalır ve yeni bağımsız bölüm bu paya göre belirlenir.",
        "adimlar": [
            {"ad": "Ana yapı tamamen yıkılır", "not": "Mülkiyet yok olmaz, biçim değiştirir"},
            {"ad": "Kat mülkiyeti sona erer", "not": "KMK m.47 · tapuda re'sen terkin"},
            {"ad": "Arsa payı oranında paylı mülkiyet", "not": "Malikler adına payları oranında tescil"},
            {"ad": "Yeni daire arsa payına göre belirlenir",
             "not": "Metrekare, kat, cephe ve oy ağırlığı", "durum": "uyari"},
            {"ad": "Pay hatalıysa düzeltme davası",
             "not": "Her kat maliki açabilir · KMK m.3 ve m.44", "durum": "tehlike"},
        ],
        "altyazi": "Arsa payını bina ayaktayken kontrol etmek, yıkıldıktan sonra "
                   "hak kaybını önlemenin tek yoludur.",
    },

    "deprem-vergi-ve-emlak-vergisi": {
        "tip": "karsilastirma",
        "baslik": "Emlak vergisinde bildirimin sonucu",
        "aciklama": "Yıkılan veya kullanılamaz hâle gelen bina için mükellefiyetin "
                    "sona ermesi bildirime bağlıdır; bildirim yapılmazsa tahakkuk "
                    "devam eder.",
        "sol": "BİLDİRİM YAPILIRSA",
        "sag": "BİLDİRİM YAPILMAZSA",
        "sol_tur": "vurgu",
        "sag_tur": "tehlike",
        "satirlar": [
            {"sol": "Takip eden taksitten mükellefiyet biter", "sag": "Tahakkuk devam eder"},
            {"sol": "Kullanılamayan bina için vergi alınmaz", "sag": "Yıkık bina için ödeme sürer"},
            {"sol": "Muafiyet değerlendirilebilir", "sag": "Kayıt eski hâliyle kalır"},
        ],
        "altyazi": "Mücbir sebep ilanı süreleri durdurur; terkin ise ayrı bir "
                   "karara bağlıdır.",
    },

    # --- Dava yolları -------------------------------------------------------
    "muteahhit-sorumlulugu": {
        "tip": "sure",
        "birim": "yıl",
        "baslik": "Zamanaşımı süreleri",
        "aciklama": "Taşınmaz yapı dışındaki eserlerde 2 yıl, taşınmaz yapılarda "
                    "5 yıl, ilgili suçlarda 15 yıl, yüklenicinin ağır kusuru "
                    "hâlinde 20 yıl.",
        "kalemler": [
            {"ad": "Taşınmaz dışı eserler", "deger": 2, "durum": "normal"},
            {"ad": "Taşınmaz yapılar", "deger": 5, "durum": "normal"},
            {"ad": "Ceza davası zamanaşımı", "deger": 15, "durum": "uzun"},
            {"ad": "Ağır kusur hâlinde", "deger": 20, "durum": "uzun"},
        ],
        "altyazi": "Deprem davalarının neredeyse tamamı 20 yıllık süreye dayanır; "
                   "beş yıllık süre çoğu binada çoktan dolmuştur.",
    },

    "idare-ve-yapi-denetimi-sorumlulugu": {
        "tip": "sure",
        "baslik": "İdari yargı süreleri",
        "aciklama": "İdari başvuruya 30 gün içinde cevap verilmezse zımni ret "
                    "sayılır; iptal davası ve zımni ret sonrası dava süresi 60 "
                    "gündür.",
        "kalemler": [
            {"ad": "Cevap verilmezse zımni ret", "deger": 30, "durum": "acil"},
            {"ad": "İptal davası", "deger": 60, "durum": "normal"},
            {"ad": "Zımni ret sonrası dava", "deger": 60, "durum": "normal"},
        ],
        "altyazi": "Tam yargı davasında ayrıca eylemi öğrenmeden itibaren 1 yıl, "
                   "her hâlde 5 yıl içinde idareye ön başvuru gerekir.",
    },

    # --- Deprem öncesi ------------------------------------------------------
    "riskli-yapi-tespiti": {
        "tip": "akis",
        "baslik": "Riskli yapı tespiti süreci",
        "aciklama": "Tek malikin başvurusu, binadan numune alınması, raporun "
                    "bildirilmesi, 15 günlük itiraz ve riskli çıkması hâlinde "
                    "dönüşüm süreci.",
        "adimlar": [
            {"ad": "Malik lisanslı kuruluşa başvurur",
             "not": "Diğer maliklerin onayı GEREKMEZ · 6306 m.3"},
            {"ad": "Binadan numune alınır", "not": "Beton karotu, donatı taraması, taşıyıcı sistem"},
            {"ad": "Rapor Bakanlığa/İdareye bildirilir", "not": "Sonuç maliklere tebliğ edilir"},
            {"ad": "15 gün içinde itiraz edilebilir",
             "not": "Farklı bir teknik heyet yeniden inceler", "durum": "uyari"},
            {"ad": "Riskli çıkarsa tahliye ve dönüşüm",
             "not": "Kararlarda oy ağırlığı arsa payına bağlı", "durum": "tehlike"},
        ],
        "altyazi": "Masraf başvuran malike aittir; sonradan hisseleri oranında "
                   "maliklere dağıtıldığı belirtilmektedir.",
    },

    "imar-barisi-yapi-kayit-belgesi": {
        "tip": "karsilastirma",
        "baslik": "Yapı Kayıt Belgesi ne yapar, ne yapmaz?",
        "aciklama": "Belge mevcut kullanıma hukuki statü tanır; binanın depreme "
                    "dayanıklı olduğunu göstermez ve maliki sorumluluktan "
                    "kurtarmaz.",
        "sol": "YAPAR",
        "sag": "YAPMAZ",
        "sol_tur": "vurgu",
        "sag_tur": "tehlike",
        "satirlar": [
            {"sol": "Mevcut kullanıma hukuki statü", "sag": "Depreme dayanıklılığı göstermez"},
            {"sol": "Bazı işlemlerde kolaylık", "sag": "Maliki sorumluluktan kurtarmaz"},
            {"sol": "Yapıyı kayda alır", "sag": "İmar mevzuatına uygun hâle getirmez"},
            {"sol": "—", "sag": "Mühendislik hizmeti anlamına gelmez"},
        ],
        "altyazi": "Esaslı onarım yapılması hâlinde belgenin geçerliliğini "
                   "yitirdiği belirtilmektedir.",
    },

    "bina-yasi-ve-deprem-yonetmelikleri": {
        "tip": "eksen",
        "baslik": "Deprem yönetmeliği kuşakları",
        "aciklama": "1975 ve 1998 yönetmelikleri, 2001'de zorunlu yapı denetimi, "
                    "2007 yönetmeliği ve 2019'da yürürlüğe giren Türkiye Bina "
                    "Deprem Yönetmeliği.",
        "noktalar": [
            {"yil": 1975, "ad": "ABYYHY"},
            {"yil": 1998, "ad": "ABYYHY revizyon"},
            {"yil": 2001, "ad": "Yapı denetimi (4708)"},
            {"yil": 2007, "ad": "DBYBHY"},
            {"yil": 2019, "ad": "TBDY yürürlükte", "vurgulu": True},
        ],
        "altyazi": "2001 öncesi yapılar zorunlu yapı denetiminden geçmemiştir. "
                   "Eski dönemlerin Resmî Gazete tarihleri doğrulama bekliyor.",
    },
}
