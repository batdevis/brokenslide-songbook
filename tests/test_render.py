"""Tests for tools/render.py. Run with: python3 -m unittest discover tests"""
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import render  # noqa: E402

SONG = """\
{title: Test}
{key: G}
{tempo: 110}
{meta: tuning GDG}
{meta: slide yes}

{start_of_tab: Riff A}
G|0--3--|
{end_of_tab}

{start_of_verse: Intro}
# Reaper: intro
{x_bars: 4}
{x_times: 2}
{x_cbg: riff}
{x_drums: kick}
{x_cue: Devis: stop}
{end_of_verse}

{start_of_verse: V1}
{x_bars: open}
[G]Testo
{end_of_verse}

{start_of_chorus: label="C"}
{x_bars: 4}
[C]Ritornello
{end_of_chorus}
{start_of_grid: shape="4x4"}
| C . . . |
{end_of_grid}

{chorus: C}
{x_times: 4}

{chorus}
"""


def _no_external_process(*args, **kwargs):
    raise AssertionError(f"unstubbed external process: {args!r}")


class ExternalCallGuard(unittest.TestCase):
    """Fail any test that starts a real subprocess without stubbing it."""

    def setUp(self):
        guard = mock.patch.object(subprocess, "Popen", _no_external_process)
        guard.start()
        self.addCleanup(guard.stop)


class ConvertTest(ExternalCallGuard):
    def setUp(self):
        super().setUp()
        self.lines = render.convert(SONG).splitlines()

    def test_no_x_directives_left(self):
        self.assertFalse([l for l in self.lines if l.startswith("{x_")])

    def test_header_inserted_before_first_section(self):
        first_section = self.lines.index("{start_of_tab: Riff A}")
        header = self.lines[:first_section]
        self.assertIn("{comment_box: Form: | Intro x2 | V1 | C | C x4 | C |}", header)
        self.assertTrue(any("GDG" in l and l.startswith("{comment:") for l in header))

    def test_parts_merged_in_one_line(self):
        parts = [l for l in self.lines if l.startswith("{comment_italic:")]
        self.assertEqual(len(parts), 3)  # Intro, V1, C
        self.assertIn("riff", parts[0])
        self.assertNotIn("times", parts[0])  # x_times goes in the label
        self.assertIn("kick", parts[0])

    def test_times_added_to_labels(self):
        self.assertIn("{start_of_verse: Intro x2}", self.lines)
        self.assertIn('{start_of_chorus: label="C"}', self.lines)
        self.assertIn("{chorus: C x4}", self.lines)

    def test_recall_without_label_takes_last_chorus(self):
        self.assertEqual(self.lines[-1], "{chorus: C}")

    def test_cue_is_boxed(self):
        self.assertTrue(any(l.startswith("{comment_box: Cue:") for l in self.lines))

    def test_hash_comments_dropped_and_lyrics_kept(self):
        self.assertNotIn("# Reaper: intro", self.lines)
        self.assertIn("[G]Testo", self.lines)


class SongFormTest(ExternalCallGuard):
    def form(self, text):
        return list(render.song_form(text.splitlines()).values())

    def test_times_default_to_one(self):
        self.assertEqual(self.form("{start_of_verse: V1}\n{end_of_verse}"), ["V1"])

    def test_tabs_and_unlabeled_sections_left_out(self):
        text = "{start_of_tab: Riff}\n{end_of_tab}\n{start_of_grid: shape=\"4x4\"}\n{end_of_grid}"
        self.assertEqual(self.form(text), [])

    def test_invalid_times_rejected(self):
        for value in ("0", "due", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.form(f"{{start_of_verse: V1}}\n{{x_times: {value}}}")

    def test_times_before_any_section_rejected(self):
        with self.assertRaises(ValueError):
            self.form("{x_times: 2}")


class HtmlWorkaroundsTest(ExternalCallGuard):
    def lines(self, text):
        return render.html_workarounds(text).splitlines()

    def test_artist_repeated_as_subtitle(self):
        self.assertEqual(self.lines("{artist: Broken Slide}"),
                         ["{artist: Broken Slide}", "{subtitle: Broken Slide}"])

    def test_grid_becomes_chordgrid(self):
        self.assertEqual(
            self.lines('{start_of_grid: label="Intro" shape="4x4"}\n| G . . . |\n{end_of_grid}\n'
                       '{start_of_grid: shape="4x4"}\n{end_of_grid}'),
            ['{start_of_chordgrid: label="Intro"}', "| G . . . |", "{end_of_chordgrid}",
             "{start_of_chordgrid}", "{end_of_chordgrid}"])

    def test_tab_becomes_labeled_riff(self):
        self.assertEqual(
            self.lines("{start_of_tab: Main riff}\nG|--0--|\n{end_of_tab}\n{start_of_tab}\n{end_of_tab}"),
            ['{start_of_riff: label="Main riff"}', "G|--0--|", "{end_of_riff}",
             "{start_of_riff}", "{end_of_riff}"])

    def test_chorus_recall_becomes_labeled_section(self):
        self.assertEqual(
            self.lines("{chorus: C x4}\n{chorus}"),
            ['{start_of_chorus_recall: label="C x4"}', "{end_of_chorus_recall}",
             '{start_of_chorus_recall: label="Chorus"}', "{end_of_chorus_recall}"])

    def test_form_box_becomes_form_section(self):
        nbsp = render.NBSP
        self.assertEqual(
            self.lines("{comment_box: Form: | Intro x2 | V1 |}"),
            ['{start_of_form: label="Form:"}',
             f"| Intro{nbsp}x2{nbsp}| V1{nbsp}|", "{end_of_form}"])

    def test_comment_box_wrapped_only_outside_sections(self):
        self.assertEqual(
            self.lines("{comment_box: A}\n{start_of_verse}\n{comment_box: B}\n{end_of_verse}"),
            ["{start_of_box}", "{comment_box: A}", "{end_of_box}",
             "{start_of_verse}", "{comment_box: B}", "{end_of_verse}"])


CHORDPRO_PAGE = """\
<html>
<head>
<meta charset="utf-8">
</head>
<body>
<div class="song">
<style>
@page {
  @top-center {
      content: counter(song) ". Test";
  }
}
</style>
<div class="title">Test</div>
</div>
</body>
</html>
"""


class RenderTest(ExternalCallGuard):
    def setUp(self):
        super().setUp()
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.song = self.tmp / "song.cho"
        self.song.write_text(SONG, encoding="utf-8")
        self.out_dir = self.tmp / "out"
        self.page = self.out_dir / "html" / "song.html"
        self.pdf = self.out_dir / "pdf" / "song.pdf"
        self.installed = {"chordpro", "chromium", "google-chrome"}
        self.commands = []

    def fake_which(self, name):
        return f"/bin/{name}" if name in self.installed else None

    def fake_run(self, cmd, **kwargs):
        """Stand-in for chordpro (writes the page) and the browser (writes the PDF)."""
        self.commands.append(cmd)
        if cmd[0] == "chordpro":
            self.chordpro_input = Path(cmd[-3]).read_text(encoding="utf-8")
            Path(cmd[-1]).write_text(CHORDPRO_PAGE, encoding="utf-8")
        else:
            option = next(arg for arg in cmd if arg.startswith("--print-to-pdf="))
            Path(option.partition("=")[2]).write_bytes(b"%PDF")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    def run_render(self, fmt="pdf"):
        """Render the test song with chordpro and the browser stubbed."""
        with mock.patch.object(render.shutil, "which", side_effect=self.fake_which), \
                mock.patch.object(render.subprocess, "run", side_effect=self.fake_run):
            return render.render(self.song, self.out_dir, fmt)

    def test_html_format_only_runs_chordpro(self):
        self.assertEqual(self.run_render("html"), self.page)
        self.assertEqual(len(self.commands), 1)
        cmd = self.commands[0]
        self.assertEqual(cmd[0], "chordpro")
        self.assertIn("--no-chord-grids", cmd)
        self.assertIn("--generate=HTML", cmd)
        self.assertEqual(cmd[-2:], ["-o", str(self.page)])

    def test_pdf_is_the_printed_page(self):
        self.assertEqual(self.run_render(), self.pdf)
        browser = self.commands[-1]
        self.assertEqual(browser[0], "/bin/chromium")
        self.assertIn("--headless", browser)
        self.assertIn("--no-pdf-header-footer", browser)
        self.assertIn(f"--print-to-pdf={self.pdf}", browser)
        self.assertEqual(browser[-1], self.page.resolve().as_uri())
        self.assertTrue(self.pdf.is_file())

    def test_chrome_when_chromium_missing(self):
        self.installed.discard("chromium")
        self.run_render()
        self.assertEqual(self.commands[-1][0], "/bin/google-chrome")

    def test_no_browser_stops_with_message(self):
        self.installed -= {"chromium", "google-chrome"}
        with self.assertRaises(SystemExit):
            self.run_render()

    def test_failed_print_stops_with_message(self):
        def browser_fails(cmd, **kwargs):
            if cmd[0] == "chordpro":
                return self.fake_run(cmd)
            return subprocess.CompletedProcess(cmd, 1, "", "boom")
        with mock.patch.object(render.shutil, "which", side_effect=self.fake_which), \
                mock.patch.object(render.subprocess, "run", side_effect=browser_fails), \
                self.assertRaises(SystemExit):
            render.render(self.song, self.out_dir)

    def test_styles_copied_next_to_page(self):
        self.run_render("html")
        styles = sorted(p.name for p in render.HTML_STYLES.glob("*.css"))
        self.assertEqual(styles, ["chordpro.css", "chordpro_print.css"])
        for name in styles:
            self.assertTrue((self.page.parent / name).is_file(), name)

    def test_page_head_fixed_once(self):
        self.run_render("html")
        render.finish_html(self.page)  # a second pass must not duplicate anything
        html = self.page.read_text(encoding="utf-8")
        self.assertTrue(html.startswith(render.DOCTYPE + "\n<html>"))
        self.assertEqual(html.count(render.DOCTYPE), 1)
        self.assertEqual(html.count(render.VIEWPORT), 1)
        self.assertNotIn("counter(song)", html)
        self.assertIn('<div class="title">Test</div>', html)
        self.assertEqual(html.count(render.FOOTER_ID), 1)

    def test_footer_text_is_artist_and_title(self):
        self.assertEqual(render.footer_text("{title: El Boogie}\n{artist: Broken Slide}"),
                         "Broken Slide · El Boogie")
        self.assertEqual(render.footer_text("{title: El Boogie}"), "El Boogie")
        self.assertEqual(render.footer_text("[G]la la"), "")

    def test_footer_style_escapes_quotes(self):
        self.assertIn(r'content: "Il \"Boogie\"";', render.footer_style('Il "Boogie"'))

    def test_chordpro_input_gets_html_workarounds(self):
        self.run_render("html")
        self.assertIn("{start_of_chorus_recall:", self.chordpro_input)

    def test_main_defaults(self):
        with mock.patch.object(render, "render") as fake_render, \
                mock.patch.object(render, "write_index") as fake_index, \
                contextlib.redirect_stdout(io.StringIO()):
            render.main([str(self.song)])
        self.assertEqual(fake_render.call_args.args, (self.song, render.OUT_DIR, "pdf"))
        fake_index.assert_called_once_with(render.OUT_DIR)

    def test_folder_renders_every_song_but_templates(self):
        songs = self.tmp / "songs"
        for name in ("b/b.live.cho", "a/a.demo.cho", "a/notes.txt", "_template.cho"):
            (songs / name).parent.mkdir(parents=True, exist_ok=True)
            (songs / name).write_text(SONG, encoding="utf-8")
        with mock.patch.object(render, "render") as fake_render, \
                mock.patch.object(render, "write_index"), \
                contextlib.redirect_stdout(io.StringIO()):
            render.main([str(songs), "--format", "html"])
        rendered = [c.args[0] for c in fake_render.call_args_list]
        self.assertEqual(rendered, [songs / "a/a.demo.cho", songs / "b/b.live.cho"])

    def test_folder_without_songs_stops_with_message(self):
        empty = self.tmp / "empty"
        empty.mkdir()
        with self.assertRaises(SystemExit):
            render.song_files([empty])


class IndexTest(ExternalCallGuard):
    def setUp(self):
        super().setUp()
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.out = Path(tmp.name)
        (self.out / "html").mkdir()
        (self.out / "pdf").mkdir()

    def add_page(self, stem, title, pdf=True):
        (self.out / "html" / f"{stem}.html").write_text(
            f'<div class="song">\n<div class="title">{title}</div>\n</div>', encoding="utf-8")
        if pdf:
            (self.out / "pdf" / f"{stem}.pdf").write_bytes(b"%PDF")

    def test_versions_grouped_by_title_in_order(self):
        self.add_page("b.live", "Zeta")
        self.add_page("b.demo", "Zeta", pdf=False)
        self.add_page("a.disco", "alfa")
        songs = render.song_versions(self.out)
        self.assertEqual(list(songs), ["alfa", "Zeta"])
        self.assertEqual([(v, p.name, pdf and pdf.name) for v, p, pdf in songs["Zeta"]],
                         [("demo", "b.demo.html", None), ("live", "b.live.html", "b.live.pdf")])

    def test_index_links_pages_and_pdfs(self):
        self.add_page("song.demo", "Song")
        index = render.write_index(self.out)
        self.assertEqual(index, self.out / "index.html")
        html = index.read_text(encoding="utf-8")
        self.assertTrue(html.startswith(render.DOCTYPE))
        self.assertIn(render.VIEWPORT, html)
        self.assertIn('href="html/chordpro.css"', html)
        self.assertIn('href="html/song.demo.html"', html)
        self.assertIn('href="pdf/song.demo.pdf"', html)


if __name__ == "__main__":
    unittest.main()
