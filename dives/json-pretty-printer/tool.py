import json
import re


_BARE_KEY_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")
_BARE_VALUE_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_ .-]*")


def _json_type(value):
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, bool):
        return "boolean"
    if value is None:
        return "null"
    return "number"


def _preview(value):
    if isinstance(value, (dict, list)):
        return ""
    return json.dumps(value)


def _copy_value(value):
    return json.dumps(value, indent=2, sort_keys=True)


def _path_for_child(parent_path, key):
    if isinstance(key, int):
        return f"{parent_path}[{key}]"
    if key.isidentifier():
        return f"{parent_path}.{key}"
    return f"{parent_path}[{json.dumps(key)}]"


def _node(value, path="$", key=None, depth=1):
    kind = _json_type(value)
    node = {
        "key": key,
        "path": path,
        "type": kind,
        "preview": _preview(value),
        "copy_value": _copy_value(value),
        "count": 0,
        "children": [],
    }

    if isinstance(value, dict):
        node["count"] = len(value)
        for child_key, child_value in value.items():
            node["children"].append(_node(child_value, _path_for_child(path, child_key), child_key, depth + 1))
    elif isinstance(value, list):
        node["count"] = len(value)
        for index, child_value in enumerate(value):
            node["children"].append(_node(child_value, _path_for_child(path, index), index, depth + 1))

    return node


def _stats(node, depth=1):
    total = 1
    max_depth = depth
    for child in node["children"]:
        child_total, child_depth = _stats(child, depth + 1)
        total += child_total
        max_depth = max(max_depth, child_depth)
    return total, max_depth


def _parse_error(exc):
    return {
        "error": exc.msg,
        "line": exc.lineno,
        "column": exc.colno,
    }


def _json_error_response(exc, **extra):
    response = {
        "ok": False,
        "output": "",
        **_parse_error(exc),
    }
    response.update(extra)
    return response


def _append_missing_closers(source):
    stack = []
    in_string = False
    escaped = False

    for char in source:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            stack.append("}")
        elif char == "[":
            stack.append("]")
        elif char in "}]":
            if not stack or char != stack[-1]:
                return source, [], False
            stack.pop()

    if in_string or not stack:
        return source, [], not in_string

    closers = "".join(reversed(stack))
    return source + closers, [f"appended missing closing {closers}"], True


def _previous_significant(source, index):
    index -= 1
    while index >= 0 and source[index].isspace():
        index -= 1
    return source[index] if index >= 0 else ""


def _next_significant(source, index):
    while index < len(source) and source[index].isspace():
        index += 1
    return source[index] if index < len(source) else ""


def _quote_bare_keys(source):
    output = []
    repairs = []
    i = 0
    in_string = False
    escaped = False

    while i < len(source):
        char = source[i]
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            i += 1
            continue

        if char == '"':
            in_string = True
            output.append(char)
            i += 1
            continue

        match = _BARE_KEY_RE.match(source, i)
        if match:
            token = match.group(0)
            key_context = _previous_significant(source, i) in "{,"
            next_char = _next_significant(source, match.end())
            if key_context and next_char == ":":
                output.append(json.dumps(token))
                repairs.append(f"quoted bare key {token}")
                i = match.end()
                continue

        output.append(char)
        i += 1

    return "".join(output), repairs


def _is_json_number(token):
    try:
        value = json.loads(token)
    except json.JSONDecodeError:
        return False
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _quote_bare_values(source):
    output = []
    repairs = []
    i = 0
    in_string = False
    escaped = False

    while i < len(source):
        char = source[i]
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            i += 1
            continue

        if char == '"':
            in_string = True
            output.append(char)
            i += 1
            continue

        if char != ":":
            output.append(char)
            i += 1
            continue

        output.append(char)
        i += 1
        value_start = i
        while i < len(source) and source[i].isspace():
            i += 1
        token_start = i
        while i < len(source) and source[i] not in ",}]":
            i += 1
        token_end = i

        raw_value = source[value_start:token_end]
        token = source[token_start:token_end].strip()
        leading = source[value_start:token_start]
        trailing_count = len(source[token_start:token_end]) - len(source[token_start:token_end].rstrip())
        trailing = source[token_end - trailing_count:token_end] if trailing_count else ""

        if token and _BARE_VALUE_RE.fullmatch(token) and token not in {"true", "false", "null"} and not _is_json_number(token):
            output.append(leading)
            output.append(json.dumps(token))
            output.append(trailing)
            repairs.append(f"quoted bare string value {token}")
        else:
            output.append(raw_value)

    return "".join(output), repairs


def format_json(source, indent=2, sort_keys=False, minify=False):
    try:
        parsed = json.loads(source)
    except json.JSONDecodeError as exc:
        return _json_error_response(exc)

    if minify:
        output = json.dumps(parsed, sort_keys=sort_keys, separators=(",", ":"))
    else:
        output = json.dumps(parsed, indent=int(indent), sort_keys=sort_keys)

    return {
        "ok": True,
        "output": output,
        "error": "",
        "line": None,
        "column": None,
    }


def heal_json(source, indent=2, sort_keys=True):
    repairs = []
    try:
        parsed = json.loads(source)
    except json.JSONDecodeError as original_error:
        repaired, closer_repairs, balanced = _append_missing_closers(source)
        if not balanced:
            return _json_error_response(original_error, repairs=[], repaired=False)
        repairs.extend(closer_repairs)

        repaired, key_repairs = _quote_bare_keys(repaired)
        repairs.extend(key_repairs)

        repaired, value_repairs = _quote_bare_values(repaired)
        repairs.extend(value_repairs)

        try:
            parsed = json.loads(repaired)
        except json.JSONDecodeError as repaired_error:
            return _json_error_response(repaired_error, repairs=[], repaired=False)
    else:
        repaired = source

    return {
        "ok": True,
        "output": json.dumps(parsed, indent=int(indent), sort_keys=sort_keys),
        "error": "",
        "line": None,
        "column": None,
        "repairs": repairs,
        "repaired": bool(repairs),
    }


def analyze_json(source):
    try:
        parsed = json.loads(source)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "tree": None,
            "summary": {},
            "error": exc.msg,
            "line": exc.lineno,
            "column": exc.colno,
        }

    tree = _node(parsed)
    total_nodes, max_depth = _stats(tree)
    return {
        "ok": True,
        "tree": tree,
        "summary": {
            "root_type": tree["type"],
            "total_nodes": total_nodes,
            "max_depth": max_depth,
            "root_count": tree["count"],
        },
        "error": "",
        "line": None,
        "column": None,
    }
