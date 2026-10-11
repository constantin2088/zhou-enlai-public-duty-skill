import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
errors=[]
for file in root.rglob('*.md'):
    if '.git' in file.parts:continue
    for link in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
        if link.startswith(('http:','https:','#')):continue
        path=link.split('#')[0]
        if path and not (file.parent/path).exists():errors.append(f'{file.relative_to(root)}: {link}')
if errors:raise SystemExit('\n'.join(errors))
print('PASS: local Markdown links resolve')
