""" A... Sequence.py: convenience classes for OEIS sequences
"""

class Sequence(dict):
  """Base class for integer sequences. Typical usage:
  a = Sequence() creates an instance of the sequence;
  then: `for x in a: ...`  or  a(n) == a[n]  or  a[start:stop[:step]].
  and:  `x in a` : checks whether x is a term (considering limits if given).
  Sequence(n) returns just the n-th term (using the class attributes)  
  Possibly: Sequence(upto = limit) ; Sequence(first = number_of_terms) ; 
  Sequence(start, stop, step) : generator form of a[start:stop:step] (= list)
  
  If memoization or some "state info" is required, 
  the instances can be at a different state than the class.
  
  By default (which can be overridden in subclasses):
  * Sequence() gives a sequence object
  * Sequence(n) = Sequence()[n] = Sequence()(n): the n-th term
  * Sequence(terms) = Sequence(terms = terms)
                    = Sequence(*terms) if no ambiguity can arise (len(terms)>1 or 2)
  Standard attributes (and kwargs) are:
  terms: list of already computed terms (if this is relevant)
  Standard ddunder methods:
  __len__: number of "existing" (already computed or max.possible) terms
  __getitem__: the n-th term, or a slice [start:stop:step]
  __contains__: implements 'x in self' = characteristic function.
  """
  offset = 1; "Index of first term. Subclasses should redefine this."
  terms = []; "Precomputed terms, if any."
  
  def __new__(cls, *args, **kwargs) -> int | object :
    """Return a single term (if args = just one integer) or a Sequence object 'a',
    which can be iterated over, or indexed (to get a term or a slice) or called:
    a(n) == a[n];  also:  `x in a`  or  `x in Sequence()`  to check whether x is a term.
    """
    a = super().__new__(cls); kwargs and a.update(**kwargs)
    return a(n) if len(args)==a.dim and all(isinstance(args[0], list[int]) else a
    
  def __getattr__(self, key, default=None):
      # allows to access elements of the dict as attributes, some of which default values are provided for. 
      if key in self: return self[key]
      match key:
        case 'dim'|'dimension': return 1 # default velue
        case 'offset': return 1
        case 'memoize': return False  # if we have a method 'nth_term', don't store in 'terms' by default
        case 'return_slices_as_list': return True
        case 'terms': result = []
        case _: raise AttributeError(f"Sequence has no attribute {key!r}.")
      self[key] = result  # if in the above cases, the result isn't 'return'ed ("drop-through")
      return result       # it is stored so that it can be accessed directly next time

  def __call__(self, index:int): 
    """Return a single term a(n). To get the result, the following is tried, in order:
    * If the list (of precomputed) a.terms has enough elements, return that.
      (To clarify: What if index < offset?  negative index = count from end of precomputed terms?)
    * If the sequence has a method '.nth-term()', call this 
      (It's up to that method to store in terms if expensive. TODO: provide option 'memoize')
    * If the sequence has a method '.extend()'
    """
    try: return self.terms[index - self.offset if index >= self.offset else index] # that was easy
    except IndexError: pass # no or not enough precomputed terms
    if hasattr(self,'nth_term'):
      result = self.nth_term(index)  # also easy
      if self.memoize: # append to terms if just that element was missing, otherwise store in dict
        if len(self.terms) == index - self.offset: self.terms.append(result)
        else: self[index] = result
      return result
    try: # try to extend the sequence using the .extend() method (if it exists)
          while index >= self.offset + len(self.terms) or -index > len(self.terms): self.extend()
          return self.terms[index - self.offset if index >= self.offset else index]
    except AttributeError: # i.e.: not hasattr(self, 'extend'):
    except StopIteration: # Seq. can't be extended far enough
          raise IndexError(f"Sequence {index = !r} out of range.")
          ...
    
  def __getitem__(self, index: int|slice) -> (int | list[int]):
    if isinstance(index, slice):
      subseq = (self(n) for n in range(*index.indices(len(cls))))
      return list(subseq) if self.return_slices_as_list else subseq
    elif not isinstance(index, int):
      raise IndexError(f"Can't interpret {index = !r} as index.")
    else:
      try: return terms[index - cls.offset if index >= 0 else index] # that was easy
      except IndexError:
        if hasattr(cls,'nth_term'): return cls.nth_term(index) # also easy
        try:
          while index >= cls.offset + len(self.terms) or -index > len(self.terms): cls.extend()
          return terms[index - cls.offset if index >= 0 else index]
        except StopIteration: # Seq. can't be extended far enough
          raise IndexError(f"Sequence {index = !r} out of range.")
        except AttributeError: # i.e.: not hasattr(cls,'extend'):
          ...
        
      if 0 <= index - cls.offset < len(terms): return t
    el
  pos, N, terms, grid, neighbors = 0, 1, [1], {0: 1}, (1, 1+1j, 1j, 1j-1, -1, -1-1j, -1j, 1-1j)
  def __str__(self):
    X = sorted({z.real for z in self.grid})
    return "\n".join("".join(f"{self.grid.get(x+y*1j,'')!s:5}" for x in X)
                     for y in sorted({z.imag for z in self.grid}, reverse=1))
  def __new__(cls, n=None) -> int:
    "Return n-th term or the sequence object if no n is given."
    return super().__new__(cls) if n is None else cls.nth_term(n)
  @classmethod
  def __getitem__(self, n): # TODO: implement slices
    any((len(cls.terms)>n or cls.extend()) for _ in range(n)); return cls.terms[n]
  ''' actually, __iter__ isn't needed when we have __getitem__ !
  def __iter__(self, start = 0, stop = None, step = 1):
    while stop is None or start < stop: yield self.nth_term(start); start += step
  '''
  @classmethod
  def extend(cls):
    free_neighbors = [N for d in cls.neighbors if not cls.grid.get(N := cls.pos + d)];
    # find where to start: absolute value of difference of positions is > 1 iff there's a hole
    holes = (i+1 for i,(z,w) in enumerate(zip(free_neighbors[1:], free_neighbors)) if abs(z-w) > 1)
    if h := next(holes, 0):
      if next(holes, 0): print("WARNING: multiple holes") # never occurred so far. Can it occur? Proof?
      # there's at least 1 hole, not at the beginning of the "free neighbor's list".
      # "rotate" the list of free cells to start after the first occupied neighbor cell 
      free_neighbors = free_neighbors[h:] + free_neighbors[:h]
    for n in free_neighbors: cls.N += 1; cls.grid[n] = cls.N  # fill in the numbers
    cls.pos = n # free_neighbors[-1]   # update position
    cls.terms.append(cls.N)
    # NB : this method should not return anything! (its use in any() assumes it returns None or falsy)
