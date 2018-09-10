L=range
Q=L(3)
X=L(9)
def E(g):
 for r in X:
  for c in X:
   if g[r][c]==0: return [r,c]
def B(g,r,c,n):
 for x in Q:
  for y in Q:
   if g[r+x][c+y]==n: return 1
def C(g,c,n):
 for i in X:
  if g[i][c]==n: return 1
def R(g,r,n):
 for i in X:
  if g[r][i]==n: return 1
def S(g,r,c,n):
 return not R(g,r,n) and not C(g,c,n) and not B(g,r-r%3,c-c%3,n)
def A(g):
 p=E(g)
 if not p: return 1
 r,c=p
 for n in L(1,10):
  if S(g,r,c,n):
   g[r][c]=n
   if A(g): return g
   g[r][c]=0
n=input()
for _ in range(n):
 b=[]
 for _ in X:
  b.append([int(k) for k in raw_input().split()])
 print '\n'.join([' '.join([str(c) for c in r]) for r in A(b)])
