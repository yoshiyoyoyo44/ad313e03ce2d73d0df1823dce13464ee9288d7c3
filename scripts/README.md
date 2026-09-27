# 検算コード

[入口](../README.md) · **[実行方法](../docs/VERIFICATION.md)** · [証明ノート](../research/README.md)

リポジトリのルートから `python scripts/audit_i3_mixed_parameter_bound.py` で実行します。

| 名前 | 役割 |
|---|---|
| `audit_*.py` | 恒等式・不等式・保存された計算の検算 |
| `replay_*.py` | 有限証明書の再生 |
| `certify_*.py`、`make_*.py` | 証明書・計算入力の生成 |
| `explore_*.py` | 探索用。証明の保証範囲は各ノートを参照 |
| [check_repository.py](check_repository.py) | リンク・構文・原本保存と、代表的な動作の確認 |
| [repo_paths.py](repo_paths.py) | 証明書やログに記録された旧ファイル名を新配置へ対応 |
| [package_results.py](package_results.py) | 現在の構成をSHA-256付きのZIPにする |

最初に実行するものは[検算の案内](../docs/VERIFICATION.md)で選べます。
全スクリプトをまとめて走らせる必要はありません。

9月27日の統合・研究継続の入口：

- [audit_i4_residue_closeout.py](audit_i4_residue_closeout.py)：全 $n$ の六合同類への分類、12類の空行と5セル、追加セルの重み恒等式。SymPyによる360二次式と全係数の検算。
- [audit_i4_quadratic_weight.py](audit_i4_quadratic_weight.py)：全 $n$ の二次式による積の制限。10セルの重み・正値性・定数を標準Pythonで確認。
- [audit_i4_five_cell_closeout.py](audit_i4_five_cell_closeout.py)：対象5類の5セル分岐を全列挙し、二次式とPell降下の有限部分を検算。一般証明は研究ノート、記号計算にはSymPyを使用。
- [audit_quadratic_relaxation_i27.py](audit_quadratic_relaxation_i27.py)：全32,547直線と666二次式の条件を満たす指数の有理数配置を整数で検証。元問題の反例ではない。
- [replay_september27_attachments.py](replay_september27_attachments.py)：原本保存を確認し、三添字の全範囲と26添字の有限域の全5検証を隔離コピーで再生。
- [audit_maximal_row_moment.py](audit_maximal_row_moment.py)：新しい行番号の和の不等式の定数・全行集合・有理数の緩和配置を検算。標準ライブラリのみ。

9月26日の統合・追加研究の入口：

- [audit_handoff_integration_2026_09_26.py](audit_handoff_integration_2026_09_26.py)：追加の引継ぎ2件の原本保存、余因子・定数、空行の302候補、全36支持配置と被覆証拠。一般の占有枝の省略部分は認証しない。
- [replay_september26_attachments.py](replay_september26_attachments.py)：添付の114ハッシュ項目と6監査を、原本を書き換えずに再生。
- [replay_weighted_cover_extension.py](replay_weighted_cover_extension.py)：$i=29$、$35\le i\le119$ の全区間・小範囲例外・無限尾部を検証。
- [audit_weighted_common_divisor.py](audit_weighted_common_divisor.py)：共通約数の下界と、線形の重み族内の最適化を監査。
- [certify_weighted_cover_extension.py](certify_weighted_cover_extension.py)：拡張証明書を生成。再生器とは別の対数区間計算を使う。

`run_magma_*.py`は指定した入力を外部のMagma計算サービスへ送るためのものです。
保存済みの応答を検算するだけなら実行は不要です。
