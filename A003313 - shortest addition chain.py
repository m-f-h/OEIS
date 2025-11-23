""" A003313.py - (c) 2025 by M.F.Hasler

A003313(1,...) = (0, 1, 2, 2, 3, 3, 4, 3, 4, 4, 5, 4, 5, 5, 5, 4, 5, 5, 6, 5, 6, 6, 6, 5, 6, 6, 6, 6, 7, 6, 7, 5, 6, 6, 7, 6, 7, 7, 7, 6, 7, 7, 7, 7, 7, 7, 8, 6, 7, 7, 7, 7, 8, 7, 8, 7, 8, 8, 8, 7, 8, 8, 8, 6, 7, 7, 8, 7, 8, 8, 9, 7, 8, 8, 8, 8, 8, 8, 9, 7, 8, 8, 8, 8, 8, 8, 9, 8, 9, 8, 9, 8, 9, 9, 9, 7, 8, 8, 8, 8, ...)
= Length of shortest addition chain for n.

An addition chain for n is a sequence s with s(0) = 1 and s(k) = s(l) + s(m) with some 0 <= l <= m < k for all k until s(k) = n. - _M. F. Hasler_, Nov 14 2025

(PARI)

"""

# first variant : store all chains of given length

def A003313(n): # A.chains has m! elements when a(n)=m
  if not hasattr(A:=A003313, 'terms'): A.terms={1:0}; A.chains={(1,)}
  while n not in A.terms: # make the set of addition chains of next possible length
    # no need for a set, we know all elements are different
    A.chains=[c+(c[-1]+s,) for c in A.chains for s in c]
    for c in A.chains:
      if c[-1] not in A.terms: A.terms[c[-1]] = len(c)-1
    """ or:
    for *c,t in A.chains:
      if t not in A.terms: A.terms[t] = len(c)
    """
  return A.terms[n] # ~~~~

# second version : generator of all chains
""" WORK IN PROGRESS ***
def chains():
    todo = [[(1,)]]
    while t := todo.pop(0):
      for c in t:
        print(end=f"processing {c}. ")
        yield c
        print(end=f"queing children of {c}. ")
        todo.append( c+(c[-1]+s,) for s in c )

def A3313(n): # A.chains has m! elements when a(n)=m
  if not hasattr(A:=A3313, 'terms'): A.terms={1:0}; A.chains={(1,)}
  while n not in A.terms: # make the set of addition chains of next possible length
    # no need for a set, we know all elements are different
    A.chains=[c+(c[-1]+s,) for c in A.chains for s in c]
    for c in A.chains:
      if c[-1] not in A.terms: A.terms[c[-1]] = len(c)-1
    """ or:
    for *c,t in A.chains:
      if t not in A.terms: A.terms[t] = len(c)
    """
  return A.terms[n] # ~~~~
"""
