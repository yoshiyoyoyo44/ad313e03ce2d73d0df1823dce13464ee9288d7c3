# i=4：合同類・セル・有限j

[入口](../../README.md) · [分野一覧](../README.md) · [現在地](../../docs/STATUS.md) · [用語](../../docs/GLOSSARY.md)

**一般のi=4は未解決です。** $`5\le j\le1000`$ は全 $`n`$ で成立。
巨大な $`n`$ には6セル以上が必要ですが、6セルの全排除は未達です。

## おすすめの読む順序

1. [最大付値行・占有セルの統合](i4_occupied_cells_integration_2026-09-26.md)：行・空行・セルの定義と基本還元。
2. [二次式による積の制限](i4_quadratic_weight_2026-09-27.md)：全 $`n`$ の必要条件。
3. [五類の5セル](i4_five_cell_closeout_2026-09-27.md) → [六合同類と12類の閉鎖](i4_residue_closeout_2026-09-27.md)：$`n\ge10^{87}`$ に6セル以上を強制。
4. [6セル容量](i4_six_cell_capacity_2026-09-30.md)：全103支持の有理重みと小素数冪の必要下限。
5. [有限j・全nの証明](../general/known_bridge_and_i4_fixed_j_2026-09-30.md)：$`5\le j\le1000`$ の独立再生。

[素数の直後の平方族](i4_prime_neighbor_squares_2026-09-20.md)も全素数を扱う特定の族の結果として保存しています。

## 証明と検算

| 対象 | 再生器 | 保存結果 |
|---|---|---|
| 二次式の積 | [audit_i4_quadratic_weight.py](../../scripts/audit_i4_quadratic_weight.py) | [結果](../../data/results/verification_i4_quadratic_weight.json) |
| 五類の5セル | [audit_i4_five_cell_closeout.py](../../scripts/audit_i4_five_cell_closeout.py) | [結果](../../data/results/verification_i4_five_cell_closeout.json) |
| 六合同類・12類 | [audit_i4_residue_closeout.py](../../scripts/audit_i4_residue_closeout.py) | [結果](../../data/results/verification_i4_residue_closeout.json) |
| 6セル容量 | [audit_i4_six_cell_capacity.py](../../scripts/audit_i4_six_cell_capacity.py) | [結果](../../data/results/verification_i4_six_cell_capacity.json) |
| 有限j | [replay_i4_fixed_j.py](../../scripts/replay_i4_fixed_j.py) | [結果](../../data/results/verification_i4_fixed_j.json) |

有限の添字範囲と、全 $`j`$ の結果を区別してください。[検算手順](../../docs/VERIFICATION.md)

## 全ノート索引

<details>
<summary>全6件を表示（原題・ファイル名を保持）</summary>

| ファイル名の日付 | ノート |
|---|---|
| 2026-09-27 | [$`i=4`$：五つの合同類の5セルを閉じる](i4_five_cell_closeout_2026-09-27.md) |
| 2026-09-26 | [$`i=4`$：最大付値行・空行・占有セルの統合](i4_occupied_cells_integration_2026-09-26.md) |
| 2026-09-20 | [i=4：n=(p+1)² の全ての素数 p を処理する](i4_prime_neighbor_squares_2026-09-20.md) |
| 2026-09-27 | [$`i=4`$：二次式を使う、全 $`n`$ の積の制限](i4_quadratic_weight_2026-09-27.md) |
| 2026-09-27 | [$`i=4`$：全 $`n`$ の六合同類と、12類の閉鎖](i4_residue_closeout_2026-09-27.md) |
| 2026-09-30 | [i=4：全6セル支持の有理重みと小素数冪の下限](i4_six_cell_capacity_2026-09-30.md) |

</details>
