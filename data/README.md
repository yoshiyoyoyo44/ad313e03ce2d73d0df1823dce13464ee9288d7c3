# 証明書と検算結果

[入口](../README.md) · [検算の案内](../docs/VERIFICATION.md)

| フォルダ | 内容 |
|---|---|
| [certificates](certificates/) | CRT、素数証明書、区間・指数などの有限証明書 |
| [cases](cases/) | 楕円曲線や小さい因子ごとのケース一覧 |
| [results](results/) | `verification_*.json`など、検算器の出力 |

今回の整理では元のファイル名・バイト列を保って移動しました。
JSON内の旧ファイル名は[参照先の解決](../scripts/repo_paths.py)で新しい保存先へ対応します。
保存済みの成功表示を読むことと、証明書を再生することは区別してください。

最新の[全 $n$ の合同類分類・12類の全係数と二次式](results/verification_i4_residue_closeout.json)は、
六合同類への制限と12類の5セル排除を確認します。既存の五類と合わせると、$n\ge10^{87}$ の全合同類で6セル以上が必要です。

9月27日の $i=4$ の続行は、[全 $n$ の二次式による積の制限](results/verification_i4_quadratic_weight.json)と
[5セルの全配置・二次式・Pell軌道](results/verification_i4_five_cell_closeout.json)です。
$i=27$ の[追加曲線を含む有理数配置](certificates/quadratic_relaxation_i27_2026-09-27.json)と
[再生結果](results/verification_quadratic_relaxation_i27.json)は、指数の緩和がまだ矛盾しないことを確認するもので、整数反例を意味しません。

9月27日の[証明書の再生結果](results/verification_september27_attachments.json)は、全5検証と原本の出力一致を記録します。
新しい最大行の和の結果は[定数・個数・診断](results/verification_maximal_row_moment.json)、
[全15,247行集合](cases/maximal_row_sets_2026-09-27.json.gz)、
[有理数の緩和配置](certificates/maximal_row_relaxation_2026-09-27.json)にあります。

9月26日の86添字への拡張は、[gzip圧縮した有限証明書](certificates/weighted_cover_2026-09-26/)と
[再生結果](results/verification_weighted_cover_extension.json)に保存しています。
元の5添字証明書と因子分配証明書は、[添付原本](../archive/attachments/incoming_2026-09-26/README.md)にあります。
