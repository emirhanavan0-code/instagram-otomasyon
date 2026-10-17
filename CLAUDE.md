# @seovedijital Instagram otomasyonu

Bu depo @seovedijital Instagram hesabını ajans düzeninde yönetir: Claude her hafta içerik hazırlar,
sahibi PR'ı birleştirerek onaylar, GitHub Actions zamanı gelince Composio üzerinden yayınlar.

## Akış
1. `icerik/<id>.json` dosyası yazılır (`durum: "taslak"`).
2. `node uret.js` görsel/video üretir → `medya/<id>/`, durum `planlandi` olur.
3. İçerikler `hafta-YYYY-WW` dalında PR olarak açılır. **PR birleşmesi = onay.**
4. `.github/workflows/yayinla.yml` 30 dakikada bir `yayinla.py` çalıştırır; `main`'deki
   `planlandi` içerikleri `yayin_zamani` gelince yayınlar ve durumu `yayinlandi` yapar.
5. `rapor.yml` her cuma sabahı `raporlar/analiz_*.json` üretir.

## Haftalık içerik görevi (her cuma, gelecek pazartesi–pazar için)
1. `raporlar/` içindeki en yeni raporu ve önceki haftaların `icerik/` dosyalarını oku.
   Hangi tür/konu daha çok erişim, kaydetme ve paylaşım almış? Konuları tekrar etme.
2. Gelecek hafta için 4 içerik yaz, yaklaşık iki günde bir (saatler Türkiye, `+03:00`):
   - Pazartesi 12:30: `reels`, 4–6 sahne, toplam 15–22 sn
   - Çarşamba 19:00: `carousel`, eğitici (5–7 slayt: kapak, maddeler, cta)
   - Cuma 12:30: `reels`
   - Pazar 11:00: `gorsel` (tek slayt, `alinti` veya `rakam`) ya da vaka odaklı kısa carousel
   Rapor bir formatın açıkça daha iyi gittiğini gösterirse dağılımı ona göre kaydır.
3. `npm install` (gerekirse) sonra `node uret.js` ile medyaları üret ve görselleri kontrol et
   (taşan veya sığmayan yazı olmamalı).
4. `hafta-YYYY-WW` dalına commit et, push et, PR aç. PR açıklamasında her içerik için
   kapak görseli (`https://raw.githubusercontent.com/<repo>/<dal>/medya/<id>/01.jpg` veya
   `kapak.jpg`), yayın zamanı ve açıklama metni olsun.

## Marka ve ses
- Hizmetler: Trendyol / pazaryeri satış artırma, SEO, GEO (yapay zeka aramalarında görünürlük),
  reklam ve kampanya yönetimi. Ankara merkezli, KOBİ ve e-ticaret satıcılarına hitap eder.
- Ton: net, uzman, samimi. "Siz" diliyle. Somut ipucu ver, jargonu açıkla, abartılı vaat yok.
- Her içerik tek bir fikir anlatsın. Kapak başlığı en fazla ~8 kelime, merak uyandırsın.
- Çağrı: "DM'e “ANALİZ” yazın", web: seovedijital.com, tel: 0501 048 3732.
- Açıklama: ilk satır kanca, 3–6 kısa satır, çağrı, 5–8 hashtag (#trendyol #seo #geo #eticaret
  #ankaraseo #seovedijital gibi).

## Doğruluk kuralları (kesin)
- **Uydurma istatistik, yüzde, müşteri adı veya sonuç yazma.** Kullanılabilecek bilinen
  gerçekler: Fropie ile Trendyol'da satışlar 3 kat arttı; Desen Triko Yenimahalle ile SEO ve
  pazaryeri iş birliği. Başka rakam gerekiyorsa kaynağını açıklamada belirt veya rakamsız yaz.
- Trendyol / Google / Instagram kuralları hakkında emin olmadığın iddiada bulunma.

## İçerik dosyası şeması
```json
{
  "id": "2026-10-21-trendyol-baslik",
  "tur": "carousel | gorsel | reels",
  "durum": "taslak",
  "yayin_zamani": "2026-10-21T19:00:00+03:00",
  "aciklama": "Instagram açıklaması",
  "slaytlar": [
    {"tip": "kapak",  "ust": "Etiket", "baslik": "*vurgu* içeren başlık", "alt": "alt metin"},
    {"tip": "madde",  "no": 1, "baslik": "...", "metin": "**kalın** destekli", "liste": ["..."]},
    {"tip": "rakam",  "ust": "...", "rakam": "3x", "etiket": "...", "metin": "..."},
    {"tip": "alinti", "ust": "...", "baslik": "...", "metin": "..."},
    {"tip": "cta",    "baslik": "...", "eylem": "DM'e “ANALİZ” yazın", "aciklama": "..."}
  ]
}
```
Reels sahnelerine `"sure": 3.5` (saniye) eklenebilir. `*metin*` turuncu vurgu, `**metin**` kalın.
Uzun başlıklar taşar: kapak başlığı ≤ 45 karakter, madde başlığı ≤ 40 karakter civarı tut.

## Komutlar
- `node uret.js [icerik/x.json ...]`: medya üret (yerelde `NODE_PATH=/opt/node-tools/node_modules` gerekebilir)
- `python ig.py analiz | araclar | calistir SLUG '{json}'`: Composio üzerinden analiz/araçlar
- `python yayinla.py --kuru`: zamanı gelenleri göster; `--test ID`: yayınlamadan Instagram'a yükleme testi
- `COMPOSIO_API_KEY` ortam değişkeni veya `.env` dosyası gerekir (GitHub'da Actions secret).
