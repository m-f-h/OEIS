permalink: /A035014/
---
# A035014 etc.: multiple of 2^n with n digits in {A, B}

These sequences (most in [A053312](http://oeis.org/A053312)-[A053380](http://oeis.org/A053380)) are of the form

> a(n) = unique number having n digits A or B which is divisible by 2^n

where 0 < A < B < 10 are two nonzero digits with opposite parity.

It is somewhat remarkable that this definition defines a(n) uniquely.
<br/>
Also note that they are not "the same up to substitution of the digits".
<br/>
**FORMULA:** a(n+1) = a(n) + 10^n * (A if a(n)/2^n odd else B), assuming A is the odd digit.

## Program (PARI/GP, others to follow)
```(PARI)
/* Shortest possibility in the 3rd vector arg is to use d[!(t%2^k)+1]
 * which is = d[2] if !t%2^k <=> t%2^k == 0 <=> need even digit, = d[1] else.
 * So the odd digit must come first.
 */
first(n, d=[1,2], t=0)= d[2]%2 && d=Vecrev(d); vector(n, k, t += d[!(t%2^k)+1]*10^(k-1))

/* explicit exhaustive search (this works only for digits [d,d+1], use e.g. vecextract for other cases) */
find(n,D=[7,8])=forvec(d=vector(n,i,D),fromdigits(d)%2^n||print(d)) \\ not return() to see all solutions

```
## Table of the sequences for given digits A, B:

* 1,2 : [A053312](http://oeis.org/A053312) = 2, 12, 112, 2112, 22112, 122112, 2122112, 12122112, 212122112, 1212122112
* 1,4 : [A053314](http://oeis.org/A053314) = 4, 44, 144, 4144, 14144, 414144, 1414144, 41414144, 441414144, 1441414144
* 2,3 : [A053316](http://oeis.org/A053316) = 2, 32, 232, 3232, 23232, 223232, 2223232, 32223232, 232223232, 3232223232
* 2,5 : [A053317](http://oeis.org/A053317) = 2, 52, 552, 5552, 55552, 255552, 5255552, 55255552, 255255552, 2255255552
* 2,7 : [A053318](http://oeis.org/A053318) = 2, 72, 272, 2272, 22272, 222272, 7222272, 27222272, 727222272, 2727222272
* 2,9 : [A053313](http://oeis.org/A053313) = 2, 92, 992, 2992, 92992, 292992, 2292992, 22292992, 222292992, 2222292992
* 3,4 : [A035014](http://oeis.org/A035014) = 4, 44, 344, 3344, 33344, 433344, 3433344, 33433344, 333433344, 3333433344
* 4,5 : [A053315](http://oeis.org/A053315) = 4, 44, 544, 4544, 44544, 444544, 4444544, 54444544, 454444544, 5454444544
* 4,7 : [A053332](http://oeis.org/A053332) = 4, 44, 744, 7744, 47744, 447744, 4447744, 44447744, 444447744, 4444447744
* 4,9 : [A053333](http://oeis.org/A053333) = 4, 44, 944, 4944, 94944, 994944, 4994944, 94994944, 494994944, 9494994944<br><br>
* 1,6 : [A053334](http://oeis.org/A053334) = 6, 16, 616, 1616, 11616, 111616, 6111616, 16111616, 616111616, 1616111616
* 3,6 : [A053335](http://oeis.org/A053335) = 6, 36, 336, 6336, 66336, 366336, 6366336, 36366336, 636366336, 3636366336
* 5,6 : [A053336](http://oeis.org/A053336) = 6, 56, 656, 6656, 66656, 566656, 6566656, 66566656, 666566656, 6666566656
* 6,7 : [A053337](http://oeis.org/A053337) = 6, 76, 776, 7776, 67776, 667776, 6667776, 66667776, 766667776, 6766667776
* 6,9 : [A053338](http://oeis.org/A053338) = 6, 96, 696, 9696, 69696, 669696, 6669696, 96669696, 696669696, 9696669696<br><br>
* 1,8 : [A053376](http://oeis.org/A053376) = 8, 88, 888, 1888, 81888, 181888, 8181888, 18181888, 118181888, 8118181888
* 3,8 : [A053377](http://oeis.org/A053377) = 8, 88, 888, 3888, 33888, 333888, 3333888, 83333888, 383333888, 3383333888
* 5,8 : [A053378](http://oeis.org/A053378) = 8, 88, 888, 5888, 85888, 885888, 8885888, 58885888, 558885888, 8558885888
* 7,8 : [A053379](http://oeis.org/A053379) = 8, 88, 888, 7888, 77888, 877888, 7877888, 87877888, 787877888, 8787877888
* 8,9 : [A053380](http://oeis.org/A053380) = 8, 88, 888, 9888, 89888, 989888, 9989888, 89989888, 989989888, 8989989888

