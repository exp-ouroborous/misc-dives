# Pyodide Text Tool Dives Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build four standalone static Pyodide text-tool dives: regex tester, JSON pretty printer, text diff, and Markdown to HTML.

**Architecture:** Each dive lives under `dives/<slug>/` with its own `README.md`, `index.html`, and `tool.py`. A tiny shared `dives/assets/` layer provides common CSS and Pyodide helpers while keeping the pages static, relative-path friendly, and easy to split later. Local `unittest` coverage imports the same `tool.py` files that the browser runs through Pyodide.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Pyodide CDN, Python stdlib (`re`, `json`, `difflib`), and the Python `markdown` package loaded with `micropip`.

---

## File Structure

- Create `dives/assets/dive.css`: shared restrained tool UI styling.
- Create `dives/assets/pyodide-tools.js`: shared Pyodide loader, Python file loader, JSON bridge, output helpers, and clipboard helpers.
- Create `dives/regex-tester/README.md`: dive notes.
- Create `dives/regex-tester/index.html`: regex UI and Python `re` bridge.
- Create `dives/regex-tester/tool.py`: tested regex behavior.
- Create `dives/json-pretty-printer/README.md`: dive notes.
- Create `dives/json-pretty-printer/index.html`: JSON UI and Python `json` bridge.
- Create `dives/json-pretty-printer/tool.py`: tested JSON behavior.
- Create `dives/text-diff/README.md`: dive notes.
- Create `dives/text-diff/index.html`: diff UI and Python `difflib` bridge.
- Create `dives/text-diff/tool.py`: tested diff behavior.
- Create `dives/markdown-to-html/README.md`: dive notes.
- Create `dives/markdown-to-html/index.html`: Markdown UI and `micropip` package bridge.
- Create `dives/markdown-to-html/tool.py`: tested Markdown behavior when the package exists.
- Modify `dives/README.md`: index the four dives.
- Create `tests/test_text_tool_dives.py`: local CPython tests for the Pyodide-targeted Python modules.

## Tasks

### Task 1: Test Scaffold

**Files:**
- Create: `tests/test_text_tool_dives.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_text_tool_dives.py` with tests that dynamically import each future `tool.py` file and verify representative behavior for regex, JSON, text diff, and Markdown.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests/test_text_tool_dives.py`

Expected: errors for missing `tool.py` files.

### Task 2: Shared Static Assets

**Files:**
- Create: `dives/assets/dive.css`
- Create: `dives/assets/pyodide-tools.js`

- [ ] **Step 1: Create shared CSS**

Create `dives/assets/dive.css` with layout, form, status, output, and preview styles used by all four pages. Keep it framework-free and responsive with two-column tool layouts collapsing to one column below 760px.

- [ ] **Step 2: Create shared Pyodide helper**

Create `dives/assets/pyodide-tools.js` exporting:

```js
export async function getPyodide(statusEl) {
  if (!window.__miscDivesPyodidePromise) {
    statusEl.textContent = "Loading Pyodide...";
    window.__miscDivesPyodidePromise = loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
    });
  }
  const pyodide = await window.__miscDivesPyodidePromise;
  statusEl.textContent = "Pyodide ready";
  return pyodide;
}

export function setText(el, value) {
  el.textContent = value == null ? "" : String(value);
}

export function setStatus(el, message, kind = "ready") {
  el.textContent = message;
  el.dataset.kind = kind;
}

export async function copyText(text, statusEl) {
  await navigator.clipboard.writeText(text);
  setStatus(statusEl, "Copied", "ready");
}
```

- [ ] **Step 3: Inspect assets**

Run: `sed -n '1,220p' dives/assets/dive.css` and `sed -n '1,180p' dives/assets/pyodide-tools.js`

Expected: CSS and helper file exist, use only relative/local exports except the Pyodide CDN URL.

### Task 3: Regex Tester Dive

**Files:**
- Create: `dives/regex-tester/README.md`
- Create: `dives/regex-tester/index.html`
- Create: `dives/regex-tester/tool.py`

- [ ] **Step 1: Create README**

Use the repo dive template and describe exploring Python `re` in the browser.

- [ ] **Step 2: Create page**

Build a static page with pattern, sample text, replacement, flags, run button, match summary, match JSON, substitution preview, and readable errors.

- [ ] **Step 3: Verify samples**

Run via a local static server and test:

Pattern: `(?P<word>\b\w{4}\b)`

Text: `time code test go`

Expected: three matches with named group `word`.

Invalid pattern: `(`

Expected: readable Python regex compile error.

### Task 4: JSON Pretty Printer Dive

**Files:**
- Create: `dives/json-pretty-printer/README.md`
- Create: `dives/json-pretty-printer/index.html`
- Create: `dives/json-pretty-printer/tool.py`

- [ ] **Step 1: Create README**

Use the repo dive template and describe exploring Python `json` parsing and formatting in the browser.

- [ ] **Step 2: Create page**

Build a static page with JSON input, indent selector, sort-keys checkbox, minify checkbox, format button, formatted output, and parse errors with line/column.

- [ ] **Step 3: Verify samples**

Input: `{"z":2,"a":{"b":1}}`

Expected with sort keys and indent 2:

```json
{
  "a": {
    "b": 1
  },
  "z": 2
}
```

Invalid input: `{"a":}`

Expected: readable JSON parse error.

### Task 5: Text Diff Dive

**Files:**
- Create: `dives/text-diff/README.md`
- Create: `dives/text-diff/index.html`
- Create: `dives/text-diff/tool.py`

- [ ] **Step 1: Create README**

Use the repo dive template and describe exploring Python `difflib` in the browser.

- [ ] **Step 2: Create page**

Build a static page with left text, right text, labels, diff button, unified diff output, and added/removed/context summary.

- [ ] **Step 3: Verify samples**

Left:

```text
alpha
beta
gamma
```

Right:

```text
alpha
better
gamma
delta
```

Expected: unified diff contains `-beta`, `+better`, and `+delta`.

### Task 6: Markdown To HTML Dive

**Files:**
- Create: `dives/markdown-to-html/README.md`
- Create: `dives/markdown-to-html/index.html`
- Create: `dives/markdown-to-html/tool.py`

- [ ] **Step 1: Create README**

Use the repo dive template and describe loading the real Python `markdown` package through Pyodide.

- [ ] **Step 2: Create page**

Build a static page with Markdown input, extension checkboxes for `extra` and `tables`, convert button, HTML source output, and an iframe preview using `srcdoc`.

- [ ] **Step 3: Verify samples**

Input:

```markdown
# Hello

| a | b |
| - | - |
| 1 | 2 |
```

Expected: HTML source contains `<h1>Hello</h1>` and table markup after the package loads.

### Task 7: Dive Index And Repo Check

**Files:**
- Modify: `dives/README.md`

- [ ] **Step 1: Update dive index**

Add links and one-line descriptions for the four dives.

- [ ] **Step 2: Run static checks**

Run:

```bash
python3 -m unittest tests/test_text_tool_dives.py
find dives -maxdepth 2 -type f -print
python3 -m http.server 8000
```

Expected: tests pass, all files are present, and pages can load from `http://127.0.0.1:8000/dives/<slug>/`.

- [ ] **Step 3: Commit implementation**

Run:

```bash
git add dives tests docs/superpowers/plans/2026-06-21-pyodide-text-tool-dives.md
git commit -m "feat: add pyodide text tool dives"
```
