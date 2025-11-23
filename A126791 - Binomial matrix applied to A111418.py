"""
Mathar's Maple code:

A126791 := proc(n, k)
    if n=0 and k = 0 then        1 ;
    elif k <0 or k>n then        0;
    elif k= 0 then        4*procname(n-1, 0)+procname(n-1, 1) ;
    else        procname(n-1, k-1)+3*procname(n-1, k)+procname(n-1, k+1) ;
    end if;
end proc:
def A126791(n, k):
    if n==0 and k==0: return 1
    if k<0 or k>n: return        0;
    elif k= 0 then        4*procname(n-1, 0)+procname(n-1, 1) ;
    else        procname(n-1, k-1)+3*procname(n-1, k)+procname(n-1, k+1) ;
def A126791(n, k):
    return int(k==0 or k==n) if  k <= 0 or k >= n else (
      A126791(n-1, k-1)+3*A126791(n-1, k) if k else 4*A126791(n-1, 0))+A126791(n-1, k+1)
"""
def A126791(n, k):
    return (A126791(n-1, k-1)+3*A126791(n-1, k) if k else 4*A126791(n-1, 0)
        )+A126791(n-1, k+1)  if 0 <= k < n else int(k == n)

if "test":
  for n in range(N:=9):
    print([A126791(n, k) for k in range(N)])
