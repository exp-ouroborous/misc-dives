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
    """The regex page runs a regex engine in the chosen language inside the
    wasm-dives sandbox; the engines and their contract tests live there."""

    def setUp(self):
        self.page = (ROOT / "dives" / "regex-tester" / "index.html").read_text()

    def test_page_has_prominent_result_regions(self):
        self.assertIn('id="fullMatchBanner"', self.page)
        self.assertIn('id="matchList"', self.page)
        self.assertIn("renderMatchCards", self.page)
        self.assertIn("renderMatchContext", self.page)
        self.assertNotIn("match-chars", self.page)

    def test_language_picker_and_view_source(self):
        self.assertIn('id="languagePicker"', self.page)
        self.assertIn('id="viewSource"', self.page)
        self.assertIn("../wasm-assets/language-picker.mjs", self.page)
        self.assertIn("../wasm-assets/source-viewer.mjs", self.page)
        self.assertIn("../wasm-assets/tool-engine.mjs", self.page)
        self.assertIn("../wasm-assets/format.mjs", self.page)
        self.assertIn('["python", "csharp", "go", "cpp"]', self.page)

    def test_explains_where_to_run_when_the_engine_modules_are_missing(self):
        # Served straight from misc-dives.pages.dev there is no /learn/wasm-assets/.
        self.assertIn('import("../wasm-assets/', self.page)
        self.assertNotIn('from "../wasm-assets/', self.page)
        self.assertIn("https://wordsfortheunwise.com/learn/regex-tester/", self.page)

    def test_stop_cancels_a_scheduled_rerun(self):
        self.assertIn("clearTimeout(debounce);\n        engine.stop(language);", self.page)

    def test_no_in_page_python_and_no_ascii_flag(self):
        self.assertNotIn("pyodide.js", self.page)
        self.assertNotIn('id="ascii"', self.page)
        self.assertNotIn("innerHTML", self.page)
        self.assertFalse((ROOT / "dives" / "regex-tester" / "tool.py").exists())


class JsonToolTests(unittest.TestCase):
    """The JSON page runs a JSON engine in the chosen language inside the
    wasm-dives sandbox; the engines (and the heal tests) live there."""

    def setUp(self):
        self.page = (ROOT / "dives" / "json-pretty-printer" / "index.html").read_text()

    def test_language_picker_and_view_source(self):
        self.assertIn('id="languagePicker"', self.page)
        self.assertIn('id="viewSource"', self.page)
        self.assertIn('id="stop"', self.page)
        self.assertIn('engine.call(runFor, "json"', self.page)
        self.assertIn('["python", "csharp", "go", "cpp"]', self.page)

    def test_explains_where_to_run_when_the_engine_modules_are_missing(self):
        self.assertIn('import("../wasm-assets/', self.page)
        self.assertNotIn('from "../wasm-assets/', self.page)
        self.assertIn("https://wordsfortheunwise.com/learn/json-pretty-printer/", self.page)

    def test_heal_is_disabled_outside_python_never_rerouted(self):
        self.assertIn("healButton.disabled = language !== \"python\"", self.page)
        self.assertIn('id="healNote"', self.page)
        self.assertIn("only available in Python", self.page)

    def test_heal_never_overwrites_newer_edits(self):
        self.assertIn("sourceEl.value !== submitted", self.page)

    def test_stop_cancels_a_scheduled_rerun(self):
        self.assertIn("clearTimeout(debounce);\n        engine.stop(language);", self.page)

    def test_no_in_page_python_and_no_inner_html(self):
        self.assertNotIn("pyodide.js", self.page)
        self.assertNotIn("innerHTML", self.page)
        self.assertFalse((ROOT / "dives" / "json-pretty-printer" / "tool.py").exists())

    def test_json_page_has_explorer_regions(self):
        page = self.page

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

    def test_builds_side_by_side_rows(self):
        tool = load_tool("text-diff")

        result = tool.build_diff("alpha\nbeta\ngamma\n", "alpha\nbetter\ngamma\ndelta\n")

        self.assertTrue(result["ok"])
        self.assertEqual(
            result["rows"],
            [
                {"kind": "equal", "left_line": 1, "left_text": "alpha", "right_line": 1, "right_text": "alpha"},
                {"kind": "replace", "left_line": 2, "left_text": "beta", "right_line": 2, "right_text": "better"},
                {"kind": "equal", "left_line": 3, "left_text": "gamma", "right_line": 3, "right_text": "gamma"},
                {"kind": "insert", "left_line": None, "left_text": "", "right_line": 4, "right_text": "delta"},
            ],
        )

    def test_text_diff_page_has_visual_diff_region(self):
        page = (ROOT / "dives" / "text-diff" / "index.html").read_text()

        self.assertIn('id="visualDiff"', page)
        self.assertIn("renderVisualDiff", page)
        self.assertIn("formatRowsForCopy", page)
        self.assertIn("diff-cell-left", page)
        self.assertIn("diff-cell-right", page)
        self.assertNotIn('id="output"', page)
        self.assertNotIn("Unified diff", page)

    def test_text_diff_page_has_file_loaders(self):
        page = (ROOT / "dives" / "text-diff" / "index.html").read_text()

        self.assertIn('id="leftFile"', page)
        self.assertIn('id="rightFile"', page)
        self.assertIn("loadFileIntoPane", page)


class MarkdownToolTests(unittest.TestCase):
    """The Markdown page runs a Markdown library in the chosen language inside
    the wasm-dives sandbox; the engines and their contract tests live there."""

    def setUp(self):
        self.page = (ROOT / "dives" / "markdown-to-html" / "index.html").read_text()

    def test_language_picker_and_view_source(self):
        self.assertIn('id="languagePicker"', self.page)
        self.assertIn('id="viewSource"', self.page)
        self.assertIn('id="stop"', self.page)
        self.assertIn('engine.call(runFor, "markdown"', self.page)
        self.assertIn('["python", "csharp", "go", "cpp"]', self.page)

    def test_features_follow_the_shared_capability_table(self):
        # Unavailable features are disabled, never silently dropped.
        self.assertIn('import("../wasm-assets/markdown-features.mjs")', self.page)
        self.assertIn("SUPPORT[language]", self.page)
        self.assertIn('"always"', self.page)

    def test_explains_where_to_run_when_the_engine_modules_are_missing(self):
        self.assertIn('import("../wasm-assets/', self.page)
        self.assertNotIn('from "../wasm-assets/', self.page)
        self.assertIn("https://wordsfortheunwise.com/learn/markdown-to-html/", self.page)

    def test_preview_stays_in_a_script_free_sandbox(self):
        self.assertIn('<iframe id="preview" class="preview-frame" title="Markdown preview" sandbox=""></iframe>', self.page)

    def test_stop_cancels_a_scheduled_rerun(self):
        self.assertIn("clearTimeout(debounce);\n        engine.stop(language);", self.page)

    def test_no_in_page_python_or_micropip(self):
        self.assertNotIn("pyodide.js", self.page)
        self.assertNotIn("micropip", self.page)
        self.assertNotIn("innerHTML", self.page)
        self.assertFalse((ROOT / "dives" / "markdown-to-html" / "tool.py").exists())

    def test_markdown_page_has_upgrade_controls(self):
        page = self.page

        for control_id in [
            "markdownFile",
            "fencedCode",
            "footnotes",
            "toc",
            "saneLists",
            "smarty",
            "nl2br",
            "sanitize",
            "tabPreview",
            "tabHtml",
            "tabNotes",
            "copyHtml",
            "copyText",
            "copyDocument",
        ]:
            self.assertIn(f'id="{control_id}"', page)

        self.assertIn("loadMarkdownFile", page)
        self.assertIn("activateTab", page)
        self.assertIn("copyPlainText", page)
        self.assertIn("copyFullDocument", page)


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
