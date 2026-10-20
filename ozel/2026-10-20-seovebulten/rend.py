import sys,json,subprocess,os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__))
R=json.load(open(D+'/rects.json'))
mode=sys.argv[1]; FPS=30; DUR=17.0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.add_init_script('window.RECTS='+json.dumps(R))
    pg.goto('file://'+D+'/anim.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(2500)
    st=pg.locator('#st')
    if mode=='test':
        for t in map(float,sys.argv[2:]):
            pg.evaluate(f'render({t})'); pg.wait_for_timeout(50); st.screenshot(path=f'{D}/t{t}.jpg',type='jpeg',quality=80)
    else:
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-preset','medium','-crf','18','-r',str(FPS),D+'/video.mp4'],stdin=subprocess.PIPE)
        n=int(DUR*FPS)
        for f in range(n):
            pg.evaluate(f'render({f/FPS})'); ff.stdin.write(st.screenshot(type='jpeg',quality=92))
        ff.stdin.close(); ff.wait()
    b.close()
