''' A377090.py - Feb 2025 by MFH

Same as A377091 with primes instead of squares.
'''
from sympy import isprime

# version 0: the simplest would be to use "optional keyword arguments" for static variables
def A377090(n, terms = [0]):    # A377090.N = least unused candidate
    while len(terms) <= n:
        while (k := getattr(A377090,'N',1)) in terms: A377090.N = (k<0)-k
        while not isprime(abs(k - terms[-1])) or k in terms: k = (k<0)-k
        terms.append(k)
    return terms[n] # _M. F. Hasler_, Feb 10 2025

# But this becomes ugly when 'terms' becomes very large, because most Python
# interfaces show the value of 'terms' when a user types " A377090( ".

# version 1
def A377090(n):    # A377090.N = least unused candidate
    if not getattr(A := A377090, 'N', 0):  A.N = 1; A.terms = [0]
    while len(A.terms) <= n:
        while (k := A.N) in A.terms: A.N = (k<0)-k
        while not isprime(abs(k - A.terms[-1])) or k in A.terms: k = (k<0)-k
        A.terms.append(k)
    return A.terms[n] # _M. F. Hasler_, Feb 10 2025

# it may be considered elegant to "hide" all technicalities inside the function,
# but this way there is the "getattr" call at each call of the function...
# maybe better "hard-wire" this? see next version.

# version 1-b
def A377090(n):   
    while len(terms := A377090.terms) <= n:
        while (k := A377090.N) in terms: A377090.N = (k<0)-k
        while not isprime(abs(k - terms[-1])) or k in terms: k = (k<0)-k
        terms.append(k)
    return terms[n] # _M. F. Hasler_, Feb 10 2025
A377090.terms = [0]; A377090.N = 1 # least unused candidate.  # initialization.

# Now we could implement additional functionality:
# for example:
# * A377090() - generator of the entire (infinite) sequence
# * A377090(n) - return the n-th element
# * A377090(start, stop [, step]) - return [generator or sequence?] of sequence from start to stop [by step ?]

# version 3
def A377090(n = None, stop = None):
    if n is None or stop is not None: return(A377090(n) for n in range(n or 0, stop or 2**63))
    while len(terms := A377090.terms) <= n:
        while (k := A377090.N) in terms: A377090.N = (k<0)-k
        while not isprime(abs(k - terms[-1])) or k in terms: k = (k<0)-k
        terms.append(k)
    return terms[n] # _M. F. Hasler_, Feb 10 2025
A377090.terms = [0]; A377090.N = 1 # least unused candidate.  # initialization.


# version 2. The class structure is mainly used to hide the terms and 'N' inside 
class A377090: # A377090(n) gives a(n)
    def __new__(A, n):  # or use __class_getitem__ to allow slices A377090[a:b:c]
        while len(A.terms) <= n: # if type(n)==int else max(n.start or 0, ...)
            while (k := A.N) in A.terms: A.N = (k<0)-k
            while not isprime(abs(k-A.terms[-1])) or k in A.terms: k = (k<0)-k
            A.terms.append(k)
        return A.terms[n] # _M. F. Hasler_, Feb 10 2025
    terms = [0]; N = 1 # least unused candidate

# version 2-b: use __class_getitem__ to allow slices A377090[a:b:c]
class A377090:
    "A377090(n) and A377090[n] gives a(n); A377090[slice] gives a slice (a(k); k in range(*slice.indices))."
    def __class_getitem__(A, n = None):
        if type(n)==int: return A377090(n)
        if n is None: return(A377090(n)for n in range(1<<63)) # quasi-infinite generator
        if type(n)==type: return ... # GenericAlias
        if type(n)!=slice: raise ValueError(f"Expected index, slice, type or None, got '{n}'")
        # return generator for the requested slice;
        # in case of negative ending index or step, use len(already computed terms)
        return(A377090(n)for n in range(*n.indices(n.stop if(n.stop or 0)>0<=(n.step or 0)else len(A.terms))))
    def __new__(A, n): # compute enough terms (if necessary) and return terms[n] 
        while len(A.terms) <= n:
            while (k := A.N) in A.terms: A.N = (k<0)-k
            while not isprime(abs(k-A.terms[-1])) or k in A.terms: k = (k<0)-k
            A.terms.append(k)
        return A.terms[n] # _M. F. Hasler_, Feb 10 2025
    terms = [0]; N = 1 # least unused candidate



