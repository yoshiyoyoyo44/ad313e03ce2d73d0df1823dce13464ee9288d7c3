# i=5: all collision maximal-row cases closed in the infinite tail

Working note, 2026-10-02. Combined with `i5_quadratic_capacity_closeout_2026-10-02.md`.

Assume an `i=5` counterexample with `n>=10^87` and suppose the maximal 2-adic and 3-adic rows collide: `r_2=r_3=r`.

For every other row `s!=r`, the 2-part of `n-s` is at most 4 and the 3-part at most 3: any such prime power divides the row difference `|s-r|<=4`. Removing the one denominator factor 5 costs at most another factor 5. Hence

`Q_s >= (n-s)/60 >= (n-4)/60`.

There are four nonmaximal rows, so

`R=prod_{s!=r} Q_s >= (n-4)^4/60^4`.                         (1)

For each `r=0,1,2,3,4` an exact rational dual certificate was found using only lines whose evaluations at `(n,j)` are nonzero throughout `5<j<=n/2`, plus positive-definite quadratic curves. The verifier stores the weights directly and checks every cell in the four nonmaximal rows receives total weight at least 1.

The resulting exponent capacities are:

| collision row r | upper exponent alpha for R | gap 4-alpha |
|---:|---:|---:|
|0|18/5|2/5|
|1|7/2|1/2|
|2|19/6|5/6|
|3|28/9|8/9|
|4|17/6|7/6|

Thus in every case `R=O(n^alpha)` with `alpha<4`, contradicting (1) for all sufficiently large n. The exact integer comparison in the verifier checks that `n=10^87` is already beyond the crude threshold in every row, so the whole unresolved tail is excluded.

All quadratic leading forms are positive definite. The verifier also checks an explicit lower bound on the leading form over `0<=j/n<=1/2`, proving each quadratic value is positive already for `n>=14`; hence no zero-value divisibility loophole occurs.

Therefore

`r_2 != r_3`

in any `i=5` counterexample with `n>=10^87`.

Together with the distinct-row closeout of supports `{0,4}` and `{1,2}`, the only remaining unordered maximal-row supports in the tail are

`{0,1}, {0,2}, {0,3}, {1,3}`.

The existing theorem for `i>=5,n<=10^87` handles the finite side. This note does not yet exclude those final four tail supports and therefore does not claim a complete proof for `i=5`.
