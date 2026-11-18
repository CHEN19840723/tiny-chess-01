import argparse,importlib.util,time,json,collections,concurrent.futures,types
START='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
NEW=load('engine.py','new_engine')
R7=types.ModuleType('r7');exec(open('/tmp/r7-engine.py').read().split('while True:')[0],R7.__dict__)
# R7's qsearch omits non-losing captures; keep its baseline search safe.
_original_r7_choose=R7.choose
def safe_r7_choose(fen,legal):
 if not R7.moves(R7.position(fen)):return legal[0]
 return _original_r7_choose(fen,legal)
R7.choose=safe_r7_choose
def position(f,mod=NEW):return mod.parse(f)if mod==NEW else mod.position(f)
def moves(f,mod=NEW):return {mod.uci(m):m for m in mod.moves(position(f,mod))}
def apply(f,u):
 p=NEW.play(position(f),moves(f)[u]);board=p[0];rows=[]
 for rank in range(7,-1,-1):
  row='';n=0
  for x in range(8):
   v=board[rank*16+x]
   if not v:n+=1;continue
   if n:row+=str(n);n=0
   c=' pnbrqk'[abs(v)];row+=c.upper()if v>0 else c
  if n:row+=str(n)
  rows.append(row)
 c=''.join(x for i,x in enumerate('KQkq')if p[2]&1<<i)or'-'
 e='-'if p[3]<0 else NEW.G[p[3]&7]+str((p[3]>>4)+1)
 return '/'.join(rows)+' '+('w'if p[1]==1 else'b')+' '+c+' '+e+' '+str(p[4])+' '+str(int(f.split()[5])+('b'==f.split()[1]))
OPENINGS=['','e2e4 e7e5','d2d4 d7d5','c2c4 e7e5','e2e4 c7c5','d2d4 g8f6','g1f3 d7d5','e2e4 e7e6','c2c4 g8f6','b2b3 d7d5']
def opening(i):
 f=START
 for u in OPENINGS[i].split():f=apply(f,u)
 return f
def terminal(f,hist):
 ms=moves(f)
 if not ms:
  p=position(f);return ('0-1'if p[1]==1 else'1-0')if NEW.attack(p[0],p[0].index(6*p[1]),-p[1])else'1/2-1/2'
 if hist[' '.join(f.split()[:4])]>=3 or int(f.split()[4])>=100:return'1/2-1/2'
 if not any(abs(x)not in(0,6)for x in position(f)[0]):return'1/2-1/2'
 return None
def game(arg):
 i,seconds=arg;f=opening(i%10);hist=collections.Counter([' '.join(f.split()[:4])]);record=[];times=[]
 while len(record)<300:
  new=(i<10)==(f.split()[1]=='w');mod=NEW if new else R7;legal=moves(f);t=time.monotonic()
  if new:u=mod.choose(f,list(legal))
  else:
   mod.T=60000
   u=mod.choose(f,list(legal))
  elapsed=time.monotonic()-t;times.append(elapsed)
  if elapsed>=10:return {'game':i+1,'result':'timeout','score':0,'max_time':elapsed,'moves':record}
  if u not in legal:return {'game':i+1,'result':'illegal','score':0,'max_time':elapsed,'moves':record}
  f=apply(f,u);hist[' '.join(f.split()[:4])]+=1;record.append(u);result=terminal(f,hist)
  if result:
   score=1 if result=='1/2-1/2'else int((result=='1-0')==(i<10))
   return {'game':i+1,'new_white':i<10,'result':result,'score':score,'plies':len(record),'max_time':round(max(times),3),'moves':record,'opening':opening(i%10)}
 return {'game':i+1,'result':'adjudicated draw','score':.5,'plies':len(record),'max_time':round(max(times),3),'moves':record}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=20);ap.add_argument('--seconds',type=float,default=7.5);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args();results=[]
 with concurrent.futures.ProcessPoolExecutor(a.jobs)as pool:
  for r in pool.map(game,[(i,a.seconds)for i in range(a.games)]):results.append(r);print(json.dumps(r),flush=True)
 print('NEW SCORE',sum(r['score']for r in results),'/',len(results),'max time',max(r['max_time']for r in results));json.dump(results,open('tools/match-results.json','w'),indent=2)
if __name__=='__main__':main()
