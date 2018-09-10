import random
T=range(3)
X=range(9)
random.shuffle(X)
def F(g):
 for r in X:
  for c in X:
   if g[r][c]==0:
    return [r,c]
 return False
def B(g,r,c,n):
 for x in T:
  for y in T:
   if g[r+x][c+y]==n:
    return True
 return False
def C(g,c,n):
 for i in X:
  if g[i][c]==n:
   return True
 return False
def R(g,r,n):
 for i in X:
  if g[r][i]==n:
   return True
 return False
def S(g,r,c,n):
 return not R(g,r,n) and not C(g,c,n) and not B(g,r-r%3,c-c%3,n)
def A(g):
 p=F(g)
 if not p:
  return True
 r,c=p
 for n in range(1,10):
  if S(g,r,c,n):
   g[r][c]=n
   if A(g):
    return g
   g[r][c]=0
 return False
n=input()
for i in range(n):
 b=[]
 for _ in X:
  b.append([int(k) for k in raw_input().split()])
 print '\n'.join([' '.join([str(c) for c in r]) for r in A(b)])
