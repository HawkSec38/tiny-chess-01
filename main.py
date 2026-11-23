import json,os,sys,urllib.error,urllib.request
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit(1)
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
A="abcdefgh"

def p(t,b):
 r=urllib.request.Request(E+t,data=json.dumps(b).encode(),headers={"ct":"application/json"})
 try:return json.load(urllib.request.urlopen(r))
 except:return{}

def B(f):
 b={}
 for i,r in enumerate(f.split()[0].split("/")):
  f2=0
  for c in r:
   if c.isdigit():f2+=int(c)
   else:b[A[f2]+str(8-i)]=c;f2+=1
 return b

def Eval(b):
 v=0
 for s,p in b.items():
  sgn=1 if p.isupper()else-1
  v+=sgn*V[p.lower()]
  x,y=ord(s[0])-97,8-int(s[1])
  if 2<=x<=5 and 2<=y<=5:v+=sgn*5
 return v

def order(b,l):
 ms=[]
 for m in l:
  b2=b.copy()
  b2[m[2:4]]=b[m[:2]]
  del b2[m[:2]]
  ms.append((Eval(b2),m))
 return sorted(ms,reverse=True)

def ab(b,l,d,a,ba,mo):
 if d==0:return Eval(b)
 for v,m in mo:
  b2=b.copy()
  b2[m[2:4]]=b[m[:2]]
  del b2[m[:2]]
  s=-ab(b2,[x for x in l if x!=m],d-1,-a,-ba,order(b2,[x for x in l if x!=m]))
  if s>a:a=s;ba=m
  if a>=ba:break
 return a

def C(f,l):
 b=B(f)
 mo=order(b,l)
 best=mo[0][1]
 best_v=-999999
 for v,m in mo[:8]:
  b2=b.copy()
  b2[m[2:4]]=b[m[:2]]
  del b2[m[:2]]
  s=ab(b2,[x for x in l if x!=m],2,-999999,best_v,order(b2,[x for x in l if x!=m]))
  if s>best_v:best_v=s;best=m
 return best

while 1:
 g=p("/game",{})
 if g.get("status")=="done":break
 while g.get("status")=="your_move":
  g=p("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})
