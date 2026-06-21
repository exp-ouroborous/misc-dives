# Regex Tester

## What question are we exploring?

Can a tiny static page use Pyodide to make Python's `re` module feel like a practical browser regex tester?

## What did we try?

We built a standalone `index.html` that loads Pyodide, fetches `tool.py`, and runs Python `re` against a pattern, sample text, flags, and optional replacement.

## What did we learn?

Python regex behavior can be exposed cleanly through a small JSON-shaped function. Named groups, numbered groups, spans, compile errors, and substitution previews all fit in a compact result object.

## What should happen next, if anything?

Add highlighting in the input text if this grows beyond a learning dive.
