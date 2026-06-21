# Text Diff

## What question are we exploring?

Can Python's `difflib` provide a useful text diff inside a static browser page?

## What did we try?

We built a two-input page that loads a `build_diff` Python function through Pyodide, accepts pasted text or browser-local files, and renders both side-by-side rows and unified diff output.

## What did we learn?

`difflib.unified_diff` is enough for copyable output, while `difflib.SequenceMatcher` provides a compact structure for a friendlier side-by-side view. Browser file inputs can load local text into the page without uploading anything.

## What should happen next, if anything?

Add word-level highlights inside replaced lines only if the row-level view still feels too coarse.
