# 読む順序と分野別の案内

[入口](../README.md) · [現在地](STATUS.md) · [全成果の一覧](RESULTS_CATALOG.md) · [検算](VERIFICATION.md)

全ノートを日付順に読む必要はありません。まず[現在地](STATUS.md)を確認し、目的に応じて以下をたどってください。

## 現在の最優先：10月3日の i=5

全添字へ広げる最新の入口は[隣接行の桁降下](../research/general/adjacent_row_digit_descent_2026-10-03.md)。第2–5節で任意iの復元・正の実根・数値から多項式への移行、第6節で有界桁和・素数個数の上限、第7–9節でi=5の低い桁重みの全指数排除、第10節で全素数の行積への結合と最小桁和の二族の排除、第11節で未解決境界を確認します。全添字を解決した稿ではありません。

最新の[880分配と5の高桁条件](../research/i5/i5_odd_sparse_allocation_and_prime5_lift_2026-10-03.md)は、9類を研究する入口です。第2–5節で8セル以下の完全被覆、第6–7節で5の持ち上げと付値100・112、第8節でBFTを併用した全次数の容量の限界、第9節で残る一般域を確認してください。[検算器](../scripts/audit_i5_sparse_allocation.py)が全880証明書を再生します。9類全体の解決ではありません。

[ZIP統合後の最新稿](../research/i5/i5_global_product_and_affine_exclusions_2026-10-03.md)を追加しました。45類、小さいjと有理直線近傍を閉じ、必要合同類を9・64へ更新しています。復元余因子の不均衡と、古典的定理による非有効な有限性を、一般i=5の完全解決と区別してください。[新検算器](../scripts/audit_i5_global_product_and_affine.py)で整数閾値を再生できます。

同稿第9節はn−1,n,n＋1のいずれかが完全冪となる全域、およびn=3^f5^dの全域を閉じます。第10節は有効な指数条件の残る障壁、第11節は現在の証明義務です。

[AI引き継ぎ第0節](AI_HANDOFF_2026-10-02.md) → [i=5 の新証明](../research/i5/i5_multiplicity_frontier_2026-10-03.md) → [9証明書の検算器](../scripts/audit_i5_multiplicity_frontier.py)の順に読みます。行0最大、支持{0,3}の三次曲線による直接閉鎖、最後2支持の混合余因子上界、純冪の閉鎖、全次数容量障壁を区別します。さらに第13節で四次・六次と外部BFTにより支持02を閉じ、残る支持は01だけです。一般i=5は未解決です。

## 10月2日の先行稿

最初に[AI引き継ぎ](AI_HANDOFF_2026-10-02.md)で前提・全成果・未解決境界を確認します。
[任意二次商](../research/i3/i3_quadratic_cofactor_single_allocation_closeout_2026-10-02.md) → [六次部分共有](../research/i3/i3_sextic_partial_sharing_closeout_2026-10-02.md) → [奇素数接続](../research/i3/i3_odd_prime_gluing_and_even_multiplier_2026-10-02.md)が今回の続稿です。
[整数根値と全共有](../research/i3/i3_integral_root_values_and_split_geometric_closeout_2026-10-02.md)は保存済み本文をそのまま復元しました。

[任意の共有因子の閉鎖](../research/i3/i3_arbitrary_cofactor_closeout_2026-10-02.md)は先行する依存先です。
幾何級数への制限を外し、$F-2=(aX-1)B$ の全体の $B$ が一つの $J-s$ を割る場合を、三次以上の全次数で数値排除します。第2–3節で商の全三形、第4–6節で三次の完全な分岐と合同証明書、第7節で既約な $B$ の次数に依存しない底の上界を示します。依存先は以下の両隣接法の稿と、その幾何級数の三次の証明です。複数の添字への割当てなどは残り、一般の $i=3$ は未解決です。

## 10月1日の先行稿

[両隣接法の終結式と幾何級数族の閉鎖](../research/i3/i3_adjacent_resultants_and_geometric_closeout_2026-10-01.md)が依存先です。
一般数値領域で両法の全非共有部分を使い、因子の次数比が退化する幾何級数の共有族を、全次数・全係数で直接排除します。依存先は初等的還元と[前稿の終結式評価](../research/i3/i3_prime_power_resultant_frontier_2026-10-01.md)です。一般の $i=3$ は未解決です。

[中央群の二段平方降下と11/15境界](../research/i3/i3_central_square_descent_2026-10-01.md)は先行稿です。
均衡の中央飽和を全比率で $h>11u/15$ へ強化し、等号も全排除します。前稿の平方恒等式を入力に、二つの剰余と低次数のノルムを追います。無限降下や一般の数値問題の解決は主張しません。

[全半比率分配と中央飽和の厳密下限](../research/i3/i3_half_ratio_and_central_saturation_bounds_2026-10-01.md)は依存先です。
飽和を要求しない半比率の $h>(5u-v)/6$ と、均衡中央飽和の $h>5u/7$ を全次数で示します。前提は因子分配と行列式の還元です。一般の数値領域へ移す証明は別に残ります。

[均衡最小境界の全排除と全分配下限](../research/i3/i3_balanced_boundary_closeout_2026-10-01.md)は先行する閉鎖稿です。
前提は[全分配のノルム降下](../research/i3/i3_chebyshev_boundary_and_prime_transfer_2026-10-01.md)。均衡最小境界を全次数で閉じ、全分配に $h\ge\lceil(8u-v)/12\rceil$ を示します。
非均衡境界の残る奇数芯は[5冪の続稿](../research/i3/i3_five_power_composition_and_local_frontier_2026-10-01.md)で $D=5^a,a\ge4$ です。

[半次数の境界の合成と全整数評価の排除](../research/i3/i3_half_degree_composition_2026-10-01.md)は先行する閉鎖稿です。
次数下限の等号を四次・五次の合成へ戻し、次数に上限を置かず数値排除します。[八次の最後の分岐](../research/i3/i3_octic_last_branch_2026-10-01.md)も閉じています。
四次・五次の有理分類と五次の全整数評価の排除が依存先です。

一般の数値領域を狙う先行稿は[完全素数冪の桁予算と正実根の終結式](../research/i3/i3_prime_power_resultant_frontier_2026-10-01.md)です。次数に上限を置かず、数値の整除性から選んだ因子の整数値を直接抑えます。条件付き有限化と一般枝の未解決を区別しています。

[七次の全係数分類と数値排除](../research/i3/i3_septic_closeout_2026-10-01.md)は先行する閉鎖稿です。
そこから[任意次数の半次数下限と八次の3+5の排除](../research/i3/i3_half_degree_bound_and_octic_frontier_2026-10-01.md)へ進みます。
[対称な飽和分配の任意次数の排除](../research/i3/i3_symmetric_saturation_2026-10-01.md)は独立に読めます。

[六次の全分岐の分類・数値排除](../research/i3/i3_sextic_closeout_2026-10-01.md)を先に読むと、9月30日までの未完了の四分岐がどう閉じたか分かります。
前提は任意次数の因子分配、最高次係数比、端点分配の証明です。一般の数値から多項式へ移る条件は別の証明義務として残しています。

## 最新の進展を読む

まず[これまでの進展と次の課題](PROGRESS_SUMMARY.md)を読むと、証明済みの成果・各結果の適用条件・未解決範囲を一度に確認できます。
日付ごとの経緯は[研究履歴](RESEARCH_HISTORY.md)に分けました。

1. [9月30日の五次閉鎖と任意次数への一般化](../research/general/quintic_and_extremal_progress_2026-09-30.md) — 証明済みの最新の入口。
2. [五次の分類](../research/i3/i3_quintic_digit_classification_2026-09-30.md) → [反例候補の二枝の排除](../research/i3/i3_quintic_closeout_2026-09-30.md)。
3. [任意次数の端点分配と六次の四分岐](../research/i3/i3_extremal_split_closeout_2026-09-30.md)。
4. [六次の作業メモ](../research/i3/i3_sextic_working_notes_2026-09-30.md) — 二つの明示モデルの検算を保存。一般分類・整数評価の排除は未完了。
5. [$i=4$ の有限 $j$](../research/general/known_bridge_and_i4_fixed_j_2026-09-30.md)、[6セルの必要条件](../research/i4/i4_six_cell_capacity_2026-09-30.md)、[高次数容量](../research/general/polynomial_capacity_supports_2026-09-30.md)。

## 9月27日の統合と研究継続を読む

9月27日の続行は [$i=4$ の全 $n$ の合同類分類と12類の5セル排除](../research/i4/i4_residue_closeout_2026-09-27.md)です。
基礎として [全 $n$ の積の制限](../research/i4/i4_quadratic_weight_2026-09-27.md)と
[五つの合同類の5セル排除](../research/i4/i4_five_cell_closeout_2026-09-27.md)を使います。
これらを合わせ、$n\ge10^{87}$ の全合同類で6セル以上を強制します。全 $n$ で必要な追加セルの位置も示します。
残る28添字全体の排除は未達です。
[$i=27$ の二次曲線の探索](../research/general/quadratic_capacity_frontier_2026-09-27.md)では、現在の指数条件だけでは矛盾しない配置を保存し、次に必要な整数条件を明記しています。

1. [三添字の全範囲と26添字の有限域](../research/general/september27_integration.md) — 5検証の再生、成立範囲、外部定理への依存。
2. [最大付値行の和の不等式](../research/general/maximal_row_moment_2026-09-27.md) — $i=27,30,33$ の無限尾部を1,410・3,887・9,950行集合へ制限する新しい証明。
3. [添付REPORT](../archive/attachments/incoming_2026-09-27/erdos699_continuation/REPORT.md) — 指数還元、円周間隔、CRT、先頭範囲の完全被覆。

行集合の制限は必要条件です。素数の割当てと無制限の指数は残ります。

## 9月26日の追加引継ぎを読む

1. [二資料の統合](../research/general/handoff_integration_2026-09-26.md) — 共通の余因子法、有効上限の報告、原本と確認状況の対応。
2. [$i=4$ の最大行・空行・占有セル](../research/i4/i4_occupied_cells_integration_2026-09-26.md) — 5族の空行排除、18・28の残配置、6セル報告の省略部分。
3. [新しい検算器](../scripts/audit_handoff_integration_2026_09_26.py)と[結果・全支持配置](../data/results/verification_handoff_integration_2026-09-26.json) — 原本保存、定数、有限境界、被覆証拠。

原本の研究提案は自動実行の指示ではありません。今回の統合で新たな添字の完全解決はありません。

## 全体の証明を理解する

最新の三添字は[9月27日の統合](../research/general/september27_integration.md)、その基礎は[三方向の重み・86添字の完全被覆](../research/general/weighted_cover_and_integration_2026-09-26.md)から読めます。
これは $i=29$ と $35\le i\le119$ の自足した証明です。従来の $i\ge120$ の経路は次のとおりです。

1. [判別式の積公式と共通因子の下界](../research/general/discriminant_continuation.md) — 全体の基礎。
2. [区間ごとの付値評価](../research/general/interval_valuation_continuation.md) — 大きい添字の範囲を改善。
3. [臨界添字の処理](../research/general/critical_indices_and_handoff_integration.md) — $i\ge120$と追加の添字、非有効な有限性。

## $i=3$を基礎から読む

| 順序 | ノート | 読む目的 |
|---|---|---|
| 1 | [正規化と因子分割](../research/i3/i3_nonsquare_merged_continuation.md) | $u,M,T,A,B,C,R,S$などの記号と必要条件 |
| 2 | [全ての $M$ での平方排除](../research/i3/i3_all_square_branches.md) | 解決した枝と、非平方の枝の違い |
| 3 | [境界と固定因子](../research/i3/i3_boundary_and_fixed_blocks.md) | $A,B,C\ge11$と、固定因子ごとの有限性 |
| 4 | [全桁条件と中心](../research/i3/i3_integrated_digits_and_center.md) | 局所条件を結びつける共通の式 |
| 5 | [中心・添字の曲線](../research/i3/i3_direct_center_and_endpoint_curves.md) | $w,\lambda$を固定した還元 |

## 最近の研究を追う

| 方向 | 中心となるノート | 続き・関連 |
|---|---|---|
| 一般数値領域・任意次数の終結式 | [完全素数冪と正実根の因子](../research/i3/i3_prime_power_resultant_frontier_2026-10-01.md) | ブロック桁和での $\omega$ 予算、$m/d$ による底の上界。桁和と相対因子次数を制限した枝は個数・指数・次数が動いても有限化。両量が増える一般枝は残る |
| 任意次数の降下と残る存在命題 | [桁和への縮小、全奇素数の付値保存、局所証明書](../research/i3/i3_uniform_digit_descent_2026-09-23.md) | 条件付き降下を証明。適用できる基数が必ず存在するかが現在の課題。強い基数合同条件の限界も証明 |
| 四次の完全分類と任意次数の係数比 | [2+2分配の全分類、二族の2進排除、Newtonの恒等式](../research/i3/i3_quartic_digit_classification_2026-09-23.md) | 四次を全係数で分類。桁和上界を m≤4 へ拡張し、五次の係数比を三通りへ限定 |
| 全素因数の桁和と任意次数の分配 | [桁和・素因数個数の明示的不等式と因子の次数制限](../research/i3/i3_digit_height_budget_and_factor_degrees_2026-09-23.md) | j の偶奇を問わない結果。重複込みの個数と異なる素数の個数を区別。四次の残った2+2分配は上の続稿で分類 |
| 一般偶数枝の高い冪と素数台 | [T・冪の重複の同時上界と、新しい Kummer 素数の積](../research/i3/i3_multiplicity_budget_and_fresh_support_2026-09-23.md) | 9月23日の証明と18恒等式の検算。T=1を仮定しない。一般枝を完全排除した結果ではない |
| 9月22日の四つの進捗 | [全桁・非平方中心・二曲線の統合](../research/i3/i3_four_handoffs_integration_2026-09-22.md) | 原文4件への導線と、新規報告・未独立監査・残枝の区別。まずこの統合を読み、詳しい議論は各原文へ |
| 全てのGで平方枝を除く | [中心式の二係数と一様な因数分解](../research/i3/i3_gap_square_obstructions_2026-09-21.md) | 9月21日の検算済み稿。$\delta_2TPW_*$ は非平方。先頭係数が平方なら $2G-u\ge7$、平方の $T$ では不可能。両非平方の枝は残る |
| 増大する指数差 | [第二のFrey曲線と $mTPW_*$ の素数の積](../research/i3/i3_growing_gap_and_auxiliary_frey_2026-09-21.md) | $v_2(\Delta_{F,\min})=2G-14$、$N_F>1000$。$R_F=o(G/(\log G)^2)$ の枝を排除。両方が速く増える領域は未解決 |
| 新成果と指数差の有効上限 | [商の同定、素数冪の合同式、固定Gの明示的有限化](../research/i3/i3_new_chat_integration_and_effective_gap_2026-09-21.md) | 偶数jで $u<(6561/4)2^G(G+10)^2+124$。指数差の増大が十分遅い枝も制限 |
| 二次捻りとKummerの橋 | [3乗因子の除去、捻りの最適性、四つの補助因子](../research/i3/i3_quadratic_twist_and_kummer_support_2026-09-21.md) | 導手の量を $\operatorname{rad}_{\ge5}(ab)\operatorname{rad}_{\ge5}(\operatorname{cf}_3(G_0H_0))^2$ に還元。全領域の排除は未達 |
| 判別式の素因数と楕円曲線 | [2で最小のモデル、素数集合の有限化、6乗因子の除去](../research/i3/i3_discriminant_support_and_elliptic_curve_2026-09-21.md) | 上の続稿の基盤。最大素因数11以下と奇素因数の積500以下を指数無制限で排除。全曲線リストに依存 |
| 4チャットの統合・原始点の降下 | [整数系の訂正と判別式の上界改善](../research/i3/i3_four_chat_integration_2026-09-21.md) | [Thue–Mahler全解表で終端判別式3000以下を排除](../research/i3/i3_terminal_thue_mahler_2026-09-21.md)。全指数を対象とし、外部の完全性定理に依存 |
| 小判別式と2進条件 | [独立な有限証明と定数79・71・229・961](../research/i3/i3_cubic_discriminant_minima_2026-09-21.md) | 上記の基盤。一様な284と、有限排除による $u\ge51$。こちらは数体の外部表に依存しない |
| 混合した差 $D$ | [明示的な上限と固定 $D$ の有限化](../research/i3/i3_mixed_parameter_bound_2026-09-20.md) | [回答の統合と因子構造](../research/i3/i3_chatgpt_uniform_integration_2026-09-20.md) |
| 三次整環と末尾 | [判別式と連分数末尾の統合](../research/i3/i3_cubic_discriminant_and_cf_tail_2026-09-21.md) | 判別式49、分母条件のない下界、最大公約数の訂正。判別式の定数は上の続稿で強化 |
| 三次式と近似 | [既約性と有理近似](../research/i3/i3_irreducible_cubic_and_rational_gaps_2026-09-20.md) | [分母の2進付値と連分数](../research/i3/i3_dyadic_denominators_and_continued_fractions_2026-09-21.md) |
| 全桁Kummer条件 | [六ブロックの桁和](../research/i3/i3_global_digit_constraints_2026-09-19.md) | [補数側の桁和の改善](../research/i3/i3_complement_digit_bounds_2026-09-20.md) |
| 桁多項式 | [二つの法と桁の高さ](../research/i3/i3_cross_modulus_and_digit_height_2026-09-20.md) | [三次](../research/i3/i3_cubic_digit_classification_2026-09-20.md)・[四次](../research/i3/i3_quartic_digit_classification_2026-09-23.md)の分類 |
| 降下の可否 | [更新式と上位桁の障害](../research/i3/i3_descent_kummer_obstruction_2026-09-20.md) | [有限個の素数だけを使う方法の限界](../research/i3/i3_finite_prime_obstruction_2026-09-20.md) |
| 指数の差 | [正確な2進付値](../research/i3/i3_exact_gap_and_g9_continuation.md) | [$g=13$までの排除](../research/i3/i3_gap13_and_descent_continuation.md) |

その他のノートは[$i=3$のファイル一覧](../research/i3/)または[成果の詳細一覧](RESULTS_CATALOG.md)で探せます。

## 他の添字

- **$i=4$：** [素数の直後の平方の族](../research/i4/i4_prime_neighbor_squares_2026-09-20.md)。一般の場合は未解決。
- **$i=119$：** [9月26日の重み付き積](../research/general/weighted_cover_and_integration_2026-09-26.md)で全範囲を閉じました。[$10^{87}$までの有限範囲](../research/i119/i119_a100_continuation.md)と[Hankel係数の還元](../research/i119/i119_hankel_content_continuation.md)は以前の経路です。

## 原本や過去の方針を確認する

[添付・外部回答の原文](../sources/README.md)と[過去の進捗一覧・ZIP](../archive/README.md)を分けて保存しています。
原文に書かれた提案や未検証の報告を、現在の証明済みの結論として扱わないでください。
