# composite numbers

next_A002808=lambda n: next(n for n in range(n, n*5)if not isprime(n)) # next composite >= n > 0; next_A002808(n)==n <=> iscomposite(n). - M. F. Hasler, Mar 28 2025

is_A002808=lambda n:not isprime(n) and n>1 # where isprime(n) can be replaced with: any(n%d==0 for d in range(2, int(n**.5)+1))

# generators of composite numbers:

A002808_upto=lambda stop=1<<59: filter(is_A002808, range(2, stop))

A002808_seq=lambda:(q:=2)and(n for p in primes if (o:=q)<(q:=p) for n in range(o+1, p)) # with, e.g.: primes=filter(isprime, range(2, 1<<59)) # M. F. Hasler, Mar 28 2025
