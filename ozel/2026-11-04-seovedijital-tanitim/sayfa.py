"""Çekim için sayfa.html üretir: site header'ı + ana sayfa içeriği + footer (seovedijital.com mobil görünümü, canlı kod).
Kullanım: python3 sayfa.py HEADER_HTML ANASAYFA_HTML FOOTER_HTML"""
import sys
HDR, ANA, FTR = sys.argv[1:4]
kill = ('<style>*,*::before,*::after{transition:none!important;scroll-behavior:auto!important}'
        '.sx-cur,.sx-prog,.sx-wa,.sx-dock,#sx-yzp,#sx-cookie,.sx-cookie,#sx-pop,.sx-pop{display:none!important}html,body{overflow:hidden!important}#sx-hz-track{scroll-snap-type:none!important}'
        '.sx-r,.reveal,[data-r],.tk-r,.sx-man__t .w,.sx-h1 .ln > span{opacity:1!important;transform:none!important;filter:none!important}</style>')
html = ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=390"></head>'
        '<body style="margin:0;background:#050507">' + open(HDR).read() + open(ANA).read() + open(FTR).read() + kill +
        '<script>window.scrollTo=function(){};</script></body></html>')
open('sayfa.html', 'w').write(html)
print('sayfa.html', len(html))
