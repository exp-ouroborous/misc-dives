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
        self.assertNotIn("match-chars", page)


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

    def test_formats_jsonc_when_enabled(self):
        tool = load_tool("json-pretty-printer")
        source = """
        {
          // user-facing label
          "name": "Ada",
          "skills": [
            "math",
          ],
          /* keep boolean values intact */
          "active": true,
        }
        """

        result = tool.format_json(source, indent=2, sort_keys=True, minify=False, allow_jsonc=True)
        analysis = tool.analyze_json(source, allow_jsonc=True)

        self.assertTrue(result["ok"])
        self.assertEqual(result["output"], '{\n  "active": true,\n  "name": "Ada",\n  "skills": [\n    "math"\n  ]\n}')
        self.assertTrue(analysis["ok"])
        self.assertEqual(analysis["summary"]["root_type"], "object")

    def test_analyzes_tree_paths_for_explorer(self):
        tool = load_tool("json-pretty-printer")

        result = tool.analyze_json('{"users":[{"name":"Ada","active":true}],"count":1}')

        self.assertTrue(result["ok"])
        self.assertEqual(result["summary"]["root_type"], "object")
        self.assertEqual(result["summary"]["total_nodes"], 6)
        self.assertEqual(result["summary"]["max_depth"], 4)
        self.assertEqual(result["tree"]["path"], "$")
        self.assertEqual(result["tree"]["children"][0]["path"], "$.users")
        self.assertEqual(result["tree"]["children"][0]["children"][0]["path"], "$.users[0]")
        self.assertEqual(result["tree"]["children"][0]["children"][0]["children"][0]["path"], "$.users[0].name")
        self.assertEqual(result["tree"]["children"][0]["children"][0]["children"][0]["preview"], '"Ada"')

    def test_heals_missing_quotes_and_closing_brace(self):
        tool = load_tool("json-pretty-printer")

        result = tool.heal_json("{name:Ada, active:true")

        self.assertTrue(result["ok"])
        self.assertTrue(result["repaired"])
        self.assertEqual(result["output"], '{\n  "active": true,\n  "name": "Ada"\n}')
        self.assertIn("quoted bare key", " ".join(result["repairs"]))
        self.assertIn("quoted bare string value", " ".join(result["repairs"]))
        self.assertIn("appended missing closing", " ".join(result["repairs"]))

    def test_heals_missing_comma_between_object_members(self):
        tool = load_tool("json-pretty-printer")

        result = tool.heal_json('{"name":"Ada" "active":true}')

        self.assertTrue(result["ok"])
        self.assertEqual(result["output"], '{\n  "active": true,\n  "name": "Ada"\n}')
        self.assertIn("inserted missing comma", " ".join(result["repairs"]))
        self.assertEqual(result["repaired_source"], '{"name":"Ada", "active":true}')
        self.assertIn({"text": ",", "added": True}, result["diff_segments"])

    def test_heals_missing_string_end_quote_before_next_key(self):
        tool = load_tool("json-pretty-printer")

        result = tool.heal_json('{"name":"Ada "active":true}')

        self.assertTrue(result["ok"])
        self.assertEqual(result["output"], '{\n  "active": true,\n  "name": "Ada"\n}')
        self.assertIn("closed unterminated string value", " ".join(result["repairs"]))
        self.assertEqual(result["repaired_source"], '{"name":"Ada", "active":true}')
        self.assertTrue(any(segment["added"] and '"' in segment["text"] for segment in result["diff_segments"]))
        self.assertTrue(any(segment["added"] and "," in segment["text"] for segment in result["diff_segments"]))

    def test_heal_rejects_unfixable_json(self):
        tool = load_tool("json-pretty-printer")

        result = tool.heal_json("{name:}")

        self.assertFalse(result["ok"])
        self.assertFalse(result["repaired"])
        self.assertIn("Expecting value", result["error"])

    def test_json_page_has_explorer_regions(self):
        page = (ROOT / "dives" / "json-pretty-printer" / "index.html").read_text()

        self.assertIn('id="jsonBanner"', page)
        self.assertIn('id="jsonTree"', page)
        self.assertIn('id="heal"', page)
        self.assertIn('id="allowJsonc"', page)
        self.assertIn("healJson", page)
        self.assertIn("allow_jsonc", page)
        self.assertIn('id="healedPreview"', page)
        self.assertIn("renderHealedPreview", page)
        self.assertIn("json-added", page)
        self.assertIn("renderJsonTree", page)
        self.assertIn("copy-node", page)
        self.assertLess(page.index('id="output"'), page.index('id="jsonTree"'))
        self.assertIn('"Copy path"', page)
        self.assertIn('"Copy value"', page)
        self.assertIn("pathIconSvg", page)
        self.assertIn("copyIconSvg", page)
        self.assertIn("copy-tooltip", page)
        self.assertIn("copy-tooltip-below", page)
        self.assertNotIn("Copy Path", page)
        self.assertNotIn("Copy Value", page)


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
