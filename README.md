# Erdős Problem 699

**二項係数に共通する「大きな素数」を探す研究。問題全体は未解決です。**

[English](README.en.md) · [はじめて読む](docs/PROGRESS_SUMMARY.md) · [証明を読む](docs/READING_GUIDE.md) · [検算する](docs/VERIFICATION.md)

## どんな問題？

同じ $`n`$ から作る二つの二項係数について、小さい方の添字 $`i`$ 以上の共通素因数が必ずあるか、という問題です。

```math
\begin{gathered}
1\le i<j\le n/2\\
\Longrightarrow\quad\exists\text{ prime }p\ge i:\\
p\mid\binom ni\quad\text{and}\quad p\mid\binom nj\ ?
\end{gathered}
```

例えば $`\binom{10}{2}=45`$ と $`\binom{10}{3}=120`$ は、$`i=2`$ 以上の素数3を共有します。

[元の問題文](https://www.erdosproblems.com/699) · [上流のLean定式化](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/699.lean)

## どこまで分かっている？

2026年10月3日時点。このリポジトリに保存した紙上証明・有限証明書の成立範囲です。

| 範囲 | 現在の結論 |
|---|---|
| $`i=1,2,28,29,31,34`$ および $`i\ge35`$ | 全ての許される $`n,j`$ で成立 |
| $`i\ge5`$、$`n\le10^{87}`$ | 全ての許される $`j`$ で成立 |
| $`i=3,4`$ | 一般の場合は未解決 |
| $`5\le i\le33`$、$`i\notin\{28,29,31\}`$ | $`n>10^{87}`$ が未解決 |

**未解決の添字は28個。** 特定の族の排除を、添字全体の解決に数えていません。
第三者査読と問題全体のLean形式検証は未実施です。[成立範囲・前提・残る課題](docs/STATUS.md)

## 目的から読む

| 知りたいこと | 入口 |
|---|---|
| 問題と進展を平易に把握したい | [研究の概要](docs/PROGRESS_SUMMARY.md) → [用語・記号](docs/GLOSSARY.md) |
| 成立範囲と未解決部分を確認したい | [現在地](docs/STATUS.md) |
| 証明とその前提を確かめたい | [読む順序](docs/READING_GUIDE.md) → [分野別ノート](research/README.md) |
| 計算を自分で再現したい | [検算手順](docs/VERIFICATION.md) → [コード](scripts/README.md)・[データ](data/README.md) |
| 経緯や受領資料を追いたい | [研究履歴](docs/RESEARCH_HISTORY.md) → [原文](sources/README.md)・[保存原本](archive/README.md) |

## 現在の研究の焦点

- **全添字に共通する桁降下。** 桁和と素因数の個数が有界なら、$`n`$ の有効な上限が出ます。一般の上限は未証明です。[証明と適用範囲](research/general/README.md)
- **$`i=5`$ の残る巨大な領域。** 支持を{0,1}、法72の類を9・64へ絞り、少数セルや小さい桁和の族を排除しました。一般の $`i=5`$ は残っています。[4段階の証明](research/i5/README.md)
- **$`i=3,4`$ の構造の制限。** $`i=3`$ の条件付き多項式分配、$`i=4`$ の有限 $`j`$ とセル条件を研究しています。[i=3](research/i3/README.md) · [i=4](research/i4/README.md)

補題ごとの詳細は[成果一覧](docs/RESULTS_CATALOG.md)、次の課題は[現在地](docs/STATUS.md)にまとめています。

## 検算を始める

Python 3.12以上。リポジトリのルートで実行します。

```console
python -m pip install -r requirements-verification.txt
python -X utf8 scripts/check_repository.py
```

上は案内・構文・原本保存の確認です。研究更新に対応する35件を再生する場合：

```console
python -X utf8 scripts/verify_latest.py
```

[保存した全35件の通過ログ](data/results/verification_github_publish_2026-10-03.log) · [対象・外部依存・出力の注意](docs/VERIFICATION.md)

## フォルダ案内

| 場所 | 内容 |
|---|---|
| [docs](docs/README.md) | 概要、現在地、用語、読む順序、成果一覧、検算、履歴 |
| [research](research/README.md) | 分野別の証明・研究ノートと全ノート索引 |
| [scripts](scripts/README.md) / [data](data/README.md) | 検算器・生成器 / 証明書・ケース・実行結果 |
| [formal](formal/README.md) / [magma](magma/README.md) | Leanの代数恒等式 / Magmaの入力と保存応答 |
| [sources](sources/README.md) / [archive](archive/README.md) | 一次文献・受領原文 / ZIP・旧版・ファイル対応表 |

[資料の追加・整理のルール](CONTRIBUTING.md) · [10月3日のZIP統合](docs/IMPORT_2026-10-03.md)
