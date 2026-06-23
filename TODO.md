# TODO

Repo bootstrap is done: there are four dives under `dives/<topic-slug>/`, a
browsable static index (`dives/index.html` + `dives/README.md`), and a live
Cloudflare Pages deploy (see `DEPLOY.md`).

## Possible next dives

- [ ] Another stdlib-backed Pyodide tool (e.g. `datetime`/`zoneinfo` converter,
      `base64`/hashing, `csv` viewer) following the existing dive shape.

## Per-dive enhancements (deferred on purpose)

Each is intentionally gated on the dive outgrowing "learning dive" status:

- [ ] Regex Tester — highlight matches inline in the input text.
- [ ] JSON Pretty Printer — JSONPath-style extraction.
- [ ] Text Diff — word-level highlights inside replaced lines.
- [ ] Markdown to HTML — extension-specific sample presets.

## Repo decisions

- [ ] Decide when a dive should graduate into its own repository (criteria in
      `README.md` / `AGENTS.md`: real infra, CI, secrets, or a long-lived app).
- [ ] CI for `tests/` is deliberately **not** set up — `AGENTS.md` discourages
      infrastructure. Run `python3 -m pytest tests/` locally. Revisit only if the
      suite grows enough that manual runs stop being reliable.
