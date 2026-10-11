# Template design guide

This repo intentionally has **no root SKILL.md**, because it is a source template and not an installable thinker.

## Name and structure

Generated directory slug must be lowercase letters, numbers and single hyphens, at most 64 chars. That slug must match the frontmatter `name` exactly.

Generated scaffold:

```text
<slug>/
├── SKILL.md
├── README.md
├── AGENTS.md
├── LICENSE
├── references/
│   ├── frameworks.md
│   ├── sources.md
│   └── boundaries.md
├── examples/
│   └── demo.md
└── evals/
    └── test-cases.md
```

## Release gate

Run `python scripts/check_skill.py PATH --release`, then perform runtime verification in the actual agent. The script catches structural/placeholder issues, **not source accuracy or the quality of reasoning**.

Require at least one reviewer to check quotes and modern-transfer boundaries. See [docs/release-checklist.md](docs/release-checklist.md).