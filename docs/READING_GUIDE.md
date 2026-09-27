# 読む順序と分野別の案内

[入口](../README.md) · [現在地](STATUS.md) · [全成果の一覧](RESULTS_CATALOG.md) · [検算](VERIFICATION.md)

全ノートを日付順に読む必要はありません。まず[現在地](STATUS.md)を確認し、目的に応じて以下をたどってください。

## 9月27日の統合と研究継続を読む

最新は [$i=4$ の全 $n$ の合同類分類と12類の5セル排除](../research/i4/i4_residue_closeout_2026-09-27.md)です。
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
