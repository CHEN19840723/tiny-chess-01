"""HTTP mock of MAKEFUN_ENV_URL; validates packed main.py /game + /move."""
import http.server,json,subprocess,os,threading,time
from harness import START,moves,apply
class Handler(http.server.BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_POST(self):
  body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
  if self.path=='/game':
   # main.py loops back to /game after each /move; only the first /game is
   # your_move, later ones must answer done or main.py hangs forever.
   if not getattr(self.server,'served',False):
    self.server.served=True
    reply={'status':'your_move','game':'mock-1','fen':START,'legal_moves':list(moves(START))}
   else:
    reply={'status':'done','game':'mock-1','outcome':'1/2-1/2','reason':'mock end'}
  else:
   assert body['move'] in moves(START),body
   reply={'status':'done','game':'mock-1','outcome':'1/2-1/2','reason':'mock smoke','move':body['move']}
  raw=json.dumps(reply).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
env=os.environ.copy();env['MAKEFUN_ENV_URL']=f'http://127.0.0.1:{server.server_port}';env['ENGINE_TIME']='0.1'
r=subprocess.run(['python3','-P','-s','main.py'],env=env,capture_output=True,text=True,timeout=30)
print(r.stdout+r.stderr);assert r.returncode==0
open('tools/mock-env.log','w').write(r.stdout+r.stderr)
