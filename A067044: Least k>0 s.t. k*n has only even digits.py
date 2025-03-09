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
  if all(int(d)%2==0 for d in str(n)): return 1 # all digits even
  if all(d < '5' for d in str(n)): return 2    # all digits < 5

  # "simple" multiple of 10^k-1 ?
  if n%9==0 and (k := len(str(n//9))) and (m := n / (10**k-1)).is_integer():
    R = 8*round(10**k/6)**2
    match m:
      case 1 | 2 | 4 | 8: return R/m
      case 5: return 2*R
    #raise ValueError(f"Not yet implemented: {n} / 9 = {n/9} not a repdigit, m = {m}.")

  # odd multiples of 5 :  n = (2k-1)*5
  if n%5 == 0 and n//5 & 1:
    #  k == 1 or 2 (mod 5)  and   k//5 has only digits <5 ### testes and confirmed
    if (k := (n//5+1)//2) % 5 in (1,2) and all(d < '5' for d in str( k//5 )): return 4
    if k % 5 in (3,4): return 8 ### NOT ALWAYS TRUE
    raise ValueError(f"Not yet implemented: odd multiple of 5, n = 5*{n/5}.")
  raise ValueError(f"Not yet implemented: {n}.")

def test_formula( n_values, count = 1 ):
  for n in n_values:
      assert A67044(n)==A067044(n), f"For n = {n}, formula gives {A67044(n)} instead of {A067044(n)}"
      if count: count += 1; largest=n
  if count: print(f"OK - Tested {count-1} cases, up to n = {n}.")
    
if k_max := 3*0 : # OK up to 3
  "check formula for m*(10^k-1) with m=1,2,4,8 or 5."
  test_formula( m*(10**k-1) for k in range(1, k_max+1) for m in (1,2,4,5,8) )

if m_max := 200*0 : ## OK up to 200
  print(
  "check formula for n = 5*(2k-1) with k = 5m+{1 or 2}, m having digits < 5.")
  test_formula( 5*(2*k-1) for m in range(m_max) if all(d<'4' for d in str(m)) 
                for k in (5*m+1, 5*m+2) ) # OK

if m_max := 200:
  print(
  "test formula for n = 5*(2k-1) with k = 5m+{3 or 4}, m having digits < 5.")
  test_formula( 5*(2*k-1) for m in range(m_max) if all(d<'4' for d in str(m)) 
                for k in (5*m+3,5*m+4)) ## if k%10 ) ## (5*m+1, 5*m+2)):
  # yields error for 125 = 5 * 25 = 5*(2k-1) with k=13

if 'make_odd5': #__name__=='__main__':
  print("Make dictionary of results a(5(2k-1)) and corresponding k-values.")
  D={} # dict. of k-values per result
  for k in range(1,999): r=A067044(5*(2*k-1)); D[r].append(k)if r in D else D.update({r:[k]})
  # print(sorted(D)) # all keys: 4, 8, 12, 16, 24, 28, 32, 36, 44, 48, 52, 56, 64, ...
  # ... 512, 524, 536, 548, 624, 648, 668, 692, 744, 776, 784, 872, 888, 944, 952, 1128, 1676, 2032, 3352, 4464, 4624, 9248, 446224]

  # It seems these are all multiples of 4 not multiple of 5, up to 252 (which is the first missing one):
  assert set(x for x in D if x < 252)=={m for m in range(4,252,4) if m%5}
  
  print("Values of k%5 for a(n)=4:",set(k%5 for k in D[4])) # = {1,2} -- formula covers them all

  print("Values of k%5 for a(n)=8:",set(k%5 for k in D[8])) # = {1,3,4} -- to do...
  

