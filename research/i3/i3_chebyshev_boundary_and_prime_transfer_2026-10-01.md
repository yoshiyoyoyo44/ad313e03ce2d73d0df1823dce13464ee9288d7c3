# i=3：全分配のノルム降下と、非均衡境界のチェビシェフ分類

2026年10月1日。基点 **60d80f9**。
[全残余群の微分と二群ノルム降下](i3_residual_differential_and_norm_descent_2026-10-01.md) ·
[検算器](../../scripts/audit_i3_chebyshev_boundary.py) ·
[検算結果](../../data/results/verification_i3_chebyshev_boundary.json)

**一般の数値問題 i=3 は未解決である。** 固定次数の計算を増やすのでなく、以下を全次数で証明する。

1. ノルム降下を、二つの一次残余群という条件を外して全分配に適用する。各正次数群に明示的な次数下限を得る。
2. 非均衡分配の最小境界は、三配置のチェビシェフ型の合成に限られる。そのうち二配置は、原点の有理性と正実軸の条件で全排除する。
3. 残る配置は、芯の次数 $D$ に3または7以上の素因数があれば、その素数が全ての整数評価で共有される。
4. $D=5^a$ にも、$n$ の奇数部分とパラメータの5進合同条件を全 $a$ で与える。$D=5$ は既存稿で排除済みだが、$a\ge2$ は本稿では閉じていない。

最小境界の全閉鎖、全桁多項式の排除、全数値候補の排除を主張するものではない。

## 1. 全分配を同じノルムへ送る

前稿と同じ記号を使う。

$$F-1=UV,\quad U\mid J,\quad V\mid J-1,\quad U(0)=V(0)=1,$$
$$u=\deg U\le v=\deg V,\quad
J=1+V(tU+H),\quad h=\deg H<u,\quad 0<t<1,$$
$$r_s=s-1-t,\quad z=1-3t,\quad
H-r_sU=D_sR_s,\quad d_s=\deg D_s\le u,$$
$$\sum_s d_s=u+v,\quad
(u+v)t=u+d_2-d_0,\quad
H^3+R=zH^2U+U^2W,\quad R\sim R_0R_1R_2.$$

$D_s$ は $F-2$ の完全な因子冪の群である。各 $R_s$ の重根、および同じ群の $D_s,R_s$ の共通根を許す。
$U,H,R$ は二つずつ互いに素。$H$ は非零で、$\deg W<h$。$h=0$ の場合も次数比較で $W=0$ となる。

任意の $\epsilon$ について $e=d_\epsilon>0$ とし、$M=D_\epsilon$ をモニックにする。
定数の調整を $Q$ に含めて

$$H-r_\epsilon U=QM,\quad
W-\kappa_\epsilon H=LQ,\quad
\kappa_\epsilon=r_\epsilon(r_\epsilon-z).$$

既存の残余整除性から $L\in\mathbb Q[X]$。平方を完成すると

$$\tau=(r_\epsilon-z)/2,\quad
B=H+\tau U,\quad A=\tau^2M+L,\quad N=R/Q$$

に対し

$$\boxed{AU^2-MB^2=N,\quad B-cU\equiv0\pmod M},\quad
c=(3\epsilon-4)/2,\tag{1}$$
$$\boxed{\nu:=\deg N=u-v+e,\quad 0\le\nu\le e.}\tag{2}$$

$M,N$ は互いに素。異なる群の根では $H/U$ の値が異なるためであり、単根という仮定は要らない。
$N$ のうち $R_s$ の根では $B/U=\beta_s=s+\epsilon/2-2$、$s\ne\epsilon$。

| $\epsilon$ | $\tau$ の範囲 | $c$ | 他の二群の $\beta_s$ |
|---|---|---|---|
| 0 | $-1<\tau<0$ | $-2$ | $-1,0$ |
| 1 | $-1/2<\tau<1/2$ | $-1/2$ | $-3/2,1/2$ |
| 2 | $0<\tau<1$ | $1$ | $-1,0$ |

常に $\beta_s^2\ne\tau^2$。$N$ の根で(1)を評価すると $L=(\beta_s^2-\tau^2)M$ なので

$$\boxed{L\ne0,\quad\gcd(L,MN)=1.}\tag{3}$$

$L=0$ なら(1)は $M\mid N$ を要求するので不可能。$M,L$ の共通根も $\gcd(M,N)=1$ に反する。
$\epsilon=1,t=1/2$ を除けば $\tau,\kappa_\epsilon$ は非零なので

$$\boxed{\delta:=\deg L=h-u+e,\quad 0\le\delta<e.}\tag{4}$$

中央の例外は $\tau=\kappa_\epsilon=0$。その最小境界 $h=u-e$ では $\deg W<h=\deg Q$ なので $L=W/Q=0$ となり(3)に反する。
以下の行列の次数式を、この例外へ適用してはいない。

## 2. 全分配に対する次数下限

$\tau\ne0$ とする。前稿と同じ行列

$$
\binom{U_{r+1}}{B_{r+1}}=
\begin{pmatrix}A+\tau^2M&-2\tau M\\-2\tau A&A+\tau^2M\end{pmatrix}
\binom{U_r}{B_r},\quad(U_0,B_0)=(U,B)
$$

は

$$AU_r^2-MB_r^2=L^{2r}N,\quad
B_r\equiv(c-2r\tau)U_r\pmod M.\tag{5}$$

無限遠の形式級数 $S=\sqrt{A/M}$ の枝を $S\sim\tau$ と選べば
$\deg(U+B/S)=u$、$\deg(U-B/S)=\nu-e-u$。
固有値 $M(S-\tau)^2,M(S+\tau)^2$ の次数は $2\delta-e,e$。従って重根を含めて厳密に

$$\boxed{\max(\deg U_r,\deg B_r)
=\max\{u-r(e-2\delta),\ re-v\}.}\tag{6}$$

**$\delta>0$ のとき、(6)は全 $r\ge1$ で $e$ 以上。**
(3)と法 $L$ の(1)から $M(B-\tau U)(B+\tau U)$ は単元。
行列を反復すると

$$U_r\equiv-2\tau M(B-\tau U)(4\tau^2M)^{r-1}\pmod L,$$

なので $\gcd(U_r,L)=1$。
もし(6)が $e$ 未満なら(5)は等式 $B_r=c_rU_r$ となり

$$U_r^2\{(\tau^2-c_r^2)M+L\}=L^{2r}N.$$

$L^{2r}$ は中括弧を割らねばならない。法 $L$ で $c_r^2=\tau^2$ を得るが、それでは中括弧が $L$ 自身となり $\delta>0,2r>1$ に矛盾する。
$r_*=\lceil v/e\rceil$ なら $0\le r_*e-v<e$。従って

$$\boxed{h\ge u-e+
\left\lceil\frac{e(r_*+1)-u}{2r_*}\right\rceil,\quad
r_*=\left\lceil\frac ve\right\rceil.}\tag{7}$$

これは全分配の正次数群に対する下限。ただし $\delta=0$ の分岐は次節で別に処理し、中央 $t=1/2,\epsilon=1$ にこの式を適用してはいない。
二つの一次残余群の場合には $v=u+e-2$ となり、前稿の下限を含む。平方因子を除いたり、曲線の滑らかさを仮定したりする必要はない。

## 3. 最小境界の分類

$h=u-e$、すなわち $\delta=0$ とする。$L$ と行列式 $L^2$ は非零定数。
$\gcd(U,B)=\gcd(U,H)=1$ は全反復で保たれる。
$r=\lceil v/e\rceil$ で(6)は $e$ 未満となるので $B_r=c_rU_r$。
互いに素であるため $U_r,B_r$ は定数。従って

$$\nu=\deg\{(\tau^2-c_r^2)M+L\}\in\{0,e\}.\tag{8}$$

**非均衡分配 $v>u$ では $\nu<e$、従って $\nu=0$。**
群の次数の和から

$$\boxed{e=v-u,\quad d_a=d_b=u\ (a,b\ne\epsilon).}\tag{9}$$

また(6)が0という結論から $e\mid v$、従って $e\mid u$。
$q=u/e\ge1,D=2q+1$ と置けば

$$u=qe,\quad v=(q+1)e,\quad\deg F=De.$$

$q$ 回の反復で

$$U_q=\alpha,\quad B_q=\tau\alpha,\quad
\alpha\in\mathbb Q^\times,\quad N=L\alpha^2.\tag{10}$$

最後の比は $(u+v)t=u+d_2-d_0$ と $c-2q\tau$ から得られる。

**均衡分配 $v=u$** では $\nu=e$。同じ次数式から $e\mid u$ が必要。
他の二つの $R_s$ がともに非定数なら、それらの根で行列は相異なる比 $\beta_a,\beta_b$ を保つ。
行列式が単元なので $U_r$ はそれらの根で非零。定数の比 $B_r/U_r$ が二つの値になることはない。
従って均衡境界には

$$\boxed{\{d_a,d_b\}=\{u,u-e\},\quad e\mid u}\tag{11}$$

が必要。ここでは(11)を満たす全均衡境界を排除していない。

## 4. 非均衡境界の三つの芯

以下は(9)の場合。$w=1+2\tau^2M/L$ と置き

$$\mathcal P=T_q(w)+(w-1)\mathcal U_{q-1}(w),\quad
\mathcal Q=T_q(w)+(w+1)\mathcal U_{q-1}(w).$$

$T_q,\mathcal U_{q-1}$ は第一種・第二種チェビシェフ多項式。
$L$ で割った行列の逆行列は

$$\begin{pmatrix}w&(w-1)/\tau\\\tau(w+1)&w\end{pmatrix}.$$

その $q$ 乗を(10)に作用させると

$$\boxed{U=\alpha\mathcal P,\quad B=\alpha\tau\mathcal Q,\quad
H=\alpha\tau(\mathcal Q-\mathcal P).}\tag{12}$$

これは内側 $w\in\mathbb Q[X]$ の係数に符号条件を課さない合成分類である。
$F-2$ は $M(B-\beta_aU)(B-\beta_bU)$ の定数倍。
法 $U$ では $MB^2=-N$ なので、$U\mid F-1$ はその定数を $1/N$ と決定する。

| $\epsilon$ | $t$ | $\tau$ | $F-2$ |
|---|---|---|---|
| 0 | $(D-2)/D$ | $-2/D$ | $(w-1)\mathcal Q(2\mathcal Q-D\mathcal P)/4$ |
| 1 | $(D-1)/(2D)$ | $-1/(2D)$ | $-(w-1)(3D\mathcal P-\mathcal Q)(D\mathcal P+\mathcal Q)/2$ |
| 2 | $1/D$ | $1/D$ | $(w-1)\mathcal Q(D\mathcal P+\mathcal Q)/2$ |

全配置で

$$J=1+(F-1)\left\{(2-\epsilon)/2+
\tau\mathcal Q/\mathcal P\right\}.\tag{13}$$

$F-1$ は $\mathcal P$ で割り切れるので(13)は多項式。

## 5. 二配置を原点の有理性で全排除する

$F$ は非定数で非負係数、$F(0)=2$ なので全ての $X>0$ で $F(X)>2$。
配置0,1の芯は奇数次数で最高次係数が負だから $X\to+\infty$ で $w(X)\to-\infty$。
従って $w(0)\in\mathbb Q$ は $F-2$ の最小実根でなければならない。他の根から出発すると、正の $X$ で最小根を横切り $F(X)=2$ となる。

### 配置0

$\mathcal Q$ の根は $\cos(2k\pi/D)$、$\mathcal P$ の根は $\cos((2k-1)\pi/D)$、$1\le k\le q$。
最小の $\mathcal Q$ の根は $w_{\min}=-\cos(\pi/D)$。
その左では因子ごとの比較から $\mathcal P/\mathcal Q>1$。
従って $2\mathcal Q-D\mathcal P$ にそれより左の根はなく、$w_{\min}$ が $F-2$ の最小実根。
$D\ge5$ では $2\cos(\pi/D)$ は有理数なら整数となる代数的整数だが、1と2の間にあり有理数ではない。
原点の有理性に反する。$D=3$ は $v=2u$ の[既存の三次合成・共通素数3の証明](i3_extremal_split_closeout_2026-09-30.md)で排除済み。

### 配置1：有理根の分母を制限する

恒等式

$$D\mathcal P+\mathcal Q=2\{(w-1)\mathcal Q\}'\tag{14}$$

より、この式の根は $\mathcal Q$ の根と1の間に一つずつある。
最小根は最小の $\mathcal Q$ の根と最小の $\mathcal P$ の根の間：

$$\boxed{-\cos(\pi/D)<w_{\min}<-\cos(2\pi/D).}\tag{15}$$

この区間では $\mathcal P/\mathcal Q<0$ なので $3D\mathcal P-\mathcal Q$ の根はない。
その左でも $\mathcal P/\mathcal Q>1$。従って(15)の根が $F-2$ の最小実根。

**分母補題。** $D\mathcal P(w)+\mathcal Q(w)=0$ の有理根 $w=a/b$ を既約、$b>0$ と書けば

$$\boxed{b\mid D+1.}\tag{16}$$

証明：$\lambda+\lambda^{-1}=2w$ とする。多項式恒等式

$$
\begin{aligned}
\Phi_D(\lambda)
&=(D+1)\lambda^{D+1}-(D-1)\lambda^D+(D-1)\lambda-(D+1)\\
&=\lambda^q(\lambda^2-1)
\{D\mathcal P((\lambda+\lambda^{-1})/2)
+\mathcal Q((\lambda+\lambda^{-1})/2)\}
\end{aligned}
$$

がある。奇素数 $\ell\mid b$ では、二次式 $\lambda^2-2w\lambda+1=0$ の一つの根が
$s=v_\ell(\lambda)=-v_\ell(b)<0$ を持つ。
$\Phi_D(\lambda)=0$ の四項のうち、低い二項の付値は対応する高い二項より大きい。
従って高い二項が同じ付値でなければならず

$$s=v_\ell(D-1)-v_\ell(D+1).$$

$D-1,D+1$ の奇素因数は共通しないので $v_\ell(b)=v_\ell(D+1)$。
2について $v_2(b)=1$ なら自動的に $2\mid D+1$。
$v_2(b)\ge2$ なら $s=1-v_2(b)<0$ を用いて同じ比較をし、
$v_2(D-1)=1$、$v_2(b)=v_2(D+1)$ を得る。これで(16)。□

$D\ge21$ では(15)と $\pi^2<10$ から

$$0<1+w_{\min}<1-\cos(2\pi/D)
<20/D^2<1/(D+1).$$

しかし有理根なら(16)から $1+w_{\min}\ge1/b\ge1/(D+1)$。矛盾。
残る $D=5,7,9,11,13,15,17,19$ は、$b\mid D+1$、$-b<a<b$、$\gcd(a,b)=1$ の200候補の全てで
$b^q(D\mathcal P+\mathcal Q)(a/b)\ne0$。
検算結果に原始多項式と非零の整数値を保存した。
この有限部分は、解析的な上界で残った全例外の検証。
$D=3$ は配置0と同じ既存稿で排除済み。

**非均衡最小境界の配置0,1は全次数・全係数で排除された。**

## 6. 配置2の原点と、内側の全係数の整数性

残る芯を

$$\begin{aligned}
f_D(w)&=2+\frac{w-1}{2}\mathcal Q(D\mathcal P+\mathcal Q)
=\frac{T_D(w)+D(w-1)\mathcal U_{D-1}(w)+3}{2},\\
j_D(w)&=\frac{w+1}{2D}\mathcal P(D\mathcal P+\mathcal Q)
=\frac{T_D(w)+(w+1)\mathcal U_{D-1}(w)/D+1}{2}
\end{aligned}\tag{17}$$

と書く。$D$ は奇数。
(14)により $f_D-2$ の全実根は1以下で最大実根は1。
最高次係数が正なので $w(X)\to+\infty$。第5節と同じ横断の議論から

$$w(0)=1,\quad \alpha=1.\tag{18}$$

$x=w-1$ と置く。内側の係数を最初から非負整数とは仮定していない。
$\mathcal P,\mathcal Q\equiv1\pmod2$ なので $f_D,Dj_D\in\mathbb Z[w]$。

$$[x]f_D(1+x)=D^2,\quad
[x^D]f_D(1+x)=(D+1)2^{D-2},\quad
\gcd(D^2,(D+1)2^{D-2})=1.$$

$f_D(1+x)$ の非定数係数の最大公約数は1。
**このことと $x(0)=0$ から $x\in\mathbb Z[X]$ が従う。**
素数 $\ell$ において $x$ の係数の最小付値が負なら
$x=\ell^{-b}y$、$b>0$、$\bar y\in\mathbb F_\ell[X]$ 非定数と書ける。
$f_D(1+Y)=\sum f_kY^k$ の $\mu=\min_k\{v_\ell(f_k)-bk\}$ は、非定数係数が原始的なので負。
$\ell^{-\mu}f_D(1+x)$ の還元は、非零多項式を非定数 $\bar y$ に合成したものとなり0にはならない。
$F\in\mathbb Z[X]$ に矛盾する。

$\ell\mid D$ なら $Dj_D$ の最高次係数は法 $\ell$ で非零。
$Dj_D(1+x(X))=DJ(X)\equiv0\pmod\ell$ なので、合成の次数比較から $\bar x$ は定数。
$x(0)=0$ より $\bar x=0$。従って

$$\boxed{x\in\operatorname{rad}(D)\mathbb Z[X],\quad x(0)=0.}\tag{19}$$

許容整数評価 $n\ge8,4\le j\le n/2$ では $w$ は整数。
$w\le-1$ では $f_D(w)\le1-D^2<0$、
$w=0$ では $j_D(0)=(1+(-1)^q/D)/2$ が非整数、
$w=1$ では $n=2$。従って $w\ge2,x>0$。
$w\le-1$ の評価は $T_D(w)\le-1$、$\mathcal U_{D-1}(w)\ge D$ による。

## 7. 全整数評価での共通素数3・7以上

$x=w-1$、$P=\mathcal P(1+x)$、$B_0=\mathcal Q(1+x)/D$ と書く。
添字0は正規化を表し、第1節の $B$ と区別する。

$$a_k=2^k\binom{q+k}{2k}\in\mathbb Z,\quad
P=\sum_{k=0}^q a_kx^k,\quad
B_0=\sum_{k=0}^q\frac{a_k}{2k+1}x^k.\tag{20}$$

これは三角式を微分して得る

$$x(x+2)P''+(2x+1)P'-q(q+1)P=0,$$
$$x(x+2)B_0''+(2x+3)B_0'-q(q+1)B_0=0$$

と $P(0)=B_0(0)=1$ の係数比較から従う。
次の恒等式が成り立つ：

$$\begin{aligned}
(x+2)P^2-D^2xB_0^2&=2,\\
n-2&=xD^2B_0(P+B_0)/2,\\
j&=(x+2)P(P+B_0)/2,\\
j-1&=B_0\{(x+2)P+D^2xB_0\}/2.
\end{aligned}\tag{21}$$

$[x]\{j-2\}=(5D^2+1)/6$。
(20)(21)から、$x^k$ の係数の $\ell$ 進付値は
$-\lfloor\log_\ell(2k+1)\rfloor$ 以上。

**$\ell\ge7$、$\ell\mid D$。**
$a=v_\ell(D)\ge1,b=v_\ell(x)\ge1$。
$P,B_0\equiv1\pmod\ell$。一次係数は単元で、
$k\ge2$ では $\lfloor\log_\ell(2k+1)\rfloor\le k-2$ なので高次項の付値は $b+1$ 以上。
従って

$$v_\ell(n-2)=b+2a,\quad v_\ell(j-2)=b.\tag{22}$$

法 $\ell^{b+1}$ で $n$ の剰余は2、$j$ の剰余は2より大きい。
Kummerの定理で $\ell\mid\binom nj$。
$\ell\mid n-2,\ell\nmid6$ より $\ell\mid\binom n3$ でもある。

**$3\mid D$。**
$a=v_3(D)\ge1,b=v_3(x)\ge1$。
$b\ge2$ なら $P,B_0\equiv1\pmod3$、
一次係数の付値は $-1$、高次項はそれより大きいので
$v_3(n-2)=b+2a$、$v_3(j-2)=b-1$。法 $3^b$ で同じ桁の矛盾が生じる。

$b=1$ なら $x=3y,3\nmid y$。
$[x]B_0=(D^2-1)/12$ と(20)から $P\equiv1,B_0\equiv1-y\pmod3$。

* $y\equiv1\pmod3$：$c=v_3(B_0)\ge1$ とすると(21)から
  $v_3(j-1)=c$、$v_3(n-2)=1+2a+c$。
* $y\equiv2\pmod3$：$c=v_3(P+B_0)\ge1$ とすると
  $v_3(j)=c$、$v_3(n-2)=1+2a+c$。

いずれも法 $3^{c+1}$ で $n$ の剰余は2、$j$ の剰余は2より大きい。
$n\ge8,j\ge4$ により使った付値は有限。
$v_3(n-2)\ge2$ なので、$\binom n3$ の分母6で3を一つ除いても共有される。

**配置2の芯の次数に3または7以上の素因数があれば、全整数評価で奇素数が共有される。**
合成の内側に負の係数があっても(19)と整数評価だけを使うので、この結論は変わらない。

## 8. 5の冪にも残る必要条件を一様に出す

以上から未排除の芯は $D=5^a$。
$a=1$ は(19)で $x=5K,K\in\mathbb Z[X]$、全許容整数評価で $K>0$ となり
[五次の全整数評価の排除](i3_quintic_closeout_2026-09-30.md)が適用できる。

全奇数 $D$ に対し

$$\boxed{\gcd(n,j)_{\rm odd}\mid D^2-1.}\tag{23}$$

証明：(19)から $p\mid D$ という奇素数は $n\equiv2\pmod p$ により $\gcd(n,j)$ を割らない。
$p^c\mid\gcd(n,j)$、$p\nmid2D$ とする。
$D\mathcal P+\mathcal Q$ が $p$ で0なら(17)から $n\equiv2$ となり矛盾。
また

$$f_D(w)-1=
\mathcal P(w)\{(w+1)\mathcal P(w)+D(w-1)\mathcal Q(w)\}/2$$

より $\mathcal P(w)$ も $p$ 進単元。
$p^c\mid j$ から $w+1\equiv0\pmod{p^c}$。
$f_D(-1)=1-D^2$ なので $p^c\mid D^2-1$。□

仮に数値反例なら、$p\ge5$ が $n$ を割る場合、Lucasの定理は $p^{v_p(n)}\mid j$ を要求する。
$3^b\Vert n,b\ge2$ でも同様。
$b=1$ の例外は、$3\nmid D$ のとき自動的に $3\mid D^2-1$、
$3\mid D$ のとき $3\nmid n$ で処理できる。従って

$$\boxed{n=2^uM,\quad M\ {\rm odd},\quad M\mid D^2-1.}\tag{24}$$

共通素数2を排除してはいない。反例の $4\mid n$ は既存の奇素数に関する還元による。

$D=5^a$ では $x=5y$。
$v_5(x)\ge2$ なら第7節と同じ一次項の比較から
$v_5(j-2)=v_5(x)<v_5(n-2)$ となり5が共有される。
残るのは $5\nmid y$。この場合 $P,B_0\equiv1\pmod5$ なので

$$v_5(n-2)=2a+1.\tag{25}$$

一次・二次の係数は

$$[x]\{j-2\}=(5D^2+1)/6,\quad
[x^2]\{j-2\}=(D^2-1)(7D^2+2)/60.$$

三次以上の項の付値は2以上なので

$$\{j_D(1+5y)-2\}/5\equiv y-y^2\pmod5.$$

5を共有しないためには、末尾が2の全 $2a+1$ 桁で $j\equiv2$ が必要であり

$$\boxed{y\equiv1\pmod5,\quad
j_D(1+5y)\equiv2\pmod{5^{2a+1}}.}\tag{26}$$

$S_D(Y)=\{j_D(1+5Y)-2\}/(5Y)\in\mathbb Z[Y]$、
$S_D(Y)\equiv1-Y\pmod5$ だから、Henselの持ち上げで(26)は
各 $a$ ごとにただ一つの $y\bmod5^{2a}$ に制限される。
整数係数であることは、$j_D$ の分母が5の冪のみであり、
$k-\lfloor\log_5(2k+1)\rfloor\ge1$ が全 $k\ge1$ で成り立つことから従う。
例：$D=5$ は $y\equiv6\pmod{25}$、$D=25$ は $y\equiv56\pmod{625}$。
一意な5進剰余が存在すること自体は、整数解が存在しない証明ではない。

## 9. 検算と未解決の範囲

    python scripts/audit_i3_chebyshev_boundary.py
    python scripts/audit_i3_residual_differential_and_norm_descent.py

新検算器は奇数次数3〜41の20組で三つの芯、整除条件、係数展開、微分、$\lambda$ の疎な恒等式を厳密な有理数で確認する。
配置1の全例外には200個の非零整数の証明書がある。
次数3〜75の888整数評価で、(23)、局所付値、およびKummer付値による1,160個の共有素数の確認を行った。
任意次数の根拠は本稿の証明であり、有限評価を一般の数値問題の証明としてはいない。

閉じたのは、非均衡最小境界の配置0,1と、配置2の $D$ が5の冪以外の全評価、および既存稿による $D=5$。
なお残るものは、配置2の $D=5^a,a\ge2$、(11)の均衡最小境界、(7)以上の差次数を持つ全分配、
そして多項式整除へ移行できない一般数値領域である。
$i=3$ 全体を閉じたとは結論しない。
