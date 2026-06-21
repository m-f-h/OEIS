""" from_GF.py - (c) 2026 by MFH
"""
import functools # for 'update_wrapper' which "preserves metadata" (docstring, name)

def indexable(f): # decorator allowing to use a[0:5] for [a(k)for k in range(0,5)]
    class Wrapper:
        def __call__(self, x): return f(x)
        def __getitem__(self, key): 
          return [f(i) for i in range(key.start or 0, key.stop, key.step or 1)
                  ] if isinstance(key, slice) else f(key)
    w = Wrapper(); functools.update_wrapper(w, f)
    return w

from typing import Callable
from numbers import Number
from fractions import Fraction
# "poor man's" versions:
for n,d in {'Polynomial': list, 'Callable':type(lambda:0), 'Number':float|int}.items():
  try: eval(n) # if type isn't known, define it as some default
  except NameError: globals()['d'] = d

def from_GF(P: Polynomial, Q: Polynomial) -> Callable:
    """
    Return a memoized function `a(n)` that gives the n-th term of the
    sequence defined by the ordinary rational generating function P(x) / Q(x).
    a(n) will be of type int as long as possible, then Fraction if possible,
    or else `float` (as soon as a float enters the calculation).
    Args:
        P: numerator polynomial, given as list s.t. P(x) = Sum P[i]*x^i.
        Q: denominator polynomial, given as list s.t. Q(x) = Sum Q[i]*x^i.
           The constant term Q[0] must not be zero, else raise ValueError.
    """
    if not(Q and Q[0]):
        raise ValueError("The constant term of the denominator polynomial cannot be zero.")
    len_P = len(P); len_Q = len(Q); terms = []  # To store computed terms: terms[k] = a_k
    integers = isinstance(Q[0], int) # while this is true, try to compute in integers or fractions

    def a(n: int) -> Number:
        nonlocal integers
        if n < 0: raise ValueError("n must be a non-negative integer.")
        
        # compute terms as long as the requested term is not yet available,
        while n >= len(terms):
            k = len(terms)-1 ; pk = P[k] if k < len_P else 0
            # Recurrence: a_k = (p_k - sum_{j=1 to k} (a_{k-j} * q_j)) / q_0
            pk -= sum(terms[k - j] * Q[j] for j in range(1, min(k+1, len_Q)))
            if not isinstance(pk, int): integers = False
            terms.append(pk / Q[0] if not integers else 
                Fraction(pk, Q[0]) if pk % Q[0] else pk // Q[0])
        return terms[n] # end of def a(n)
    return a # end of from_GF

""" If you need a class Polynomial to compute the numer/denom/coefficients, here's
class Pol(list): #  a minimalistic implementation
    def __repr__(P):return f"Pol({list(P)})"
    def __add__(P,Q):
      if not hasattr(Q,'__iter__'): Q=[Q]
      return type(P)([p+q for p,q in zip(P,Q )]+P[len(Q):]+Q[len(P):])
    def __mul__(P,Q): return type(P)([p*Q for p in P]if not hasattr(Q,'__iter__')
      else[sum(P[i]*Q[k-i]for i in range(max(0,k-len(Q)+1),min(len(P),k+1)))
      for k in range(len(P)+len(Q)-1)])
    __radd__=__add__ ; __rmul__=__mul__ ;
    def __pow__(P,n:int): # better use binary exponentiation
      if n<0: raise ValueError("Negative powers not implemented.")
      return P*P**(n-1)if n>1 else P if n else 1
if 1:#test
  X = Pol([0,1]);  P = Pol(2 + 5*X**2);  Q = Pol(3 + -7*X**3)
  print(f"{P = }, {Q = }, {P + Q = }, {P * Q = }, ")
""" # end class Pol

