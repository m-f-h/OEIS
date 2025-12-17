---
title: super-d numbers :  d*n^d contains 'd...d'
---
* oeis.org/A032743: super-2 numbers
* oeis.org/A014569: super-3 numbers
* oeis.org/A032744: super-4 numbers
* ...
* oeis.org/A032749: super-9 numbers

Giovanni Resta, <a href="https://www.numbersaplenty.com/set/super-d_number/">super-d numbers</a>, personal web site "Numbers Aplenty", 2013

### PROG	
#### (PARI)
```PARI/GP
select( {is_A032743(n, d=2, m=10^d, r=m\9*d)=n=d*n^d; until(r>n\=10, n%m==r && return(1))}, [0..999]) \\ _M. F. Hasler_, Jul 16 2024
```
#### (Python)
```Python
is_A032743=lambda n, d=2: str(d)*d in str(d*n**d) # _M. F. Hasler_, Jul 16 2024
```
