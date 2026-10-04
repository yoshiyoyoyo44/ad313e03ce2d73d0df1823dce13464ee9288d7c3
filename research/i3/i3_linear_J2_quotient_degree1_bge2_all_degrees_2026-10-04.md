# E一次・b>=2の線形J−2商を全次数で閉じる

2026-10-04。この稿は指定の標準桁・多項式分配を閉じる条件付き定理であり、一般 i=3 や Erdős 699 の証明ではない。自由な探索次数上限は使わない。元の数値条件から N<=3 を証明した後、すべての整数パラメータを列挙する。

## 設定

```math
F=2+(aX-1)(1+bX)Q,\quad J=2+(vX-h)Q,\quad
h\in\{1,2\},\quad b\ge2,\quad a\ge2,\quad N=\deg Q\ge1.
```

Q は整数係数、Q0=1、最高係数 s>=1。標準桁の条件は整数の奇数底 q>=5 に対し 0<=Jr<=Fr<q、F1>=1。また 1+bX は J-g を割り、g は0または1。第一の数値条件は

```math
n=F(q),\quad j=J(q),\qquad n-1\mid3j(j-1).
```

すべての Q 係数は正整数である。J の係数を最高次から逆向きに見ると、vQr-1-hQr>=0 と QN>0 からこれが従う。標準桁の最高係数と低桁により

```math
q>abs,\quad v\ge h,\quad v<ha,\quad
F_1=a-b-Q_1\ge1,\quad a\ge b+2,\quad q\ge9.
```

v<ha は X=1/a で F=2、J<F を評価して得る。Q(1/a)>0 なので v/a-h<0。これは j が n 未満という元の範囲を含む標準桁の非端点条件である。

## 共通の整数商

```math
E=1+bq,\quad P=(aq-1)E,\quad R=vq-h,\quad U=Q(q),
\qquad n-1=1+PU,\quad j=2+RU.
```

E は j(j-1) を割り、gcd(E,n-1)=1 だから、第一条件の商は kE、k は正整数となる。U で評価すれば

```math
kE=6+\ell U,\quad \ell\in\mathbb Z,\qquad
(3R^2-\ell P)U=6P+\ell-9R.
```

E>=19>6 なので ell>0。a>=b+2 から

```math
P=abq^2+(a-b)q-1>abq^2>R,\qquad
\ell<\frac{3R^2}{P}<\frac{3v^2}{ab}<\frac{3hv}{b}.
```

第一の厳密上界には

```math
\left(\frac{3R^2}{P}-\ell\right)(1+PU)
=\frac{3(R-P)(R-2P)}P>0
```

を使う。

J-g を E で評価し kE=6+ellU を使えば

```math
E\mid C=6R-(2-g)\ell.
```

d=2-g と書く。上の ell 上界と h<=v、h/b<=1 より

```math
C>6v(q-1-h/b)\ge6v(q-2)>0.
```

したがって

```math
\lambda=C/E\in\mathbb Z_{>0},\quad \lambda<6v/b,\quad
Z=\lambda+6h+d\ell=q(6v-b\lambda)>0.
```

ゆえに q<=Z<18v/b+12。

## b>=7の全排除

v<2a、q>ab、a>=b+2 から

```math
0<Z/q<36/b^2+12/(ab)
\le36/b^2+12/[b(b+2)].
```

b>=7 では右辺は単調減少し、b=7 でも

```math
36/49+12/63=952/1029<1.
```

Z/q は正整数なので矛盾。以後 b=2,3,4,5,6 のみ。

## N>=4の全排除

T=3R²-ellP、V=6P+ell-9R と書く。P>abq²、R<2aq、bq>=18 より P>9R、従って V>0。

T=0 なら TU=V から V=0 となり矛盾する。一般の共通の代数確認でも、T=V=0 は (3R-ell)(6R-ell)=0、P=ell/3 または ell/12 を強制する。ここでは V>0 を使うだけで十分である。

TU=V、U>0 だから T は正整数で、U<=V。q>ab と ell<3hv/b により

```math
P<q^3+q^2/b\le q^3+q^2/2,\qquad
\ell<12a/b<12q/b^2\le3q.
```

従って

```math
U\le V<6q^3+3q^2+3q<q^4.
```

最後の不等式は q>=9 で、q³-6q²-3q-3 を q-9 で展開した全係数が正であることによる。全 Q 係数は正で U>q^N。したがって N>=4 は不可能であり、N=1,2,3 に限られる。

## 有限域を漏れなく導く

多項式 1+bX が J-g を割るので X=-1/b で

```math
(v+hb)b^NQ(-1/b)=d b^{N+1},\qquad
v+hb\mid d b^{N+1}.
```

b²からb⁴までの固定整数の約数だから v は絶対的に有限になる。N=1,2,3、b=2..6、h=1,2、g=0,1、正の約数 D|(d b^(N+1)) を全て取り、v=D-hb>=h とする。

その他の範囲はすべて先の厳密不等式から得る。

```math
a_{\min}=\max(b+2,\lfloor v/h\rfloor+1),\quad
q>a_{\min}b,\quad
bq<(6+3dh)v+6hb,
```

```math
1\le\ell\le\left\lfloor\frac{3hv-1}{b}\right\rfloor,\qquad
a\le\min\left(
\left\lfloor\frac{q-1}{b}\right\rfloor,
\left\lfloor\frac{3v^2-1}{b\ell}\right\rfloor\right).
```

底 q はこの範囲の奇数整数すべて。lambda を先に仮定せず、

```math
d\ell\equiv6vq-6h\pmod{1+bq}
```

を gcd と逆元で解き、範囲内の全解を列挙する。候補ごとに C>0 と lambda=C/(1+bq) の整数性を確認する。

その後 T,V を整数で計算する。TU=V の解 U は一意であり、必要条件は

```math
U\in\mathbb Z,\quad U>q,\quad U\equiv1\pmod q.
```

検算は297個の整除根パラメータ、5465個の底候補、596個の完全な整数パラメータ行を得る。最後の U 条件を満たすものは0件である。Q の係数をさらにチェックする必要が生じる候補すらない。

よって指定の E一次・b>=2 の線形 J-2 商は、全 N>=1 で排除された。

## b=1を加える場合の完全付値条件

b>=2 の証明は q の完全素数付値を使わない。b=1 は次の追加条件のもとで全次数を閉じる。

```math
A(q)=\frac{n-1}{q},\qquad \gcd(q,A(q))=1.
```

例えば q=p^e が n-1 の完全 p 付値であればこの条件を満たす。q は n-1 自体を割るので、gcd(q,n-1)=1 と書いてはならない。

X=-1 の評価は

```math
(v+h)Q(-1)=2-g.
```

v>=h>=1 なので g=1 は不可能。g=0 では v+h=2、従って h=v=1。J の非負係数から Qr-1>=Qr>0、Q0=1 なので全 Q 係数は1。Q(-1)=1 だから N は偶数、N>=2。

```math
Q=1+X+\cdots+X^N,\quad J=1+X^{N+1},\quad a\ge3.
```

直接の係数比較により

```math
A(q)=a q^{N+1}+(2a-1)q^N+
(2a-2)\sum_{r=1}^{N-1}q^r+(a-2)>3j.
```

最後の評価は a>=3、N>=2、q>=5 に対し、A-3j の最高係数 a-3 は非負、定数 a-5 は-2以上、q^N の係数2a-1は5以上であることから従う。

第一の整除性と j-1=q^(N+1) から A(q)|3q^Nj。完全付値の追加条件で q を取消せば A(q)|3j となり、A(q)>3j に矛盾する。

したがって **完全付値条件を加えれば b=1も含む E一次の全域が閉じる**。この追加条件を標準桁条件だけから推測してはならない。

## 範囲と検算

[厳密検算器](../../scripts/audit_i3_linear_J2_quotient_degree1_bge2_all_degrees.py) は数値範囲の整数端点、低桁の合同、全約数、全 a、商の整数性を確認する。b=1の追加節については任意 N の係数公式を有理恒等式として検算する。互いに素の追加条件と整数の取消しは明示した数学的入力であり、計算で省略しない。

[独立再生](../../scripts/audit_i3_linear_J2_quotient_degree1_independent.py) は lambda と q を先に列挙し、低桁の式から ell を逆算する。
元の検算器の合同の逆元による列挙と独立に、297整除根パラメータ・596整数行・許される整数Qが0件であることを再確認した。
