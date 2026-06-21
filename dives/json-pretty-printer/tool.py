import json


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


def format_json(source, indent=2, sort_keys=False, minify=False):
    try:
        parsed = json.loads(source)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "output": "",
            "error": exc.msg,
            "line": exc.lineno,
            "column": exc.colno,
        }

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
