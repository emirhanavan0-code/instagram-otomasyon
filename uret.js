// İçerik dosyalarından (icerik/*.json) marka şablonuyla görsel ve Reels videosu üretir.
// Kullanım: node uret.js icerik/2026-10-20-ornek.json [...]   (dosya verilmezse durumu "taslak" olan hepsi)
// Üretimden sonra durum "planlandi" olur; main dalına birleşince yayinla.py zamanı gelince paylaşır.
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright");

const ROOT = __dirname;
const FPS = 30;
const VARSAYILAN_SAHNE_SURESI = 3.5;

function icerikDosyalari(argv) {
  if (argv.length) return argv;
  return fs.readdirSync(path.join(ROOT, "icerik"))
    .filter(f => f.endsWith(".json"))
    .map(f => path.join("icerik", f))
    .filter(f => JSON.parse(fs.readFileSync(path.join(ROOT, f))).durum === "taslak");
}

async function sayfaAc(browser, format) {
  const page = await browser.newPage({ viewport: { width: 1080, height: format === "reels" ? 1920 : 1350 } });
  await page.goto("file://" + path.join(ROOT, "marka", "sablon.html"));
  return page;
}

async function gorselUret(browser, icerik, cikti) {
  const page = await sayfaAc(browser, "post");
  const dosyalar = [];
  for (const [i, slayt] of icerik.slaytlar.entries()) {
    await page.evaluate(([s, o]) => window.ciz(s, o), [slayt, { format: "post", sira: i + 1, toplam: icerik.slaytlar.length }]);
    const dosya = path.join(cikti, `${String(i + 1).padStart(2, "0")}.jpg`);
    await page.locator("#sahne").screenshot({ path: dosya, type: "jpeg", quality: 92 });
    dosyalar.push(path.relative(ROOT, dosya));
  }
  await page.close();
  return dosyalar;
}

function muzikGirdisi(sure) {
  const klasor = path.join(ROOT, "muzik");
  const parcalar = fs.existsSync(klasor) ? fs.readdirSync(klasor).filter(f => /\.(mp3|m4a|wav)$/i.test(f)) : [];
  if (parcalar.length) {
    const parca = parcalar[Math.floor(Math.random() * parcalar.length)];
    return ["-stream_loop", "-1", "-i", path.join(klasor, parca)];
  }
  // Telifsiz yedek: yumuşak akor + hafif ritim, ffmpeg ile sentezlenir
  const ifade = [
    "0.10*sin(2*PI*220*t)", "0.08*sin(2*PI*277.18*t)", "0.08*sin(2*PI*329.63*t)", "0.05*sin(2*PI*440*t)",
  ].join("+");
  const ritim = "0.12*sin(2*PI*55*t)*exp(-12*mod(t,0.5))";
  return ["-f", "lavfi", "-i", `aevalsrc='(${ifade})*(0.75+0.25*sin(2*PI*0.25*t))+${ritim}':s=44100:d=${sure}`];
}

async function reelsUret(browser, icerik, cikti) {
  const page = await sayfaAc(browser, "reels");
  const sahneler = icerik.slaytlar.map(s => ({ ...s, sure: s.sure || VARSAYILAN_SAHNE_SURESI }));
  const toplamSure = sahneler.reduce((t, s) => t + s.sure, 0);
  const video = path.join(cikti, "reels.mp4");

  const ffmpeg = spawn("ffmpeg", [
    "-y", "-loglevel", "error",
    "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
    ...muzikGirdisi(toplamSure),
    "-filter_complex", `[1:a]afade=t=in:d=1,afade=t=out:st=${toplamSure - 1.5}:d=1.5,volume=0.8[a]`,
    "-map", "0:v", "-map", "[a]", "-t", String(toplamSure),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "20",
    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", video,
  ], { stdio: ["pipe", "inherit", "inherit"] });
  const bitti = new Promise((ok, hata) => ffmpeg.on("close", k => (k === 0 ? ok() : hata(new Error("ffmpeg " + k)))));

  for (const [i, sahne] of sahneler.entries()) {
    await page.evaluate(([s, o]) => window.ciz(s, o), [sahne, { format: "reels", sira: i + 1, toplam: sahneler.length, sure: sahne.sure }]);
    await page.evaluate(() => document.getAnimations().forEach(a => a.pause()));
    const kare = Math.round(sahne.sure * FPS);
    for (let f = 0; f < kare; f++) {
      const t = f / FPS;
      // Sahne sonunda 0.3 sn kararma geçişi
      const opaklik = Math.min(1, (sahne.sure - t) / 0.3, i === 0 ? 1 : t / 0.2 + 0.2);
      await page.evaluate(([ms, o]) => {
        document.getAnimations().forEach(a => (a.currentTime = ms));
        document.querySelector("main").style.opacity = o;
      }, [t * 1000, Math.max(0, opaklik)]);
      const buf = await page.locator("#sahne").screenshot({ type: "jpeg", quality: 90 });
      if (!ffmpeg.stdin.write(buf)) await new Promise(r => ffmpeg.stdin.once("drain", r));
    }
  }
  ffmpeg.stdin.end();
  await bitti;

  // Kapak görseli: ilk sahnenin animasyon bitmiş hali
  await page.evaluate(([s, o]) => window.ciz(s, o), [sahneler[0], { format: "reels", sira: 1, toplam: 1 }]);
  await page.evaluate(() => document.getAnimations().forEach(a => a.finish()));
  const kapak = path.join(cikti, "kapak.jpg");
  await page.locator("#sahne").screenshot({ path: kapak, type: "jpeg", quality: 92 });
  await page.close();
  return [path.relative(ROOT, video), path.relative(ROOT, kapak)];
}

(async () => {
  const dosyalar = icerikDosyalari(process.argv.slice(2));
  if (!dosyalar.length) return console.log("Üretilecek taslak içerik yok.");
  const browser = await chromium.launch();
  for (const dosya of dosyalar) {
    const icerik = JSON.parse(fs.readFileSync(path.join(ROOT, dosya)));
    // Elle kurgulanmış reels (ozel/ klasöründe kaynağı var): medyası şablonla ezilmesin
    if (icerik.ozel) { console.log(`↷ ${icerik.id}: özel kurgu (${icerik.ozel}), atlandı`); continue; }
    const cikti = path.join(ROOT, "medya", icerik.id);
    fs.mkdirSync(cikti, { recursive: true });
    const t0 = Date.now();
    icerik.medya = icerik.tur === "reels" ? await reelsUret(browser, icerik, cikti) : await gorselUret(browser, icerik, cikti);
    icerik.durum = "planlandi";
    fs.writeFileSync(path.join(ROOT, dosya), JSON.stringify(icerik, null, 2) + "\n");
    console.log(`✓ ${icerik.id} (${icerik.tur}) → ${icerik.medya.join(", ")} [${((Date.now() - t0) / 1000).toFixed(1)} sn]`);
  }
  await browser.close();
})();
