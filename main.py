import json,os,sys,urllib.error,urllib.request
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit(1)
V={"p":10,"n":30,"b":30,"r":50,"q":90,"k":900}

def post(t,b):
 r=urllib.request.Request(E+t,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:return json.load(urllib.request.urlopen(r))
 except urllib.error.HTTPError as e:sys.exit(f"{t}: HTTP {e.code}")

def board_of(fen):
 b={}
 for i,row in enumerate(fen.split()[0].split("/")):
  f=0
  for c in row:
   if c.isdigit():f+=int(c)
   else:b["abcdefgh"[f]+str(8-i)]=c;f+=1
 return b

def eval_board(b):
 v=0
 for s,p in b.items():
  sgn=1 if p.isupper()else-1
  v+=sgn*V[p.lower()]
  # Add small positional bonus for center control
  cx,cy=ord(s[0])-97,8-int(s[1])
  if 2<=cx<=5 and 2<=cy<=5:v+=sgn*1
 return v

def choose(fen,legal):
 board=board_of(fen)
 best=legal[0]
 best_v=-99999
 # Try top 20 moves with 1-ply lookahead
 for m in legal[:20]:
  b2=board.copy()
  b2[m[2:4]]=b2[m[:2]]
  del b2[m[:2]]
  v=eval_board(b2)
  if v>best_v or(v==best_v and m<best):
   best_v=v
   best=m
 return best

while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
