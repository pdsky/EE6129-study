"""Which lecture sections each past final-exam question tests (4 papers: 2023-24 S2, 2024-25 S2, 2025-26 S1, 2025-26 S2).

Used by inject_anim.py (the 🎯 期末考点 line under each section heading) and by build_hub.py (the 考试重点图 on the learn hub).
Question ids are the ids in src/exams/data_*.py; sections are 'page:N.M' as in <span class="zh-num">.
"""
import importlib, pathlib, re, sys

HITS = {
    # ---------- Part 2 Q1: channel / detection / diversity / MIMO ----------
    'y2324s2-q1a':  ['p2:2.1', 'p2:2.2', 'p2:2.4', 'p2:2.5', 'p2:2.7'],
    'y2425s2-q1a':  ['p2:2.1', 'p2:2.6', 'p2:2.8'],
    'y2526s1-q1a':  ['p2:1.5', 'p2:3.2', 'p2:3.3'],
    'y2526s2-q1a':  ['p2:2.4', 'p2:2.5', 'p2:2.6', 'p2:2.7'],
    'y2324s2-q1b1': ['p2:4.2', 'p2:4.3'],
    'y2425s2-q1b1': ['p2:4.2', 'p2:4.3'],
    'y2526s1-q1b1': ['p2:4.2', 'p2:4.3'],
    'y2526s2-q1b1': ['p2:4.3'],
    'y2324s2-q1b2': ['p2:4.4', 'p2:5.4'],
    'y2425s2-q1b2': ['p2:4.4', 'p2:5.5'],
    'y2526s1-q1b2': ['p2:5.2', 'p2:5.5'],
    'y2526s2-q1b2': ['p2:5.1', 'p2:5.4'],
    # ---------- Part 2 Q2: equalization + OFDM ----------
    'y2324s2-q2a':  ['p2:6.1', 'p2:6.3'],
    'y2425s2-q2a':  ['p2:6.1', 'p2:6.3'],
    'y2526s1-q2a':  ['p2:6.1', 'p2:6.3'],
    'y2526s2-q2a':  ['p2:6.1', 'p2:6.3'],
    'y2324s2-q2b':  ['p2:7.1', 'p2:7.3', 'p2:7.4'],
    'y2425s2-q2b':  ['p2:7.1', 'p2:7.4', 'p2:7.5'],
    'y2526s1-q2b':  ['p2:7.1', 'p2:7.2'],
    'y2526s2-q2b':  ['p2:7.2', 'p2:7.3', 'p2:7.4'],
    # ---------- Part A Q3 / Q4 ----------
    'y2324s2-q3a':  ['A:8.3', 'A:8.4', 'A:9.2'],
    'y2324s2-q3b':  ['A:1.1', 'A:1.2', 'A:1.3'],
    'y2324s2-q4c':  ['A:7.2', 'A:7.3', 'A:9.2'],
    'y2425s2-q3':   ['A:6.1', 'A:7.2', 'A:8.3', 'A:9.1', 'A:9.2'],
    'y2425s2-q4a':  ['A:2.3'],
    'y2425s2-q4c':  ['A:6.1', 'A:8.3', 'A:8.4'],
    'y2526s1-q3a':  ['A:4.2', 'A:6.2'],
    'y2526s1-q3b':  ['A:8.5'],
    'y2526s1-q3c':  ['A:7.4'],
    'y2526s2-q3a':  ['A:6.1', 'A:6.2'],
    'y2526s2-q3bc': ['A:8.1', 'A:8.5'],
    'y2526s2-q4a':  ['A:10.3'],
    # ---------- Part B / C (Q4) ----------
    'y2324s2-q4ab': ['B:7.2', 'B:7.6'],
    'y2425s2-q4b':  ['B:7.4'],
    'y2526s1-q4a':  ['B:3.3'],
    'y2526s1-q4bc': ['B:7.1', 'B:7.6'],
    'y2526s2-q4c':  ['B:5.2'],
    'y2526s2-q4d':  ['B:7.4'],
    'y2526s2-q4b':  ['C:6.2'],
}

PAPERS = [('y2324s2', '2023-24 S2'), ('y2425s2', '2024-25 S2'), ('y2526s1', '2025-26 S1'), ('y2526s2', '2025-26 S2')]
SHORT = {'y2324s2': '23-24', 'y2425s2': '24-25', 'y2526s1': '25-26 S1', 'y2526s2': '25-26 S2'}


def load_questions():
    ex = pathlib.Path(__file__).resolve().parents[1] / 'exams'
    sys.path.insert(0, str(ex))
    qs = {}
    for m in ['data_2324', 'data_2425', 'data_2526s1', 'data_2526s2']:
        for q in importlib.import_module(m).QS:
            qs[q['id']] = {'id': q['id'], 'paper': q['paper'], 'q': q['q'], 'page': q['page'],
                           'topic': re.sub(r'<[^>]+>', '', q['topic'])}
    missing = set(qs) - set(HITS)
    extra = set(HITS) - set(qs)
    if missing or extra:
        raise SystemExit(f'exam_hits: unmapped questions {sorted(missing)}, unknown ids {sorted(extra)}')
    return qs


def by_section():
    """{ 'p2:6.3': [question dicts in paper order] }"""
    qs = load_questions()
    order = [p for p, _ in PAPERS]
    out = {}
    for qid, secs in HITS.items():
        for s in secs:
            out.setdefault(s, []).append(qs[qid])
    for s in out:
        out[s].sort(key=lambda q: (order.index(q['paper']), q['q']))
    return out


def years(qlist):
    return len({q['paper'] for q in qlist})
