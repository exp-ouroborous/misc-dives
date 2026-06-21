# JSON Pretty Printer

## What question are we exploring?

Can Pyodide turn Python's `json` module into a small browser-side formatter and validator?

## What did we try?

We built a standalone page that sends pasted JSON plus formatting options to Python functions for formatting, validation, tree analysis, and conservative repair.

## What did we learn?

The stdlib JSON decoder gives useful line and column information, which makes browser validation easy without a server or JavaScript parsing library. A tiny repair layer can help with common almost-JSON snippets, but it should stay narrow: quote simple bare keys or values, append missing closing braces or brackets, then only accept the repair if Python can parse the result.

## What should happen next, if anything?

Add JSONPath-style extraction only if this stops being a simple pretty printer.
