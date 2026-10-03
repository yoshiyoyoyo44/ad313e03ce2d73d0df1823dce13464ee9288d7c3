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

10月3日の [i=5 の新結果](results/verification_i5_multiplicity_frontier.json)は、9容量証明書の全入力係数・局所重複度・評価定数・セル被覆、分母360剰余、復元5の同時評価とBFTによる支持02閉鎖、純冪と剰余を保存します。残る支持は01です。全次数の容量障壁は[紙上証明](../research/i5/i5_multiplicity_frontier_2026-10-03.md)に依存し、一般i=5は未解決です。

[GitHub基準との全パス照合](results/verification_github_baseline_2026-10-03.json)は、全504基準ファイルと全追加ファイルの収録、保持したバイト列、変更した索引・コードを記録します。

10月1日の[半次数の境界・合成・整数係数条件](results/verification_i3_half_degree_composition.json)を追加しました。任意次数の根拠は紙上証明で、56合成例と168整数評価は診断です。一般の i=3 は未解決です。

10月1日の[完全素数冪・正実根の終結式・LCMと桁予算](results/verification_i3_prime_power_resultants.json)を追加しました。数値診断で使う仮定の差と、一般の $i=3$ の未解決を記録しています。

9月30日の成果と対応する証明書・結果は[総括](../docs/PROGRESS_SUMMARY.md)と[検算の案内](../docs/VERIFICATION.md)からたどれます。
[五次の数値排除](results/verification_i3_quintic_closeout.json)、[任意次数の端点分配](results/verification_i3_extremal_split_closeout.json)、
[6セルの有理容量](results/verification_i4_six_cell_capacity.json)、[高次数の追加容量](results/verification_iterated_polynomial_capacity.json)、
[有限 $j$ の再生](results/verification_i4_fixed_j.json)を保存しました。
[六次の作業モデル](results/verification_i3_sextic_working_models.json)は一般分類や反例排除を認証しません。

9月27日の[全 $n$ の合同類分類・12類の全係数と二次式](results/verification_i4_residue_closeout.json)は、
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
