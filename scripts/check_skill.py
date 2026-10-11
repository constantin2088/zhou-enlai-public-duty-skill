#!/usr/bin/env python3
"""Check generated thinker skill completeness."""
import argparse
import re
from pathlib import Path

def check(root,release=False):
    root=Path(root)
    problems=[]
    skill=root/'SKILL.md'
    if not skill.exists():problems.append('missing SKILL.md')
    else:
        txt=skill.read_text(encoding='utf-8')
        match=re.match(r'^---\n(.*?)\n---\n',txt,re.S)
        if not match:problems.append('missing YAML frontmatter')
        else:
            yaml=match.group(1)
            for k in ('name','description'):
                if not re.search(r'^'+k+r':\s*\S+',yaml,re.M): problems.append(f'missing {k}')
        if release and ('TODO' in txt or 'DRAFT' in txt):problems.append('unresolved TODO/DRAFT in SKILL.md')
    for rel in ('README.md','references/sources.md','references/frameworks.md','references/boundaries.md','evals/test-cases.md'):
        p=root/rel
        if not p.exists():problems.append('missing '+rel)
        elif release and ('TODO' in p.read_text(encoding='utf-8') or 'DRAFT' in p.read_text(encoding='utf-8')):problems.append('unfinished '+rel)
    if release:
        for file in root.rglob('*.md'):
            if '.git' not in file.parts and re.search(r'\b(?:TODO|DRAFT)\b', file.read_text(encoding='utf-8')):
                problems.append('unfinished '+file.relative_to(root).as_posix())
        if skill.exists():
            name=re.search(r'^name:\s*(\S+)',skill.read_text(encoding='utf-8'),re.M)
            if not name or name.group(1)!=root.resolve().name:problems.append('skill name must match directory')
    return problems

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('path',nargs='?',default='.')
    p.add_argument('--release',action='store_true')
    a=p.parse_args()
    errors=check(a.path,a.release)
    for err in errors:print('ERROR:',err)
    print('FAIL' if errors else 'PASS')
    raise SystemExit(bool(errors))
