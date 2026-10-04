# i=3・次数4の完全分配：J0=0 の三一次型の残る二順序

2026-10-04。**一般 i=3 と元問題の完全解決ではない。**
仮定は [b>t>c の稿](i3_three_linear_order_working_2026-10-04.md)と同じ。
ここでは $c>t>b$ と $t>c>b$ を閉じる。
同稿と [b>c>t の稿](i3_three_linear_b_c_t_working_2026-10-04.md)により、
条件付き標準桁設定の $J_0=0$ の三一次型全体が閉じる。

## 共通する新しい二つの評価

```math
D_0=1+bX,\ D_1=1+cX,\ D_2=1+tX,
\quad J=X(1+bX)(v+wX),\ v\ge0,w>0,
```

```math
S_1=b+c+t,\quad S_2=bc+bt+ct,
\quad a\ge S_1+v,\quad q>abct,
\quad A=(F-1)/X,\quad k=3K(q)/A(q)\in\mathbb Z_{>0}.
```

$qA(q)=(aq-1)D(q)+1$ と $J\equiv2\pmod{D_2}$ から

```math
kD_0(q)D_1(q)\equiv6\pmod{1+tq}.
```

$tq\equiv-1$ を代入して分母を払うと

```math
1+tq\mid H:=k(t-b)(t-c)-6t^2.\tag{1}
```

さらに標準桁の第3係数の上限は

```math
bw\le aS_2-bct.
```

$v<a<ctq$ より $v+wq<(aS_2/b)q$。
第一条件の商を正確に評価すると

```math
k=\frac{3J(q)(J(q)-1)}{qA(q)D_0(q)D_1(q)}
<\frac{3q^2(v+wq)^2}{(aq-1)(1+cq)^2(1+tq)}
<\frac{3aS_2^2}{b^2c^2t}.\tag{2}
```

最後は $(aq-1)(1+tq)>atq^2$ を使う。$a>t$ なので成り立つ。
また低桁では $q\mid kF_1+3v$。

## c>t>b

$H<0$。$x=b/t,y=t/c\in(0,1)$ とすると

```math
\frac{(t-b)(c-t)S_2^2}{c^3t^3}
=(1-x)(1-y)(1+x+xy)^2\le\frac{32}{27}.
```

この上限は次の二つの非負恒等式から出る。

```math
(1-x)(1+x)^2-(1-x)(1-y)(1+x+xy)^2
=(1-x)\{(1-x)(1+x)y+x(2+x)y^2+x^2y^3\},
```

```math
32-27(1-x)(1+x)^2=(3x-1)^2(3x+5).
```

(2) と $1+tq>abct^2$ を用いて、$b\ge2$ なら

```math
\frac{|H|}{1+tq}<\frac{32}{9b^3}+\frac6{abc}
\le\frac49+\frac1{12}<1.
```

(1) と $H\ne0$ に矛盾する。

$b=1$ では根条件から $w=vc+c^3/(c-1)<vc+2c^2$。
従って $v+wq<(v+2c)(1+cq)$ を (2) の直前の式へ入れて
$k<3(v+2c)^2/(at)<12a/t$ を得る。
$t\ge4,c\ge5,a\ge10$ なら

```math
\frac{|H|}{1+tq}
<\frac{12(c-t)}{ct^2}+\frac6{ac}
<\frac34+\frac3{25}<1.
```

残る $t=2,3$ は根条件
$c^3/(c-1)\le2t^3/(t-1)$ と、この関数の $c\ge2$ での単調増大から、
それぞれ $c=3,4$ だけ。
その $v$ は $5/2,17/3$ で整数でない。よって全排除。

## t>c>b

$f(z)=z^3/(z-b)$ とする。根条件と $v\ge0$ より $f(c)\ge2f(t)$。
$f(t)>t^2>c^2$ なので

```math
c<2b,\qquad
\frac tc<\sqrt{\frac{c}{2(c-b)}}<\sqrt b.
```

$b\le3$ では $b<c<2b$ を全て読むと、いずれも $f(c)<2f(c+1)$。
$f$ は $z\ge c+1$ で増加するので不可能。
従って $b\ge4,c\ge5,t\ge6,a\ge15$。

```math
\frac{(t-b)(t-c)S_2^2}{c^3t^3}
<\frac tc\left(\frac{S_2}{ct}\right)^2<9\sqrt b.
```

(2) から

```math
\frac{|H|}{1+tq}<\frac{27}{b^{5/2}}+\frac6{abc}
\le\frac{27}{32}+\frac1{50}<1.
```

よって (1) は $H=0$ を強制し、
$k=6t^2/((t-b)(t-c))$。
一方

```math
bct(t-b)(t-c)-6t^2-3(t-b)(t-c)>0
\quad(b\ge4,\ c\ge b+1,\ t\ge c+1).
```

この多項式に $b=4+B,c=b+1+C,t=c+1+T$ を代入すると、
全40係数が正（定数項18、最小係数1）。従って $k+3<bct$。
しかし

```math
0<kF_1+3v<(k+3)a<abct<q,
```

であり、$q\mid kF_1+3v$ に矛盾する。

## 厳密検算と適用境界

[検算器](../../scripts/audit_i3_three_linear_above_2026_10_04.py)は、
上限の二恒等式、三つの有理数比較、全40係数、
$b=1$ と $b\le3$ の全小分岐を整数・有理数で確認する。
[保存結果](../../data/results/verification_i3_three_linear_above_2026-10-04.json)

三次の $J$ の正係数と根条件により、$c,t$ はともに $b$ より大きいか、
ともに小さい。片方だけ大きいと $w/v$ の二つの必要な大小が矛盾する。
$v=0$ では根条件から両方が大きい。
従ってここで扱った二順序と先行二稿の二順序で、$J_0=0$ の三一次型を尽くす。
$J_0=1$ と数値領域からの一般の分配移行は別に残る。
