"""Check the apparatus for broken references. Run from the repository root:

    python tools/verify.py

Checks: every shipped module has its data file; citation labels (zk)
are unique per module; every '#/text/...' link in the timeline and the compare
pairs points to an existing unit; every compare
voice exists; every plate has its image and thumbnail; every timeline plate
exists. Prints the problems and a last line 'bad N'.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
load = lambda f: json.load(open(D / f, encoding="utf-8"))

bad = []
mods = load("modules.json")
units, labels = set(), {}
for m in mods["shipped"]:
    f = D / f"{m['datei']}.json"
    if not f.exists():
        bad.append(f"module file missing: {f.name}")
        continue
    t = json.load(open(f, encoding="utf-8"))
    for s in t["sections"]:
        if s["zk"] in labels and labels[s["zk"]] != m["id"]:
            bad.append(f"zk '{s['zk']}' used by two modules ({labels[s['zk']]} and {m['id']})")
        labels[s["zk"]] = m["id"]
        for u in s["units"]:
            units.add(f"#/text/{m['id']}/{s['id']}/{u['n']}")

def check_link(href, where):
    if href.startswith("#/text/") and href not in units:
        bad.append(f"{where}: no such unit {href}")

tl = load("timeline.json")
plates = load("plates.json")
plate_ids = {p["id"] for p in plates["plates"]}
for s in tl["stations"]:
    if s.get("cite"):
        check_link(s["cite"], f"timeline '{s['titel']}'")
    if s.get("plate") and s["plate"] not in plate_ids:
        bad.append(f"timeline '{s['titel']}': no such plate {s['plate']}")
for p in plates["plates"]:
    for suffix in ("", "_t"):
        if not (ROOT / "assets" / "plates" / f"{p['id']}{suffix}.jpg").exists():
            bad.append(f"plate image missing: {p['id']}{suffix}.jpg")
cmp_ = load("compare.json")
shipped = {m["id"]: m for m in mods["shipped"]}
for p in cmp_["pairs"]:
    for v in p["voices"]:
        for n in v["n"]:
            check_link(f"#/text/{v['text']}/{v['sec']}/{n}", f"compare '{p['id']}'")

for b in bad:
    print(b)
print(f"bad {len(bad)} modules {len(labels)} units {len(units)} plates {len(plate_ids)} stations {len(tl['stations'])} pairs {len(cmp_['pairs'])}")
