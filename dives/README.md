# Dives

Each folder here is a small, self-contained learning dive.

## Current Dives

- [Regex Tester](./regex-tester/) - one regex, four engines: Python `re`, .NET, Go RE2 and C++ `std::regex`, each in WebAssembly in the wasm-dives sandbox, with View source.
- [JSON Pretty Printer](./json-pretty-printer/) - Python `json` formatting, minifying, sorting, validation, tree explorer, and conservative repair.
- [Markdown To HTML](./markdown-to-html/) - real Python `markdown` package conversion through Pyodide and `micropip`.
- [Text Diff](./text-diff/) - Python `difflib` side-by-side and unified diffs for two text blocks.

## Suggested structure

```text
dives/<topic-slug>/
  README.md
  index.html
  tool.py
```
