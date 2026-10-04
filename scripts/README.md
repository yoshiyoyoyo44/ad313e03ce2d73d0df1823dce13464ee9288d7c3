# 検算器・生成器の案内

[入口](../README.md) · [検算手順](../docs/VERIFICATION.md) · [データ](../data/README.md) · [証明ノート](../research/README.md)

10月4日の後続追加：i=21の全域証明に対応する[有限入力再生](audit_bft_i21_finite_dependency_2026_10_04.py)と
[位置重みの結合検算](audit_bft_i21_moment_closeout_2026_10_04.py)。40件の実行器より後の追加です。

## 最初に使うコマンド

リポジトリのルートから、assertを有効にして実行します。

```console
python -m pip install -r requirements-verification.txt
python -X utf8 scripts/check_repository.py
python -X utf8 scripts/verify_latest.py
python -X utf8 scripts/verify_october04.py
```

| スクリプト | 役割 |
|---|---|
| [check_repository.py](check_repository.py) | リンク・索引・構文・保存原本の確認。`--smoke` は一時コピーで代表8本を実行 |
| [verify_latest.py](verify_latest.py) | 研究更新に対応する39件を順に再生 |
| [verify_october04.py](verify_october04.py) | 10月4日の新しい全域証明と、その有限入力・G下界・独立監査を依存順に再生 |
| [replay_all_progress_import.py](replay_all_progress_import.py) | 10月3日の受領ZIPを照合。更新後は `--source-only` |
| [repo_paths.py](repo_paths.py) | 作業ディレクトリに依存しない入出力・旧名の解決 |

## 目的と命名

| 種類 | 使うときの注意 |
|---|---|
| `audit_*` / `replay_*` | 保存証明書、係数、閾値、応答などを照合。保証する範囲は本文を確認 |
| `build_*` / `certify_*` | 証明書の生成。独立再生器による確認と区別 |
| `search_*` / `scan_*` / 作業モデル | 探索・診断。有限例を一般証明へ外挿しない |
| `package_*` | 配布物の作成。出力場所と対象コミットを確認 |

検算器の多くは `data/results/` の対応するJSONを再出力します。
生成器にはNumPyなど追加依存が必要なものがあります。全スクリプトを一律に実行する必要はありません。

## 分野別に選ぶ

- [全体の被覆・全添字の方法](../research/general/README.md)
- [i=5：支持・積・分配・桁降下](../research/i5/README.md)
- [i=3：数値・分配・完全分配](../research/i3/README.md)
- [i=4：合同類・セル・有限j](../research/i4/README.md)

各分野の案内に証明・再生器・保存結果の対応表があります。

## 全コード索引

ファイル冒頭の説明を併記しています。詳しい引数と保存先は各スクリプトを確認してください。

<details open>
<summary>10月4日の追加（44件）</summary>

全域の添字拡張、BFTの新しいG下界、条件付きi=3・i=5の枝の排除を含みます。探索器の出力は証明書と区別してください。

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_bft_G_3_2_analytic_tail_2026_10_04.py](audit_bft_G_3_2_analytic_tail_2026_10_04.py) | Exact analytic tail of a strengthened BFT G(3,2,n) lower bound. |
| [audit_bft_gcd_10_7_and_two_anchors_2026_10_04.py](audit_bft_gcd_10_7_and_two_anchors_2026_10_04.py) | New universal G(10,7,n) bound and explicit (2,13)/(11,13) edges. |
| [audit_bft_gcd_19_14_finite_blocks_2026_10_04.py](audit_bft_gcd_19_14_finite_blocks_2026_10_04.py) | Exact finite prime-interval certificate for G(19,14,n), L1=1.444. |
| [audit_bft_gcd_19_14_independent_2026_10_04.py](audit_bft_gcd_19_14_independent_2026_10_04.py) | Independent exact analytic audit of the new G(19,14) certificate. |
| [audit_bft_gcd_19_14_universal_2026_10_04.py](audit_bft_gcd_19_14_universal_2026_10_04.py) | Exact universal new G(19,14,n) bound and the 3,11 BFT anchor. |
| [audit_bft_gcd_3_2_finite_blocks_2026_10_04.py](audit_bft_gcd_3_2_finite_blocks_2026_10_04.py) | Exact finite theta-block part of a strengthened BFT G(3,2,n) bound. |
| [audit_bft_gcd_4_3_anchor_7_13_2026_10_04.py](audit_bft_gcd_4_3_anchor_7_13_2026_10_04.py) | Exact BFT 2.4 application of the separately proved new G(4,3) bound. |
| [audit_bft_gcd_4_3_finite_blocks_2026_10_04.py](audit_bft_gcd_4_3_finite_blocks_2026_10_04.py) | Exact theta-block proof for G(4,3,3m-delta) >= 1.444^(3m). |
| [audit_bft_gcd_4_3_universal_2026_10_04.py](audit_bft_gcd_4_3_universal_2026_10_04.py) | Exact analytic completion of the new G(4,3,n) lower bound. |
| [audit_bft_i16_closeout_2026_10_04.py](audit_bft_i16_closeout_2026_10_04.py) | Exact all-n closure of i16: six updated edges and complete range join. |
| [audit_bft_i16_finite_dependency_2026_10_04.py](audit_bft_i16_finite_dependency_2026_10_04.py) | Targeted exhaustive replay of the finite input for i16 all-n index. |
| [audit_bft_i19_finite_dependency_2026_10_04.py](audit_bft_i19_finite_dependency_2026_10_04.py) | Targeted exhaustive replay of the finite input for i19 all-n index. |
| [audit_bft_i19_i24_graph_2026_10_04.py](audit_bft_i19_i24_graph_2026_10_04.py) | Exact graph lemmas and capacity comparisons for potential i19/i24 closure. |
| [audit_bft_i22_i25_finite_dependency_2026_10_04.py](audit_bft_i22_i25_finite_dependency_2026_10_04.py) | Targeted exhaustive replay of the finite input for i22 and i25 all-n indices. |
| [audit_bft_i24_closeout_2026_10_04.py](audit_bft_i24_closeout_2026_10_04.py) | Exact all-n closure of i24: six BFT anchors, graph and three ranges. |
| [audit_bft_i24_finite_dependency_2026_10_04.py](audit_bft_i24_finite_dependency_2026_10_04.py) | Targeted exhaustive replay of the finite input for i24 all-n index. |
| [audit_bft_matching_closeout_2026_10_04.py](audit_bft_matching_closeout_2026_10_04.py) | Exact replay of the BFT disjoint-matching closeout for i=27,30,33. |
| [audit_bft_newvertex_i22_i25_2026_10_04.py](audit_bft_newvertex_i22_i25_2026_10_04.py) | Exact rational intervals for three BFT 2.4 applications and i22/i25. |
| [audit_bft_newvertex_i22_i25_independent_2026_10_04.py](audit_bft_newvertex_i22_i25_independent_2026_10_04.py) | Independent source/parameter and integral audit of the three BFT anchors. |
| [audit_bft_pair_graph_closeout_independent_2026_10_04.py](audit_bft_pair_graph_closeout_independent_2026_10_04.py) | Independent exact audit of six all-n extensions via BFT's pair graph. |
| [audit_bft_proposition61_intermediate_bridge_2026_10_04.py](audit_bft_proposition61_intermediate_bridge_2026_10_04.py) | Exact audit of the finite BFT Proposition 6.1 bridge. |
| [audit_bft_six_finite_dependency_2026_10_04.py](audit_bft_six_finite_dependency_2026_10_04.py) | Targeted exhaustive replay of the finite input for six new all-n indices. |
| [audit_bft_strengthened_gcd_i19_2026_10_04.py](audit_bft_strengthened_gcd_i19_2026_10_04.py) | Exact closure of i19 with a newly certified G(3,2,n) bound. |
| [audit_i3_largest_base_endpoint_balance_2026_10_04.py](audit_i3_largest_base_endpoint_balance_2026_10_04.py) | Exact algebra and rational constants for the largest-base endpoint lemma. |
| [audit_i3_largest_base_general_shared_degree_2026_10_04.py](audit_i3_largest_base_general_shared_degree_2026_10_04.py) | Exact identities for the largest-base three-gcd degree bound. |
| [audit_i3_linear_J2_quotient_degree_ge2_all_degrees.py](audit_i3_linear_J2_quotient_degree_ge2_all_degrees.py) | Finite boundary certificate for the arbitrary-degree linear J-2 quotient theorem. |
| [audit_i3_linear_J2_quotient_degree1_bge2_all_degrees.py](audit_i3_linear_J2_quotient_degree1_bge2_all_degrees.py) | Exhaustive exact finite certificate for the E=1+bX, b>=2 branch. |
| [audit_i3_linear_J2_quotient_degree1_independent.py](audit_i3_linear_J2_quotient_degree1_independent.py) | Independent lambda-first replay of the degree-one linear-quotient certificate. |
| [audit_i3_nrow_dyadic_strip_2026_10_04.py](audit_i3_nrow_dyadic_strip_2026_10_04.py) | Exact certificates for n-row dyadic strips and a resultant-zero exclusion. |
| [audit_i3_quadratic_group_linear_residual_all_degrees.py](audit_i3_quadratic_group_linear_residual_all_degrees.py) | Derived finite certificate for an arbitrary-degree conditional i=3 family. |
| [audit_i3_quadratic_J2_Elinear_high_degree_2026_10_04.py](audit_i3_quadratic_J2_Elinear_high_degree_2026_10_04.py) | Exact finite end of the E-linear / quadratic J-2 quotient bound. |
| [audit_i3_quadratic_J2_Elinear_high_degree_independent.py](audit_i3_quadratic_J2_Elinear_high_degree_independent.py) | Independent backward-digit replay and rational bounds for the high-degree theorem. |
| [audit_i3_three_linear_above_2026_10_04.py](audit_i3_three_linear_above_2026_10_04.py) | Exact small algebraic certificates for the two b-minimal split orders. |
| [audit_i3_three_linear_b_c_t_2026_10_04.py](audit_i3_three_linear_b_c_t_2026_10_04.py) | Exact universal coefficient certificate for conditional i=3, b>c>t. |
| [audit_i3_three_linear_congruence_2026_10_04.py](audit_i3_three_linear_congruence_2026_10_04.py) | Exact certificate for the short three-linear congruence argument. |
| [audit_i3_three_linear_order_2026_10_04.py](audit_i3_three_linear_order_2026_10_04.py) | Exact all-parameter certificate for one conditional i=3 split ordering. |
| [audit_i32_bft_finite_extension_2026_10_04.py](audit_i32_bft_finite_extension_2026_10_04.py) | Generate and independently replay the i=32 finite extension to 10^116. |
| [audit_i32_bft_prefix_dependency_2026_10_04.py](audit_i32_bft_prefix_dependency_2026_10_04.py) | Replay the existing i32 prefix against the new finite-extension endpoint. |
| [audit_i5_pell_primitive_unit_reduction.py](audit_i5_pell_primitive_unit_reduction.py) | Exact symbolic/threshold audit of the i=5 Pell primitive-unit reduction. |
| [audit_largest_base_adjacent_shared_degree_2026_10_04.py](audit_largest_base_adjacent_shared_degree_2026_10_04.py) | Exact identities and thresholds for the general largest-base gcd bound. |
| [audit_nonmaximum_row_zero_rational_closeout_2026_10_04.py](audit_nonmaximum_row_zero_rational_closeout_2026_10_04.py) | Exact row-zero bounds and finite i=4 common-prime witnesses. |
| [search_bft_anchor_i19_2026_10_04.py](search_bft_anchor_i19_2026_10_04.py) | Finite floating-point anchor search; candidates are not proof certificates. |
| [search_bft_binding_new_L1_2026_10_04.py](search_bft_binding_new_L1_2026_10_04.py) | Finite diagnostic of rational s and the asymptotic BFT L(s). |
| [verify_october04.py](verify_october04.py) | Replay the October 4 proof dependencies in order and save the publication check. |

</details>

<details>
<summary>案内・入出力・配布（4件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [check_repository.py](check_repository.py) | Check navigation, artifact preservation, and optional isolated smoke runs. |
| [package_results.py](package_results.py) | Package the current tracked tree, preserving its directory structure. |
| [repo_paths.py](repo_paths.py) | Resolve archived basenames without changing certificate or transcript bytes. |
| [verify_latest.py](verify_latest.py) | Replay the October 3 independent research and prior checks. |

</details>

<details>
<summary>全体の被覆・一般の方法・原本照合（47件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_adjacent_digit_descent.py](audit_adjacent_digit_descent.py) | Exact replay for the all-index adjacent-row digit-descent note. |
| [audit_global_independent_2026_10_03.py](audit_global_independent_2026_10_03.py) | Independent exact diagnostics for the October 3 global audit. |
| [audit_two_position_digit_bound.py](audit_two_position_digit_bound.py) | Exact diagnostics for the all-index bounded-weight two-position lemma. |
| [audit_algebra.py](audit_algebra.py) | Independent symbolic audit of the supplied progress note. |
| [audit_discriminant.py](audit_discriminant.py) | Exact checks for the discriminant continuation; no Lean invocation. |
| [audit_github_baseline.py](audit_github_baseline.py) | Audit the fetched GitHub baseline against its local Git object and tracked tree. |
| [audit_handoff_algebra.py](audit_handoff_algebra.py) | Symbolic checks for the structural identities introduced by the handoff. |
| [audit_handoff_integration_2026_09_26.py](audit_handoff_integration_2026_09_26.py) | Reproduce the checks added when integrating the two September 26 handoffs. |
| [audit_iterated_polynomial_capacity.py](audit_iterated_polynomial_capacity.py) | Integer replay of an i27 exponent witness surviving new capacities. |
| [audit_maximal_row_moment.py](audit_maximal_row_moment.py) | Exact audit of the maximal-row moment bound and its exponent relaxation. |
| [audit_october03_integration.py](audit_october03_integration.py) | Preserve October 3 sources and reconstruct selected supplied certificates. |
| [audit_polynomial_capacity_supports.py](audit_polynomial_capacity_supports.py) | Integer-only replay of high-degree geometric capacity certificates. |
| [audit_quadratic_relaxation_i27.py](audit_quadratic_relaxation_i27.py) | Replay an exact exponent-relaxation witness with no optimization package. |
| [audit_weighted_common_divisor.py](audit_weighted_common_divisor.py) | Audit the quantitative common-divisor consequence and optimal ramp weights. |
| [certify_critical_indices.py](certify_critical_indices.py) | Finite Kummer certificate below the new near-collision tail bounds. |
| [certify_fixed_block_modular.py](certify_fixed_block_modular.py) | Generate finite periodic obstructions for fixed B and all exponents u. |
| [certify_interval_indices.py](certify_interval_indices.py) | Build the adaptive valuation certificate for i=97,101 and 121..204. |
| [certify_large_indices.py](certify_large_indices.py) | Rational-interval certificates for all large indices. |
| [certify_near_collisions.py](certify_near_collisions.py) | Certify bounded-coefficient near collisions via elementary approximation bounds. |
| [certify_near_collisions_a100.py](certify_near_collisions_a100.py) | Extend the close-power certificate to coefficients <=100, compactly. |
| [certify_prime_gaps.py](certify_prime_gaps.py) | Deterministic Eratosthenes sieve, gap covering, and residue certificates. |
| [certify_weighted_cover_extension.py](certify_weighted_cover_extension.py) | Extend the supplied weighted-cover proof to i=29 and 35<=i<=119. |
| [explore_descent.py](explore_descent.py) | Search for obstructions to possible universal descent lemmas. |
| [explore_gap_layers.py](explore_gap_layers.py) | Exploratory modular and factorization screen of the new fixed-gap equations. |
| [explore_interval_valuations.py](explore_interval_valuations.py) | Exploration only: adaptive exact interval bounds, not a saved certificate. |
| [explore_invariants.py](explore_invariants.py) | Exact algebraic exploration of invariants of the four cubic orbit values. |
| [explore_large_indices.py](explore_large_indices.py) | Exploratory floating-point screening only, not a certificate. |
| [explore_square_parameters.py](explore_square_parameters.py) | Test whether the square exclusion could hold without n's special shape. |
| [make_center_curve_magma.py](make_center_curve_magma.py) | Generate direct center/endpoint curves for fixed w/lambda, without T/u branches. |
| [make_certificate.py](make_certificate.py) | Produce elementary Lucas primality certificates for the saved sieve. |
| [make_gap_curve_magma.py](make_gap_curve_magma.py) | Complete integral points for the fixed-gap handoff's five small curves. |
| [make_small_block_magma.py](make_small_block_magma.py) | Generate elliptic-curve audits for a fixed A, B, or C block. |
| [near_collision_arithmetic.py](near_collision_arithmetic.py) | Integer interval arithmetic used to construct the near-collision certificate. |
| [replay_all_progress_import.py](replay_all_progress_import.py) | Verify the received October 3 package, backups, and optional import snapshot. |
| [replay_certificate.py](replay_certificate.py) | Replay the finite i=3 proof certificates using only Python's standard library. |
| [replay_critical_indices.py](replay_critical_indices.py) | Independent standard-library replay of the critical-index finite remainder. |
| [replay_interval_indices.py](replay_interval_indices.py) | Independent standard-library replay of interval_index_certificate.json. |
| [replay_large_indices.py](replay_large_indices.py) | Replay the large-index certificate using only Python's standard library. |
| [replay_near_collisions.py](replay_near_collisions.py) | Independent exact replay of the bounded-coefficient near-collision theorem. |
| [replay_near_collisions_a100.py](replay_near_collisions_a100.py) | Independent rational replay for coefficient bound 100 and the i=119 bootstrap. |
| [replay_september26_attachments.py](replay_september26_attachments.py) | Replay all six supplied audits in disposable copies and check source hashes. |
| [replay_september27_attachments.py](replay_september27_attachments.py) | Replay the September 27 package in an isolated copy, preserving originals. |
| [replay_weighted_cover_extension.py](replay_weighted_cover_extension.py) | Independently replay every interval, tail and small-n exception of the extension. |
| [run_magma_audit.py](run_magma_audit.py) | Submit a specified mathematical input to the public Magma calculator. |
| [run_magma_batches.py](run_magma_batches.py) | Run a generated fixed-block input in small, resumable public-calculator batches. |
| [sieve_i3.py](sieve_i3.py) | Exact necessary-condition sieve for Erdős 699 at i=3. |
| [weighted_cover_sources.py](weighted_cover_sources.py) | Locate the byte-preserved September 26 proof package without changing it. |

</details>

<details>
<summary>i=5（5件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_i5_global_product_and_affine.py](audit_i5_global_product_and_affine.py) | Exact certificates for the i=5 product, affine strips, and valuation frontier. |
| [audit_i5_multiplicity_frontier.py](audit_i5_multiplicity_frontier.py) | Exact i=5 tail closeouts, cofactor bounds, and an all-degree capacity barrier. |
| [audit_i5_sparse_allocation.py](audit_i5_sparse_allocation.py) | Replay exact i=5 certificates for sparse allocations and a method barrier. |
| [audit_i5_weight4_two_positions.py](audit_i5_weight4_two_positions.py) | Exact audit of weights 4, 6, 8, two-position exclusions and all-digit mod-24 conditions. |
| [build_i5_sparse_allocation_certificate.py](build_i5_sparse_allocation_certificate.py) | Build or resume the 880 i=5 allocation certificates. |

</details>

<details>
<summary>i=4（7件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_i4_five_cell_closeout.py](audit_i4_five_cell_closeout.py) | Exact finite audits for the five-cell theorem (see the accompanying proof). |
| [audit_i4_prime_neighbor_squares.py](audit_i4_prime_neighbor_squares.py) | Exact finite remainder for i=4, n=(p+1)^2 with p prime. |
| [audit_i4_quadratic_weight.py](audit_i4_quadratic_weight.py) | Audit the all-n quadratic weighted-product inequality, using exact integers. |
| [audit_i4_residue_closeout.py](audit_i4_residue_closeout.py) | Exact audits for the all-n i=4 residue classification and class 12. |
| [audit_i4_six_cell_capacity.py](audit_i4_six_cell_capacity.py) | Exact replay of all six-cell certificates and the seven-cell obstruction. |
| [audit_known_bridge_and_i4_fixed_j.py](audit_known_bridge_and_i4_fixed_j.py) | Exact EEES exception audit and the all-n i=4, 5<=j<=1000 region. |
| [replay_i4_fixed_j.py](replay_i4_fixed_j.py) | Separate replay of the finite-j certificate using different arithmetic. |

</details>

<details>
<summary>i=3（72件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_i3_2adic_square.py](audit_i3_2adic_square.py) | Exact audit of the 2-adic inequalities and the 3*2^u square branch. |
| [audit_i3_adjacent_resultants.py](audit_i3_adjacent_resultants.py) | Exact checks for adjacent-resultant bounds and the geometric-family proof. |
| [audit_i3_all_square.py](audit_i3_all_square.py) | Independent finite audit of the all-M square exclusion; no Lean calls. |
| [audit_i3_arbitrary_cofactor.py](audit_i3_arbitrary_cofactor.py) | Replay exact certificates for the arbitrary-cofactor numerical exclusion. |
| [audit_i3_balanced_boundary.py](audit_i3_balanced_boundary.py) | Replay the finite certificates and exact identities of the balanced boundary. |
| [audit_i3_center_curve.py](audit_i3_center_curve.py) | Replay exact arithmetic for the direct center curve and saved Magma runs. |
| [audit_i3_central_square_descent.py](audit_i3_central_square_descent.py) | Exact audit of two square remainders and the strict central 11/15 bound. |
| [audit_i3_chat_integration.py](audit_i3_chat_integration.py) | Exact algebra and finite diagnostics for the four-chat integration. |
| [audit_i3_chatgpt_uniform_integration.py](audit_i3_chatgpt_uniform_integration.py) | Short exact checks for the September 20 ChatGPT integration. |
| [audit_i3_chebyshev_boundary.py](audit_i3_chebyshev_boundary.py) | Exact identities and valuation diagnostics for the all-degree boundary. |
| [audit_i3_complement_digit_bounds.py](audit_i3_complement_digit_bounds.py) | Exact local audits for the September 20 complement-digit bounds. |
| [audit_i3_cross_modulus_and_digit_height.py](audit_i3_cross_modulus_and_digit_height.py) | Audit universal cross-modulus bounds and polynomial rigidity for i=3. |
| [audit_i3_cubic_cofactor.py](audit_i3_cubic_cofactor.py) | Replay the cubic-cofactor partial-sharing theorem. |
| [audit_i3_cubic_digit_classification.py](audit_i3_cubic_digit_classification.py) | Exact audits of the complete cubic digit-polynomial classification. |
| [audit_i3_cubic_discriminant_and_cf_tail.py](audit_i3_cubic_discriminant_and_cf_tail.py) | Targeted exact checks; does not enumerate counterexamples or cubic fields. |
| [audit_i3_descent.py](audit_i3_descent.py) | Check the descent identities and constructive local-solubility examples. |
| [audit_i3_descent_kummer_obstruction.py](audit_i3_descent_kummer_obstruction.py) | Exact checks for the descent update and its local Kummer obstruction. |
| [audit_i3_digit_height_budget.py](audit_i3_digit_height_budget.py) | Audit the all-prime digit-height budget and polynomial factor degrees. |
| [audit_i3_digit_reciprocity.py](audit_i3_digit_reciprocity.py) | Exact checks accompanying the general proofs of 2026-09-14. |
| [audit_i3_discriminant_support.py](audit_i3_discriminant_support.py) | Elliptic j-invariant gap and unbounded-exponent support exclusions. |
| [audit_i3_dyadic_denominators_and_continued_fractions.py](audit_i3_dyadic_denominators_and_continued_fractions.py) | Exact arithmetic for the dyadic denominator and continued-fraction bounds. |
| [audit_i3_even_multiplier.py](audit_i3_even_multiplier.py) | Audit odd-prime gluing and partial sharing for odd half-degrees >=5. |
| [audit_i3_extremal_split_closeout.py](audit_i3_extremal_split_closeout.py) | Check the all-degree extremal split proof and its cubic numerical obstruction. |
| [audit_i3_finite_prime_obstruction.py](audit_i3_finite_prime_obstruction.py) | Short modular checks for i3_finite_prime_obstruction_2026-09-20.md. |
| [audit_i3_five_power_composition.py](audit_i3_five_power_composition.py) | Exact diagnostics for the all-exponent five-power frontier. |
| [audit_i3_five_power_low_degree_closeout.py](audit_i3_five_power_low_degree_closeout.py) | Exact certificates excluding the Chebyshev cores D=25 and D=125. |
| [audit_i3_fixed_blocks.py](audit_i3_fixed_blocks.py) | Check the fixed-block reduction and the arithmetic of saved Magma outputs. |
| [audit_i3_gap_square_obstructions.py](audit_i3_gap_square_obstructions.py) | Exact certificates for uniform square obstructions in the gap equation. |
| [audit_i3_global_digit_constraints.py](audit_i3_global_digit_constraints.py) | Exact audits and finite certificates for the accompanying global digit note. |
| [audit_i3_growing_gap_frey.py](audit_i3_growing_gap_frey.py) | Audit the auxiliary Frey curve for growing G and its support exclusions. |
| [audit_i3_half_degree_composition.py](audit_i3_half_degree_composition.py) | Exact diagnostics for the arbitrary-degree half-degree boundary theorem. |
| [audit_i3_half_ratio_central_bounds.py](audit_i3_half_ratio_central_bounds.py) | Exact identities for the all-degree half-ratio and central-group bounds. |
| [audit_i3_integrated_digits.py](audit_i3_integrated_digits.py) | Audit the 2026-09-13 integration and new center-cofactor identities. |
| [audit_i3_irreducible_cubic_and_rational_gaps.py](audit_i3_irreducible_cubic_and_rational_gaps.py) | Exact checks for the irreducible orbit cubic and rational-gap bounds. |
| [audit_i3_low_digit_continuation.py](audit_i3_low_digit_continuation.py) | Exact finite audits for i3_low_digit_continuation_2026-09-19.md. |
| [audit_i3_mixed_parameter_bound.py](audit_i3_mixed_parameter_bound.py) | Exact checks and finite fibers for the mixed parameter D = w - 4*lambda. |
| [audit_i3_multiplicity_and_fresh_support.py](audit_i3_multiplicity_and_fresh_support.py) | Audit the all-even-j multiplicity budget and fresh-support product. |
| [audit_i3_new_chat_and_effective_gap.py](audit_i3_new_chat_and_effective_gap.py) | Audit the new chat results and the effective bound in G=u-4*v. |
| [audit_i3_nonsquare_lifts.py](audit_i3_nonsquare_lifts.py) | Exact audits of the merged nonsquare lemmas, not an unbounded proof. |
| [audit_i3_octic_last_branch.py](audit_i3_octic_last_branch.py) | Exact ideal-membership certificate and rational-root obstruction. |
| [audit_i3_octic_saturation_and_pell.py](audit_i3_octic_saturation_and_pell.py) | Exact checks for saturation and the degree-unbounded Pell obstruction. |
| [audit_i3_prime_power_resultants.py](audit_i3_prime_power_resultants.py) | Exact diagnostics for the degree-unbounded prime-power/resultant note. |
| [audit_i3_quadratic_cofactor.py](audit_i3_quadratic_cofactor.py) | Exact audit of the quadratic-cofactor exclusion, including its finite tail. |
| [audit_i3_quartic_digit_classification.py](audit_i3_quartic_digit_classification.py) | Exact audits of the unbounded quartic digit-polynomial classification. |
| [audit_i3_quintic_closeout.py](audit_i3_quintic_closeout.py) | Replay the complete exclusion of the classified quintic i=3 family. |
| [audit_i3_quintic_digit_classification.py](audit_i3_quintic_digit_classification.py) | Independent symbolic diagnostics for the coefficient-unbounded proof. |
| [audit_i3_quintic_quadratic_complete.py](audit_i3_quintic_quadratic_complete.py) | Audit the complete degree-five single-allocation exclusion. |
| [audit_i3_quintic_quadratic_endpoint.py](audit_i3_quintic_quadratic_endpoint.py) | Exact audit of the new degree-five endpoint bounds. |
| [audit_i3_quintic_split_allocation.py](audit_i3_quintic_split_allocation.py) | Exact certificates for the quintic, degree-three complete allocation. |
| [audit_i3_residual_and_degree_two_group.py](audit_i3_residual_and_degree_two_group.py) | Symbolic checks for degree-unbounded residual and genus-one arguments. |
| [audit_i3_residual_differential_and_norm_descent.py](audit_i3_residual_differential_and_norm_descent.py) | Exact checks for the all-degree residual differential and norm descent. |
| [audit_i3_septic_and_saturation.py](audit_i3_septic_and_saturation.py) | Exact certificates for the septic classification and arbitrary-degree lemma. |
| [audit_i3_sextic_closeout.py](audit_i3_sextic_closeout.py) | Exact checks for the paper proof closing all sextic digit-polynomial branches. |
| [audit_i3_sextic_partial_sharing.py](audit_i3_sextic_partial_sharing.py) | Exact symbolic and integer certificates for sextic partial sharing. |
| [audit_i3_sextic_working_models.py](audit_i3_sextic_working_models.py) | Check two explicit sextic working models, without certifying exhaustiveness. |
| [audit_i3_split_geometric.py](audit_i3_split_geometric.py) | Reconstructed audit of the saved integral-root-value/split-geometric proof. |
| [audit_i3_split_mahler_frontier.py](audit_i3_split_mahler_frontier.py) | Exact positive-polynomial certificates for the split Mahler frontier. |
| [audit_i3_rho6_degree7_independent.py](audit_i3_rho6_degree7_independent.py) | Exact finite audit of the standard-digit complete split rho=6,d=4,m=7. |
| [audit_i3_thue_mahler_table.py](audit_i3_thue_mahler_table.py) | Audit published Thue-Mahler data and its interface with our cubics. |
| [audit_i3_twist_and_kummer_support.py](audit_i3_twist_and_kummer_support.py) | Exact audits for quadratic twists and the Kummer cofactor bridge. |
| [audit_i3_two_group_recurrence.py](audit_i3_two_group_recurrence.py) | Exact polynomial recurrence for the smooth two-linear-residual branch. |
| [audit_i3_uniform_digit_descent.py](audit_i3_uniform_digit_descent.py) | Exact finite diagnostics for the conditional, all-degree digit descent. |
| [certify_i3_cubic_discriminant_minima.py](certify_i3_cubic_discriminant_minima.py) | Enumerate all Hessian-reduced irreducible binary cubics of discriminant <= 961. |
| [certify_i3_gap13.py](certify_i3_gap13.py) | Finite certificates for gap layers 10--13; elliptic completeness uses Magma. |
| [certify_i3_gap_layers.py](certify_i3_gap_layers.py) | Save complete residue/factorization coverage for gap layers 4 through 9. |
| [certify_i3_prime_neighbor_powers.py](certify_i3_prime_neighbor_powers.py) | Generate the bounded remainder for the prime-neighbor power theorem. |
| [extend_i3_certificate.py](extend_i3_certificate.py) | Extend the independently replayable i=3 exclusion to 43 <= u <= 48. |
| [extend_i3_cubic_minima_certificate.py](extend_i3_cubic_minima_certificate.py) | Extend the i=3 CRT exclusion to u=49,50 using 284*M^3 < 2^u. |
| [replay_i3_cubic_discriminant_minima.py](replay_i3_cubic_discriminant_minima.py) | Independent coefficient-box replay and exact algebra for cubic minima. |
| [replay_i3_gap13.py](replay_i3_gap13.py) | Independent replay, using only the Python standard library. |
| [replay_i3_gap_layers.py](replay_i3_gap_layers.py) | Independent standard-library replay of the gap-layer certificate. |
| [replay_i3_prime_neighbor_powers.py](replay_i3_prime_neighbor_powers.py) | Independently replay prime-neighbor power certificates (standard library). |

</details>

<details>
<summary>i=119（3件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_i119_hankel.py](audit_i119_hankel.py) | Exact finite checks for the independently proved Hankel/content identities. |
| [certify_i119_finite.py](certify_i119_finite.py) | Close the finite range left below the A=100 near-collision bootstrap. |
| [replay_i119_finite.py](replay_i119_finite.py) | Independent replay of the lower range needed for the i=119, n<=10^87 result. |

</details>
