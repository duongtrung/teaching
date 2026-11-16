"""Audit a fictional internship recommender. Python standard library only."""
from csv import DictReader, DictWriter
from math import log2
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
K = 3
ATTENTION = (1.0, 0.5, 0.25)  # Hypothetical attention units, not the DCG discounts.


def read_csv(name):
    """Read an input CSV from the package."""
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as source:
        return list(DictReader(source))


def load_case():
    """Return employer groups, learner groups, rankings, and held-out judgments."""
    size = {r["item"]: r["employer_size"] for r in read_csv("listings.csv")}
    learners = read_csv("learners.csv")
    segments = {r["learner"]: r["learner_group"] for r in learners}
    lists = {r["learner"]: [r[f"rank_{i}"] for i in range(1, 5)] for r in learners}
    grades = {r["learner"]: {item: int(r[item]) for item in size}
              for r in read_csv("relevance.csv")}
    return size, segments, lists, grades


def dcg(ranked_grades, k=K):
    """Use gain 2**grade - 1 and the reciprocal log rank discount."""
    total = 0.0
    for rank, grade in enumerate(ranked_grades[:k], start=1):
        gain = 2**grade - 1  # Convert a grade of 0, 1, or 2 to gain 0, 1, or 3.
        total += gain / log2(rank + 1)  # Earlier positions contribute more.
    return total


def ndcg(ranking, judgments, k=K):
    """Normalize against the best k eligible judged items, including unseen items."""
    shown = [judgments[item] for item in ranking[:k]]
    ideal = sorted(judgments.values(), reverse=True)
    best = dcg(ideal, k)
    return dcg(shown, k) / best if best else None  # No useful known item: undefined.


def exposure(rankings, size):
    """Return modeled exposure per listing; unshown listings receive zero."""
    by_item = dict.fromkeys(size, 0.0)
    for ranking in rankings.values():
        for item, weight in zip(ranking[:K], ATTENTION):
            by_item[item] += weight
    return by_item


def promote_small(ranking, size, target=2):
    """If needed, move the highest-ranked Small candidate to rank 1 or 2.

    The input contains only eligible candidates. Preserve the order of other
    candidates. If none are Small, return the original order and skip the move.
    """
    if target not in (1, 2):
        raise ValueError("Use position 1 or 2 in this exercise.")
    revised = list(ranking)
    if any(size[item] == "Small" for item in revised[:target]):
        return revised
    for index, item in enumerate(revised):
        if size[item] == "Small":
            revised.insert(target - 1, revised.pop(index))
            break
    return revised


def compare(name, rankings, size, segments, grades):
    """Summarize the same learners and exposure model for one policy."""
    q = {u: ndcg(order, grades[u]) for u, order in rankings.items()}
    e = exposure(rankings, size)
    valid = [v for v in q.values() if v is not None]
    count_small = sum(size[i] == "Small" for order in rankings.values() for i in order[:K])
    slots = sum(len(order[:K]) for order in rankings.values())
    total_exposure = sum(e.values())
    group_means = {}
    for group in ("New", "Returning"):
        known = [q[u] for u in q if segments[u] == group and q[u] is not None]
        group_means[group] = mean(known) if known else None
    return {
        "policy": name,
        "new_ndcg": group_means["New"],
        "returning_ndcg": group_means["Returning"],
        "overall_ndcg": mean(valid) if valid else None,
        "learners_with_ndcg": len(valid),
        "small_slot_share": count_small / slots if slots else None,
        "small_exposure_share": sum(e[i] for i in e if size[i] == "Small") / total_exposure
        if total_exposure else None,
        "total_exposure": total_exposure,
    }


def run():
    """Print an audit and write the exact results to CSV."""
    size, segments, base, grades = load_case()
    variants = {"Baseline": base}
    for target in (2, 1):
        variants[f"Promote to {target}"] = {u: promote_small(order, size, target)
                                            for u, order in base.items()}
    results = [compare(name, ranking, size, segments, grades)
               for name, ranking in variants.items()]
    for result in results:
        print(result["policy"],
              f'New={result["new_ndcg"]:.3f}',
              f'Returning={result["returning_ndcg"]:.3f}',
              f'Overall={result["overall_ndcg"]:.3f}',
              f'Small exposure={result["small_exposure_share"]:.1%}')
    directory = ROOT / "results"
    directory.mkdir(exist_ok=True)
    with (directory / "policy_comparison.csv").open("w", newline="", encoding="utf-8") as out:
        writer = DictWriter(out, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    return results


if __name__ == "__main__":
    run()
