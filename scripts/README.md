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

10月3日の研究継続の入口：

- [audit_adjacent_digit_descent.py](audit_adjacent_digit_descent.py)：全添字に共通する完全付値の復元、隣接行の正の実根、モニック逆順除算、桁の重み2以下と二か所の重み3の全指数排除、全素数の乗法的結合、i=5の整数上限・桁和を再生。30,586の局所桁診断・190多項式診断・216消去式・乗法部分群の完全閉包を普遍証明と区別。一般i=5と問題全体は未解決。
- [audit_i5_sparse_allocation.py](audit_i5_sparse_allocation.py)：重い3行の8セル以下の全880配置を、全Taylor係数・厳密除算・終結式・共通成分の正値・整数閾値で再生。9セル以上の必要条件、任意の2セル選択の外側の積の下限、5の完全付値の条件付き持ち上げと奇数付値100・112、全次数の容量とBFTの限界を記録。9類全体と一般i=5は未解決。
- [build_i5_sparse_allocation_certificate.py](build_i5_sparse_allocation_certificate.py)：同じ880配置の証明書の生成・再開。全再生成は `--fresh`。生成だけで独立検算に代えない。
- [audit_i5_global_product_and_affine.py](audit_i5_global_product_and_affine.py)：ZIP統合後の最新稿。復元分母、45類の排除、付値下限、全積・二項係数恒等式、直線のセル集約と零直線、全nのj・中央・有理直線近傍、不均衡と非有効な有限性の適用代数を再生。残る合同類は9・64。古典的外部定理の証明・未知の上限・一般i=5の解決は認証しない。
  続行でn−1,n,n＋1の完全冪の全排除に必要な因数分解・LTE・整数閾値と、n=3^f5^dの全排除も再生。有限の診断例と本文の普遍証明を区別する。
- [audit_i5_multiplicity_frontier.py](audit_i5_multiplicity_frontier.py)：現在の最優先。9証明書の局所重複度を二方法で照合し、行0最大・分母360周期・四次六次の非零性・復元5の同時評価・BFT支持02閉鎖・混合上界・剰余・純冪の端点を再生。残る支持は01。容量障壁の全次数と付値式の普遍性は紙上証明を参照。一般i=5は未解決。
- [audit_github_baseline.py](audit_github_baseline.py)：GitHub取得記録と基準Git object・READMEバイト列を照合し、全504基準パスの同梱・保持・変更と全追加パスを列挙。Git objectのある開発checkoutで実行。ZIP単体は同梱SHA256.jsonで検証。
- [audit_i3_quintic_split_allocation.py](audit_i3_quintic_split_allocation.py)：次数5・deg J=3の両定数桁の全14型を再生。補数を使わず完全分配を閉じ、第二条件の残余への圧縮も確認。
- [audit_i3_split_mahler_frontier.py](audit_i3_split_mahler_frontier.py)：高次数の測度評価、残余次数5の全域と残余次数6の高次数排除、aD6≤13・q≤13,762の厳密な証明書。有限境界全体の列挙ではない。
- [audit_october03_integration.py](audit_october03_integration.py)：原本2件・展開12件のハッシュ、26行モーメント表、i=5の容量2証明書を再構築。他の支持の終端検算は未添付。

10月2日の研究継続の入口：

- [audit_i3_cubic_cofactor.py](audit_i3_cubic_cofactor.py)：任意 P の整数圧縮、次数8以上の三次因子と中央の次数7、導かれた206配置・2,548商を前後二列挙・全商と全CRTで再生。次数7の小さい端点の構造的 q>5F1、三群共有と深い2進持ち上げも検算。
- [audit_i3_quadratic_cofactor.py](audit_i3_quadratic_cofactor.py)：次数6以上の任意二次商の有限残り993配置・12,308商を二方式で再生。次数5中央割当ての普遍的符号証明書も確認。
- [audit_i3_sextic_partial_sharing.py](audit_i3_sextic_partial_sharing.py)：六次の部分共有、六圧縮、30ノルム、最高次零、全上界、b=1の負根・付値式・64剰余・28例外。全奇素数の最後の排除は紙上証明。
- [audit_i3_even_multiplier.py](audit_i3_even_multiplier.py)：奇素数接続、4,698割当て、54CRT標準形、任意半次数の圧縮と第二の整数、全高次上界、法5の14組、十二次の適用限界。
- [audit_i3_split_geometric.py](audit_i3_split_geometric.py)：保存済み本文から独立に復元。3,905係数ベクトル・19許容例を二方式で比較し、圧縮・整数商・適用限界を確認。
- [audit_i3_arbitrary_cofactor.py](audit_i3_arbitrary_cofactor.py)：任意の共有因子の恒等式と全三商、三次の消去、19分岐の完全被覆、符号証明書、17合同証明書の全4,096剰余、前稿の七判別式を検算。全体が一つの $J-s$ を重複度込みで割る枝を三次以上で数値排除し、一般の $i=3$ は未解決。

10月1日の研究継続の入口：

- [audit_i3_adjacent_resultants.py](audit_i3_adjacent_resultants.py)：両隣接法の全非共有部分、因子の重複度、整数終結式、全25商分岐と七判別式、幾何級数を共有する族の全数値排除を検算。有限診断を一般証明の代用にせず、一般の $i=3$ は未解決。
- [audit_i3_half_degree_composition.py](audit_i3_half_degree_composition.py)：任意次数の半次数の境界、合成の整除性、有理原点・モデル、内側の全係数の整数性と5倍性を検算。有限合成例を一般証明の代用にしない。八次の $h=3$ と一般の i=3 は未解決。
- [audit_i3_prime_power_resultants.py](audit_i3_prime_power_resultants.py)：完全素数冪への桁まとめ、正実根の因子の終結式とSylvester行列、LCMによる有限化、異なる素因数個数での桁予算を検算。一般の $i=3$ は未解決。
- [audit_i3_septic_and_saturation.py](audit_i3_septic_and_saturation.py)：七次の全有理分類、全評価の共通素数7、任意次数の下限・対称飽和補題、八次の3+5排除に用いた恒等式。八次全体と一般の $i=3$ は未解決。
- [audit_i3_sextic_closeout.py](audit_i3_sextic_closeout.py)：六次の全有理分岐の分類・整数評価の排除、全原点表、消去証明書、3進付値の検算。一般の $i=3$ は未解決。

10月1日の半比率・中央飽和と均衡境界：

- [audit_i3_central_square_descent.py](audit_i3_central_square_descent.py)：中央群の二つの平方差と低次数のノルム恒等式、全比率の均衡中央飽和の $h>11u/15$、等号の係数の矛盾と一般中央群の三分岐制限を検算。無限降下や一般の $i=3$ の解決は主張しない。
- [audit_i3_half_ratio_central_bounds.py](audit_i3_half_ratio_central_bounds.py)：全半比率分配の $h>(5u-v)/6$、中央群の二つの下限、均衡中央飽和の $h>5u/7$ に使う元の恒等式、平方差、偶六次の係数、次数の整数丸めを検算。一般の $i=3$ は未解決。

- [audit_i3_balanced_boundary.py](audit_i3_balanced_boundary.py)：均衡最小境界の全排除の有限例外、疎な恒等式、解析評価の厳密な分数、2進の整数係数条件、全分配の差次数下限を検算。標準PythonとSymPy。一般の $i=3$ は未解決。

9月30日の研究継続の入口：

- [verify_latest.py](verify_latest.py)：今回の4検算と先行する20数学検算、原本保存・リンク確認の計25件を実行し、失敗時に停止。依存は[requirements-verification.txt](../requirements-verification.txt)。
- [audit_i3_sextic_working_models.py](audit_i3_sextic_working_models.py)：六次の明示二族の両整除条件・行列式・原点と非負性だけを確認。一般分類・整数条件・反例排除を認証しない。
- [audit_i3_extremal_split_closeout.py](audit_i3_extremal_split_closeout.py)：任意次数の端点分配の三次合成への分類と数値排除。SymPyで恒等式と3進条件を検算。
- [audit_i3_quintic_closeout.py](audit_i3_quintic_closeout.py)：五次族の反例の全排除。隣接する5乗の比較、法28001の全剰余と多項式証明書を標準Pythonで検算。
- [audit_i3_quintic_digit_classification.py](audit_i3_quintic_digit_classification.py)：係数無制限の五次分類、商の分母、Bézout恒等式と純冪指数合同条件。SymPyを使用。
- [audit_i4_six_cell_capacity.py](audit_i4_six_cell_capacity.py)：全103支持の有理重みと小素数冪の下限。標準Python。
- [audit_polynomial_capacity_supports.py](audit_polynomial_capacity_supports.py)：旧四配置を排除する整数多項式と尾部閾値。
- [audit_iterated_polynomial_capacity.py](audit_iterated_polynomial_capacity.py)：追加33多項式の全支持・閾値、最後の102セル配置の全35容量。
- [audit_known_bridge_and_i4_fixed_j.py](audit_known_bridge_and_i4_fixed_j.py)、[replay_i4_fixed_j.py](replay_i4_fixed_j.py)：$i=4$ の有限 $j$・全 $n$ と、既知小 $j$ の12例外。二つの独立な算式で再生。

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
