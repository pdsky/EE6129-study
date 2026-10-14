#!/usr/bin/python3
"""Numerical checks for EE6129 past exam solutions (2023-24 S2 .. 2025-26 S2)."""
from math import *
import cmath
def Q(x): return 0.5*erfc(x/sqrt(2))
def Qinv(p):
    lo,hi=-10,40
    for _ in range(200):
        m=(lo+hi)/2
        if Q(m)>p: lo=m
        else: hi=m
    return lo
def erlB(A,M):
    b=1.0
    for k in range(1,M+1): b=A*b/(k+A*b)
    return b
def erlC(A,M):
    B=erlB(A,M); r=A/M
    return B/(1-r+r*B)
def solve(f,M,p):
    lo,hi=1e-6,M*1.5
    for _ in range(200):
        m=(lo+hi)/2
        if f(m,M)<p: lo=m
        else: hi=m
    return lo
dB=lambda x:10*log10(x); lin=lambda d:10**(d/10)

print('=== 2324S2')
# Q1a(ii) shadowing
z=Qinv(0.01); print('Q1a(ii) z=',z,' sigma<=',10/z,' var<=',(10/z)**2)
# Q1a(iv)
eps=0.001; print('Q1a(iv) -ln(1-eps)=',-log(1-eps),' FM=',-dB(-log(1-eps)))
# Q1b(i) DPSK SD
g10,g12=lin(10),lin(12)
avg_in=0.2*g10+0.8*g12; print('Q1b(i) avg branch SNR',avg_in,dB(avg_in),' avg dB',0.2*10+0.8*12)
pl=0.2*0.2
avg_out=pl*g10+(1-pl)*g12; print(' SD out',avg_out,dB(avg_out))
Pe=pl*0.5*exp(-g10)+(1-pl)*0.5*exp(-g12); print(' Pe SD',Pe, ' single-branch Pe',0.2*0.5*exp(-g10)+0.8*0.5*exp(-g12))
# Q2a
s2=0.3*(1+0.36); s=sqrt(s2); print('Q2a var',s2,'sd',s,' Pe',0.5*(Q(0.64/s)+Q(1.36/s)), Q(0.64/s),Q(1.36/s))
print(' no-eq Pe (h=1,0,0.6):',0.5*(Q(0.4/sqrt(0.3))+Q(1.6/sqrt(0.3))))
# Q2b
h=[1,-0.6,0.2]; N=4
for k in range(1,N+1):
    H=sum(h[i]*cmath.exp(-2j*pi*i*k/N) for i in range(3)); print(' H',k,H,abs(H))
print(' loss',dB(5/4))
# Q3a
Au=0.9*90/3600; print('Q3a Au',Au)
A57=solve(erlB,57,0.01); print(' A(57,1%)',A57,' users',A57/Au)
m=A57/Au; area=m/720; R=sqrt(area/(3*sqrt(3)/2)); print(' area',area,' R',R,' Tg',m/57, ' trunking eff',A57/57)
A19=solve(erlB,19,0.01); Ac=3*A19; m2=Ac/Au; R2=sqrt(m2/720/(3*sqrt(3)/2)); print(' A19',A19,' cell',Ac,' users',m2,' R',R2,' Tg',m2/57, 'eff', Ac/57)
# Q4c
for n in [4]:
    print('Q4c(i)',1.76+20*log10(7), dB(sqrt(21)**4/6))
n=log10(600)/log10(sqrt(21)); print(' n',n)
Qr=sqrt(21); sir=1/(2*(Qr-1)**-n+2*Qr**-n+2*(Qr+1)**-n); print(' worst',dB(sir))
sir=1/(Qr**-n+(Qr+0.7)**-n); print(' 120',dB(sir))

print('=== 2425S2')
print('Q1a(i) B=log10 d',88/35,' d=',10**(88/35))
print('Q1a(ii) Ts',6e-6/3,' errors/s',5*3)
g=[lin(18),lin(10),lin(3)]
inv0=(1+sum(1/x for x in g))/3; print('Q1a(iii) 1/g0',inv0,' g0',1/inv0,dB(1/inv0),[inv0-1/x for x in g])
gb=Qinv(1.35e-3)**2/2; print('Q1b(i) gb',gb); x=1-exp(-gb/30); print(' base',x,' M',log(0.02)/log(x), [x**M for M in (1,2,3)])
print('Q1b(ii) SNR',10**(3/3),' R',2*log2(10))
print('Q1b(iii)',log2(1+1*4/0.25),log2(1+2/0.25))
print('Q2a(iii)',0.5*(Q(0.4/0.8)+Q(1.6/0.8)),Q(0.5),Q(2))
Pk=2**3.6-1; H=[1,0.2,1,1.4]; P=[Pk/x**2 for x in H]; print('Q2b(iii)',Pk,P,sum(P))
# Q3
ch=(20-2)/0.2*8; print('Q3 channels',ch)
for N in [3,4,7,9,12]:
    q=sqrt(3*N); print(' N',N,' omni simple',dB(q**3.7/6),' worst',dB(1/(2*(q-1)**-3.7+2*q**-3.7+2*(q+1)**-3.7)),' 120',dB(1/(q**-3.7+(q+0.7)**-3.7)))
Acell=3*sqrt(3)/2*1.0; traf=Acell*2000*0.03; print(' cell area',Acell,' traffic',traf)
A80=solve(erlB,80,0.01); print(' A80',A80)
area=A80/(2000*0.03); print(' new area',area,' R',sqrt(area/(3*sqrt(3)/2)))
for N in [4,7]:
    c=720/N; A=solve(erlB,int(c),0.01); print(' N',N,'ch/cell',c,'A omni',A)
A60=solve(erlB,60,0.01); totalA=60*Acell*2000*0.03; print(' sector A60',A60,'cell',3*A60,' total traffic',totalA,' cells',totalA/(3*A60))
A56=solve(erlB,56,0.01); print(' (no sharing 56/sector)',A56, totalA/(3*A56))
# Q4c
A56b=solve(erlB,56,0.02); A72=solve(erlB,72,0.02); print('Q4c A56',A56b,A56b*0.98,A56b/56,A56b*.98/56,A56b/0.5,' A72',A72,A72*.98,A72/72,A72*.98/72,A72/0.5)

print('=== 2526S1')
print('Q1a(iii)',Q(1/0.5))
g=[lin(11),lin(12),lin(13)]; p=[0.2,0.5,0.3]
gin=sum(a*b for a,b in zip(g,p)); print('Q1b(i) in',gin,dB(gin),' dBavg',sum(a*b for a,b in zip([11,12,13],p)),' MRC out',2*gin,dB(2*gin),' d',-log10(2e-4)/log10(gin))
print('Q2a(ii)',0.5*(Q(0.7/0.6)+Q(1.3/0.6)),Q(0.7/0.6),Q(1.3/0.6), ' no ISI',Q(1/0.6))
print('Q2b(i) N>=',500/30,' (ii) T',50/500e3,' Rb no CP',50*2/(50/500e3),' with CP',50*2/(50/500e3+10e-6))
cellA=3*sqrt(3)/2*4; print('Q3a cell area',cellA,' cells',1500/cellA)
chs=(25e3-40)/30; print(' channels',chs,' voice',chs-18,' per cell',(chs-18)/9, chs/9)
print(' eta',1/(0.03*cellA*9), ' alt',(chs/9*ceil(1500/cellA))/(25*1500))
c=1001//9; A=solve(erlC,c,0.05); print('Q3b ch/cell',1001/9,' A',A, ' users/cell',A/0.03,' per km2',A/0.03/4,' H s',0.03/1.5*3600)

print('=== 2526S2')
print('Q1a(ii) LCR',40/10,' per fade',20/5,' errs/s',4*4)
g=lin(25); e=0.005; gm=g*(-log(1-e)); print('Q1a(iii) gmin',gm,dB(gm),' FM',25-dB(gm), -dB(-log(1-e)))
print('Q1b(i) g',lin(3),' Pe',lin(12)**-3.7, ' (with output SNR)',lin(15)**-3.7)
print('Q2a(ii) noise',0.25*2.56,' (iii) Pe',0.5*(Q(0.2/0.8+0.8/0.8-0.2/0.8)+0),' ',0.5*(Q(0.8/0.8)+Q(1.2/0.8)),Q(1),Q(1.5))
h=[1,0.3]
for k in range(1,5): print(' H',k,sum(h[i]*cmath.exp(-2j*pi*i*k/4) for i in range(2)))
print(' Tofdm',4*2,' total',8+20,' loss',dB(28/8))
cl=1071/7; print('Q3a ch/cell',cl,' cluster area',42,' reps',2100/42,' cap',1071*2100/42)
A=solve(erlC,153,0.05); print('Q3b A',A,' users/cell',A/0.03,' per km2',A/0.03/6,' H',0.03/1.2*3600)
