#!/usr/bin/env python3
"""Post-exposure, source-only goose individual calendar-offset consistency audit.

No breeding, feeding, energy or other fitness variables are parsed or fitted.
Permutation shuffles the five-stage calendar-time vector between bird IDs
within each year, preserving all within-year and cross-stage covariance.
Outputs exploratory individual-equal statistics, descriptive pair correlations,
identity-permutation p and the max-over-5-stages postselection contrast.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_COMMIT = "2171bcd36bf37022c8716e15c0f75412103b0f3f"
SOURCE_URL = (
    "https://raw.githubusercontent.com/aschindler23/"
    "Schindler_etal_2024_ProcB/" + SOURCE_COMMIT + "/spring_data.csv"
)
DRYAD_SHA256 = "9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd"
STAGES = (2, 3, 4, 5, 6)
N_PERM = 10000
N_BOOT = 10000
SEED = 20261008


def read_dates(raw: bytes) -> list[dict]:
    digest = hashlib.sha256(
        raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    ).hexdigest()
    if digest != DRYAD_SHA256:
        raise ValueError("pinned author source mismatch versus Dryad manifest")

    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    fields = {"id", "year", "sub_season", "first_day"}
    if not fields.issubset(reader.fieldnames or []):
        raise ValueError("required timestamp columns absent")
    grouped = defaultdict(dict)
    count = 0
    for row in reader:
        count += 1
        key = (int(row["id"]), int(row["year"]))
        stage = int(row["sub_season"])
        date = float(row["first_day"])
        if stage in grouped[key] or not 1 <= stage <= 6 or not 1 <= date <= 366:
            raise ValueError("duplicate or malformed stage boundary")
        grouped[key][stage] = date
    if count != 642 or len(grouped) != 107:
        raise ValueError("source rows/bird-years changed")
    dates = []
    for (bird, year), stages in sorted(grouped.items()):
        if not 1 <= year <= 5 or set(stages) != set(range(1, 7)):
            raise ValueError("missing or out-of-range year/stage")
        if any(stages[i+1] <= stages[i] for i in range(1, 6)):
            raise ValueError("stage chronology must be strictly increasing")
        dates.append({
            "bird": bird,
            "year": year,
            "times": [stages[s] for s in STAGES]
        })
    if len({r["bird"] for r in dates}) != 49:
        raise ValueError("source identity count changed")
    return dates


def standardized_stage_residuals(records: list[dict]) -> tuple[list[list[float]], dict]:
    byyear = defaultdict(list)
    for i, row in enumerate(records):
        byyear[row["year"]].append(i)
    values = [[0.0] * len(STAGES) for _ in records]
    scales = {}
    for year, indexes in sorted(byyear.items()):
        year_scale = {}
        for j, stage in enumerate(STAGES):
            x = [records[i]["times"][j] for i in indexes]
            mu = statistics.mean(x)
            sd = statistics.stdev(x)
            if sd <= 1e-12:
                raise ValueError(f"year {year}, stage {stage}: no usable timing spread")
            for i in indexes:
                values[i][j] = (records[i]["times"][j] - mu) / sd
            year_scale[str(stage)] = {
                "n": len(x),
                "mean": mu,
                "sd": sd,
            }
        scales[str(year)] = year_scale
    return values, scales


def bird_pair_index(records):
    grouped = defaultdict(list)
    byyear = defaultdict(list)
    for i, row in enumerate(records):
        grouped[row["bird"]].append(i)
        byyear[row["year"]].append(i)
    repeated = [list(combinations(ix, 2)) for ix in grouped.values() if len(ix) >= 2]
    if len(repeated) != 30 or sum(map(len, repeated)) != 97:
        raise ValueError("repeat-bird support changed")
    return repeated, dict(byyear), grouped


def per_bird_products(values, repeated, index_map=None):
    if index_map is None:
        index_map = list(range(len(values)))
    result = []
    for pairs in repeated:
        z = []
        for j in range(len(STAGES)):
            z.append(sum(
                values[index_map[i]][j] * values[index_map[k]][j]
                for i, k in pairs
            ) / len(pairs))
        result.append(z)
    return result


def stats(values, repeated, index_map=None):
    individual = per_bird_products(values, repeated, index_map)
    return [
        statistics.mean(row[j] for row in individual)
        for j in range(len(STAGES))
    ]


def pair_pearson(records, repeated, stage_index):
    byyear = defaultdict(list)
    for i, row in enumerate(records):
        byyear[row["year"]].append(i)
    means = {
        year: statistics.mean(records[i]["times"][stage_index] for i in ix)
        for year, ix in byyear.items()
    }
    points = []
    for pairs in repeated:
        for i, k in pairs:
            a = records[i]["times"][stage_index] - means[records[i]["year"]]
            b = records[k]["times"][stage_index] - means[records[k]["year"]]
            points.append((a, b))
    aa = [x for x, _ in points]
    bb = [x for _, x in points]
    ma, mb = statistics.mean(aa), statistics.mean(bb)
    cov = sum((x-ma)*(y-mb) for x, y in points)
    va = sum((x-ma)**2 for x in aa)
    vb = sum((x-mb)**2 for x in bb)
    if va <= 0 or vb <= 0:
        raise ValueError("cannot calculate pair correlation")
    return cov / math.sqrt(va*vb)


def percentile(arr, level):
    x = sorted(arr)
    pos = (len(x)-1)*level
    lo = int(pos)
    hi = min(lo+1, len(x)-1)
    return x[lo] * (1-(pos-lo)) + x[hi] * (pos-lo)


def permutation_test(records, permutations=N_PERM, boots=N_BOOT):
    values, year_scales = standardized_stage_residuals(records)
    repeated, byyear, bybird = bird_pair_index(records)
    base = stats(values, repeated)
    pears = [pair_pearson(records, repeated, j) for j in range(len(STAGES))]
    rng = random.Random(SEED)
    perm_scores = []
    for _ in range(permutations):
        index_map = list(range(len(values)))
        for ix in byyear.values():
            shuffle = ix[:]
            rng.shuffle(shuffle)
            for original, reassigned in zip(ix, shuffle):
                index_map[original] = reassigned
        perm_scores.append(stats(values, repeated, index_map))

    b_individual = per_bird_products(values, repeated)
    bootstrap_stage5 = []
    for _ in range(boots):
        sampled = [rng.choice(b_individual) for i in b_individual]
        bootstrap_stage5.append(statistics.mean(t[3] for t in sampled))

    n = len(perm_scores)
    pstage = {
        str(st): (
            1 + sum(z[j] >= base[j] for z in perm_scores)
        ) / (n+1)
        for j, st in enumerate(STAGES)
    }
    pmax5 = (
        1 + sum(max(z) >= base[3] for z in perm_scores)
    ) / (n+1)
    p5_minus3 = (
        1 + sum(z[3]-z[1] >= base[3]-base[1] for z in perm_scores)
    ) / (n+1)
    repeated_lengths = Counter(len(ix) for ix in bybird.values())
    return {
        "status": "POST_EXPOSURE_EXPLORATORY_IDENTITY_PERSISTENCE_NOT_CAUSAL",
        "source_commit": SOURCE_COMMIT,
        "source_sha256_crlf": DRYAD_SHA256,
        "n_bird_years": len(records),
        "n_individuals": len(bybird),
        "n_repeat_observed_individuals": len(repeated),
        "n_nonindependent_within_individual_year_pairs": sum(map(len, repeated)),
        "observed_years_per_individual_distribution": {
            str(k): v for k, v in sorted(repeated_lengths.items())
        },
        "stage_names": {
            "2": "first_migration_flight",
            "3": "iceland_staging_start",
            "4": "later_iceland_staging_start",
            "5": "iceland_departure_second_flight",
            "6": "early_breeding_start",
        },
        "bird_equal_standardized_crossyear_product": {
            str(stage): base[j] for j, stage in enumerate(STAGES)
        },
        "descriptive_crossyear_pair_pearson": {
            str(stage): pears[j] for j, stage in enumerate(STAGES)
        },
        "stage_identity_permutation_p_positive": pstage,
        "stage5_max_of_all_five_stages_postselection_p": pmax5,
        "stage5_minus_stage3_observed_bird_equal_product": base[3]-base[1],
        "stage5_minus_stage3_permutation_p_positive": p5_minus3,
        "stage5_bird_equal_product_bootstrap_95_descriptive": [
            percentile(bootstrap_stage5, .025),
            percentile(bootstrap_stage5, .975)
        ],
        "permutations": n,
        "bird_bootstrap_samples": boots,
        "seed": SEED,
        "source_year_stages": year_scales,
        "outcome_or_energy_read": False,
        "ecological_claim": (
            "Identity-associated persistence of year-centred exit timing, "
            "if above an identity-shuffle null; not clock/cue/control/fitness"
        ),
        "prior_exposure_caveat": (
            "All five stage pair correlations had been inspected before "
            "this permutation audit; adjusted p does not transform an "
            "exploratory contrast into a preregistered confirmatory test."
        )
    }


def test_synthetic():
    rng = random.Random(SEED)
    rows = []
    for yr in range(1, 6):
        for bird in range(1, 21):
            # Stable per-bird exit residual; other stages have fresh noise.
            noise = [rng.gauss(0, 3) for _ in range(5)]
            stage5 = 125 + yr + (bird-10)*.36 + rng.gauss(0, .4)
            stage3 = 95 + yr + noise[1]
            rows.append({
                "bird": bird,
                "year": yr,
                "times": [
                    85 + noise[0] + yr,
                    stage3,
                    110 + yr + noise[2],
                    stage5,
                    145 + yr + noise[4],
                ],
            })
    vals, _ = standardized_stage_residuals(rows)
    pairs = list(combinations(range(5), 2))
    assert len(STAGES) == 5
    assert len(vals) == len(rows)
    # Synthetic has 20 repeated birds, not the exact source panel of 30.
    repeats = []
    bybird = defaultdict(list)
    for i, r in enumerate(rows):
        bybird[r["bird"]].append(i)
    for ix in bybird.values():
        repeats.append(list(combinations(ix, 2)))
    z = stats(vals, repeats)
    assert z[3] > z[1] and z[3] > 0.5, z
    print("PAYOFF_B_GOOSE_INDIVIDUAL_EXIT_REPEATABILITY_SYNTHETIC_PASS")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--output", default="outputs/payoff_b_goose_individual_exit_repeatability.json")
    args = p.parse_args()
    if args.self_test:
        test_synthetic()
    else:
        request = Request(SOURCE_URL, headers={
            "Accept": "text/csv",
            "User-Agent": "PAYOFF-B/public-source-identity-audit"
        })
        with urlopen(request, timeout=30) as resp:
            raw = resp.read(200000)
        records = read_dates(raw)
        result = permutation_test(records)
        target = Path(args.output)
        target.parent.mkdir(exist_ok=True, parents=True)
        target.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        print("PAYOFF_B_GOOSE_INDIVIDUAL_EXIT_REPEATABILITY_RESULT")
        print(json.dumps({
            k: result[k]
            for k in (
                "n_repeat_observed_individuals",
                "observed_years_per_individual_distribution",
                "bird_equal_standardized_crossyear_product",
                "descriptive_crossyear_pair_pearson",
                "stage_identity_permutation_p_positive",
                "stage5_max_of_all_five_stages_postselection_p",
                "stage5_minus_stage3_permutation_p_positive",
                "stage5_bird_equal_product_bootstrap_95_descriptive",
                "permutations",
            )
        }, sort_keys=True))
        print("NO FITNESS, ENVIRONMENTAL CUE OR ACTIVE CONTROL IDENTIFIED")
