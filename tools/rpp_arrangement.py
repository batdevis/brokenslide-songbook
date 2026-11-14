"""Read a Reaper .RPP and print, for each region (marker pair), which tracks have unmuted items.

Usage: python3 -I rpp_arrangement.py <project.RPP>
"""
import re
import sys

MIN_OVERLAP_BEATS = 1  # ignore overlaps shorter than one beat
SILENT = 0.05  # envelope gain below this counts as silence
STEP = 0.05  # sampling step (seconds) for coverage


def envelope_gain(points, t):
    """Gain of a Reaper envelope at time t (square shape = 1 holds, others linear)."""
    if not points:
        return 1.0
    if t <= points[0][0]:
        return points[0][1]
    for (t0, v0, shape), (t1, v1, _) in zip(points, points[1:]):
        if t0 <= t < t1:
            if shape == 1 or t1 == t0:
                return v0
            return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return points[-1][1]


def parse(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    tempo = 120.0
    regions = {}
    tracks = []
    stack = []
    track = item = None
    for raw in lines:
        line = raw.strip()
        if line.startswith("TEMPO ") and not stack[1:]:
            tempo = float(line.split()[1])
        if line.startswith("MARKER "):
            parts = re.findall(r'"[^"]*"|\S+', line)
            idx, pos, name = parts[1], float(parts[2]), parts[3].strip('"')
            if name:
                regions[idx] = [name, pos, None]
            elif idx in regions:
                regions[idx][2] = pos
        if line.startswith("<"):
            tag = line[1:].split()[0]
            stack.append(tag)
            if tag == "TRACK":
                track = {"name": "", "muted": False, "items": [], "envs": []}
                tracks.append(track)
            elif tag == "ITEM":
                item = {"pos": 0.0, "len": 0.0, "muted": False}
            elif tag in ("VOLENV", "VOLENV2") and stack[-2:-1] == ["TRACK"]:
                track["envs"].append({"active": True, "points": []})
            continue
        if line == ">":
            tag = stack.pop() if stack else None
            if tag == "ITEM" and track is not None:
                track["items"].append(item)
                item = None
            continue
        top = stack[-1] if stack else None
        if top in ("VOLENV", "VOLENV2") and stack[-2:-1] == ["TRACK"]:
            env = track["envs"][-1]
            if line.startswith("ACT "):
                env["active"] = line.split()[1] == "1"
            elif line.startswith("PT "):
                p = line.split()
                shape = int(p[3]) if len(p) > 3 else 0
                env["points"].append((float(p[1]), float(p[2]), shape))
            continue
        if top == "TRACK" and track is not None:
            if line.startswith("NAME "):
                track["name"] = line[5:].strip().strip('"')
            elif line.startswith("MUTESOLO "):
                track["muted"] = line.split()[1] == "1"
        elif top == "ITEM" and item is not None:
            if line.startswith("POSITION "):
                item["pos"] = float(line.split()[1])
            elif line.startswith("LENGTH "):
                item["len"] = float(line.split()[1])
            elif line.startswith("MUTE "):
                item["muted"] = line.split()[1] == "1"
    ordered = sorted(regions.values(), key=lambda r: r[1])
    return tempo, ordered, tracks


def main(path):
    tempo, regions, tracks = parse(path)
    beat = 60.0 / tempo
    print(f"tempo {tempo}")
    print("muted tracks:", [t["name"] for t in tracks if t["muted"]])
    for name, start, end in regions:
        playing = []
        for t in tracks:
            if t["muted"] or t["name"] == "lyrics":
                continue
            items = [i for i in t["items"] if not i["muted"]]
            envs = [e["points"] for e in t["envs"] if e["active"]]
            covered = 0.0
            x = start
            while x < end:
                has_item = any(i["pos"] <= x < i["pos"] + i["len"] for i in items)
                audible = all(envelope_gain(p, x) >= SILENT for p in envs)
                if has_item and audible:
                    covered += STEP
                x += STEP
            if covered >= MIN_OVERLAP_BEATS * beat:
                playing.append(f"{t['name']}({covered / (end - start):.0%})")
        bars = round((end - start) / (beat * 4), 2)
        print(f"{name:12} {bars:5} bars | " + ", ".join(playing))


if __name__ == "__main__":
    main(sys.argv[1])
