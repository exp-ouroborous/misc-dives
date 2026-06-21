import difflib


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
    }
