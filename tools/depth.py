import engine,time,json
fens=['r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQKBNR w KQkq - 4 4','r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1','2rq1rk1/pp1bppbp/2np1np1/8/2BNP3/2N1BP2/PPPQ2PP/2KR3R w - - 0 1']
out=[]
for f in fens:
 engine.nodes=0;t=time.monotonic();engine.choose(f,[engine.uci(m)for m in engine.moves(engine.parse(f))]);dt=time.monotonic()-t
 out.append({'fen':f,'nodes':engine.nodes,'seconds':dt,'nps':round(engine.nodes/dt)})
print(json.dumps(out));open('tools/depth-results.json','w').write(json.dumps(out))
