#!/usr/bin/python3
"""知识讲解 + 详细解析 boxes for every practice question (written per BRIEF.md, one file per group).

load(*groups) -> {id: entry};  box(entry, lang) -> <details class="deep xpl"> … </details>
CSS works on every page (variables fall back between the page families' names).
Used by: p2build/add_xpl.py (Part 2 practice), exams/build_exams.py, tools/add_xpl_examples.py,
p2build/build_bc.py.
"""
import importlib.util
import pathlib

D = pathlib.Path(__file__).resolve().parent
GROUPS = {'p2': ('p2a', 'p2b', 'p2c'), 'exams': ('exA', 'exB'), 'examples': ('exm',), 'bc': ('bcB', 'bcC')}


def load(*groups):
    out = {}
    for g in groups:
        f = D / f'{g}.py'
        if not f.exists():
            raise SystemExit(f'missing {f}')
        spec = importlib.util.spec_from_file_location(f'xpl_{g}', f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for k, v in m.XPL.items():
            assert k not in out, k
            out[k] = v
    return out


def load_available(key):
    """Groups of one page family whose files exist (lets pages build while some are still being written)."""
    return load(*[g for g in GROUPS[key] if (D / f'{g}.py').exists()])


def box(e, lang='zh', indent=''):
    title = e['title_en'] if lang == 'en' else e['title']
    body = e['en'] if lang == 'en' else e['zh']
    return (f'{indent}<details class="deep xpl">\n{indent}  <summary>{title}</summary>\n'
            f'{indent}  <div class="deep-body">\n{body.strip()}\n{indent}  </div>\n{indent}</details>\n')


CSS = '''
.xpl{--xa:var(--extra,var(--accent));--xs:var(--extra-soft,var(--accent-soft));--xl:var(--line,var(--border));--xp:var(--surface-2,var(--paper,transparent));--xt:var(--ink,var(--text))}
details.deep.xpl{margin:12px 0 4px;border:1px solid var(--xa);border-left-width:5px;border-radius:10px;background:var(--card,var(--surface,transparent))}
details.deep.xpl > summary{cursor:pointer;list-style:none;padding:9px 14px;font-weight:700;font-size:.92rem;color:var(--xa);display:flex;gap:8px;align-items:baseline}
details.deep.xpl > summary::-webkit-details-marker{display:none}
details.deep.xpl > summary::before{content:'📘';font-size:.9rem}
details.deep.xpl[open] > summary{border-bottom:1px solid var(--xl)}
.xpl .deep-body{padding:4px 16px 14px;font-size:.93rem;line-height:1.75;color:var(--xt)}
.xpl h4{font-size:.95rem;font-weight:700;margin:16px 0 4px;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px}
.xpl h4 .st{font-size:.7rem;font-weight:700;background:var(--xs);color:var(--xa);border-radius:6px;padding:1px 8px;letter-spacing:.02em}
.xpl p{margin:.4em 0;max-width:78ch}
.xpl ul,.xpl ol{margin:.3em 0;padding-left:1.4em}
.xpl li{margin:.25em 0}
.xpl .tw{overflow-x:auto;margin:6px 0}
.xpl table.mini{border-collapse:collapse;width:auto;min-width:240px;font-size:.86rem}
.xpl table.mini th,.xpl table.mini td{padding:5px 10px;border-bottom:1px solid var(--xl);text-align:left;vertical-align:top}
.xpl table.mini th{font-size:.74rem;font-weight:700;color:var(--xa)}
.xpl .tmpl{border-left:3px solid var(--xa);background:var(--xp);border-radius:0 8px 8px 0;padding:6px 14px;margin:.4em 0;font-size:.9rem}
.xpl .tmpl p{margin:.3em 0}
.xpl .calc{overflow-x:auto}
.xpl .ans{margin-top:12px}
'''
