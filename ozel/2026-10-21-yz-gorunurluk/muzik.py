"""Telifsiz müzik + efektler (24,5 sn). SeoveBülten reels'inden farklı: D minör, 100 BPM, elektrik piyano akorları,
swing'li hi-hat, yumuşak clap, çan arpejleri; kurgudaki her geçişe whoosh, yazmaya tık, sonuçlara 'ding'.
Kullanım: python3 muzik.py  ->  muzik.wav"""
import numpy as np, wave
SR = 44100; DUR = 24.5; N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(21)
L = np.zeros(N); R = np.zeros(N)


def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig)); s = sig[:j - i] * gain
    L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))


def lp(x, fc):
    """Tek kutuplu alçak geçiren filtre (üstel çekirdekle konvolüsyon)."""
    a = np.exp(-2 * np.pi * fc / SR); n = int(np.log(1e-4) / np.log(a)) + 1
    k = (1 - a) * a ** np.arange(n)
    return np.convolve(x, k)[:len(x)]


def hp(x, fc): return x - lp(x, fc)


def env(n, a, r):
    e = np.ones(n); A = int(a * SR); Rn = int(r * SR)
    if A: e[:A] = np.linspace(0, 1, A)
    if Rn: e[-Rn:] *= np.linspace(1, 0, Rn)
    return e


hz = lambda m: 440 * 2 ** ((m - 69) / 12)
BPM = 100; BEAT = 60 / BPM; BAR = 4 * BEAT
DROP, END = 3.55, 22.85
# Dm9 · Bbmaj7 · Gm9 · A7sus4 (her akor bir ölçü)
CH = [[50, 53, 57, 60, 64], [46, 50, 53, 57, 62], [43, 46, 50, 53, 57], [45, 50, 52, 55, 59]]
chord_at = lambda s: CH[int(max(0, s - DROP) / BAR) % 4] if s >= DROP else CH[0]


def epiano(m, d):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    mod = np.sin(2 * np.pi * f * 14 * tt) * 1.2 * np.exp(-tt / .25)
    s = np.sin(2 * np.pi * f * tt + mod) * np.exp(-tt / 1.4) + .25 * np.sin(4 * np.pi * f * tt) * np.exp(-tt / .4)
    return s * env(n, .004, .3)


# Giriş (0–3.55): yumuşak pad + saat tıkırtısı gibi ince pluck
pad = np.zeros(N)
for m in [38, 50, 57, 60, 64]:
    for d in (-.12, .12):
        pad += np.sin(2 * np.pi * hz(m) * (1 + d / 100) * t + rng.random() * 6)
pad = pad / 10 * np.clip(t / 1.2, 0, 1) * np.clip((DROP + .2 - t) / .4, 0, 1)
L += pad * .5; R += pad * .5
for k in range(int(DROP / (BEAT / 2))):
    n = int(.08 * SR); tt = np.arange(n) / SR
    add(np.sin(2 * np.pi * (2200 if k % 4 == 0 else 1700) * tt) * np.exp(-tt / .012), k * BEAT / 2 + .1, .06, pan=.3 if k % 2 else -.3)

# Ana bölüm (3.55–22.85)
steps = int((END - DROP) / (BEAT / 4))
duck = np.ones(N)
for k in range(steps):
    s = DROP + k * BEAT / 4
    pos = k % 16
    swing = (BEAT / 4) * .18 if k % 2 else 0
    if pos in (0, 6, 8, 11):  # kick (hafif kırık ritim)
        n = int(.4 * SR); tt = np.arange(n) / SR; f = 46 + 85 * np.exp(-tt / .03)
        add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .14), s, .7)
        i = int(s * SR); j = min(N, i + n); duck[i:j] = np.minimum(duck[i:j], 1 - .55 * np.exp(-np.arange(j - i) / SR / .11))
    if pos in (4, 12):  # clap
        n = int(.25 * SR); x = hp(lp(rng.standard_normal(n), 3500), 900)
        e = np.exp(-np.arange(n) / SR / .07); e[:int(.012 * SR)] *= 1.6
        add(x * e, s, .22)
    if k % 2 == 1 or pos % 4 == 2:  # hi-hat (swing)
        n = int(.06 * SR); x = hp(rng.standard_normal(n), 7000) * np.exp(-np.arange(n) / SR / (.03 if pos % 4 == 2 else .012))
        add(x, s + swing, .07 if pos % 4 == 2 else .04, pan=.35)
    if pos % 2 == 0:  # sub bas
        ch = chord_at(s); f = hz(ch[0] - 12)
        n = int(BEAT / 2 * SR); tt = np.arange(n) / SR
        add(np.sin(2 * np.pi * f * tt) * env(n, .005, .05) * (1 if pos in (0, 8) else .6), s, .26)
# Elektrik piyano akorları (her ölçü başı + senkoplu tekrar)
for b in range(int((END - DROP) / BAR) + 1):
    s = DROP + b * BAR; ch = CH[b % 4]
    for off, g in ((0, .1), (BEAT * 2.5, .06)):
        if s + off < END:
            for m in ch: add(epiano(m + 12, BAR), s + off, g / 2, pan=(m % 5 - 2) * .15)
# Çan arpeji (motif)
motif = [0, 2, 4, 3, 1, 4, 2, 3]
for k in range(int((END - DROP - BAR) / (BEAT / 2))):
    s = DROP + BAR + k * BEAT / 2; ch = chord_at(s); m = ch[motif[k % 8] % len(ch)] + 24
    n = int(.5 * SR); tt = np.arange(n) / SR
    bell = (np.sin(2 * np.pi * hz(m) * tt) + .4 * np.sin(2 * np.pi * hz(m) * 2.76 * tt) * np.exp(-tt / .08)) * np.exp(-tt / .22)
    add(bell, s, .045, pan=.45 if k % 2 else -.45)
# Kick'e bağlı hafif sidechain (pompa hissi)
L *= (1 - .35 * (1 - duck)); R *= (1 - .35 * (1 - duck))


# Efektler
def noise_sweep(d, f0, f1, shape):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); acc = 0.0
    fc = np.linspace(f0, f1, n) if shape == 'up' else f0 + (f1 - f0) * np.sin(np.linspace(0, np.pi, n))
    a = np.exp(-2 * np.pi * fc / SR)
    for k in range(n): acc = (1 - a[k]) * x[k] + a[k] * acc; out[k] = acc
    return out * (np.linspace(0, 1, n) ** 2 if shape == 'up' else np.sin(np.linspace(0, np.pi, n)) ** 2)


riser = lambda d: noise_sweep(d, 300, 9000, 'up')
whoosh = lambda d=.6: noise_sweep(d, 600, 5600, 'arc')


def boom(d=2.5):
    n = int(d * SR); tt = np.arange(n) / SR; f = 36 + 64 * np.exp(-tt / .08)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .7) + .5 * lp(rng.standard_normal(n), 1600) * np.exp(-tt / .25)


def tick(): n = int(.03 * SR); return hp(rng.standard_normal(n), 3000) * np.exp(-np.arange(n) / SR / .006)


def ding(f, d=.9):
    n = int(d * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt / .15)) * np.exp(-tt / .35)


add(riser(1.6), 1.95, .35); add(whoosh(.7), 3.1, .5); add(boom(1.8), DROP, .55)
for w, g, pn in [(4.85, .3, -.3), (6.15, .35, .3), (7.65, .3, -.2), (10.85, .35, .3), (12.25, .35, -.3), (14.95, .3, .2), (17.95, .4, -.3), (20.45, .4, .3)]:
    add(whoosh(.6), w - .2, g, pan=pn)
add(riser(1.2), 21.7, .35); add(whoosh(.7), 22.45, .5); add(boom(2.0), END, .8)
for k in range(30): add(tick(), .35 + k * 1.0 / 30 + rng.random() * .015, .16, pan=.1)       # sohbet sorusu
for k in range(17): add(tick(), 8.15 + k * 1.0 / 17 + rng.random() * .015, .16, pan=-.1)    # marka
for k in range(12): add(tick(), 9.3 + k * .7 / 12 + rng.random() * .015, .16, pan=.1)       # site
add(ding(1400, .2), 10.15, .12)                                                             # sektör seçimi
n = int(.12 * SR); tt = np.arange(n) / SR; add(np.sin(2 * np.pi * 1100 * tt) * np.exp(-tt / .03), 11.45, .18)  # dokunma
add(ding(880), 12.9, .13, pan=-.2); add(ding(1175), 13.75, .13, pan=.2); add(ding(1568, 1.4), 14.6, .16)  # cevaplar
for k in range(12): add(ding(900 + k * 60, .12), 15.7 + k * 1.3 / 12 * (k / 12) ** .5, .05)           # skor sayacı
add(ding(1760, .6), 2.05, .07)                                                               # yapay zekâ cevabı
# Kapanış akoru
n = N - int(END * SR); tt = np.arange(n) / SR; s = np.zeros(n)
for m in [38, 50, 57, 60, 64, 69, 74]:
    s += epiano(m + 12, n / SR) * .5 + np.sin(2 * np.pi * hz(m) * tt) * .2
add(s * env(n, .02, 1.6) / 4, END, .9)


def verb(x):
    y = x.copy()
    for dl, g in [(.029, .32), (.043, .28), (.067, .24), (.103, .2), (.149, .15), (.211, .11), (.293, .07)]:
        d = int(dl * SR); y[d:] += x[:-d] * g
    return y


L = verb(L); R = verb(R)
mix = np.stack([L, R], 1)
mix *= np.minimum(1, np.minimum(t / .1, (DUR - t) / 1.3))[:, None]
mix = np.tanh(mix * 1.15); mix /= np.abs(mix).max() / .89
w = wave.open('muzik.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype('<i2').tobytes()); w.close()
print('muzik.wav')
