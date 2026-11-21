"""Render a BrokenSlide .cho file to PDF or HTML, keeping the x_ extensions visible.

ChordPro ignores x_ directives when printing, so the song is first converted
into plain ChordPro (x_ directives become comments), then passed to the
`chordpro` command line tool. Fonts and spacing come from tools/chordpro.json.
The HTML page loads its style sheets from tools/html/, copied next to it.

The song form (Struttura) is built from the sections themselves: every labeled
section and every chorus recall, in order, with its x_times repetitions.

Usage: python3 tools/render.py <song.cho> [--format pdf|html] [-o <out>]
Default output: out/pdf/<song>.pdf or out/html/<song>.html in the repository.
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
FORMATS = {"pdf": "PDF", "html": "HTML"}  # --format → ChordPro backend
HTML_STYLES = REPO_ROOT / "tools" / "html"  # CSS caricati dalla pagina HTML
DIRECTIVE = re.compile(r"^\{\s*([\w-]+)\s*(?::\s*(.*?))?\s*\}\s*$")
LABEL_ATTR = re.compile(r'label="([^"]*)"')

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


def parse_directive(line):
    """(name, value) of a `{name: value}` line, or (None, None)."""
    match = DIRECTIVE.match(line.strip())
    return (match.group(1), match.group(2) or "") if match else (None, None)


def section_label(value):
    """Label from a section argument: `V1` or `label="V1" shape=...`."""
    match = LABEL_ATTR.search(value)
    if match:
        return match.group(1)
    return value if value and "=" not in value else None


def parse_times(value):
    if not value.isdigit() or int(value) < 1:
        raise ValueError(f"x_times deve essere un intero >= 1, non {value!r}")
    return int(value)


def is_form_section(name):
    """Section openers and chorus recalls; tab blocks only hold riffs."""
    return name == "chorus" or (
        name.startswith("start_of_") and name != "start_of_tab")


def song_form(lines):
    """Form of the song as {line index: entry}, in playing order.

    Entries look like `Intro` or `C x2`. A section is in the form when it has
    a label; a chorus recall without label takes the label of the last
    chorus. `x_times` sets how many times the last section is played
    (default 1).
    """
    form = {}
    last = None
    last_chorus = None
    for index, line in enumerate(lines):
        name, value = parse_directive(line)
        if name and is_form_section(name):
            label = section_label(value)
            if name == "chorus":
                label = label or last_chorus
            elif name == "start_of_chorus" and label:
                last_chorus = label
            if label:
                form[index] = [label, 1]
                last = index
        elif name == "x_times":
            if last is None:
                raise ValueError("x_times prima di qualunque sezione")
            form[last][1] = parse_times(value)
    return {index: label if times == 1 else f"{label} x{times}"
            for index, (label, times) in form.items()}


def relabel(line, name, value, label):
    """Same section line, with `label` in place of its label."""
    if LABEL_ATTR.search(value):
        return LABEL_ATTR.sub(lambda _: f'label="{label}"', line, count=1)
    return f"{{{name}: {label}}}"


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
    lines = text.splitlines()
    form = song_form(lines)
    info = {"form": " ".join(form.values())} if form else {}
    out = []
    parts = []
    header_done = False

    def flush_parts():
        if parts:
            out.append(f"{{comment_italic: {' · '.join(parts)}}}")
            parts.clear()

    for index, line in enumerate(lines):
        name, value = parse_directive(line)

        if name in ("key", "tempo", "time", "duration"):
            info[name] = value
        elif name == "meta" and value:
            meta_name, _, meta_value = value.partition(" ")
            info[meta_name] = meta_value.strip()
        elif name == "x_times":
            continue  # already in the section label
        elif index in form:
            line = relabel(line, name, value, form[index])

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


def render(song, out, fmt="pdf"):
    """Convert `song` and write it to `out` in `fmt` with the chordpro CLI."""
    if shutil.which("chordpro") is None:
        sys.exit("chordpro non trovato nel PATH")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        plain = Path(tmp) / song.name
        plain.write_text(convert(song.read_text(encoding="utf-8")), encoding="utf-8")
        # No chord diagrams: the defaults are for 6-string guitar, not cigar box.
        subprocess.run(
            ["chordpro", "--config", str(CONFIG), "--no-chord-grids",
             f"--generate={FORMATS[fmt]}", str(plain), "-o", str(out)],
            check=True,
        )
    if not out.exists():
        sys.exit(f"chordpro non ha generato {out}")
    if fmt == "html":
        copy_styles(out.parent)
    return out


def copy_styles(folder):
    """The HTML page links its CSS files by name, from its own folder."""
    for css in sorted(HTML_STYLES.glob("*.css")):
        shutil.copy(css, folder / css.name)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("song", type=Path)
    parser.add_argument("-f", "--format", choices=FORMATS, default="pdf")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args(argv)
    out = args.output or REPO_ROOT / "out" / args.format / f"{args.song.stem}.{args.format}"
    print(render(args.song, out, args.format))


if __name__ == "__main__":
    main()
