from playwright.sync_api import sync_playwright
W='/home/claude/pa/anasayfa/wordpress/'
hdr=open(W+'1-header.html').read(); sb=open(W+'seovebulten.html').read()
page='<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head><body style="margin:0;background:#060609">'+hdr+sb+'</body></html>'
open('site.html','w').write(page)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=4,locale='tr-TR')
    pg.goto('file://'+__import__('os').getcwd()+'/site.html'); pg.wait_for_timeout(2500)
    pg.evaluate("localStorage.clear()")
    pg.add_style_tag(content='.sx-cur,.sx-prog,.sx-wa,.sx-dock{display:none!important}')
    # reveal any scroll-in elements
    pg.evaluate("document.querySelectorAll('*').forEach(e=>{e.classList.add('sx-in')})")
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(2500); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1500)
    pg.screenshot(path='site-full.png',full_page=True)
    info=pg.evaluate("""(()=>{const r=s=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return [b.top+scrollY,b.height]};return {h:document.documentElement.scrollHeight,h1:r('#sb-h1'),form:r('.sb-form'),icerik:r('#sb-icerik'),kit:r('#sb-kit'),mail:r('#sb-mail-1'),son:r('#sb-son')}})()""")
    print(info)
    import json
    R=lambda q: pg.evaluate("(q)=>{const b=document.querySelector(q).getBoundingClientRect();return [b.left,b.top+scrollY,b.width,b.height]}", q)
    rects={'input':R('.sb-form input[type=email]'),'btn':R('.sb-form button'),'form':R('.sb-form')}
    # filled form state
    pg.evaluate("document.querySelector('.sb-form input[type=email]').placeholder=''")
    pg.locator('.sb-form').first.screenshot(path='form-bos.png')
    pg.evaluate("document.querySelector('.sb-form input[type=email]').value='siz@markaniz.com'")
    f=pg.locator('.sb-form').first; f.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    f.screenshot(path='form-dolu.png')
    pg.evaluate("document.getElementById('sx-sb').classList.add('kayitli')"); pg.wait_for_timeout(300)
    pg.locator('.sb-ok').first.screenshot(path='form-ok.png')
    rects['ok']=R('.sb-ok'); json.dump(rects,open('rects.json','w')); print(rects)
    # pdf cover
    pg2=b.new_page(viewport={'width':794,'height':1123},device_scale_factor=2)
    pg2.goto('file://'+W+'seovebulten/pdf-trendyol-kampanya.html'); pg2.wait_for_timeout(2000)
    pg2.screenshot(path='pdf-kapak.png',clip={'x':0,'y':0,'width':794,'height':1123})
    b.close()
