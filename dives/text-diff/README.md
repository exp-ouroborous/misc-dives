# Text Diff

## What question are we exploring?

Can Python's `difflib` provide a useful text diff inside a static browser page?

## What did we try?

We built a two-input page that loads a `build_diff` Python function through Pyodide and renders unified diff output.

## What did we learn?

`difflib.unified_diff` is enough for a compact learning tool. A polished side-by-side diff would need more presentation code, but the core comparison is tiny.

## What should happen next, if anything?

Add inline or side-by-side rendering if the unified diff output feels too raw.
