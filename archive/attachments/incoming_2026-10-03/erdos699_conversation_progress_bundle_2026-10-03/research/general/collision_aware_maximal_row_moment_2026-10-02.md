# Collision-aware maximal-row moment for all unresolved i >= 5

Working note, 2026-10-02. This extends the September 27 maximal-row moment argument from the distinct-maximal-row cases to possible collisions. It is a research result internal to the current project; no claim of literature novelty or external review is made.

## Setting

Fix an unresolved index `5 <= i <= 33`, excluding `28,29,31`, and suppose a counterexample exists with `n >= 10^87`.
Let

- `h=i-1`, `m=pi(i-1)`, `k=i-m`;
- for each prime `p<i`, `E_p=max_{0<=r<i} v_p(n-r)` and choose a maximal row `r_p`;
- `a_p=(n-r_p)/p^{E_p}` and `P=prod_{p<i} a_p`.

The September 26 cofactor inequality gives, for

`b0=ceil(2h/3)`, `d0=3b0-h`, `S0=b0(b0+1)/2`, `D0=3S0-d0(i-m)`,

`P^{d0} <= ((i-1)!)^{d0}/4^{S0} * (n/(n-h))^{i d0} * n^{D0}`.

Since `n>=10^87`, Bernoulli gives `(n/(n-h))^{i d0}<2`. Exact integer verification shows for every one of the 26 unresolved indices

`2 ((i-1)!)^{d0} n^{D0}/4^{S0} < (n-h)^{2d0}`

at `n=10^87`, and the ratio `(n-h)^{2d0}/n^{D0}` is increasing because `2d0>D0`. Therefore

`P < (n-h)^2`.                                                     (1)

## Theorem 1: at most one collision pair

For a row `r`, let `S_r={p<i:r_p=r}` and `t_r=|S_r|`. Because the prime powers `p^{E_p}` for `p in S_r` are pairwise coprime and their product divides `n-r`,

`prod_{p in S_r} a_p = (n-r)^{t_r}/prod_{p in S_r}p^{E_p} >= (n-r)^{t_r-1} >= (n-h)^{t_r-1}`.

Multiplying over occupied maximal rows gives

`P >= (n-h)^{m-|R|}`, where `R={r_p:p<i}` is the set of distinct maximal rows.

Combining with (1) yields `m-|R|<=1`. Hence:

- no three small primes can share one maximal row;
- two different collision rows cannot occur;
- the maximal rows are either all distinct, or exactly one pair of small primes shares one row.

This conclusion holds for all 26 unresolved indices `i>=5` in the tail `n>=10^87`.

## Theorem 2: collision-aware weighted row moment

Let `Q` be the `p>=i` part of `binom(n,i)` and `Q_s=gcd(Q,n-s)`. For a distinct maximal row `r in R`, put

`A_r = gcd(a_p : r_p=r)`.

Then `Q_r | A_r`. With row weights `w_s=s`, column/diagonal weights

`x_u=max(0,b-u)`, `z_v=max(0,b-v)`, `d=2b`, `S=b(b+1)/2`,

the standard cell argument gives

`Q^d <= 4^{-S} n^{2S} prod_s Q_s^s`.

Writing `T_R=sum_{r in R}r`,

`prod_s Q_s^s <= n^{i(i-1)/2-T_R} prod_{r in R} A_r^r`.

The Legendre lower bound remains

`Q >= i P (n-h)^i/(i! n^m) = P(n-h)^i/((i-1)! n^m)`.

Therefore

`P^d / prod_{r in R} A_r^r
 <= ((i-1)!)^d/4^S * (n/(n-h))^{id} * n^{H_b-T_R}`,

where

`H_b=i(i-1)/2 + 2S - d(i-m)`.

For `b=k-1` or `b=k`, one has the same

`H=i(i-1)/2-k(k-1)`.

Choose `b=k-1` whenever `2b>=h`; for `i=6,8` choose `b=k`. Then `d>=h`, so the left side is at least 1 even with the single allowed collision. Hence if

`C_i = 2 ((i-1)!)^d / 4^S`,

and `q_i` is defined by `N^{q_i} <= C_i < N^{q_i+1}`, `N=10^87`, then

`T_R <= H+q_i`.                                                     (2)

Exact integer arithmetic gives the bounds saved by the verifier.

## Consequence

The September 27 row-moment restriction was used only for `i=27,30,33` after proving distinct maximal rows. The collision-aware form gives an unconditional tail restriction for every unresolved `i>=5`:

1. at most one collision pair among maximal rows;
2. an explicit bound on the sum of the distinct maximal-row positions.

This does not by itself solve any new index. The next step is to combine the reduced row supports with integer prime-power proximity, Kummer digit constraints, and the factor-allocation/nonshared-degree methods developed for `i=3`.
