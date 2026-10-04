# 二次残余と J−2 の一次商：全次数の排除

2026-10-04。これは標準桁・完全分配の条件付き定理であり、一般 i=3 や問題699の解決ではない。
次数を自由に動かし、導かれた有限域の全検査で排除する。任意の次数上限を仮定しない。

## 定理の正確な仮定

奇数の底 $q\ge5$ において $n=F(q),j=J(q)$、
$F_0=1,F_1\ge1,0\le J_k\le F_k<q$ とする。
正整数 $a$ と整数多項式 $E,Q$ が

```math
F-2=(aX-1)E Q,\quad E=1+bX+wX^2,
\quad Q(0)=1,\quad\deg Q=N\ge1,
```

を満たし、$E=B_g\mid J-g$ for $g=0$ or $1$、$Q=B_2\mid J-2$ とする。
全重複度を含む分配であり、もう一つの群は定数1。
さらに

```math
J=2+(vX-h)Q,\qquad h=2-J_0\in\{1,2\},\qquad v\in\mathbb Z_{>0}
```

と一次商を持つと仮定する。すなわち $\deg F=N+3,\deg J=N+1$。
**この設定では $n-1\mid3j(j-1)$ は不可能。** $4\mid n$、底の素数冪性は必要ない。
同じ結論は $E=(1+bX)(1+cX)$ を二群 $B_0,B_1$ に分ける場合にも成立する。
その証明は後述する。従って $\deg(B_0B_1)=2$ の完全分配は全て含まれる。

## 次数を消す二段合同

$D=EQ$ の全係数は標準桁の逆向き漸化式から正整数。
$E$ は正実根を持たず、$w>0$。$Q$ の最高次係数を $s>0$ とする。
$J_k=vQ_{k-1}-hQ_k\ge0$ を最高次から逆にたどると、$Q$ の全係数も正整数。
特に $Q_1\ge1$ なので $v\ge h$、$b<a$、$a\ge2$。
$J(1/a)$ の長さ1の区間から $v<ha$、最高次桁から $q>aws$。

二次式 $E$ の正実根がないことは、$b<0$ の場合 $b^2<4w$ を意味する。
従って $q\ge5$ に対し

```math
E(q)\ge(\sqrt w\,q-1)^2\ge\frac{16}{25}wq^2>6.
```

$A=(F-1)/X$ と $K=J(J-1)/(XE)$ に対して、第一条件は
$k=3K(q)/A(q)\in\mathbb Z_{>0}$ を与える。
$qA(q)=(aq-1)E(q)Q(q)+1$、$J\equiv2\pmod Q$ より

```math
kE(q)=6+\ell Q(q),\qquad\ell\in\mathbb Z_{>0}.
```

$J/Q<vq$、$(J-1)/Q<vq$ と $aq\ge10$ から

```math
\ell<\frac{3v^2q^2}{(aq-1)E(q)}
<\frac{125v^2}{24awq}
<\frac{125h^2}{24w^2s}\le\frac{125}{6},
\qquad\ell\le20.\tag{1}
```

$E\mid J-g$ と組み合わせると

```math
E(q)\mid C:=6vq-6h-(2-g)\ell.
```

(1) は $\ell<125hv/(24wq)$ も与える。
従って $q\ge5,v\ge h$ により
$C>(6q-25/6)v-6h>0$。
整数 $\lambda=C/E(q)>0$ を取ると

```math
\lambda<\frac{75v}{8wq}
<\frac{75h}{8w^2s}\le\frac{75}{4},\qquad\lambda\le18.
```

この第二合同を低桁に落とすと

```math
q\mid\lambda+6h+(2-g)\ell,
\qquad5\le q\le18+12+40=70.\tag{2}
```

ここまで $N$ に制限を置いていない。

## Q(q) の決定と全有限域

```math
P=(aq-1)E(q),\quad R=vq-h,\quad
T=3R^2-\ell P,\quad V=6P+\ell-9R.
```

$3j(j-1)=(6+\ell Q(q))(PQ(q)+1)$ を展開・相殺すると

```math
TQ(q)=V.\tag{3}
```

$T=V=0$ なら $R=\ell/3$ または $\ell/6$、$P=\ell/3$ または $\ell/12$。
しかし $P>144,\ell\le20$ に反する。$T=0,V\ne0$ も (3) に反する。
従って $Q(q)=V/T$ は一意な有理数で、整数性を検査できる。

(2) に $z=(\lambda+6h+(2-g)\ell)/q$ と置く。
$\lambda E(q)=C$ は

```math
b=(6v-z)/\lambda-wq
```

を与える。必要な全パラメータは次の有限域に含まれる。

```math
h=1,2,\quad g=0,1,\quad1\le\ell\le20,\quad1\le\lambda\le18,
\quad5\le q\le70\text{ は奇数},
```

```math
q\mid\lambda+6h+(2-g)\ell,
\quad2\le a<q,\quad1\le w\le\lfloor(q-1)/a\rfloor,
\quad h\le v<ha,
```

```math
b\in\mathbb Z,\quad b<a,\quad b<0\Rightarrow b^2<4w.
```

この全域は12,258組。
$T\ne0$、$Q(q)=V/T$ が整数、$Q(q)>q$、$Q(q)\equiv1\pmod q$ を同時に満たす組は0。
$Q$ は定数項1の正係数・正次数の整数多項式だから、最後の二条件は必須である。
したがって全 $N\ge1$ が排除される。

[検算器](../../scripts/audit_i3_quadratic_group_linear_residual_all_degrees.py) は
上限の有理数、二恒等式、導かれた全有限域を整数で確認する。
[保存結果](../../data/results/verification_i3_quadratic_group_linear_residual_all_degrees.json) は `passed`。
小さい範囲の一致0を、未導出の無限域へ外挿しているのではない。

## 二つの一次群に分ける場合

$B_0=1+bX,B_1=1+cX$、$b,c$ は相異なる正整数とし、$E=B_0B_1$ とする。
上の $Q$ の全係数正性、$a\ge2$、$v\ge h$、$v<ha$ はこの場合も成立する。
最高次桁は $q>abcs$ を与える。$E(q)>bcq^2>6$ から $\ell\ge1$ であり、

```math
\ell<\frac{3v^2q^2}{(aq-1)E(q)}
<\frac{10v^2}{3abcq}
<\frac{10h^2}{3(bc)^2s}.\tag{4}
```

$h=1$ なら $bc\ge2$ より $\ell<5/6$ で矛盾する。
$h=2$ かつ $b,c\ge2$ なら $bc\ge4$ より、やはり $\ell<5/6$ で矛盾する。
残るのは $b=1$ または $c=1$ である。

$b=1$ なら $J(-1)=0$ と $J=2+(vX-h)Q$ より
$(v+h)Q(-1)=2$。しかし $h=2,v\ge2$ だから $v+h\ge4$ で整数 $Q(-1)$ と両立しない。
$c=1$ なら $J(-1)=1$ より $(v+h)Q(-1)=1$ となり、同様に不可能。
以上は $N=\deg Q$ に一切依存しない。

残るのは $\deg(B_0B_1)\ne2$、$J-2$ の商が二次以上の場合、
正実根の因子が一次でない場合、非完全分配、一般数値領域である。
