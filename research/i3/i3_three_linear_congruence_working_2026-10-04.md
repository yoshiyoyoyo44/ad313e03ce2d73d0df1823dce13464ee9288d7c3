# 三一次分配の短い合同証明

2026-10-04。これは条件付き標準桁・完全分配の研究稿であり、一般 i=3 や問題699の解決ではない。

## 設定と共通評価

```math
F=2+(aX-1)(1+bX)(1+cX)(1+tX),\qquad
\deg J=3,\quad J_0=\varepsilon\in\{0,1\},
```

標準桁条件は $0\le J_r\le F_r<q$、$F_1>0$、$q>abct$。
$b,c,t$ は相異なる正整数で、$1+bX\mid J$、$1+cX\mid J-1$、$1+tX\mid J-2$。
$A=(F-1)/X$、$K=J(J-1)/(X(1+bX)(1+cX))$ と置き、
第一数値条件から $k=3K(q)/A(q)\in\mathbb Z_{>0}$ を得る。

```math
S_1=b+c+t,\quad S_2=bc+bt+ct,\quad S_3=bct,
\qquad A=(a-S_1)+(aS_1-S_2)X+(aS_2-S_3)X^2+aS_3X^3.
```

両定数桁で $J_1=v\ge0$、$a\ge S_1+v$。

```math
\begin{array}{c|c|c}
\varepsilon&J&\text{根の整数等式}\\\hline
0&X(1+bX)(v+wX)&(c-b)(w-vc)=c^3,\quad(t-b)(w-vt)=2t^3\\
1&1+X(1+cX)(v+wX)&(c-b)(w-vb)=b^3,\quad(t-c)(w-vt)=t^3
\end{array}
```

ここで $w>0$。$qA(q)=(aq-1)D(q)+1$ と $J\equiv2\pmod{1+tX}$ より

```math
1+tq\mid H:=k(t-b)(t-c)-6t^2.\tag{1}
```

また両定数桁で

```math
k<\frac{3aS_2^2}{b^2c^2t}.\tag{2}
```

$\varepsilon=0$ では $bw\le aS_2-bct$ より $v+wq<aS_2q/b$。
$\varepsilon=1$ では $cw\le aS_2-bct$ と $btq-v>1$ より
$v+wq+1/(q(1+cq))<aS_2q/c$。
それぞれ $J/(1+bq)$、$J/(1+cq)$ を第一条件の商へ代入し、
$(aq-1)(1+tq)>atq^2$、$(1+bq)^2>b^2q^2$、$(1+cq)^2>c^2q^2$ を使えば (2)。

低桁の条件は

```math
q\mid k(a-S_1)+3v\quad(\varepsilon=0),\qquad
q\mid k(a-S_1)-3v\quad(\varepsilon=1).\tag{3}
```

## t が中間の場合：両定数桁で排除

$m=\min(b,c)\ge2$ とする。$x=m/t,y=t/\max(b,c)$ により

```math
\frac{|(t-b)(t-c)|S_2^2}{\max(b,c)^3t^3}
=(1-x)(1-y)(1+x+xy)^2\le32/27.
```

この上限の証明は、$(1-x)(1+x)^2$ との差が
$(1-x)\{(1-x)(1+x)y+x(2+x)y^2+x^2y^3\}$ となることと、
$32-27(1-x)(1+x)^2=(3x-1)^2(3x+5)$ による。
従って

```math
0<\frac{|H|}{1+tq}<\frac{32}{9m^3}+\frac6{abc}
\le\frac49+\frac1{12}=\frac{19}{36}<1,
```

で (1) に矛盾。$m=1$ は上の根の整数等式から
$\max(b,c)-1\mid1$ となり、$1<t<\max(b,c)$ に反する。

## t が最大の場合

$t>c>b$ だけが根条件と両立する。
$\varepsilon=0$ では $c^3/(c-b)\ge2t^3/(t-b)$ より
$c<2b$、$t/c<\sqrt b$。$b\le3$ は $b<c<2b$ の有限個の値で
$c^3/(c-b)<2(c+1)^3/(c+1-b)$ となり排除される。
$\varepsilon=1$ では

```math
v(t-b)=\frac{b^3}{c-b}-\frac{t^3}{t-c}\ge0
```

から同じ二つの上限を得る。また $t^3/(t-c)\ge27c^2/4$ より $b\ge9$。
両定数桁に $b\ge4,c\ge5,t\ge6,a\ge15$ を使えるため

```math
\frac{|H|}{1+tq}<\frac{27}{b^{5/2}}+\frac6{abc}
\le\frac{27}{32}+\frac1{50}<1.
```

従って $H=0$、$k=6t^2/((t-b)(t-c))$。
$b=4+B,c=b+1+C,t=c+1+T$ に代入すると

```math
bct(t-b)(t-c)-6t^2-3(t-b)(t-c)
```

の全40係数が正（定数項18、最小係数1）。ゆえに $k+3<bct$。
$\varepsilon=0$ では (3) の正の被除数が $q$ 未満となり矛盾。
$\varepsilon=1$ では (3) の絶対値が $q$ 未満となり $k(a-S_1)=3v$。
$a-S_1\ge v$ と $a-S_1>0$ より $v>0,k\le3$。
一方 $(t-b)(t-c)<t^2$ なので $k>6$。矛盾。

## t が最小の場合：定数桁0を排除

根条件が許す順序は $b>c>t$。$S_2<3bc$、$(b-t)(c-t)<bc$ より、$t\ge4$ では

```math
\frac{|H|}{1+tq}<\frac{27}{t^3}+\frac6{abc}<1.
```

よって $H=0$、$k=6t^2/((b-t)(c-t))\le3t^2$。
$bct\ge t(t+1)(t+2)>3t^2+3$ より $k+3<bct$、(3) に矛盾。

$t=1,2,3$ では $(b-t)\mid2t^3$ のため、$b$ と $t<c<b$ は有限。
上の根等式から整数 $v\ge0,w>0$ を持つものは正確に次の11組。

| t | (b,c,v,w) |
|---|---|
| 1 | (3,2,7,6) |
| 2 | (4,3,19,30), (6,3,5,6), (6,4,14,24), (10,6,13,24) |
| 3 | (5,4,37,84), (6,4,14,24), (9,6,21,54), (12,6,10,24), (21,12,21,60), (57,30,37,110) |

```math
K=-v+\{v(v+c)-w\}X+
\{vw(b+c)/c+wc\}X^2+(bw^2/c)X^3.
```

全11組で桁条件が要求する最小 $a$ において $(bct-2)A-3K$ の全係数が正。
各係数の $a$ の傾きも正であるから、全ての許される $a,q$ に $k<bct-2$。
ここで $k$ は整数だから $k+3\le bct$。
従って (3) の被除数は再び $0$ と $q$ の間に入り、矛盾する。
これは自由な探索上限ではなく、整除性で導いた全小分岐の排除である。

## t が最小の場合：定数桁1も排除

```math
J=1+X(1+cX)(v+wX),\quad z=cw/b\in\mathbb Z_{>0},
\quad K=v+\{w+v(v-b)\}X+\{w(v-b)+zv\}X^2+zwX^3.
```

$t\ge4$ は同じ評価で $H=0$。$k\le3t^2$、$k+3<bct$ なので (3) の絶対値は $q$ 未満。
従って

```math
k(a-S_1)=3v,\quad v>0,\quad k\in\{1,2,3\},
\quad (b-t)(c-t)=6t^2/k,\quad a=S_1+3v/k.\tag{4}
```

根条件と (4) から差 $R=kA-3K$ は

```math
R=X(1+tX)(\alpha X+\beta),\qquad
\beta=k(aS_1-S_2)-3\{w+v(v-b)\}.
```

整数係数の $R$ を primitive な整数多項式 $X(1+tX)$ が割るため、Gauss補題により
$\alpha,\beta$ も整数。$\alpha\ne0$ で $R(q)=0$ なら $q\le|\beta|$。
$\alpha=0,\beta\ne0$ では直ちに $R(q)\ne0$。
以下は $t\ge6$ で $|\beta|<abct<q$ を示す。

$\beta\ge0$ の場合、$v(b-v)\le b^2/4$ を用いて

```math
\frac{\beta}{abct}
<\frac{3S_1}{bct}+\frac{3b^2}{4abct}
<\frac{39}{4t^2}<1.
```

$\beta<0$ なら $w<vt$ より $|\beta|<3v(v+t)$。
$d=b-t,e=c-t,\delta=b-c=d-e$ とすると
$de\ge2t^2$、$d>\sqrt2t$、$t/d<5/7$。
根条件の $v<b^3/(\delta d)$ から

```math
\frac v{bct}
<\frac1t\left(1+\frac td\right)
\left(\frac1\delta+\frac1c\right).
```

$\delta=1$ では $c=t+d-1>2t$。$a\ge v$ と合わせて

```math
\frac{|\beta|}{abct}
<3\left\{\frac{12}{7t}\left(1+\frac1{2t}\right)+\frac1{4t^2}\right\}
\le\frac{319}{336}<1.
```

$\delta\ge2$ では $c\ge t+1,b\ge t+2$ なので

```math
\frac{|\beta|}{abct}
<3\left\{\frac{12}{7t}\left(\frac12+\frac1{t+1}\right)
+\frac1{(t+1)(t+2)}\right\}
\le\frac{237}{392}<1.
```

どちらの上限も $t$ について減少し、右端は $t=6$。
残る恒等的な場合 $\alpha=\beta=0$ も起こらない。
$x=(c-t)/t$ により $b/t=1+6/(kx),c/t=1+x$ と正規化すると、
$\alpha/t^3$ と $\beta/t^2$ の分子は各 $k=1,2,3$ で互いに素。
$b>c>t$ より $0<x<\sqrt{6/k}$ であり、正規化した式の分母は0にならない。
検算器は三つの有理係数 Bezout 恒等式 $UP+VQ=1$ を生成・展開確認して保存する。
よって同時に0となる $x$ は存在しない。

$t=4,5$ は (4) により有限。$(c-t)(b-t)=6t^2/k$ の全約数を列挙して、
$v,w,z,a$ の整数性を満たすのは

```math
(t,k,b,c,v,w,a)=(4,3,12,8,52,192,76),\quad(5,3,15,10,65,300,95).
```

一次式の根はそれぞれ $13/24,13/30$ で、許される底にならない。

$t=1,2,3$ は (4) を先に仮定しない。
根条件から $(c-t)\mid t^3$、$(b-c)\mid c^3$ のため、この場合も有限。
整数 $v,w,z$ を持つ全12組は、$t$ ごとに1組・4組・7組。
全組で最小の許される $a$ において $(bct-2)A-3K$ が正となる。
11組は全係数が正で、残る $(b,c,t,v,w)=(3,2,1,13,12)$ は
最小 $a=19$ において $13-14X+140X^2+168X^3>0$ for $X\ge1$。
各係数の $a$ の傾きは正だから、全 $a$ で $k<bct-2$。
整数性により $k+3\le bct$。
従って低桁で (4) の最初の三条件を得る。
各 $k=1,2,3$ と整数 $a=S_1+3v/k$ を全て検査すると、$H\ne0$ の場合は
$|H|<1+taS_3<1+tq$ に反する。$H=0$ は
$b=3t,c=2t,v=13t,w=12t^2,k=3,a=19t$ の三組だけで、
一次式の根 $q=13/(6t)$ が $q>abct$ に反する。

以上で定数桁1の最後の順序も全パラメータで閉じた。

## 検算と残る範囲

[厳密検算器](../../scripts/audit_i3_three_linear_congruence_2026_10_04.py) は
二つの上限恒等式、40係数の正性、定数桁0の11組、定数桁1の12組と2組、
正係数・根条件・$K$、差の因数分解、三つの Bezout 恒等式を確認する。
[保存結果](../../data/results/verification_i3_three_linear_congruence_2026-10-04.json) は `passed`。

これで両定数桁の三一次分配は全順序で閉じる。
一般の数値領域、次数と桁和が増大する分配への結論は含まない。

## 残余次数6との接続

[非三一次型の全証明](i3_degree4_complete_split_working_2026-10-04.md) と合わせると、
完全 $Q_1$ 素数冪の底、$4\mid n$、正整数 $a$、
$F-2=(aX-1)D$ の全重複度の完全分配を既に満たす
$\deg F=4,\deg J=3$ の全型が排除される。
$\deg B_2\le2$ は $J-2$ の正実根から従い、
三次一群は既存の一群割当て定理、二次・一次の全配置は上記稿、
三一次は本稿で覆う。これにより未処理の次数型は残らない。

$\rho=3d-m+1=6$、$m\ge3$ では $d\ge3$。
$d=3,m=4$ は今回、$d=4,m=7$ は
[先行する全排除](i3_independent_attack_2026-10-03.md)、$d\ge5$ は
[Mahler測度の次数評価](i3_split_mahler_frontier_2026-10-03.md) で排除される。
従って、**この条件付き設定の残余次数6は全域で閉じた。**
元の数値反例がこの完全分配を満たすという移行、残余次数7以上の一般枝は依然として未証明。
元問題の完全解決を意味しない。
