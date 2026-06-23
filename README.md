# misc-dives

Small learning dives that do not need standalone repositories.

This repo is a home for compact experiments, notes, and tiny demos that are useful to keep, but not large or coherent enough to justify their own repo. Each dive should be self-contained and easy to delete, promote, or archive later.

## What's here now

The dives have converged into a small set of browser-based Python tools: each runs entirely client-side via [Pyodide](https://pyodide.org/), with no build step. See [`dives/`](dives/) for the index, [DEPLOY.md](DEPLOY.md) for hosting, and the live site at <https://misc-dives.pages.dev>.

## Shape

- Put each topic under `dives/<topic-slug>/`.
- Give each dive a short `README.md` with the question, what was tried, and what was learned.
- Keep setup light. If a dive starts needing real infrastructure, CI, secrets, or a long-lived app, consider promoting it to its own repository.

## Good candidates

- One-off learning notes
- Small API or library experiments
- Runtime behavior probes
- Tiny static demos
- Comparisons that fit in a few files

## Not a fit

- Production apps
- Long-lived services
- Experiments with sensitive data or secrets
- Anything that deserves its own release/history/issue space
