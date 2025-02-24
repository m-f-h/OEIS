''' A37709x.py - Feb 2025 by MFH

A37709x: Choose unused integer with minimal |a(n) - 0.25| such that |a(n)-a(n-1)| = something:
A377090: something = prime
A377091: something = square
A377092: something = Fibonacci

See also A377090 for a simpler variant
'''
from sympy import isprime # for A377090

# version 1-b
def A377090(n = None, ok = isprime):
    """If no n is given, return generator of infinite sequence. 
    Change 'ok' for variants (ok=issquare => A377091, ok=is_A45 => A377092)."""
    if not getattr(A := A377090, 'N', 0): A.N = 1; A.terms = [0]
    while len(A.terms) <= (n or 1):
        while (k := A.N) in A.terms: A.N = (k<0)-k # update least unused
        while not ok(abs(k - A.terms[-1])) or k in A.terms: k = (k<0)-k
        A.terms.append(k)
    return A.terms[n] if n or n==0 else(A(n,ok) for n in range(1<<63))# "infinite"
    # Possible extension: optional 'stop' parameter, then use 
    # (... for n in range(n or 0, stop or 2**63))
# _M. F. Hasler_, Feb 10 2025


# Now we could implement additional functionality:
# for example:
# * A377090() - generator of the entire (infinite) sequence
# * A377090(n) - return the n-th element
# * A377090(start, stop [, step]) - return [generator or sequence?] of sequence from start to stop [by step ?]

# version 2-b: use __class_getitem__ to allow slices A377090[a:b:c]
class A377090:
    """A37709x(n) and A37709x[n] gives a(n); A377090[slice] gives a slice (a(k); k in range(*slice.indices)).
    Uses the class method/function ok(): set this to whatever you want (isprime, issquare, is_Axxx, ...)
    for the specific sequence (A377090, A377091, A377092, ...)
    """
    ok = isprime  # default: A377090
    def __class_getitem__(A, n = None): # This part can be omitted 
        if type(n)==int: return A(n)
        if n is None: return(A(n)for n in range(1<<63)) # quasi-infinite generator
        if type(n)==type: return ... # GenericAlias
        if type(n)!=slice: raise ValueError(f"Expected index, slice, type or None, got '{n}'")
        # return generator for the requested slice;
        # in case of negative ending index or step, use len(already computed terms)
        return(A(n)for n in range(*n.indices(n.stop if(n.stop or 0)>0<=(n.step or 0)else len(A.terms))))
    def __new__(A, n): # compute enough terms (if necessary) and return terms[n] 
        while len(A.terms) <= n:
            while (k := A.N) in A.terms: A.N = (k<0)-k
            while not A.ok(abs(k-A.terms[-1])) or k in A.terms: k = (k<0)-k
            A.terms.append(k)
        return A.terms[n] # _M. F. Hasler_, Feb 10 2025
    terms = [0]; N = 1 # least unused candidate

issquare = lambda n: (n**.5).is_integer() # issquare

class A377091(A377090): # note: it is essential to initialize N and terms in each subclass!
    terms=[0]; N=1; ok = issquare

A010056 = lambda n: issquare(k := 5*n**2+4) or (n>0 and issquare(k-8)) # is_A000045 (is_fibonacci)

# check: (note, the select won't put the 1 twice so we test from 1,2... onwards

assert (F1 := [k for k in range(1,50) if A010056(k)]) == (
    (F2 := [1,2]) and any(len(F2)==len(F1)or F2.append(sum(F2[-2:]))for _ in range(50)) and F2)
 
class A377092(A377090):
    terms=[0]; N=1; ok = is_A000045 # is_fibonacci

