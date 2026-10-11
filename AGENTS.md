# Agent instructions

This is a developer template, not an Agent Skill. Do not add a root `SKILL.md` here.

- Keep generators dependency-free and deterministic.
- The generated Skill `name` must match its parent directory.
- Never infer a personality or claim of a historical figure from template variables.
- Do not bypass placeholder checks just to mark an unfinished Skill as released.
- Ensure templates warn about exact historical quotations and modern events.
- Add a regression test for changes to generator behavior.
- Run `python -m unittest discover -s tests -v` before merging.