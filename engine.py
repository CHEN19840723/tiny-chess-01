# Original R8 engine: tapered PST, PVS, qsearch, TT, killers/history.
import os,sys,json,urllib.request,time
V=(0,82,337,365,477,1025,0)
N=(-33,-31,-18,-14,14,18,31,33)
D=(-17,-16,-15,-1,1,15,16,17)
G='abcdefgh'
# Compact symmetric PSTs, from White's perspective, ranks 1..8.
P='<<<<<<<<AFF((FFAA72<<27A<<<PP<<<AAFUUFAAFFPZZPFFnnnnnnnn<<<<<<<<\n\x14\x1e\x1e\x1e\x1e\x14\n\x14(<AA<(\x14\x1eAFKKFA\x1e\x1e<KPPK<\x1e\x1eAKPPKA\x1e\x1e<FKKF<\x1e\x14(<<<<(\x14\n\x14\x1e\x1e\x1e\x1e\x14\n(222222(2<<<<<<22AAFFAA22<FFFF<22<AFFA<22<<AA<<22<<<<<<2(222222(<<<AA<<<7<<<<<<77<<<<<<77<<<<<<77<<<<<<77<<<<<<7AFFFFFFA<<<<<<<(227722(2<A<<<<22AAAAA<2<<AAAA<77<AAAA<77<<<<<<72<<<<<<2(227722(\x1e\x14\x14\n\n\x14\x14\x1e\x1e\x14\x14\n\n\x14\x14\x1e\x1e\x14\x14\n\n\x14\x14\x1e\x1e\x14\x14\n\n\x14\x14\x1e(\x1e\x1e\x14\x14\x1e\x1e(2((((((2PP<<<<PPPZF<<FZP\n\x1e\x1e\x1e\x1e\x1e\x1e\n\x1e\x1e<<<<\x1e\x1e\x1e2PZZP2\x1e\x1e2ZddZ2\x1e\x1e2ZddZ2\x1e\x1e2PZZP2\x1e\x1e<<<<<\x1e\x1e\n\x1e\x1e\x1e\x1e\x1e\x1e\n'

T={};K={};H={};nodes=0
class Timeout(Exception):pass
def parse(f):
 f=f.split();b=[0]*128;p={c:i+1 for i,c in enumerate('pnbrqk')}
 for r,s in enumerate(f[0].split('/')):
  x=(7-r)*16
  for c in s:
   if c.isdigit():x+=int(c)
   else:b[x]=p[c.lower()]*(1-2*c.islower());x+=1
 return b,1-2*(f[1]!='w'),sum(1<<i for i,c in enumerate('KQkq')if c in f[2]),-1 if f[3]=='-'else(int(f[3][1])-1)*16+G.index(f[3][0]),int(f[4])
def attack(b,k,s):
 for x in(k-16*s-1,k-16*s+1):
  if not x&136 and b[x]==s:return 1
 for d in N+D:
  x=k+d
  if x&136:continue
  p=b[x]
  if p*s>0 and ((d in N and abs(p)==2)or(d in D and abs(p)==6)):return 1
 for d in D:
  x=k+d
  while not x&136:
   p=b[x]
   if p:
    if p*s>0 and abs(p)in((4,5)if d in(-16,-1,1,16)else(3,5)):return 1
    break
   x+=d
 return 0
def play(p,m):
 b,s,c,e,h=p;b=b.copy();a,z,q=m;v=b[a];w=b[z];b[a]=0
 if abs(v)==1 and z==e and not w:b[z-16*s]=0;w=-s
 b[z]=(5-'qrbn'.index(q))*s if q else v
 if abs(v)==6:
  c&=12 if s==1 else 3
  if z==a+2:b[z-1]=b[z+1];b[z+1]=0
  if z==a-2:b[z+1]=b[z-2];b[z-2]=0
 if a==0 or z==0:c&=13
 if a==7 or z==7:c&=14
 if a==112 or z==112:c&=7
 if a==119 or z==119:c&=11
 return b,-s,c,a+16*s if abs(v)==1 and abs(z-a)==32 else-1,0 if abs(v)==1 or w else h+1
def moves(p,caps=0):
 b,s,c,e,h=p;r=[]
 for a,v in enumerate(b):
  if v*s<=0:continue
  t=abs(v)
  if t==1:
   d=16*s
   if not b[a+d]:
    if a+d>>4==(7 if s==1 else 0):r.extend((a,a+d,q)for q in'qrbn')
    else:r.append((a,a+d,''))
    if a>>4==(1 if s==1 else 6)and not b[a+2*d]:r.append((a,a+2*d,''))
   for d in(16*s-1,16*s+1):
    z=a+d
    if not z&136 and(b[z]*s<0 and abs(b[z])<6 or z==e):
     if z>>4==(7 if s==1 else 0):r.extend((a,z,q)for q in'qrbn')
     else:r.append((a,z,''))
  else:
   for d in N if t==2 else D[::2]if t==4 else D[1::2]if t==3 else D:
    z=a+d
    while not z&136:
     if not b[z]:r.append((a,z,''))
     else:
      if b[z]*s<0 and abs(b[z])<6:r.append((a,z,''))
      break
     if t in(2,6):break
     z+=d
  if t==6:
   if a==4 and c&1 and not(b[5]or b[6]or attack(b,4,-1)or attack(b,5,-1)):r.append((4,6,''))
   if a==4 and c&2 and not(b[3]or b[2]or b[1]or attack(b,4,-1)or attack(b,3,-1)):r.append((4,2,''))
   if a==116 and c&4 and not(b[117]or b[118]or attack(b,116,1)or attack(b,117,1)):r.append((116,118,''))
   if a==116 and c&8 and not(b[115]or b[114]or b[113]or attack(b,116,1)or attack(b,115,1)):r.append((116,114,''))
 return [m for m in r if(not caps or m[2]or b[m[1]]and abs(b[m[1]])!=6)and not attack(play(p,m)[0],play(p,m)[0].index(6*s),-s)]
def value(p):
 b,s,c,e,h=p;q=5 in b or -5 in b;score=0
 for x,v in enumerate(b):
  if not v:continue
  y=x if v>0 else x^119;r=y>>4;f=y&7;i=r*8+f;t=abs(v)
  if t==6:z=ord(P[320+i]if q else P[384+i])-60
  else:z=V[t]+ord(P[(t-1)*64+i])-60
  score+=z*(1 if v>0 else-1)
 return score*s
def search(p,d,a,b,ply=0):
 global nodes
 nodes+=1
 if nodes&1023==0 and time.monotonic()>end:raise Timeout
 if p[4]>=100:return 0
 inc=attack(p[0],p[0].index(6*p[1]),-p[1])
 if inc:d+=1
 elif d>2 and value(p)>=b+90:
  v=-search((p[0],-p[1],p[2],-1,p[4]),d-3,-b,-b+1,ply+1)
  if v>=b:return v
 if d<=0:return quiesce(p,a,b,ply)
 key=hash((tuple(p[0]),p[1],p[2],p[3]));old=T.get(key);a0=a
 if old and old[0]>=d and(old[2]==0 or old[2]==1 and old[1]<=a or old[2]==2 and old[1]>=b):return old[1]
 ms=moves(p)
 if not ms:return -20000+ply if attack(p[0],p[0].index(6*p[1]),-p[1])else 0
 tm=old[3]if old else None
 ms.sort(key=lambda m:(m!=tm,-bool(p[0][m[1]]or m[2]),-H.get(m,0),m!=K.get(ply)))
 best=-30000
 for i,m in enumerate(ms):
  if i>1 and d>1 and not p[0][m[1]]and not m[2]:v=-search(play(p,m),max(0,d-2-i//3),-a-1,-a,ply+1)
  else:v=0
  if not i or v>a:
   v=-search(play(p,m),d-1,-a-1,-a,ply+1)
   if a<v<b:v=-search(play(p,m),d-1,-b,-a,ply+1)
  if v>best:best=v;bm=m
  if v>a:a=v
  if a>=b:
   if not p[0][m[1]]:
    K[ply]=m;H[m]=H.get(m,0)+d*d
   break
 T[key]=(d,best,0 if a0<best<b else 1 if best<=a0 else 2,bm)
 return best
def quiesce(p,a,b,ply):
 global nodes
 nodes+=1
 if nodes&1023==0 and time.monotonic()>end:raise Timeout
 v=value(p)
 if v>=b:return v
 a=max(a,v);ms=moves(p,1);ms.sort(key=lambda m:-V[abs(p[0][m[1]])])
 for m in ms:
  if p[0][m[1]]and v+V[abs(p[0][m[1]])]+180<a:continue
  v=-quiesce(play(p,m),-b,-a,ply+1)
  if v>=b:return v
  a=max(a,v)
 return a
def uci(m):return G[m[0]&7]+str((m[0]>>4)+1)+G[m[1]&7]+str((m[1]>>4)+1)+m[2]
def choose(fen,legal):
 global nodes,end
 p=parse(fen);ms=moves(p);best=ms[0];nodes=0;end=time.monotonic()+float(os.environ.get('ENGINE_TIME','7.5'))
 try:
  for d in range(1,30):
   a=-30000;cur=None
   if cur:pass
   ms.sort(key=lambda m:m!=best)
   for m in ms:
    v=-search(play(p,m),d-1,-30000,-a,1)
    if v>a:a=v;cur=m
   best=cur
   print('depth',d,'score',a,'nodes',nodes,file=sys.stderr,flush=True)
   if abs(a)>19000:break
 except Timeout:pass
 u=uci(best);return u if u in legal else legal[0]
def request(path,body):
 with urllib.request.urlopen(urllib.request.Request(os.environ['MAKEFUN_ENV_URL']+path,data=json.dumps(body).encode())) as r:return json.load(r)
def main():
 while 1:
  a=request('/game',{})
  if a['status']=='done':break
  while a['status']=='your_move':a=request('/move',{'game':a['game'],'move':choose(a['fen'],a['legal_moves'])})
  print(a['game'],a['outcome'],a['reason'])
if __name__=='__main__':main()
