"""anim.html zaman çizelgesini 30 fps kare kare çeker. Sayfa durumu sırayla ilerlediği için kareler baştan sona çekilir.
Kullanım: python3 -m http.server 8765 (bu klasörde) açıkken  python3 rend.py full  |  python3 rend.py test 2 9 16"""
import os, subprocess, sys
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
mode = sys.argv[1]; FPS = 30; DUR = 24.5
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, locale='tr-TR')
    pg.goto('http://localhost:8765/anim.html'); pg.evaluate('document.fonts.ready'); pg.evaluate('window.hazir'); pg.wait_for_timeout(1500)
    st = pg.locator('#st')
    if mode == 'test':
        hedef = sorted(map(float, sys.argv[2:]))
        n = int(max(hedef) * FPS) + 1
        for f in range(n):
            t = f / FPS; pg.evaluate(f'render({t})')
            for h in hedef:
                if abs(t - h) < .5 / FPS:
                    pg.wait_for_timeout(80); st.screenshot(path=f'{D}/t{h}.jpg', type='jpeg', quality=80)
    else:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-preset', 'medium', '-crf', '19',
                               '-r', str(FPS), D + '/video.mp4'], stdin=subprocess.PIPE)
        for f in range(int(DUR * FPS)):
            pg.evaluate(f'render({f / FPS})'); ff.stdin.write(st.screenshot(type='jpeg', quality=92))
        ff.stdin.close(); ff.wait()
    b.close()
