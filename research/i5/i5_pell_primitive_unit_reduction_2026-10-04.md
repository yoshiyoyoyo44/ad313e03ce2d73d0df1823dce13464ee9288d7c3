# i=5: Pell の全非基本指数と最大整数環の三乗枝を排除

これは元問題の完全解決ではない。既存の i=5 尾部の混合上界から、平方類 D に属する Pell 解が基本単数でなければならないことを証明する作業稿である。最後の平方類同期は未証明であり、本稿の結論に含めない。

## 使用する既存の入力

[積・完全冪の稿](i5_global_product_and_affine_exclusions_2026-10-03.md) の第7、9節を使う。反例候補の尾部は n>N=10^87、6<=j<=n/2、支持01、n mod72 が9または64であり、復元余因子 A,B は次の通り。

```math
\begin{array}{ll}
n\equiv9\pmod{72}:& n=3^F A,\quad n-1=2^E B,\\
n\equiv64\pmod{72}:& n=2^E A,\quad n-1=3^F B.
\end{array}
```

A,B は正整数であり、5を除去した余因子ではない。両向きに共通して

```math
A^6B^5<C_6n^3,\qquad A^9B^4<K_9n^4,
\qquad C_6=1458000000,\quad K_9=71191406250000.
```

既存稿は n が平方数の尾部を BFT Theorem 2.1 と整数の閾値比較で排除している。この入力をここでも使う。n-1 が平方数の排除には外部定理を要さない: 9類では n-1=2 mod3、64類では n-1=7 mod8 だからである。本稿の追加の Pell 上界には BFT を使わない。

## 1. 整数 Pell 解の指数を全部排除する

一意に

```math
n(n-1)=DZ^2,\qquad D\ge2\text{ は平方因子を持たない},\quad Z\ge1
```

と書く。n(n-1) は n-1 と n の平方の間にあるので D=1 ではない。

```math
\varepsilon_n=2n-1+2Z\sqrt D,\qquad N_{K/\mathbb Q}(\varepsilon_n)=1.
```

整数係数の最小正ノルム1解を

```math
\varepsilon_1=X_1+Y_1\sqrt D>1,\qquad X_1,Y_1\in\mathbb Z_{>0}
```

とする。Pell の正ノルム1群は巡回群だから、ある m>=1 に対し

```math
\varepsilon_n=\varepsilon_1^m,\qquad 2n-1=T_m(X_1).
```

m が偶数なら

```math
T_{2r}(x)=2T_r(x)^2-1,\qquad n=T_r(X_1)^2
```

となり、既存の平方数排除に反する。

m=2r+1>=3 とする。T_m(X_1) が奇数なので X_1 も奇数。第二種 Chebyshev 多項式 U_r と U_{-1}=0 により

```math
T_{2r+1}(x)+1=(x+1)(U_r(x)-U_{r-1}(x))^2,
T_{2r+1}(x)-1=(x-1)(U_r(x)+U_{r-1}(x))^2.
```

U_r(x) mod2 は r が偶数なら1、奇数なら0だから、両括弧は奇数である。n,n-1 の偶数の方を N_2 とすれば、sigma=+1（n が偶数）、sigma=-1（n が奇数）に対して

```math
N_2=\frac{X_1+\sigma}{2}R^2,\qquad R\text{ は奇数}.
```

従って N_2 の2冪を除いた余因子は R^2 以上である。

x>=1 で T_m(x)>=x^m は全 m に成立する。実際 T_m>=xT_{m-1} を Chebyshev の漸化式で帰納すればよい。よって m>=3 から

```math
X_1\le(2n-1)^{1/m}<(2n)^{1/3},
X_1+\sigma<2(2n)^{1/3}.
```

n>=2 で 2(n-1)>=n、また (2*2^(1/3))^3=16<27 なので

```math
R^2=\frac{2N_2}{X_1+\sigma}>
\frac{n}{2(2n)^{1/3}}>\frac{n^{2/3}}3.
```

奇数の向きでは B>=R^2 だから

```math
B^5>\frac{n^{10/3}}{3^5},\qquad B^5<C_6n^3,
\qquad n<(3^5C_6)^3<N.
```

偶数の向きでは A>=R^2 だから

```math
A^9>\frac{n^6}{3^9},\qquad A^9<K_9n^4,
\qquad n^2<3^9K_9<N^2.
```

したがって全ての m>1 が排除された。

**結論1:** epsilon_n は整数係数の基本正ノルム1 Pell 単数である。

## 2. 最大整数環に残る指数3も排除する

K=Q(sqrt D) の最大整数環を O_D とする。O_D の正ノルム1基本単数 eta が整数係数なら結論1から eta=epsilon_n。

非整数係数なら D=1 mod4 で

```math
\eta=\frac{x+y\sqrt D}{2}>1,\qquad x,y\text{ は奇数},\quad x^2-Dy^2=4.
```

x=Tr(eta)>2 なので x>=3。eta^2=x eta-1 は非整数係数だが

```math
\eta^3=(x^2-1)\eta-x
```

は整数係数である。従って正ノルム1単数群の最初の整数係数単数は eta^3。結論1により epsilon_n=eta^3 とならなければならない。この場合

```math
2n-1=\frac{x^3-3x}{2},
n=\left(\frac{x-1}{2}\right)^2(x+2),
n-1=\left(\frac{x+1}{2}\right)^2(x-2).
```

x<15 なら n<10^3<N。以下 x>=15 とする。

奇数の9類では n=0 mod3 から x=1 mod3。a=(x-1)/2、b=x+2 は共に3で割れ、b-2a=3 だから min(v3(a),v3(b))=1。

```math
A=\frac{a^2b}{3^{v_3(a^2b)}}\ge
\min\left(\frac{x+2}{3},\frac{(x-1)^2}{36}\right)\ge\frac x3.
```

最後の評価は

```math
(x-1)^2-12x=(x-15)^2+16(x-15)+16>0
```

で確認できる。n-1 側の x-2 は奇数なので

```math
B\ge x-2\ge x/2,\qquad A^6B^5\ge\frac{x^{11}}{3^6\,2^5}.
```

偶数の64類では n-1=0 mod3 から x=2 mod3。x+2 が奇数なので A>=x+2>x。c=(x+1)/2、d=x-2 について 2c-d=3 であり、

```math
B\ge\min\left(\frac{x-2}{3},\frac{(x+1)^2}{36}\right)
 =\frac{x-2}{3}\ge\frac x6.
```

最小値の等号は (x+1)^2-12(x-2)=(x-5)^2>=0 による。したがって

```math
A^6B^5\ge\frac{x^{11}}{3^5\,2^5}.
```

両向きとも n=(x^3-3x+2)/4<x^3/4 と混合上界から

```math
x^2<\frac{3^6C_6}{2}
 =531441000000=729000^2,\qquad
n<\frac{729000^3}{4}<10^{17}<N.
```

尾部で eta が非整数係数となる全域を閉じた。

**結論2:** epsilon_n は O_D 全体でも正ノルム1の基本単数である。

## 3. 負ノルム単数は整数・半整数とも存在しない

O_D に正のノルム-1単数が存在すれば、その最小のもの theta の平方が正ノルム1基本単数になる。これは正単数群の巡回性、または最小性による割り算で示せる。

theta=a+b sqrt D が整数係数なら

```math
\varepsilon_n=\theta^2,\qquad
2n-1=2a^2+1,\qquad n-1=a^2,
```

となり、法72の9・64類に反する。

theta=(r+t sqrt D)/2 が非整数係数なら r,t は奇数で、theta^2 のトレース r^2+2 も奇数。theta^2 は非整数係数のノルム1単数なので、結論2の整数係数基本単数 epsilon_n と一致できない。

**結論3:** O_D にノルム-1単数は存在しない。

## 4. 依然として必要な平方類同期

結論2から、1<l<n について

```math
l(l-1)=Dw^2,\quad w\in\mathbb Z
```

は不可能である。従って j または k=n-j から同じ D の平方商を作れれば尾部は閉じる。

全候補素数の Kummer 条件が与える D の大きい素因数の整除は、この平方商をまだ与えない。セル(s,u)で p>=7、e=v_p(n-s)、v=s-u とし

```math
f=v_p(j-u),\qquad g=v_p(k-v).
```

すると j-u+k-v=n-s より min(f,g)=e。従って f=e+h,g=e または f=e,g=e+h と書けるが、h の偶奇は確定していない。

普遍的に使える追加の局所上限は、p^(e+1)>j-u なら f=e であること。特に p^(e+1)>n/2 なら j 側では必ず f=e、p^(e+1)>n なら両側とも f=g=e となる。これは全セルに適用できるが、小さい候補素数の追加付値と、j(j-1) に入る候補集合外の素数の平方類を消す補題にはまだなっていない。

第3・4行に対しても、p が j-u に割り当てられ u>=2 なら p は j(j-1) を割らず、

```math
\left(\frac{D_j}{p}\right)=\left(\frac{u(u-1)}p\right),
\qquad D_j=\operatorname{sf}(j(j-1)).
```

例えば第4行の中央セル u=v=2 では

```math
\left(\frac{D_j}{p}\right)=\left(\frac{D_k}{p}\right)
=\left(\frac2p\right),\qquad
\left(\frac{D_jD_k}{p}\right)=1.
```

これは割当てから確実に得られる局所条件である。D_j=D または D_k=D への持ち上げを本稿は証明していない。

## 検算

[検算器](../../scripts/audit_i5_pell_primitive_unit_reduction.py) は浮動小数点を使わず、Chebyshev の全奇数指数恒等式に必要な初期値と共通漸化式、三乗・半整数公式、余因子下限の多項式証明書、全閾値の整数比較を確認する。有限の指数の一致だけを全指数の証明に代用しない。n が平方数の既存排除は上記の入力であり、検算器がその外部定理を新たに証明するとは主張しない。
