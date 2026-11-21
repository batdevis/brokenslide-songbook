"""Render a BrokenSlide .cho file to HTML and PDF, keeping the x_ extensions visible.

ChordPro ignores x_ directives, so the song is first converted into plain
ChordPro (x_ directives become comments), then passed to the `chordpro`
command line tool, which writes an HTML page. ChordPro's HTML backend drops
chord grids, chorus recalls and boxed comments outside sections, so those
become custom sections first (see html_workarounds). The page loads its style
sheets from tools/html/, copied next to it, and gets a doctype and a viewport
meta tag so phones and tablets show it at their own width.

The PDF is the page printed by a headless browser (Chromium, or Chrome as a
fallback), so it follows tools/html/chordpro_print.css.

The song form is built from the sections themselves: every labeled
section and every chorus recall, in order, with its x_times repetitions.

Usage: python3 tools/render.py <song.cho|folder>... [--format pdf|html] [--out-dir <dir>]
A folder means every .cho file inside it, subfolders included (e.g. songs/);
files starting with "_" (templates) are skipped.
Output: <dir>/html/<song>.html, plus <dir>/pdf/<song>.pdf unless --format html.
Default <dir>: out/ in the repository, the same for every song.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "out"
FORMATS = ("pdf", "html")
BROWSERS = ("chromium", "chromium-browser", "google-chrome")  # in order of preference
HTML_STYLES = REPO_ROOT / "tools" / "html"  # CSS caricati dalla pagina HTML
DIRECTIVE = re.compile(r"^\{\s*([\w-]+)\s*(?::\s*(.*?))?\s*\}\s*$")
LABEL_ATTR = re.compile(r'label="([^"]*)"')
FORM_TITLE = "Form:"
NBSP = "\u00a0"
DOCTYPE = "<!DOCTYPE html>"
CHARSET = '<meta charset="utf-8">'
FOOTER_ID = "page-footer"
CHORDPRO_PAGE_STYLE = re.compile(r"<style>\s*@page\b.*?</style>\n?", re.DOTALL)
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'

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


SLIDE_TEXT = {"yes": "slide", "no": "no slide", "mixed": "partial slide"}


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


def form_line(entries):
    """Song form written like a grid row: `| Intro x2 | V1 | C x4 |`."""
    return "| " + " | ".join(entries) + " |"


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
        f"Key {info['key']}" if "key" in info else None,
        f"{info['tempo']} BPM" if "tempo" in info else None,
        info.get("time"),
        info.get("duration"),
    ]
    second = [
        f"Tuning {info['tuning']}" if "tuning" in info else None,
        SLIDE_TEXT.get(info.get("slide"), info.get("slide")),
        f"{info['version']} version" if "version" in info else None,
    ]
    lines = []
    for parts in (first, second):
        text = " · ".join(p for p in parts if p)
        if text:
            lines.append(f"{{comment: {text}}}")
    if "form" in info:
        lines.append(f"{{comment_box: {FORM_TITLE} {info['form']}}}")
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
    info = {"form": form_line(form.values())} if form else {}
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


def html_workarounds(text):
    """Rewrite plain ChordPro so the HTML backend keeps what it would drop.

    The artist, which the backend ignores, is repeated as a subtitle.
    Custom sections become `<div class="name">` in the page:
    - grids → `chordgrid` (label only), whose bar lines are printed as text;
    - tabs → `riff`, so the riff name is printed (the backend drops it);
    - chorus recalls → an empty `chorus_recall` with the chorus label;
    - the Form box → a `form` section with the form as a text line,
      breakable only after a bar so a section name is never split;
    - other boxed comments outside sections → a `box` section.
    """
    out = []
    depth = 0
    for line in text.splitlines():
        name, value = parse_directive(line)
        if name == "artist" and value:
            out += [line, f"{{subtitle: {value}}}"]
            continue
        if name == "start_of_grid":
            # Custom sections take only a label: `shape` would void it.
            label = section_label(value)
            line = f'{{start_of_chordgrid: label="{label}"}}' if label else "{start_of_chordgrid}"
        elif name == "end_of_grid":
            line = "{end_of_chordgrid}"
        elif name == "start_of_tab":
            label = section_label(value)
            line = f'{{start_of_riff: label="{label}"}}' if label else "{start_of_riff}"
        elif name == "end_of_tab":
            line = "{end_of_riff}"
        if name == "chorus":
            label = section_label(value) or "Chorus"
            out += [f'{{start_of_chorus_recall: label="{label}"}}',
                    "{end_of_chorus_recall}"]
            continue
        if name == "comment_box" and depth == 0 and value.startswith(FORM_TITLE):
            bars = value[len(FORM_TITLE):].strip()
            bars = bars.replace(" ", NBSP).replace(f"|{NBSP}", "| ")
            out += [f'{{start_of_form: label="{FORM_TITLE}"}}', bars, "{end_of_form}"]
            continue
        if name == "comment_box" and depth == 0:
            out += ["{start_of_box}", line, "{end_of_box}"]
            continue
        if name and name.startswith("start_of_"):
            depth += 1
        elif name and name.startswith("end_of_"):
            depth -= 1
        out.append(line)
    return "\n".join(out) + "\n"


def render(song, out_dir=OUT_DIR, fmt="pdf"):
    """Write the HTML page of `song` and, for "pdf", print it; return the last file."""
    page = render_html(song, out_dir / "html" / f"{song.stem}.html")
    if fmt == "html":
        return page
    return print_pdf(page, out_dir / "pdf" / f"{song.stem}.pdf")


def render_html(song, page):
    """Convert `song` and write its HTML page with the chordpro CLI."""
    if shutil.which("chordpro") is None:
        sys.exit("chordpro non trovato nel PATH")
    page.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        plain = Path(tmp) / song.name
        text = html_workarounds(convert(song.read_text(encoding="utf-8")))
        plain.write_text(text, encoding="utf-8")
        # No chord diagrams: the defaults are for 6-string guitar, not cigar box.
        subprocess.run(
            ["chordpro", "--no-chord-grids", "--generate=HTML", str(plain), "-o", str(page)],
            check=True,
        )
    if not page.exists():
        sys.exit(f"chordpro non ha generato {page}")
    finish_html(page, footer_text(song.read_text(encoding="utf-8")))
    copy_styles(page.parent)
    return page


def find_browser():
    for name in BROWSERS:
        path = shutil.which(name)
        if path:
            return path
    sys.exit(f"nessun browser per la stampa del PDF: installa uno tra {', '.join(BROWSERS)}")


def print_pdf(page, pdf):
    """Print `page` to `pdf` with a headless browser and a throwaway profile.

    The Chromium snap cannot read /tmp or hidden folders of the home, so the
    page and the PDF must stay in ordinary folders (like out/).
    """
    pdf.parent.mkdir(parents=True, exist_ok=True)
    pdf.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        result = subprocess.run(
            [find_browser(), "--headless", "--disable-gpu", f"--user-data-dir={profile}",
             "--no-pdf-header-footer", f"--print-to-pdf={pdf}", page.resolve().as_uri()],
            capture_output=True, text=True,
        )
    if result.returncode != 0 or not pdf.exists():
        sys.exit(f"stampa del PDF non riuscita:\n{result.stderr}")
    return pdf


def footer_text(text):
    """`Artist · Title` of a song, for the footer of every printed page."""
    found = {}
    for line in text.splitlines():
        name, value = parse_directive(line)
        if name in ("title", "artist") and value:
            found.setdefault(name, value)
    return " · ".join(found[key] for key in ("artist", "title") if key in found)


def footer_style(footer):
    """@page rule with the footer text; its look is in chordpro_print.css."""
    text = footer.replace("\\", "\\\\").replace('"', '\\"')
    return f'<style id="{FOOTER_ID}">@page {{ @bottom-left {{ content: "{text}"; }} }}</style>'


def finish_html(page, footer=""):
    """Add what ChordPro leaves out of the page head.

    Without the doctype the browser falls back to quirks mode; without the
    viewport, mobile browsers lay the page out ~980px wide and shrink it.
    ChordPro's own @page style (a numbered title on top of every page) is
    dropped: the header and footer of printed pages come from
    chordpro_print.css, plus the `footer` text (artist and title) added here,
    since browsers cannot take it from the page itself.
    """
    html = page.read_text(encoding="utf-8")
    html = CHORDPRO_PAGE_STYLE.sub("", html)
    if not html.startswith(DOCTYPE):
        html = f"{DOCTYPE}\n{html}"
    if VIEWPORT not in html:
        html = html.replace(CHARSET, f"{CHARSET}\n{VIEWPORT}", 1)
    if footer and FOOTER_ID not in html:
        html = html.replace("</head>", f"{footer_style(footer)}\n</head>", 1)
    page.write_text(html, encoding="utf-8")


def copy_styles(folder):
    """The HTML page links its CSS files by name, from its own folder."""
    for css in sorted(HTML_STYLES.glob("*.css")):
        shutil.copy(css, folder / css.name)


def song_files(paths):
    """The .cho files named in `paths`: files as they are, folders searched."""
    songs = []
    for path in paths:
        if path.is_dir():
            songs += sorted(p for p in path.rglob("*.cho") if not p.name.startswith("_"))
        else:
            songs.append(path)
    if not songs:
        sys.exit(f"nessun file .cho in {', '.join(map(str, paths))}")
    return songs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("songs", type=Path, nargs="+", metavar="song.cho|folder")
    parser.add_argument("-f", "--format", choices=FORMATS, default="pdf",
                        help="html: only the page, without printing the PDF")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args(argv)
    for song in song_files(args.songs):
        print(render(song, args.out_dir, args.format))


if __name__ == "__main__":
    main()
