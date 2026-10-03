# 検算の案内

[入口](../README.md) · [現在地](STATUS.md) · [コード一覧](../scripts/README.md) · [データの場所](../data/README.md)

以下のコマンドは**リポジトリのルート**で実行します。Pythonのassertを使うため、`python -O`は使わないでください。
各ノートの検算はその主張に対応するもので、全てを一度に実行する必要はありません。

## 10月3日のZIP統合時の再検算

この作業フォルダへの統合では、受領ZIPの隔離コピーで `python scripts/verify_latest.py` の全32件を通しで再実行し、すべて通過しました。Python 3.14.3、SymPy 1.14.0を使用しました。下記の「今回通し再実行していない」という記述と過去のログは、配布元での実行履歴です。今回の結果は[統合記録](IMPORT_2026-10-03.md)に保存しています。

    python -X utf8 scripts/replay_all_progress_import.py

[統合原本の照合器](../scripts/replay_all_progress_import.py)は受領ZIP、665ハッシュ項目、更新前13ファイル、統合時点の全ファイルを確認します。その後に研究を更新した場合、原本保存だけの確認には `--source-only` を指定します。配布元のBUILD_METADATA.jsonは現在のGitコミットを表すものではありません。

## 必要なもの

- Python。9月30日の整理と再検算ではPython 3.12.14を使用。以前の記録ではPython 3.14.3を使用。
- 代数の検算にはSymPy。既存の記録ではSymPy 1.14.0を使用。
- 一部の証明書の**再生成**にはNumPy。標準ライブラリだけで動く再生器とは区別します。
- 保存済みMagma応答のローカル検算には、Magmaへの再送信は不要です。

必要に応じて `python -m pip install sympy` で導入できます。

## 最新の検算をまとめて実行

    python -m pip install -r requirements-verification.txt
    python scripts/verify_latest.py

[実行器](../scripts/verify_latest.py)は最新の全添字の桁降下・乗法部分群、i=5の880分配・5の高桁・積・付値・直線近傍と先行する9証明書、10月3日の先行3検算、三次因子の部分共有・五次の全排除・任意二次商・六次部分共有・奇素数接続・全共有を含め、先行する任意一次商・両隣接法・中央群・均衡境界・5冪・低次数・i=4などと、構文・リンク・原本保存を含む計35件を順に実行し、失敗した時点で停止します。
SymPy 1.14.0を[依存ファイル](../requirements-verification.txt)で固定しました。
リポジトリのルート以外から実行しても、保存先をルート基準で解決します。
過去の全証明の再生をまとめたものではなく、今回の更新範囲の確認です。

## 最新：全添字の桁降下と、全素数の行積の結合

    python -X utf8 scripts/audit_adjacent_digit_descent.py

[新稿](../research/general/adjacent_row_digit_descent_2026-10-03.md)の完全付値復元、正の実根による全体整除の否定、逆順モニック整数除算、有界桁和・素数個数の有効上限を確認します。30,586素数単位の診断、190除算、低桁重みの終結式、重み3の216消去式と54零終結式、各96剰余型、法24の乗法部分群の完全閉包、全整数閾値を再生します。重み2以下・二か所の重み3を全指数で閉じ、全底が最小桁和の二族を全素数個数で排除しました。普遍性は本文の証明に依存し、有限診断の外挿ではありません。問題699・一般i=5は未解決。

GitHub更新前に、現在登録した全35件を通しで再実行して全件通過しました。[今回の実行ログ](../data/results/verification_github_publish_2026-10-03.log)と[実行記録](../data/results/verification_adjacent_digit_continuation_2026-10-03.json)を保存しています。受領時の32件の隔離再生と、その後の個別再生も各時点の履歴として保持します。

## 先行：i=5の880分配と5の高桁条件

    python -X utf8 scripts/audit_i5_sparse_allocation.py

[新稿](../research/i5/i5_odd_sparse_allocation_and_prime5_lift_2026-10-03.md)の全880配置を、生成器とは別のTaylor係数計算・厳密除算・終結式・Cauchy根上界・20共通成分の正値・整数閾値で再生します。8セル以下の完全被覆から9セル以上を強制し、任意の2セル選択の外側の積も評価します。5の全桁条件からの条件付き完全付値復元は紙上証明と診断を区別し、奇数付値100・112および25の枝の102・115を整数冪で確認します。一般9類とi=5は未解決。

[生成器](../scripts/build_i5_sparse_allocation_certificate.py)は保存済み配置から再開できます。`--fresh` は全880配置を再生成します。証明書の生成と独立検算を区別します。全次数の手法の限界は新稿第8節の普遍的制限次数の証明が根拠であり、有限次数の診断を全次数へ外挿していません。

この検算器の追加時点では34件でした。最新の桁降下検算を加えた現在の登録数は35件です。

## ZIP統合後の続行：i=5の積・45類・直線近傍

    python -X utf8 scripts/audit_i5_global_product_and_affine.py

[新稿](../research/i5/i5_global_product_and_affine_exclusions_2026-10-03.md)の復元5を含む全分母、二項係数恒等式、全セルの直線集約、零直線、jと中央近傍の全整数閾値、付値下限、CRT必要進行、復元余因子の不均衡を検算します。[結果](../data/results/verification_i5_global_product_and_affine.json)に各範囲と外部依存を保存しました。古典的Mahlerの定理から得る有限性は非有効であり、未知の数値上限を検算したとは主張しません。

この稿の追加時点では計33件、880分配検算の追加後は34件、現在は35件です。統合時に通過した32件の記録はその時点の履歴として保持しています。

この検算は続行で、n−1,n,n＋1の完全冪の全排除も含むよう拡張しました。平方根の完全な余因子分解、奇数指数のLTE、指数無制限の単調性に用いる整数閾値、全ての奇数5-smooth整数の合同式を照合します。根・指数の診断例の列挙を全域の証明と取り違えないでください。一般尾部の有効な指数条件が両立する有理点も保存しています。

## 先行：i=5 の9証明書と支持02の閉鎖

    python -X utf8 scripts/audit_i5_multiplicity_frontier.py

[紙上証明](../research/i5/i5_multiplicity_frontier_2026-10-03.md)の局所重複度をTaylor平行移動と偏導関数の二方法で照合し、9証明書の全セル被覆・正値性・次数・対直線・評価定数・分母360周期・閉鎖閾値を再生します。行0最大と、$n\ge10^{24}$ の最後2支持への直接証明を確認します。必要6剰余と純冪の指数端点・単調性も検算します。

全次数の容量障壁と純冪の普遍付値式は紙上証明が根拠です。有限曲線の検査や初期500指数の付値照合を普遍証明に読み替えません。浮動小数点最適化・未提供のMatveev終端スクリプトはこの証明の依存ではありません。一般i=5は未解決。結果は[全証明書JSON](../data/results/verification_i5_multiplicity_frontier.json)。先行31検算は以前通過済みで、今回全32件の通し再実行は行っていません。

同じ検算器は、四次・六次の圧縮表示と整数係数の一致、復元5と非最大分母の同時360周期、$B<200n^{1/4}$、$10^{75}$ の閾値を厳密比較します。外部Bennett–Filaseta–Trifonov Theorem 2.1と併用して支持02を閉じ、残る支持は01のみです。外部定理の証明そのものは再生しません。先行する $R_0<23n^{23/400}$ と形式的なノルム診断も履歴として保持します。

今回の対象3件（新i=5検算、追加資料の再照合、構文・リンク・原本検査）は通過しました。[実行ログ](../data/results/verification_i5_2026-10-03.log)に対象と実出力を保存しています。

支持02閉鎖と全進展ZIPへの更新では、この3件を更新後に再生し、さらに[GitHub基準の全504パス照合](../scripts/audit_github_baseline.py)も通過しました。最新4件の出力は同じ実行ログに保存しています。GitHub照合器はGit objectのある開発用checkoutで動き、ZIP単体はSHA256.jsonを使います。

## 10月3日の追加資料、完全分配と有限境界

    python -X utf8 scripts/audit_i3_quintic_split_allocation.py
    python -X utf8 scripts/audit_i3_split_mahler_frontier.py
    python -X utf8 scripts/audit_october03_integration.py

[全14型の証明](../research/i3/i3_quintic_split_allocation_repair_2026-10-03.md)の両定数桁・係数消去・4有限形・有理数上界を再生します。[測度の証明](../research/i3/i3_split_mahler_frontier_2026-10-03.md)は3つの高次数の正係数証明書、aD6≤13の単調性、q≤13,762の整数証明書を再生します。この有限域全体を列挙したものではありません。

[追加資料の監査](../research/general/october03_integration.md)は2原本とZIP19項目・12ハッシュ、26行モーメント表、i=5の支持{0,2}の2容量証明書を独立に照合します。添付されなかったMatveev・連分数の終端検算や、全支持の閉鎖は認証しません。

## 10月2日の三次因子と複数群への部分共有

    python -X utf8 scripts/audit_i3_cubic_cofactor.py

[紙上証明](../research/i3/i3_cubic_cofactor_partial_sharing_2026-10-02.md)の任意因子 P の圧縮、全三割当ての上界、4つの正係数証明書、次数7の小さい端点の法8と構造的な $q>5F_1$ を再生します。数学的に導かれた有限残り206配置・2,548商を前後の独立列挙で比較し、全商と全CRTの二方法で第一条件の一致0を確認します。三群共有の具体例と、同じ式の $2^{51}\mid n$ への持ち上げも検査します。後者の底が素数冪とは主張しません。結果は [verification_i3_cubic_cofactor.json](../data/results/verification_i3_cubic_cofactor.json)。一般の i=3 は未解決です。

## 10月2日の二次商と部分共有の追加検算

    python -X utf8 scripts/audit_i3_quadratic_cofactor.py
    python -X utf8 scripts/audit_i3_sextic_partial_sharing.py
    python -X utf8 scripts/audit_i3_even_multiplier.py
    python -X utf8 scripts/audit_i3_split_geometric.py

[任意二次商](../research/i3/i3_quadratic_cofactor_single_allocation_closeout_2026-10-02.md)の完全な有限残りは993配置・12,308商、一致0。前後の独立列挙・畳み込み・第二評価で照合し、次数5中央割当ての全底の二つの符号証明書も確認します。次数5の全端割当てを閉じた検算ではありません。
[六次部分共有](../research/i3/i3_sextic_partial_sharing_closeout_2026-10-02.md)は六圧縮・30係数ノルム・最高次零の全形・狭義有理上界・負根と微分・64剰余・28小底例外を再生。b=1 の最後は完全Q1と全奇素数Kummerの紙上論証です。
[奇素数接続](../research/i3/i3_odd_prime_gluing_and_even_multiplier_2026-10-02.md)は4,698割当て中54有効例、54 CRT標準形、任意半次数の恒等式・全高次上界・法5の14組・十二次の適用限界を確認します。
[全共有の先行本文](../research/i3/i3_integral_root_values_and_split_geometric_closeout_2026-10-02.md)は保存された11824バイトをそのまま復元し、検算器は独立に作り直しました。3,905係数ベクトル中19許容例を巡回畳み込みと分円因子の独立除算で照合します。全次数の分母・分散分類は紙上証明に依存します。
結果はそれぞれ `data/results/verification_i3_quadratic_cofactor.json`、`verification_i3_sextic_partial_sharing.json`、`verification_i3_even_multiplier.json`、`verification_i3_split_geometric.json`。設定と残る証明義務は[AI引き継ぎ](AI_HANDOFF_2026-10-02.md)を参照します。

## 10月2日の任意の共有因子の全数値排除

    python scripts/audit_i3_arbitrary_cofactor.py

[紙上証明](../research/i3/i3_arbitrary_cofactor_closeout_2026-10-02.md)の任意の $B$ の恒等式、商の全三形と補数、三次の消去式、符号証明書、19組の完全被覆を検算します。
17個の合同証明書は法4・8・12の全4,096剰余を再生し、整数パラメータの全体を覆います。幾何級数の残りは前稿の七判別式の検算を呼び出して再生します。
[結果JSON](../data/results/verification_i3_arbitrary_cofactor.json)に、非幾何級数・重根の局所診断と、次数・4の条件を外せない例も保存します。全共有因子が一つの $J-s$ を重複度込みで割る場合の排除であり、複数の割当てなどを含む一般の $i=3$ は未解決です。

## 10月1日の両隣接法と幾何級数族の全数値排除

    python scripts/audit_i3_adjacent_resultants.py

[紙上証明](../research/i3/i3_adjacent_resultants_and_geometric_closeout_2026-10-01.md)の共有因子の全重複度除去を因数分解と独立に照合し、終結式をSylvester行列でも確認します。
全25組の整数の商の符号証明書、七つの判別式、法8・16・7の排除、隣接平方の差を厳密に再生します。
四次以上は一般の不等式、三次は全整数パラメータの符号と合同式で排除し、有限診断から外挿しません。
[結果JSON](../data/results/verification_i3_adjacent_resultants.json)は、一つの底の局所診断と真の反例を区別します。幾何級数族以外の一般の $i=3$ は未解決です。

## 10月1日の中央群の二段平方降下と11/15境界

    python scripts/audit_i3_central_square_descent.py

[紙上証明](../research/i3/i3_central_square_descent_2026-10-01.md)の二つの平方差、二次式と判別式、低次数のノルム、等号の四次式への消去、定数項と四次項の係数、正の二次式への還元を厳密に再生します。
3,958,140件の次数の変換、33件の11/15等号の次数構造、10,000件の低次数剰余の比較は補助診断です。全次数の証明は紙上の恒等式と次数比較に依存します。
一般の $i=3$、無限平方降下、高い差次数、5冪の芯、一般数値領域は未解決です。

## 10月1日の全半比率分配と中央飽和の厳密下限

    python scripts/audit_i3_half_ratio_central_bounds.py

[紙上証明](../research/i3/i3_half_ratio_and_central_saturation_bounds_2026-10-01.md)の元の行列式からの6恒等式、三次の判別式、二つの平方恒等式、低次数の平方差、偶六次の最高次係数と非零定数項を厳密に再生します。
半比率の338,350件の次数丸め、中央群の9,410,061件の非負次数、57件の5/7等号の次数構造は補助診断です。有限診断から全次数を外挿しません。
半比率の $h>(5u-v)/6$ と均衡中央飽和の $h>5u/7$ は紙上証明に依存します。
一般の $i=3$、高い差次数、5冪の芯、一般数値領域への移行は未解決です。

## 10月1日の均衡境界の全排除と全分配の下限

    python scripts/audit_i3_balanced_boundary.py

[紙上証明](../research/i3/i3_balanced_boundary_closeout_2026-10-01.md)の有限例外855件と3430件の非零剰余証明書、33芯の両整除性、22疎多項式恒等式、176Taylor係数を検算します。
解析評価の有理部分和・無限尾部の上界、24偶数芯の2進係数、二例外の六次族への変換も再生します。
空の中央群の整除性の恒等式と、新しい全分配の $h\ge\lceil(8u-v)/12\rceil$ の整数丸めも確認します。
全次数の分類・分母補題・根の配置は紙上証明に依存し、有限診断から外挿していません。
一般の $i=3$、より高い差次数、奇数芯 $D=5^a,a\ge4$、数値領域全体は未解決です。

## 10月1日の5冪の共通枝と25・125の芯

    python scripts/audit_i3_five_power_composition.py
    python scripts/audit_i3_five_power_low_degree_closeout.py

[紙上証明](../research/i3/i3_five_power_composition_and_local_frontier_2026-10-01.md)の全指数の共通5進根、$n$ の剰余と指数、合成の補正、固定法の合同式の整合性に対応します。
二次環の反復二乗を独立な二階漸化式でも照合し、$a\le100$ の診断を保存しました。この有限診断から全指数を外挿しません。
25・125の芯は26件のFrobenius・Bézout恒等式で全40組の指数の剰余を被覆します。
素数性・位数・必要剰余を再生し、指数やパラメータの上限を使わずに全評価を排除します。
[証明書](../data/certificates/i3_five_power_low_degree_closeout_2026-10-01.json)の再生は標準PythonとSymPyのみで、探索用の有限体ライブラリは不要です。
この配置で $a\ge4$、他の多項式分配、一般数値領域は残ります。

## 10月1日の半次数の合成と整数係数条件

    python scripts/audit_i3_half_degree_composition.py

[紙上証明](../research/i3/i3_half_degree_composition_2026-10-01.md)の境界の6恒等式、45合成整除、20有理モデル恒等式・整除、原点の分岐を検算します。
288件の係数付値と240件の法5の合成も確認し、内側の分母と全係数の5倍性を区別します。
56合成例・168整数評価は補助診断で、次数80までの検算から一般定理を外挿しません。負の係数を持つ内側の例も含みます。
[結果JSON](../data/results/verification_i3_half_degree_composition.json)は、多項式移行済みの境界の排除と、一般の i=3 の未解決を区別します。
五次の全整数評価の排除は既存の証明と一括検算で再生します。

## 10月1日の一般数値領域・完全素数冪・終結式

    python scripts/audit_i3_prime_power_resultants.py

[任意次数の紙上証明](../research/i3/i3_prime_power_resultant_frontier_2026-10-01.md)に対応します。130,218件のブロック進への含意、逆向きの反例、16積恒等式、2,548ノルム評価、600LCM整除、二つの桁予算恒等式、580閾値比較を確認します。
8数値診断例の終結式をSylvester行列の行列式でも照合します。末尾1は二つの数値整除条件、末尾0は証明に必要な前半だけを使い、全素数での反例とは扱いません。
[結果JSON](../data/results/verification_i3_prime_power_resultants.json)は仮定の差と一般領域の未解決を明記します。有限検算と条件付き有限化を、一般の i=3 の証明に数えていません。

## 10月1日の七次・任意次数・八次の一分配

    python scripts/audit_i3_septic_and_saturation.py

[七次の紙上証明](../research/i3/i3_septic_closeout_2026-10-01.md)、[差の下限と八次の3+5の排除](../research/i3/i3_half_degree_bound_and_octic_frontier_2026-10-01.md)、[任意次数の対称飽和補題](../research/i3/i3_symmetric_saturation_2026-10-01.md)に対応します。
上位係数の還元、二次環の跡・ノルム、有限体での三次式の既約性、全有理原点・符号、整数係数と7進付値の恒等式を確認します。
262整数評価の診断と、全評価の紙上証明を区別しています。
[結果JSON](../data/results/verification_i3_septic_and_saturation.json)は七次の閉鎖を記録し、八次全体・一般の $i=3$ の未解決を明示します。

## 10月1日の六次の閉鎖

    python scripts/audit_i3_sextic_closeout.py

[紙上証明](../research/i3/i3_sextic_closeout_2026-10-01.md)の全有理パラメータ還元、全12原点・符号の表、整数係数条件、最後の枝の短い消去恒等式、共通素数3の全合同類をSymPy 1.14.0で検算します。
[結果JSON](../data/results/verification_i3_sextic_closeout.json)に、六次の反例排除と一般の $i=3$ の未解決を区別して保存しています。
256個の整数評価は付値の補助診断で、普遍的な結論の根拠は紙上証明です。

添付更新の初回再生では数学の9検算は通過しましたが、原本保存検査が `.gitattributes` の変更を検出しました。
保護対象のルート設定を元のバイト列へ戻し、フォーラム原文の行末空白の設定をそのフォルダ内の設定へ移しました。
原本のハッシュ検査を緩めずに、一括検算を復旧しています。

## 9月30日の研究継続

```text
python scripts/audit_i3_quintic_digit_classification.py
python scripts/audit_i3_quintic_closeout.py
python scripts/audit_i3_extremal_split_closeout.py
python scripts/audit_i3_sextic_working_models.py
python scripts/audit_i4_six_cell_capacity.py
python scripts/audit_polynomial_capacity_supports.py
python scripts/audit_iterated_polynomial_capacity.py
python scripts/audit_known_bridge_and_i4_fixed_j.py
python scripts/replay_i4_fixed_j.py
python scripts/check_repository.py
```

最初はSymPyで、五次分類の九分岐・三候補・因数分解・Bézout恒等式・5進例外・指数合同条件を確認します。一般分類の根拠は[紙上証明](../research/i3/i3_quintic_digit_classification_2026-09-30.md)です。

[五次の閉鎖](../research/i3/i3_quintic_closeout_2026-09-30.md)は、$M=3$ の隣接する5乗の恒等式と、$M=1$ の法28001の全剰余・別の多項式証明書を検算します。反例に必要な条件を保って五次の族を全排除し、一般の $i=3$ は未解決です。

任意次数の[端点分配の閉鎖](../research/i3/i3_extremal_split_closeout_2026-09-30.md)の検算にはSymPyを使い、微分に使う恒等式・三次の合成・3進の数値条件を確認します。任意次数の根拠は紙上証明です。

[六次の作業モデル](../research/i3/i3_sextic_working_notes_2026-09-30.md)の検算は、二つの明示族の行列式・両整除条件・因子群次数・有理原点と非負性だけを確認します。
[結果JSON](../data/results/verification_i3_sextic_working_models.json)でも、一般分類・整数パラメータ分類・数値の反例排除は認証しないと明記しています。

残りの新検算は標準Pythonだけで動きます。6セルの全103有理証明書、高次数の全37支持の整数係数・零点・無限尾部閾値、最後の102セル有理配置の全32,547直線・666二次式・35追加容量を再計算します。

有限 $j$ の生成・再生は、異なる算式で496,499整数を完全走査し、全53,072約数と唯一の橋渡し候補を一致させます。無限尾部は初等的な付値評価で閉じ、EEES78の定理には依存しません。既知の小 $j$ 領域の接続だけはEEES78に依存し、一次PDFのハッシュと全12例外・41共通素数を確認します。

全て部分結果の検算であり、28添字の完全解決を認証しません。詳細・結果へのリンクは[研究継続の記録](../research/general/continuation_2026-09-30.md)を参照してください。

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

AI引き継ぎ一式は、変更をコミットしてから次で作成します。

    python scripts/package_results.py --include-git-metadata --output dist/erdos699_ai_handoff_2026-10-02.zip

`BUILD_METADATA.json` に確定コミット・枝・時刻を記録し、このファイルも全体の SHA-256 照合に含めます。Git の履歴データベースは同梱しません。[今回の25件の通過ログ](../data/results/verification_latest_2026-10-02.log)も保存しました。
