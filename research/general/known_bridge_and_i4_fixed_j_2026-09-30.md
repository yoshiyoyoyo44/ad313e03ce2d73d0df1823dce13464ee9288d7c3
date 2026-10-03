# 外部文献の接続と i=4 の有限 j・全 n 領域

2026年9月30日。基点 `cf00db1`。
[現在地](../../docs/STATUS.md) · [証明書](../../data/certificates/known_bridge_and_i4_fixed_j_2026-09-30.json) · [独立再生](../../scripts/replay_i4_fixed_j.py)
問題699全体、あるいは i=4 全体の完全解決ではない。

## 1. 今回の検算済み補助定理

**定理。** 全ての整数 $n,j$ について、

$$
5\le j\le\min(1000,n/2)
\quad\Longrightarrow\quad
\exists p\ge5:\ p\mid\gcd\left(\binom n4,\binom nj\right).
$$

有限な j の領域を、n の上限なしで扱う。無限尾部の証明は以下の
初等的な Legendre 付値評価で閉じ、EEES78 の定理には依存しない。
文献全体に対する新規性は主張しない。

### 紙上還元

$A=\binom n4$ とし、$Q_4(n)$ を A の 5 以上の素数部分とする。
反例なら $\gcd(Q_4(n),\binom nj)=1$。

$$
\binom n4\binom{n-4}{j-4}=\binom nj\binom j4
$$

より $Q_4(n)\mid\binom j4$、従って
$Q_4(n)\mid Q_4(j)$ が必要である。

Legendre の差の式では、$v_2\binom n4$ の $2^1,2^2$ 層は
$2^e\mid4$ のため0。他の層は高々1で、$p^e>n$ の層は0である。
$n\ge10$ だから

$$
2^{v_2(A)}\le n/4,\qquad 3^{v_3(A)}\le n.
$$

従って

$$
Q_4(n)\ge\frac{4A}{n^2}
=\frac{(n-1)(n-2)(n-3)}{6n}.\tag{1}
$$

$5\le j\le1000$ の Q 値を厳密に計算すると

$$
M:=\max Q_4(j)=41086285255.
$$

式(1)の右辺は $n>3$ で増加する。
実際 $(n-1)(n-2)(1-3/n)/6$ は正の増加因子の積である。

$$
\begin{aligned}
496508\cdot496507\cdot496506
&=122398508954739336,\\
6\cdot496509\cdot M
&=122398262434048770.
\end{aligned}
$$

前者が後者より大きいので、反例は必ず $10\le n\le496508$ にある。
この有限化は EEES78 を使わず、n の大きい所でも有効である。

### 有限部の完全被覆

各 $j=5,\ldots,1000$ の $Q_4(j)$ を完全因数分解し、全約数を列挙した。
重複込み 53,072 約数、1を除く異なる約数は22,050個。
これを、約数 d と $d\mid Q_4(j)$ を満たす全 j の辞書にする。
式(1)の右辺は $n=10$ ですでに $42/5>1$ となり単調増加するため、$Q_4(n)=1$ の場合はなく、辞書から約数1を除いてよい。

$n=10,\ldots,496508$ の496,499整数の $Q_4(n)$ を辞書と照合し、
$j\le n/2$ を満たす全候補を取り出す。得られるのは

$$
(n,j)=(57,22),\qquad Q_4(57)=7315
$$

の1件だけ。この場合

$$
\gcd\left(\binom{57}{4},\binom{57}{22}\right)=35910
$$

は素数5を共有する。これで有限部も閉じる。

この1件は橋渡し条件の不十分性も示す。
$57\bmod5\ge22\bmod5$ だが $57\bmod25=7<22=22\bmod25$。
素数5の上位 Kummer 層に共通素因数が現れ、
$Q_4(n)\mid Q_4(j)$ 自体は反例の十分条件ではない。

## 2. 公的な既知部分結果との接続

[問題699の公的ページ](https://www.erdosproblems.com/699)には、
GPT 5.6 Sol の proof claim を Thomas Bloom が説明する
$j\le3i/2$ の部分証明が載る。これは完全解決とされていない。
[上流の Lean 定式化](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/699.lean)
も本問題を `research open` と分類する。

一次文献は E. F. Ecklund Jr., R. B. Eggleton, P. Erdős, J. L. Selfridge,
*On the prime factorization of binomial coefficients*, J. Austral. Math. Soc.
(Series A) **26** (1978), 257–269。
[一次PDF](https://users.renyi.hu/~p_erdos/1978-31.pdf) p.258を画像でも確認した。

この論文の大素数部分 v は **p≥i** によって定義され、$n\ge2i$ において
$v>\sqrt{\binom ni}$ が、次の12組を除いて成立する。

$$
\begin{gathered}
(8,3),(9,4),(10,5),(12,5),(21,7),(21,8),\\
(30,7),(33,13),(33,14),(36,13),(36,17),(56,13).
\end{gathered}
$$

原文は $u>v$ の例外として列挙する。$u,v$ は互いに素であり、
$\binom ni>1$ なので、例外外では $u=v$ も不可能である。
全12組に対し許される全 j を列挙した41件を、
直接の `math.comb`、gcd、素数試し割りで確認し、全て p≥i の共通素数を得た。
2組は許される j がない。

一般の反例では $v\mid\binom ji=\binom j{j-i}$。
Vandermonde から

$$
v^2\le\binom j{j-i}^2<\binom{2j}{2(j-i)}.
$$

$j\le3i/2$ なら $2(j-i)\le i<j$ なので、
右辺 $\le\binom{2j}{i}\le\binom ni<v^2$、矛盾する。
上の41件の例外監査を合わせると既知の部分領域を例外漏れなく取り込める。

厳密な条件 $\binom ji^2<\binom{2j}i$ はこの部分領域を少し伸ばす。
$i=3,\ldots,34$ の連続上端 j を証明書にも保存した。
i=3では5、i=4では6、i=5では8、i=34では52。
この伸長は公的フォーラムで既に言及されている J1 と同じで、
新しい文献定理としては数えない。

## 3. 橋渡し恒等式の位置づけ

一般に A=$\binom ni$、B=$\binom nj$、D=gcd(A,B) とすると

$$
\frac AD\mid\binom ji,\qquad
\frac AD\mid\binom{n-j}i.
$$

第一の整除性は上記の恒等式、第二は

$$
\binom ni\binom{n-i}j=\binom nj\binom{n-j}i
$$

による。反例の大素数部分 Q に対しても両方の整除性がある。
ただし、これらは既存 `sources/source_progress.md` §2 の
軌道恒等式(2.1)の h=0 と h=i であり、新規の拘束ではない。
12,826組の小範囲整数で代数恒等式と整除性を診断した。

公的フォーラムの [post-8092](https://www.erdosproblems.com/forum/thread/699#post-8092)
には小素数部分 $\le n^{\pi(i-1)}$ と prime gap による有限 j 上端の
別の部分領域が既に掲載されている。これは投稿者による機械生成・検算報告であり、
本調査ではその大きい prime gap データや漸近量まで再認証していない。
リポジトリの三方向の重み、全桁 Kummer、余因子の拘束を代替するものでもない。

## 4. 再生と保存した根拠

```sh
python scripts/audit_known_bridge_and_i4_fixed_j.py
python scripts/replay_i4_fixed_j.py
```

標準Pythonだけで動く。第二の検証器は n の走査で `comb` の大素数部分を使わず、
四つの分子因子の2・3を除く積を計算する。
j の全約数も、素数篩と素数冪群の直積により別経路で再構成する。
両実装で有限候補集合、境界の整数比較、全約数数、共通素数が一致した。
数学的な無限尾部の根拠は(1)の紙上証明であり、有限診断との区別は維持する。

- [証明書](../../data/certificates/known_bridge_and_i4_fixed_j_2026-09-30.json): 12例外の41共通素数、
  既知小j上端、有限j証明書、原文PDF SHA-256。
- [再生結果](../../data/results/verification_i4_fixed_j.json): 別実装の完全再生結果。
- [EEES78原文PDF](../../sources/literature_2026-09-30/1978-31.pdf)、[抽出文](../../sources/literature_2026-09-30/1978-31.txt)。p258は画像でも監査した。
- [原問題文PDF](../../sources/literature_2026-09-30/1978-46.pdf)、[抽出文](../../sources/literature_2026-09-30/1978-46.txt): Erdős–Szekeresの原問題文、Gazette 5 (1978), 97–99。
- [公的ページの保存本文](../../sources/literature_2026-09-30/erdosproblems_699_snapshot.md): 公的部分証明の取得本文。
- [フォーラムの保存本文](../../sources/literature_2026-09-30/forum_8092_snapshot.md): フォーラムの抽出された1投稿。
- [上流の保存定式化](../../sources/literature_2026-09-30/upstream_699.lean): 取得時点の上流定式化。`sorry` を含む定式化であり、
  問題のLean証明ではない。

PDFバイト列のSHA-256:

| 原文 | SHA-256 |
|---|---|
| 1978-31.pdf | a9c060afbd03a56db5c0ccc9432e0a03ff30a75e6fca0e3ebaea85bee47a768d |
| 1978-46.pdf | da8bfddd328fa01605cba4c751a7bf9fe07c4fa31bd6cf519fd32c5707ed302b |

独立査読、一般 i=4 の閉鎖、問題699全体の完全解決は未達。
