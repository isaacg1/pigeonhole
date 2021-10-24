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

