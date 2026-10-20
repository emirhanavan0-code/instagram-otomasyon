import numpy as np, wave
SR=44100; DUR=17.0; N=int(SR*DUR); t=np.arange(N)/SR
rng=np.random.default_rng(7)
L=np.zeros(N); Rr=np.zeros(N)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); j=min(N,i+len(sig)); s=sig[:j-i]*gain
    L[i:j]+=s*(1-max(0,pan)); Rr[i:j]+=s*(1+min(0,pan))
def lp(x,fc):
    a=np.exp(-2*np.pi*fc/SR); y=np.zeros_like(x); acc=0.0
    # vectorized-ish via scipy-free loop in chunks
    for k in range(len(x)): acc=(1-a)*x[k]+a*acc; y[k]=acc
    return y
def env(n,a,r):
    e=np.ones(n); A=int(a*SR); Rn=int(r*SR)
    if A: e[:A]=np.linspace(0,1,A)
    if Rn: e[-Rn:]*=np.linspace(1,0,Rn)
    return e
def saw(f,n,ph=0):
    tt=np.arange(n)/SR; return 2*((tt*f+ph)%1)-1
hz=lambda m:440*2**((m-69)/12)
BEAT=0.5
# pad: Am F C G, 2 s each
chords=[[57,60,64,69],[53,57,60,65],[48,55,60,64],[55,59,62,67]]
pad=np.zeros(N)
for ci in range(int(DUR/2)+1):
    st=ci*2.0; n=int(2.2*SR)
    if st>=DUR: break
    s=np.zeros(n)
    for m in chords[ci%4]:
        for d in (-0.08,0.08): s+=saw(hz(m)*(1+d/100*3),n,rng.random())
    s*=env(n,.35,.6)/8
    i=int(st*SR); j=min(N,i+n); pad[i:j]+=s[:j-i]
pad=lp(lp(pad,1400),2200)
# filter opening intro: amplitude ramp
pad*=np.clip(t/1.5,0.2,1)
# sidechain from 3.5 to 13.5
duck=np.ones(N)
kicks=[3.5+k*BEAT for k in range(int((13.5-3.5)/BEAT))]
for kt in kicks:
    i=int(kt*SR); n=int(.42*SR); j=min(N,i+n); duck[i:j]=np.minimum(duck[i:j],1-0.65*np.exp(-np.arange(j-i)/SR/0.12))
padL=pad*duck; 
L+=padL*0.55; Rr+=padL*0.55
# sub bass following chord roots (8ths) from 3.5
for k in range(int((13.5-3.5)/(BEAT/2))):
    st=3.5+k*BEAT/2; ci=int(st/2)%4; f=hz(chords[ci][0]-12)
    n=int(.22*SR); tt=np.arange(n)/SR; s=np.sin(2*np.pi*f*tt)*np.exp(-tt/.18)*env(n,.005,.03)
    add(s, st, 0.22 if k%2 else 0.3)
# kick
def kick():
    n=int(.45*SR); tt=np.arange(n)/SR; f=48+90*np.exp(-tt/.035)
    ph=2*np.pi*np.cumsum(f)/SR; return np.sin(ph)*np.exp(-tt/.16)
K=kick()
for kt in kicks: add(K,kt,0.75)
# hats offbeat
def hat(dec=.04):
    n=int(.12*SR); x=rng.standard_normal(n); x=x-lp(x,6000); return x*np.exp(-np.arange(n)/SR/dec)
for k in range(int((13.5-4.6)/BEAT)):
    add(hat(),4.6+k*BEAT+BEAT/2,0.10,pan=0.3)
    add(hat(.015),4.6+k*BEAT+BEAT*0.75,0.04,pan=-0.3)
# pluck arp from 4.6
for k in range(int((13.4-4.6)/(BEAT/2))):
    st=4.6+k*BEAT/2; ci=int(st/2)%4; m=chords[ci][(k*3)%4]+12
    n=int(.3*SR); tt=np.arange(n)/SR
    s=(np.sin(2*np.pi*hz(m)*tt)+0.3*np.sin(4*np.pi*hz(m)*tt))*np.exp(-tt/.09)
    add(s,st,0.07,pan=0.4 if k%2 else -0.4)
# fx
def riser(d):
    n=int(d*SR); x=rng.standard_normal(n); out=np.zeros(n); acc=0.0
    fcs=np.linspace(300,9000,n)**1; a=np.exp(-2*np.pi*fcs/SR)
    for k in range(n): acc=(1-a[k])*x[k]+a[k]*acc; out[k]=acc
    return out*np.linspace(0,1,n)**2
def whoosh(d=.6):
    n=int(d*SR); x=rng.standard_normal(n); out=np.zeros(n); acc=0.0
    fcs=600+5000*np.sin(np.linspace(0,np.pi,n)); a=np.exp(-2*np.pi*fcs/SR)
    for k in range(n): acc=(1-a[k])*x[k]+a[k]*acc; out[k]=acc
    return out*np.sin(np.linspace(0,np.pi,n))**2
def boom(d=2.5):
    n=int(d*SR); tt=np.arange(n)/SR; f=38+60*np.exp(-tt/.08)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt/.7)
    nz=rng.standard_normal(n); nz=lp(nz,1800)*np.exp(-tt/.25)
    return s+0.6*nz
add(riser(1.7),1.8,0.35); add(whoosh(.7),3.1,0.5); add(boom(1.6),3.5,0.5)
add(whoosh(.5),5.0,0.25,pan=-.3); add(whoosh(.6),7.4,0.35,pan=.3); add(whoosh(1.0),8.5,0.35)
add(whoosh(.7),10.4,0.45,pan=-.4); add(riser(1.4),12.15,0.4); add(whoosh(.6),13.1,0.45)
add(boom(3.4),13.55,0.85)
# typing ticks and tap
for k in range(16):
    n=int(.03*SR); x=rng.standard_normal(n); x=x-lp(x,3000); add(x*np.exp(-np.arange(n)/SR/.006),5.35+k*1.2/16+rng.random()*.02,0.18,pan=.1)
n=int(.12*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*1200*tt)*np.exp(-tt/.03),6.75,0.15)
add(np.sin(2*np.pi*1600*tt)*np.exp(-tt/.05),6.95,0.12)
# end pad: sustained chord bloom from 13.55
n=N-int(13.55*SR); s=np.zeros(n)
for m in [45,57,60,64,69,76]:
    for d in (-.1,.1): s+=saw(hz(m)*(1+d/100*2),n,rng.random())
s=lp(lp(s,1800),1800)*env(n,.08,2.2)/10
add(s,13.55,0.8)
# simple reverb: multitap
def verb(x):
    y=x.copy()
    for dl,g in [(.031,.35),(.047,.3),(.071,.25),(.113,.2),(.163,.15),(.229,.1)]:
        d=int(dl*SR); y[d:]+=x[:-d]*g
    return y
L=verb(L); Rr=verb(Rr[::1])
mix=np.stack([L,Rr],1)
mix*=np.minimum(1,np.minimum(t/0.15,(DUR-t)/1.2))[:,None]
mix=np.tanh(mix*1.1)
mix/=np.abs(mix).max()/0.89
w=wave.open('muzik.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype('<i2').tobytes()); w.close()
print('ok')
