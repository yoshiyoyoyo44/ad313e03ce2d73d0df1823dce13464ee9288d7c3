# i=3：六次の幾何級数で、負の一次因子以外を共有する枝

[現在地](../../docs/STATUS.md) · [先行する全共有稿](i3_integral_root_values_and_split_geometric_closeout_2026-10-02.md) · [任意の二次商](i3_quadratic_cofactor_single_allocation_closeout_2026-10-02.md) · [検算](../../scripts/audit_i3_sextic_partial_sharing.py) · [結果](../../data/results/verification_i3_sextic_partial_sharing.json)

2026-10-02。一般の i=3 は未解決。本稿は六次の特定構造で、二つの二次因子を別々の $J-s$ に割り当てる場合を閉じる。全ての六次の標準桁多項式を閉じた結論ではない。

## 定理

$G_m(Y)=\sum_{e=0}^{m-1}Y^e$ とする。$a,b\ge1$、整数底 $q\ge2$ に対し、

$$F=2+(aX-1)G_6(bX),\quad n=F(q),\quad j=J(q),$$

$$0\le J_k\le F_k<q,\qquad\min(j,n-j)\ge4$$

を仮定する。さらに

$$\boxed{G_6(bX)/(1+bX)\mid J(J-1)(J-2)}$$

とする。倍率 $b$ と3の互いに素性は要求しない。

1. **$b\ge2$ の全ての整数評価で、$4\mid n$ と $n-1\mid3j(j-1)$ は両立しない。** 底の素数冪性や他の素数での桁条件は使わない。
2. **$b=1$ でも、$q$ が真の反例の $Q_1$ の完全素数冪で、全ての奇共通候補素数の Kummer 条件が成立すれば、反例は不可能。** この場合は第一の整除条件だけで閉じたとは主張しない。

従って真の反例で $F$ がこの六次の形なら、全重複度の非共有部分は **$r_2\ge3$**。正実根の一次因子に加え、二次因子が少なくとも一つ非共有になる。

## 二つの二次因子による完全な形

$a<b$ は負の桁係数を生む。$a=b$ では $F=1+ab^5X^6$ となり、以下の共有条件を使った標準形から添字が $0,1,n-1,n$ に限られる。
以下 $\Delta=a-b>0$。最高次の桁より **$q>ab^5\ge b^6$**。

$$G_6(Y)/(1+Y)=\Phi_3(Y)\Phi_6(Y)=1+Y^2+Y^4.$$

この二つは $\mathbb Q[Y]$ で既約かつ互いに素。各々が割る $J-s$ の整数 $s$ を $s_o,s_e\in\{0,1,2\}$ とする。原始3乗根で $Y^3=1$、原始6乗根で $Y^3=-1$ だから

$$J(Y/b)\equiv(s_o+s_e)/2+(s_o-s_e)Y^3/2\pmod{1+Y^2+Y^4}.$$

補数で $J_0=1$ とできる。次数6までの商と、一次・二次係数を比較すると

$$\boxed{J=1+(cX+dX^2)G_3(b^2X^2)+\theta(bX)^6+\beta(bX)^3},$$

$$\theta=(s_o+s_e)/2-1,\qquad\beta=(s_o-s_e)/2,$$

$$0\le c\le\Delta,\quad0\le d\le b\Delta,\quad
0\le c+\beta b\le\Delta,\quad0\le d+\theta b^2\le ab.$$

$c,d$ は整数。半整数の $\beta$ は整数係数性から $b$ が偶数の場合に限る。
$\beta=0$ は $G_3(b^2X^2)\mid J-s_o$ となり、[任意の二次商の定理](i3_quadratic_cofactor_single_allocation_closeout_2026-10-02.md)で第一条件だけから排除済み。以下は六つの非定数割当てである。

## 第一条件を四次の整数剰余へ送る

$$Q=bq,\quad g=aq-1,\quad k=Q+1,\quad z=Q^2,$$

$$A=(n-1)/q=\Delta\sum_{e=0}^{4}Q^e+aQ^5,$$

$$V=c+dq-\theta\Delta k,\quad L=gk-2qV,$$

$$C=\beta^2gk^2\Delta-V(gk-qV),\quad
N=C+\beta gkbzL,\quad H=q(c+dq)+\theta k(Q-1).$$

直接の恒等式は

$$\frac{g^2k^2J(q)(J(q)-1)}q-N
=A\{qH^2A+HL+2\beta HgkQz+\beta^2gk^2(Q-1)\}.$$

分母は高々4なので第一条件は $A\mid12N$ を要求する。次の整数剰余の次数は4以下。

$$T=12\beta\{[(2\theta+1)ab-2\theta b^2-2d]q
 +(2\theta+1)\Delta-2c\},\quad R=12bN-TA,$$

$$R_4=-12ab^3\beta W,\qquad
W=(2\theta+1)ab+(1-2\theta)b^2-2d.$$

$R=\sum_{e=0}^4R_eq^e$。展開した各単項式に $c\le a,d\le ab,b\le a$ を使い、$|R_e|\le K_ea^2b^e$ とする係数表は次の通り。

| $(s_o,s_e)$ | $K_0$ | $K_1$ | $K_2$ | $K_3$ | $K_4$ |
|---|---:|---:|---:|---:|---:|
| (0,1) | 42 | 90 | 72 | 54 | 24 |
| (0,2) | 132 | 288 | 288 | 168 | 48 |
| (1,0) | 18 | 54 | 108 | 90 | 24 |
| (1,2) | 102 | 270 | 312 | 162 | 24 |
| (2,0) | 60 | 96 | 96 | 96 | 48 |
| (2,1) | 42 | 72 | 66 | 60 | 24 |

表は記号展開と係数の絶対値和で独立再生する。$a,b,c$ の重み1、$d$ の重み2で、$R_e$ は重み $e+2$、各単項式の $a,c,d$ の指数和は高々2である。このため各単項式は $a^2b^e$ 以下になる。

## b≥2：四次係数が非零の場合

$A>ab^5q^5$、$a<q/b^5$ より

$$\frac{|R|}A<\frac1{b^6}\left(48+\frac{168}{bq}
 +\frac{312}{(bq)^2}+\frac{288}{(bq)^3}+\frac{132}{(bq)^4}\right)
\le\frac{3310593057}{4294967296}<1.$$

従って $A\mid R$ は $R(q)=0$ を要求する。
$W\ne0$ なら $|R_4|\ge6ab^3$。低次部分と最高次の比は

$$\frac{\sum_{e<4}|R_e|q^e}{|R_4|q^4}
<\frac1{b^5}\left(28+\frac{52}{bq}+\frac{48}{(bq)^2}
 +\frac{22}{(bq)^3}\right)
\le\frac{29789195}{33554432}<1.$$

零になることはできない。評価は $b\ge2,q>b^6$ 全体を扱い、有限探索への外挿ではない。

## b≥2：四次係数が零の場合

$4\mid n$ なら $q$ は奇数。$b$ が奇数なら $a$ は偶数、半整数の $\beta$ は不可、$\theta=0$ の $W=b(a+b)-2d$ は奇数で零にならない。従って $W=0$ では **$b$ は偶数、$a$ は奇数**。

**$\theta=0,\beta=\varepsilon=\pm1$。** $d=b(a+b)/2$、$a\ge3b$。

$$R_3=-3\varepsilon b^3E_\varepsilon,\quad
E_+=a^2-8ac-b^2,\quad E_-=7a^2-8ab-8ac+b^2.$$

$E_\varepsilon=aK\pm b^2$、$K$ は奇数なので $E_\varepsilon$ は非零の奇数。
展開後の端点と単調性で

$$0<R_2\le30a^2b^2,\quad |R_1|\le24a^2b,\quad|R_0|\le12a^2$$

が従う。三次より下の比は

$$\frac a{|E_\varepsilon|}\left(\frac{10}{b^6}
 +\frac8{b^7q}+\frac4{b^8q^2}\right).$$

$b\ge4$ なら $a/|E|\le2b^2$ で、比は $671121409/8589934592<1$。
$b=2$ なら $a\ge7$、$|E|\ge a-4$、$a/|E|\le7/3$、$q>224$ で $502657/1376256<1$。従って $R(q)\ne0$。

**$\theta=1/2$。** $W=2(ab-d)\ge2b^2>0$ なので零の枝はない。

**$\theta=-1/2$。** $d=b^2$、$a\ge2b$。
$\beta=-1/2$ なら

$$R_3=-3b^3\{a(b+4c)-b^2\},\quad |R_3|\ge\tfrac32ab^4.$$

$|R_2|\le12a^2b^2,|R_1|\le3a^2b,|R_0|\le12a^2$ を使った低次の比は
$16417/262144<1$。これらは端点・二次式の頂点の符号証明書で再生する。

$\beta=1/2$ なら $E=a(b-4c)-b^2$、$R_3=-3b^3E$。
$E\le0$ の場合は他の三係数が正なので $R(q)>0$。
$E>0$ では $c<b/4$、$b-4c$ は正の偶数、$a/E\le b^2$。
$R_2\le(15/2)ab^3,R_1\le15ab^2,R_0\le6ab$ と $q>2b^6$ から低次の比は
$82561/1048576<1$。これで $b\ge2$ の全割当てが閉じる。

## b=1：まず整除条件と4の条件を使う

半整数の割当ては整数係数性に反する。定数の割当ては既に閉じた。従って
$\theta=0,\beta=\pm1$、$0\le c,d\le\Delta=a-1$、$0\le c+\beta\le\Delta$。

$G_6(q)=(q+1)(q^2+q+1)(q^2-q+1)$。$4\mid n$ は **$a$ が偶数、$q\equiv1\pmod4$** を要求する。$q>a$。

真の反例の完全素数冪 $q\Vert Q_1$ なら **$3\nmid A$**。
$3\nmid q$ なら $G_6(q)\equiv0\pmod3$、$n\equiv2\pmod3$ である。
$q$ が3冪なら、$Q_1$ に3が現れるのは $v_3(n-1)\ge2$ の場合だけで、その完全性から $3\nmid(n-1)/q$。
従って第一条件の $A\mid3N$ から **$A\mid N$** が従う。

$$V=c+dq,\quad Z=a(q+1)-2V,\quad T'=\beta(Z-1),\quad R'=N-T'A.$$

$R'$ は整数四次式で

$$|R'_4|\le a(a+1),\quad |R'_3|\le3a^2,\quad
|R'_2|\le26a^2,\quad |R'_1|\le24a^2,\quad |R'_0|\le11a^2.$$

三次係数はそれぞれ

$$-a^2+2ac+ad-2d+d^2+1,$$
$$3a^2-2a-2ac-3ad+2d+d^2-1,$$

で、$c,d$ に関する単調性の端点が絶対値 $3a^2$ 以下を示す。
$q\ge9$ なら

$$\frac{|R'|}A<1+\frac3q+\frac{26}{q^2}+\frac{24}{q^3}
 +\frac{11}{q^4}\le\frac{11081}{6561}<2.$$

従って $h=R'/A\in\{-1,0,1\}$。$q=5$ は $a=2,4$ の全28商を整数評価し、第一条件の剰余が非零であることを別に確認する。

法4では $A\equiv3$。$V$ が偶数なら $N\equiv0,T'\equiv-\beta$ で **$h=\beta$**。
$V$ が奇数なら $N\equiv3,T'\equiv\beta$ で、$\beta=-1$ は不可、$\beta=1,h=0$ だけが残る。全64剰余配置を直接再生した。

## b=1：非零の商を大きさで閉じる

$V$ 偶数、$h=\beta$ では $N=\beta ZA$。$k=q+1,g=aq-1$ として

$$A_3=A-gkq^3=\Delta(1+q+q^2)+aq^3,$$

$$\beta C-gk^2q^2=ZA_3.$$

$0<C\le gk^2\Delta$、$Z\ge(2-a)k$ なので、左辺は $-gk^2(q^2-\Delta)$ 以下、右辺は $-(a-2)kA_3$ 以上。しかし

$$gk(q^2-\Delta)>(a-2)A_3.$$

実際 $gk>\Delta q^2$、$q^2-\Delta>q(q-1)$、$A_3<aq^4/(q-1)$ を使えば、必要な差は

$$\Delta(q-1)^2-a(a-2)q
=\Delta(q-a-1)^2+a^2(q-a-1)+2a>0$$

に戻る。この枝は全 $q>a$、両符号で不可能。

## b=1：零の商を全奇素数の Kummer 条件で閉じる

最後は $V$ 奇数、$\beta=1,h=0$、$R'(q)=0$。
$s=c-d$ は奇数で

$$R'(-1)=-(s+1)^2,\qquad J(-1)=-3s,\qquad
J'(-1)=3(3c-4d+1).$$

従って $q+1\mid(s+1)^2$。
もし奇素数 $p\ge5$ が $q+1$ を割れば、$s\equiv-1\pmod p$、$j\equiv3\pmod p$、$n\equiv2\pmod p$。
$p\mid\binom n3$ である一方、Kummer の無繰上げ条件は $j\bmod p\in\{0,1,2\}$ を要求し、矛盾する。

$q\equiv1\pmod4$ だから $v_2(q+1)=1$。他の奇素数を排除したので

$$q+1=2\cdot3^e,\qquad e\ge1.$$

$q\equiv-1\pmod3$ に対し

$$\Phi_6(-1+3t)=3-9t+9t^2$$

だから $v_3(\Phi_6(q))=1$、$v_3(n-2)\ge e+1$。
従って3も共通候補素数で、最初の $e+1$ 個の3進桁は $n\equiv2\pmod{3^{e+1}}$。無繰上げから

$$j\bmod3^{e+1}\in\{0,1,2\}.$$

整数係数の Taylor 展開と $q=-1+2\cdot3^e$、上の $J'(-1)$ より

$$j\equiv-3s\pmod{3^{e+1}}.$$

二次以上の項は $3^{2e}$ の倍数であり $2e\ge e+1$。$j$ は3の倍数なので上の許容剰余は0だけ。従って $3^e\mid s$。
一方 $q+1\mid(s+1)^2$ は $3\mid s+1$ を要求し、矛盾する。これで最後の枝も閉じた。

## 検算の意味と残る境界

    python -X utf8 scripts/audit_i3_quadratic_cofactor.py
    python -X utf8 scripts/audit_i3_sextic_partial_sharing.py

六つの圧縮恒等式、30係数ノルム、四次係数が零の全形、端点・単調性・頂点の符号証明書、六つの狭義な有理上界、$b=1$ の二つの四次式、負根・微分・正の二次式・付値の恒等式、全64剰余配置と全28小底例外を再生する。

最後の Kummer 論証は全奇素数・全指数を扱う紙上証明であり、有限の $a,q$ の探索で置き換えていない。単一の底の桁条件だけでは最後の議論は使えない。2については無繰上げを要求しない。

先行稿の $b=2,m=6$ の半整数の根値の例も、この新定理の形に含まれ、数値反例から排除された。因子の割当ての分類が先行稿と異なる点は保持する。
一般の非共有因子を持つ配置、他の次数での複数割当て、任意の共有多項式の複数割当て、増大する桁和は残る。新たな完全解決添字は0である。
