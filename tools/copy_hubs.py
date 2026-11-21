#!/usr/bin/env python3
"""Copy the four hub pages (学习 / 练习, 中文 + 中英对照) from EE6129_artifacts into the repo root,
so they can be opened from a clone or a downloaded ZIP (e.g. on Windows) without claude.ai.

The published hubs link to each other by claude.ai artifact URL; in the repo copies those four URLs
become the local file names. Links to the other course pages stay as they are: inside the hubs they
are routed to the embedded copies by the page script.

Run after rebuilding the hubs:  /usr/bin/python3 tools/copy_hubs.py
"""
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
HUBS = {  # file name : artifact id of the published page
    'hub-learn.html': 'XqzQHgfNzRa3aBXWVY2zyN',
    'hub-practice.html': 'BmujPtNyD7Jrz8g3kKta7T',
    'hub-learn-en.html': 'Rvbr4jMsP64PmHcmAh1goW',
    'hub-practice-en.html': 'DkEztJ4HDiLy67E3E1b4Bb',
}

for name in HUBS:
    s = (ART / name).read_text(encoding='utf-8')
    n = 0
    for other, aid in HUBS.items():
        url = f'https://claude.ai/artifact/{aid}'
        n += s.count(url)
        s = s.replace(url, other)
    assert 'claude.ai/artifact/' + HUBS[name] not in s
    (REPO / name).write_text(s, encoding='utf-8')
    print(f'{name}: {len(s.encode()) / 1e6:.2f} MB, {n} hub links made local')
