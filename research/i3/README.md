# i=3：数値条件と多項式分配

[入口](../../README.md) · [分野一覧](../README.md) · [現在地](../../docs/STATUS.md) · [用語](../../docs/GLOSSARY.md)

**一般のi=3は未解決です。** この分野はノートが多いため、まず前提を確認し、下の3つの経路を選んでください。
標準桁の $F(0)=1$ と、変換後の $F(0)=2$ の設定は、別の仮定を持ちます。

## まず前提を読む

- [非平方枝の正規化](i3_nonsquare_merged_continuation.md)：反例候補を整理する基本の記号。
- [全桁のKummer条件](i3_global_digit_constraints_2026-09-19.md)：一つの素数と全素数の条件を区別。
- [専門的な引き継ぎ](../../docs/AI_HANDOFF_2026-10-02.md)：二つの桁設定と適用境界をまとめた詳細。

## 経路A：一般数値領域

1. [完全素数冪と正実根の終結式](i3_prime_power_resultant_frontier_2026-10-01.md)：多項式全体への移行を仮定しない条件付き上限。
2. [両隣接法と幾何級数](i3_adjacent_resultants_and_geometric_closeout_2026-10-01.md)：特定の共有族を数値条件から全排除。
3. [任意の共有因子の一割当て](i3_arbitrary_cofactor_closeout_2026-10-02.md)：$B\mid J-s$ を重複度込みで満たす枝。
4. [任意二次商](i3_quadratic_cofactor_single_allocation_closeout_2026-10-02.md)・[三次因子の部分共有](i3_cubic_cofactor_partial_sharing_2026-10-02.md)：外側の因子を増やした制限。

複数群への一般の共有、正実根の因子、増大する桁和などは残ります。

## 経路B：多項式へ移行済みの分配

1. [八次の閉鎖](i3_octic_last_branch_2026-10-01.md)：先行する低次数の分類と接続し、移行済み設定の次数8以下を扱う。
2. [チェビシェフ境界](i3_chebyshev_boundary_and_prime_transfer_2026-10-01.md) → [5冪の枝](i3_five_power_composition_and_local_frontier_2026-10-01.md)：特定の任意次数境界。
3. [中央群の平方降下](i3_central_square_descent_2026-10-01.md)：均衡中央飽和の $h>11u/15$ など。
4. [整数根値と幾何級数の分割](i3_integral_root_values_and_split_geometric_closeout_2026-10-02.md)：特定の全共有を全割当てで排除。

九次以上の一般分配と、数値からの一般移行は残ります。本文の前提を保って読んでください。

## 経路C：標準桁の完全分配

1. [次数5の割当ての修復](i3_quintic_split_allocation_repair_2026-10-03.md)：両定数桁の全14型を直接排除。
2. [残余次数とMahler測度](i3_split_mahler_frontier_2026-10-03.md)：残余次数5を排除。残余次数6の一枝を $aD_6\le13,q\le13,762$ に有限化。

この有限境界の全排除は未実施です。経路Bの低次数結果を別設定へ無条件に移さないでください。

## 代表的な証明と検算

| 対象 | 再生器 | 保存結果 |
|---|---|---|
| 完全素数冪の数値評価 | [audit_i3_prime_power_resultants.py](../../scripts/audit_i3_prime_power_resultants.py) | [結果](../../data/results/verification_i3_prime_power_resultants.json) |
| 両隣接法 | [audit_i3_adjacent_resultants.py](../../scripts/audit_i3_adjacent_resultants.py) | [結果](../../data/results/verification_i3_adjacent_resultants.json) |
| 任意の共有因子 | [audit_i3_arbitrary_cofactor.py](../../scripts/audit_i3_arbitrary_cofactor.py) | [結果](../../data/results/verification_i3_arbitrary_cofactor.json) |
| 二次商 | [audit_i3_quadratic_cofactor.py](../../scripts/audit_i3_quadratic_cofactor.py) | [結果](../../data/results/verification_i3_quadratic_cofactor.json) |
| 中央群の平方降下 | [audit_i3_central_square_descent.py](../../scripts/audit_i3_central_square_descent.py) | [結果](../../data/results/verification_i3_central_square_descent.json) |
| 標準桁の完全分配 | [audit_i3_split_mahler_frontier.py](../../scripts/audit_i3_split_mahler_frontier.py) | [結果](../../data/results/verification_i3_split_mahler_frontier.json) |

他の係数・曲線・低次数の証明は下の索引から探せます。
[検算手順](../../docs/VERIFICATION.md) · [全コード](../../scripts/README.md)

## 全ノート索引

<details>
<summary>全68件を表示（原題・ファイル名を保持）</summary>

| ファイル名の日付 | ノート |
|---|---|
| 本文参照 | [i=3：判別式の2進指数と M=3 の平方の枝](i3_2adic_and_square_continuation.md) |
| 2026-10-01 | [i=3：二つの隣接法の終結式と、幾何級数を共有する族の全数値排除](i3_adjacent_resultants_and_geometric_closeout_2026-10-01.md) |
| 本文参照 | [i=3：全ての奇数 M に対する平方の枝の排除](i3_all_square_branches.md) |
| 2026-10-02 | [i=3：任意の共有因子を一つの添字へ割り当てる枝の数値排除](i3_arbitrary_cofactor_closeout_2026-10-02.md) |
| 2026-10-01 | [i=3：均衡最小境界の全排除と、全分配の差次数下限](i3_balanced_boundary_closeout_2026-10-01.md) |
| 本文参照 | [Erdős 699：例外の境界と、因子を固定した場合の有限性](i3_boundary_and_fixed_blocks.md) |
| 2026-10-01 | [i=3：中央群の二段平方降下と、中央飽和の 11/15 境界の排除](i3_central_square_descent_2026-10-01.md) |
| 2026-09-20 | [ChatGPT回答の統合：変換の範囲、Dの局所構造、共通因子](i3_chatgpt_uniform_integration_2026-09-20.md) |
| 2026-10-01 | [i=3：全分配のノルム降下と、非均衡境界のチェビシェフ分類](i3_chebyshev_boundary_and_prime_transfer_2026-10-01.md) |
| 2026-09-20 | [Erdős 699：8∣j での Q₁、Q₂ の最小桁和の排除](i3_complement_digit_bounds_2026-09-20.md) |
| 2026-09-20 | [i=3：二つの法の間の評価、一般の桁多項式、二次の例外の完全分類](i3_cross_modulus_and_digit_height_2026-09-20.md) |
| 2026-10-02 | [i=3：三つの一次因子を残す部分共有と、任意次数の因子による圧縮](i3_cubic_cofactor_partial_sharing_2026-10-02.md) |
| 2026-09-20 | [i=3：三次の桁多項式の完全分類と、例外族の3進排除](i3_cubic_digit_classification_2026-09-20.md) |
| 2026-09-21 | [i=3：三次整環の判別式と連分数末尾の制約](i3_cubic_discriminant_and_cf_tail_2026-09-21.md) |
| 2026-09-21 | [i=3：三次式の小判別式を独立に証明し、2進条件で下界を強める](i3_cubic_discriminant_minima_2026-09-21.md) |
| 2026-09-20 | [i=3：降下候補の正確な更新式と、上位桁の非保存](i3_descent_kummer_obstruction_2026-09-20.md) |
| 2026-09-23 | [i=3：全素因数をまとめる桁和評価と、任意次数の因子分配](i3_digit_height_budget_and_factor_degrees_2026-09-23.md) |
| 本文参照 | [Erdős 699：全桁条件の統合、平方剰余の相互法則、W の一般化](i3_digit_reciprocity_and_W_continuation.md) |
| 本文参照 | [Erdős 699：中心・添字からの直接の楕円曲線と、端に近い候補の有限性](i3_direct_center_and_endpoint_curves.md) |
| 2026-09-21 | [i=3：増大する判別式を、悪い還元を持つ素数へ圧縮する](i3_discriminant_support_and_elliptic_curve_2026-09-21.md) |
| 2026-09-21 | [i=3：分母の2進付値を使う近似の下界と、連分数の分母への制約](i3_dyadic_denominators_and_continued_fractions_2026-09-21.md) |
| 本文参照 | [Erdős 699：中心の正確な2進付値と、差 g≤9 の完全な排除](i3_exact_gap_and_g9_continuation.md) |
| 2026-09-30 | [i=3：任意次数の端点分配を三次の合成へ分類し、数値排除する](i3_extremal_split_closeout_2026-09-30.md) |
| 2026-09-20 | [i=3：有限個の素数による排除の限界と、今回の研究記録](i3_finite_prime_obstruction_2026-09-20.md) |
| 2026-10-01 | [i=3：5冪の共通5進枝、25次・125次の芯の全排除](i3_five_power_composition_and_local_frontier_2026-10-01.md) |
| 2026-09-21 | [i=3：4件のチャットの統合と、整数点を保つ判別式降下](i3_four_chat_integration_2026-09-21.md) |
| 2026-09-22 | [$i=3$・偶数 $j$：9月22日の四つの進捗メモの統合](i3_four_handoffs_integration_2026-09-22.md) |
| 本文参照 | [Erdős 699：g=13 の排除と、降下案の検証](i3_gap13_and_descent_continuation.md) |
| 2026-09-21 | [i=3：増大するGにも通用する平方枝の一様排除](i3_gap_square_obstructions_2026-09-21.md) |
| 2026-09-19 | [Erdős 699：全六ブロックの桁和下界と、桁和から別の素数への移行](i3_global_digit_constraints_2026-09-19.md) |
| 2026-09-21 | [i=3：増大する指数差を捉える第二のFrey曲線](i3_growing_gap_and_auxiliary_frey_2026-09-21.md) |
| 2026-10-01 | [i=3：任意次数の半次数下限と、八次の3+5分配の排除](i3_half_degree_bound_and_octic_frontier_2026-10-01.md) |
| 2026-10-01 | [i=3：半次数の境界は四次・五次の合成となり、全次数で数値反例を排除できる](i3_half_degree_composition_2026-10-01.md) |
| 2026-10-01 | [i=3：全半比率分配の厳密下限と、中央飽和の 5/7 境界の排除](i3_half_ratio_and_central_saturation_bounds_2026-10-01.md) |
| 2026-09-20 | [2026-09-20 添付の即時統合と一様な条件への継続](i3_handoff_uniform_integration_2026-09-20.md) |
| 2026-10-02 | [i=3：整数の根値の分類と、分かれた幾何級数の共有因子の排除](i3_integral_root_values_and_split_geometric_closeout_2026-10-02.md) |
| 本文参照 | [Erdős 699：二つの新資料の統合と、中心の整数による継続](i3_integrated_digits_and_center.md) |
| 2026-09-20 | [i=3：三次式の既約性と、有理数へ近づく領域の有効な排除](i3_irreducible_cubic_and_rational_gaps_2026-09-20.md) |
| 2026-09-19 | [Erdős 699：桁和6の排除、中心への整除性の訂正、桁和12の一般下界](i3_low_digit_continuation_2026-09-19.md) |
| 2026-09-20 | [i=3：中心と添字の差による明示的な上限と有限還元](i3_mixed_parameter_bound_2026-09-20.md) |
| 2026-09-23 | [i=3：一般の偶数 j に対する冪の重複と Kummer ブロックの素数台](i3_multiplicity_budget_and_fresh_support_2026-09-23.md) |
| 2026-09-21 | [i=3：新成果の統合、素数冪の合同式、指数差の明示的有限化](i3_new_chat_integration_and_effective_gap_2026-09-21.md) |
| 本文参照 | [Erdős 699：進捗の統合と非平方の枝の継続](i3_nonsquare_merged_continuation.md) |
| 2026-10-01 | [i=3：八次の最後の分岐を有理根のない九次式で閉じる](i3_octic_last_branch_2026-10-01.md) |
| 2026-10-01 | [i=3：八次の飽和分岐と、任意次数の対称な二次中央群を排除する](i3_octic_saturation_and_pell_2026-10-01.md) |
| 2026-10-02 | [i=3：奇素数による根値の接続と奇数半次数の部分共有](i3_odd_prime_gluing_and_even_multiplier_2026-10-02.md) |
| 2026-09-20 | [i=3：素数の直後の整数の冪を、有限の証明書へ還元する](i3_prime_neighbor_powers_2026-09-20.md) |
| 2026-10-01 | [i=3：完全素数冪の桁予算と、正の実根の終結式による任意次数の評価](i3_prime_power_resultant_frontier_2026-10-01.md) |
| 2026-10-02 | [i=3：正負の一次因子と任意の二次商を持つ一割当て枝](i3_quadratic_cofactor_single_allocation_closeout_2026-10-02.md) |
| 2026-09-21 | [i=3：二次捻りによる3乗因子の除去と、Kummer補助因子への還元](i3_quadratic_twist_and_kummer_support_2026-09-21.md) |
| 2026-09-23 | [i=3：四次の桁多項式の完全分類と2進排除](i3_quartic_digit_classification_2026-09-23.md) |
| 2026-09-30 | [i=3：五次の数値評価を排除し、桁和上界を五次まで延長する](i3_quintic_closeout_2026-09-30.md) |
| 2026-09-30 | [i=3：五次の桁多項式の分類と、二つの純冪方程式への還元](i3_quintic_digit_classification_2026-09-30.md) |
| 2026-10-02 | [i=3：任意の三次残余を一割当てする五次枝の全排除](i3_quintic_quadratic_complete_2026-10-02.md) |
| 2026-10-02 | [i=3：五次の二次商に残る端点割当ての絞り込み](i3_quintic_quadratic_endpoint_2026-10-02.md) |
| 2026-10-03 | [i=3：次数5・deg J=3 の完全分配を両定数桁で排除](i3_quintic_split_allocation_repair_2026-10-03.md) |
| 2026-10-01 | [i=3：残余群の任意次数下限と、二次群の境界を種数1で排除する](i3_residual_and_degree_two_group_2026-10-01.md) |
| 2026-10-01 | [i=3：全残余群の微分恒等式と、二群分岐の多項式ノルム降下](i3_residual_differential_and_norm_descent_2026-10-01.md) |
| 2026-10-01 | [i=3：七次の全係数分類と共通素数7による閉鎖](i3_septic_closeout_2026-10-01.md) |
| 2026-10-01 | [i=3：六次の全分岐の分類・整数評価の排除](i3_sextic_closeout_2026-10-01.md) |
| 2026-10-02 | [i=3：六次の幾何級数で、負の一次因子以外を共有する枝](i3_sextic_partial_sharing_closeout_2026-10-02.md) |
| 2026-09-30 | [六次の追加研究：作業メモ](i3_sextic_working_notes_2026-09-30.md) |
| 2026-10-03 | [i=3：完全分配の残余次数5を全排除し、次数7の境界を有限化](i3_split_mahler_frontier_2026-10-03.md) |
| 本文参照 | [i=3、n が2の冪の場合の平方の枝](i3_square_branch.md) |
| 2026-10-01 | [i=3：対称な飽和分配に対する任意次数の排除](i3_symmetric_saturation_2026-10-01.md) |
| 2026-09-21 | [i=3：Thue–Mahler完全解表による終端判別式3000以下の排除](i3_terminal_thue_mahler_2026-09-21.md) |
| 2026-10-01 | [i=3：二つの一次残余群を微分方程式と有理係数の漸化式へ還元する](i3_two_group_differential_recurrence_2026-10-01.md) |
| 2026-09-23 | [i=3：任意次数の桁和降下と、全奇素数の付値保存](i3_uniform_digit_descent_2026-09-23.md) |

</details>
