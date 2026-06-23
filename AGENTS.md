# AGENTS.md

## Project Intent

`misc-dives` is for small learning topics that should not need their own repository. Optimize for low ceremony, clear notes, and easy future cleanup.

## Ground Rules

- Keep each dive self-contained under `dives/<topic-slug>/`.
- Prefer a short README per dive over elaborate scaffolding.
- Avoid broad frameworks, services, or infrastructure unless the dive specifically needs them.
- Do not add secrets, credentials, private data, or machine-specific assumptions.
- If a topic grows into a real project, recommend promoting it to a dedicated repo instead of expanding this one indefinitely.
- Keep root-level files focused on repo-wide guidance and indexes.

## Tests

Each dive's `tool.py` is pure data-in/data-out, so the logic is testable in
plain CPython (no browser). The suite in `tests/` also asserts that each
`index.html` contains its expected UI regions. Run it with:

```bash
python3 -m pytest tests/
```

Markdown tests skip locally unless the `markdown`/`bleach` packages are
installed — in the browser Pyodide's `micropip` supplies them.

## Dive Template

Each dive README should answer:

- What question are we exploring?
- What did we try?
- What did we learn?
- What should happen next, if anything?
