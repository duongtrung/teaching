"""Synthetic classroom network. All counts include the seeds."""
from pathlib import Path
import random
from itertools import combinations
import pandas as pd

def load_data(root):
    root = Path(root)
    people = pd.read_csv(root / 'data/raw/people.csv')
    links = pd.read_csv(root / 'data/raw/links.csv')
    assert people.person.is_unique, 'Each person needs a unique ID'
    ids = set(people.person)
    assert set(links.source) | set(links.target) <= ids
    assert not links.duplicated(['source', 'target']).any()
    assert links.p.between(0, 1).all()
    return people, links

def cascade(people, links, seeds, deadline=1, p=None, rng=None):
    """Sample one live-edge graph, then record first arrival by round.

    Independent edge draws are equivalent to one forwarding attempt per edge
    in the Independent Cascade model. A newly informed node forwards next round.
    p=None uses each row's probability. Supplying p overrides every edge.
    Only edges whose source becomes informed can affect the observed cascade.
    """
    ids = set(people.person)
    seeds = set(seeds)
    if not seeds <= ids: raise ValueError('Unknown seed')
    if not isinstance(deadline, int) or deadline < 0: raise ValueError('Invalid deadline')
    if p is not None and not 0 <= p <= 1: raise ValueError('Invalid probability')
    rng = rng or random.Random(42)
    adjacency = {person: [] for person in sorted(ids)}
    for row in links.itertuples(index=False):
        probability = row.p if p is None else p
        if rng.random() < probability: adjacency[row.source].append(row.target)
    arrival = {person: 0 for person in seeds}
    frontier = seeds
    for round_number in range(1, deadline + 1):
        new = {target for source in frontier for target in adjacency[source]} - set(arrival)
        for person in new: arrival[person] = round_number
        frontier = new
        if not frontier: break
    result = people.copy()
    result['arrival_round'] = pd.array([arrival.get(person) for person in result.person], dtype='Int64')
    result['reached'] = result.arrival_round.notna()
    return result

def trace(arrivals, deadline):
    rows = []
    class_order = {person: i for i, person in enumerate(arrivals.person)}
    for t in range(deadline + 1):
        new = sorted(arrivals.loc[arrivals.arrival_round.eq(t).fillna(False), 'person'], key=class_order.get)
        cumulative = sorted(arrivals.loc[arrivals.arrival_round.le(t).fillna(False), 'person'], key=class_order.get)
        rows.append({'round': t, 'new': ', '.join(new), 'cumulative': ', '.join(cumulative), 'count': len(cumulative)})
    return pd.DataFrame(rows)

def metrics(arrivals):
    by_group = arrivals.groupby('group').reached.agg(reached='sum', size='count').reindex(arrivals.group.drop_duplicates())
    by_group['coverage'] = by_group.reached / by_group['size']
    by_group['coverage_pct'] = 100 * by_group.coverage
    summary = {'total': int(arrivals.reached.sum()),
               'gap_pp': float(by_group.coverage_pct.max() - by_group.coverage_pct.min()),
               'min_coverage_pct': float(by_group.coverage_pct.min()),
               'sqrt_count_utility': float(by_group.reached.pow(0.5).sum())}
    return by_group, summary

def evaluate_pairs(people, links, deadline=1):
    """Exact enumeration for the p=1 teaching example, not a scalable optimizer."""
    rows = []
    for pair in combinations(people.person.tolist(), 2):
        a = cascade(people, links, pair, deadline=deadline, p=1.0)
        group, m = metrics(a)
        rows.append({'seeds': ', '.join(pair), 'deadline': deadline,
                     'reached_residents': int(group.loc['Resident', 'reached']),
                     'reached_commuters': int(group.loc['Commuter', 'reached']), **m})
    return pd.DataFrame(rows)

def greedy_reach(people, links, budget=2, deadline=1):
    """Break ties by class-list row order and record the tie explicitly."""
    selected, history = [], []
    for step in range(budget):
        current = metrics(cascade(people, links, selected, deadline, p=1))[1]['total']
        gains = {}
        for person in (x for x in people.person if x not in selected):
            total = metrics(cascade(people, links, selected + [person], deadline, p=1))[1]['total']
            gains[person] = total - current
        best_gain = max(gains.values())
        tied = [person for person in gains if gains[person] == best_gain]
        choice = tied[0]
        history.append({'step': step+1, 'selected_before': ', '.join(selected),
                        'ties': ', '.join(tied), 'choice': choice, 'new_recipients': best_gain})
        selected.append(choice)
    return selected, pd.DataFrame(history)
