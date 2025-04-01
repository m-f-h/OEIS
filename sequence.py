""" sequence.py
    defines classes with general properties and methods for integer sequences.

    (c) MFH, Oct. 2022 - Apr. 2025

The idea is to be able to sublass it, viz:
class Axxx(Sequence):
    # minimal adjustments.

    For any subclass or instance, at least one of the two methods:
    * __call__(self, n): #(returns the n-th term), or 
    * extend(self): #(extends self.data by at least 1 term, if possible)
    should be user provided, to define the sequence.

    Examples:
    class squares(Sequence):
        def __getitem__(self, n): return n**2

    s = squares();
    s[:20] == list(s(first=20)) = squares(first = 20)  # list the first 20 squares, 0² ... 19².
    s[-4] # gives element of index -4 among the precomputed terms, ==> 16.
    
    If the user "overloads" the function __getitem__, then that function
    will be used to get the n-th term of any instance of this class
    
    # default offset = 0 and default __getitem__ raises IndexError if n < offset,
    # but if user defines getitem for any n, then that's OK.
    
    class primes(Sequence):
        offset = 1
        data = [2, 3]  # if we don't redefine offset, the default offset = 0
        def extend(self):      # is used, so p[0] = 2, p[1] = 3, p[2] = 5, ...
            q = self.data[-1]
            for q in range(q+2, q**2, 2):
                for p in self.data[1:]:
                    if q % p == 0: break
                    if p*p >= q: self.data.append(q); return
    p = primes()
    p[5]         # prime with index
    list(primes(20))  # list the first 20 primes
    list(primes(1,20)) # primes with index 1..20: the first 19 odd primes
"""

class Sequence:
    """ Some typical uses of the sequence class:
    Sequence() => generator (unless finite, when it could be list) of the entire sequence ;
                  also allows to access all methods below; in particular:
                  a = Sequence()  ==>  a(n) = a[n] = n-th term, etc.
    Sequence(*args, *kwargs) = Sequence[*args, **kwargs]
    = Sequence.__call__(self, *args, **kwargs) = Sequence.__getitem__(self, ...):
        return either Sequence.nth_term(n) = a(n) if args = (n) 
          or args=(r,c) or 'r'/'row' *and* 'c', 'col' in kwargs
        or a subsequence (slice) or row, column, diagonal... of the sequence,
          if args = (slice()) or only 'r'/'row' *or* 'c'/'col' or 'd'/'diag' is given
    Specific methods:
    .nth_term(n) => a(n)
    .slice(start,stop,step): Sequence a(start + k*step; 0 <= k <= (stop-start)/step)
    .__contains__(n): characteristic function : truthy iff n is a term (<=> n in Sequence())
    .next(n): next larger (>= n) term of the sequence
    .prev(n): next smaller (<= n) term of the sequence
    .index(n): index of first occurrence of the term n.
    .is_set(): True if sequence is strictly increasing <=> represents a set bounded from below
    .offset: index of the first term
    
    The class provides default methods __init__, __iter__ and __next__ (for
    use as generator), __getitem__ (allows to use self[n] to get the
    term with index n), extend (extends the list of memoized terms
    self.data by at least 1 element unless no more terms exist).
"""
    # This allows to call the class and get just a term (or slice, row, column, etc):
    def __new__(cls, *args, **kwargs): # instantiate an object only if no args given:
        return cls.__call__(*args, **kwargs) if args else super().__new__(cls)

    offset = 1   # Warning: subclasses should redefine these default variables as *class variables*,
    terms=[]     # not only in __init__(), otherwise they'd be *shared* by all subclasses/instances,
                 # i.e., if an instance adds terms to cls.data,
                 # all subsequent instances of subclasses would have these terms.
    def __str__(S):
        s = f"{type(S).__name__}(terms={S.terms}, offset={S.offset},"
        if S.extend.__code__ == Sequence.extend.__code__:
            s += f" extend={S.extend},"
        if S.__getitem__.__code__ == Sequence.__getitem__.__code__:
            s += f" getitem={S.__getitem__},"
        return s + f" digits={S.digits})"

    def __init__(self, *args, **kwargs):
        """Positional args may be:
        * data: list (initial terms).
        * start: int (index of first term produced by __next__)
        * end: int (index of last term produced by __next__)
        Supported special keyword args:
        offset: index of first element (also, first element stored in self.data)
        start: (default: offset) index of first term to be produced by __next__.
        end: (default: None) index at which __next__ raises StopIteration
        data: (default: []) memoized initial terms of the sequence.
        """
        # check whether data and/or offset were provided as class variables,
        # or else set the default values, just for this instance
        # (both can be overridden by kwargs)
        self.data = getattr(self, 'data', [])
        self.offset = getattr(self, 'offset', 0)
        # If only 1 arg is given, it is taken to be the first among (end, start)
        # not in kwargs
        start = end = None # to know whether "we" have set the respective arg
        for arg in args:
            if isinstance(arg, list) and 'data' not in kwargs:
                kwargs['data'] = arg; continue
            if isinstance(arg, int):
                if end is None and 'end' not in kwargs: end = arg; continue
                if start is None and 'start' not in kwargs:
                    if end is None: start = arg
                    else: start, end = end, arg
                    continue
            raise TypeError(f"Don't know how to interpret argument '{arg}'.")
        if start is not None: kwargs . update ( start = start )
        if end is not None:   kwargs . update ( end = end )        
        # recall: '|' syntax introduced in 3.9, not yet available in colab
        self.__dict__ . update ( kwargs )
        
    def __getitem__(self, n):
        """Method to compute the term with index n.
        By default (if this is not overloaded), this calls extend() while 
        self.data is not long enough, and then returns self.data[n]."""
        if n < self.offset: raise IndexError
        while len(self.data) + self.offset <= n:
            self.extend()
        return self.data[n - self.offset]
    def __iter__(self):
        self.index = getattr(self, 'start', self.offset)
        return self
    def __next__(self):
        if self.index < getattr(self, 'end', self.index):
            self.index += 1
            return self[self.index-1]
        raise StopIteration
    def extend(self):
        """Method to append a new term to the stored list self.data,
        to be provided by the user if __getitem__ is not provided.
        Not used unless memoization is desired.
        Set any of data, memoize or memoization to False to avoid this."""
        if all(getattr(self,attr,1)!=False for attr in('data','memoize','memoization')):
           self.data.append(self[self.offset + len(self.data)])


class primes(Sequence):
    data = [2, 3]; offset = 1
    def extend(self):
        q = self.data[-1]
        if getattr(self, 'debug', 0): print("computing next prime after", q)
        for q in range(q+2, q**2, 2):
            for p in self.data[1:]:
                if q % p == 0: break
                if p*p >= q: self.data.append(q); return

class squares(Sequence):
    def __getitem__(self, n): return n**2

if __name__ == '__main__1':
    p = primes()
    print("primes[5] =",p[5])
    print( list( primes(2, 25))) # odd primes: prime(2 .. 24) 
    print( list( squares( 10 ))) # squares 0² .. 9²


class Table(Sequence):
    """A class for tabf/tabl sequences.
    Subclass of Sequence that supports additional keyword arguments and provides additional methods & properties:
    .col(c) => Sequence given by column with index c
    .row(r) => Sequence given by row with index r
    .diag(k) => Sequence given by diagonal with index k
                (k=0 = main diagonal, k>0: upper/right diagonals, k<0: lower/left diagonals)
    .element(r,c) => element in row r, column c, for a tabf/tabl sequence
                  (possibly also with kw row and/or column;
                  should yield a generator if one of the two is omitted)
"""
    ... #TODO...


class Candidates():
    """Provides an iterator producing (a priori) unique, increasing candidates.
    User may get / set any of the attributes min, max, used, ok(), increment().
    See doc for the respective attibute/method, or __init__ for min, max, used.
    """
    def __str__(self): return f"{type(self).__name__}(min={self.min}, "\
        f"max={getattr(self,'max',None)}, used={self.used})"
    def __init__(self, **kwargs):
        """Possible kwargs (and thereafter attributes that can be read & set):
        * min: int = 0: smallest available candidate; incremented when used.
        * max: int = None: upper limit; when set & reached => StopIteration.
        * used = set(): set of no more available terms > min
        * ok, use, increment: see help(...)
        """
        self.min = 0; self.used = set(); self.__dict__.update(kwargs)
    def increment(self, k):
        """Return the next larger candidate that comes next after k.
        To define a different increment() method, 4 ways:
        1)  class MyCandid(Candidates):       # define you own subclass
                def increment(self, k): ...   # define the method there
        2)  cand = Candidates( increment = lambda k: ...) # can't access self
        3)  cand = Candidates(); cand.increment = lambda k: ... # as above
        4)  import types ; def my_increment(self, k): ...
            cand.increment = types.MethodType(my_increment, cand)
        """
        return k+1
    def ok(self, k):
        """Check whether k is a valid candidate and should be yielded, or not.
        By default this only checks whether k is not in self.used.
        If other checks are to be done, it's up to you to decide whether it's
        more efficient to test those before or after this check.
        """
        return k not in self.used
    def __iter__(self):
        k = self.min; M = getattr(self, 'max', None)
        while not M or k < M:
            if self.ok(k): yield k
            k = self.increment(k)
    def use(self, k):
        """Declare the candidate k as no more available: If > self.min,
            k is added to self.used; if ==, then self.min is incremented."""
        if k == self.min:
            self.min = k = self.increment(k)
            self.used.difference_update(x for x in self.used if x < k)
        elif k > self.min: self.used.add(k)
        # shouldn't happen, but if k < min, do nothing.
# end class Candidates

#primes.debug=1
if __name__ == '__main__':
    print("Test: Candidates")
    from types import MethodType
    #cand = Candidates(); #cand.increment = lambda s,k: k+2
    cand = Candidates(increment = lambda k: k+2)
    #cand = Candidates()
    #def inc(k): return k+2
    #cand
    cand.max = 25
    print(list(cand))
