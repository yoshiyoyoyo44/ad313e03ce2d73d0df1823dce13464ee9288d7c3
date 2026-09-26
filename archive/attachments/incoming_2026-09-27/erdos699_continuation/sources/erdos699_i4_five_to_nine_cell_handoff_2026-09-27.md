# Erdős Problem 699 — i=4 continuation handoff (5-cell elimination through 6–9-cell frontier)

Date: 2026-09-27 JST  
Repository: `yoshiyoyoyo44/erdos699`  
GitHub HEAD checked in this chat: `934ccd69f4e4c6cc607215ff5cf4c3660a1071fa`  
Status: **working research handoff**. This note records both repository-verified inputs and new session-derived arguments. It does **not** claim a complete solution of Problem 699 or of `i=4`.

---

## 0. Problem and repository baseline

The original statement is:

\[
1\le i<j\le n/2,\qquad
\exists p\ge i:\quad p\mid\gcd\!\left(\binom ni,\binom nj\right).
\]

Do not replace `p>=i` by `p>i`.

At GitHub HEAD `934ccd69...`, the repository records

\[
\boxed{i=1,2,29\text{ and }i\ge35}
\]

as solved, leaving

\[
\boxed{3\le i\le34,\quad i\ne29}
\]

unresolved.

For `i=4`, an alleged counterexample has `5<=j<=n/2` and no common prime `p>=5` between `C(n,4)` and `C(n,j)`.

For `s=0,1,2,3`, define

\[
R_s=\frac{n-s}{2^{v_2(n-s)}3^{v_3(n-s)}}
\]

and

\[
B_{s,k}=\gcd(R_s,j-k),\qquad0\le k\le s.
\]

Then in a counterexample

\[
R_s=\prod_{k=0}^s B_{s,k},
\]

all nontrivial cells `B_{s,k}` are pairwise coprime, and the column/diagonal divisibilities hold:

\[
\prod_{s=k}^3B_{s,k}\mid j-k,
\qquad
\prod_{s=v}^3B_{s,s-v}\mid n-j-v.
\]

More generally, for any integer line `bu-as=c` through cells,

\[
\boxed{
\prod_{bu-as=c} B_{s,u}\mid bj-an-c.
}
\]

For `n>=10^87`, the repository's two-position theorem gives

\[
\boxed{B_xB_y\le3(n-3)}
\]

for distinct cells.

The global `i=4` residue classification inherited from the repository is

\[
\boxed{n\bmod36\in\{4,8,9,12,16,18,20,27,28,32\}}.
\]

The five classes `4,8,12,16,32 (mod 36)` transfer to the existing `i=3` machinery. The genuinely `i=4` classes are

\[
\boxed{9,18,20,27,28\pmod{36}}.
\]

The empty `q`-row branch was already eliminated in all five classes in the integrated GitHub note.

---

# 1. New session result A — `n ≡ 28 (mod 36)`: occupied-q five-cell branch eliminated

## 1.1 Repository starting point

For `n≡28 (mod36)`, the `q`-row is row 1 with

\[
q=3^{v_3(n-1)},
\]

while

\[
R_2=\frac{n-2}{2},\qquad R_3=n-3.
\]

A five-cell configuration has exactly one occupied cell in row 1 and two in each of rows 2 and 3.

The GitHub integration reduced the raw 36 supports to 18 supports using simultaneous column/diagonal capacity. For the heavy rows, if the row-2 occupied cells have product `AB` and the row-3 occupied cells product `CD`, then

\[
\boxed{2AB-CD=1}.
\]

## 1.2 Session continuation

The key strengthening is to use **all lattice lines**, not only columns and diagonals:

\[
\prod_{bu-as=c} B_{s,u}\mid bj-an-c.
\]

Applied to the 18 supports, this gives additional simultaneous line-capacity eliminations and reduces the support set to a small number of quotient branches. The remaining branches can be parameterized using the unique row-1 cell `E=R_1` and

\[
n=qE+1,
\]

with `j=aE+k`, `k∈{0,1}` depending on which row-1 position is occupied.

The continuation produces congruences for the normalized row-2 and row-3 products modulo `q`; combining them with the exact relation `2AB-CD=1` leaves two Pell-type terminal branches.

The two terminal mechanisms obtained in the session were:

1. one branch reducing to a Pell equation of shape
   \[
   X^2-3Y^2=-2,
   \]
   together with
   \[
   q\mid Y+3;
   \]

2. one branch reducing to
   \[
   X^2-3Y^2=1,
   \]
   together with
   \[
   q\mid Y+1.
   \]

Writing Pell solutions via powers of `2+sqrt(3)` gives a lower bound on the Pell index of order `q`; meanwhile the pairwise-position bound gives a polynomial-size upper bound on the corresponding Pell coordinate. For `q>=27`, exponential growth wins, giving a contradiction.

### Working conclusion

The session reached the proof structure

\[
\boxed{
 n\ge10^{87},\ n\equiv28\pmod{36},\ i=4\text{ counterexample}
 \Longrightarrow
 \text{at least 6 occupied cells in rows }1,2,3.
}
\]

Equivalently, the five-cell support count was pushed from

\[
36\to18\to0.
\]

### Audit status

This `28 mod 36` closeout was derived in-chat after the checked GitHub HEAD and is **not yet repository-audited** in this note. Before promoting it to a theorem, reconstruct all 18 support branches explicitly and verify the Pell reductions and small-`q` boundaries with a script/certificate.

---

# 2. New session result B — `n ≡ 9 (mod 36)`: 28 remaining five-cell supports eliminated

## 2.1 Setup

For `n≡9 (mod36)`, let

\[
q=2^{v_2(n-1)}=2H,
\qquad
E=R_1=\frac{n-1}{q}.
\]

Thus

\[
n=2HE+1.
\]

If row 1 has its unique occupied cell at `k∈{0,1}`, then

\[
j=aE+k.
\]

The two heavy rows satisfy

\[
R_2=n-2=2HE-1,
\]

\[
R_3=\frac{n-3}{6}=\frac{HE-1}{3}.
\]

If the two row-2 occupied columns form `K_2` and the two row-3 occupied columns form `K_3`, define

\[
D=\prod_{u\in K_2}\bigl(a+2H(k-u)\bigr),
\]

\[
G=\prod_{v\in K_3}\bigl(a+H(k-v)\bigr).
\]

Since `R_2|D` and `R_3|G`, define signed integers

\[
r=\frac{D}{2HE-1},
\qquad
S=\frac{G}{(HE-1)/3}.
\]

Modulo `H`,

\[
r\equiv-a^2\pmod H,
\qquad
S\equiv-3a^2\pmod H.
\]

Hence the key integer relation

\[
\boxed{S-3r=tH,\qquad t\in\mathbb Z.}
\]

This is the main structural reduction for the `9 mod 36` five-cell branch.

The exact heavy-row identity is

\[
\boxed{AB-6CD=1}.
\]

## 2.2 Nonzero `t`

Using the crude support bounds obtained from the factors in `D,G`, the session obtained

\[
|D|\le8H^2,
\qquad
|G|\le6H^2.
\]

Therefore, for `t!=0`,

\[
|t|H
\le
\frac{18H^2}{HE-1}
+
\frac{24H^2}{2HE-1},
\]

which gives

\[
\boxed{E\le29,\qquad1\le|t|\le6.}
\]

Because `E` is coprime to 6,

\[
E\in\{5,7,11,13,17,19,23,25,29\}.
\]

The residue condition `HE≡4 (mod18)` fixes the allowed power-of-two exponent class for `H`.

After support-wise inequalities, only 43 nonzero-`t` branches remain. Modular filtering reduces these branches dramatically; the session reports a chain

\[
43\to22\to7\to4,
\]

with two of the final four killed by low 2-adic congruences.

Two Pell-type branches remain.

### Pell branch 1

One branch leads to

\[
15a^2+60aH-15a-20H^2-6H+2=0.
\]

Its discriminant yields

\[
Y^2-3Z^2=1,
\qquad
Y=40H-6.
\]

Hence

\[
Y\equiv4\pmod5.
\]

But for Pell solutions

\[
Y_m+Z_m\sqrt3=(2+\sqrt3)^m,
\]

the real-coordinate residues modulo 5 cycle through values not containing 4. Thus this branch is impossible.

### Pell branch 2

The last nonzero-`t` branch leads to

\[
21a^2-126aH+3a+56H^2+24H-2=0,
\]

and hence

\[
X^2-57Z^2=-32,
\qquad
X=266H-33.
\]

The session reduced positive solutions under the fundamental unit

\[
151+20\sqrt{57}
\]

to four base orbits

\[
(5,1),\ (14,2),\ (166,22),\ (385,51).
\]

The required solution additionally satisfies

\[
X\equiv5\pmod{19},
\qquad
X\equiv7\pmod8.
\]

The two even-base orbits are excluded immediately. For the odd base orbits, modulo 19 the fundamental unit has real part `151≡-1`, forcing an even orbit exponent to preserve `X≡5 (mod19)`. But the square of the fundamental unit is `1 (mod8)` in the relevant sense, so an even exponent leaves the real part congruent to the base real part (`5` or `1 mod8`), never `7`. Contradiction.

Thus the session closes all `t!=0` branches.

## 2.3 Zero `t`

If `t=0`, then `S=3r`, giving the exact identity

\[
\boxed{
E(2G-D)=\frac{G-D}{H}.
}
\]

Across the 28 supports, sign/size analysis eliminates 26 supports. Two supports remain.

### Zero-`t` support A

For

\[
k=1,\quad K_2=\{0,1\},\quad K_3=\{2,3\},
\]

the equation becomes

\[
Ea^2-8EaH+4EH^2+5a-2H=0.
\]

Writing `z=EH`, the discriminant reduces to

\[
\boxed{(12z-9)^2-3X^2=6.}
\]

Since `H` is even, `z` is even, so

\[
12z-9\equiv15\pmod{24}.
\]

But the positive solutions to

\[
Y^2-3X^2=6
\]

are generated by

\[
(3+\sqrt3)(2+\sqrt3)^m,
\]

whose real coordinate modulo 24 cycles through `3,9,9,3`, never 15. Contradiction.

### Zero-`t` support B

For

\[
k=1,\quad K_2=\{1,2\},\quad K_3=\{0,2\},
\]

one obtains

\[
Ea^2+2EaH-2EH^2-2a+H=0.
\]

Let `z=EH`. Then

\[
X^2=3z^2-3z+1.
\]

With

\[
U=2X,\qquad V=2z-1,
\]

this becomes

\[
U^2-3V^2=1.
\]

Since `V` is odd, write

\[
U+V\sqrt3=(2+\sqrt3)^{2s+1}.
\]

Using Pell half-angle identities

\[
U_{2s+1}+2=2U_sU_{s+1},
\]

\[
V_{2s+1}+1=2U_sV_{s+1},
\]

and the integrality condition inherited from `a`, the session derives

\[
E\mid X+1.
\]

Meanwhile

\[
z=\frac{V+1}{2}=U_sV_{s+1}
\]

and `E` is the odd part of `z`. Coprimality of consecutive Pell factors then forces the odd part of `V_{s+1}` to be 1, i.e.

\[
V_{s+1}\text{ is a power of }2.
\]

For Pell `V_n`, the only powers of 2 are

\[
V_1=1,\qquad V_2=4.
\]

The corresponding small cases give either `z=1` (contradicting `H>=2`) or `E=1` (contradicting an occupied row-1 large-prime factor). Thus this branch is also impossible.

## 2.4 Working conclusion for `9 mod 36`

The session therefore reaches

\[
\boxed{
 n\ge10^{87},\ n\equiv9\pmod{36},\ i=4\text{ counterexample}
 \Longrightarrow
 \text{at least 6 occupied cells in rows }1,2,3.
}
\]

Thus the support count is pushed

\[
\boxed{36\to28\to0}
\]

for the five-cell branch.

### Audit status

This derivation is substantially more explicit than the `28 mod 36` outline above, but it is still **session-derived and not yet independently certificate-audited**. A formal continuation should regenerate all 28 supports, verify the 43 nonzero-`t` branches and all modular eliminations, and independently confirm the Pell orbit assertions.

---

# 3. New session result C — exact 6 occupied cells: a universal obstruction except one hexagonal support, then eliminate the hexagon

This section assumes an `i=4` counterexample with `n>=10^87` and **exactly 6 occupied cells** among rows 1,2,3.

The session pursued a weighted-cover linear program using the divisibilities along all lattice lines

\[
\prod_{bu-as=c}B_{s,u}\mid bj-an-c.
\]

For almost all six-cell supports, the line capacities force the `q`-row product to be at most a constant times `sqrt(n)`.

## 3.1 Exceptional six-cell support

The unique support where the ordinary weighted line cover does not directly produce the desired exponent gap is

\[
\boxed{
S_*=\{(1,0),(1,1),(2,0),(2,2),(3,1),(3,2)\}.
}
\]

These six lattice points lie on the quadratic

\[
\boxed{
F(s,k)=s^2-sk+k^2-3s+2=0.
}
\]

Indeed, `F` vanishes at all six points.

For each occupied cell, because

\[
n\equiv s\pmod{B_{s,k}},
\qquad
j\equiv k\pmod{B_{s,k}},
\]

we obtain

\[
B_{s,k}\mid F(n,j).
\]

The six cell factors are pairwise coprime, so

\[
\boxed{
R_1R_2R_3\mid n^2-nj+j^2-3n+2.
}
\]

For `j<=n/2`,

\[
0<n^2-nj+j^2-3n+2<n^2
\]

in the large range. Therefore

\[
\boxed{R_1R_2R_3<n^2.}
\]

But in each of the five genuine residue classes, `R_1R_2R_3` is approximately `n^3/q`, while the fact that the `q`-row itself has two occupied cells implies its large-prime part is at least `25`, hence an upper bound on `q` of order `n/25` (or stronger). Combining with the divisibility above forces an incompatible lower bound on `q`.

The relevant row products are:

\[
\begin{array}{c|c}
 n\bmod36 & R_1R_2R_3\\ \hline
9 & \dfrac{(n-1)(n-2)(n-3)}{6q}\\[2mm]
28 & \dfrac{(n-1)(n-2)(n-3)}{2q}\\[2mm]
18 & \dfrac{(n-1)(n-2)(n-3)}{3q}\\[2mm]
20 & \dfrac{(n-1)(n-2)(n-3)}{2q}\\[2mm]
27 & \dfrac{(n-1)(n-2)(n-3)}{6q}
\end{array}
\]

The `q`-row two-cell lower bound gives, respectively, upper bounds of the shape

\[
q\le\frac{n-r}{25}
\]

or stronger (for the row normalization in the class). These contradict the lower bound obtained from `R_1R_2R_3<n^2`.

Hence

\[
\boxed{S_*\text{ is impossible in all five genuine residue classes}.}
\]

## 3.2 All other six-cell supports

For every other six-cell support, the weighted-cover search reported a rational line-cover certificate with total line weight at most 4. Combining this with the two non-`q` row lower bounds

\[
R_s\ge\frac{n-3}{6} > \frac n7
\]

in the large range gives an upper bound of the form

\[
\boxed{R_q\le 5^4 7^4\sqrt n}
\]

for the `q`-row large-prime part.

Since

\[
5^4 7^4=1,500,625,
\]

this is

\[
R_q\le1,500,625\sqrt n.
\]

Writing the `q`-row relation as

\[
n-r=cqR_q,
\qquad c\le3,
\]

and using `n-r>n/2` for the large range gives

\[
\boxed{
q>\frac{\sqrt n}{9,003,750}.
}
\]

At `n>=10^87`, this means `q` is already larger than roughly `3*10^36`.

Consequently, for `q=2^e` one needs roughly

\[
e\ge122,
\]

and for `q=3^e` roughly

\[
e\ge77.
\]

### Interpretation

The exact-six-cell branch is not yet globally contradicted by this inequality alone, but it is forced into a **near-pure-small-prime-power regime**:

\[
q\gg\sqrt n.
\]

That is a strong structural reduction.

### Audit status

The quadratic `S_*` argument is symbolic and should be easy to re-check independently. The claim that **every other six-cell support** admits the stated weighted rational cover needs a saved support/certificate enumeration before promotion to a repository theorem. The constant `1,500,625` should be regenerated from that certificate, not trusted merely from this handoff.

---

# 4. Preliminary new observation — 7, 8, 9 occupied cells

The session then started extending the weighted-cover LP to supports of size 7, 8 and 9.

The important preliminary pattern was:

> Every support for which the ordinary weighted line-cover LP remained weak appeared to contain the six-point hexagonal support `S_*`.

Thus the apparent exceptional family is not arbitrary: the obstruction seems organized around the same quadratic curve

\[
F(s,k)=s^2-sk+k^2-3s+2.
\]

This suggests treating all `S_*`-containing 7–9-cell supports by combining

\[
R(S_*)\mid F(n,j)
\]

with one, two or three additional cell divisibilities coming from independent lattice lines.

### Important caution

This 7–9-cell classification was only a **preliminary in-chat LP observation** when the user requested this save. A complete enumeration and certificate was not finished in the conversation. Do not cite “all weak 7–9 supports contain `S_*`” as proved until a script enumerates every support and records the optimal/feasible line weights.

---

# 5. Current research frontier after this handoff

If the five-cell closeouts above survive audit, then for `n>=10^87` all five genuine residue classes

\[
9,18,20,27,28\pmod{36}
\]

are forced to have at least six occupied cells (with the caveat that GitHub's `18,20,27` occupied-q five-cell elimination itself still contains omitted reductions that should be reconstructed independently).

The immediate tasks are therefore:

1. **Audit `28 mod 36` five-cell closeout.**  
   Regenerate all 18 supports and certify every quotient/Pell branch.

2. **Audit `9 mod 36` five-cell closeout.**  
   Regenerate all 28 supports, the 43 nonzero-`t` branches, modular reductions and the two `t=0` branches.

3. **Make the exact-six weighted-cover claim reproducible.**  
   Enumerate all six-cell supports, identify `S_*` as the unique exceptional support, and save rational weights/certificates for all others.

4. **Verify the quadratic support lemma exactly.**  
   Check that `F(s,k)` vanishes precisely on `S_*` within the triangular grid and verify the residue-class-specific `q` contradiction with explicit inequalities valid already at `n>=10^87`.

5. **Finish 7–9 occupied cells.**  
   Exhaustively classify supports, confirm whether every LP-weak support contains `S_*`, and exploit `F(n,j)` together with the added cells to derive a stronger bound or contradiction.

6. **Only after the large-`n` branch closes**, return to the finite region `n<10^87` using the existing certificate infrastructure.

7. Remember that the transferred residue classes `4,8,12,16,32 mod36` still depend on the unresolved `i=3` problem; an `i=4` large-`n` closeout of the five genuine classes alone does not solve all of `i=4` unless the transfer branch is also handled.

---

# 6. Trust / provenance table

| Item | Status at save time |
|---|---|
| GitHub HEAD `934ccd69...` baseline | Checked in chat via GitHub connector |
| `i=4` definitions, residue classes, empty q-row elimination, two-position theorem | Repository-backed |
| `18,20,27 mod36` >=6-cell conclusion | Present as source-report in GitHub; some occupied-q branch reductions omitted from independent audit |
| `28 mod36` five-cell elimination | New session-derived proof structure; not independently scripted yet |
| `9 mod36` 28->0 five-cell elimination | New session-derived detailed proof structure; not independently scripted yet |
| six-cell exceptional support `S_*` and quadratic `F` | New session-derived symbolic argument; should be independently checked |
| all other six-cell supports have weighted cover and `R_q <= 1,500,625 sqrt(n)` | New session-derived computational claim; certificate still needed |
| all weak 7–9-cell supports contain `S_*` | Preliminary only; enumeration not completed at save time |

---

# 7. Suggested prompt for the next AI

> Continue Erdős Problem 699 at `i=4` from `erdos699_i4_five_to_nine_cell_handoff_2026-09-27.md` and GitHub HEAD `934ccd69f4e4c6cc607215ff5cf4c3660a1071fa`. First audit the new claims rather than trusting them: (1) regenerate the 28-mod-36 18-support closeout; (2) regenerate the 9-mod-36 28-support closeout, including `S-3r=tH`, the 43 nonzero-t branches and the Pell terminal cases; (3) enumerate every exact-six support and verify that the only weighted-cover exception is `S_*={(1,0),(1,1),(2,0),(2,2),(3,1),(3,2)}`, then certify the quadratic `F(s,k)=s^2-sk+k^2-3s+2` obstruction; (4) continue to 7–9 occupied cells and test whether every LP-weak support contains `S_*`. Produce scripts/JSON certificates and exact symbolic proofs. Do not claim `i=4` solved unless all residue-transfer and finite-range issues are closed.

---

## Final checkpoint

The strongest **working** picture at save time is:

\[
\boxed{
\begin{array}{c}
9\pmod{36}:\text{ five-cell branch }28\to0,\\
28\pmod{36}:\text{ five-cell branch }18\to0,\\
\text{exact six cells}:\text{ one hexagonal support }S_*\text{ is killed by a quadratic curve,}\\
\text{all other six-cell supports force }q\gg\sqrt n.
\end{array}}
\]

The next real bottleneck is the complete, reproducible treatment of 7–9 occupied cells and independent auditing of the new five-/six-cell claims.
