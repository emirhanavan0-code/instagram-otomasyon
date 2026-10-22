"""23–31 Ekim 2026: günde 3 gönderi (reels + carousel + kısa not). Reels ve carousel içerikleri.
Kısa notlar ayrı (notlar_44.py). Çalıştır: python3 araclar/hafta_44.py"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SON = "🔗 Detaylar: seovedijital.com\n📞 0501 048 3732"


def kaydet(d):
    d.setdefault("durum", "taslak")
    p = ROOT / "icerik" / f"{d['id']}.json"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    print("✓", d["id"])


def acik(*satirlar, etiket):
    return "\n\n".join(satirlar) + "\n\n" + SON + "\n\n" + etiket


ICERIK = [
    # ---------------- 24 Ekim ----------------
    dict(id="2026-10-24-trendyol-varyant-hatalari", tur="carousel", stil="zumrut", yayin_zamani="2026-10-24T12:30:00+03:00",
         aciklama=acik("Aynı ürünün 5 rengi için 5 ayrı sayfa mı açtınız? 🎨",
                       "Varyantlar doğru kurulmazsa yorumlar bölünür, ürün aramada dağılır, müşteri istediği bedeni bulamaz.",
                       "Yayına almadan önce bu 4 hatayı kontrol edin.",
                       "📌 Kaydedin, yeni ürün eklerken açıp bakın.",
                       etiket="#trendyol #trendyolsatıcı #varyant #eticaret #pazaryeri #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Trendyol · Ürün Sayfası", baslik="5 renk, 5 sayfa mı? *Yanlış.*", alt="Varyant kurarken en sık yapılan 4 hata."),
             dict(tip="madde", no=1, baslik="Her rengi *ayrı ürün* açmak", metin="Aynı modelin renk ve bedenleri **tek ürün altında** toplanmalı. Böylece yorumlar ve satış geçmişi bölünmez.", liste=["Tek model kodu", "Renk / beden seçeneği"]),
             dict(tip="madde", no=2, baslik="Tüm varyantlara *aynı görsel*", metin="Kırmızıyı seçen müşteri kırmızıyı görmeli. Yanlış görsel, **iade** olarak geri döner."),
             dict(tip="madde", no=3, baslik="Barkodları *karıştırmak*", metin="Her varyantın kendi barkodu olmalı. Karışırsa yanlış ürün gönderilir, stok sayımı bozulur."),
             dict(tip="madde", no=4, baslik="Popüler bedende *stok bitmesi*", metin="Sayfa açık ama en çok aranan beden yoksa satış kaçar. Stoğu **varyant bazında** takip edin.", liste=["Haftalık kontrol", "Kritik beden uyarısı"]),
             dict(tip="cta", ust="Trendyol Ürün Analizi", baslik="Ürün sayfalarınızı *birlikte* düzenleyelim", aciklama="Varyant, görsel ve başlık yapınızı inceleyip öncelik listesi çıkarıyoruz."),
         ]),
    dict(id="2026-10-25-trendyol-iade-maliyeti", tur="reels", stil="gece", muzik="lofi", yayin_zamani="2026-10-25T15:00:00+03:00",
         aciklama=acik("Bir iade size sadece satışı değil, daha fazlasını kaybettirir. 📦",
                       "Gidiş kargosu, dönüş kargosu, paketleme ve bazen tekrar satılamayan ürün. Hepsi ayrı bir gider.",
                       "İade oranınızı bilmeden gerçek kârınızı bilemezsiniz.",
                       "📌 Kaydedin, ay sonu hesabında kullanın.",
                       etiket="#trendyol #iade #eticaret #trendyolsatıcı #kârhesabı #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Trendyol · Kâr Hesabı", baslik="Bir iade size *kaça* mal oluyor?", alt="Çoğu satıcı bu kalemleri hesaba katmıyor.", sure=3.5),
             dict(tip="madde", no=1, baslik="İki yönlü *kargo*", metin="Ürün gider, geri gelir. **Dönüş kargosu** da çoğu zaman sizin cebinizden çıkar.", sure=4),
             dict(tip="madde", no=2, baslik="Paketleme ve *emek*", metin="Kutu, poşet, etiket ve iadeyi kontrol etmek için harcanan zaman.", sure=4),
             dict(tip="madde", no=3, baslik="Satılamayan *ürün*", metin="Açılmış, hasarlı ya da sezonu geçmiş ürün **tekrar aynı fiyata** satılmayabilir.", sure=4),
             dict(tip="alinti", ust="Pratik kural", baslik="Kârı *iade oranıyla* birlikte hesaplayın", metin="Sipariş başı kârınızdan, iade oranınız kadar iade maliyetini düşün. Ay sonunda kalan **gerçek kârdır**.", sure=4.5),
             dict(tip="cta", ust="Trendyol Satış Artırma", baslik="Kârınızı eriten ürünleri *bulalım*", aciklama="Mağazanızın iade ve kâr tablosunu birlikte çıkarıyoruz.", sure=4),
         ]),
    dict(id="2026-10-25-google-isletme-profili", tur="carousel", stil="altin", yayin_zamani="2026-10-25T19:00:00+03:00",
         aciklama=acik("\"Yakınımdaki ...\" diye arayan müşteri sizi buluyor mu? 📍",
                       "Yerel aramalarda ilk izlenim çoğu zaman web siteniz değil, Google İşletme Profilinizdir.",
                       "5 dakikada kontrol edebileceğiniz 5 nokta.",
                       "📌 Kaydedin, profilinizi açıp tek tek bakın.",
                       etiket="#yerelseo #googleişletmeprofili #seo #ankaraseo #kobi #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Yerel SEO", baslik="Haritada *görünmüyorsanız* yoksunuz", alt="Google İşletme Profili için 5 dakikalık kontrol."),
             dict(tip="madde", no=1, baslik="Doğru *kategori*", metin="Ana kategori, insanların sizi aradığı kelimeyle örtüşmeli. Gerekirse **ek kategoriler** ekleyin."),
             dict(tip="madde", no=2, baslik="Ad, adres, telefon *aynı*", metin="Sitenizde, profilinizde ve diğer rehberlerde bilgiler **birebir aynı** yazılmalı."),
             dict(tip="madde", no=3, baslik="Güncel *fotoğraflar*", metin="Mekân, ekip ve işiniz. Müşteri gelmeden önce nereye geleceğini görmek ister.", liste=["Dış cephe", "İç mekân", "Ekip", "Ürün / hizmet"]),
             dict(tip="madde", no=4, baslik="Yorumlara *cevap*", metin="Olumlu ya da olumsuz, her yoruma kısa ve kibar bir cevap verin. Yeni müşteri bunu okur."),
             dict(tip="madde", no=5, baslik="Düzenli *gönderi*", metin="Kampanya, yeni hizmet, duyuru. Profilin **canlı** olduğunu gösterir."),
             dict(tip="cta", ust="Yerel SEO", baslik="Mahallenizde *ilk sırada* çıkın", aciklama="Profilinizi ve yerel görünürlüğünüzü birlikte düzenliyoruz."),
         ]),
    # ---------------- 26 Ekim ----------------
    dict(id="2026-10-26-sozluk-3-terim", tur="reels", stil="altin", muzik="pozitif", yayin_zamani="2026-10-26T12:30:00+03:00",
         aciklama=acik("SEO toplantısında duyduğunuz terimlere yabancı mı kaldınız? 📖",
                       "30 saniyede 3 terim. Daha fazlası ücretsiz SEO, GEO ve Trendyol sözlüğümüzde, sade Türkçe ile.",
                       "📌 Kaydedin, ekibinizle paylaşın.",
                       etiket="#seo #geo #sözlük #dijitalpazarlama #yapayzeka #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Sözlük · 30 Saniye", baslik="3 terim, *30 saniye*", alt="Toplantıda duyup sormaya çekindikleriniz.", sure=3),
             dict(tip="alinti", ust="AI Overviews", baslik="Google'ın *yapay zekâ özeti*", metin="Bazı aramalarda sonuçların üstünde çıkan, yapay zekâyla yazılmış **özet cevap ve kaynaklar**.", sure=4.5),
             dict(tip="alinti", ust="GEO", baslik="Yapay zekâ cevaplarında *görünmek*", metin="Markanızın ChatGPT, Gemini gibi araçların **cevaplarında kaynak** olarak geçmesi için yapılan çalışma.", sure=4.5),
             dict(tip="alinti", ust="Schema", baslik="Sayfanın *makine dili*", metin="Sayfadaki bilgiyi (fiyat, adres, SSS) arama motorlarının **net anlayacağı** biçimde işaretleyen kod.", sure=4.5),
             dict(tip="cta", ust="Ücretsiz Sözlük", baslik="Gerisi *sözlükte*", aciklama="SEO, GEO ve Trendyol terimleri sade Türkçe ile tek sayfada.", eylem="seovedijital.com/sozluk", sure=4),
         ]),
    dict(id="2026-10-26-trendyol-stok-yonetimi", tur="carousel", stil="kor", yayin_zamani="2026-10-26T19:00:00+03:00",
         aciklama=acik("En pahalı stok, bitmiş olan stoktur. 📦",
                       "Kasım'da tükenen ürün, en çok satacağı günlerde satış kaçırır.",
                       "3 basit kavramla stoğunuzu planlayın.",
                       "📌 Kaydedin, haftalık stok kontrolünde kullanın.",
                       etiket="#trendyol #stokyönetimi #kasımindirimleri #eticaret #trendyolsatıcı #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Trendyol · Kasım Hazırlığı", baslik="Stok bitti, *satış da* bitti", alt="Kampanya öncesi 3 basit stok hesabı."),
             dict(tip="madde", no=1, baslik="Stok *gün sayısı*", metin="Elinizdeki stok ÷ günlük ortalama satış. Bu sayı **tedarik sürenizden** kısaysa risk var."),
             dict(tip="madde", no=2, baslik="Yeniden *sipariş noktası*", metin="Stok bu seviyeye inince siparişi verin. Tedarik süresi boyunca satılacak miktar + **güvenlik payı**."),
             dict(tip="madde", no=3, baslik="Kampanya *çarpanı*", metin="İndirim döneminde satış normalden yüksek olur. Geçen yılın aynı dönemine bakıp **stok hedefini** buna göre büyütün.", liste=["Geçen yıl verisi", "Tedarikçi teyidi"]),
             dict(tip="madde", no=4, baslik="Fazla stok da *sorun*", metin="Satılmayan ürün nakdi bağlar. Az satanları **kampanyayla** eritin, çok satanlara odaklanın."),
             dict(tip="cta", ust="Trendyol Mağaza Yönetimi", baslik="Kasım planınızı *birlikte* kuralım", aciklama="Stok, fiyat ve reklam planınızı rakamlarla hazırlıyoruz."),
         ]),
    # ---------------- 27 Ekim ----------------
    dict(id="2026-10-27-llms-txt-nedir", tur="carousel", stil="gece", yayin_zamani="2026-10-27T12:30:00+03:00",
         aciklama=acik("Yapay zekâya sitenizin haritasını verebilirsiniz: llms.txt 🤖",
                       "llms.txt, sitenizin kökünde duran ve yapay zekâ araçlarına önemli sayfalarınızı özetleyen basit bir metin dosyası.",
                       "Henüz bir standart değil, bir öneri. Ama hazırlaması kolay ve zararsız.",
                       "📌 Kaydedin, siteniz için not alın.",
                       etiket="#geo #llmstxt #yapayzeka #seo #chatgpt #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="GEO · Teknik", baslik="llms.txt *nedir?*", alt="Yapay zekâya sitenizi anlatan küçük dosya."),
             dict(tip="alinti", ust="Tanım", baslik="Yapay zekâ için *site özeti*", metin="Sitenizin kökünde (**/llms.txt**) duran, markanızı ve en önemli sayfalarınızı kısa başlıklarla anlatan bir Markdown dosyası."),
             dict(tip="madde", no=1, baslik="robots.txt'ten *farkı*", metin="robots.txt neyin taranacağını söyler. llms.txt ise **neyin önemli olduğunu** anlatır."),
             dict(tip="madde", no=2, baslik="İçine *ne yazılır?*", liste=["Marka tanımı", "Hizmet sayfaları", "Sık sorulanlar", "İletişim"]),
             dict(tip="madde", no=3, baslik="Gerçekçi *beklenti*", metin="Bir **öneri standardı**; her yapay zekâ aracının okuduğu garanti değil. Asıl iş yine net ve güvenilir içerik."),
             dict(tip="cta", ust="GEO · Yapay Zekâ Görünürlüğü", baslik="Yapay zekâda *görünür* olun", aciklama="llms.txt, schema ve içerik yapınızı yapay zekâ aramalarına hazırlıyoruz."),
         ]),
    dict(id="2026-10-27-urun-gorseli", tur="reels", stil="", muzik="sinematik", yayin_zamani="2026-10-27T19:00:00+03:00",
         aciklama=acik("Müşteri ürününüzü önce görür, sonra okur. 📸",
                       "Arama sonucunda tıklanıp tıklanmayacağınızı çoğu zaman ana görsel belirler.",
                       "Telefonla bile doğru çekilmiş bir görsel seti fark yaratır.",
                       "📌 Kaydedin, yeni ürün çekiminden önce bakın.",
                       etiket="#trendyol #ürüngörseli #eticaret #trendyolsatıcı #ürünfotoğrafı #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Trendyol · Ürün Görseli", baslik="Görsel kötüyse *kimse okumaz*", alt="Satan bir görsel setinin 4 kuralı.", sure=3.5),
             dict(tip="madde", no=1, baslik="Ana görsel *sade* olsun", metin="Ürün net, ortada ve kalabalıksız. Arama sonucunda **küçük boyutta** da anlaşılmalı.", sure=4),
             dict(tip="madde", no=2, baslik="Ölçü ve *detay* gösterin", metin="Boyut, doku, dikiş, etiket. Belirsizlik **iade** olarak geri döner.", sure=4),
             dict(tip="madde", no=3, baslik="Kullanım *anı* ekleyin", metin="Ürün gerçek hayatta nasıl duruyor? Müşteri kendini onunla hayal etmeli.", sure=4),
             dict(tip="madde", no=4, baslik="Gün ışığında *çekin*", metin="Pahalı ekipman şart değil. Pencere ışığı ve sabit bir zemin çoğu ürün için yeterli.", sure=4),
             dict(tip="cta", ust="Trendyol Ürün Analizi", baslik="Ürün sayfalarınızı *analiz edelim*", aciklama="Görsel, başlık ve açıklamalarınız için öncelik listesi çıkarıyoruz.", sure=4),
         ]),
    # ---------------- 28 Ekim ----------------
    dict(id="2026-10-28-trendyolda-ne-satilir", tur="reels", stil="kor", muzik="trap", yayin_zamani="2026-10-28T12:30:00+03:00",
         aciklama=acik("\"Trendyol'da ne satsam?\" sorusunun cevabı tek bir ürün değil, bir yöntem. 🧭",
                       "Talep, rekabet, kâr payı, kargo ve iade riski. Bir ürüne karar vermeden önce bu 4 soruyu sorun.",
                       "📌 Kaydedin, yeni ürün kararından önce bakın.",
                       etiket="#trendyol #trendyoldanesatılır #eticaret #yenisatıcı #pazaryeri #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Trendyol · Yeni Satıcı", baslik="Ne satacağınızı *4 soruyla* seçin", alt="Doğru ürün, işin yarısıdır.", sure=3.5),
             dict(tip="madde", no=1, baslik="Aranıyor *mu?*", metin="Ürün aramalarda ve rakip yorumlarında **gerçekten talep** görüyor mu?", sure=3.8),
             dict(tip="madde", no=2, baslik="Kaç kişi *satıyor?*", metin="Aynı ürünü onlarca satıcı satıyorsa fiyat savaşına girersiniz.", sure=3.8),
             dict(tip="madde", no=3, baslik="Komisyon sonrası *kâr* kalıyor mu?", metin="Komisyon, kargo, KDV ve reklam düşünce **elde kalan** rakama bakın.", sure=4),
             dict(tip="madde", no=4, baslik="Kargo ve *iade* riski", metin="Kırılgan, büyük ya da beden sorunu çok olan ürünler ek maliyet getirir.", sure=3.8),
             dict(tip="cta", ust="Trendyol Satış Artırma", baslik="Doğru kategoriyle *başlayın*", aciklama="Ürün ve kategori seçiminizi rakamlarla birlikte değerlendiriyoruz.", sure=4),
         ]),
    dict(id="2026-10-28-schema-rehberi", tur="carousel", stil="zumrut", yayin_zamani="2026-10-28T19:00:00+03:00",
         aciklama=acik("Sayfanızı makinelere kendi dillerinde anlatın. 🧩",
                       "Yapılandırılmış veri (schema), Google'ın ve yapay zekâ araçlarının sayfanızdaki bilgiyi doğru okumasına yardım eder.",
                       "İşletmeler için en önemli 4 tür.",
                       "📌 Kaydedin, sitenizi kontrol ederken kullanın.",
                       etiket="#seo #schema #yapılandırılmışveri #teknikseo #geo #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Teknik SEO", baslik="Schema nedir, *neden* önemli?", alt="İşletmeler için en önemli 4 tür."),
             dict(tip="alinti", ust="Tanım", baslik="Sayfanın *etiketleri*", metin="Sayfadaki adres, fiyat, yorum, SSS gibi bilgileri **standart bir dille** işaretleyen kod. Ziyaretçi görmez, arama motorları okur."),
             dict(tip="madde", no=1, baslik="LocalBusiness", metin="Adres, telefon, çalışma saatleri. **Yerel işletmeler** için temel."),
             dict(tip="madde", no=2, baslik="Product", metin="Ürün adı, fiyat, stok durumu. **E-ticaret siteleri** için."),
             dict(tip="madde", no=3, baslik="FAQPage", metin="Sık sorulan sorular ve cevapları. Sayfadaki bilginin **soru-cevap** olarak anlaşılmasına yardım eder."),
             dict(tip="madde", no=4, baslik="Article", metin="Blog yazılarında yazar, tarih ve konu bilgisi."),
             dict(tip="cta", ust="Teknik Altyapı", baslik="Teknik altyapınızı *kontrol edelim*", aciklama="Schema, hız ve taranabilirlik durumunuzu inceleyip yol haritası çıkarıyoruz."),
         ]),
    # ---------------- 29 Ekim ----------------
    dict(id="2026-10-29-cumhuriyet-bayrami", tur="gorsel", stil="kor", yayin_zamani="2026-10-29T10:00:00+03:00",
         aciklama="Cumhuriyetimizin 103. yılı kutlu olsun. 🇹🇷\n\nGazi Mustafa Kemal Atatürk ve silah arkadaşlarını saygı, minnet ve özlemle anıyoruz.\n\n#29ekim #cumhuriyetbayramı #cumhuriyet103yaşında #seovedijital",
         slaytlar=[dict(tip="alinti", ust="29 Ekim 1923 · 2026", baslik="Cumhuriyetimizin *103. yılı* kutlu olsun", metin="Atatürk ve silah arkadaşlarını **saygı, minnet ve özlemle** anıyoruz.")]),
    dict(id="2026-10-29-seovedijital-ne-yapar", tur="reels", stil="gece", muzik="ambient", yayin_zamani="2026-10-29T19:00:00+03:00",
         aciklama=acik("Müşteriniz sizi nerede arıyor? Google'da, yapay zekâda, Trendyol'da. 🔎",
                       "Seovedijital olarak bu üç kanalı tek planda yönetiyoruz: SEO, GEO ve pazaryeri. Ankara'dan, KOBİ ve e-ticaret satıcıları için.",
                       "Her ay ne yaptığımızı ve ne değiştiğini açıkça raporluyoruz.",
                       etiket="#seo #geo #trendyol #ankaraseo #dijitalajans #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Seovedijital", baslik="Müşteriniz sizi *nerede* arıyor?", alt="Üç kanal, tek plan.", sure=3.5),
             dict(tip="madde", no=1, baslik="Google'da *SEO*", metin="Hizmetinizi arayan kişi sizi **ilk sayfada** bulsun.", liste=["Teknik SEO", "İçerik", "Yerel SEO"], sure=4.2),
             dict(tip="madde", no=2, baslik="Yapay zekâda *GEO*", metin="ChatGPT ve Gemini cevaplarında markanız **kaynak** olarak geçsin.", liste=["Schema", "llms.txt", "Marka sinyali"], sure=4.2),
             dict(tip="madde", no=3, baslik="Trendyol'da *satış*", metin="Ürün sayfası, reklam ve kampanya planıyla mağazanız **kârlı** büyüsün.", liste=["Ürün SEO", "Reklam", "Kampanya"], sure=4.2),
             dict(tip="alinti", ust="Nasıl çalışıyoruz?", baslik="Önce *ücretsiz* ön analiz", metin="Mevcut durumunuzu çıkarıyor, neyin önce yapılacağını gösteriyoruz. Sonra her ay **şeffaf rapor**.", sure=4.5),
             dict(tip="cta", ust="Ücretsiz Ön Analiz", baslik="Nereden başlayacağınızı *birlikte* görelim", aciklama="SEO, GEO ve Trendyol durumunuzu tek raporda çıkarıyoruz.", sure=4),
         ]),
    # ---------------- 30 Ekim ----------------
    dict(id="2026-10-30-pazaryeri-bagimliligi", tur="reels", stil="zumrut", muzik="pozitif", yayin_zamani="2026-10-30T12:30:00+03:00",
         aciklama=acik("Tüm satışlarınız tek pazaryerinden mi geliyor? 🧺",
                       "Komisyon değişir, kural değişir, hesap askıya alınabilir. Tek kanala bağlı kalmak risklidir.",
                       "Kendi siteniz pazaryerinin rakibi değil, sigortasıdır.",
                       "📌 Kaydedin, ekibinizle konuşun.",
                       etiket="#eticaret #trendyol #kendisiteni #pazaryeri #seo #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="E-ticaret · Strateji", baslik="Tüm yumurtalar *tek sepette* mi?", alt="Pazaryeri bağımlılığının 3 riski.", sure=3.5),
             dict(tip="madde", no=1, baslik="Kurallar *sizin değil*", metin="Komisyon, kargo ve görünürlük kuralları **tek taraflı** değişebilir.", sure=4),
             dict(tip="madde", no=2, baslik="Müşteri de *sizin değil*", metin="Pazaryerinde müşteri bilgisi ve tekrar satış imkânı **sınırlıdır**.", sure=4),
             dict(tip="madde", no=3, baslik="Tek hesap, *tek risk*", metin="Bir hesap sorunu tüm cironuzu durdurabilir.", sure=3.8),
             dict(tip="alinti", ust="Çözüm", baslik="Pazaryeri + *kendi site*", metin="Pazaryerinde satmaya devam edin; kendi sitenize **SEO ile** düzenli trafik kurun.", sure=4.5),
             dict(tip="cta", ust="E-ticaret SEO", baslik="Kendi kanalınızı *birlikte* kuralım", aciklama="Sitenize Google'dan düzenli trafik getirecek planı hazırlıyoruz.", sure=4),
         ]),
    dict(id="2026-10-30-ucretsiz-araclar", tur="carousel", stil="altin", yayin_zamani="2026-10-30T19:00:00+03:00",
         aciklama=acik("Sitemizde herkesin ücretsiz kullanabileceği araçlar ve kaynaklar var. 🧰",
                       "Yapay zekâ görünürlük testi, SEO sözlüğü ve e-ticaret bülteni. Kayıt olmadan deneyebilirsiniz.",
                       "📌 Kaydedin, ihtiyacınız olduğunda açın.",
                       etiket="#ücretsizaraç #seo #geo #yapayzeka #eticaret #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Ücretsiz Kaynaklar", baslik="Sitemizde *ücretsiz* neler var?", alt="Kayıt gerektirmeyen araçlar ve rehberler."),
             dict(tip="madde", no=1, baslik="Yapay Zekâ *Görünürlük Testi*", metin="Markanızın yapay zekâ cevaplarında nasıl anlatıldığını **hızlıca** görün.", liste=["ChatGPT'de var mısınız?"]),
             dict(tip="madde", no=2, baslik="SEO, GEO, Trendyol *Sözlüğü*", metin="Terimler sade Türkçe ile: ne demek, **neden önemli**.", liste=["seovedijital.com/sozluk"]),
             dict(tip="madde", no=3, baslik="SeoveBülten", metin="E-ticaret ve SEO için **kontrol listeleri** ve kısa notlar e-postanıza gelsin.", liste=["Menü → SeoveBülten"]),
             dict(tip="madde", no=4, baslik="Düzenli yeni *rehberler*", metin="Blogumuzda Trendyol, SEO ve GEO üzerine **uygulanabilir** rehberler."),
             dict(tip="cta", ust="Ücretsiz Ön Analiz", baslik="Daha fazlası için *bize yazın*", aciklama="Sitenizin ve mağazanızın durumunu ücretsiz çıkarıyoruz."),
         ]),
    # ---------------- 31 Ekim ----------------
    dict(id="2026-10-31-basabas-noktasi", tur="carousel", stil="kor", yayin_zamani="2026-10-31T12:30:00+03:00",
         aciklama=acik("Sipariş başı kâr yetmez. Ay sonunda cebinizde ne kalıyor? 🧮",
                       "Başabaş noktası, sabit giderlerinizi karşılamak için ayda kaç sipariş gerektiğini söyler.",
                       "Kasım kampanyasına girmeden önce bu rakamı bilin.",
                       "📌 Kaydedin, kendi rakamlarınızla hesaplayın.",
                       etiket="#trendyol #başabaş #kârhesabı #eticaret #kasımindirimleri #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Trendyol · Kâr", baslik="Ayda *kaç sipariş* lazım?", alt="Başabaş noktasını 3 adımda bulun."),
             dict(tip="madde", no=1, baslik="Sabit *giderler*", metin="Siparişten bağımsız ödedikleriniz: kira, maaş, yazılım, muhasebe.", liste=["Kira", "Maaş", "Yazılım"]),
             dict(tip="madde", no=2, baslik="Sipariş başı *katkı*", metin="Satış fiyatı − (ürün maliyeti + komisyon + kargo + paketleme + reklam payı)."),
             dict(tip="alinti", ust="Formül", baslik="Sabit gider ÷ *katkı payı*", metin="Çıkan sayı, ayda **zarar etmemek** için gereken sipariş adedidir. Bunun üstü kârdır."),
             dict(tip="madde", no=3, baslik="İndirimde *yeniden* hesaplayın", metin="İndirim katkı payını düşürür, başabaş sipariş sayısı **yükselir**. Kampanya öncesi kontrol edin."),
             dict(tip="cta", ust="Trendyol Satış Artırma", baslik="Mağazanızın rakamlarını *birlikte* kuralım", aciklama="Kâr, başabaş ve kampanya senaryolarınızı tabloya döküyoruz."),
         ]),
    dict(id="2026-10-31-black-friday-4-hafta", tur="reels", stil="kor", muzik="funk", yayin_zamani="2026-10-31T19:00:00+03:00",
         aciklama=acik("Kasım'ın en yoğun günlerine yaklaşık 4 hafta var. ⏳",
                       "Hazırlığı son haftaya bırakan satıcı stok, fiyat ve reklamda acele karar verir.",
                       "Bugünden başlayabileceğiniz 4 adım.",
                       "📌 Kaydedin, her hafta bir adımı tamamlayın.",
                       etiket="#blackfriday #kasımindirimleri #trendyol #eticaret #kampanya #seovedijital"),
         slaytlar=[
             dict(tip="kapak", ust="Kasım Hazırlığı", baslik="Büyük indirime *4 hafta* var", alt="Her hafta bir adım.", sure=3.5),
             dict(tip="madde", no=1, baslik="1. hafta: *ürün seçimi*", metin="Kampanyaya hangi ürünlerle gireceğinize **kâr hesabıyla** karar verin.", sure=4),
             dict(tip="madde", no=2, baslik="2. hafta: *stok*", metin="Çok satacak ürünlerin stoğunu ve tedarik sürelerini netleştirin.", sure=4),
             dict(tip="madde", no=3, baslik="3. hafta: *sayfa ve görsel*", metin="Başlık, görsel ve açıklamaları güncelleyin. Kampanya trafiği gelmeden hazır olsun.", sure=4),
             dict(tip="madde", no=4, baslik="4. hafta: *reklam ve operasyon*", metin="Reklam bütçesini planlayın, kargo ve müşteri sorularına hazırlanın.", sure=4),
             dict(tip="cta", ust="Trendyol Kampanya Yönetimi", baslik="Kasım'a *planla* girin", aciklama="Kampanya takviminizi, stok ve reklam planınızı birlikte hazırlıyoruz.", sure=4),
         ]),
]

if __name__ == "__main__":
    for d in ICERIK:
        if not d.get("stil"): d.pop("stil", None)
        kaydet(d)
