"""23–31 Ekim 2026 kısa notları: güncel, kaynağı doğrulanmış sektör haberleri (tek görsel, tip "not").
Çalıştır: python3 araclar/notlar_44.py"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SON = "🔗 Detaylar: seovedijital.com\n📞 0501 048 3732"

NOTLAR = [
    ("2026-10-23", "ai-mode-linkler", "google", "kor", "Google · AI Mode", "15 Ekim 2026",
     "Yapay zekâ cevaplarında *daha çok link*",
     "Google, AI Overviews ve AI Mode cevaplarında **satır içi linkleri artırdığını** ve daha üstte gösterdiğini duyurdu.",
     "Cevapta kaynak gösterilen sitelerin tıklanma fırsatı artabilir. Net ve güvenilir içerik daha da önemli.",
     "Google (The Keyword blogu)", "Google'ın yapay zekâ cevaplarında artık daha fazla link var. 🔗",
     "#googleaimode #aioverviews #geo #seo #yapayzeka #seovedijital"),
    ("2026-10-24", "trendyol-ortak", "eticaret", "zumrut", "E-ticaret · Trendyol", "15 Ekim 2026",
     "Trendyol satıcılara *yapay zekâ* anlattı",
     "Trendyol Group CEO'su Erdem İnan, satıcılar için dijital asistan **\"Ortak\"** ile 10 dilde yurt dışı satışa yardım eden **Trendyol LLM**'i anlattı.",
     "Operasyon, stok ve yurt dışı satışta platformun yapay zekâ araçları satıcının gündemine giriyor.",
     "Anadolu Ajansı", "Trendyol tarafında yapay zekâ gündemi hızlanıyor. 🤖",
     "#trendyol #eticaret #yapayzeka #trendyolsatıcı #pazaryeri #seovedijital"),
    ("2026-10-26", "chatgpt-utm-hatasi", "geo", "gece", "GEO · Ölçüm", "20 Ekim 2026",
     "ChatGPT trafiği *direct* göründü: hata",
     "Ekim başında ChatGPT linklerinden **utm_source=chatgpt.com** etiketi kayboldu. OpenAI hatayı doğruladı; düzeltme 15 Ekim'de yayılmaya başladı.",
     "GA4'te 8–15 Ekim arasında ChatGPT trafiği düşüp direct arttıysa, büyük ihtimalle **ölçüm hatasıdır**.",
     "Search Engine Land", "Analytics'te ChatGPT trafiğiniz birden düştü mü? Panik yapmayın. 📊",
     "#chatgpt #ga4 #geo #analytics #seo #seovedijital"),
    ("2026-10-27", "search-console-multimodal", "google", "altin", "Search Console", "24 Eylül 2026",
     "Search Console'a *Multimodal* filtresi",
     "Performans raporunda web aramaları artık **metin** ve **multimodal** (Lens, görselle arama) olarak ayrı görülebiliyor.",
     "Ürün görseli olan siteler, görselle yapılan aramalardan ne kadar trafik aldığını ayrıca takip edebilir.",
     "Google Search Central blogu", "Görselle arama trafiğinizi artık ayrı görebilirsiniz. 📷",
     "#searchconsole #googlelens #seo #eticaret #görselarama #seovedijital"),
    ("2026-10-28", "instagram-canli-one-cikar", "instagram", "kor", "Instagram", "30 Eylül 2026",
     "Canlı yayınlara *Öne Çıkar* geldi",
     "Instagram, canlı yayınları da uygulama içinden **öne çıkarma** imkânı ekledi. Hedef kitle ve saat yayın ekranından seçiliyor.",
     "Canlı ürün tanıtımı yapan işletmeler, Reklam Yöneticisi'ne girmeden yayınlarını daha çok kişiye gösterebilir.",
     "Social Media Today", "Canlı yayınlarınızı artık doğrudan öne çıkarabilirsiniz. 🎥",
     "#instagram #instagramcanlı #sosyalmedya #kobi #dijitalpazarlama #seovedijital"),
    ("2026-10-29", "bing-topics-portfolio", "geo", "zumrut", "GEO · Bing", "13 Ekim 2026",
     "Bing, yapay zekâ atıflarını *konulara* ayırdı",
     "Bing Webmaster Tools'a **Topics Portfolio** (beta) eklendi: sitenizin yapay zekâ cevaplarında kaynak gösterildiği konuları ve **fırsat sorgularını** listeliyor.",
     "Yapay zekâ aramalarında hangi konularda eksik kaldığınızı görüp içerik planlayabilirsiniz. Sekme yeterli verisi olan sitelerde çıkıyor.",
     "Bing Webmaster blogu", "Yapay zekâ cevaplarında hangi konularda eksiksiniz? Bing artık gösteriyor. 🧭",
     "#bing #geo #yapayzeka #copilot #seo #seovedijital"),
    ("2026-10-30", "gemini-kobi-araclari", "geo", "gece", "Google · Gemini", "20 Ekim 2026",
     "Gemini'ye *KOBİ'lere özel* araçlar",
     "Google, Gemini uygulamasına küçük işletmeler için **iş sayfası**, pazarlama ve finans becerileri ile **İşletme Profili, Google Ads** gibi bağlı uygulamalar ekleneceğini duyurdu.",
     "Kampanya içeriği ve işletme özetleri için Gemini tek yerden kullanılabilecek. Kademeli olarak açılıyor.",
     "Google (The Keyword blogu)", "Gemini küçük işletmeler için yeni araçlar alıyor. 🧩",
     "#gemini #kobi #yapayzeka #googleads #dijitalpazarlama #seovedijital"),
    ("2026-10-31", "chatgpt-google-trafik", "geo", "altin", "GEO · Araştırma", "21 Ekim 2026",
     "ChatGPT trafiği Google'ın *%1'i bile* değil",
     "100 sitenin 12 aylık GA4 verisini inceleyen bir analizde ChatGPT, Google organiğin **%0,62'si** kadar ziyaret getirdi; ama ziyaretçileri **daha yüksek oranda** dönüşüm yaptı.",
     "Google SEO hâlâ ana trafik kaynağı. GEO onun yerini almaz, yanına eklenir.",
     "Marie Haynes analizi, Search Engine Land", "Yapay zekâ trafiği büyüyor ama Google hâlâ çok önde. 📈",
     "#chatgpt #seo #geo #googleseo #yapayzeka #seovedijital"),
]

if __name__ == "__main__":
    for gun, slug, konu, stil, ust, tarih, baslik, metin, anlami, kaynak, kanca, etiket in NOTLAR:
        d = dict(id=f"{gun}-not-{slug}", tur="gorsel", durum="taslak", stil=stil, yayin_zamani=f"{gun}T16:00:00+03:00",
                 aciklama=f"{kanca}\n\n{metin.replace('**', '')}\n\nSizin için anlamı: {anlami.replace('**', '')}\n\nKaynak: {kaynak}, {tarih}.\n\n📌 Kaydedin, takip edin.\n{SON}\n\n{etiket}",
                 slaytlar=[dict(tip="not", ust=ust, tarih=tarih, baslik=baslik, metin=metin, anlami=anlami, kaynak=f"{kaynak} · {tarih}")])
        (ROOT / "icerik" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        print("✓", d["id"])
