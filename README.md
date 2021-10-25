# Problem

The Pidgeonhole formula states that if you have n+1 birds in n holes, it is impossible for each hole to contain one bird.
We are interested in proofs of unsatisfiability for this formula.

Cook wrote a [paper](https://dl.acm.org/doi/pdf/10.1145/1008335.1008338) in 1976 about this problem.
He gave an encoding of the problem with O(n^3) clauses,
which we can call PHP(n).
Cook gave an extended resolution proof of PHP(n) with O(n^4) steps.
He did so by reducing PHP(n) to PHP(n-1) in O(n^3) steps.
This was a fully explicit extended resolution proof.

# Proposed solution

We hope to find an explicit O(n^3) DRAT (perhaps extended resolution) proof.
By doing so, we hope to find a smaller proof of PHP(100) than is currently known.

Our planned steps:

- Choose a O(n^2) encoding of the pidgeonhole problem (call it PHP'(n)).
- Find a O(n^3) clause reduction from PHP(n) to PHP'(n).
- Find a O(n^2) clause reductino from PHP'(n) to PHP'(n-1).

We also hope to perform some direct solving for the shortest proofs of formulas such as PHP(10) and PHP'(10).

# Cook's formula PHP(n)

Cook has n birds and n-1 holes.
He has n(n-1) variables: p_ij, 1 <= i <= n, 1 <= j <= n-1. i is the index of the bird, j is the index of the hole.
Cook's encoding is as follows:

- OR(p_i1, p_i2, ..., p_i{n-1}), for all 1 <= i <= n.
- OR(not(p_ik), not(p_jk)), for all 1 <= i < j <= n, 1 <= k <= n-1.

The first group of clauses encodes the constraint that each bird is in at least one hole.
The second group of clauses encodes the constrain that no pair of birds can be in the same hole.
There are O(n) clauses in the first group and O(n^3) clauses in the second group.

# An O(n^2) encoding.

One way to encode the second group of clauses more efficiently is as follows.
Greate a new set of variables q_ij, 1 <= i <= n, 1 <= j <= n-1.
q_ij represents whether any bird <= i is in hole j.

To define q_ij, we simply say that q_ij <=> OR(q_{i-1}j, p_ij).

Then, we simply add the constraint that OR(not(q_{i-1}j), not(p_ij)).

Here's all of the clauses in the new encoding

- OR(p_i1, p_i2, ..., p_i{n-1}), for all 1 <= i <= n.
- OR(not(q_ij), q_{i-1}j, p_ij), for all 2 <= i <= n, 1 <= j <= n-1.
- OR(not(q_{i-1}j), q_ij), for all 2 <= i <= n, 1 <= j <= n-1.
- OR(not(p_ij), q_ij), for all 1 <= i <= n, 1 <= j <= n-1.
- OR(not(q_{i-1}j), not(p_ij)), for all 2 <= i <= n, 1 <= j <= n-1.

# Two more O(n^2) encodings

AMO(x1, .. xn)
->

- AMO(x1,x2,x3,y) and AMO(x4, ... not(y))
- AMO(x1,x2,x3,y) and AMO(not(y),x4, ...)
- AMO(x1,x2,y) and AMO(not(y),x3, ...)

# Plan

1. Generate: generate Cook formula

2. Derive each of the O(n^2) encodings from Cook formula (three options above)

3. From a O(n^2) encoding of PHP(n) recursively derive PHP(n-1) encoding.

When I say "derive" I mean write an extension / blocked clause addition-style DRAT proof.

