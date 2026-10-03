# i=5: two maximal-row supports closed by exact line/conic capacity certificates

Working note, 2026-10-02. This is a continuation of the collision-aware maximal-row reduction and the polynomial-capacity method. It proves two of the six distinct-maximal-row supports impossible in the tail `n >= 10^87`. Combined with the repository's verified theorem for `i>=5, n<=10^87`, these two supports are impossible for all `n`. It does **not** solve `i=5` completely.

## 1. Setup

Assume an `i=5` counterexample. Let `r_2,r_3 in {0,...,4}` be chosen maximal valuation rows for 2 and 3. In the distinct-row case the collision-aware row-moment theorem leaves only

`{0,1},{0,2},{0,3},{0,4},{1,2},{1,3}`.

Let `Q` be the `p>=5` part of `binom(n,5)`, `Q_s=gcd(Q,n-s)`, and

`B_{s,u}=gcd(Q_s,j-u)`, `0<=u<=s<=4`.

Kummer gives `Q_s=prod_u B_{s,u}` and the nontrivial cell factors are pairwise coprime.

If `s` is neither maximal row, then for `p=2,3`, `p^{v_p(n-s)}` divides `|s-r_p|` whenever the exponent is nonzero below the chosen maximum; hence the 2-part is at most 4 and the 3-part at most 3. Removing the single denominator factor 5 from `5!` costs at most another factor 5. Therefore

`Q_s >= (n-s)/60 >= (n-4)/60`.

For three nonmaximal rows, with `R=prod Q_s`,

`R >= (n-4)^3/60^3`.                                           (1)

For any integer line `L(S,U)=bU-aS-c` vanishing on cells `Z`, pairwise coprimality gives

`prod_{(s,u) in Z} B_{s,u} | L(n,j)`.

For the lines used below, `L(n,j)` is nonzero throughout `5<j<=n/2`; crudely `|L(n,j)| <= K n` with `K=|a|+|b|+|c|`.

Likewise, for an integer quadratic `F` vanishing on a cell set, the cell product divides `F(n,j)`. Both quadratics below have positive-definite leading form and are positive for the tail; crudely `0<F(n,j)<8n^2`.

## 2. Support {0,4}

Use the following capacities with the displayed rational weights:

- `U=0`, weight `1/2`;
- `U-S=0`, weight `1/2`;
- `U-S+1=0`, weight `1/3`;
- `U-1=0`, weight `1/3`;
- `S-2=0`, weight `1/3`;
- `S-3=0`, weight `1/2`;
- `F_04=S^2-SU+U^2-3S+2=0`, weight `1/6`.

`4AC-B^2=3>0` for `F_04`. Exact cell-by-cell addition shows every cell in rows `1,2,3` has total covering weight at least 1. Hence the product `R=Q_1Q_2Q_3` satisfies, after raising to the sixth power,

`R^6 <= 1327104 n^17`.                                         (2)

Combining (1),(2), and `n-4>=n/2` for `n>=8`,

`n <= 120^18 * 1327104 < 10^44 < 10^87`.

Thus `{r_2,r_3}={0,4}` is impossible in the unresolved tail.

## 3. Support {1,2}

Use:

- `U=0`, weight `1/3`;
- `U-S=0`, weight `1/6`;
- `3U-2S=0`, weight `1/3`;
- `U-1=0`, weight `1/6`;
- `S-3=0`, weight `2/3`;
- `S-4=0`, weight `5/6`;
- `F_12=S^2-2SU+2U^2-S-2U=0`, weight `1/6`.

The line `3U-2S` evaluates to `3j-2n`, which is strictly negative because `j<=n/2`; the other line values are also manifestly nonzero. The leading quadratic form of `F_12` has `4AC-B^2=4>0` and `F_12(n,j)>0` in the tail.

Exact cell-by-cell addition gives coverage at least 1 on every cell in rows `0,3,4`. Thus for `R=Q_0Q_3Q_4`,

`R^6 <= 640000000 n^17`.                                       (3)

Together with (1),

`n <= 120^18 * 640000000 < 10^47 < 10^87`.

Hence `{r_2,r_3}={1,2}` is also impossible in the unresolved tail.

## 4. Current i=5 frontier

The six distinct-row supports are reduced to

`{0,1},{0,2},{0,3},{1,3}`.

A floating-point relaxation using all pair-determined lines also rejected `{1,3}`, but every proof-grade certificate found so far for that support uses at least one line that can vanish at a special ratio such as `j=n/2` or `j=n/4`. It is therefore **not** counted as closed here.

Collision cases `r_2=r_3` also look infeasible in the exponent relaxation, but converting them to a paper proof requires writing the stronger four-heavy-row lower bound with constants. They are not counted as closed in this note.

The attached verifier uses only exact `Fraction` arithmetic for the dual coverage and integer arithmetic for the thresholds.
