# 検算の案内

[入口](../README.md) · [現在地](STATUS.md) · [コード一覧](../scripts/README.md) · [データの場所](../data/README.md)

以下のコマンドは**リポジトリのルート**で実行します。Pythonのassertを使うため、`python -O`は使わないでください。
各ノートの検算はその主張に対応するもので、全てを一度に実行する必要はありません。

## 必要なもの

- Python。既存の記録ではPython 3.14.3を使用。
- 代数の検算にはSymPy。既存の記録ではSymPy 1.14.0を使用。
- 一部の証明書の**再生成**にはNumPy。標準ライブラリだけで動く再生器とは区別します。
- 保存済みMagma応答のローカル検算には、Magmaへの再送信は不要です。

必要に応じて `python -m pip install sympy` で導入できます。

## 9月27日の $i=4$ の続行

最新の[六合同類への分類と12類の閉鎖](../research/i4/i4_residue_closeout_2026-09-27.md)は次で検算します。

```text
python -X utf8 scripts/audit_i4_residue_closeout.py
```

全尾部に適用する単調性の端点、境界の共通素数、商の恒等式、12支持の係数符号、
360二次式（359の符号排除と1個の法8排除）、追加のセル重みを確認します。SymPyを使用します。
[結果JSON](../data/results/verification_i4_residue_closeout.json)に全係数証明書を保存しました。
全合同類での6セルの帰結には、以下の五類の検算と紙上証明も必要です。

```text
python -X utf8 scripts/audit_i4_quadratic_weight.py
python -X utf8 scripts/audit_i4_five_cell_closeout.py
python -X utf8 scripts/audit_quadratic_relaxation_i27.py
python -X utf8 scripts/check_repository.py
```

最初は標準Pythonで、[全 $n$ の積の不等式](../research/i4/i4_quadratic_weight_2026-09-27.md)のセル重み、正値性、定数を確認します。
2番目はSymPyと正確な整数・分数の演算で、全120支持、4608組の非零商候補、57本の二次式、Pell降下の全小出発点と閉軌道を確認します。
[5セルの一般証明](../research/i4/i4_five_cell_closeout_2026-09-27.md)を併せて読む必要があります。
結果は[二次式](../data/results/verification_i4_quadratic_weight.json)と[5セル](../data/results/verification_i4_five_cell_closeout.json)です。
有限の $n$ や指数まで試して全範囲を推測する検算ではありません。新たな完全解決添字を認証するものでもありません。
3番目は[指数の緩和配置](../data/certificates/quadratic_relaxation_i27_2026-09-27.json)を標準Pythonで再生し、全32,547直線と666二次式について容量を確認します。
これは[全尾部の排除に向けた探索で残った配置](../research/general/quadratic_capacity_frontier_2026-09-27.md)で、整数反例ではありません。

## 9月27日の証明書統合と最大行の和

標準Pythonだけで実行できます。原本を保持して全5検証を隔離コピーで再生します。

```text
python -X utf8 scripts/replay_september27_attachments.py
python -X utf8 scripts/audit_maximal_row_moment.py
python -X utf8 scripts/check_repository.py
```

最初のコマンドは2原本、40ハッシュ項目、ZIPの41項目、基点の7個のGit blobを照合し、全5出力JSONを添付の結果と比較します。
55素数対、859近接対、23,999区間と355,462例外、189還元と248,252整数二項係数、276,586区間と60,784単一点が対象です。
[結果](../data/results/verification_september27_attachments.json)と[紙上証明への依存](../research/general/september27_integration.md)を参照してください。
原本の大きなgzipを展開するため、十分なメモリが必要です。

2番目は[最大付値行の和の証明](../research/general/maximal_row_moment_2026-09-27.md)の定数、全セルの重み、二方式の行集合数、有理数の緩和配置を確認します。
全15,247集合を[圧縮JSON](../data/cases/maximal_row_sets_2026-09-27.json.gz)へ、定数と個数を[結果JSON](../data/results/verification_maximal_row_moment.json)へ保存します。
緩和配置の探索には整数最適化を使いましたが、保存された有理数証明書の再生には最適化ソフトは不要です。
行集合の制限は一般の必要条件で、整数反例の有限全列挙ではありません。

## 9月26日の追加引継ぎ2件の検算

標準Pythonのみで、原本を書き換えずに実行できます。

```text
python -X utf8 scripts/audit_handoff_integration_2026_09_26.py
python -X utf8 scripts/check_repository.py
```

[新しい検算器](../scripts/audit_handoff_integration_2026_09_26.py)は原本2件のSHA-256、31添字の $\beta_i$、8,143組の付値・余因子診断、定数・純冪の式を確認します。
空 $q$ 行の20境界例に対する302候補と、9・28類の各36支持配置を全列挙し、除外理由を[結果JSON](../data/results/verification_handoff_integration_2026-09-26.json)へ保存します。
28類で18配置、9類で28配置が残り、後者は原文の30から訂正しました。
一般の尾部・容量の証明は[$i=4$ 統合稿](../research/i4/i4_occupied_cells_integration_2026-09-26.md)、原本報告との区別は[全体の統合稿](../research/general/handoff_integration_2026-09-26.md)にあります。
未添付の過去スクリプトを再実行したものではなく、占有 $q$ 行の省略された全場合分け、$i=3$ の新しい恒等式、外部定理の適用を認証するものでもありません。

## 9月26日の先行する添付統合と86添字の完全被覆

次はPython標準ライブラリだけで実行できます。原本への書き込みや外部通信は行いません。
全区間の再生は数分以上かかり、gzip圧縮された証明書を展開して計算するため、十分なメモリが必要です。

```text
python -X utf8 scripts/replay_september26_attachments.py
python -X utf8 scripts/replay_weighted_cover_extension.py
python -X utf8 scripts/audit_weighted_common_divisor.py
python -X utf8 scripts/check_repository.py
```

| 再生 | 対象 |
|---|---|
| 添付 | 原本5件、同梱SHA-256の114項目、5添字と因子分配・前段3層の6監査。歴史的出力と一致することを確認 |
| 86添字への拡張 | $i=29$、$35\le i\le119$。1,509,157整数区間の不等式と連続被覆、1,031,146組の小範囲例外、86件の無限尾部開始点 |
| 無条件の共通約数 | 22,035組、172境界例、4,719通りの重み比較。全117添字で正の次数差になる集合も確認 |

一般証明は[統合・追加研究](../research/general/weighted_cover_and_integration_2026-09-26.md)、
有限データは[証明書](../data/certificates/weighted_cover_2026-09-26/manifest.json)、
実行結果は[拡張の再生](../data/results/verification_weighted_cover_extension.json)と
[添付の再生](../data/results/verification_september26_attachments.json)を参照してください。
添付検証器は一時コピーで動かし、原本のハッシュを実行前後に照合します。
添付にない $i=3$ の3本文や、前段のA=100基点証明書まで再認証したことにはなりません。

再生成は `python scripts/certify_weighted_cover_extension.py` です。
生成器は192ビット区間漸化式、再生器は128ビットの直接有理数和を用い、再生器は生成器をimportしません。
探索時の余裕を持たせた尾部閾値と、再生成時の最初に通る閾値の違いにより、分割・ハッシュは一致しない場合があります。
生成後は必ず再生器で全被覆を確認してください。Pythonの最適化オプション `-O` は使用しません。

## 最新の結果を短く検算する

```text
python -X utf8 scripts/audit_i3_uniform_digit_descent.py
python -X utf8 scripts/audit_i3_quartic_digit_classification.py
python -X utf8 scripts/audit_i3_digit_height_budget.py
python -X utf8 scripts/audit_i3_multiplicity_and_fresh_support.py
python -X utf8 scripts/audit_i3_gap_square_obstructions.py
python -X utf8 scripts/audit_i3_growing_gap_frey.py
python -X utf8 scripts/audit_i3_new_chat_and_effective_gap.py
python -X utf8 scripts/audit_i3_twist_and_kummer_support.py
python -X utf8 scripts/audit_i3_discriminant_support.py
python -X utf8 scripts/audit_i3_chat_integration.py
python -X utf8 scripts/audit_i3_thue_mahler_table.py
python -X utf8 scripts/replay_i3_cubic_discriminant_minima.py
python -X utf8 scripts/audit_i3_cubic_discriminant_and_cf_tail.py
python -X utf8 scripts/audit_i3_irreducible_cubic_and_rational_gaps.py
python -X utf8 scripts/audit_i3_dyadic_denominators_and_continued_fractions.py
python -X utf8 scripts/audit_i3_mixed_parameter_bound.py
```

出力は[検算結果](../data/results/)へ保存されます。標準出力にも確認項目を表示します。

9月23日の[任意次数の桁和降下](../research/i3/i3_uniform_digit_descent_2026-09-23.md)の検算は標準Pythonだけで実行できます。H=4〜192の全添字18,711組、69,187件の元の付値、138,374件の合同な大きい行への移行、60,805件の局所証明書を確認します。3の法9の補正、共有する素数の三乗、3,400件の桁の結合、基数11の無限族の24例も含みます。条件付き降下の一般証明は本文にあり、適用基数の存在は主張していません。

9月23日の[四次分類の検算](../research/i3/i3_quartic_digit_classification_2026-09-23.md)は、還元の17恒等式、10因数分解、三つの剰余分岐と三つの定数項分岐、100組の非自明な多項式、1,050整数値を確認します。個々の二次因子に負の係数も許す7,665個のCRT候補は、分類された二族だけを再検出しました。さらに128件のNewton恒等式診断を行います。全係数での分類は本文の証明によるもので、有限のCRT検査を一般化した主張ではありません。

9月23日の[桁和と因子次数の検算](../research/i3/i3_digit_height_budget_and_factor_degrees_2026-09-23.md)は、13記号恒等式、800件の整数閾値比較、次数2〜12の32個の非自明な合成多項式、216件の有理数による診断、次数の分配表を確認します。一般証明は本文にあり、合成例は元問題の反例ではありません。

9月23日の[一般偶数枝の検算](../research/i3/i3_multiplicity_budget_and_fresh_support_2026-09-23.md)は、中心式と直接曲線の18恒等式、49個の素数指数パターン、17個の素数配置、1,000個の人工的な曲線、四分岐の定数を確認します。全指数を扱う証明は本文の指数公式と素数ごとの割当てです。一般の導手・判別式定理を使いますが、公開曲線表の再走査は不要です。

指数差の平方枝の検算は、5恒等式、四分岐の定数証明書、256件の法16の条件、317件の平方差の人工的な診断を確認します。
全ての $G$ に対する排除は[続稿の一般証明](../research/i3/i3_gap_square_obstructions_2026-09-21.md)によります。
新たな外部表や高さ定理は不要ですが、既存の正規化の証明依存は引き継ぎます。

増大する指数差の検算は、14恒等式、2,471個の人工的な曲線診断、保存済みの全曲線表1,813,534行を確認します。
106個の根がない証明書と92個の根の分解を保存し、残る三つの和も全分岐で排除します。
素数の積に対する増大評価と閾値は[第二のFrey曲線の稿](../research/i3/i3_growing_gap_and_auxiliary_frey_2026-09-21.md)に証明しています。
表の完全性は外部計算、増大評価はvon Känelの一般定理に依存し、人工的な曲線は元の反例候補ではありません。

新チャットの統合と指数差の検算は、14恒等式、1,440件の局所合同式診断、四分岐の係数と $u=2^{42}$ の閾値を確認します。
診断例は二つの入力合同式を満たす人工的な局所データであり、元の反例候補ではありません。
固定した指数差 $G$ からの明示的上限の一般証明は[統合稿](../research/i3/i3_new_chat_integration_and_effective_gap_2026-09-21.md)にあります。

二次捻りとKummer補助因子の検算は、8恒等式と6剰余類の最小化・最適性を記号計算し、
9,000組の局所付値と256通りの符号を補助診断します。
3乗因子を除去した曲線のモデル、2進条件の保存、Kummerの四つの商との正確な対応が対象です。
一般証明は[続稿](../research/i3/i3_quadratic_twist_and_kummer_support_2026-09-21.md)にあります。

判別式の素因数を扱う検算は、14恒等式、整数系と局所付値の診断、公開曲線全リストの1,813,534行を確認します。
保存したgzip原本は約13.7MBで、展開後のSHA-256も照合します。外部への問い合わせは不要です。
素数集合の被覆、最大2進付値48・51、1728からの最小の隔たりを整数・分数で再計算します。
全曲線がリストに含まれるという完全性は、[証明ノート](../research/i3/i3_discriminant_support_and_elliptic_curve_2026-09-21.md)に明記した外部計算に依存します。
同稿第6.3節では、別の証明済み定理である von Känel の判別式・導手評価から $u$ の明示的上限を導きます。
検算器は $u\ge2^{40}\Rightarrow R>u^{1/4}$ の閾値に用いる定数比較を分数で確認します。一般の不等式の証明はノートに記載しています。

4チャットの統合検算は15恒等式、2,000件の原始点輸送、6通りの座標変換を確認します。
Thue–Mahler表の検算は保存した原本を使い、全33,456点の原始性・値、2冪値の最大指数28、
独立な239,190組の列挙から得た268形式の表への整数可逆変換を確認します。
**掲載解の完全性は von Känel–Matschke のTheorem Eに依存**し、このPython検算だけでは再証明していません。
詳細は[終端形式の排除](../research/i3/i3_terminal_thue_mahler_2026-09-21.md)を参照してください。

小判別式の再生は、65,790組の係数を生成器とは別に全列挙し、74組の簡約形と一致することを確認します。
判別式の2進付値を下げる恒等式も検算します。数体の外部表やMagmaは使いません。
その[証明ノート](../research/i3/i3_cubic_discriminant_minima_2026-09-21.md)に、有限範囲の完全性と一様な上限 $M^3<2^u/284$ の根拠があります。
証明書を再生成する場合は `python scripts/certify_i3_cubic_discriminant_minima.py` を実行します。

## 主な証明書を再生する

| 対象 | コマンド | 読む証明 |
|---|---|---|
| 大きい添字の基盤 | `python scripts/replay_large_indices.py` | [判別式](../research/general/discriminant_continuation.md) |
| 区間ごとの改善 | `python scripts/replay_interval_indices.py` | [区間評価](../research/general/interval_valuation_continuation.md) |
| 臨界添字 | `python scripts/replay_critical_indices.py` | [臨界添字](../research/general/critical_indices_and_handoff_integration.md) |
| $i=119$の有限範囲 | `python scripts/replay_i119_finite.py` | [有限範囲](../research/i119/i119_a100_continuation.md) |
| $i=3$の指数差 | `python scripts/replay_i3_gap13.py` | [指数差の証明](../research/i3/i3_gap13_and_descent_continuation.md) |
| 素数の直後の冪 | `python scripts/replay_i3_prime_neighbor_powers.py` | [特殊な冪の族](../research/i3/i3_prime_neighbor_powers_2026-09-20.md) |

詳細な実行の組み合わせや外部定理への依存は、それぞれの証明ノートにあります。

初期のCRT証明書と、$u\le50$ までの拡張は次のとおりです。

```text
python scripts/replay_certificate.py i3_original_replay.json i3_u42.json
python scripts/replay_certificate.py i3_u43_to_u48.json --primes prime_certificates_u48.json --output verification_u48.json
python scripts/replay_certificate.py i3_u49_to_u50.json --primes prime_certificates_u50.json --output verification_u50.json
```

最後のコマンドは新しい $284M^3<2^u$ を使う $u=49,50$ の証明書です。
14,194個の奇数部分の被覆、164個のCRT候補の排除、43,353個の素数を標準Pythonだけで確認します。
上限の数学的根拠は[小判別式の証明ノート](../research/i3/i3_cubic_discriminant_minima_2026-09-21.md)とその再生器で確認します。
CRT証明書の再生成は `python scripts/extend_i3_cubic_minima_certificate.py` です。

データの旧ファイル名はそのまま指定できます。[参照先の解決](../scripts/repo_paths.py)で新しい保存場所へ対応させています。
明示的な相対パスはリポジトリのルート基準、絶対パスはそのまま使います。

## MagmaとLean

```text
python scripts/audit_i3_center_curve.py
python scripts/audit_i3_fixed_blocks.py
```

これは保存された入力・応答・点・逆変換の確認です。整数点のリストの完全性は、ノートに記載したMagmaの証明計算への依存が残ります。
[Magmaの入力と応答](../magma/README.md)から対応をたどれます。

Leanについては[形式化の範囲と環境](../formal/README.md)を参照してください。

## リポジトリ構成を確認する

```text
python scripts/check_repository.py
python scripts/check_repository.py --smoke
```

文書リンク、Pythonの構文、移動前後の原本・証明書・ログのSHA-256を確認します。
`--smoke`は一時的なコピーで代表的な検算器を実行し、保存済みの結果を上書きしません。
今回の整理に必要な確認であり、全数学的成果の再監査ではありません。

## 現在の構成でZIPを作る

```text
python scripts/package_results.py
```

Git管理下のファイルをフォルダ構成ごと `dist/erdos699-current.zip` に保存し、ZIP内の `SHA256.json` と照合します。
[過去のZIP](../archive/README.md)は当時の配布物として保存し、このコマンドでは上書きしません。
