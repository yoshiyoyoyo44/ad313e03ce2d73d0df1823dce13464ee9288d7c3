# 検算手順

[入口](../README.md) · [現在地](STATUS.md) · [コード](../scripts/README.md) · [データ](../data/README.md)

コマンドはリポジトリのルートで実行します。assertを使うため **`python -O` は使わないでください**。
紙上証明、有限証明書の再生、有限診断の役割を分けて確認します。

## 環境と最初の確認

Python3.12以上。直前の全35件はPython3.14.3、SymPy1.14.0で通過しました。
SymPyは[依存ファイル](../requirements-verification.txt)で固定しています。

```console
python -m pip install -r requirements-verification.txt
python -X utf8 scripts/check_repository.py
```

[check_repository.py](../scripts/check_repository.py)は内部リンク、案内の索引、Python構文、JSON、保存原本のSHA-256を確認します。
数学的な問題全体を証明する検算器ではありません。

## 研究更新に対応する全39件

以下の39件は10月3日までの更新に対応します。10月4日の全域証明は次節の実行器を使います。

```console
python -X utf8 scripts/verify_latest.py
```

[実行器](../scripts/verify_latest.py)に登録した39件を順に実行し、失敗した時点で停止します。
全添字の桁降下、i=5、i=3の近年の分配、i=4、容量と有限 $`j`$、リポジトリ確認を含みます。
過去の全検算器を網羅するものではありません。

| 保存記録 | 何を記録したものか |
|---|---|
| [今回の独立研究の実行記録](../data/results/verification_independent_research_2026-10-03.json) | 既存数学34件の隔離再生、追加4件、案内検査。39件の一回の通し実行という意味ではない |
| [全35件の実行ログ](../data/results/verification_github_publish_2026-10-03.log) | 直前のGitHub研究更新前の通し実行。全件通過 |
| [対応する実行記録](../data/results/verification_adjacent_digit_continuation_2026-10-03.json) | 環境、検算、原本照合、当時のファイル数 |
| [ZIP統合記録](IMPORT_2026-10-03.md) | 受領時の隔離コピーで当時の全32件を再生した記録 |
| [案内整理の確認](../archive/navigation_validation_2026-10-03.json) | 今回のリンク・索引・旧版保存・数学資料のバイト保存確認 |

検算器の多くは `data/results/verification_*.json` を再出力します。
保存済みログを保ちたい場合は、別の作業コピーで再生してください。

## 10月4日の全域証明と追加補題

```console
python -X utf8 scripts/verify_october04.py
```

[10月4日の実行器](../scripts/verify_october04.py)は40件を依存順に実行します。
まず六添字・i=32・i=22,25の有限入力とグラフを再生し、新しいG下界の有限素数区間と解析尾部を検証します。
続いてi=19,24,16の全域接続、一般の部分補題、i=3の条件付き分配と数値制限、i=5のPell還元を確認します。
最後に索引・内部リンク・保存原本を照合します。全てassertを有効にしてください。

[実行記録](../data/results/verification_october04_publication_2026-10-04.json)と
[全出力ログ](../data/results/verification_october04_publication_2026-10-04.log)を保存します。
各検算器は対応する結果JSONを上書きします。独立監査の記録は、その記録に書いた担当者と範囲に限ります。
この実行器が通過しても、引用する外部定理自体の再証明や、問題全体の解決を意味しません。

新しい全域添字は **16,17,19,22,23,24,25,26,27,30,32,33の12個** です。
各証明と外部入力は[現在地](STATUS.md)と[一般のノート索引](../research/general/README.md)からたどれます。
i=3・i=5の追加補題は、それぞれの仮定が必要な部分成果です。

## 主な証明と個別検算

40件の通過後、i=21を全域へ拡張しました。この後続分は別に再生します。

```console
python -X utf8 scripts/audit_bft_i21_finite_dependency_2026_10_04.py
python -X utf8 scripts/audit_bft_i21_moment_closeout_2026_10_04.py
```

[証明](../research/general/bft_i21_position_moment_closeout_2026-10-04.md) ·
[結合結果](../data/results/verification_bft_i21_moment_closeout_2026-10-04.json) ·
[独立監査](../research/general/bft_i21_position_moment_independent_audit_2026-10-04.md)。
現在の新しい全域添字は13個、残りは15個です。40件のログに記した12個は、その実行時点の記録です。

| 対象 | コマンドのスクリプト | 保存結果 |
|---|---|---|
| [i=3残余次数6・七次境界](../research/i3/i3_independent_attack_2026-10-03.md) | [audit_i3_rho6_degree7_independent.py](../scripts/audit_i3_rho6_degree7_independent.py) | [結果](../data/results/verification_i3_rho6_degree7_independent.json) |
| [i=5二位置族と全桁合同](../research/i5/i5_independent_attack_2026-10-03.md) | [audit_i5_weight4_two_positions.py](../scripts/audit_i5_weight4_two_positions.py) | [結果](../data/results/verification_i5_weight4_two_positions.json) |
| [全添字の二位置有限化](../research/general/two_position_digit_finite_bound_2026-10-03.md) | [audit_two_position_digit_bound.py](../scripts/audit_two_position_digit_bound.py) | [結果](../data/results/verification_two_position_digit_bound.json) |
| [正実根の除算予算](../research/general/global_independent_audit_2026-10-03.md) | [audit_global_independent_2026_10_03.py](../scripts/audit_global_independent_2026_10_03.py) | [結果](../data/results/verification_global_independent_2026-10-03.json) |
| [全添字の桁降下](../research/general/adjacent_row_digit_descent_2026-10-03.md) | [audit_adjacent_digit_descent.py](../scripts/audit_adjacent_digit_descent.py) | [結果](../data/results/verification_adjacent_digit_descent.json) |
| [i=5の880分配・5の高桁](../research/i5/i5_odd_sparse_allocation_and_prime5_lift_2026-10-03.md) | [audit_i5_sparse_allocation.py](../scripts/audit_i5_sparse_allocation.py) | [結果](../data/results/verification_i5_sparse_allocation.json) |
| [i=5の積・完全冪・直線近傍](../research/i5/i5_global_product_and_affine_exclusions_2026-10-03.md) | [audit_i5_global_product_and_affine.py](../scripts/audit_i5_global_product_and_affine.py) | [結果](../data/results/verification_i5_global_product_and_affine.json) |
| [i=5の9重複度証明書](../research/i5/i5_multiplicity_frontier_2026-10-03.md) | [audit_i5_multiplicity_frontier.py](../scripts/audit_i5_multiplicity_frontier.py) | [結果](../data/results/verification_i5_multiplicity_frontier.json) |
| [i=3の標準桁・完全分配](../research/i3/i3_split_mahler_frontier_2026-10-03.md) | [audit_i3_split_mahler_frontier.py](../scripts/audit_i3_split_mahler_frontier.py) | [結果](../data/results/verification_i3_split_mahler_frontier.json) |
| [i=3の任意共有因子](../research/i3/i3_arbitrary_cofactor_closeout_2026-10-02.md) | [audit_i3_arbitrary_cofactor.py](../scripts/audit_i3_arbitrary_cofactor.py) | [結果](../data/results/verification_i3_arbitrary_cofactor.json) |
| [i=4の有限 $`j`$](../research/general/known_bridge_and_i4_fixed_j_2026-09-30.md) | [replay_i4_fixed_j.py](../scripts/replay_i4_fixed_j.py) | [結果](../data/results/verification_i4_fixed_j.json) |
| [全体の成立範囲・有限域](../research/general/september27_integration.md) | [replay_september27_attachments.py](../scripts/replay_september27_attachments.py) | [結果](../data/results/verification_september27_attachments.json) |

個別の実行例：

```console
python -X utf8 scripts/audit_adjacent_digit_descent.py
python -X utf8 scripts/audit_i5_sparse_allocation.py
```

全添字の桁降下では30,586の素数単位の診断、190除算、重み3の216消去式と54零終結式、合同条件と整数閾値などを再生します。
無限の範囲を扱う補題の根拠は本文の証明です。有限診断を全次数へ外挿しません。
i=5の分配は880配置の完全被覆を確認し、局所重複度は生成器と異なる算式でも照合します。

他の検算器は[分野別案内](../research/README.md)の証明・検算対応表と、[全コード索引](../scripts/README.md)から探せます。

## 原本とZIPを照合する

```console
python -X utf8 scripts/replay_all_progress_import.py --source-only
```

[原本照合器](../scripts/replay_all_progress_import.py)は受領ZIP、665ハッシュ項目、更新前13ファイルを確認します。
研究や案内を更新した現在は `--source-only` を使います。指定なしの実行は**統合時点の作業ツリー**も照合するため、その後の正当な更新でも一致しなくなります。
BUILD_METADATA.jsonは配布元の記録で、現在のGitコミットを表しません。

他の受領資料の照合は `check_repository.py` に含まれます。
[原本一覧](../archive/README.md) · [10月3日の統合台帳](../archive/attachments/all_progress_2026-10-03/README.md)

## 証明書の生成、Magma、Lean

- **生成器：** `build_*`、`certify_*` などは証明書を作ります。独立再生器と区別してください。再生成にはNumPyなど追加依存が必要なものがあります。
- **Magma：** [入力と保存応答](../magma/README.md)を保存しています。ローカル照合に再送信は不要です。時間制限の応答を完了した証明として扱いません。
- **Lean：** [三つの代数恒等式](../formal/README.md)だけを確認しています。問題全体や全再生器の形式化ではありません。
- **代表8本の隔離スモーク：** 必要なら `python -X utf8 scripts/check_repository.py --smoke`。一時コピーで入出力の場所も検査します。

外部BFT、Matveev、Mahlerなどの定理は、各ノートの仮定と[文献の取得記録](../sources/literature_2026-09-30/README.md)を確認してください。

## 過去の詳しい手順

以前の456行の案内は[整理前の検算案内](../archive/snapshots/navigation_2026-10-03/files/docs/VERIFICATION.md)にバイト保存しています。
当時の相対リンクは[整理前のGitHubツリー](https://github.com/yoshiyoyoyo44/erdos699/tree/67e04ead726d485f38c31a641183cf6a1bb0316a)でたどれます。
実行対象を選ぶときは、現在の証明と対応するスクリプトを確認してください。
