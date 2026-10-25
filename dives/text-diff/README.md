# Text Diff

## What question are we exploring?

Can Python's `difflib` provide a useful text diff inside a static browser page?

## What did we try?

We built a two-input page that loads a `build_diff` Python function through Pyodide, accepts pasted text or browser-local files, and renders side-by-side rows.

## What did we learn?

`difflib.SequenceMatcher` provides a compact structure for a friendly side-by-side view. Browser file inputs can load local text into the page without uploading anything.

## What should happen next, if anything?

Add word-level highlights inside replaced lines only if the row-level view still feels too coarse.

## Update (2026-10-25): every language

The page now diffs in the language you pick: Python's `difflib`, DiffPlex
1.9.0 (C#), go-diff v1.4.0 (Go) or a hand-written linear-space Myers diff
(C++), each in WebAssembly inside the wasm-dives sandbox. difflib's
Ratcliff/Obershelp matching can pair lines differently from the Myers-based
three; all four produce the same rows/counts/unified-diff shape, checked by
wasm-dives' diff contract (which validates every diff by applying it). Lines
split on LF only now; `tool.py` is gone.
