"""Telifsiz müzik + efektler (30 sn), SeoveDijital tanıtım kurgusuna göre zamanlı: kancada arama çubukları için pop + yazma tıkı,
2.85'te onay çanı, 3.7'de drop, A minör 118 BPM, geçişlerde whoosh, sekme kaydırmada swipe, kapanışta boom + akor.
Kullanım: python3 muzik.py  ->  muzik.wav"""
import numpy as np, wave
SR = 44100; DUR = 30.0; N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(57)
L = np.zeros(N); R = np.zeros(N)


def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig)); s = sig[:j - i] * gain
    L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); n = int(np.log(1e-4) / np.log(a)) + 1
    return np.convolve(x, (1 - a) * a ** np.arange(n))[:len(x)]


def hp(x, fc): return x - lp(x, fc)


def env(n, a, r):
    e = np.ones(n); A = int(a * SR); Rn = int(r * SR)
    if A: e[:A] = np.linspace(0, 1, A)
    if Rn: e[-Rn:] *= np.linspace(1, 0, Rn)
    return e


hz = lambda m: 440 * 2 ** ((m - 69) / 12)
BPM = 118; BEAT = 60 / BPM; BAR = 4 * BEAT
DROP, END = 3.7, 25.95
HITS = [0.55, 1.25, 1.95]
# Am9 · Fmaj7 · Cmaj9 · G6
CH = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 52, 55, 59, 62], [55, 59, 62, 64, 67]]
chord_at = lambda s: CH[int(max(0, s - DROP) / BAR) % 4]


def pluck(m, d):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    s = sum(np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * (3 + h * 2.5)) / h for h in (1, 2, 3, 4))
    return s * env(n, .003, .05)


def epiano(m, d):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    mod = np.sin(2 * np.pi * f * 14 * tt) * 1.1 * np.exp(-tt / .25)
    return (np.sin(2 * np.pi * f * tt + mod) * np.exp(-tt / 1.4) + .25 * np.sin(4 * np.pi * f * tt) * np.exp(-tt / .4)) * env(n, .004, .3)


def boom(d=2.5):
    n = int(d * SR); tt = np.arange(n) / SR; f = 34 + 70 * np.exp(-tt / .07)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .7) + .5 * lp(rng.standard_normal(n), 1600) * np.exp(-tt / .25)


def hit():  # kanca darbesi: alçak tok vuruş + kağıt yırtılma sesi
    n = int(.6 * SR); tt = np.arange(n) / SR; f = 50 + 120 * np.exp(-tt / .025)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .18)
    rip = hp(rng.standard_normal(n), 2500) * np.exp(-tt / .05) * .5
    return body + rip


def noise_sweep(d, f0, f1, shape):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); acc = 0.0
    fc = np.linspace(f0, f1, n) if shape == 'up' else f0 + (f1 - f0) * np.sin(np.linspace(0, np.pi, n))
    a = np.exp(-2 * np.pi * fc / SR)
    for k in range(n): acc = (1 - a[k]) * x[k] + a[k] * acc; out[k] = acc
    return out * (np.linspace(0, 1, n) ** 2 if shape == 'up' else np.sin(np.linspace(0, np.pi, n)) ** 2)


riser = lambda d: noise_sweep(d, 300, 9000, 'up')
whoosh = lambda d=.6: noise_sweep(d, 600, 5600, 'arc')


def tick(): n = int(.03 * SR); return hp(rng.standard_normal(n), 3000) * np.exp(-np.arange(n) / SR / .006)


def ding(f, d=.9):
    n = int(d * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt / .15)) * np.exp(-tt / .35)


# Kanca (0–4): gerilimli drone + saat tıkırtısı, kesintilerde darbe
drone = np.zeros(N)
for m in [45, 52, 57, 60]:
    for d in (-.15, .15): drone += np.sin(2 * np.pi * hz(m) * (1 + d / 100) * t + rng.random() * 6)
drone = drone / 8 * np.clip(t / .6, 0, 1) * np.clip((DROP - t) / .25, 0, 1)
L += drone * .45; R += drone * .45
for k in range(int(DROP / (BEAT / 2))):
    n = int(.06 * SR); tt = np.arange(n) / SR
    add(np.sin(2 * np.pi * (2400 if k % 4 == 0 else 1800) * tt) * np.exp(-tt / .01), k * BEAT / 2, .05, pan=.3 if k % 2 else -.3)
for i, h in enumerate(HITS): add(hit(), h - .01, .4, pan=(-.2, 0, .2)[i])
add(ding(1319, 1.2), 2.85, .14, pan=-.2); add(ding(1760, 1.2), 2.9, .1, pan=.2)

# Ana bölüm (4–25.15)
duck = np.ones(N)
for k in range(int((END - DROP) / (BEAT / 4))):
    s = DROP + k * BEAT / 4; pos = k % 16
    if pos in (0, 4, 8, 12) or (pos == 14 and (k // 16) % 2):  # kick
        n = int(.4 * SR); tt = np.arange(n) / SR; f = 45 + 95 * np.exp(-tt / .03)
        add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .15), s, .75)
        i = int(s * SR); j = min(N, i + n); duck[i:j] = np.minimum(duck[i:j], 1 - .6 * np.exp(-np.arange(j - i) / SR / .12))
    if pos in (4, 12):  # clap
        n = int(.25 * SR); x = hp(lp(rng.standard_normal(n), 4000), 900); e = np.exp(-np.arange(n) / SR / .08); e[:int(.012 * SR)] *= 1.6
        add(x * e, s, .24)
    if pos % 2 == 1 or pos % 4 == 2:  # hi-hat
        n = int(.06 * SR); x = hp(rng.standard_normal(n), 7500) * np.exp(-np.arange(n) / SR / (.035 if pos % 4 == 2 else .012))
        add(x, s, .07 if pos % 4 == 2 else .04, pan=.35)
    # 16'lık bas (sürüş hissi)
    ch = chord_at(s); f = hz(ch[0] - 12 + (12 if pos % 4 == 2 else 0))
    n = int(BEAT / 4 * SR); tt = np.arange(n) / SR
    add(lp(np.sign(np.sin(2 * np.pi * f * tt)), 600) * env(n, .003, .03) * (1 if pos % 4 == 0 else .55), s, .16)
for b in range(int((END - DROP) / BAR) + 1):  # akor + arpej
    s = DROP + b * BAR; ch = CH[b % 4]
    for m in ch: add(epiano(m + 12, BAR), s, .05, pan=(m % 5 - 2) * .15)
    for k in range(8):
        if s + k * BEAT / 2 < END: add(pluck(ch[[0, 2, 4, 3, 1, 4, 2, 3][k] % 5] + 24, .4), s + k * BEAT / 2, .05, pan=.4 if k % 2 else -.4)
L *= (1 - .35 * (1 - duck)); R *= (1 - .35 * (1 - duck))

# Efektler
add(riser(1.0), 2.75, .3); add(boom(1.8), DROP, .6)
for w, g, pn in [(6.3, .3, -.3), (7.3, .35, .3), (10.2, .35, -.2), (10.9, .25, .4), (12.1, .25, -.4), (13.7, .35, .3), (16.2, .35, -.3), (19.3, .35, .3), (21.6, .35, -.2), (23.9, .35, .3)]:
    add(whoosh(.6), w - .25, g, pan=pn)
add(riser(1.0), 24.95, .35); add(boom(2.2), END, .8)
for a, txt, d in [(0.7, 9, .55), (1.4, 11, .55), (2.1, 12, .55)]:
    for k in range(txt): add(tick(), a + k * d / txt + .02, .2, pan=.1)
n = int(.12 * SR); tt = np.arange(n) / SR; add(np.sin(2 * np.pi * 1100 * tt) * np.exp(-tt / .03), 9.05, .2)  # CTA dokunuşu
add(ding(1047), 19.4, .1, pan=-.2)  # sonuç kartı
n = N - int(END * SR); tt = np.arange(n) / SR; s = np.zeros(n)
for m in [45, 57, 64, 67, 71, 76, 81]: s += epiano(m + 12, n / SR) * .5 + np.sin(2 * np.pi * hz(m) * tt) * .18
add(s * env(n, .02, 1.6) / 4, END, .9)


def verb(x):
    y = x.copy()
    for dl, g in [(.029, .3), (.043, .26), (.067, .22), (.103, .18), (.149, .14), (.211, .1), (.293, .06)]:
        d = int(dl * SR); y[d:] += x[:-d] * g
    return y


L = verb(L); R = verb(R)
mix = np.stack([L, R], 1)
mix *= np.minimum(1, np.minimum(t / .05, (DUR - t) / 1.3))[:, None]
mix = np.tanh(mix * 1.2); mix /= np.abs(mix).max() / .89
w = wave.open('muzik.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype('<i2').tobytes()); w.close()
print('muzik.wav')
