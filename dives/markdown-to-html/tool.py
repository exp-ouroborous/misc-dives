def build_extensions(
    extra=False,
    tables=False,
    fenced_code=False,
    footnotes=False,
    toc=False,
    sane_lists=False,
    smarty=False,
    nl2br=False,
):
    extension_options = [
        (extra, "extra"),
        (tables, "tables"),
        (fenced_code, "fenced_code"),
        (footnotes, "footnotes"),
        (toc, "toc"),
        (sane_lists, "sane_lists"),
        (smarty, "smarty"),
        (nl2br, "nl2br"),
    ]
    extensions = []
    for enabled, name in extension_options:
        if enabled and name not in extensions:
            extensions.append(name)
    return extensions


def _sanitize_html(html):
    try:
        import bleach
    except ImportError as exc:
        return None, "The Python bleach package is not installed: " + str(exc)

    allowed_tags = set(bleach.sanitizer.ALLOWED_TAGS).union(
        {
            "abbr",
            "blockquote",
            "br",
            "code",
            "dd",
            "div",
            "dl",
            "dt",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "hr",
            "img",
            "li",
            "ol",
            "p",
            "pre",
            "span",
            "sup",
            "table",
            "tbody",
            "td",
            "tfoot",
            "th",
            "thead",
            "tr",
            "ul",
        }
    )
    allowed_attributes = {
        **bleach.sanitizer.ALLOWED_ATTRIBUTES,
        "*": ["class", "id", "title"],
        "a": ["href", "title", "rel"],
        "img": ["alt", "src", "title"],
        "td": ["align"],
        "th": ["align"],
    }
    cleaned = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=["http", "https", "mailto"],
        strip=True,
    )
    return cleaned, ""


def convert_markdown(source, extensions=None, sanitize=False):
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

    sanitized = False
    if sanitize:
        html, error = _sanitize_html(html)
        if error:
            return {
                "ok": False,
                "html": "",
                "error": error,
                "sanitized": False,
            }
        sanitized = True

    return {
        "ok": True,
        "html": html,
        "error": "",
        "sanitized": sanitized,
    }
