# i=3：J−2 の二次商と一次 E、共有因子次数4以上の全排除

2026-10-04。これは標準桁・完全多項式分配の条件付き結果である。一般の数値反例からこの分配を得る橋は証明していない。

## 1. 仮定と結論

q は奇整数、q≥5 とする。F,J は整数係数の標準 q 進桁多項式で、各係数について

$$
F_0=1,\quad F_1\ge1,\quad 0\le J_k\le F_k<q.
$$

次の整数係数の分解を仮定する。

$$
F-2=(aX-1)E Q,\quad E=1+bX,\quad Q_0=1,
$$

$$
b\ge1,\quad \deg Q=N\ge4,\quad Q_N=s>0,
$$

$$
J-2=(vX^2+uX-h)Q,\quad v>0,\quad h=2-J_0\in\{1,2\},
$$

$$
E\mid J(J-1)\qquad\text{in }\mathbb Z[X].
$$

n=F(q), j=J(q) に対して

$$
4\mid n,\quad 4\le j\le n/2,\quad n-1\mid3j(j-1)
$$

は同時に成立しない。Q の係数非負性は仮定しない。q の素数冪性も使わない。

## 2. 正の D と整数商の恒等式

D=EQ とする。D の最高係数は bs>0。F−2=(aX−1)D の係数を上から戻すと D の全係数は正整数になる。D_1=a−F_1≥1 から a≥2。標準最高桁から

$$
abs<q.
$$

また、全ての係数に

$$
0<D_k<\frac q{a-1}
$$

が成り立つ。最高係数 D_{N+1}<q/a から開始し、

$$
D_{k-1}=\frac{D_k+F_k}{a}<\frac{q/(a-1)+q}{a}
       =\frac q{a-1}
$$

と帰納する。

評価値を

$$
\mathcal Q=Q(q),\quad \mathcal E=1+bq,\quad
P=(aq-1)(bq+1),\quad R=vq^2+uq-h
$$

と書く。D(q)>bs q^{N+1} と E(q)>0 により Q(q)>0 であり、

$$
\mathcal Q>\frac{bsq^{N+1}}{1+bq}>
\frac56s q^N.
$$

n−2=P Q(q), j−2=R Q(q)。j≥4 により R は正整数。半分の範囲から

$$
0<R<P/2.
$$

E(q)|j(j−1) かつ gcd(E(q),n−1)=1 なので、正整数 k が存在して

$$
3j(j-1)=k\mathcal E(n-1).
$$

法 Q(q) を取ると j≡2、n−1≡1 であるから、整数 ℓ により

$$
k\mathcal E=6+\ell\mathcal Q.
$$

E(q)≥6 なので ℓ≥0。展開して

$$
\ell(P\mathcal Q+1)=3R^2\mathcal Q+9R-6P,
$$

$$
(3R^2-\ell P)\mathcal Q=6P+\ell-9R.\tag{1}
$$

ℓ=0 が可能なのは E(q)=6、すなわち q=5,b=1 の場合だけ。この場合 a≤4、P≤114。一方 N≥4 なので Q(q)>(5/6)5^4>500。(1) の ℓ=0 は 3R²Q(q)=6P−9R<684 を要求し、R≥1 に矛盾する。従って ℓ≥1。

R<P/2 と上の ℓ の明示式から

$$
\ell<\frac{3R^2}{P}<\frac{3P}{4}.
$$

V=6P+ℓ−9R とすると

$$
\frac32P<V<\frac{27}{4}P.
$$

T=3R²−ℓP は整数であり、(1) と Q(q)>0、V>0 により T≥1。
従って

$$
\mathcal Q\le V<\frac{27}{4}P
   <\frac{27}{4}\left(q^3+\frac{q^2}{b}\right)
   \le\frac{27}{4}(q^3+q^2).\tag{2}
$$

ここで最後の P の上界には abs<q を使った。

## 3. 無限範囲の排除

N≥5、q≥5 では

$$
\frac56q^N\ge\frac56q^5>
\frac{27}{4}(q^3+q^2)
$$

なので (2) に矛盾する。N=4、q≥9 でも

$$
10q^2\ge81(q+1)
$$

により (5/6)q⁴≥(27/4)(q³+q²)。q=9 の等号でも、Q の下界と (2) が厳密不等号なので矛盾する。

残るのは N=4、q=5,7 のみである。

## 4. 有限末端の完全被覆

N=4 なら D の次数は5、D_0=1、D_5=bs。
a,b,s は a≥2、abs<q で有界。全ての D_k は

$$
1\le D_k\le\left\lfloor\frac{q-1}{a-1}\right\rfloor,
\quad 1\le D_1\le a-1.
$$

最高桁による半分の範囲から 2v≤ab が必要。実際、F−2J の最高係数が負なら、下位の正寄与は各 F_k≤q−1 により q^{N+2}−1 以下であり、負の最高項を補えない。

Q_1=D_1−b、J_1=u−hQ_1 なので

$$
u=hQ_1+J_1,\quad 0\le J_1\le F_1,
\quad 1\le v\le\lfloor ab/2\rfloor.
$$

従って、全整数パラメータと全 D 係数を有限に被覆できる。[独立検算器](../../scripts/audit_i3_quadratic_J2_Elinear_high_degree_2026_10_04.py)は Q の係数を D_k−bQ_{k−1} で正確に復元し、D=EQ、全 F,J 桁支配、J(−1/b)∈{0,1} を有理数で検査する。

| 段階 | 件数 |
|---|---:|
| D の全整数パラメータ行 | 1469 |
| 標準 F | 167 |
| 整数 Q を持つ D | 40 |
| 二次商パラメータ | 254 |
| 標準 J、係数支配 | 103 |
| E の多項式分配 | 6 |
| 半分の添字範囲 | 4 |
| 4 が n を割る | 0 |

六つの分配は全て b=s=v=h=1。(q,a)=(5,2),(7,2),(7,3) のみ。
a=3,q=7 では aq−1=20 により n≡2 (mod 4)。
a=2 の二行では

$$
D=1+X+X^2+2X^3+2X^4+X^5,
$$

q=5,7 の両方で D(q)≡0 (mod 4)、従って n≡2 (mod 4)。
これは第一隣接行の数値整除を使う前に全て排除する。

再生：

```text
python -X utf8 scripts/audit_i3_quadratic_J2_Elinear_high_degree_2026_10_04.py
```

実行結果 exit 0。1469 行の範囲を越える外挿は行っておらず、無限の q,N 範囲は第2–3節の不等式で扱った。

[独立再生](../../scripts/audit_i3_quadratic_J2_Elinear_high_degree_independent.py) は、
Dの係数を先に列挙する方法とは別に、Fの中間桁を列挙して最高桁から整数の桁繰上げを逆算する。
さらにEでの除算も最高次から行う。
標準F 167件、整数Q 40件、多項式分配6件、半分の範囲4件、4|nは0件で一致した。
無限範囲の有理数定数と商の二恒等式も同じ検算器で確認した。
[保存結果](../../data/results/verification_i3_quadratic_J2_Elinear_high_degree_independent.json) は `passed`。

## 5. 残る義務

この結論は complete allocation における二次商・一次 E の N≥4 を閉じる。
N≤3 の一般二次商、正実根因子の高次数、一般数値領域からの complete allocation は本稿では未解決。
