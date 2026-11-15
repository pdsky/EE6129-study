#!/usr/bin/python3
"""Merge the English steps written by the step-expansion groups into src/p2build/sol_en.py.

Each src/steps/en_<group>.py defines STEPS = {qid: [step, ...]} and optionally IDEA = {qid: text}.
This script replaces the `steps=` list (and `idea=` value) of EN['qid'] = dict(...) in sol_en.py,
using the ast source positions, then re-imports sol_en.py and checks the result matches.
usage: merge_en.py [--dry]
"""
import ast, pathlib, runpy, sys

HERE = pathlib.Path(__file__).resolve().parent
SOL = HERE.parent / 'p2build' / 'sol_en.py'


def lit(s):
    assert "'''" not in s and not s.endswith('\\'), s[:60]
    return "r'''" + s + "'''"


def load_groups():
    steps, idea = {}, {}
    for f in sorted(HERE.glob('en_*.py')):
        d = runpy.run_path(str(f))
        for k, v in d.get('STEPS', {}).items():
            assert k not in steps, f'{k} twice'
            assert isinstance(v, list) and v and all(isinstance(x, str) for x in v), k
            steps[k] = v
        idea.update(d.get('IDEA', {}) or {})
    return steps, idea


def main(dry=False):
    steps, idea = load_groups()
    src = SOL.read_text(encoding='utf-8')
    lines = src.splitlines(keepends=True)
    off = [0]
    for ln in lines:
        off.append(off[-1] + len(ln))
    pos = lambda l, c: off[l - 1] + len(lines[l - 1].encode('utf-8')[:c].decode('utf-8'))

    edits = []  # (start, end, text)
    seen = set()
    for node in ast.parse(src).body:
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        t = node.targets[0]
        if not (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == 'EN'):
            continue
        qid = t.slice.value if isinstance(t.slice, ast.Constant) else None
        if qid not in steps and qid not in idea:
            continue
        kw = {k.arg: k.value for k in node.value.keywords}
        if qid in steps:
            v = kw['steps']
            body = ',\n'.join('  ' + lit(s) for s in steps[qid])
            edits.append((pos(v.lineno, v.col_offset), pos(v.end_lineno, v.end_col_offset), '[\n' + body + ']'))
        if qid in idea:
            if 'idea' in kw:
                v = kw['idea']
                edits.append((pos(v.lineno, v.col_offset), pos(v.end_lineno, v.end_col_offset), lit(idea[qid])))
            else:
                v = kw['steps']
                p = pos(v.lineno, v.col_offset) - len('steps=')
                edits.append((p, p, 'idea=' + lit(idea[qid]) + ',\n '))
        seen.add(qid)
    missing = (set(steps) | set(idea)) - seen
    assert not missing, f'not in sol_en.py: {sorted(missing)}'
    for a, b, txt in sorted(edits, reverse=True):
        src = src[:a] + txt + src[b:]
    if dry:
        print('dry run ok:', len(steps), 'steps,', len(idea), 'ideas')
        return
    SOL.write_text(src, encoding='utf-8')
    EN = runpy.run_path(str(SOL))['EN']
    for k, v in steps.items():
        assert EN[k]['steps'] == v, k
    for k, v in idea.items():
        assert EN[k]['idea'] == v, k
    print('merged:', len(steps), 'step lists,', len(idea), 'ideas →', SOL)


if __name__ == '__main__':
    main('--dry' in sys.argv)
