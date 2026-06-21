import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_tool(slug):
    path = ROOT / "dives" / slug / "tool.py"
    spec = importlib.util.spec_from_file_location(f"{slug.replace('-', '_')}_tool", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RegexToolTests(unittest.TestCase):
    def test_reports_named_groups_and_substitution(self):
        tool = load_tool("regex-tester")

        result = tool.analyze_regex(
            r"(?P<word>\b\w{4}\b)",
            "time code test go",
            ["ignorecase"],
            "[$word]",
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["match_count"], 3)
        self.assertEqual(result["matches"][0]["groups"]["word"], "time")
        self.assertEqual(
            result["matches"][0]["group_spans"],
            [
                {
                    "number": 1,
                    "name": "word",
                    "text": "time",
                    "start": 0,
                    "end": 4,
                    "matched": True,
                }
            ],
        )
        self.assertEqual(result["substitution"], "[time] [code] [test] go")
        self.assertFalse(result["full_match"])

    def test_reports_full_string_match(self):
        tool = load_tool("regex-tester")

        result = tool.analyze_regex(r"\w{4}", "time", [], "")

        self.assertTrue(result["ok"])
        self.assertTrue(result["full_match"])
        self.assertEqual(result["full_match_span"], [0, 4])

    def test_reports_regex_errors(self):
        tool = load_tool("regex-tester")

        result = tool.analyze_regex("(", "abc", [], "")

        self.assertFalse(result["ok"])
        self.assertIn("missing", result["error"].lower())

    def test_page_has_prominent_result_regions(self):
        page = (ROOT / "dives" / "regex-tester" / "index.html").read_text()

        self.assertIn('id="fullMatchBanner"', page)
        self.assertIn('id="matchList"', page)
        self.assertIn("renderMatchCards", page)
        self.assertIn("renderMatchContext", page)


class JsonToolTests(unittest.TestCase):
    def test_formats_with_sorting(self):
        tool = load_tool("json-pretty-printer")

        result = tool.format_json('{"z":2,"a":{"b":1}}', indent=2, sort_keys=True, minify=False)

        self.assertTrue(result["ok"])
        self.assertEqual(result["output"], '{\n  "a": {\n    "b": 1\n  },\n  "z": 2\n}')

    def test_reports_parse_location(self):
        tool = load_tool("json-pretty-printer")

        result = tool.format_json('{"a":}', indent=2, sort_keys=False, minify=False)

        self.assertFalse(result["ok"])
        self.assertEqual(result["line"], 1)
        self.assertGreater(result["column"], 0)


class TextDiffToolTests(unittest.TestCase):
    def test_builds_unified_diff_and_summary(self):
        tool = load_tool("text-diff")

        result = tool.build_diff("alpha\nbeta\ngamma\n", "alpha\nbetter\ngamma\ndelta\n")

        self.assertTrue(result["ok"])
        self.assertIn("-beta", result["diff"])
        self.assertIn("+better", result["diff"])
        self.assertIn("+delta", result["diff"])
        self.assertEqual(result["added"], 2)
        self.assertEqual(result["removed"], 1)


class MarkdownToolTests(unittest.TestCase):
    def test_builds_extensions_without_duplicates(self):
        tool = load_tool("markdown-to-html")

        self.assertEqual(tool.build_extensions(True, True), ["extra", "tables"])
        self.assertEqual(tool.build_extensions(True, False), ["extra"])
        self.assertEqual(tool.build_extensions(False, True), ["tables"])

    def test_converts_markdown_when_package_is_available(self):
        tool = load_tool("markdown-to-html")
        try:
            import markdown  # noqa: F401
        except ImportError:
            self.skipTest("Python markdown package is not installed in local CPython")

        result = tool.convert_markdown("# Hello", ["extra"])

        self.assertTrue(result["ok"])
        self.assertIn("<h1>Hello</h1>", result["html"])


class DiveIndexTests(unittest.TestCase):
    def test_dive_index_links_to_each_tool(self):
        index = (ROOT / "dives" / "README.md").read_text()

        for slug in [
            "regex-tester",
            "json-pretty-printer",
            "text-diff",
            "markdown-to-html",
        ]:
            self.assertIn(f"./{slug}/", index)


if __name__ == "__main__":
    unittest.main()
