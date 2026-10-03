# 検算の保存結果

[データ案内](../README.md) · [検算手順](../../docs/VERIFICATION.md) · [現在地](../../docs/STATUS.md)

検算器の実行結果を保存しています。`verification_*.json` は対象・入力・被覆範囲・診断を、ログはその時点の実行を記録します。
JSONの成功表示が保証する範囲は、対応する証明と検算器で確認してください。

## 主な結果

| 結果 | 対応する証明・実行 |
|---|---|
| [全35件の通過ログ](verification_github_publish_2026-10-03.log) | [実行記録](verification_adjacent_digit_continuation_2026-10-03.json)・[35件の実行器](../../scripts/verify_latest.py) |
| [全添字の桁降下](verification_adjacent_digit_descent.json) | [証明](../../research/general/adjacent_row_digit_descent_2026-10-03.md) |
| [i=5の880分配](verification_i5_sparse_allocation.json) | [証明](../../research/i5/i5_odd_sparse_allocation_and_prime5_lift_2026-10-03.md) |
| [i=5の積・完全冪](verification_i5_global_product_and_affine.json) | [証明](../../research/i5/i5_global_product_and_affine_exclusions_2026-10-03.md) |
| [i=5の重複度](verification_i5_multiplicity_frontier.json) | [証明](../../research/i5/i5_multiplicity_frontier_2026-10-03.md) |
| [全体の有限証明書](verification_september27_attachments.json) | [9月27日の統合](../../research/general/september27_integration.md) |

## 読むときの注意

- 日付や件数は、その実行時点の記録です。後から登録した検算は含まれません。
- 有限診断や探索が通っても、一般の整数を証明したことにはなりません。
- 外部定理の仮定や無限域の議論は紙上証明を確認してください。
- 再実行すると対応するJSONを更新する検算器があります。別コピーで再生すれば当時の出力を保てます。

今回の案内整理の確認は、数学の実行履歴と分けて[archiveの整理記録](../../archive/navigation_validation_2026-10-03.json)に保存しています。
