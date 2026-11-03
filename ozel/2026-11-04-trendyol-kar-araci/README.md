# Trendyol Kâr ve Komisyon Hesaplama reels (özel kurgu, 4 Kasım 16:30; ücretli reklamda da kullanılacak)

Kurgu (29 sn, 1080×1920): kanca (1.000 ₺ satış → komisyon, KDV, kargo, paketleme düşülür → "Cebinize kaç lira kaldı?")
→ başlık → telefonda gerçek araç sayfası (rakamlar yazılır, %15 komisyon seçilir) → net kâr 312,50 ₺ → satış dökümü
→ hedef fiyat ve indirim senaryosu kaydırıcıları → kapanış (seovedijital.com, telefon).
Telefon ekranı ekran görüntüsü değil, aracın kendi kodu (canlı JS). Rakamlar aracın "Örnek değerlerle dene" değerleri; videoda "Örnek hesaplama" etiketi var.

- `python3 sayfa.py HEADER_HTML ARAC_KOD_TXT` → `sayfa.html` (header: `seovedijital-anasayfa/1-header.html`, araç: `seovedijital-anasayfa/trendyol-kar-hesaplama-KOD.txt`, proje dosyaları).
- Bu klasörde `python3 -m http.server 8766`, sonra `NODE_PATH=/opt/node-tools/node_modules node rend.js test 3 9 16` (kare kontrolü) ya da `node rend.js full` → `video.mp4`.
- `python3 muzik.py` → `muzik.wav` (F minör, 112 BPM; kanca darbeleri, drop, geçiş, yazma ve sonuç efektleri kurguya göre zamanlı).
- Birleştirme: `ffmpeg -i video.mp4 -i muzik.wav -filter_complex "[1:a]loudnorm=I=-14:TP=-1.5,aresample=48000[a]" -map 0:v -map "[a]" -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -preset slow -crf 20 -maxrate 4500k -bufsize 9000k -c:a aac -b:a 160k -ar 48000 -shortest -movflags +faststart reels.mp4`
- Kapak: `ffmpeg -ss 4.9 -i video.mp4 -frames:v 1 -q:v 2 kapak.jpg`
