#!/usr/bin/env python3
"""Create a safe, clearly marked draft Agent Skill. No network/deps."""
import argparse
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / 'templates'

def validate_slug(slug):
    if len(slug)>64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):
        raise ValueError('slug must be <=64 chars, lowercase ASCII with single hyphens')
    return slug

def clean_one_line(value, label):
    if not value.strip():
        raise ValueError(f'{label} required')
    if any(ord(c) < 32 for c in value) or '__' in value:
        raise ValueError(f'{label} must be one line without control characters or template markers')
    return value.strip()

def create(slug,person,focus,output):
    validate_slug(slug)
    person=clean_one_line(person, 'name')
    focus=clean_one_line(focus, 'focus')
    target = Path(output).expanduser().resolve() / slug
    if target.exists():
        raise FileExistsError(f'Output already exists (will not overwrite): {target}')
    variables={'__SLUG__':slug,'__PERSON__':person,'__FOCUS__':focus,'__YEAR__':str(date.today().year)}
    for src in sorted(TEMPLATES.rglob('*.tmpl')):
        rel=src.relative_to(TEMPLATES)
        dst=target / str(rel)[:-5]
        dst.parent.mkdir(parents=True,exist_ok=True)
        data=src.read_text(encoding='utf-8')
        for key,value in variables.items():data=data.replace(key,value)
        dst.write_text(data,encoding='utf-8')
    import json
    from sync_series import sync_readme
    catalog = json.loads((target/'series-catalog.json').read_text(encoding='utf-8'))
    sync_readme(target, catalog, slug)
    return target

def main():
    p=argparse.ArgumentParser(description='Generate a new research-grounded thinker Skill draft')
    p.add_argument('--slug',required=True)
    p.add_argument('--name-zh',required=True)
    p.add_argument('--focus',required=True)
    p.add_argument('--output',default='./dist')
    a=p.parse_args()
    try:
        target=create(a.slug,a.name_zh,a.focus,a.output)
    except (ValueError,FileExistsError) as exc:
        p.error(str(exc))
    print(f'Created draft: {target}')
    print('Next: fill TODO fields, verify sources and run check_skill.py --release')

if __name__=='__main__': main()
