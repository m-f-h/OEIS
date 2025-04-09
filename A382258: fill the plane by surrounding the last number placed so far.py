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
  pos, N, terms, grid, neighbors = 0, 1, [1], {0: 1}, (1, 1+1j, 1j, 1j-1, -1, -1-1j, -1j, 1-1j)
  def __str__(self):
    X = sorted({z.real for z in self.grid})
    return "\n".join("".join(f"{self.grid.get(x+y*1j,'')!s:5}" for x in X)
                     for y in sorted({z.imag for z in self.grid}, reverse=1))
  def __new__(cls, n=None) -> int:
    "Return n-th term or the sequence object if no n is given."
    return super().__new__(cls) if n is None else cls.nth_term(n)
  @classmethod
  def nth_term(cls, n): any((len(cls.terms)>n or cls.extend()) for _ in range(n)); return cls.terms[n]
  def __iter__(self, start = 0, stop = None, step = 1):
    while stop is None or start < stop: yield self.nth_term(start); start += step
  def __getitem__(self, n): return self.nth_term(n) # TODO: implement slices
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
