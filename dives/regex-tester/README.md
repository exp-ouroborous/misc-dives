# Regex Tester

## What question are we exploring?

Can a tiny static page use Pyodide to make Python's `re` module feel like a practical browser regex tester?

## What did we try?

We built a standalone `index.html` that loads Pyodide, fetches `tool.py`, and runs Python `re` against a pattern, sample text, flags, and optional replacement.

## What did we learn?

Python regex behavior can be exposed cleanly through a small JSON-shaped function. Named groups, numbered groups, spans, compile errors, and substitution previews all fit in a compact result object.

## What should happen next, if anything?

Add highlighting in the input text if this grows beyond a learning dive.

## Update (2026-10-25): every language

The page now runs the regex in the language you pick — Python, C#, Go or
C/C++ — on that language's own engine in WebAssembly, inside the wasm-dives
sandbox (a separate origin). The engines and their shared contract tests live
in the `wasm-dives` repo (`site/run/<lang>/engines/regex.*`,
`tests/engines/regex-cases.json`); this page only renders results. "View
source" shows the engine for the chosen language. `tool.py` is gone: Python
runs through the same sandbox path as the others.
