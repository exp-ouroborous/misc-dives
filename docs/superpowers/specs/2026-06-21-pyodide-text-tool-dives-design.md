# Pyodide Text Tool Dives Design

## Context

`misc-dives` is a home for small learning topics that should not need standalone repositories. The first batch of dives should be compact, static, and easy to delete, archive, or later promote. Each dive should live under `dives/<topic-slug>/` and answer the repo's README questions: what question we explored, what we tried, what we learned, and what should happen next.

The dives should also be suitable for later surfacing from the sibling `words-for-the-unwise` site's `/learn` catalog, following the existing Pyodide dive pattern: separately deployed static experiences, linked by cards, and reverse-proxied under `/learn/<slug>/` if same-origin hosting is needed.

## Goals

- Add four separate browser-based dives:
  - `regex-tester`
  - `json-pretty-printer`
  - `text-diff`
  - `markdown-to-html`
- Prefer Pyodide for the runtime logic, using Python stdlib where possible.
- Keep each dive self-contained and static: no framework, no build step, no server, no secrets.
- Update `dives/README.md` as a simple index.
- Preserve an easy future path for `words-for-the-unwise` cards and proxy prefixes.

## Non-Goals

- Do not build a shared app shell or router.
- Do not add package managers, bundlers, CI, or service infrastructure.
- Do not edit `../words-for-the-unwise` in this first implementation unless explicitly requested after the dives exist.
- Do not attempt production-grade sanitization or adversarial input handling beyond clear browser-demo boundaries.

## Architecture

Each dive is a standalone static page:

```text
dives/<topic-slug>/
  README.md
  index.html
```

The `index.html` page loads Pyodide from a CDN, initializes it on page load or first use, and calls small Python snippets from JavaScript. UI state stays in vanilla browser JavaScript. Python returns JSON-serializable results so the JavaScript layer can render outputs and errors predictably.

The pages should use relative paths only, so they can work directly under `/dives/<slug>/`, from a static host, or behind a future reverse proxy subpath such as `/learn/<slug>/`.

## Dive Behavior

### Regex Tester

Uses Python `re`.

Inputs:
- regex pattern
- test text
- flags such as ignore case, multiline, dotall
- optional replacement text

Outputs:
- compile or runtime errors
- match count
- spans and matched text
- named and numbered groups
- substitution preview

### JSON Pretty Printer

Uses Python `json`.

Inputs:
- JSON text
- formatting options: indent, sort keys, minify

Outputs:
- validation status
- formatted or minified JSON
- parse error message with line and column when available

### Text Diff

Uses Python `difflib`.

Inputs:
- left text
- right text
- optional labels

Outputs:
- unified diff text
- simple summary of added, removed, and changed lines

### Markdown To HTML

Uses Pyodide plus `micropip.install("markdown")` to load the real Python `markdown` package.

Inputs:
- Markdown text
- a small extension preset if supported without extra complexity

Outputs:
- rendered HTML source
- live preview in a sandboxed or carefully isolated preview region
- package loading and conversion errors

## Error Handling

Each page should show:

- Pyodide loading state
- package loading state for Markdown
- Python exception messages in a readable output area
- invalid input errors without throwing unhandled browser exceptions

If Pyodide or package loading fails, the page should remain usable enough to show the failure and let the user retry by reloading.

## Testing And Verification

Because these are static dives, verification should be lightweight:

- Open each `index.html` locally or through a simple static server.
- Confirm Pyodide loads.
- Run one happy-path sample per dive.
- Run one invalid-input sample per dive.
- Confirm `dives/README.md` links to each dive.

If browser tooling is available, use a local static server and basic rendered checks. If not, document the limitation and at least inspect the files and sample logic.

## Future Linkage From `words-for-the-unwise`

After these dives exist and a static hosting origin is chosen, the sibling site can add:

- four themed cards in `src/pages/learn/index.astro`
- four matching proxy prefixes in `src/middleware.ts`, if same-origin subpaths are desired

The dive pages must continue using relative asset and fetch paths so the proxy model remains viable.
