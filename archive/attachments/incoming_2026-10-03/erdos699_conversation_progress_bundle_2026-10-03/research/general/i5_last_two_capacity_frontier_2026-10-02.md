# Erdős 699: new capacity bounds for the last two i=5 tail supports

2026-10-02 working note. This does **not** solve `i=5`. After the previously verified closeouts, the only maximal-row supports left in the `n >= 10^87` tail are `{0,1}` and `{0,2}`. This note records two exact capacity certificates that sharpen the latter and identify the current hard frontier.

Let `R_s` be the full `p>=5` row factor and `B_{s,u}` the pairwise-coprime cell factors. For a row which is not a maximal row for either small prime 2 or 3, the existing coupled-factor bound gives

\[
R_s\ge \frac{n-s}{60}\ge \frac{n-4}{60}.
\]

## 1. Support `{0,2}`: first new certificate

Use the following integer multiplicities (common denominator 10):

- lines `U=0`, `U-S=0`, `S=1`, `U-S+1=0`, `U=1`, `S=3`, `S=4` with multiplicities `2,2,4,1,1,7,8`;
- the positive-definite conics
  \[
  S^2-3SU+3U^2-S,
  \qquad
  S^2-SU+U^2-4S+3
  \]
  with multiplicities `2,1`.

Every cell in rows `1,3,4` is covered at least 10 times, the row-0 cell 6 times, and every row-2 cell 2 times. The total polynomial degree is 31. For `0<j<=n/2` and `n>=10^87`, every line value has absolute value `<n`, while both conics are positive and `<n^2`. Hence

\[
R_0^6R_2^2R_1^{10}R_3^{10}R_4^{10}<n^{31}.
\]

Using the nonmaximal-row lower bounds and `(n/(n-4))^{30}<2`,

\[
\boxed{R_0^6R_2^2<2\,60^{30}n.}
\tag{1}
\]

Thus `R0=O(n^(1/6))` already follows.

## 2. Support `{0,2}`: second independent certificate

A second rational certificate, scaled by denominator 30, has line multiplicities

\[
6,6,14,4,4,23,24
\]

on the same seven lines, together with four positive-definite conics

\[
\begin{aligned}
&S^2-2SU+3U^2-3S-U+2,\\
&2S^2-4SU+3U^2-4S+U+2,\\
&2S^2-3SU+6U^2-8S-3U+6,\\
&5S^2-9SU+6U^2-11S+3U+6
\end{aligned}
\]

with multiplicities `2,2,1,1`. It covers the row-0 cell 12 times, every row-2 cell at least 8 times, and every cell of rows `1,3,4` at least 30 times. The total degree is 93. Bounding the four conics by `1,2,2,5` times `n^2` gives

\[
\boxed{R_0^{12}R_2^8<80\,60^{90}n^3.}
\tag{2}
\]

In particular

\[
R_0=O(n^{1/6}),\qquad R_2=O(n^{3/8}).
\]

Consequently the complete small-prime power at the row-0 maximal position is `Omega(n^(5/6))`, and the one at row 2 is `Omega(n^(5/8))`, up to fixed explicit factors coming from the other small prime and the possible single factor 5 removed by `5!`.

This is substantially narrower than the earlier general cofactor bound, but it is not yet a contradiction: the remaining equation is still a near `2^e`--`3^f` equation with growing cofactors.

## 3. Support `{0,1}` remains the harder branch

A line-only certificate with denominator 6 covers the row-0 cell 6 times, both row-1 cells 5 times, and every cell in rows `2,3,4` 6 times. Its total degree is 21, yielding

\[
\boxed{R_0^6R_1^5<2\,60^{18}n^3.}
\tag{3}
\]

This matches the previous exponent frontier rather than breaking it. Thus `{0,1}` is currently the harder of the two remaining supports.

## 4. Verification and status

Run

```text
python -X utf8 scripts/audit_i5_last_two_capacity_frontier.py
```

The verifier checks the exact cell coverages, conic definiteness, total degrees, endpoint inequalities, and the displayed constants using integer/rational arithmetic.

Current tail frontier:

\[
\boxed{\{0,1\},\{0,2\}}.
\]

No new index is declared solved in this note.
