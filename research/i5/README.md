# i=5：残る支持01の研究

[入口](../../README.md) · [分野一覧](../README.md) · [現在地](../../docs/STATUS.md) · [用語](../../docs/GLOSSARY.md)

**一般のi=5は未解決です。** 残るのは $`n\gt 10^{87}`$、支持{0,1}、法72の9・64類。
下の4段階で、どの仮定から何を排除したかをたどれます。

## おすすめの読む順序

| 順 | 証明 | 何が分かるか |
|---|---|---|
| 1 | [尾部の再構築と支持02の閉鎖](i5_multiplicity_frontier_2026-10-03.md) | 最大行、9重複度証明書、外部BFTと有限域の接続。残りは支持01 |
| 2 | [積・完全冪・直線近傍](i5_global_product_and_affine_exclusions_2026-10-03.md) | 45類、完全冪、広い添字域と中央近傍を排除。残りは9・64 |
| 3 | [880分配と5の高桁](i5_odd_sparse_allocation_and_prime5_lift_2026-10-03.md) | 8セル以下を全排除、奇数付値100・112、条件付き102・115 |
| 4 | [隣接行の桁降下](../general/adjacent_row_digit_descent_2026-10-03.md) | 小さい桁重みの族と、全底が最小桁和の二族を全指数・全素数個数で排除 |

最後の稿は任意の添字を扱うため `general/` にあります。
奇数9類の行2には少なくとも一底で桁和7以上、偶数64類の行3には8以上が必要です。

## 残る課題

素数個数、桁和、セル分配が同時に増える一般枝が残っています。
非有効な有限性から、実際に再生できる全域の数値上限へは到達していません。
全次数容量に両立する形式的な重みは手法の限界を示し、整数反例を与えるものではありません。
完全な適用条件と外部定理への依存は各ノートを確認してください。

## 証明と検算

| 段階 | 再生器 | 保存結果 |
|---|---|---|
| 1 | [audit_i5_multiplicity_frontier.py](../../scripts/audit_i5_multiplicity_frontier.py) | [9証明書の検算](../../data/results/verification_i5_multiplicity_frontier.json) |
| 2 | [audit_i5_global_product_and_affine.py](../../scripts/audit_i5_global_product_and_affine.py) | [積・完全冪・近傍](../../data/results/verification_i5_global_product_and_affine.json) |
| 3 | [audit_i5_sparse_allocation.py](../../scripts/audit_i5_sparse_allocation.py) | [880分配・高桁](../../data/results/verification_i5_sparse_allocation.json) |
| 4 | [audit_adjacent_digit_descent.py](../../scripts/audit_adjacent_digit_descent.py) | [桁降下・合同条件](../../data/results/verification_adjacent_digit_descent.json) |

[実行環境とコマンド](../../docs/VERIFICATION.md) · [生成器と再生器の違い](../../scripts/README.md)

## 全ノート索引

<details>
<summary>全3件を表示（原題・ファイル名を保持）</summary>

| ファイル名の日付 | ノート |
|---|---|
| 2026-10-03 | [i=5：45類と完全冪の全排除、積の下界、添字域と直線近傍の閉鎖](i5_global_product_and_affine_exclusions_2026-10-03.md) |
| 2026-10-03 | [i=5：尾部の再構築、四次・六次による支持02の閉鎖、最後の支持01](i5_multiplicity_frontier_2026-10-03.md) |
| 2026-10-03 | [i=5：880分配の全排除、5の高桁条件、全次数の容量障壁](i5_odd_sparse_allocation_and_prime5_lift_2026-10-03.md) |

</details>
