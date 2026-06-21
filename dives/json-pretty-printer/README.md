# JSON Pretty Printer

## What question are we exploring?

Can Pyodide turn Python's `json` module into a small browser-side formatter and validator?

## What did we try?

We built a standalone page that sends pasted JSON plus formatting options to a Python `format_json` function.

## What did we learn?

The stdlib JSON decoder gives useful line and column information, which makes browser validation easy without a server or JavaScript parsing library.

## What should happen next, if anything?

Add JSONPath-style extraction only if this stops being a simple pretty printer.
