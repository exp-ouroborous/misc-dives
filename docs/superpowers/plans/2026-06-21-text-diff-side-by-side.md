# Text Diff Side-by-Side Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a side-by-side visual diff and local file loading to the Text Diff dive.

**Architecture:** Keep `difflib` as the comparison engine. Extend `dives/text-diff/tool.py` to return structured side-by-side rows alongside the existing unified diff, then render those rows in `dives/text-diff/index.html` with DOM APIs. File loading stays in browser JavaScript using `File.text()`.

**Tech Stack:** Static HTML/CSS, Pyodide, Python `difflib`, existing `unittest` scaffold.

---

### Task 1: Structured Diff Rows

**Files:**
- Modify: `dives/text-diff/tool.py`
- Modify: `tests/test_text_tool_dives.py`

- [ ] **Step 1: Write failing tests**

Add tests under `TextDiffToolTests`:

```python
def test_builds_side_by_side_rows(self):
    tool = load_tool("text-diff")

    result = tool.build_diff("alpha\nbeta\ngamma\n", "alpha\nbetter\ngamma\ndelta\n")

    self.assertTrue(result["ok"])
    self.assertEqual(
        result["rows"],
        [
            {"kind": "equal", "left_line": 1, "left_text": "alpha", "right_line": 1, "right_text": "alpha"},
            {"kind": "replace", "left_line": 2, "left_text": "beta", "right_line": 2, "right_text": "better"},
            {"kind": "equal", "left_line": 3, "left_text": "gamma", "right_line": 3, "right_text": "gamma"},
            {"kind": "insert", "left_line": None, "left_text": "", "right_line": 4, "right_text": "delta"},
        ],
    )
```

- [ ] **Step 2: Run the focused tests and verify failure**

Run: `python3 -m unittest tests.test_text_tool_dives.TextDiffToolTests`

Expected: failure because `rows` is not returned.

- [ ] **Step 3: Implement structured rows**

Use `difflib.SequenceMatcher` over `splitlines()` without line endings. Return row dictionaries with `kind`, `left_line`, `left_text`, `right_line`, and `right_text`. For `replace`, pair changed lines by index and emit extra `delete` or `insert` rows if one side has more lines.

- [ ] **Step 4: Run full tests**

Run: `python3 -m unittest tests/test_text_tool_dives.py`

Expected: all tests pass, with the existing markdown package skip if local CPython lacks it.

### Task 2: Side-by-Side Rendering

**Files:**
- Modify: `dives/text-diff/index.html`
- Modify: `dives/assets/dive.css`
- Modify: `tests/test_text_tool_dives.py`

- [ ] **Step 1: Write failing page contract tests**

Extend the Text Diff page test to assert the page contains:

```python
self.assertIn('id="visualDiff"', page)
self.assertIn("renderVisualDiff", page)
self.assertIn("diff-cell-left", page)
self.assertIn("diff-cell-right", page)
```

- [ ] **Step 2: Run the focused tests and verify failure**

Run: `python3 -m unittest tests.test_text_tool_dives.TextDiffToolTests`

Expected: failure because the page has no visual diff region.

- [ ] **Step 3: Add visual diff markup and renderer**

Add a `#visualDiff` container above the raw `<pre id="output">`. In `run()`, call `renderVisualDiff(result.rows)`. Render each row as a grid with left line number, left text, right line number, right text, and a `data-kind` attribute.

- [ ] **Step 4: Add CSS**

Add styles for `.visual-diff`, `.diff-row`, `.diff-line-number`, `.diff-cell-left`, `.diff-cell-right`, and row states for `equal`, `delete`, `insert`, and `replace`.

- [ ] **Step 5: Run full tests**

Run: `python3 -m unittest tests/test_text_tool_dives.py`

Expected: all tests pass.

### Task 3: Local File Loading

**Files:**
- Modify: `dives/text-diff/index.html`
- Modify: `tests/test_text_tool_dives.py`

- [ ] **Step 1: Write failing page contract tests**

Extend the Text Diff page test to assert the page contains:

```python
self.assertIn('id="leftFile"', page)
self.assertIn('id="rightFile"', page)
self.assertIn("loadFileIntoPane", page)
```

- [ ] **Step 2: Run focused tests and verify failure**

Run: `python3 -m unittest tests.test_text_tool_dives.TextDiffToolTests`

Expected: failure because file inputs are absent.

- [ ] **Step 3: Add file inputs**

Add one hidden or compact `<input type="file">` per pane and visible secondary buttons/labels in each panel header. On selection, read the file via `await file.text()`, update the relevant textarea, set the relevant label input value to `file.name`, and set the status to a ready state. On read error, set status to error and leave the textarea unchanged.

- [ ] **Step 4: Browser verify**

Use Playwright against `http://127.0.0.1:8000/dives/text-diff/` to load two temporary text files, click `Build diff`, and confirm the visual diff contains changed rows.

- [ ] **Step 5: Run full tests and commit**

Run: `python3 -m unittest tests/test_text_tool_dives.py`

Commit message: `feat: add side-by-side text diff`
