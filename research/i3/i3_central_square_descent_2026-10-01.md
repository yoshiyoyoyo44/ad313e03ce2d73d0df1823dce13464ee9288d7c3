# i=3：中央群の二段平方降下と、中央飽和の 11/15 境界の排除

2026年10月1日。基点 **9428c54**。
[前稿の半比率・中央群の下限](i3_half_ratio_and_central_saturation_bounds_2026-10-01.md) ·
[先行する中央飽和の平方類](i3_octic_saturation_and_pell_2026-10-01.md) ·
[検算器](../../scripts/audit_i3_central_square_descent.py) ·
[検算結果](../../data/results/verification_i3_central_square_descent.json)

**一般の数値問題 i=3 は未解決である。** 今回は中央群の平方恒等式の剰余を二段追い、次の全次数の必要条件を証明する。

1. $t\ne1/2$ の全分配に、

   $$7h\le6u-v\quad\text{または}\quad4h\ge3u-v+d_1\quad\text{または}\quad15h+4v\ge11u+4d_1.$$

2. 均衡かつ中央飽和 $v=u,d_1=u$ には、**全比率で $h>11u/15$**。
   等号も全次数で排除する。前稿の全比率 $h>5u/7$ を強化した。

数値候補が必ず多項式条件へ移ることを仮定していない。
今回の「降下」は多項式の平方の剰余を順次低次数へ移す操作であり、元の整数反例を小さい整数反例へ移す操作ではない。

## 1. 入力と前稿の平方恒等式

$F,J\in\mathbb Z[X]$ は非負係数、$F(0)=2$、係数ごとに $0\le J\le F$ とし、既存の桁多項式還元の入力

$$F-1\mid J(J-1),\qquad F-2\mid J(J-1)(J-2)\quad\text{in }\mathbb Q[X]$$

を満たす。非自明な分配を

$$F-1=UV,\quad U\mid J,\quad V\mid J-1,\quad U(0)=V(0)=1,$$
$$J=1+V(tU+H),\quad UC-VH=1,$$
$$u=\deg U\le v=\deg V<2u,\quad0<h=\deg H<u,\quad0<t<1$$

と正規化する。定数差は既存の二次・三次合成の数値排除で処理済み。
$u,v,h$ は多項式の次数であり、数値の2進付値ではない。

完全な因子冪を保持した中央群を $D=D_1=\gcd(F-2,J-1)$、$d=\deg D$ とする。
前稿と同じく $D$ はモニック、$d\le u$。以下 $t\ne1/2$ とし、

$$\rho=t(1-t)>0,\quad\sigma=2t-1\ne0,\quad\sigma^2=1-4\rho,$$
$$A=(tU+H)/D,\quad B=((1-t)V-C)/D,\quad E=AB,$$
$$Q=(1-t)AC-tBH,\quad R=tAC-(1-t)BH,$$
$$S=(DR-1)/(DE+R),\quad P=R-SE,\quad K=\rho P-\sigma^2Q$$

は全て有理係数多項式である。$E$ の最高次係数は正である。
前稿で、根の重複度に上限を設けず

$$DP=SR+1,\qquad \gcd(Q,K)=1,$$
$$\boxed{W^2=\sigma^2Q^4+KQ^3+4\rho KEQ-K^2E},\qquad W=(KR-\rho PQ)/\sigma\tag{1}$$

を証明した。正確な次数は

$$\ell=\deg Q=2h+v-u-d,\quad k=\deg K=3h+v-2u-d\ge0,$$
$$e=\deg E=u+v-2d\ge0,\quad\ell-k=u-h>0.\tag{2}$$

以下では $W$ の符号を必要なら変え、最高次係数が $\sigma Q^2$ と一致するようにする。

## 2. 第一の平方差：次数 $r=3k-\ell$

今回は

$$\boxed{e<r:=3k-\ell<k}\tag{3}$$

という範囲を扱う。特に $k>r>0$、$\ell>2k$ である。

$$W_0=\sigma Q^2+\frac{KQ}{2\sigma}-\frac{K^2}{8\sigma^3}$$

と置くと、前稿の厳密な平方差は

$$W^2-W_0^2
=KQ\left(4\rho E+\frac{K^2}{8\sigma^4}\right)-K^2E-\frac{K^4}{64\sigma^6}.\tag{4}$$

$e<r<k$ なので、右辺の最高次項は $K^3Q/(8\sigma^4)$、次数は $3k+\ell$。
$\deg(W+W_0)=2\ell$ より

$$\delta:=W-W_0\ne0,\qquad\boxed{\deg\delta=r=3k-\ell.}\tag{5}$$

ここで $\delta$ は定数ではない。
$W=W_0+\delta$ を(1)へ代入すると、$Q$ に関する二次式

$$aQ^2+b(K)Q+c(K)=0,\tag{6}$$
$$a=2\delta\sigma,$$
$$b(K)=\delta K/\sigma-K^3/(8\sigma^4)-4\rho EK,$$
$$c(K)=K^4/(64\sigma^6)+(E-\delta/(4\sigma^3))K^2+\delta^2$$

を得る。係数に $\delta,E$ が含まれてよい。
判別式を $\Delta=b(K)^2-4ac(K)$ とすると

$$Z^2=\Delta,\qquad Z=\pm\{2aQ+b(K)\}.\tag{7}$$

## 3. 第二の平方差：次数 $s=2r-k$

$$Z_0=-\frac{K^3}{8\sigma^4}+\left(\frac{3\delta}{2\sigma}-4\rho E\right)K$$

と置く。直接の恒等式は

$$\boxed{\Delta-Z_0^2
=\delta K^2\left(\frac{3\delta}{4\sigma^2}+\frac{4E(\rho-2\sigma^2)}\sigma\right)-8\sigma\delta^3.}\tag{8}$$

$e<r<k$ より右辺の最高次項は $3\delta^2K^2/(4\sigma^2)$、次数は $2r+2k$。
$\Delta$ の最高次項は $K^6/(64\sigma^8)$ なので、$Z$ の符号を $Z_0$ に合わせれば $\deg(Z+Z_0)=3k$。
従って

$$\varepsilon:=Z-Z_0\ne0,\qquad\boxed{\deg\varepsilon=s=2r-k\ge0.}\tag{9}$$

$s<0$ なら、非零多項式の次数が負になるため、この段階で排除される。
中央飽和に特殊化するだけでも $h\ge8u/11$ を与えるが、次の恒等式がさらに強い。

## 4. 三つ目の低次数多項式と全中央群の追加制限

定数を

$$b_0=16\sigma^3(\rho-2\sigma^2)$$

とし、

$$\Lambda=\varepsilon K+3\sigma^2\delta^2+b_0E\delta\tag{10}$$

と置く。(8)へ $Z=Z_0+\varepsilon$ を代入して整理すると、厳密に

$$\boxed{\begin{aligned}
\varepsilon^2={}&\Lambda\left(\frac{K^2}{4\sigma^4}+8\rho E-\frac{3\delta}\sigma\right)
+\sigma\delta^3\\
&+24\sigma^2(\rho-4\sigma^2)E\delta^2
-128\sigma^3\rho(\rho-2\sigma^2)E^2\delta.
\end{aligned}}\tag{11}$$

右辺の $\Lambda$ を含まない三項では、$e<r$ より最高次項は $\sigma\delta^3$、次数は $3r$。
左辺の次数は $2s=4r-2k<3r$。$\Lambda$ に掛かる多項式の次数は $2k$。
従って、$\Lambda=0$ は不可能であり、

$$\boxed{\deg\Lambda=3r-2k\ge0.}\tag{12}$$

よって(3)の範囲には $3r\ge2k$、同値に $7k\ge3\ell$ が必要となる。
元の次数で

$$e<r\iff7h>6u-v,$$
$$r<k\iff4h<3u-v+d,$$
$$7k\ge3\ell\iff15h+4v\ge11u+4d.$$

従って全 $t\ne1/2$ の中央群に、次の三分岐の必要条件が成立する。

$$\boxed{7h\le6u-v\quad\text{または}\quad4h\ge3u-v+d_1\quad\text{または}\quad15h+4v\ge11u+4d_1.}\tag{13}$$

これは固定次数の計算結果からの外挿ではない。$E$ が非定数でも、(3)では最高次の比較が厳密である。

## 5. 均衡の中央飽和：全比率で $h>11u/15$

$v=u,d_1=u$ なら $A,B,E$ は非零定数で、$E>0$。
$t\ne1/2$ には前稿の $h>5u/7$ がある。
既に $h\ge3u/4$ なら $h>11u/15$ なので、$h<3u/4$ を考えればよい。
この範囲では(3)が成立し、(12)から

$$h\ge11u/15.\tag{14}$$

### 5.1 等号の正確な次数と四次式

等号 $h=11u/15$ では

$$k=u/5,\quad\ell=7u/15,\quad r=2u/15,\quad s=u/15>0,$$
$$\deg\Lambda=0.$$

$\Lambda=\lambda\in\mathbb Q^\times$ と置く。

$$B_0=16E\sigma^3(\rho-2\sigma^2),$$
$$a_0=24E\sigma^2(\rho-4\sigma^2),\qquad
c_0=-128E^2\sigma^3\rho(\rho-2\sigma^2)$$

と略記する。(10)から

$$\varepsilon K=\lambda-3\sigma^2\delta^2-B_0\delta.$$

これを(11)へ代入し、$\varepsilon^2$ を掛ければ

$$f(\delta,\varepsilon)=0,\tag{15}$$
$$\begin{aligned}
f(D,Y)={}&\frac\lambda{4\sigma^4}(\lambda-3\sigma^2D^2-B_0D)^2\\
&+Y^2\left\{\sigma D^3+a_0D^2+c_0D
+\lambda(8E\rho-3D/\sigma)-Y^2\right\}.
\end{aligned}$$

ここで $\deg\delta=2s$、$\deg\varepsilon=s$。

### 5.2 非定数剰余は次数で排除される

(15)の次数 $8s$ の二項は $(9\lambda/4)\delta^4$ と $\sigma\varepsilon^2\delta^3$。
最高次係数から

$$\delta=a\varepsilon^2+T,\qquad a=-4\sigma/(9\lambda),\quad\deg T<2s.$$

$D=aY^2+T$ を $f$ に代入すると、$Y^6$ の係数は

$$-\frac{16\sigma^3}{81\lambda^2}\left(T-\frac{8E\sigma(5\rho-28\sigma^2)}3\right).\tag{16}$$

他の項は $Y^4$ と高々二次の $T$、$Y^2$ と高々三次の $T$、$Y^0$ と高々四次の $T$ からなる。
もし $0<m=\deg T<2s$ なら、(16)の最高次は $6s+m$。
他の項の次数は高々 $\max\{4s+2m,2s+3m,4m,6s\}<6s+m$。
従って相殺できない。$T$ は定数でなければならない。
さらに(16)から

$$\boxed{\delta=a\varepsilon^2+c,\qquad c=8E\sigma(5\rho-28\sigma^2)/3.}\tag{17}$$

### 5.3 定数項と四次項が同時には消えない

$f(aY^2+c,Y)$ が恒等的に零なら、$Y^4$ と定数項も零である。
厳密にその係数は

$$[Y^4]f=\frac{N_4}{81\lambda},\qquad
[Y^0]f=\frac\lambda{36\sigma^4}N_0^2,$$

$$N_4=17152E^2\rho^2\sigma^4-123904E^2\rho\sigma^6+262144E^2\sigma^8+3\lambda,$$
$$N_0=2240E^2\rho^2\sigma^4-22784E^2\rho\sigma^6+57344E^2\sigma^8-3\lambda.$$

$\lambda\ne0$ より $N_4=N_0=0$ が必要だが、その和は

$$N_4+N_0=192E^2\sigma^4\{101\rho^2-764\rho\sigma^2+1664\sigma^4\}.$$

中括弧は

$$\frac{(101\rho-382\sigma^2)^2+22140\sigma^4}{101}>0$$

であり、$E\ne0,\sigma\ne0$ のため和は非零。矛盾する。
従って $h=11u/15$ は、次数にも有理パラメータにも上限を置かず不可能。

半比率 $t=1/2$ の中央飽和には既存の $h>3u/4$ がある。
合わせて

$$\boxed{v=u,\ d_1=u\quad\Longrightarrow\quad h>11u/15\quad\text{（全比率）}.}\tag{18}$$

| $u$（$\deg F=2u$） | 前稿 $h>5u/7$ の最小整数 | 今回 $h>11u/15$ の最小整数 |
|---|---|---|
| 12 | 9 | 9 |
| 18 | 13 | 14 |
| 30 | 22 | 23 |
| 60 | 43 | 45 |

例えば次数36の中央飽和で $h=13$、次数60の中央飽和で $h=22$ を新たに排除する。
次数36や60の全分配を排除した結論ではない。
表は整数丸めの例示であり、全次数の証明の代用ではない。

## 6. 検算と、なお未解決の範囲

    python scripts/audit_i3_central_square_descent.py

検算器は二つの平方差、二次式と判別式、三つ目の剰余のノルム恒等式、
等号の四次式への消去、(16)(17)と $N_4,N_0$ の係数、正の二次式への還元を全て厳密演算で再生する。
次数の診断では、条件(3)の範囲・元の次数の三分岐との同値・中央飽和の整数丸めを確認する。
有限の次数診断は誤記検出用で、全次数の排除は第2〜5節の紙上証明による。

未解決なのは、なお高い差次数の一般分配、奇数のチェビシェフ芯 $D=5^a,a\ge4$ の全整数評価、一般数値領域への移行である。
前稿に示した奇数芯は、正次数 $a$ と整数 $q\ge3$ について

$$u=qa,\quad v=(q+1)a,\quad h=(q-1)a,\quad d_1=u.$$

従って $e=\deg E=a>0$、$k=(q-2)a$、$r=(2q-5)a\ge k$ である。
今回の $e<r<k$ に入らず、(13)の第二分岐を満たす。
従って5冪の残る芯を閉じたとは主張しない。

同じ剰余追跡を無限回反復できる証明は得ていない。
中央飽和の $k,r,s,\deg\Lambda$ は順に $3h-2u,7h-5u,11h-8u,15h-11u$ で、差はいずれも $4h-3u$。
この四項の形だけから、全反復に同じ次数則を仮定することはできない。
今回の有限段の下限から、$h\ge3u/4$ や全ての差次数の排除へ外挿してはいけない。
新たな完全解決添字は0、一般の $i=3$ と問題699全体は未解決である。
