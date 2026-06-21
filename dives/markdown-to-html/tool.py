def build_extensions(extra=False, tables=False):
    extensions = []
    if extra:
        extensions.append("extra")
    if tables and "tables" not in extensions:
        extensions.append("tables")
    return extensions


def convert_markdown(source, extensions=None):
    try:
        import markdown
    except ImportError as exc:
        return {
            "ok": False,
            "html": "",
            "error": "The Python markdown package is not installed: " + str(exc),
        }

    try:
        html = markdown.markdown(source, extensions=extensions or [])
    except Exception as exc:
        return {
            "ok": False,
            "html": "",
            "error": str(exc),
        }

    return {
        "ok": True,
        "html": html,
        "error": "",
    }
