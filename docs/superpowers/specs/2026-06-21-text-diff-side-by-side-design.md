# Text Diff Side-by-Side Design

## Goal

Make the Text Diff dive easier to read than a raw unified diff while keeping the tool small, static, and Pyodide-driven.

## Scope

Add two user-facing improvements to `dives/text-diff/`:

- A side-by-side visual diff rendered above the raw unified diff.
- Browser-local file loading for the left and right inputs.

The raw unified diff remains available for copy/paste and debugging.

## User Experience

The existing left and right textareas remain editable. Each pane gets a file-load control in its header. When a user selects a file, the browser reads it locally, replaces that pane's textarea value, and updates the side label to the filename. No file contents leave the browser.

After the user builds a diff, the result area shows:

- Summary metrics for added, removed, and changed lines.
- A side-by-side table/grid with left and right line numbers.
- Removed lines highlighted light red on the left.
- Added lines highlighted light green on the right.
- Replaced lines shown as paired red/green rows when possible.
- Unchanged context rows in a neutral style.
- The raw unified diff below the visual view for copy/export.

On narrow screens, the side-by-side diff can scroll horizontally rather than collapsing into a less aligned layout.

## Data Flow

`tool.py` continues to use Python `difflib`. `build_diff` will return the current unified diff fields plus a new structured row list. Each row describes:

- Left line number and text, when present.
- Right line number and text, when present.
- A row kind such as `equal`, `delete`, `insert`, or `replace`.

The browser renders those rows with DOM APIs rather than injecting HTML strings.

## Error Handling

File loading errors should set the status badge to an error state and leave the existing textarea content untouched. Empty files are allowed.

Diff generation should continue to show `No differences.` in the raw output when there are no changes and should render an empty/neutral visual state.

## Testing

Extend `tests/test_text_tool_dives.py` to cover:

- Structured diff rows for equal, deleted, inserted, and replaced lines.
- The Text Diff page exposing left/right file inputs.
- The Text Diff page rendering a side-by-side diff region.

Existing tests for unified diff output and metrics should keep passing.
