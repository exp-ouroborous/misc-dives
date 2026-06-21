# Deploy & integration

This is a **pure static site** — no build step, no bundler, no server. The site is
the [`dives/`](dives/) directory: each dive is a folder with an `index.html` +
`tool.py`, sharing [`dives/assets/`](dives/assets/) (`dive.css`, `pyodide-tools.js`),
and Pyodide loads from a CDN. "Deploying" is just serving `dives/` as static files.

## Cloudflare Pages

**Status: live** at **https://misc-dives.pages.dev** (project `misc-dives`).

Config lives in [wrangler.jsonc](wrangler.jsonc) — `pages_build_output_dir: "dives"`,
so the deployed site root is the `dives/` directory:

- `misc-dives.pages.dev/` — index of the dives
- `misc-dives.pages.dev/<slug>/` — a dive (e.g. `/regex-tester/`)
- `misc-dives.pages.dev/assets/` — the shared CSS/JS

The verified Pages settings (set these if you re-create the project):

| Setting             | Value      |
|---------------------|------------|
| Production branch   | `main`     |
| Build command       | *(empty)*  |
| Build output dir    | `dives`    |
| Framework preset    | None       |

**Recommended — connect Git (zero secrets, auto-deploys).** In the Cloudflare
dashboard: Workers & Pages → `misc-dives` → Settings → Builds & deployments →
Connect to Git → pick this repo, with the settings above. After that every push to
`main` auto-deploys. (The project's first deployment was a one-shot
`wrangler pages deploy dives` CLI upload; connecting Git switches it to auto-deploy.)

**Manual one-off deploy — CLI:**

```bash
npx wrangler pages deploy dives --project-name misc-dives
```

## Integration contract (read before changing paths)

Each dive is **also reverse-proxied same-origin** by the sister repo
`words-for-the-unwise` under `wordsfortheunwise.com/learn/<slug>/` (its `/learn`
splash links to each dive; the proxy lives in that repo's `src/middleware.ts`,
mapping `/learn/<slug>/* → misc-dives.pages.dev/<slug>/*` and
`/learn/assets/* → misc-dives.pages.dev/assets/*`).

For that to keep working, **every reference must stay relative**:

- ✅ `href="../assets/dive.css"`, `import "../assets/pyodide-tools.js"`,
  `fetch("tool.py")`, back-link `href="../"` — all relative today.
- ❌ Never use leading-slash/root paths (`/assets/...`) — they break when mounted
  at `/learn/<slug>/`.
- ❌ Never hardcode a `<base href>` — it would pin a dive to one mount path.
- Pyodide stays an absolute CDN URL — unaffected by mounting.

The bare-path → trailing-slash redirect (so `fetch("tool.py")` resolves against
`/learn/<slug>/`) is handled by the proxy on the `words-for-the-unwise` side, so
nothing here needs to change for it.

### Adding a dive

1. Create `dives/<slug>/` with `index.html` + `tool.py` (relative paths only).
2. Add a row to `dives/index.html`.
3. In `words-for-the-unwise`, add `<slug>` to the `PROXIES` table in
   `src/middleware.ts` and a card to `src/pages/learn/index.astro`.
