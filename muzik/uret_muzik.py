"""Telifsiz reels müzikleri: her biri farklı tempo, ton ve enstrümanla 7 parça (32 sn, döngüye uygun).
Kullanım: python3 muzik/uret_muzik.py  ->  muzik/<ad>.m4a
İçerik dosyasında "muzik": "<ad>" verilirse o parça, verilmezse id'ye göre biri seçilir (uret.js)."""
import numpy as np, wave, subprocess, pathlib, os

SR = 44100
DIR = pathlib.Path(__file__).parent
hz = lambda m: 440 * 2 ** ((m - 69) / 12)


def env(n, a, r):
    e = np.ones(n); A = min(n, int(a * SR)); Rn = min(n, int(r * SR))
    if A: e[:A] = np.linspace(0, 1, A)
    if Rn: e[-Rn:] *= np.linspace(1, 0, Rn)
    return e


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); n = int(np.log(1e-4) / np.log(a)) + 1
    return np.convolve(x, (1 - a) * a ** np.arange(n))[:len(x)]


class Mix:
    def __init__(s, dur):
        s.N = int(SR * dur); s.L = np.zeros(s.N); s.R = np.zeros(s.N)

    def add(s, sig, start, gain=1.0, pan=0.0):
        i = int(start * SR)
        if i >= s.N or i < 0: return
        j = min(s.N, i + len(sig)); x = sig[:j - i] * gain
        s.L[i:j] += x * (1 - max(0, pan)); s.R[i:j] += x * (1 + min(0, pan))


# ---------- sesler ----------
def kick(punch=1.0, d=.45):
    n = int(d * SR); t = np.arange(n) / SR
    f = 45 + 110 * punch * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)


def k808(m, d=.9):
    n = int(d * SR); t = np.arange(n) / SR
    f = hz(m) * (1 + 1.5 * np.exp(-t * 40))
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 2.4)


def snare(rng, d=.22, tone=190):
    n = int(d * SR); t = np.arange(n) / SR
    return (rng.standard_normal(n) * .7 + np.sin(2 * np.pi * tone * t) * .5) * np.exp(-t * 18)


def clap(rng, d=.25):
    n = int(d * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    e = np.exp(-t * 22) + .6 * np.exp(-np.maximum(0, t - .012) * 30) * (t > .012) + .4 * np.exp(-np.maximum(0, t - .024) * 30) * (t > .024)
    return (x - lp(x, 900)) * e * .8


def hat(rng, d=.05, open_=False):
    n = int((.28 if open_ else d) * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    return (x - lp(x, 7000)) * np.exp(-t * (9 if open_ else 70))


def shaker(rng):
    n = int(.09 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    return (x - lp(x, 4500)) * np.sin(np.pi * t / t[-1]) ** 2 * .6


def epiano(m, d):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    mod = np.sin(2 * np.pi * f * 14 * t) * 1.1 * np.exp(-t / .25)
    return (np.sin(2 * np.pi * f * t + mod) * np.exp(-t / 1.3) + .2 * np.sin(4 * np.pi * f * t) * np.exp(-t / .4)) * env(n, .004, .25)


def piano(m, d):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    s = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.6 + k * .9)) / k ** 1.3 for k in range(1, 7))
    return s * env(n, .002, .2)


def pluck(m, d, bright=1.0):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    saw = 2 * ((f * t) % 1) - 1
    return lp(saw, 600 + 4000 * bright) * np.exp(-t * 6) * env(n, .002, .05) * .7


def pad(m, d, det=.004):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    s = sum(2 * ((f * (1 + det * k) * t) % 1) - 1 for k in (-1, 0, 1)) / 3
    return lp(s, 1400) * env(n, d * .35, d * .4) * .5


def bell(m, d=1.6):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * t + 2 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 3))) * np.exp(-t * 2.2) * env(n, .002, .1)


def bass(m, d, kind="sine"):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    if kind == "sine": s = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)
    else: s = lp(2 * ((f * t) % 1) - 1, 500)
    return s * env(n, .006, .06)


# ---------- düzenleme ----------
PRESETS = {
    # ad: bpm, akorlar (MIDI), akor sesi, bas, davul tarzı, melodi
    "lofi":       dict(bpm=84,  ch=[[50,53,57,60,64],[46,50,53,57,62],[43,46,50,53,57],[45,49,52,55,59]], keys=epiano, bass="sine", drums="lofi",  lead=None,   vinyl=True),
    "house":      dict(bpm=122, ch=[[57,60,64,67],[53,57,60,64],[55,59,62,65],[52,55,59,62]],         keys=piano,  bass="saw",  drums="house", lead=None,   stab=True),
    "ambient":    dict(bpm=76,  ch=[[48,55,59,62,64],[45,52,55,59,62],[41,48,53,57,60],[43,50,55,59,62]], keys=pad, bass="sine", drums="soft",  lead=bell),
    "trap":       dict(bpm=140, ch=[[49,52,56,59],[45,49,52,56],[47,51,54,57],[44,47,51,54]],         keys=pad,    bass="808",  drums="trap",  lead=pluck),
    "funk":       dict(bpm=108, ch=[[52,55,59,62],[57,60,64,67],[50,54,57,60],[55,59,62,66]],         keys=epiano, bass="saw",  drums="funk",  lead=pluck),
    "sinematik":  dict(bpm=96,  ch=[[45,52,57,60],[41,48,53,57],[48,55,60,64],[43,50,55,59]],         keys=pad,    bass="sine", drums="cine",  lead=piano),
    "pozitif":    dict(bpm=116, ch=[[48,52,55,60],[43,47,50,55],[45,48,52,57],[41,45,48,53]],         keys=pluck,  bass="sine", drums="pop",   lead=bell),
}


def build(name, p, dur=32.0, seed=0):
    rng = np.random.default_rng(seed)
    mx = Mix(dur); B = 60 / p["bpm"]; BAR = 4 * B
    nbars = int(np.ceil(dur / BAR)) + 1
    intro = 2 * BAR if p["drums"] not in ("cine", "soft") else BAR
    for b in range(nbars):
        t0 = b * BAR; ch = p["ch"][b % 4]
        # akorlar
        if p["keys"] is pad:
            for m in ch: mx.add(pad(m, BAR * 1.05), t0, .16, pan=rng.uniform(-.4, .4))
        elif p["keys"] is pluck:
            for i in range(8):
                m = ch[i % len(ch)] + (12 if i % 4 == 3 else 0)
                mx.add(pluck(m, B * .6, .5 + .5 * (b % 2)), t0 + i * B / 2, .28, pan=(-.3 if i % 2 else .3))
        elif p.get("stab"):
            for off in (B * .5, B * 1.5, B * 2.5, B * 3.25, B * 3.5):
                for m in ch: mx.add(p["keys"](m + 12, B * .45), t0 + off, .10)
        else:
            sw = B * .05
            for off, ln in ((0, B * 1.8), (B * 2.5 + sw, B * 1.4)):
                for k, m in enumerate(ch): mx.add(p["keys"](m, ln), t0 + off + k * .012, .12, pan=(k - 2) * .15)
        if t0 < intro and p["drums"] not in ("cine", "soft"): continue
        # bas
        root = ch[0] - 12
        if p["bass"] == "808":
            for off in (0, B * 1.5, B * 2.75): mx.add(k808(root - 12, B * 1.4), t0 + off, .55)
        else:
            pat = [(0, B * .9), (B * 1.5, B * .4), (B * 2, B * .9), (B * 3.5, B * .4)] if p["drums"] in ("funk", "house") else [(0, B * 1.9), (B * 2, B * 1.9)]
            for k, (off, ln) in enumerate(pat): mx.add(bass(root + (7 if k == 3 and p["drums"] == "funk" else 0), ln, p["bass"]), t0 + off, .32)
        # davul
        d = p["drums"]
        for q in range(16):
            t = t0 + q * B / 4
            if d == "house":
                if q % 4 == 0: mx.add(kick(1.1), t, .8)
                if q % 4 == 2: mx.add(hat(rng, open_=True), t, .16, .2)
                if q in (4, 12): mx.add(clap(rng), t, .45)
                if q % 2: mx.add(hat(rng), t, .08, -.2)
            elif d == "lofi":
                sw = B / 4 * .18 if q % 2 else 0
                if q in (0, 7, 10): mx.add(kick(.7), t, .6)
                if q in (4, 12): mx.add(snare(rng, tone=180), t, .32)
                if q % 2 == 0 or q % 4 == 3: mx.add(hat(rng), t + sw, .07 if q % 4 else .1, .25)
            elif d == "trap":
                if q in (0, 10): mx.add(kick(1.2), t, .7)
                if q in (8,): mx.add(clap(rng), t, .5)
                roll = 3 if q in (14, 15) and b % 2 else 1
                for r in range(roll): mx.add(hat(rng, .03), t + r * B / 12, .09, .3)
            elif d == "funk":
                if q in (0, 3, 6, 10): mx.add(kick(.9), t, .65)
                if q in (4, 12): mx.add(snare(rng, tone=210), t, .38)
                if q in (7, 15): mx.add(snare(rng, .08), t, .08)
                mx.add(hat(rng), t, .06 if q % 2 else .1, -.25)
            elif d == "pop":
                if q in (0, 8, 11): mx.add(kick(1.0), t, .7)
                if q in (4, 12): mx.add(clap(rng), t, .42)
                if q % 2 == 0: mx.add(shaker(rng), t, .12, .3)
            elif d == "soft":
                if q in (0, 8) and t0 >= BAR * 2: mx.add(kick(.5), t, .35)
                if q % 4 == 2 and t0 >= BAR * 2: mx.add(shaker(rng), t, .09, .4)
            elif d == "cine":
                if q % 2 == 0 and t0 >= BAR: mx.add(bass(ch[0] - 24, B / 3, "saw"), t, .18)
                if q in (0,) and t0 >= BAR * 2: mx.add(kick(.8, .8), t, .6)
                if q in (8,) and t0 >= BAR * 3: mx.add(snare(rng, .5, 120), t, .22)
        # melodi
        if p["lead"] is not None and b % 2 == 1:
            notes = [ch[-1] + 12, ch[-2] + 12, ch[1] + 12, ch[-1] + 12 + 2]
            for i, m in enumerate(notes):
                ln = B * .9
                sig = p["lead"](m, ln) if p["lead"] is not bell else bell(m)
                mx.add(sig, t0 + i * B, .14 if p["lead"] is not pluck else .2, pan=(.35 if i % 2 else -.35))
    if p.get("vinyl"):
        crack = (rng.random(mx.N) > .9994) * rng.standard_normal(mx.N) * .25 + rng.standard_normal(mx.N) * .006
        mx.L += lp(crack, 5000); mx.R += lp(crack, 5000)
    # basit oda yankısı + yumuşak sınırlayıcı
    for ch_ in (mx.L, mx.R):
        echo = np.zeros_like(ch_); dly = int(.11 * SR)
        echo[dly:] = ch_[:-dly] * .18
        ch_ += lp(echo, 3000)
    peak = max(np.abs(mx.L).max(), np.abs(mx.R).max()) or 1
    st = np.stack([mx.L, mx.R], 1) / peak * .9
    st = np.tanh(st * 1.3) / np.tanh(1.3)
    wav = DIR / f"{name}.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32000).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "aac", "-b:a", "128k", str(DIR / f"{name}.m4a")], check=True)
    os.remove(wav)
    print("✓", name)


if __name__ == "__main__":
    for i, (n, p) in enumerate(PRESETS.items()):
        build(n, p, seed=i + 7)
