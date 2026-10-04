# 読む順序

[入口](../README.md) · [全ドキュメント](README.md) · [現在地](STATUS.md) · [分野別ノート](../research/README.md)

全ファイルを時系列に読む必要はありません。目的に合う経路を選んでください。
各分野の案内には、おすすめの順序と全ノート索引があります。

## 初めて読む

1. [研究の概要](PROGRESS_SUMMARY.md)：問題、考え方、主な進展。
2. [現在地](STATUS.md)：証明済みの範囲、残る16添字、外部依存。
3. [用語・記号](GLOSSARY.md)：分からない記号を確認。
4. 興味のある[分野の案内](../research/README.md)から証明へ。

英語の短い入口は [English README](../README.en.md) です。証明本文の多くは日本語です。

## 証明をレビューする

まず[現在地](STATUS.md)で結論の範囲を確認し、次に下表の案内へ進みます。
ノートの仮定 → 紙上証明 → 証明書 → 独立再生器 → 保存結果の順に読むと、計算が担う部分を確認できます。

| 分野 | 推奨する入口 | 特に確認する前提 |
|---|---|---|
| 10月4日の12添字の全域化 | [六添字のBFTグラフ](../research/general/bft_pair_graph_closeout_six_indices_2026-10-04.md)、下の読む順序 | BFTの明示指数・例外・閾値、有限証明書の完全再生、無限尾部との接続 |
| 9月までの全体の成立範囲 | [一般の方法](../research/general/README.md)の「全体の成立範囲」 | 重み付き被覆と有限域、適用する外部定理 |
| 全添字の桁降下 | [一般の方法](../research/general/README.md)の「桁降下」 | 非最大行、完全付値、桁和・素数個数の有界性 |
| $`i=5`$ | [i=5の4段階](../research/i5/README.md) | 有限域の接続、支持、外部BFT、全桁条件 |
| $`i=3`$ | [i=3の3つの経路](../research/i3/README.md) | 標準桁と変換後の桁設定、多項式への移行、重複度 |
| $`i=4`$ | [i=4の案内](../research/i4/README.md) | 有限 $`j`$ と全 $`j`$、6セルの必要条件と全排除の区別 |
| 初期の $`i=119`$ | [過去の有限・Hankel研究](../research/i119/README.md) | 当時の結果と現在の $`i\ge35`$ の結果の区別 |

補題ごとの結論を引く場合は[成果の詳細一覧](RESULTS_CATALOG.md)を使ってください。
過去のノートの未解決記述は、後続の証明で更新されていることがあります。

### 10月4日の全域証明を読む順序

1. [六添字の証明](../research/general/bft_pair_graph_closeout_six_indices_2026-10-04.md)で、小素数ごとの最大付値行、余因子積P、三方向の容量上界、BFT素数対のグラフを確認する。
2. [i=32の有限拡張](../research/general/bft_pair_graph_i32_finite_extension_2026-10-04.md)で、10^116までの再生と尾部開始点に隙間がないことを確認する。
3. [i=22,25](../research/general/bft_newvertex_i22_i25_closeout_2026-10-04.md)で、Theorem 2.4の全定数とProposition 6.1の中間域を読む。
4. [i=19](../research/general/bft_strengthened_gcd_i19_closeout_2026-10-04.md)、[i=24](../research/general/bft_i24_closeout_2026-10-04.md)、[i=16](../research/general/bft_i16_closeout_2026-10-04.md)で、新しいG下界・追加辺と、有限・中間・無限の三域の接続を確認する。
5. 各ノート末尾の専用検算器、有限入力の再生記録、独立監査を照合する。BFTの定理自体は[一次論文](https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf)を外部入力としている。

これらは16,17,19,22,23,24,25,26,27,30,32,33の全域証明です。
i=3の[線形商の分配](../research/i3/i3_linear_J2_quotient_degree1_bge2_all_degrees_2026-10-04.md)と
i=5の[Pell還元](../research/i5/i5_pell_primitive_unit_reduction_2026-10-04.md)は条件付き進展として読む必要があります。
一般i=3・i=5と問題全体は未解決です。

## 計算を再現する

1. [検算手順](VERIFICATION.md)で環境・対象・出力を確認。
2. [コード案内](../scripts/README.md)から該当する再生器を選択。
3. [証明書](../data/certificates/README.md)と[保存結果](../data/results/README.md)の役割を区別。
4. 必要な個別検算を実行。10月3日までの39件と、上の10月4日ノートに対応する専用検算器を区別する。

保存した成功ログだけでは、普遍的な紙上証明の前提を確認したことにはなりません。
生成器は証明書を作るもの、再生器はその証明書を検査するものです。

## 経緯・原本・研究継続を追う

| 目的 | 入口 |
|---|---|
| 日付別の研究と訂正 | [研究履歴](RESEARCH_HISTORY.md) |
| 受領資料と検討結果 | [原文と対応する統合稿](../sources/README.md) |
| 10月3日のZIP統合 | [統合記録](IMPORT_2026-10-03.md)・[保存原本](../archive/attachments/all_progress_2026-10-03/README.md) |
| 当時のGitHub基準・配布内容 | [10月3日の更新・配布記録](GITHUB_PROGRESS_2026-10-03.md) |
| 詳細な研究継続の前提 | [専門的な引き継ぎ記録](AI_HANDOFF_2026-10-02.md) |
| 旧名・古いリンクの移動先 | [全ファイル対応表](../archive/FILE_MAP.md) |

日付付き資料の指示文は、その資料の内容です。現在の作業指示や証明済みの結論とは区別してください。
[資料追加のルール](../CONTRIBUTING.md)
