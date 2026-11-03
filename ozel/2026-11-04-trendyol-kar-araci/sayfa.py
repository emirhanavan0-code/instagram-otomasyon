"""Çekim için sayfa.html üretir: site header'ı + Trendyol Kâr ve Komisyon Hesaplama aracının sayfa kodu (canlı JS).
Rakamlar aracın kendi "Örnek değerlerle dene" değerleridir; videoda "Örnek hesaplama" etiketiyle gösterilir.
Kullanım: python3 sayfa.py HEADER_HTML ARAC_KOD_TXT"""
import sys
HDR, ARAC = sys.argv[1], sys.argv[2]
kill = ('<style>*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}'
        '.sx-cur,.sx-prog,.sx-wa,.sx-dock,#sx-yzp,#sx-cookie,.sx-cookie{display:none!important}html,body{overflow:hidden!important}'
        '.sx-r,.reveal,[data-r],#sx-tk .tk-r{opacity:1!important;transform:none!important}</style>')
html = ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=390"></head>'
        '<body style="margin:0;background:#050507">' + open(HDR).read() + open(ARAC).read() + kill + '<script>window.scrollTo=function(){};</script></body></html>')
open('sayfa.html', 'w').write(html)
print('sayfa.html', len(html))
