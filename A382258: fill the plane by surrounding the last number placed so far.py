"""
A382258(n) = last number placed on an infinite square grid at the n-th step,
  in order to completely surround the last number placed at the previous step,
  always using the next larger integer and going counter-clockwise, starting with a 1 at the origin.,

A382259(n) = number of squares filled at the n-th step (= first differences of A382258).

(PARI/gp):
neighbors=[1, 1+I, I, I-1, -1, -1-I, -I, 1-I]  /* using the complex plane */
M.extend={ /* Uses global vars 'pos' and 'N'. Could be stored within M... */
  #M || mapput(M, pos=0, N=1)+return(N); /* Empty grid => initialize grid[pos=0]=(N=1). */
  n = #free_neighbors = [pos+n | n<-neighbors, !mapisdefined(M,pos+n)];
  /* find where to start: absolute value of difference of positions is > 1 iff there's a hole */
  distances = abs(free_neighbors[^1] - free_neighbors[^-1]);
  if(1 < #start = select(d -> d>1, distances, 1)
    , print("WARNING: multiple holes") /* never occurred so far. Can it occur? Proof? */
  , #start /* there's at least 1 hole, not at the beginning of the "free neighbor's list":
              "rotate" the list of free cells to start after the first occupied neighbor cell */
    , free_neighbors=concat(free_neighbors[start[1]+1..-1], 
                            free_neighbors[1..start[1]] )
  );
  foreach(free_neighbors, n, mapput(M, n, N++)); /* fill in the numbers */
  pos=free_neighbors[n]; /* update position */ 
  /* return last number filled in */ N}

/* to display the grid: */
M.show={my(m(f)=Set(f(Vec(M))), X=m(real)); /* make sorted list of real or imag parts of the positions(= keys of the map)*/
  foreach(Vecrev(m(imag)), y, /* display row with largest y fist */
    print(strjoin([iferr(mapget(M,x+I*y),E,"") | x<-X], "\t")))} /* space the numbers out with tabs. TODO: use strprintf("%5s") or so. */

/* 3rd optional arg allows to use a global Map that can be extended further afterward */
A382258_first(n, show=1, M=Map())=vector(n, i, M.extend)+(show && M.show)

(Python)
"""
class A382258:
  pos, N, terms, grid = 0, 1, [1], {0: 1}
  neighbors = (1, 1+1j, 1j, 1j-1, -1, -1-1j, -1j, 1-1j)
   
  def __str__(self):
    X = sorted({z.real for z in self.grid})
    return "\n".join("".join(f"{self.grid.get(x+y*1j,'')!s:5}" for x in X)
                     for y in sorted({z.imag for z in self.grid}, reverse=1))
     
  def __new__(cls, *args, **kwargs) -> int|object:
    """Return n-th term or the sequence object if no n is given.
    TODO: Implement stop=... (and/or first=..., upto=...), 
    maybe also start=..., step=... through slice)."""
    a = super().__new__(cls)
    a.__dict__ |= kwargs
    return a if not args else a[args]

  def __call__(self, n):
    "Return a(n)."
    while len(self.terms) <= n: self.extend()
    return self.terms[n]
     
  def __getitem__(self, n): 
    if isinstance(n, int): return self(n)
    raise NotImplementedError("Slices and indices other than integers not yet implemented.") # TODO
     
  def extend(self):
    free_neighbors = [N for d in self.neighbors if not self.grid.get(N := self.pos + d)];
    # find where to start: absolute value of difference of positions is > 1 iff there's a hole
    holes = (i+1 for i,(z,w) in enumerate(zip(free_neighbors[1:], free_neighbors)) if abs(z-w) > 1)
    if h := next(holes, 0):
      if next(holes, 0): print("WARNING: multiple holes") # never occurred so far. Can it occur? Proof?
      # there's at least 1 hole, not at the beginning of the "free neighbor's list".
      # "rotate" the list of free cells to start after the first occupied neighbor cell 
      free_neighbors = free_neighbors[h:] + free_neighbors[:h]
    for n in free_neighbors: self.N += 1; self.grid[n] = self.N  # fill in the numbers
    self.pos = n # free_neighbors[-1]   # update position
    self.terms.append(self.N)
    # NB : this method must not return anything! (its use in any() assumes it returns None or falsy)
