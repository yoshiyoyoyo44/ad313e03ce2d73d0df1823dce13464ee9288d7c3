# 一般の方法・全体の成立範囲

[入口](../../README.md) · [分野一覧](../README.md) · [現在地](../../docs/STATUS.md) · [検算](../../docs/VERIFICATION.md)

全体を被覆する結果と、残る巨大な領域を制限する方法を保存しています。
**全添字の一般解決は未達です。** 次の順に読むと、既に閉じた範囲と条件付きの方法を区別できます。

## 全体の成立範囲

1. [三方向の重み付き積](weighted_cover_and_integration_2026-09-26.md)：大きな添字の被覆と86添字への拡張。
2. [9月27日の証明書統合](september27_integration.md)：$`i=28,31,34`$ の全域と26添字の $`n\le10^{87}`$ を再生。
3. [現在地](../../docs/STATUS.md)：既存結果との合算と、残る添字。

## 10月4日の全域拡張

素数冪の余因子に対するBFTの明示評価を、重み付き積の上界と接続しました。新しく全 $`n`$ で閉じた添字は $`16,17,19,22,23,24,25,26,27,30,32,33`$ です。原問題全体の解決は未達です。

- [六添字のグラフ証明](bft_pair_graph_closeout_six_indices_2026-10-04.md)と[i=32の有限域拡張](bft_pair_graph_i32_finite_extension_2026-10-04.md)：$`17,23,26,27,30,33`$ と $`32`$。
- [17・19を加えたグラフ](bft_newvertex_i22_i25_closeout_2026-10-04.md)：$`22,25`$。
- [新しいGの下界によるi=19](bft_strengthened_gcd_i19_closeout_2026-10-04.md)、[i=24](bft_i24_closeout_2026-10-04.md)、[六つの強化辺によるi=16](bft_i16_closeout_2026-10-04.md)。
- [Proposition 6.1による中間範囲の接続](bft_proposition61_intermediate_bridge_2026-10-04.md)：既存有限域と明示尾部の間を埋める共通入力。

依存する新しいGの下界、独立監査、条件付きの一般補題は下の索引にあります。[10月4日の再生器](../../scripts/verify_october04.py)は証明依存の順に検算します。

その後、[i=21の位置重み証明](bft_i21_position_moment_closeout_2026-10-04.md)と
[独立監査](bft_i21_position_moment_independent_audit_2026-10-04.md)で、全域添字をさらに一つ追加しました。
[有限再生](../../scripts/audit_bft_i21_finite_dependency_2026_10_04.py)と
[結合検算](../../scripts/audit_bft_i21_moment_closeout_2026_10_04.py)は40件の実行器より後の追加です。

## 桁降下：任意の添字へ

[隣接行の桁降下](adjacent_row_digit_descent_2026-10-03.md)を読むときは、完全付値と桁条件 → 正の実根 → 条件付きの多項式移行 → 有効上限 → i=5への適用の順に進みます。
$`i\ge10`$ では隣接非最大行が必ずあります。素数個数と桁和が有界なら有効上限が出ますが、一般の同時上限は未証明です。

[二位置の有限化](two_position_digit_finite_bound_2026-10-03.md)は素数個数の上限を要求しない代わりに一底の桁構造を仮定します。
[正実根の重み付き除算](global_independent_audit_2026-10-03.md)は係数予算を補強し、支持・付値条件だけでは桁和・素数個数が抑えられないことも区別して示します。

## 残る支持・セルを制限する

- [最大付値行の和](maximal_row_moment_2026-09-27.md)：無限尾部の行集合と有理数の緩和配置。
- [二次曲線の容量](quadratic_capacity_frontier_2026-09-27.md)：排除できる配置と残る配置。
- [高次数補間](polynomial_capacity_supports_2026-09-30.md)：特定の支持の排除。全支持の排除ではありません。
- [外部文献とi=4の有限j](known_bridge_and_i4_fixed_j_2026-09-30.md)：$`5\le j\le1000`$ を全 $`n`$ で被覆。

## 証明と検算

| 対象 | 再生器 | 保存結果 |
|---|---|---|
| 9月26日の拡張 | [replay_weighted_cover_extension.py](../../scripts/replay_weighted_cover_extension.py) | [結果](../../data/results/verification_weighted_cover_extension.json) |
| 9月27日の統合 | [replay_september27_attachments.py](../../scripts/replay_september27_attachments.py) | [結果](../../data/results/verification_september27_attachments.json) |
| 隣接行の桁降下 | [audit_adjacent_digit_descent.py](../../scripts/audit_adjacent_digit_descent.py) | [結果](../../data/results/verification_adjacent_digit_descent.json) |
| 二位置の有限化 | [audit_two_position_digit_bound.py](../../scripts/audit_two_position_digit_bound.py) | [結果](../../data/results/verification_two_position_digit_bound.json) |
| 正実根の除算予算 | [audit_global_independent_2026_10_03.py](../../scripts/audit_global_independent_2026_10_03.py) | [結果](../../data/results/verification_global_independent_2026-10-03.json) |
| 最大行の和 | [audit_maximal_row_moment.py](../../scripts/audit_maximal_row_moment.py) | [結果](../../data/results/verification_maximal_row_moment.json) |
| 有限j | [replay_i4_fixed_j.py](../../scripts/replay_i4_fixed_j.py) | [結果](../../data/results/verification_i4_fixed_j.json) |

当時の「最新」や成立範囲は後続稿で更新されています。現在の範囲は[現在地](../../docs/STATUS.md)を確認してください。

## 全ノート索引

<details>
<summary>全38件を表示（原題・ファイル名を保持）</summary>

| ファイル名の日付 | ノート |
|---|---|
| 2026-10-04 | [i=16の全域閉鎖：六つの明示辺と指数1.0035](bft_i16_closeout_2026-10-04.md) |
| 2026-10-04 | [i=16全域閉鎖の独立監査](bft_i16_independent_audit_2026-10-04.md) |
| 2026-10-04 | [i=24の全域閉鎖：23の二辺を接続する](bft_i24_closeout_2026-10-04.md) |
| 2026-10-04 | [i=19の全域閉鎖：新しいG(3,2)下界の接続](bft_strengthened_gcd_i19_closeout_2026-10-04.md) |
| 2026-10-04 | [i=19全域閉鎖の独立監査](bft_strengthened_gcd_i19_independent_audit_2026-10-04.md) |
| 2026-10-04 | [i=22,25の全域閉鎖：17・19を加えた余因子グラフ](bft_newvertex_i22_i25_closeout_2026-10-04.md) |
| 2026-10-04 | [i=22,25の新BFT三辺の独立監査](bft_newvertex_i22_i25_independent_audit_2026-10-04.md) |
| 2026-10-04 | [i=22,25の区間・グラフ・有限入力の独立監査](bft_newvertex_i22_i25_i3_independent_audit_2026-10-04.md) |
| 2026-10-04 | [六添字の全域閉鎖：近接素数冪14組を同時に使う](bft_pair_graph_closeout_six_indices_2026-10-04.md) |
| 2026-10-04 | [i=32の全域閉鎖：グラフ下界と有限証明書の拡張](bft_pair_graph_i32_finite_extension_2026-10-04.md) |
| 2026-10-04 | [BFT三組の積によるi=27,30,33の全域閉鎖](bft_matching_closeout_i27_i30_i33_2026-10-04.md) |
| 2026-10-04 | [Proposition 6.1による巨大な中間範囲の接続](bft_proposition61_intermediate_bridge_2026-10-04.md) |
| 2026-10-04 | [i=19,24の追加辺のグラフ診断](bft_i19_i24_graph_closeout_working_2026-10-04.md) |
| 2026-10-04 | [G(3,2)の新下界：解析的な尾部](bft_G_3_2_analytic_tail_2026-10-04.md) |
| 2026-10-04 | [G(4,3)の新下界と素数対(7,13)](bft_new_gcd_4_3_and_7_13_anchor_2026-10-04.md) |
| 2026-10-04 | [G(19,14)の新下界と素数対(3,11)](bft_new_gcd_19_14_and_3_11_anchor_2026-10-04.md) |
| 2026-10-04 | [G(19,14)と(3,11)の独立監査](bft_new_gcd_19_14_independent_audit_2026-10-04.md) |
| 2026-10-04 | [G(10,7)の新下界と素数対(2,13)・(11,13)](bft_new_gcd_10_7_and_two_anchors_2026-10-04.md) |
| 2026-10-04 | [G(10,7)と二つのアンカーの独立監査](bft_new_gcd_10_7_independent_audit_2026-10-04.md) |
| 2026-10-04 | [非最大行0：固定比率の数値上限とi=4,…,18の枝の排除](nonmaximum_row_zero_rational_closeout_2026-10-04.md) |
| 2026-10-04 | [全添字：最大底での隣接行共有因子の直接次数上限](largest_base_adjacent_shared_degree_2026-10-04.md) |
| 2026-10-03 | [全添字ルートの独立監査と、正の実根による除算予算の補強](global_independent_audit_2026-10-03.md) |
| 2026-10-03 | [二位置の桁に対する、素数個数によらない全次数の上限](two_position_digit_finite_bound_2026-10-03.md) |
| 2026-10-03 | [全添字に共通する桁の降下：隣接行の正の実根とi=5の新しい排除](adjacent_row_digit_descent_2026-10-03.md) |
| 2026-09-30 | [問題699：2026年9月30日の研究継続](continuation_2026-09-30.md) |
| 本文参照 | [Erdős 699：新資料の統合、臨界添字96・100・120の証明](critical_indices_and_handoff_integration.md) |
| 本文参照 | [Erdős 699：判別式による継続](discriminant_continuation.md) |
| 2026-09-12 | [Erdős 699 — 添付ノートの検算と i=3 の継続](erdos699_continuation_2026-09-12.md) |
| 2026-09-26 | [9月26日の二つの引継ぎの統合](handoff_integration_2026-09-26.md) |
| 本文参照 | [Erdős 699：区間ごとの付値評価で、成立範囲を i≥121 へ](interval_valuation_continuation.md) |
| 2026-09-30 | [外部文献の接続と i=4 の有限 j・全 n 領域](known_bridge_and_i4_fixed_j_2026-09-30.md) |
| 2026-09-27 | [最大付値行の和による無限尾部の制限](maximal_row_moment_2026-09-27.md) |
| 本文参照 | [10月3日の追加進展の統合と、i=3 の新しい有限境界](october03_integration.md) |
| 2026-09-30 | [高次数補間による保存支持と追加33支持の排除](polynomial_capacity_supports_2026-09-30.md) |
| 2026-09-27 | [無限尾部の二次曲線による排除を試し、残る配置を厳密に確認する](quadratic_capacity_frontier_2026-09-27.md) |
| 2026-09-30 | [問題699：五次の閉鎖と任意次数の端点分配](quintic_and_extremal_progress_2026-09-30.md) |
| 本文参照 | [9月27日の証明書統合と無限尾部の研究継続](september27_integration.md) |
| 2026-09-26 | [三方向の重み付き積：添付統合と86添字への拡張](weighted_cover_and_integration_2026-09-26.md) |

</details>
