import difflib


def _line_number(index):
    return index + 1


def _row(kind, left_lines, right_lines, left_index=None, right_index=None):
    return {
        "kind": kind,
        "left_line": _line_number(left_index) if left_index is not None else None,
        "left_text": left_lines[left_index] if left_index is not None else "",
        "right_line": _line_number(right_index) if right_index is not None else None,
        "right_text": right_lines[right_index] if right_index is not None else "",
    }


def _side_by_side_rows(left, right):
    left_lines = left.splitlines()
    right_lines = right.splitlines()
    matcher = difflib.SequenceMatcher(a=left_lines, b=right_lines, autojunk=False)
    rows = []

    for tag, left_start, left_end, right_start, right_end in matcher.get_opcodes():
        if tag == "equal":
            for left_index, right_index in zip(range(left_start, left_end), range(right_start, right_end)):
                rows.append(_row("equal", left_lines, right_lines, left_index, right_index))
        elif tag == "delete":
            for left_index in range(left_start, left_end):
                rows.append(_row("delete", left_lines, right_lines, left_index=left_index))
        elif tag == "insert":
            for right_index in range(right_start, right_end):
                rows.append(_row("insert", left_lines, right_lines, right_index=right_index))
        elif tag == "replace":
            left_count = left_end - left_start
            right_count = right_end - right_start
            paired_count = min(left_count, right_count)
            for offset in range(paired_count):
                rows.append(_row("replace", left_lines, right_lines, left_start + offset, right_start + offset))
            for left_index in range(left_start + paired_count, left_end):
                rows.append(_row("delete", left_lines, right_lines, left_index=left_index))
            for right_index in range(right_start + paired_count, right_end):
                rows.append(_row("insert", left_lines, right_lines, right_index=right_index))

    return rows


def build_diff(left, right, from_label="left", to_label="right"):
    left_lines = left.splitlines(keepends=True)
    right_lines = right.splitlines(keepends=True)
    diff_lines = list(
        difflib.unified_diff(
            left_lines,
            right_lines,
            fromfile=from_label or "left",
            tofile=to_label or "right",
            lineterm="",
        )
    )
    diff = "\n".join(line.rstrip("\n") for line in diff_lines)
    added = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
    context = sum(1 for line in diff_lines if line.startswith(" "))

    return {
        "ok": True,
        "diff": diff,
        "added": added,
        "removed": removed,
        "context": context,
        "changed": min(added, removed),
        "rows": _side_by_side_rows(left, right),
    }
