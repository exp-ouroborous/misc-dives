# Markdown To HTML

## What question are we exploring?

Can a static page load a real Python package in Pyodide and use it for Markdown conversion?

## What did we try?

We used Pyodide's `micropip` support to install the Python `markdown` package in the browser, then called a local `convert_markdown` helper. The page now supports local Markdown file loading, common extension toggles, preview/HTML/notes tabs, multiple copy formats, and optional sanitizing through `bleach`.

## What did we learn?

Pyodide can run more than stdlib demos, but package installation adds a visible loading step and needs clear failure messaging. Python-Markdown is useful, but it is not GitHub Markdown, and raw HTML must be treated carefully unless sanitizing is available and enabled.

## What should happen next, if anything?

Add sample presets only if repeatedly typing extension-specific examples gets annoying.
