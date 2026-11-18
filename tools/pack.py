import lzma
s=open('engine.py','rb').read();raw=lzma.compress(s,format=lzma.FORMAT_ALONE,preset=9|lzma.PRESET_EXTREME)
def esc(x):return {0:'\\000',7:'\\a',8:'\\b',9:'\\t',10:'\\n',11:'\\v',12:'\\f',13:'\\r',39:"\\'",92:'\\\\'}.get(x,chr(x))
text="#coding:l1\nimport lzma;exec(lzma.decompress('"+''.join(map(esc,raw))+"'.encode('l1')))\n"
open('main.py','w',encoding='l1',newline='').write(text)
print(len(text.encode('l1')),len(s),len(raw))
