# Independent audit of the G(19,14) bound and the (3,11) anchor

The audited source is
[bft_new_gcd_19_14_and_3_11_anchor_2026-10-04.md](bft_new_gcd_19_14_and_3_11_anchor_2026-10-04.md).
The conclusion is valid as scoped there: every integer m>6000 and
delta=0,1 satisfies G(19,14,14m-delta)>(361/250)^(14m), and BFT
Theorem 2.4 yields exponent .344 for the (3,11) pair at
min(values)>=exp(999999). This audit does not claim the whole Erdős
problem is solved.

The common endpoints and the disjointness input were checked
mathematically. Set h=33. For every t with {14t/33}>1/2,

```math
2\lfloor14t/33\rfloor+\lfloor5t/33\rfloor=t-2.
```

BFT (5.8) applies at m>=2t. For either delta the actual upper endpoint
is at least (33m-2)/t. The two actual lower endpoints have slopes
14/(floor(14t/33)+1) and 5/(floor(5t/33)+1); their constant terms are
respectively -delta/(floor(14t/33)+1) and
(delta-1)/(floor(5t/33)+1), both nonpositive. Therefore the larger
of these two slopes times m is a safe common lower endpoint.
The source intervals are disjoint, and shrinking them preserves this
property. The finite t<=512 list and analytic t<=128 list are valid.

The finite checker was fully rerun, covering every integer
6001 through 4000000 with 12693 consecutive blocks. It reproduced
the same minimum normalized margin

```math
\frac{951921554421}{649278796070912}>0
```

on [10793,10798]. The whole Eratosthenes sieve, every prime logarithm,
and all block inequalities were rerun; the replay took about 14.6
seconds. This audit also checked the logarithm kernel in the source.
The mantissa grid divides an exactly normalized prime into g/1024
and 1+t, with 0<=t<1/1024. At scale 2^32, the Taylor remainder
2^32*t^3/3 is less than two integer units, because
2^32<6*1024^3. The lower and upper quadratic terms use opposite
outward bounds on t. The 64-bit grid bounds are rounded outward to
32-bit bounds before accumulation. Prefix lower(right)-upper(left)
is a valid lower interval sum. If this lower enclosure is negative,
replacing it by zero remains valid for the nonnegative sum.

Both analytic inequalities were independently recomputed using
direct exact fractions, square roots enclosed by integer roots at
decimal scale 10^30, and a direct 40-term atanh logarithm series.
This uses a different arithmetic scheme from the source's 128-bit
interval class. The first margin above log(361/250) is greater than
0.000471959722; the second is greater than 0.002475382439.
The first formula decreases its error terms with m throughout
[4000000,2000000000]. All endpoints lie in the required theta
square-root domain. Above the switch all endpoints are at least
10^8; the relative-error formula increases with m and has no upper
cutoff. Thus finite verification has not been extrapolated to the
unbounded interval.

The common exact Theorem 2.4 kernel was also rerun with
a=1,p=3,k0=5,b=2,q=11,l0=2,c=19,d=14,
L1=361/250,m0=6000,epsilon=3/20000. It certified

```math
\Omega_3>1.001496227521>1,
\Omega_4>50.016762544380>1,
\lambda_3>0.344178760242,
\lambda_3-\epsilon>43/125=0.344,
\log x_0<955006.234534113501<999999.
```

Both delta-dependent prefactors and all threshold terms are retained.
The seed has positive difference 3^5-2*11^2=1. The primary source
is [Bennett, Filaseta and Trifonov](https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf);
the repeated x1 in Theorem 2.4's last display is interpreted using
the Section 7 proof's explicitly defined minimum. The result adds
no cofactors-coprimality hypothesis.

[Independent checker](../../scripts/audit_bft_gcd_19_14_independent_2026_10_04.py)
and [saved result](../../data/results/verification_bft_gcd_19_14_independent_2026_10_04.json)
retain the complete finite replay's exact output, separate analytic
arithmetic, source audit and anchor check. BFT Lemmas 5.2 and 5.4
and Theorem 2.4 remain external inputs.
