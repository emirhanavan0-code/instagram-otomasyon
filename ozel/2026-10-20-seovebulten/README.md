# SeoveBülten reels (özel kurgu)

Şablon (`uret.js`) yerine elle kurgulanmış telefon + zoom animasyonu.
- `cap.py`: site ve PDF görüntülerini alır (seovedijital-blog deposundaki sayfa kodundan).
- `rend.py full`: `anim.html` zaman çizelgesini 30 fps kare kare çeker → `video.mp4`.
- `muzik.py`: telifsiz müzik + geçiş efektleri sentezler → `muzik.wav`.
- Birleştirme: `ffmpeg -i video.mp4 -i muzik.wav -filter_complex "[1:a]loudnorm=I=-14:TP=-1.5[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest reels.mp4`
