---
title: "A055165 et al.: Number of {0,1}-matrices given size and rank."
permalink: /A055165/
remarks: using <pre> didn't work :-(
---
Related sequences:
- A055165: Number of invertible n X n matrices with entries equal to 0 or 1.
  <pre>
  1, 1, 6, 174, 22560, 12514320, 28836612000, 270345669985440, 10160459763342013440, ?</pre>
- A088389 = A055165(n)/n! : `1, 1, 3, 29, 940, 104286, 40050850, 53640013886, 251995529844792, ?`
- A064230: Triangle T(n,k) = number of rational (0,1) matrices of rank k (n >= 0, 0 <= k <= n):
  <pre>
  1;
  1,   1;
  1,   9,      6;
  1,  49,    288,     174;
  1, 225,   6750,   36000,    22560;
  1, 961, 118800, 3159750, 17760600, 12514320;</pre>
  (A055165 is the main diagonal of this.)

Note: Here we consider {0,1}-matrices over integers/rationals/reals, not over GF(2), as in [A002884](https://oeis.org/A002884)!

I started by writing somehow "elementary" PARI/GP code for A055165 and A088389:
```
(PARI/GP)
{A055165(n, m=2^n-1, A=Mat(), f(x)=Col(binary(x), -n))=if(n,
   my(r=#A=matconcat([A, Col(0, n)])); n*sum(b=2^n--, m, A[, r]=f(b); if(matrank(A)==r, A055165(n, b-1, A, f)))
   , 1)} \\ M. F. Hasler, Oct 26 2026
```
and A088389 is the same without the factor " n* ". The idea(s): 
- we must have n pairwise distinct rows;
  we can WLOG assume them in strictly increasing or rather decreasing lexicographical order,
  row(r) < row(r-1), and then multiply by the n! possible permutations. 
- The largest row must have 1 in the 1st column, row(1) >= (1, 0...0).<br/>
  The smallest row must have at least it's n-th element nonzero: row(n) >= (0...0, 1),
  then the (n-1)-th row must have at least it's (n-1)-th element nonzero, etc. 
- If we code the rows in binary, that means row(r) >= 2^(r-1) and row(r) < row(r-1).
- If we have chosen rows 1..r, we need only go "deeper" in the recursion if the set of these rows is of rank r.

Up to n=5, this is blazing fast. (Obviously much faster then earlier code that constructed all {0,1}-matrices.)

However, for n >= 6, it becomes too slow. Also, to get {0,1}-matrices of larger size that have given rank
(i.e., the terms below the diagonal in A064230), this approach becomes too slow. 

So we tried some more "intelligent" approaches in Python:
```(Python)
""" rank-r-nxn-matrices.py
"""
import itertools
import numpy as np
import scipy.linalg
import time,timeit
import math

def solve_subspace_dp(n, r):
    all_vecs = [np.array(p) for p in itertools.product([0, 1], repeat=n)]
    num_vecs = len(all_vecs)
    
    # Map vector to integer index
    vec_to_idx = {tuple(p): i for i, p in enumerate(itertools.product([0, 1], repeat=n))}
    
    # Subspace represented by a frozenset of vector indices
    subspaces_by_dim = {d: set() for d in range(r + 1)}
    
    # Dim 0
    zero_subspace = frozenset([0]) # index 0 is (0,0,...,0)
    subspaces_by_dim[0].add(zero_subspace)
    
    # Build subspaces dimension by dimension
    for d in range(1, r + 1):
        for prev_sub in subspaces_by_dim[d - 1]:
            # Try adding vectors not in prev_sub
            prev_vecs = [all_vecs[i] for i in prev_sub]
            M_prev = np.array(prev_vecs)
            
            for i in range(1, num_vecs):
                if i not in prev_sub:
                    # Form new subspace
                    new_vec = all_vecs[i]
                    M_new = np.vstack([M_prev, new_vec])
                    if np.linalg.matrix_rank(M_new) == d:
                        # Find all binary vectors in span(M_new)
                        in_span = []
                        for j in range(num_vecs):
                            M_test = np.vstack([M_new, all_vecs[j]])
                            if np.linalg.matrix_rank(M_test) == d:
                                in_span.append(j)
                        subspaces_by_dim[d].add(frozenset(in_span))

    print(f"Subspace counts for n={n}, r={r}:")
    for d in range(r + 1):
        print(f"  Dim {d}: {len(subspaces_by_dim[d])} subspaces")

    # Now compute N_n(V) for each subspace in increasing dimension order
    N_map = {} # subspace -> count
    
    for d in range(r + 1):
        for sub in subspaces_by_dim[d]:
            K = len(sub)
            # Sum N_map[U] for all proper sub-subspaces U < sub
            sub_sum = 0
            for u in N_map:
                if u < sub: # proper subset
                    sub_sum += N_map[u]
            N_map[sub] = (K ** n) - sub_sum

    total_rank_r = sum(N_map[sub] for sub in subspaces_by_dim[r])
    return total_rank_r

def go(n=4,r=4,f=solve_subspace_dp):
    cmd=f'print("Résultat:",f{n,r})'; print("time:",
    f"{timeit.timeit(cmd,number=1,globals={'f':f}):.3f} sec")
'''
go()
Subspace counts for n=4, r=4:
  Dim 0: 1 subspaces
  Dim 1: 15 subspaces
  Dim 2: 55 subspaces
  Dim 3: 45 subspaces
  Dim 4: 1 subspaces
Résultat: 22560
time: 0.365 sec
go(5,4)
Subspace counts for n=5, r=4:
  Dim 0: 1 subspaces
  Dim 1: 31 subspaces
  Dim 2: 285 subspaces
  Dim 3: 845 subspaces
  Dim 4: 625 subspaces
Résultat: 17760600
time: 15.952 sec
'''
# Test Kernel / Linear Equations check for binary vectors in span(M) over R

def get_binary_vectors_in_span(basis_rows, n):
    # basis_rows: d x n matrix of float/int
    M = np.array(basis_rows, dtype=float)
    # Compute nullspace of M^T
    # Ker(M^T) gives vectors orthogonal to row space of M
    # In scipy/numpy, SVD gives null space
    u, s, vh = np.linalg.svd(M)
    rank = len(s)
    # basis for null space of M^T: columns of u corresponding to zero singular values
    # Wait, row space of M is spanned by rows of M. Nullspace of M^T is vectors perp to rows of M.
    # So y in span(M) iff y is orthogonal to nullspace of M (i.e. ker(M)) ? No, ker(M^T)!
    # Let's check: M is d x n. Row space is spanned by rows of M.
    # The orthogonal complement of rowspace(M) in R^n is Ker(M).
    # So y in rowspace(M) iff Ker(M) * y = 0!
    # Ker(M) has dimension n - rank.
    # So y is in span(M) iff Ker(M) @ y == 0!
    
    # Let's verify:
    # Compute Ker(M):
    u, s, vh = np.linalg.svd(M)
    # vh has shape (n, n). The last (n - rank) rows of vh form a basis for Ker(M)!
    ker_M = vh[rank:] # shape (n - rank, n)
    
    # All binary vectors Y: n x 2^n
    Y = np.array(list(itertools.product([0, 1], repeat=n))).T # n x 2^n
    
    # Check ker_M @ Y == 0
    residuals = ker_M @ Y
    is_zero = np.all(np.abs(residuals) < 1e-9, axis=0)
    
    # Indices of binary vectors in span(M)
    return np.where(is_zero)[0]

# Test with a basis:
def test(basis = [[1, 0, 1, 0], [0, 1, 0, 1]]):
    indices = get_binary_vectors_in_span(basis, 4)
    print("Binary vectors in span of [[1,0,1,0], [0,1,0,1]]:")
    print(indices) # should be (0,0,0,0), (1,0,1,0), (0,1,0,1), (1,1,1,1) -> indices 0, 10, 5, 15

def solve_subspace_fast(n, r):
    t0 = time.time()
    # Precompute binary vectors
    all_bin = [np.array(p) for p in itertools.product([0, 1], repeat=n)]
    num_vecs = 2**n
    
    # Store subspaces by dimension as list of sets of vector indices
    # Also store basis for each subspace
    subspaces_by_dim = {d: [] for d in range(r + 1)}
    
    # Dim 0
    subspaces_by_dim[0].append({
        'set': frozenset([0]),
        'basis': np.empty((0, n))
    })
    
    seen_sets_by_dim = {d: {frozenset([0]): 0} if d == 0 else {} for d in range(r + 1)}
    
    for d in range(1, r + 1):
        for parent_idx, parent in enumerate(subspaces_by_dim[d - 1]):
            parent_set = parent['set']
            parent_basis = parent['basis']
            
            for b in range(1, num_vecs):
                if b not in parent_set:
                    new_row = all_bin[b].reshape(1, n)
                    if parent_basis.shape[0] == 0:
                        new_basis = new_row
                    else:
                        new_basis = np.vstack([parent_basis, new_row])
                    
                    if np.linalg.matrix_rank(new_basis) == d:
                        # Find all vectors in span of new_basis
                        # Using SVD/kernel
                        u, s, vh = np.linalg.svd(new_basis)
                        ker = vh[d:] # (n - d, n)
                        
                        # All binary vectors Y
                        Y = np.array(all_bin).T # (n, 2^n)
                        if ker.shape[0] > 0:
                            res = np.abs(ker @ Y)
                            in_span = np.where(np.all(res < 1e-9, axis=0))[0]
                        else:
                            in_span = np.arange(num_vecs)
                            
                        span_set = frozenset(in_span)
                        if span_set not in seen_sets_by_dim[d]:
                            seen_sets_by_dim[d][span_set] = len(subspaces_by_dim[d])
                            subspaces_by_dim[d].append({
                                'set': span_set,
                                'basis': new_basis
                            })

    t1 = time.time()
    print(f"Time to find subspaces for n={n}, r={r}: {t1 - t0:.3f} s")
    
    # Now compute N(V) using Inclusion-Exclusion
    # Flatten all subspaces into a single list with their dimension
    all_subs = []
    for d in range(r + 1):
        for sub in subspaces_by_dim[d]:
            all_subs.append(sub['set'])
            
    num_total_subs = len(all_subs)
    N_vals = np.zeros(num_total_subs, dtype=object) # python big integers!
    
    # Compute N(V) in order
    for i in range(num_total_subs):
        S_v = all_subs[i]
        K = len(S_v)
        # sum N_vals[j] for all proper subsets S_u < S_v
        sub_sum = 0
        for j in range(i):
            if all_subs[j] < S_v: # proper subset check
                sub_sum += N_vals[j]
        N_vals[i] = (K ** n) - sub_sum

    # Total rank r count is sum over dim r
    dim_r_offset = sum(len(subspaces_by_dim[d]) for d in range(r))
    total_r = sum(N_vals[dim_r_offset:])
    
    t2 = time.time()
    print(f"Total time for n={n}, r={r}: {t2 - t0:.3f} s")
    return total_r

"""
go(4, 4, solve_subspace_fast)
Time to find subspaces for n=4, r=4: 0.040 s
Total time for n=4, r=4: 0.053 s
Résultat: 22560
time: 0.071 sec

go(5, 4, solve_subspace_fast)
Time to find subspaces for n=5, r=4: 1.109 s
Total time for n=5, r=4: 1.196 s
Résultat: 17760600
time: 1.255 sec

go(6, 4, solve_subspace_fast)
Time to find subspaces for n=6, r=4: 99.057 s
Total time for n=6, r=4: 202.315 s
Résultat: 5295204600
time: 202.365 sec
"""

def solve_with_orbit_reduction(n, r):
    all_bin = [np.array(p) for p in itertools.product([0, 1], repeat=n)]
    num_vecs = 2**n
    perms = list(itertools.permutations(range(n)))
    fact_n = math.factorial(n)

    # 1. Compute Canonical RREF key and orbit size
    def get_orbit_info(basis):
        d = basis.shape[0]
        if d == 0:
            return (), 1
        
        seen_rrefs = set()
        best_rref = None
        
        for p in perms:
            perm_b = basis[:, p]
            M = np.array(perm_b, dtype=float)
            r_idx = 0
            for c in range(n):
                pivot = None
                for i in range(r_idx, d):
                    if abs(M[i, c]) > 1e-9:
                        pivot = i
                        break
                if pivot is not None:
                    M[[r_idx, pivot]] = M[[pivot, r_idx]]
                    M[r_idx] /= M[r_idx, c]
                    for i in range(d):
                        if i != r_idx and abs(M[i, c]) > 1e-9:
                            M[i] -= M[i, c] * M[r_idx]
                    r_idx += 1
                if r_idx == d:
                    break
            
            rref_tuple = tuple(tuple(np.round(row, 5)) for row in M[:d])
            seen_rrefs.add(rref_tuple)
            if best_rref is None or rref_tuple < best_rref:
                best_rref = rref_tuple
                
        return best_rref, len(seen_rrefs)

    # 2. Get all binary vectors in the span of a basis
    def get_span_binary_indices(basis, d):
        if d == 0:
            return frozenset([0])
        u, s, vh = np.linalg.svd(basis)
        ker = vh[d:]
        Y = np.array(all_bin).T
        if ker.shape[0] > 0:
            res = np.abs(ker @ Y)
            return frozenset(np.where(np.all(res < 1e-9, axis=0))[0])
        else:
            return frozenset(range(num_vecs))

    # 3. Generate Orbit Representatives
    orbits_by_dim = {d: [] for d in range(r + 1)}
    orbits_by_dim[0].append({
        'key': (), 'basis': np.empty((0, n)), 'orbit_size': 1,
        'span': frozenset([0]), 'K': 1
    })

    seen_keys = {0: {(): 0}}

    for d in range(1, r + 1):
        seen_keys[d] = {}
        for parent in orbits_by_dim[d - 1]:
            p_basis = parent['basis']
            p_span = parent['span']
            
            for b in range(1, num_vecs):
                if b not in p_span:
                    new_row = all_bin[b].reshape(1, n)
                    new_basis = new_row if p_basis.shape[0] == 0 else np.vstack([p_basis, new_row])
                    
                    if np.linalg.matrix_rank(new_basis) == d:
                        key, num_orbit = get_orbit_info(new_basis)
                        if key not in seen_keys[d]:
                            span_set = get_span_binary_indices(new_basis, d)
                            seen_keys[d][key] = len(orbits_by_dim[d])
                            orbits_by_dim[d].append({
                                'key': key, 'basis': new_basis, 'orbit_size': num_orbit,
                                'span': span_set, 'K': len(span_set)
                            })

    # 4. Inclusion-Exclusion on Orbit Poset
    all_orbits = []
    for d in range(r + 1):
        all_orbits.extend(orbits_by_dim[d])
        
    num_total_orbits = len(all_orbits)
    N_orbit = [0] * num_total_orbits

    for i in range(num_total_orbits):
        orb_v = all_orbits[i]
        span_v = orb_v['span']
        K_v = orb_v['K']
        
        sub_sum = 0
        for j in range(i):
            orb_u = all_orbits[j]
            basis_u = orb_u['basis']
            d_u = basis_u.shape[0]
            
            if d_u == 0:
                count_in_v = 1
            else:
                count_in_v = 0
                seen_sub_spans = set()
                for p in perms:
                    perm_u = basis_u[:, p]
                    perm_span = get_span_binary_indices(perm_u, d_u)
                    if perm_span not in seen_sub_spans:
                        seen_sub_spans.add(perm_span)
                        if perm_span < span_v:
                            count_in_v += 1
            
            sub_sum += count_in_v * N_orbit[j]
            
        N_orbit[i] = (K_v ** n) - sub_sum

    # 5. Sum results for target rank r
    return sum(
        all_orbits[i]['orbit_size'] * N_orbit[i] 
        for i in range(num_total_orbits) 
        if all_orbits[i]['basis'].shape[0] == r
    )

'''
go(4, 4, solve_with_orbit_reduction) # time: 0.241 sec, Résultat: 22560
go(5, 4, solve_with_orbit_reduction) # time: 9.947 sec, Résultat: 17760600
go(6, 4, solve_with_orbit_reduction) # timeout
'''

def solve_rank_orbit_fast(n, r):
    t0 = time.time()
    num_vecs = 2**n
    all_bin = [np.array(p) for p in itertools.product([0, 1], repeat=n)]
    perms = list(itertools.permutations(range(n)))
    
    # Precompute permutation map for integer bitmasks (720 x 64 for n=6)
    perm_index_map = np.zeros((len(perms), num_vecs), dtype=int)
    for p_idx, p in enumerate(perms):
        for v_idx in range(num_vecs):
            bits = format(v_idx, f'0{n}b')
            perm_bits = "".join(bits[i] for i in p)
            perm_index_map[p_idx, v_idx] = int(perm_bits, 2)

    # Fast canonical key and permuted span cache
    def get_orbit_spans(span_indices):
        arr = np.array(sorted(span_indices))
        permuted_arrs = perm_index_map[:, arr]
        permuted_sorted = np.sort(permuted_arrs, axis=1)
        min_tuple = min(tuple(row) for row in permuted_sorted)
        distinct_spans = [frozenset(row) for row in set(tuple(row) for row in permuted_sorted)]
        return min_tuple, distinct_spans

    # Build orbit representatives dimension-by-dimension
    orbits_by_dim = {d: [] for d in range(r + 1)}
    orbits_by_dim[0].append({
        'key': (0,), 'basis': np.empty((0, n)), 'orbit_size': 1,
        'span': frozenset([0]), 'K': 1, 'distinct_spans': [frozenset([0])]
    })
    seen_keys_by_dim = {d: {(0,)} if d == 0 else set() for d in range(r + 1)}

    for d in range(1, r + 1):
        for parent in orbits_by_dim[d - 1]:
            p_basis = parent['basis']
            p_span = parent['span']
            
            for b in range(1, num_vecs):
                if b not in p_span:
                    new_row = all_bin[b].reshape(1, n)
                    new_basis = new_row if p_basis.shape[0] == 0 else np.vstack([p_basis, new_row])
                    
                    if np.linalg.matrix_rank(new_basis) == d:
                        u, s, vh = np.linalg.svd(new_basis)
                        ker = vh[d:]
                        Y = np.array(all_bin).T
                        res = np.abs(ker @ Y)
                        span_set = frozenset(np.where(np.all(res < 1e-9, axis=0))[0])
                        
                        key, distinct_spans = get_orbit_spans(span_set)
                        if key not in seen_keys_by_dim[d]:
                            seen_keys_by_dim[d].add(key)
                            orbits_by_dim[d].append({
                                'key': key, 'basis': new_basis, 'orbit_size': len(distinct_spans),
                                'span': span_set, 'K': len(span_set), 'distinct_spans': distinct_spans
                            })
    t1 = time.time()
    
    # Inclusion-Exclusion over Quotient Poset
    all_orbits = []
    for d in range(r + 1):
        all_orbits.extend(orbits_by_dim[d])
        
    num_total_orbits = len(all_orbits)
    N_orbit = [0] * num_total_orbits

    for i in range(num_total_orbits):
        orb_v = all_orbits[i]
        span_v = orb_v['span']
        K_v = orb_v['K']
        
        sub_sum = 0
        for j in range(i):
            orb_u = all_orbits[j]
            K_u = orb_u['K']
            
            if K_u < K_v:
                count_in_v = sum(1 for s in orb_u['distinct_spans'] if s < span_v)
                if count_in_v > 0:
                    sub_sum += count_in_v * N_orbit[j]
            
        N_orbit[i] = (K_v ** n) - sub_sum

    total_r = sum(all_orbits[i]['orbit_size'] * N_orbit[i] for i in range(num_total_orbits) if all_orbits[i]['basis'].shape[0] == r)
    t2 = time.time()
    
    print(f"Orbit generation: {t1 - t0:.2f} s | Inclusion-Exclusion: {t2 - t1:.2f} s | Total: {t2 - t0:.2f} s")
    return total_r

go(4, 4, solve_rank_orbit_fast) # time: 0.037 sec Résultat: 22560
go(5, 4, solve_rank_orbit_fast) # time: 0.339 sec Résultat: 17760600
go(6, 4, solve_rank_orbit_fast) # time: 7.372 sec Résultat: 5295204600
``
