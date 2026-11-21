"""Tests for tools/render.py. Run with: python3 -m unittest discover tests"""
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
{x_form: Intro V1}

{start_of_verse: Intro}
# Reaper: intro
{x_bars: 4}
{x_cbg: riff}
{x_drums: kick}
{x_cue: Devis: stop}
{end_of_verse}

{start_of_verse: V1}
{x_bars: open}
[G]Testo
{end_of_verse}
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
        first_section = self.lines.index("{start_of_verse: Intro}")
        header = self.lines[:first_section]
        self.assertIn("{comment_box: Struttura: Intro V1}", header)
        self.assertTrue(any("GDG" in l and l.startswith("{comment:") for l in header))

    def test_parts_merged_in_one_line(self):
        parts = [l for l in self.lines if l.startswith("{comment_italic:")]
        self.assertEqual(len(parts), 2)
        self.assertIn("riff", parts[0])
        self.assertIn("kick", parts[0])

    def test_cue_is_boxed(self):
        self.assertTrue(any(l.startswith("{comment_box: Cue:") for l in self.lines))

    def test_hash_comments_dropped_and_lyrics_kept(self):
        self.assertNotIn("# Reaper: intro", self.lines)
        self.assertIn("[G]Testo", self.lines)


class RenderTest(ExternalCallGuard):
    def test_calls_chordpro_without_chord_grids(self):
        with tempfile.TemporaryDirectory() as tmp:
            song = Path(tmp) / "song.cho"
            song.write_text(SONG, encoding="utf-8")
            pdf = Path(tmp) / "out" / "song.pdf"

            def fake_run(cmd, check):
                pdf.write_bytes(b"%PDF")
                return subprocess.CompletedProcess(cmd, 0)

            with mock.patch.object(render.shutil, "which", return_value="/bin/chordpro"), \
                    mock.patch.object(render.subprocess, "run", side_effect=fake_run) as run:
                self.assertEqual(render.render(song, pdf), pdf)

            cmd = run.call_args.args[0]
            self.assertEqual(cmd[0], "chordpro")
            self.assertIn("--no-chord-grids", cmd)
            self.assertEqual(cmd[-2:], ["-o", str(pdf)])


if __name__ == "__main__":
    unittest.main()
