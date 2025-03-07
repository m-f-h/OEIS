"""
A067044.py
Smallest positive k such that k*n contains only even digits.

FORMULA:
a(n) = 1 if n has only even digits, else, a(n) = 2 if n has only digits < 5;
a(m*(10^k-1)) = 8*round(10^k/6)^2/m for m = 1, 2, 4 or 8 and any k > 0;
a(5*(10^k-1)) = 16*round(10^k/6)^2 for any k > 0. (End)

PROGRAM:
(PARI)
apply( {A067044(n, f=1+n%2)=forstep(a=f*n, oo, f*n, digits(a)%2||return(a/n))}, [1..99]) \\ M. F. Hasler, Mar 03 2025
(Python) 
"""
A067044 = lambda n: next(k for k in range(1+n%2, 9<<99, 1+n%2)if not any(int(d)&1 for d in str(n*k))) # M. F. Hasler, Mar 03 2025

def A67044(n): # implementing the FORMULA
  if all(int(d)%2==0 for d in str(n)): return 1
  if all(int(d)<5 for d in str(n)): return 2
  if n%9: raise ValueError(f"Not yet implemented: {n} not in 9Z")
  k = len(str(n//9)); m = n / (10**k-1)
  R = 8*round(10**k/6)**2
  match m:
    case 1 | 2 | 4 | 8: return R/m
    case 5: return 2*R
  raise ValueError(f"Not yet implemented: {n} / 9 = {n/9} not a repdigit, m = {m}.")

for n in (m*(10**k-1) for k in range(3+1) for m in (1,2,4,5,8)):
    assert A67044(n)==A067044(n)
  
