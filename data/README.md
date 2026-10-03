# 証明書・ケース・検算結果

[入口](../README.md) · [検算手順](../docs/VERIFICATION.md) · [コード](../scripts/README.md)

| 場所 | 内容 | 用途 |
|---|---|---|
| [certificates](certificates/README.md) | CRT、区間、指数、係数、有限被覆など | 再生器が読み、完全性・整合性を確認する入力 |
| [cases](cases/) | 曲線、固定因子、行集合など | 数学的な枝と入力・応答の対応 |
| [results](results/README.md) | JSON・ログ・保存応答 | どの条件をどの環境で確認したかの実行記録 |

証明の仮定は[現在地](../docs/STATUS.md)と[ノート](../research/README.md)で確認します。
保存した成功表示、有限診断、完全な有限証明書の再生はそれぞれ役割が異なります。

## まず確認する結果

| 対象 | 保存記録 |
|---|---|
| 直前の研究更新の全35件 | [通過ログ](results/verification_github_publish_2026-10-03.log)・[環境と照合](results/verification_adjacent_digit_continuation_2026-10-03.json) |
| 全添字の桁降下・乗法的結合 | [verification_adjacent_digit_descent.json](results/verification_adjacent_digit_descent.json) |
| i=5の880分配・5の高桁 | [verification_i5_sparse_allocation.json](results/verification_i5_sparse_allocation.json) |
| i=5の積・完全冪・直線近傍 | [verification_i5_global_product_and_affine.json](results/verification_i5_global_product_and_affine.json) |
| i=5の9証明書・支持02の閉鎖 | [verification_i5_multiplicity_frontier.json](results/verification_i5_multiplicity_frontier.json) |
| 全体の成立範囲と有限域の再生 | [verification_september27_attachments.json](results/verification_september27_attachments.json) |

各検算器は結果ファイルを再出力することがあります。保存された当時の記録を保ちたい場合は別コピーで実行してください。
JSON内の旧名は[パス解決器](../scripts/repo_paths.py)が対応します。

証明書・結果の元のバイト列は今回の案内整理で変更していません。
[原本・旧版](../archive/README.md) · [過去のデータ案内](../archive/snapshots/navigation_2026-10-03/files/data/README.md)
