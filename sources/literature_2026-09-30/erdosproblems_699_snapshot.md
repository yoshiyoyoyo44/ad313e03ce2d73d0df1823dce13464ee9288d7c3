Fetched 2026-09-30 from https://www.erdosproblems.com/699 using TinyFish fetch.
The source page describes a partial proof. Text extraction below is an excerpt
selected by the fetch provider; it is not a byte-for-byte HTML archive.

This is an exposition of a proof of the conjecture when $j\leq 3i/2$,

provided by GPT 5.6 Sol

(prompted by Liam Price) in a

proof claim

.

Let $v=V\_i(n)$ be the part of $\binom{n}{i}$ supported on primes $\geq i$. This problem is then equivalent to asking whether it is possible for $v$ to be coprime to $\binom{n}{j}$ (for $i<j\leq n/2$).

The main input is a result of Ecklund, Eggleton, Erdős, and Selfridge

[EEES78]

, which proves that (with finitely many explicit exceptions) we have $v> \binom{n}{i}^{1/2}$.

The key observation (presumably a cornerstone of the divisibility of binomial coefficients literature, although I haven't looked at this properly) is that since\[\binom{n}{i}\binom{n-i}{j-i}=\binom{n}{j}\binom{j}{i}\]if $d\mid \binom{n}{i}$ is coprime to $\binom{n}{j}$ then $d\mid \binom{j}{i}$.

Therefore if $v$ is coprime to $\binom{n}{j}$ then by the above $v\mid \binom{j}{i}=\binom{j}{j-i}$, so using

Vandermonde's identity

\[v^2 \leq \binom{j}{j-i}^2<\sum\_{k} \binom{j}{k}\binom{j}{2(j-i)-k}=\binom{2j}{2(j-i)}.\]Therefore, by the

[EEES78]

result above, in any supposed counterexample to this problem we have\[\binom{n}{i}< \binom{2j}{2(j-i)}.\]Note that this immediately implies that there are only finitely many possible 'bad $n$' for fixed $i<j$. Furthermore, if $j\leq \frac{3}{2}i$, we have $2(j-i)\leq i<j\leq n/2$ and so\[ \binom{2j}{2(j-i)}\leq \binom{2j}{i}\leq \binom{n}{i},\]a contradiction.
