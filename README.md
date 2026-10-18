# @seovedijital Instagram Otomasyonu

Hesabı ajans düzeninde yöneten sistem: içerik hazırlanır, sen onaylarsın, zamanı gelince
otomatik paylaşılır.

## Haftalık döngü
| Ne zaman | Ne olur |
|---|---|
| Cuma | Performans raporu çıkar, Claude gelecek haftanın 5 içeriğini hazırlar ve **Pull Request** açar |
| Hafta sonu (sen) | PR'daki görselleri ve metinleri kontrol edersin. Beğendiysen **Merge** ile onaylarsın |
| Pzt 12:30 Reels · Sal 19:00 Kaydırmalı · Per 12:30 Reels · Cum 12:30 Reels · Paz 11:00 Görsel | Onaylı içerikler Instagram'da otomatik yayınlanır |

## Onay nasıl verilir
1. GitHub'da **Pull requests** sekmesini aç ve "Hafta ..." başlıklı PR'a gir.
2. Açıklamadaki görsellere ve metinlere bak.
3. Beğendiysen **Merge pull request → Confirm merge**.
4. Bir içeriği istemiyorsan **Files changed** sekmesinden o `icerik/*.json` dosyasını silebilir
   veya metnini düzenleyebilirsin. Düzenleme yaparsan görseller otomatik yeniden üretilir.
5. Hiçbirini istemiyorsan PR'ı **Close** et, hiçbir şey paylaşılmaz.

## Klasörler
- `icerik/`: içerik planı (her gönderi bir dosya; durum: taslak → planlandi → yayinlandi; ertelenenler beklemede)
- `medya/`: üretilen görseller ve Reels videoları
- `marka/`: logo, fontlar ve tasarım şablonu
- `raporlar/`: haftalık performans raporları
- `muzik/`: Reels arka plan müziği. Buraya telifsiz `.mp3` koyarsan rastgele seçilir,
  boşsa sade bir arka plan sesi üretilir.

## Kurulum notu
GitHub'da **Settings → Secrets and variables → Actions → New repository secret** yolundan
`COMPOSIO_API_KEY` adında bir secret eklenmeli.
