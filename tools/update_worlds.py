#!/usr/bin/env python3
"""Holt Weltliste und Weltdaten von die-staemme.de für den Tabben-Planer.

Schreibt:
  worlds/index.json          Liste aller Welten mit Laufzeiten, Einheiten, Deffwerten
  worlds/<welt>/village.txt  Dorfliste gekürzt auf "id,,x,y"

Läuft in der GitHub Action. Schlägt eine Welt fehl, bleiben ihre alten Daten erhalten.
"""
import json, os, re, sys, time, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

MARKET = os.environ.get("MARKET_URL", "https://www.die-staemme.de")
EXTRA = [w.strip() for w in os.environ.get("WORLDS", "").split(",") if w.strip()]
OUT = os.environ.get("OUT_DIR", "worlds")
BASE_SPEED = {"spear": 18, "sword": 22, "axe": 18, "archer": 18, "spy": 9, "light": 10, "marcher": 10,
              "heavy": 11, "ram": 30, "catapult": 30, "knight": 10, "snob": 35}
UA = {"User-Agent": "ds-tabbuddy world updater (GitHub Action)"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def world_list(get=fetch):
    worlds = {}
    try:
        raw = get(f"{MARKET}/backend/get_servers.php")
        for wid, url in re.findall(r's:\d+:"([a-z]+\d+[a-z]?)";s:\d+:"(https?://[^"]+)"', raw):
            worlds[wid] = url.rstrip("/")
    except Exception as e:
        print("Weltliste nicht abrufbar:", e, file=sys.stderr)
    for wid in EXTRA:
        worlds.setdefault(wid, f"https://{wid}.die-staemme.de")
    return worlds


def num(el, path, default=0.0):
    x = el.find(path)
    try:
        return float(x.text) if x is not None and x.text else default
    except ValueError:
        return default


def world_data(wid, url, get=fetch):
    cfg = ET.fromstring(get(f"{url}/interface.php?func=get_config"))
    time.sleep(1)
    ui = ET.fromstring(get(f"{url}/interface.php?func=get_unit_info"))
    time.sleep(1)
    speed, unit_speed = num(cfg, "speed", 1.0), num(cfg, "unit_speed", 1.0)
    factor = speed * unit_speed or 1.0
    units, raw_speeds, defs = [], {}, {}
    for el in ui:
        if el.tag == "militia":
            continue
        units.append(el.tag)
        raw_speeds[el.tag] = num(el, "speed", BASE_SPEED.get(el.tag, 18))
        defs[el.tag] = round((num(el, "defense") + num(el, "defense_cavalry")) / 2, 2)
    # unit_info liefert je nach Welt bereits umgerechnete Minuten pro Feld. Am Speer prüfen, welche Lesart passt.
    sp = raw_speeds.get("spear", 18)
    already_effective = abs(sp - 18 / factor) <= abs(sp - 18)
    speeds = {k: round(v if already_effective else v / factor, 6) for k, v in raw_speeds.items()}
    vt = get(f"{url}/map/village.txt")
    lines = []
    for line in vt.splitlines():
        p = line.split(",")
        if len(p) >= 4 and p[0].isdigit() and p[2].isdigit() and p[3].isdigit():
            lines.append(f"{p[0]},,{p[2]},{p[3]}")
    return {
        "id": wid, "url": url, "speed": speed, "unitSpeed": unit_speed,
        "millis": num(cfg, "commands/millis_arrival") > 0,
        "archer": num(cfg, "game/archer") > 0, "knight": num(cfg, "game/knight") > 0,
        "units": units, "speeds": speeds, "def": defs, "villages": len(lines),
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }, "\n".join(lines) + "\n"


def main(get=fetch):
    os.makedirs(OUT, exist_ok=True)
    idx_path = os.path.join(OUT, "index.json")
    old = {}
    if os.path.exists(idx_path):
        with open(idx_path, encoding="utf-8") as f:
            old = {w["id"]: w for w in json.load(f).get("worlds", [])}
    result = {}
    for wid, url in sorted(world_list(get).items()):
        try:
            info, villages = world_data(wid, url, get)
            os.makedirs(os.path.join(OUT, wid), exist_ok=True)
            with open(os.path.join(OUT, wid, "village.txt"), "w", encoding="utf-8") as f:
                f.write(villages)
            result[wid] = info
            print(f"{wid}: {info['villages']} Dörfer, Geschw. {info['speed']} × {info['unitSpeed']}")
        except Exception as e:
            print(f"{wid}: fehlgeschlagen ({e})", file=sys.stderr)
            if wid in old:
                result[wid] = old[wid]
    if not result:
        print("Keine Weltdaten erhalten, nichts geschrieben.", file=sys.stderr)
        return 1
    worlds = sorted(result.values(), key=lambda w: (re.sub(r"\d+", "", w["id"]), -int(re.sub(r"\D", "", w["id"]) or 0)))
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump({"worlds": worlds}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
