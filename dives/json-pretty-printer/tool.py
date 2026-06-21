import json


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
