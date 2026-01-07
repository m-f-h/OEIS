----
A186655(n) = number of numbers below 10^n that can be written as sum of 5 biquadrates
```
(PARI)
A186655(n, k=5) = { my(L = 10^n - k, m = sqrtnint(L,4), S = [[x^4] | x <- [1..m] ]);
  for(iter = 2, k, L++; my(b, N = #S - !S[#S]);
    S = [ [s+b | s <- concat(S[i..N]), s < L-b] | i <- [1..N], b = i^4 ];
  );
  #[0 | s <- Set(concat(S)), A002377(s)==5]
}
apply(A186655, [1..5])

/* Fast version (needs allocatemem(2^27 = 128 MB) for n=6) */

A186655(n)=#[0| t<-A002377_first(10^n-1, 5), t==5] /* with */
A002377_first(n, m=19)={my(v=vector(n), s=sum(k=1, sqrtnint(n,4), x^k^4)+ O(x^(n+1)) , p=1);
 for(k=1, m, p*=s; for(i=1, n, if(polcoef(p, i) && !v[i], v[i]=k))); v} 
(inspired from `seq` in oeis.org/A002377)

/* earlier versions: */
A186655(n, k=5) = { my(biqs = vector(sqrtnint(10^n-k,4), i, i^4), sums = biqs, L = 10^n);
  for(i=2, k, sums=concat([[a+b | a <- sums, a+b < L] | b <- biqs]));
  #sums > #(sums=Set(sums)) && print("There were duplicates!"); #sums
}
/* idea : use (sum, smallest), and add any biquadrate <= smallest */
Q: how many nondecreasing sequences do we have?
A: binomial(max+num-1, num) : choose num among 1 .. max+num-1
check: nnd(max, num, c=0)=forvec(v=vector(num,i,[1,max]),c++,1);c /* => A059481 = binomial(n+k-1, k), 0 <= k <= n >= 0 */
[nnd(m,5)|m<-[1..5]] \\ %19 = [1, 6, 21, 56, 126]

/*idea : use a list with nb items each item L[i] has the sums of (iter) terms with smallest term i^4
i | L[i] @ 0 | L[i] @ 1 (add L[j >= i])           | L[i] @ 1 (add L[j >= i])           | |
1 | 1^4      | 1^4 x 2, 1^4+2^4, 1^4+3^4, 1^4+4^4 |
2 | 2^4      | 4^4 + 2^4, 3^4 + 2^4, 2^4 x 2 : to any L[j >= i], we add i^4    | 
3 | 3^4      | 4^4 + 3^4, 3^4 x 2                 | 3^4 x 3, 3^4 x 2 + 4^4 (added 3^4 to second elt), 3^4 + 4^4 x 2
4 | 4^4      | 4^4 x 2                            | 4^4 x 3 
*/
A186655(n, k=5, verbose=0) = { my(L = 10^n - k, m = sqrtnint(L,4), sums = [ [x^4] | x <- [1..m] ], b);
  for(iter = 2, k, L++; for(i = 1, #sums, b = i^4; sums[i] = concat([[s+b | s <- S, s+b < L ] | S <- sums[i..-1]]) );
  #sums[#sums] || sums = sums[^-1];
  \\ ;print("After iter "iter", sums="sums)
  );
  \\ if( sum ( i=1, #sums, #sums[i] ) > m = #Set(concat(sums)), print("There were duplicates!")); m
  #sums = [s | s <- Set(concat(sums)), A002377(s)==5]
  \\ if ( verbose, Set(concat(sums)), #Set(concat(sums)) )
}
/* cleaned up: */
A186655(n, k=5) = { my(L = 10^n - k, m = sqrtnint(L,4), S = [[x^4] | x <- [1..m] ]);
  for(iter = 2, k, L++;
    for(i = 1, #S, my(b = i^4); S[i] = [s+b | s <- concat(S[i..-1]), s+b < L] );
  #S[#S] || S = S[^-1];
  );
  #[0 | s <- Set(concat(S)), A002377(s)==5]
}
/* further optimized: see top */

\\ gives a(3) = 69 instead of 67 ...

/* number of biquadrates requred for n -- turns ou that this is A002377 */
decompose(n, m=5 /*max terms*/, L=n /*largest part*/, r = sqrtnint(n,4), best = n) = {
if ( n == r^4, 1, m -= 1 /* dig deeper? */, forstep ( p=min(r,L),1,-1, n > (m+1)*p^4 && break;
     my(t=decompose(n-p^4, m, p)); t && best = min(best,t) ) /* end forstep */; best+1) }

apply(decompose,%50)
%58 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
(16:21) gp > select(t->t<5,%58,1)
%60 = Vecsmall([39, 43]) \\ %58[]
(16:23) gp > vecextract(%50,%)
%65 = [625, 674] \\ the first is a biquadrate itself, the 2nd can be written as sum of 4 only.

without upper limit, this is A002377. Actually, the upper limit is 19 -- see there.
```
