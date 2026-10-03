# 一般の方法・全体の成立範囲

[入口](../../README.md) · [分野一覧](../README.md) · [現在地](../../docs/STATUS.md) · [検算](../../docs/VERIFICATION.md)

全体を被覆する結果と、残る巨大な領域を制限する方法を保存しています。
**全添字の一般解決は未達です。** 次の順に読むと、既に閉じた範囲と条件付きの方法を区別できます。

## 全体の成立範囲

1. [三方向の重み付き積](weighted_cover_and_integration_2026-09-26.md)：大きな添字の被覆と86添字への拡張。
2. [9月27日の証明書統合](september27_integration.md)：$`i=28,31,34`$ の全域と26添字の $`n\le10^{87}`$ を再生。
3. [現在地](../../docs/STATUS.md)：既存結果との合算、残る28添字。

## 桁降下：任意の添字へ

[隣接行の桁降下](adjacent_row_digit_descent_2026-10-03.md)を読むときは、完全付値と桁条件 → 正の実根 → 条件付きの多項式移行 → 有効上限 → i=5への適用の順に進みます。
$`i\ge10`$ では隣接非最大行が必ずあります。素数個数と桁和が有界なら有効上限が出ますが、一般の同時上限は未証明です。

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
| 最大行の和 | [audit_maximal_row_moment.py](../../scripts/audit_maximal_row_moment.py) | [結果](../../data/results/verification_maximal_row_moment.json) |
| 有限j | [replay_i4_fixed_j.py](../../scripts/replay_i4_fixed_j.py) | [結果](../../data/results/verification_i4_fixed_j.json) |

当時の「最新」や成立範囲は後続稿で更新されています。現在の範囲は[現在地](../../docs/STATUS.md)を確認してください。

## 全ノート索引

<details>
<summary>全15件を表示（原題・ファイル名を保持）</summary>

| ファイル名の日付 | ノート |
|---|---|
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
