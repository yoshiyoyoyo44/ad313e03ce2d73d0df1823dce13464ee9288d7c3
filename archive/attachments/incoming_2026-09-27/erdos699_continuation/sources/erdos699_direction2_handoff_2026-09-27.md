# Erdős Problem 699 — Direction ② Research Handoff

Date: 2026-09-27 JST  
Repository baseline examined: `yoshiyoyoyo44/erdos699`, HEAD `934ccd69f4e4c6cc607215ff5cf4c3660a1071fa` (`Integrate September 26 handoffs and audit i4 support reductions`).

## 0. Scope and status discipline

This note records the work done in the chat after choosing **Direction ②**: attack the remaining fixed indices

\[
5\le i\le34,\qquad i\ne29,
\]

preferably by uniform arguments rather than one-off brute force.

The global repository status at the start of this work was

\[
\boxed{i=1,2,29\text{ and }i\ge35\text{ solved}},
\]

leaving exactly 31 unresolved indices

\[
3\le i\le34,\qquad i\ne29.
\]

This handoff distinguishes:

- **REPO-PROVED**: already proved/audited in GitHub.
- **DERIVED IN THIS CHAT**: mathematical deduction made from repo-proved inputs.
- **COMPUTATIONALLY CHECKED IN THIS CHAT**: exhaustive integer/rational computation reported in this chat, not yet committed to GitHub.
- **WORKING PROOF / PROVISIONAL**: proof chain looks closed internally but must be independently replayed before being promoted to the repository’s proved status.
- **OPEN**: remaining research bottleneck.

The most important new claim is that `i=28,31,34` appear completely closed by a new near-collision argument plus finite verification. This is **not yet part of GitHub HEAD** and should be adversarially replayed before being treated as a repository theorem.

---

# 1. Repo-proved common framework

For a fixed unresolved index `i`, write

\[
A=\binom ni,\qquad m=\pi(i-1).
\]

For each prime `p<i`, choose a row

\[
r_p\in\operatorname*{argmax}_{0\le r<i}v_p(n-r),
\]

set

\[
E_p=\max_{0\le r<i}v_p(n-r),\qquad
n-r_p=a_pp^{E_p},
\]

and let

\[
i_<:=\prod_{p<i}p^{v_p(i)}.
\]

With

\[
h=i-1,\quad b=\left\lceil\frac{2h}{3}\right\rceil,\quad d=3b-h,\quad S=\frac{b(b+1)}2,
\]

the repository’s weighted-cover result gives, for a counterexample,

\[
Q^d\le4^{-S}n^{3S},
\]

where `Q` is the `p>=i` part of `A`.

Combining this with the small-prime valuation bound yields the **cofactor-defect inequality**

\[
\boxed{
\prod_{p<i}a_p\le
\frac{i!}{i_<4^{S/d}}
\left(\frac n{n-i+1}\right)^i n^{\beta_i}
},
\]

where

\[
\boxed{\beta_i=\frac{3S}{d}-(i-m)}.
\]

Repo audit values include

\[
\beta_3=\tfrac14,\qquad \beta_4=1,
\]

and, crucially,

\[
\boxed{\beta_{28}=\beta_{31}=\beta_{34}=0}.
\]

Other useful small-beta values are

\[
\beta_{27}=\frac9{28},\qquad
\beta_{30}=\frac{10}{31},\qquad
\beta_{33}=\frac{11}{34}.
\]

Also

\[
\beta_5=\frac35,\ \beta_{11}=\frac7{11},\ \beta_{17}=\frac{11}{17},\ \beta_{23}=\frac{15}{23},\ \beta_{26}=\frac{17}{26},\ \beta_{32}=\frac{21}{32}.
\]

For all unresolved fixed `i>=5`, repo verification gives

\[
m-\beta_i>1,\qquad \beta_i<2.
\]

If

\[
R=\{r_p:p<i\},\qquad \rho=|R|,
\]

then grouping small primes sharing a maximizing row gives

\[
\boxed{
\prod_{p<i}a_p\ge(n-i+1)^{m-\rho}.
}
\]

Hence sufficiently large counterexamples satisfy

\[
m-\rho\le\beta_i+o(1).
\]

In particular:

- if `beta_i<1`, then all maximizing rows `r_p` must be distinct for sufficiently large `n`;
- since every unresolved `i>=5` has `beta_i<2`, at most one maximizing-row collision survives asymptotically.

---

# 2. Attempts that were ruled out

## 2.1 Arbitrary nonnegative weighted-cover LP

**DERIVED IN THIS CHAT.**

The September 26 proof optimizes over a particular linear family of row/column/diagonal weights. We investigated whether allowing completely arbitrary nonnegative weights could improve the asymptotic exponent and push the solved threshold below `i=35`.

Result: for the asymptotic cover problem, the existing linear family already attains the LP optimum. Thus simply choosing more flexible row/column/diagonal weights does **not** improve the exponent.

Interpretation: the `35` boundary is not merely an artifact of a poor choice inside the same basic three-direction weighted-cover argument.

## 2.2 Adding all lattice lines

The factor-allocation work proves a stronger divisibility fact: for a lattice line

\[
bu-as=c,
\]

the product of all occupied cell factors on that line divides the corresponding integer linear form

\[
bj-an-c.
\]

For `n>=10^87`, the dangerous zero-line case is excluded by the repo’s finite-denominator theorem.

**DERIVED / COMPUTATIONALLY EXPLORED IN THIS CHAT.**

We therefore enlarged the asymptotic LP to include capacities for arbitrary nonzero lattice lines, not only rows/columns/diagonals. This still did not produce a strict exponent improvement for the target indices.

So another purely fractional-cover improvement is unlikely to solve the low indices by itself.

## 2.3 S-part finite-set theorem is not effectively sharp enough

The repo already uses the Bugeaud–Evertse–Győry S-part theorem to show that every fixed unresolved `i>=5` has only finitely many counterexamples.

The sharp exponent form

\[
[P_R(n)]_{S_i}\ll n^{1+\varepsilon\rho}
\]

is ineffective in the constant, so it does not directly produce a usable numerical cutoff. Effective versions are weaker and do not immediately beat the cofactor lower bound strongly enough for a practical all-index closure.

Therefore this route remains useful for abstract finite-ness, but not as the main computationally effective mechanism for Direction ②.

---

# 3. The beta < 1 target block

The indices

\[
\boxed{i\in\{5,11,17,23,26,27,28,30,31,32,33,34\}}
\]

have `beta_i<1`. Thus large hypothetical counterexamples must have all small-prime maximizing rows distinct.

The strongest cluster is

\[
\boxed{i=27,28,30,31,33,34},
\]

with

\[
\beta_{27}=\frac9{28},\quad
\beta_{28}=0,\quad
\beta_{30}=\frac{10}{31},\quad
\beta_{31}=0,\quad
\beta_{33}=\frac{11}{34},\quad
\beta_{34}=0.
\]

This motivates a **multi-prime near-collision** attack on the numbers

\[
n-r_p=a_pp^{E_p},
\]

which all lie in an interval of width at most `i-1`.

---

# 4. Working closure of i = 28, 31, 34

## 4.1 Why beta = 0 is special

For `i=28,31,34`, the cofactor-defect inequality has no positive power of `n`:

\[
\prod_{p<i}a_p
\le
\frac{i!}{i_<4^{S/d}}
\left(\frac n{n-i+1}\right)^i.
\]

For `n>=2,000,000`, the right side is an explicit constant depending only on `i`.

**COMPUTATIONALLY CHECKED IN THIS CHAT.**

The corresponding crude constant bounds reported in the chat were approximately

\[
\prod_{p<28}a_p\le
1,675,329,915,916,204,456,795,278,
\]

\[
\prod_{p<31}a_p\le
502,115,673,338,155,762,729,158,273,745,
\]

\[
\prod_{p<34}a_p\le
210,443,764,161,320,951,755,422,476,589,152.
\]

Sorting the cofactors

\[
a_{(1)}\le a_{(2)}\le a_{(3)}\le\cdots,
\]

the chat derived a common exact-enough bound

\[
\boxed{
a_{(1)}\le933,\qquad
a_{(2)}\le1995,\qquad
a_{(3)}\le5159.
}
\]

These should be regenerated from exact integer inequalities in the final certificate.

## 4.2 Two-way near-collision lemma

For the two smallest cofactors, there are distinct primes `p,q<34` such that

\[
x=ap^e,\qquad y=bq^f,
\]

with

\[
a,b\le1995,\qquad \min(a,b)\le933,
\]

and because both `x` and `y` are numbers `n-r` in the same short interval,

\[
|x-y|\le33.
\]

The intended lemma is

\[
\boxed{
|ap^e-bq^f|\le33
\Longrightarrow
\max(ap^e,bq^f)\le4,209,368,322
}
\]

under the coefficient and prime restrictions above.

### Infinite-exponent reduction

The proof follows the repository’s existing `near_collision_a100` template:

1. absorb cross-prime factors from `a,b` into the exponents;
2. apply Matveev to
   \[
   \Lambda=e\log p-f\log q+\log(a/b);
   \]
3. retain the very coarse exponent bound
   \[
   \max(e,f)<10^{16};
   \]
   the larger coefficient height is still harmless since `log 2156 < 8`;
4. use a Dujella–Pethő style integer-distance reduction.

### New compression of the coefficient verification

Instead of checking millions of coefficient pairs `(a,b)` independently, observe

\[
\mu=\frac{\log(a/b)}{\log q}
=\frac{\log a}{\log q}-\frac{\log b}{\log q}.
\]

For a fixed prime pair `(p,q)` and a chosen convergent denominator `Q`, all coefficient conditions can be reduced to the circular spacing of the points

\[
\left\{
Q\frac{\log a}{\log q}
\right\}\pmod1,
\qquad 1\le a\le1995.
\]

Thus the inhomogeneous reduction can be certified by sorting about 2000 rigorous interval points, rather than iterating over all ordered pairs.

**COMPUTATIONALLY CHECKED IN THIS CHAT.**

For all `55` prime pairs `p<q<34`, a single `P/Q` per prime pair was reportedly found satisfying the needed conditions, including

\[
Q>6\cdot10^{16},
\]

\[
2\cdot10^{16}|Q\tau-P|<1,
\qquad \tau=\frac{\log p}{\log q},
\]

and the full circular-spacing inequalities for all coefficients in the allowed range.

The chat reports that a 256-bit interval implementation passed, followed by an independent 192-bit direct rational-series replay.

The resulting normalized exponent bound was

\[
E,F<128,
\]

and after restoring absorbed cross-prime factors, the original exponents were bounded by

\[
e,f<138.
\]

### Final integer enumeration

With `e,f<138`, exact enumeration over all 55 prime pairs and coefficient bounds gave the maximal close pair

\[
654\cdot19^5=4,209,368,322,
\]

\[
1700\cdot23^5=4,209,368,300,
\]

with difference `22`.

Hence a hypothetical counterexample would satisfy

\[
\boxed{n\le4,209,368,355<2^{32}}.
\]

This is the key bridge from the infinite exponent problem to a finite three-way enumeration.

## 4.3 Three-way near-collision

Since `n<2^32`, all relevant exponents are now absolutely small. Using the third cofactor bound

\[
a_{(3)}\le5159,
\]

we can exactly enumerate triples of distinct prime-power expressions lying in an interval of width at most 33.

**COMPUTATIONALLY CHECKED IN THIS CHAT.**

The maximum reported three-way cluster was

\[
21\cdot2^{20}=22,020,096,
\]

\[
1504\cdot11^4=22,020,064,
\]

\[
4482\cdot17^3=22,020,066,
\]

of width `32`.

Thus any hypothetical counterexample would satisfy

\[
\boxed{n\le22,020,129}.
\]

## 4.4 Finite range

### Small range: n < 2,000,000

The chat reports a complete prime-gap/Kummer-prime-power scan.

Candidate `n` values surviving the immediate prime-gap criterion were:

- `i=28`: `153,278`,
- `i=31`: `115,042`,
- `i=34`: `87,142`.

For each such `n`, all relevant prime-power Kummer conditions

\[
j\bmod p^e\le n\bmod p^e
\]

were intersected over the full interval `i<j<=n/2`.

Reported result:

\[
\boxed{\text{no surviving }(i,n,j)}.
\]

### Middle range: 2,000,000 <= n <= 22,020,129

The chat reports an exhaustive integer scan of the cofactor-product necessary condition.

Reported result:

\[
\boxed{
i=28:0,\qquad i=31:0,\qquad i=34:0
}
\]

surviving `n`.

## 4.5 Current status of these three indices

**WORKING PROOF / PROVISIONAL.**

Combining the two-way near-collision lemma, finite three-way enumeration, and the two finite-range scans gives a complete proof chain for

\[
\boxed{i=28,31,34}.
\]

If independently replayed and committed, the global unresolved count would drop

\[
31\longrightarrow28.
\]

Before promotion to `REPO-PROVED`, recreate and save:

1. an exact cofactor-bound script deriving `933,1995,5159`;
2. a generator for the 55 prime-pair circular-spacing certificates;
3. an independent rational replay of those certificates;
4. an exact `e,f<138` near-collision enumerator;
5. the three-way finite enumerator;
6. the `n<2,000,000` Kummer scan;
7. the `2,000,000<=n<=22,020,129` cofactor scan.

No branch is currently known to be missing, but these computations are not yet present in GitHub and should be adversarially audited.

---

# 5. Next target: i = 27, 30, 33

For these three indices,

\[
\beta_{27}=\frac9{28},\qquad
\beta_{30}=\frac{10}{31},\qquad
\beta_{33}=\frac{11}{34}.
\]

They are the natural next block because `beta` is only about one third.

The obstruction is that the cofactors are no longer absolutely bounded; they grow very slowly with `n`.

The rough consequence is that the smallest cofactor grows like a tiny power:

\[
a_{(1)}\ll n^{1/28}\quad(i=27),
\]

\[
a_{(1)}\ll n^{1/31}\quad(i=30),
\]

\[
a_{(1)}\ll n^{1/34}\quad(i=33).
\]

A direct fixed-coefficient near-collision certificate therefore no longer suffices.

---

# 6. Cell-exponent LP for i = 27, 30, 33

The repository’s factor-allocation framework defines cell factors `B_{s,u}`. For `n>=10^87`, any two distinct occupied cells satisfy

\[
B_{s,u}B_{r,v}\le(i-1)(n-i+1),
\]

because zero determinants have already been excluded.

Passing formally to exponents

\[
B_{s,u}\asymp n^{x_{s,u}},
\]

gives the pair constraint

\[
x_{s,u}+x_{r,v}\le1.
\]

Rows not exceptional for the small primes have large-prime product essentially of order `n`, so their row exponent sum is close to `1`.

**COMPUTATIONALLY EXPLORED IN THIS CHAT.**

For the three target indices, the number of such nearly-full rows is

- `i=27`: `18`,
- `i=30`: `20`,
- `i=33`: `22`.

The row/column/diagonal/pair-capacity LP permits at most exactly

- `18`, `20`, `22`

such rows respectively.

Thus the LP does not yield an immediate contradiction; instead, any large counterexample must lie on an **extremal boundary configuration**.

This is useful structural information: there is essentially no exponent slack.

Adding arbitrary lattice-line capacities was also explored and did not immediately push the optimum below these boundary values.

---

# 7. New structural lemma for distinct maximizing rows

Assume the maximizing rows `r_p` for the small primes are all distinct, as is forced asymptotically when `beta_i<1`.

Take two distinct small primes `p,q<i`. Since `r_q` maximizes the q-adic valuation among all rows,

\[
v_q(n-r_p)\le v_q(n-r_q).
\]

Hence

\[
q^{v_q(n-r_p)}\mid (r_p-r_q).
\]

Therefore the entire `<i`-smooth part of `a_p` divides the lcm of the possible row differences:

\[
\boxed{
[a_p]_{<i}\mid \operatorname{lcm}(1,2,\dots,i-1).
}
\]

Here `[a_p]_{<i}` denotes the part of `a_p` supported on primes `<i`.

This is a concrete strengthening of the abstract S-part viewpoint.

Consequently, once the maximizing rows are distinct, any growth of `a_p` beyond a fixed constant must come from prime factors `>=i`.

Because

\[
\prod_{p<i}a_p\ll_i n^{\beta_i},
\]

the total **large-prime cofactor mass** across these maximizing rows is only `n^{beta_i}`.

For `i=27,30,33`, this is approximately only `n^{1/3}` distributed across 9, 10, 11 distinct maximizing rows respectively.

This appears to be the most promising next bridge: combine

1. distinct maximizing rows,
2. bounded `<i`-smooth cofactor parts,
3. total large-prime cofactor mass `<= n^{beta_i}`,
4. near-collision of the corresponding `p^{E_p}`-dominant numbers,
5. cell/line capacity extremality,

to force either an effective bound on `n` or a rigid impossible configuration.

---

# 8. Recommended next research sequence

### Priority A — independently certify i = 28, 31, 34

Before using them as solved repo inputs, reconstruct the exact scripts/certificates listed in §4.5 and run an adversarial replay.

### Priority B — derive an effective moving-coefficient near-collision lemma

For `i=27,30,33`, target a statement of the form:

> If distinct primes `p,q<i` satisfy
> \[
> |ap^e-bq^f|\le i-1,
> \]
> while the `<i`-smooth parts of `a,b` lie in a fixed finite set and the product of all large-prime cofactor parts is `O(n^{beta_i})`, then `n` is effectively bounded.

A two- or three-prime simultaneous version is likely stronger than treating one ratio at a time.

### Priority C — exploit LP equality structure

The exponent LP is exactly tight for `27,30,33`. Characterize the equality cases. Equality in pair bounds and line capacities should force many occupied cells to have exponent approximately `1/2` and many rows to split in a very rigid pattern. Such patterns may be incompatible with pairwise coprimality or with the integer determinant divisibilities.

### Priority D — matching formulation for maximizing rows

For a concrete `n`, each small prime may have multiple maximizing rows. Treat this as a bipartite matching problem: can one choose pairwise distinct maximizing rows? If not, cofactor collision already contradicts the `beta<1` large-n regime. If yes, minimize the cofactor product over all valid matchings and compare it directly with the cofactor-defect upper bound.

This may give a strong finite verifier once an effective tail bound is established.

---

# 9. Current global picture if the provisional i=28,31,34 proof survives audit

Repository-proved before this handoff:

\[
i=1,2,29\quad\text{and}\quad i\ge35.
\]

Provisional additions from this chat:

\[
\boxed{i=28,31,34}.
\]

Then the unresolved indices would be

\[
\boxed{3\le i\le34,\quad i\notin\{28,29,31,34\}},
\]

exactly 28 indices.

The next concentrated block is

\[
\boxed{i=27,30,33},
\]

followed by the other `beta<1` indices

\[
5,11,17,23,26,32.
\]

`i=3` and `i=4` remain separate low-index hard cores with their own dedicated machinery.

---

# 10. Warnings for the next AI

1. Do not treat the new `i=28,31,34` proof as repository-certified until the certificate/replay code is reconstructed and committed.
2. Do not infer that abstract S-part finite-ness provides a practical explicit bound; the sharp theorem used in the repo is ineffective in its constant.
3. Do not assume arbitrary extra lattice-line weights automatically improve the weighted-cover exponent; exploratory LP work indicates the known bound is already extremal in the relevant fractional formulations.
4. The statement
   \[
   [a_p]_{<i}\mid\operatorname{lcm}(1,\ldots,i-1)
   \]
   requires distinct maximizing rows. Handle possible ties carefully.
5. The pair-cell bound requires the repo’s zero-determinant exclusion threshold (`n>=10^87`) when used uniformly.
6. Keep `p>=i` as the actual Erdős 699 target; do not replace it with `p>i`.

