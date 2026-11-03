// anim.html zaman çizelgesini 30 fps kare kare çeker. Sayfa durumu sırayla ilerlediği için kareler baştan sona çekilir.
// Kullanım: bu klasörde `python3 -m http.server 8767` açıkken  node rend.js full  |  node rend.js test 2 9 16
const {chromium}=require('playwright'); const {spawn}=require('child_process'); const path=require('path');
const D=__dirname, FPS=30, DUR=30.0, mode=process.argv[2];
(async()=>{
  const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:1080,height:1920},locale:'tr-TR'});
  await pg.goto('http://localhost:8767/2026-11-04-seovedijital-tanitim/anim.html'); await pg.evaluate(()=>document.fonts.ready); await pg.evaluate(()=>window.hazir); await pg.waitForTimeout(1500);
  const st=pg.locator('#st');
  if(mode==='test'){
    const hedef=process.argv.slice(3).map(Number).sort((a,b)=>a-b); const n=Math.floor(Math.max(...hedef)*FPS)+1;
    for(let f=0;f<n;f++){const t=f/FPS; await pg.evaluate(t=>render(t),t);
      for(const h of hedef) if(Math.abs(t-h)<.5/FPS){await pg.waitForTimeout(80); await st.screenshot({path:path.join(D,`t${h}.jpg`),type:'jpeg',quality:80});}}
  } else {
    const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-preset','medium','-crf','18','-r',String(FPS),path.join(D,'video.mp4')],{stdio:['pipe','inherit','inherit']});
    for(let f=0;f<Math.round(DUR*FPS);f++){await pg.evaluate(t=>render(t),f/FPS); const buf=await st.screenshot({type:'jpeg',quality:92});
      if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); if(f%90==0)console.log('kare',f);}
    ff.stdin.end(); await new Promise(r=>ff.on('close',r));
  }
  await b.close();
})();
