import json,os,sys,urllib.error,urllib.request
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL not set")
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

def evaluate(board):
 v=0
 for sq,p in board.items():
  sign=1 if p.isupper()else-1
  v+=sign*V[p.lower()]
 return v

def choose(fen,legal):
 board=board_of(fen)
 best_move=legal[0]
 best_score=-99999
 for move in legal:
  board2=board.copy()
  from_sq,to_sq=move[:2],move[2:4]
  board2[to_sq]=board[from_sq]
  del board2[from_sq]
  score=evaluate(board2)
  if score>best_score or(score==best_score and move<best_move):
   best_score=score
   best_move=move
 return best_move

while True:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
