""" Ludic numbers oeis.org/A003309 and related sequences

oeis.org/A003309: the ludic numbers (offset 1, should maybe better be 0 for initial term 1)
= (1, 2, 3, 5, 7, 11, 13, 17, 23, 25, ...)

Comment: obtained through a sieve similar to Erastothenes':
Start with the list L of all positive integers. 
Step 0: Remove 1 from the list and make it the first element of A3309.
For step = 1, 2, 3, ... : - Let k = first number of the list k. Append it to A3309. 
        - Delete k and every subsequent k-th number from the list L.

oeis.org/A255127: T(r,c) = c-th element of row r which lists the numbers that are removed from L at step = r.
     c = 1,  2,  3,  4,  5, ...
 r = 0:  1
 r = 1:  2,   4,   6,   8,  10,  12,   14,   16,   18,   20,   22,   24,   26  T(1,k) = T(2,k-1)+2 = 2n
 r = 2:  3,   9,  15,  21,  27,  33,   39,   45,   51,   57,   63,   69,   75  T(2,k) = T(2,k-1)+6 = 6k-3 ; {3n} \ every second  
 r = 3:  5,  19,  35,  49,  65,  79,   95,  109,  125,  139,  155,  169,  185  T(3,k) = T(3,k-2)+30 = 15k-11-k%2 ;
 r = 4:  7,  31,  59,  85, 113, 137,  163,  191,  217,  241,  269,  295,  323  T(4,k-8) + 210 = (k-1)\8*210 + T(4,(k-1)%8+1)
 r = 5: 11,  55, 103, 151, 203, 251,  299,  343,  391,  443,  491,  539,  587  T(5,k-48) + 2310,     P5 = P4*(7-1), S5 = S4 * 11
 r = 6: 13,  73, 133, 197, 263, 325,  385,  449,  511,  571,  641,  701,  761  T(6,k-480) + 30030,   P6 = P5*(11-1), S6 = S5 * 13
 r = 7: 17, 101, 187, 281, 367, 461,  547,  629,  721,  809,  901,  989, 1079  T(7,k-5760) + 510510, P7 = P6*(13-1), S7 = S6 * 17 
 r = 8: 23, 145, 271, 403, 523, 655,  781,  911, 1037, 1157, 1289, 1417, 1543  T(8,k-92160) + S8 		 P8 = P7*(17-1), S8 = S7 * 23
 r = 9: 25, 167, 311, 457, 599, 745,  883, 1033, 1181, 1321, 1469, 1615, 1753  T(9,k-P9) + S9		     P9 = P8*(23-1), S9 = S8*
 r =10: 29, 205, 371, 551, 719, 895, 1073, 1243, 1421, 1591, 1771, 1945, 2117  T(10,k-P10) + S10,   P10 = P9*(25-1), S10 = S9*
…
(Python)
class A255127: # use A[r, c] or A[n] = a(n) or A() for a subscriptable generator of the sequence
   def __class_getitem__(A, args): return A()[args]
   def __new__(A, *a, **k): return A[a if len(a)>1 else a[0]] if a else super().__new__(A, **k) 
   def __init__(A, n=None, k=None, start=1, stop=None, step=1):
      A.__dict__.update(start=start, stop=stop, step=step)
   def __iter__(A): return A # we want this to be iterable
   def __next__(A):
      if not(A.stop is None or A.start < A.stop): raise StopIteration 
      n = A.start; A.start += A.step; return A[n]
   row=[[1], [2], [3]] # rows 0, 1, 2
   P=[1]*3 ; S=[0,2,6] ; limit=30 ; debug=0
   def __getitem__(A, k): #print(f"getitem({A}, {k})")
      if isinstance(k, int): return A[A002260(k-1), A004736(k-1)]
      n,k = k # key/index k is a tuple (n,k). TODO: implement slice
      while len(A.row) <= n or len(A.row[n]) < min(k, A.P[n]): A.extend(2*n)
      #k -= 1; return A.row[n][k] if k < len(A.row[n]) else A.row[n][k%A.P[n]] + k//A.P[n]*A.S[n]
      return A.row[n][(k-1) % A.P[n]] + (k-1)//A.P[n] * A.S[n]
   def extend(A, nMax):
      A.limit  *= 2; L = [x+5-x%2 for x in range(0, A.limit, 3)] # after remove of every 2nd & 3rd 
      if A.debug: print(f"Extending to new limit {A.limit}.")
      for r in range(3, nMax): # we start with step r=3 of the sieve, where remaining = (5, 7, …)
         if len(A.P) == r:
            A.P += [ A.P[-1] * (A.row[-1][0] - 1) ]
            A.row += [[]] ; A.S += [ A.S[-1] * L[0] ] # ludic factorials
            if A.debug: print(f"Added row {r}, Now P[r] = {A.P[r]}, S[r] = {A.S[r]}.")
         if len(R := A.row[r]) < A.P[r]:  # append more terms to this row
            R += L[ L[0]*len(R) : A.S[r] : L[0] ]
            if A.debug: print(f"Now row {r} has length {len(R)} / {A.P[r]}.")
         L = [x for i, x in enumerate(L) if i%L[0]] # remove initial & every k-th element
      if A.debug: print(f"Done extending to limit {A.limit}.")

see also: oeis.org/A255413 - A255419 : rows 3..9
