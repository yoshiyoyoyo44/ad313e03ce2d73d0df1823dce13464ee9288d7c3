"""Exact row-zero bounds and finite i=4 common-prime witnesses.

The arbitrary-n reduction is proved in the note.  The small i=4 end is
generated using Kummer carries and independently replayed with Legendre
factorial valuations.  No finite calculation is extrapolated to all n.
"""

from hashlib import sha256
from itertools import product
from math import factorial, isqrt, lcm
from pathlib import Path
import json


def prime_trial(p):
    if p < 2:
        return False
    return all(p % divisor for divisor in range(2, isqrt(p)+1))


def smallest_prime_factors(limit):
    sieve = [0] * (limit+1)
    for p in range(2, limit+1):
        if not sieve[p]:
            for multiple in range(p, limit+1, p):
                if not sieve[multiple]:
                    sieve[multiple] = p
    return sieve


def factors(value, sieve):
    primes = set()
    while value > 1:
        p = sieve[value]
        primes.add(p)
        while value % p == 0:
            value //= p
    return primes


def first_carry(n, j, p):
    power, exponent = p, 1
    while power <= n:
        if j % power > n % power:
            return exponent
        power *= p
        exponent += 1
    return None


def factorial_valuation(n, p):
    value = 0
    while n:
        n //= p
        value += n
    return value


def generate(limit):
    sieve = smallest_prime_factors(limit)
    rows = []
    counts = {}
    for denominator in (2, 3, 6):
        counts[denominator] = 0
        for n in range(5*denominator, limit+1, denominator):
            j = n // denominator
            primes = set()
            for offset in range(4):
                primes.update(factors(n-offset, sieve))
            for p in sorted(prime for prime in primes if prime >= 5):
                carry = first_carry(n, j, p)
                if carry is not None:
                    rows.append([n, denominator, p, carry])
                    counts[denominator] += 1
                    break
            else:
                raise AssertionError((n, j, denominator, "no common-prime witness"))
    return rows, counts


def independently_replay(rows, limit):
    expected = {(n, denominator) for n in range(10, limit+1)
                for denominator in (2, 3, 6)
                if n % denominator == 0 and n // denominator >= 5}
    observed = set()
    for n, denominator, p, exponent in rows:
        pair = (n, denominator)
        assert pair not in observed
        observed.add(pair)
        j = n // denominator
        assert 5 <= j and 2*j <= n <= limit
        assert p >= 5 and prime_trial(p)
        coefficient_four = n*(n-1)*(n-2)*(n-3)//24
        assert coefficient_four % p == 0
        valuation = (factorial_valuation(n, p) - factorial_valuation(j, p)
                     - factorial_valuation(n-j, p))
        assert valuation >= 1
        assert exponent >= 1 and j % p**exponent > n % p**exponent
        assert all(j % p**e <= n % p**e for e in range(1, exponent))
    assert observed == expected
    return len(observed)


def divisor_prefix_refinement(index):
    primes = [p for p in range(2, index) if prime_trial(p)]
    L_i = lcm(*range(1, index+1))
    delta_max = L_i if prime_trial(index) else lcm(*range(1, index))
    delta_primes = primes + ([index] if prime_trial(index) else [])
    powers = []
    for p in delta_primes:
        value, exponent = delta_max, 0
        while value % p == 0:
            value //= p
            exponent += 1
        powers.append((p, exponent))
    divisors = []
    for exponents in product(*(range(exponent+1) for _, exponent in powers)):
        delta = 1
        for (p, _), exponent in zip(powers, exponents):
            delta *= p**exponent
        divisors.append(delta)
    # Independent arithmetic divisor enumeration, small for indices 17,18.
    direct_divisors = set()
    for candidate in range(1, isqrt(delta_max)+1):
        if delta_max % candidate == 0:
            direct_divisors.update((candidate, delta_max//candidate))
    assert set(divisors) == direct_divisors
    records = []
    last = 2*len(primes)-1
    for delta in sorted(divisors):
        if delta == 1:
            continue
        prime_powers = {}
        for p in primes:
            value, exponent = delta, 0
            while value % p == 0:
                value //= p
                exponent += 1
            prime_powers[p] = p**exponent if exponent else None
        modes = ([2] if delta % 2 == 0 else []) + ([3] if delta % 3 == 0 else []) + ([4] if delta >= 4 else [])
        cases = []
        for mode in modes:
            for prefix in range(1, last+1):
                eligible = sum(prime_powers[p] is None or prime_powers[p] <= prefix for p in primes)
                if mode in (2, 3):
                    eligible -= int(prime_powers[mode] <= prefix)
                    nonresonant_lower = (prefix+1)//2 if mode == 2 else prefix-prefix//3
                else:
                    nonresonant_lower = prefix-prefix//4
                if nonresonant_lower > eligible:
                    cases.append(dict(mode=mode, prefix=prefix,
                                      nonresonant_lower=nonresonant_lower,
                                      eligible_maximum_prime_upper=eligible))
                    break
            else:
                raise AssertionError((index, delta, mode, "no sufficient prefix"))
        prefix = max(case["prefix"] for case in cases)
        bound = prefix + L_i*delta**(prefix+1)*factorial(prefix)//4
        records.append(dict(delta=delta, cases=cases, prefix=prefix, maximum_n=bound))
    # Replay the eligibility by explicit allowed maximum-row sets.
    for record in records:
        delta = record["delta"]
        for case in record["cases"]:
            prefix, mode = case["prefix"], case["mode"]
            eligible_primes = []
            for p in primes:
                value, power = delta, 1
                while value % p == 0:
                    value //= p
                    power *= p
                if power == 1:
                    eligible_primes.append(p)  # Conservative unrestricted upper set.
                    continue
                allowed = [r for r in range(1, prefix+1) if r % power == 0]
                if mode in (2, 3):
                    allowed = [r for r in allowed if r % mode != 0]
                if allowed:
                    eligible_primes.append(p)
            lower = len([r for r in range(1, prefix+1) if r % mode != 0])
            assert lower == case["nonresonant_lower"]
            assert len(eligible_primes) == case["eligible_maximum_prime_upper"] < lower
        assert record["maximum_n"] < 10**87
    assert {record["delta"] for record in records} == direct_divisors-{1}
    worst = max(records, key=lambda record:record["maximum_n"])
    return dict(i=index, L_i=L_i, delta_max=delta_max,
                divisor_records=records, maximum_n=worst["maximum_n"],
                worst_delta=worst["delta"], worst_prefix=worst["prefix"],
                decimal_digits=len(str(worst["maximum_n"])))


def main():
    i4_limit = 3 + 12 * 6**4 * factorial(3)//4
    assert i4_limit == 23331
    rows, counts = generate(i4_limit)
    certificate = dict(
        index=4, maximum_n=i4_limit,
        ratios=["1/2", "1/3", "1/6"],
        record_schema=["n", "ratio_denominator", "common_prime", "first_carry_exponent"],
        records=rows,
    )
    encoded = (json.dumps(certificate, separators=(",", ":"))+"\n").encode("utf-8")
    root = Path(__file__).resolve().parents[1]
    certificate_path = root / "data/certificates/i4_nonmaximum_row_zero_rational_witnesses_2026-10-04.json"
    certificate_path.write_bytes(encoded)
    saved = json.loads(certificate_path.read_text(encoding="utf-8"))
    coverage = independently_replay(saved["records"], i4_limit)
    assert coverage == len(rows)
    bounds = []
    for index in range(5, 17):
        small_prime_count = sum(prime_trial(p) for p in range(2, index))
        last_row = 2*small_prime_count-1
        assert 1 <= last_row <= index-1
        L_i = lcm(*range(1, index+1))
        bound = last_row + L_i**(last_row+2)*factorial(last_row)//4
        assert bound < 10**87
        bounds.append(dict(i=index, prime_count=small_prime_count,
                           prefix_last_row=last_row, L_i=L_i,
                           maximum_n=bound, decimal_digits=len(str(bound)),
                           connection="Existing theorem for i>=5,n<=10^87"))
    refinements = [divisor_prefix_refinement(index) for index in (17, 18)]
    refinement_certificate = root / "data/certificates/nonmaximum_row_zero_delta_prefix_refinement_2026-10-04.json"
    refinement_encoded = (json.dumps(refinements, separators=(",", ":"))+"\n").encode("utf-8")
    refinement_certificate.write_bytes(refinement_encoded)
    result = dict(
        status="passed",
        independent_review="Parent independently audited the prefix and factorial-product proof; finite certificate uses independent Legendre replay",
        scope="Counterexample branches with row 0 not selected as a maximum row for any small prime. These branches are excluded for i=4,...,18. No newly solved full index.",
        general_bound="n <= R + lcm(1,...,i)^(R+2)*R!/4, R=2*pi(i-1)-1, all i>=4",
        i4_bound=i4_limit,
        i4_candidate_pairs=coverage,
        i4_pairs_by_ratio_denominator=counts,
        i4_certificate_sha256=sha256(encoded).hexdigest(),
        i4_generator="Smallest-prime-factor sieve and first Kummer carry",
        i4_independent_replay="Primality by trial division, binom(n,4) exact integer, binom(n,j) Legendre factorial valuation, exact coverage set",
        i5_through_i16_bounds=bounds,
        i17_i18_refined_bounds=[{key:value for key,value in refinement.items() if key != "divisor_records"}
                               for refinement in refinements],
        divisor_refinement_certificate_sha256=sha256(refinement_encoded).hexdigest(),
        no_new_full_index_solved=True,
    )
    result_path = root / "data/results/verification_nonmaximum_row_zero_rational_closeout_2026-10-04.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key:value for key,value in result.items()
                      if key != "i5_through_i16_bounds"}, ensure_ascii=False, indent=2))
    print("Bounds linked to existing finite theorem:", len(bounds))


if __name__ == "__main__":
    main()
