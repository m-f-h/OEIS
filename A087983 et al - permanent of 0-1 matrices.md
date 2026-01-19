# Sequences related to permanents of 0-1 matrices

**Definition:** A **{0,1}-matrix**, a.k.a. (0,1)-matrix or 0,1-matrix or 0-1 matrix or 01-matrix,
is a matrix which has all its entries in {0, 1}, *i.e.*, either zero or one.
For a given size $m\times n$, the set of these matrices is denoted by $\mathcal M_{m,n}(\\{0,1\\})$.

**Definition:** The permanent of an $n\times n$ matrix $M$ is ${\rm perm} M = \sum_{s\in S_n} \prod_{i=1}^n M_{i, s(i)} $

### Concerned sequences:
* http://oeis.org/A087983 : number of distinct values the permanent of a 0-1 matrix can take
* http://oeis.org/A089475 : ...
* ...

### Useful facts
1. The permanent is zero whenever one row or column is zero.
2. The permanent doesn't change when the rows or columns are reordered according to any permutation.
3. The total number of possible matrices is $2^{n^2}$: (n x n entries in {0, 1})
4. The number of 0,1-matrices where none of the rows is zero is (2^n-1)^n : choose one of 1..2^n-1 for each row.
5. The number of 0,1-matrices where at least one of the rows is zero is 2^n^2 - (2^n-1)^n  ()

%PARI [2^n^2 - (2^n-1)^n | n<-[1..5]] = [1, 7, 169, 14911, 4925281] => http://oeis.org/A005019

## Specific sequences

### [A087983 : number of distinct values the permanent of a 0-1 matrix can take](http://oeis.org/A087983)
Here we simply count the *distinct* values. The order of the rows doesn't matter so we can assume them to be in increasing order.

(We identify the rows with binary numbers from 0 to M(n) = 2^n - 1.)

The permanent is zero unless M[n,1] = M[n-1,2] = M[n-2,3] = ... = M[1, n] = 1.
```PARI/GP
A087983(n)={ my(c=Vec(1, n!+1)/* count/mark values from 1 through n! = perm(all ones: 1^{n x n}) */ ,
                Mn=2^n-1, M=matrix(n,n,i,j,j==n-i+1), min_row=vector(n,i,2^(i-1)), rows=min_row, row=n); 
while(row/* row to increment */, if( row==n, for(j=rows[n],Mn, M[n,]=binary(j); c[matpermanent(M)+1]=1); row--,
  rows[row] < Mn, rows[row]++; until(row>=n, M[row,] = Vec(binary(rows[row]),-n); rows[row++]=max(rows[row-1],min_row[row]) ),
  row--)); vecsum(c) }

/* version using bitmap, with "bittest || += " */

A087983(n)={ my(map=1/* bitmap of observed values */,
                Mn=2^n-1, M=matrix(n,n,i,j,j==n-i+1), min_row=vector(n,i,2^(i-1)), rows=min_row, row=n, t); 
while(row/* row to increment */, if( row==n, for(j=rows[n],Mn, M[n,]=binary(j); bittest(map, t=matpermanent(M)) || map += 1<<t),
  rows[row] < Mn, rows[row]++; /* store in matrix and reset subsequent rows to minimum */
                  until(row>=n, M[row,] = Vec(binary(rows[row]),-n); rows[row++]=max(rows[row-1],min_row[row]) ); next);
  row--); hammingweight(map) }

/* version using bitmap, with "bitand" */

A087983(n)={ my(map=1/* bitmap of observed values */, Mn=2^n-1, M=matrix(n,n,i,j,j==n-i+1),
                min_row=vector(n,i,2^(i-1)), rows=min_row); forstep(row=n, 1, -1,
  if( row==n, for(j=rows[n], Mn, M[n,]=binary(j); map=bitor(1<<matpermanent(M), map)),
      rows[row] < Mn, rows[row]++; /* store in matrix and reset subsequent rows to minimum */
                      until(row>=n, M[row,] = Vec(binary(rows[row]),-n); rows[row++]=max(rows[row-1],min_row[row]) ); row++)
  ); hammingweight(map) }

/* back to while(row...) */

A087983(n)={ my(map=1/* bitmap of observed values */, Mn=2^n-1, M=matrix(n,n) /* initialize through n=1 */,
                min_row=vector(n,i,2^(i-1)), rows=min_row, row=1); n&& while(row,
  if( row==n, for(j=rows[n], Mn, M[n,]=binary(j); map=bitor(1<<matpermanent(M), map)),
      rows[row] < Mn, rows[row]++; /* store in matrix and reset subsequent rows to minimum */
                      until(row>=n, M[row,] = Vec(binary(rows[row]),-n); rows[row++]=max(rows[row-1],min_row[row]) ); next);
  row--); hammingweight(map) }

apply(A087983, [0..5])
```
