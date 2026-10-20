# Yapay Zekâ Görünürlük Testi reels (özel kurgu, 21 Ekim 12:00)

Eğitim tarzı: soru sahnesi → başlık → telefonda gerçek araç sayfası (form doldurma, test, sonuç) → kapanış.
Telefon ekranı ekran görüntüsü değil, aracın kendisi: eklentinin kısa kod çıktısı + arac.js iframe'de çalışır,
yapay zekâ cevapları açıkça "Örnek sonuç" diye gösterilen sahte verilerle gelir (alan adları yer tutucu).

- `sayfa.php` + `sayfa.py EKLENTI_KLASORU HEADER_HTML`: `sayfa.html` (eklenti: seovedijital-blog deposu, yz-gorunurluk-testi dalı, `eklenti/sd-ai-gorunurluk`; header: `anasayfa/wordpress/1-header.html`).
- Bu klasörde `python3 -m http.server 8765`, sonra `python3 rend.py test 2 9 16` (kare kontrolü) ya da `python3 rend.py full` → `video.mp4`.
- `muzik.py` → `muzik.wav` (D minör, 100 BPM; geçiş, yazma, sonuç efektleri kurguya göre zamanlı).
- Birleştirme: `ffmpeg -i video.mp4 -i muzik.wav -filter_complex "[1:a]loudnorm=I=-14:TP=-1.5,aresample=48000[a]" -map 0:v -map "[a]" -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -preset slow -crf 21 -maxrate 4000k -bufsize 8000k -c:a aac -b:a 160k -ar 48000 -shortest -movflags +faststart reels.mp4`

İçerik dosyasındaki `"ozel"` alanı `uret.js`'in bu videoyu şablonla yeniden üretmesini engeller.
