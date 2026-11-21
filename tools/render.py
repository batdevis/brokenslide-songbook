"""Render a BrokenSlide .cho file to PDF, keeping the x_ extensions visible.

ChordPro ignores x_ directives when printing, so the song is first converted
into plain ChordPro (x_ directives become comments), then passed to the
`chordpro` command line tool. Fonts and spacing come from tools/chordpro.json.

Usage: python3 tools/render.py <song.cho> [-o <out.pdf>]
Default output: pdf/<song>.pdf in the repository.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG = REPO_ROOT / "tools" / "chordpro.json"  # font e spazi del PDF
DIRECTIVE = re.compile(r"^\{\s*([\w-]+)\s*(?::\s*(.*?))?\s*\}\s*$")

PART_LABELS = {
    "x_vox": "Vocals",
    "x_cbg": "CBG",
    "x_gtr": "Guitars",
    "x_bass": "Bass",
    "x_synth": "Synth",
    "x_drums": "Drums",
    "x_bv": "Backing vocals",
    "x_riff": "Riff",
    "x_dyn": "Dynamics",
}


SLIDE_TEXT = {"yes": "con slide", "no": "senza slide", "mixed": "slide in parte"}


def bars_text(value):
    return "open" if value == "open" else f"{value} bars"


def header_lines(info):
    """Summary printed once, before the first section."""
    first = [
        f"Tonalità {info['key']}" if "key" in info else None,
        f"{info['tempo']} BPM" if "tempo" in info else None,
        info.get("time"),
        info.get("duration"),
    ]
    second = [
        f"Accordatura {info['tuning']}" if "tuning" in info else None,
        SLIDE_TEXT.get(info.get("slide"), info.get("slide")),
        f"versione {info['version']}" if "version" in info else None,
    ]
    lines = []
    for parts in (first, second):
        text = " · ".join(p for p in parts if p)
        if text:
            lines.append(f"{{comment: {text}}}")
    if "form" in info:
        lines.append(f"{{comment_box: Struttura: {info['form']}}}")
    return lines


def part_text(name, value):
    """Short text for an x_ directive that describes the section."""
    if name == "x_bars":
        return bars_text(value)
    label = PART_LABELS.get(name, name[2:])
    return f"{label}: {value}"


def convert(text):
    """Turn BrokenSlide ChordPro (with x_ extensions) into plain ChordPro.

    Consecutive x_ directives inside a section are merged into one compact
    italic line; cues get their own boxed line so they stand out.
    """
    info = {}
    out = []
    parts = []
    header_done = False

    def flush_parts():
        if parts:
            out.append(f"{{comment_italic: {' · '.join(parts)}}}")
            parts.clear()

    for line in text.splitlines():
        match = DIRECTIVE.match(line.strip())
        name, value = (match.group(1), match.group(2) or "") if match else (None, None)

        if name in ("key", "tempo", "time", "duration"):
            info[name] = value
        elif name == "meta" and value:
            meta_name, _, meta_value = value.partition(" ")
            info[meta_name] = meta_value.strip()
        elif name == "x_form":
            info["form"] = value
            continue

        if name and name.startswith("start_of_") and not header_done:
            out.extend(header_lines(info))
            out.append("")
            header_done = True

        if name == "x_cue":
            flush_parts()
            out.append(f"{{comment_box: Cue: {value}}}")
        elif name and name.startswith("x_"):
            parts.append(part_text(name, value))
        elif line.lstrip().startswith("#"):
            continue  # ChordPro comment: never printed, keep parts together
        else:
            flush_parts()
            out.append(line)

    flush_parts()
    if not header_done:
        out.extend(header_lines(info))
    return "\n".join(out) + "\n"


def render(song, pdf):
    """Convert `song` and print it to `pdf` with the chordpro CLI."""
    if shutil.which("chordpro") is None:
        sys.exit("chordpro non trovato nel PATH")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        plain = Path(tmp) / song.name
        plain.write_text(convert(song.read_text(encoding="utf-8")), encoding="utf-8")
        # No chord diagrams: the defaults are for 6-string guitar, not cigar box.
        subprocess.run(
            ["chordpro", "--config", str(CONFIG), "--no-chord-grids", str(plain),
             "-o", str(pdf)],
            check=True,
        )
    if not pdf.exists():
        sys.exit(f"chordpro non ha generato {pdf}")
    return pdf


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("song", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args(argv)
    pdf = args.output or REPO_ROOT / "pdf" / f"{args.song.stem}.pdf"
    print(render(args.song, pdf))


if __name__ == "__main__":
    main()
