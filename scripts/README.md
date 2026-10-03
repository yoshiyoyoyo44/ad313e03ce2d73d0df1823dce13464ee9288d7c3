# 検算器・生成器の案内

[入口](../README.md) · [検算手順](../docs/VERIFICATION.md) · [データ](../data/README.md) · [証明ノート](../research/README.md)

## 最初に使うコマンド

リポジトリのルートから、assertを有効にして実行します。

```console
python -m pip install -r requirements-verification.txt
python -X utf8 scripts/check_repository.py
python -X utf8 scripts/verify_latest.py
```

| スクリプト | 役割 |
|---|---|
| [check_repository.py](check_repository.py) | リンク・索引・構文・保存原本の確認。`--smoke` は一時コピーで代表8本を実行 |
| [verify_latest.py](verify_latest.py) | 研究更新に対応する35件を順に再生 |
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
生成器にはNumPyなど追加依存が必要なものがあります。全134ファイルを一律に実行する必要はありません。

## 分野別に選ぶ

- [全体の被覆・全添字の方法](../research/general/README.md)
- [i=5：支持・積・分配・桁降下](../research/i5/README.md)
- [i=3：数値・分配・完全分配](../research/i3/README.md)
- [i=4：合同類・セル・有限j](../research/i4/README.md)

各分野の案内に証明・再生器・保存結果の対応表があります。

## 全コード索引

ファイル冒頭の説明を併記しています。詳しい引数と保存先は各スクリプトを確認してください。

<details>
<summary>案内・入出力・配布（4件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [check_repository.py](check_repository.py) | Check navigation, artifact preservation, and optional isolated smoke runs. |
| [package_results.py](package_results.py) | Package the current tracked tree, preserving its directory structure. |
| [repo_paths.py](repo_paths.py) | Resolve archived basenames without changing certificate or transcript bytes. |
| [verify_latest.py](verify_latest.py) | Replay the i=5 priority update, October 3 integration, and prior checks. |

</details>

<details>
<summary>全体の被覆・一般の方法・原本照合（45件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_adjacent_digit_descent.py](audit_adjacent_digit_descent.py) | Exact replay for the all-index adjacent-row digit-descent note. |
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
<summary>i=5（4件）</summary>

| スクリプト | 冒頭の説明 |
|---|---|
| [audit_i5_global_product_and_affine.py](audit_i5_global_product_and_affine.py) | Exact certificates for the i=5 product, affine strips, and valuation frontier. |
| [audit_i5_multiplicity_frontier.py](audit_i5_multiplicity_frontier.py) | Exact i=5 tail closeouts, cofactor bounds, and an all-degree capacity barrier. |
| [audit_i5_sparse_allocation.py](audit_i5_sparse_allocation.py) | Replay exact i=5 certificates for sparse allocations and a method barrier. |
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
<summary>i=3（71件）</summary>

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
