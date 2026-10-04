# New universal G(4,3) bound and an explicit (7,13) pair estimate

This note proves a new input to BFT Theorem 2.4. It does not by itself
close i=16 or the original Erdős problem. The external source is Bennett,
Filaseta and Trifonov, [On the factorization of consecutive integers](https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf),
Proposition 5.3, Lemma 5.4, Theorem 2.4 and its Section 7 proof.

## 1. Universal gcd bound

For every integer m>30000 and either delta=0 or delta=1,

```math
G(4,3,3m-\delta)>(361/250)^{3m}.
```

The proof covers every m. The finite certificate extends to 4000000;
the remainder uses inequalities valid on complete real intervals.

For w>=0, use the three pairs (r,a)=(2,1),(4,2),(6,3), and put

```math
U_{w,r}(m)=\frac{7m-2}{7w+r},
\qquad
V_{w,a}(m)=\frac{3m}{3w+a}.
```

BFT Proposition 5.3 supplies all primes in these intervals (V,U] as
divisors of G, for either delta, whenever m>=2(7w+r). To check the
subsets explicitly, the residues of t=7w+r correspond to j=6,5,4.
For delta=0 all three lie in the first source set. For delta=1, r=2,4
are in that set and its lower endpoint is (3m-1)/(3w+a), which is at
most V. For delta=1,r=6 the second source set gives lower endpoint
m/(w+1)=V. The common upper endpoint is (7m-2)/(7w+r).
The source intervals are disjoint; passing to these smaller intervals
preserves disjointness. Thus

```math
\log G(4,3,3m-\delta)
\geq \sum_{w=0}^{K-1}\sum_{(r,a)}
       \bigl(\theta(U_{w,r}(m))-\theta(V_{w,a}(m))\bigr).
```

Empty intervals contribute zero. Every finite certificate uses only
actual primes strictly above the lower endpoint and at most the upper
endpoint.

### Finite part

Take K=64. The condition m>=2t follows from m>=30001 and t<=447.
For a block [l,u], keep only primes in

```math
\left(\frac{3u}{3w+a},\frac{7l-2}{7w+r}\right].
```

They occur in the valid interval for every m in the block. Exact
outward bounds on prime logarithms give a lower bound H(l,u). The
checker verifies

```math
H(l,u)>3u\log(361/250)
```

on every block. Blocks start at l=30001, end at
u=min(4000000,l+max(1,floor(l/2000))), and the next block starts at u+1.
There are 9723 blocks, covering all integers 30001 through 4000000.
The sieve includes every prime through 13999999, totaling 910077 primes.
The smallest normalized certified margin is

```math
\frac{9917169792729158649521}
     {1375481471856152716247040}>0
```

on [49686,49710]. All logarithm operations use integer outward
rounding at scale 2^64. A 4096-point mantissa table uses 32 atanh
terms; a three-term correction has residual less than one scale unit.
The checker bounds all series residuals by rational inequalities.
It does not use floating point logarithms.

### Analytic part

Take K=20 and define, for each w and (r,a),

```math
\alpha=\frac7{7w+r},\quad
\beta=\frac3{3w+a},\quad
\nu=\frac2{7w+r},\quad
U=\alpha m-\nu,\quad V=\beta m.
```

For 4000000<=m<=20000000000 all endpoints lie in the domain of the
square-root theta inequalities in BFT Lemma 5.4. Therefore

```math
\frac{\log G}{3m}\ge
\frac13\sum(\alpha-\beta)
-\frac{\sum\nu}{3m}
-\frac{2.072\sum\sqrt\alpha}{3\sqrt m}.
```

The right side increases with m. At m=4000000 its strict excess above
log(361/250) is greater than 0.001665969246, certified by rational
intervals. The largest endpoint is below 10^11.

For m>=20000000000 every endpoint is at least 10^8. With
eta=213/1000000, the relative bounds in the same lemma give

```math
\frac{\log G}{3m}\ge
\frac13\sum\bigl((1-\eta)\alpha-(1+\eta)\beta\bigr)
-\frac{(1-\eta)\sum\nu}{3m}.
```

This right side also increases with m. At the starting point its
strict excess above log(361/250) is greater than 0.008199883739.
There is no upper cutoff in this second estimate. Both estimates
and all endpoint conditions are checked with outward rational
intervals at scale 2^128.

## 2. The explicit pair estimate

Use the seed

```math
7^3-2\cdot13^2=5,\qquad
s=4/3,\quad L_1=361/250,\quad m_0=30000.
```

Theorem 2.4 requires both Omega3>1 and Omega4>1. The exact interval
checker obtains

```math
1.000399724406<\Omega_3<1.000399724407,
2.968316291644<\Omega_4<2.968316291645,
0.122637465094<\lambda_3<0.122637465095.
```

With epsilon=1/10000, lambda3-epsilon>49/400=0.1225. The formula for
the theorem's threshold, including both delta-dependent constants,
gives

```math
798473.808386715939<\log x_0<798473.808386715940<999999.
```

For the constants C_{1,delta},C_{2,delta}, the factor from the source
is (s^2-1)^{(-1)^delta/2}; in particular the delta=0 factor is a
positive square root. The checker uses this factor for both deltas,
exact polynomial integrals, and the coarse valid enclosure 3<pi<4.

Consequently, for any positive integer cofactors x1,x2 and nonnegative
integer exponents k,l, if

```math
|7^k x_1-13^l x_2|\le100,\qquad
Z=\min(7^k x_1,13^l x_2)\ge\exp(999999),
```

then

```math
\max(x_1,x_2)>Z^{49/400}.
```

The Section 7 proof defines x as the minimum of the two values.
This resolves the repeated x1 typographical error in the last display
of Theorem 2.4. No extra coprimality condition on the cofactors is used.

## 3. Reproduction and scope

Run the three scripts in order:

1. scripts/audit_bft_gcd_4_3_finite_blocks_2026_10_04.py
2. scripts/audit_bft_gcd_4_3_universal_2026_10_04.py
3. scripts/audit_bft_gcd_4_3_anchor_7_13_2026_10_04.py

Their corresponding data/results/verification_bft_gcd_4_3_*.json
files retain the finite block, analytic interval and anchor results.
The analytic part has been independently reviewed by global_audit.
The finite part and pair certificate remain available for independent
replay. The new (7,13) edge can enter a full pair graph argument,
but this note makes no full-index or full-problem conclusion.
