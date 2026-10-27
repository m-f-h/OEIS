---
title: "A276523: Mondrian art puzzle and Python code"
permalink: /Mondrian/
History:
  2026-10-23: source code created
  2026-10-24: github page created, renamed optimal_tilings to A278970, added option tilings=None/1/all
---
The **Mondrian art puzzle** consists in finding a tiling of an <i>n &times; n</i> square into
incongruent rectangles, such that the **_defect_** := difference between the areas of the 
largest and the smallest rectangle, is minimal.

References: <small>&nbsp;&#x25CF;&nbsp;</small> [oeis:A276523](https://oeis.org/A276523) gives the least defect for size n.
- [Interactive web page `phoenixsmaug.github.io/mondrian-web` by Mia Müßig](https://phoenixsmaug.github.io/mondrian-web/)

```(Python)
#!/usr/bin/env python3
"""Mondrian Art Puzzle. - (c) Oct. 2026 by M.F.H.

Tile an n x n square with integer-sided rectangles that are pairwise non-congruent
(a x b and b x a count as the same shape), and minimise (largest area) - (smallest area).

A276523(n) gives the minimal defect for size n, and with optional arg `tilings = True` or "all",
the corresponding solution(s).
"""
# both includes only needed for __main__/driver
import sys 
import time

def A276523(n, tilings=False):
    """Return the smallest achievable defect d, or (d, L) if `tilings`,
    then L = [first (or all) optimal solution(s) if `tilings`==True (or "all")].

    For each d = 2, 3, ..., try every window [m, m + d] of allowed areas.
    The first d that admits a tiling is optimal.
    """
    found = []; n2 = n*n
    for d in range(2, n2): # we know d <= 2n, d <= n if odd, <= 4a(n/2) else
        for m in range(1, n2//2 + 1):
            shapes = shapes_in_window(n, m, m+d)
            if sum(s[0] for s in shapes) < n2: continue # only for speedup
            for t in tilings(n, shapes):
                if tilings != 'all': return d, [t] if tilings else d
                # don't repeat the same solution across windows
                if min(w * h for _, _, w, h in t) == m: found.append(t)
        if found: return d, found
    return None, [] # can & will only happen for n < 3.

def shapes_in_window(n, lo, hi):
    """Shapes (area, a, b), sorted, with lo <= area <= hi, b > a < n to exclude n x n.
    Smaller/larger shape refers to the rank (area, a), independent of the window of allowed areas.
    """
    return sorted((a*b, a, b) for a in range(1, n) for b in range(a, n + 1)
                  if lo <= a * b <= hi)

# lightweight class mainly for display -- not really needed to compute the OEIS sequence
class Tiling(tuple):
    """A tiling is a tuple of rectangles (x, y, w, h): lower-left corner and size,
       tiling an n x n square, given in the order they were placed.
    """
    def __str__(self):
        n = max(x + w for x, y, w, h in self); grid = [["."]*n for _ in range(n)]
        for c, (x, y, w, h) in enumerate(self):
            for j in range(y, y + h): grid[j][x:x + w] = chr(65+c%26)*w
        return "\n".join(reversed([self.describe(), ''] + grid)) 
    def describe(self): return ", ".join(f"{a}x{b}={s}" for s, a, b in self.sizes())
    def sizes(self): return sorted((w * h, min(w, h), max(w, h)) for x, y, w, h in self)
    def defect(self): return max(a := [w * h for x, y, w, h in self]) - min(a) # unused

def tilings(n, shapes):
    """Yield every tiling built from `shapes` (each used at most once),
    exactly once up to rotations and reflections of the square.

    Pieces are placed at the lowest, leftmost uncovered cell (skyline order).
    Symmetry breaking, with 'smaller' meaning smaller as a tuple (area, a, b):
      1. The first piece placed sits in the lower-left corner, is the smallest
         of all pieces touching a corner, and is horizontal (w >= h).
         This fixes the symmetry except in the two cases below.
      2. First piece is a square: the reflection in the diagonal through the
         lower-left corner remains.  It swaps the lower-right and upper-left
         corner pieces, so the upper-left one must be larger than the
         lower-right one.
      3. First piece is a full-width strip: the left-right mirror remains.
         Full-width pieces are mirror-symmetric, so only the first piece
         that is NOT full-width matters.  The skyline fills a row from left
         to right, so that piece is placed at the left wall first; the piece
         later placed at the right wall in the same row must be larger.
         After that the symmetry is broken and nothing more is checked.
    """
    total, heights = n*n, [0]*n # skyline: filled height of each column
    used, placed = set(), []    # shapes (ab, a, b) and tiles (x, y, w, h)

    def rec(covered, avail, p, q):
        # p: first piece; q: lower-right corner piece (mode SQUARE);
        if covered == total: Tiling(placed); return
        if avail < total - covered: return # can't fill the rest
        x = heights.index(y := min(heights))
        run = 1 # width of the flat segment at height y
        while x + run < n and heights[x + run] == y: run += 1
        square, strip = p[1] == p[2], p[2] == n   # type of first piece
        for s in shapes:
            if s in used: continue
            area, a, b = s
            for w, h in {(a, b), (b, a)}:
                if w > run or y + h > n: continue
                p2, q2 = p, q  # p,q will be re-used for next shape
                if not placed:          # Rule 1: the first rectangle
                    if w < h: continue  #    (in lower left corner)
                    p2 = s              #    must not be "vertical", and
                else:                   #    no other corner must have "smaller"
                    left, right, bottom, top = x == 0, x + w == n, y == 0, y + h == n
                    if (top or bottom) and (left or right) and s < p: continue # Rule 1
                    if square:          # Rule 2: top left > bottom right
                        if top and left and s < q: continue
                        if bottom and right: q2 = s  #   store for later
                    elif strip and left != right and q:  # Rule 3
                        if left: q2 = s
                        elif s > q: q2 = None
                        else: continue

                used.add(s) ; placed.append((x, y, w, h))
                for i in range(x, x + w): heights[i] += h
                yield from rec(covered + area, avail - area, p2, q2)
                for i in range(x, x + w): heights[i] -= h
                placed.pop() ; used.discard(s)

    yield from rec(0, sum(s[0] for s in shapes), (0,0,0), ())

# This isn't needed for the OEIS sequence, only for study/checks:
def inequivalent_tilings(n, max_defect=None, limit=None):
    """Yield pairwise inequivalent tilings (up to rotation/reflection).

    max_defect: only tilings with (max area - min area) <= max_defect.
                None means no restriction -- this explodes quickly with n.
    limit:      stop after this many tilings.
    """
    count = 0
    if max_defect is None: windows = [(1, n * n)]
    else:
        windows = [(m, m + max_defect) for m in range(1, n * n // 2 + 1)]
    for lo, hi in windows:
        shapes = shapes_in_window(n, lo, hi)
        if sum(s[0] for s in shapes) < n * n: continue
        for t in tilings(n, shapes):
            # in a window, report only tilings whose smallest area is exactly lo
            if max_defect is None or min(w * h for _, _, w, h in t) == lo:
                yield t; count += 1
                if limit and count >= limit: return

def doit(n, all = False):
    t0 = time.time()
    d, sols = A276523(n, 'all' if all else 1)
    if d is None: print(f"n={n}: no tiling exists")
    else:
        print(f"n={n}: optimal defect = {d}"
              f"  ({len(sols)} inequivalent solution(s))"
              f"  [{time.time() - t0:.2f}s]")
        for s in sols[:3]: print(s, "\n")

if __name__ == "__main__":
    doit(int(sys.argv[1] if len(sys.argv) > 1 else input("Enter size: ")),
         "--all" in sys.argv)
```
