"""Çekim için sayfa.html üretir: site header'ı + eklentinin kısa kod çıktısı + arac.js.
Yapay zekâ çağrıları sahte (örnek) cevaplarla değiştirilir; cevaplar anim.html'in verdiği sinyalle tek tek gelir.
Kullanım: python3 sayfa.py EKLENTI_KLASORU HEADER_HTML"""
import json, subprocess, sys
E, HDR = sys.argv[1].rstrip('/'), sys.argv[2]
govde = subprocess.run(['php', 'sayfa.php', E], capture_output=True, text=True, check=True).stdout
js = open(E + '/assets/arac.js').read()
SORULAR = ["Ankara'da en iyi diş klinikleri hangileri?", "Ankara'da implant için hangi diş hekimine gidebilirim?",
           "Ankara'da güvenilir bir diş hekimi önerir misin?"]
# Örnek (uydurma değil, açıkça "örnek" diye gösterilen) cevaplar; alan adları yer tutucudur.
CEVAPLAR = [
    {"sonuclar": [{"ad": "Gemini", "durum": "ok", "bahsedildi": False, "kaynak": False,
                   "kaynaklar": ["saglik-rehberi.com", "rakip-klinik.com", "haber-sitesi.com"],
                   "alinti": "Ankara'da öne çıkan diş klinikleri arasında rehber sitelerinde yüksek puan alan ve hakkında çok yorum bulunan klinikler sayılıyor."}]},
    {"sonuclar": [{"ad": "Gemini", "durum": "ok", "bahsedildi": True, "kaynak": False,
                   "kaynaklar": ["saglik-rehberi.com", "yorum-platformu.com"],
                   "alinti": "İmplant için Çankaya'daki Örnek Diş Kliniği ve rehber sitelerinde öne çıkan birkaç klinik değerlendirilebilir."}]},
    {"sonuclar": [{"ad": "Gemini", "durum": "ok", "bahsedildi": False, "kaynak": False,
                   "kaynaklar": ["rakip-klinik.com", "saglik-rehberi.com", "yorum-platformu.com"],
                   "alinti": "Güvenilir bir diş hekimi seçerken hasta yorumlarına ve rehber sitelerindeki değerlendirmelere bakmanızı öneririm."}], "skor": 23},
]
mock = f"""<script>
window.SD_AIG={{api:'/api/',sayfa:'https://seovedijital.com/yapay-zeka-gorunurluk-testi/',iletisim:'',nonce:''}};
(function(){{
  const SORULAR={json.dumps(SORULAR, ensure_ascii=False)}, CEVAP={json.dumps(CEVAPLAR, ensure_ascii=False)};
  window.__bekleyen=[];
  const yanit=j=>({{ok:true,json:()=>Promise.resolve(j)}});
  window.fetch=function(url,o){{
    if(url.endsWith('basla'))return Promise.resolve(yanit({{id:'ornek',sorular:SORULAR,saglayicilar:['Gemini']}}));
    if(url.endsWith('sor')){{const i=JSON.parse(o.body).i;return new Promise(r=>{{window.__bekleyen[i]=()=>r(yanit(CEVAP[i]));}});}}
    return Promise.reject(new Error('çevrimdışı'));
  }};
  window.scrollTo=function(){{}};
}})();
</script>"""
kill = '<style>*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}' \
       '.sx-cur,.sx-prog,.sx-wa,.sx-dock,#sx-yzp{display:none!important}html,body{overflow:hidden!important}' \
       '#sx-yz .yz-r{opacity:1!important;transform:none!important}#sx-yz .yz-orb{width:130px!important;height:130px!important;margin:0 auto}</style>'
html = ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=390"></head>'
        '<body style="margin:0;background:#060609">' + open(HDR).read() + govde + kill + mock + '<script>' + js + '</script></body></html>')
open('sayfa.html', 'w').write(html)
print('sayfa.html', len(html))
