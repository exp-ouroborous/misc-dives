# Markdown To HTML

## What question are we exploring?

Can a static page load a real Python package in Pyodide and use it for Markdown conversion?

## What did we try?

We used Pyodide's `micropip` support to install the Python `markdown` package in the browser, then called a local `convert_markdown` helper. The page now supports local Markdown file loading, common extension toggles, preview/HTML/notes tabs, multiple copy formats, and optional sanitizing through `bleach`.

## What did we learn?

Pyodide can run more than stdlib demos, but package installation adds a visible loading step and needs clear failure messaging. Python-Markdown is useful, but it is not GitHub Markdown, and raw HTML must be treated carefully unless sanitizing is available and enabled.

## What should happen next, if anything?

Add sample presets only if repeatedly typing extension-specific examples gets annoying.

## Update (2026-10-25): every language

The page now converts Markdown with a real library in the language you pick:
Python-Markdown 3.11 (with bleach for safe mode), Markdig 1.4.0 (C#),
goldmark v1.8.6 (Go) or md4c 0.6.0 (C/C++), each in WebAssembly inside the
wasm-dives sandbox. The libraries are pinned and served from that sandbox's
manifest; nothing is installed from PyPI at runtime any more. Features a
library lacks (footnotes in md4c, TOC outside Python, ...) are disabled on the
page and refused by the engine, from one capability table
(`site/cards/wasm-assets/markdown-features.mjs` in wasm-dives). `tool.py` is
gone; its tests became wasm-dives' Markdown contract.
