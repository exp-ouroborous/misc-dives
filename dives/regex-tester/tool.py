import re


FLAG_MAP = {
    "ignorecase": re.IGNORECASE,
    "multiline": re.MULTILINE,
    "dotall": re.DOTALL,
    "ascii": re.ASCII,
}


def _compile_flags(flag_names):
    flags = 0
    for name in flag_names or []:
        flags |= FLAG_MAP.get(name, 0)
    return flags


def _python_replacement(replacement):
    if not replacement:
        return replacement

    def replace_token(match):
        token = match.group(1)
        if token.isdigit():
            return "\\" + token
        return "\\g<" + token + ">"

    return re.sub(r"\$([A-Za-z_][A-Za-z0-9_]*|\d+)", replace_token, replacement)


def analyze_regex(pattern, text, flags=None, replacement=""):
    try:
        compiled = re.compile(pattern, _compile_flags(flags))
    except re.error as exc:
        return {
            "ok": False,
            "error": str(exc),
            "match_count": 0,
            "matches": [],
            "substitution": "",
        }

    matches = []
    for index, match in enumerate(compiled.finditer(text), start=1):
        matches.append(
            {
                "index": index,
                "match": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "groups": match.groupdict(),
                "numbered_groups": list(match.groups()),
            }
        )

    substitution = ""
    if replacement:
        try:
            substitution = compiled.sub(_python_replacement(replacement), text)
        except re.error as exc:
            return {
                "ok": False,
                "error": "Replacement error: " + str(exc),
                "match_count": len(matches),
                "matches": matches,
                "substitution": "",
            }

    return {
        "ok": True,
        "error": "",
        "match_count": len(matches),
        "matches": matches,
        "substitution": substitution,
    }
