# 過去の記録・配布物

[入口](../README.md) · [現在地](../docs/STATUS.md) · [原文](../sources/README.md)

## 整理前の進捗一覧

- [整理前のREADME](snapshots/README_before_reorganization_2026-09-21.md) — 505行の累積した進捗。
- [整理前のSTATUS_AND_DIRECTIONS](snapshots/STATUS_before_reorganization_2026-09-21.md) — 当時の成果一覧と研究方針。

上の二つはバイト列を変えずに保存したスナップショットです。内部の相対リンクやコマンドは当時の配置のままです。
当時のリンクをたどる場合は[整理前のGitHubツリー](https://github.com/yoshiyoyoyo44/erdos699/tree/162412e)を参照してください。
成果表を今のリンクで読みたい場合は[成果の詳細一覧](../docs/RESULTS_CATALOG.md)を使ってください。

## ZIPと当時のハッシュ

- [当時の配布ZIP](attachments/erdos699_continuation_2026-09-12.zip)
- [9月15日に追加したZIPの案内](attachments/incoming_2026-09-15/README.md)
- [9月26日の5添付と依存資料](attachments/incoming_2026-09-26/README.md) — 原本保存、同梱114ハッシュ項目と6監査を再検証。
- [9月27日の研究メモとパッケージ](attachments/incoming_2026-09-27/README.md) — 原本保存、40ハッシュ項目と全5検証の再生。
- [10月3日に受け取った別系統の研究](attachments/incoming_2026-10-03/README.md) — 原本2件と展開12ファイルの保存。独立に再構築した結果と、資料からの報告を区別。
- [10月3日の全進展ZIPの統合原本](attachments/all_progress_2026-10-03/README.md) — 受領ZIP、配布元メタデータ、全666項目の統合台帳、更新前13ファイルを保存。
- [当時のSHA-256一覧](SHA256_legacy.json)

これらは当時の配布物であり、その後の全成果を含む最新パッケージではありません。
現在の構成でZIPを作る方法は[検算の案内](../docs/VERIFICATION.md)にあります。

## 旧ファイル名から探す

[旧名と新しい場所の対応表](FILE_MAP.md)で、以前のファイル名を検索できます。
以前の `main/ファイル名` へのリンクは、移動後の場所に置き換えてください。過去のコミットを指定したリンクは当時のファイルを参照できます。

[移動記録とSHA-256](reorganization_2026-09-21.json)には、279ファイルの移動前後の対応を記録しています。
証明ノートではリンク・数式の表示形式・実行コマンドを整理し、検算コードでは入出力の保存先を修正しました。
原本・証明書・計算ログの保存は `python scripts/check_repository.py` で確認できます。

[整理時の確認結果](reorganization_validation_2026-09-21.json)には、内部リンク、原本のハッシュ、代表的な検算8本の動作確認を記録しています。
