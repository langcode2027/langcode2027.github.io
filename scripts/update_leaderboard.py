"""Copy the Task 1 CodaBench leaderboards into data/task1_leaderboard.json (run daily by .github/workflows/leaderboard.yml).

Reads the public leaderboard API of the Development and Test phases of competition 18470, keeps each
team's entry (team name and affiliation from the submission form, Pass@1), sorts by Pass@1 and writes
data/task1_leaderboard.json with the time of the update. task-src/build.py turns that file into the two
boards on /task1/leaderboard/. Submissions from the organizers' accounts are never shown.
Standard library only. Exits with an error, and leaves the file unchanged, if CodaBench cannot be read.
"""
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "task1_leaderboard.json"
API = "https://www.codabench.org/api/phases/{}/get_leaderboard/"
PHASES = {"dev": 31135, "test": 31136}
KEY = "score"                                       # Pass@1, the ranking column
ORGANIZERS = {"raihan_nishad"}                      # our own CodaBench accounts: never shown on the site boards


def fetch(phase_id):
    req = urllib.request.Request(API.format(phase_id), headers={"Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)          # a non-JSON answer raises here and is retried
        except Exception as e:                      # network hiccup or CodaBench busy: wait and retry
            if attempt == 3:
                raise
            print(f"phase {phase_id}: {e}; retrying", file=sys.stderr)
            time.sleep(10 * (attempt + 1))


def entries(board):
    out = []
    for s in board.get("submissions", []):
        if s.get("owner") in ORGANIZERS:
            continue
        score = next((float(x["score"]) for x in s.get("scores", []) if x.get("column_key") == KEY), None)
        if score is None:
            continue
        fs = s.get("fact_sheet_answers") or {}
        out.append({"team": (fs.get("team_name") or s.get("owner") or "").strip()[:80],
                    "affiliation": (fs.get("affiliation") or "").strip()[:120],
                    "score": score})
    return sorted(out, key=lambda e: -e["score"])


def main():
    data = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    for name, phase_id in PHASES.items():
        data[name] = entries(fetch(phase_id))
        print(f"{name}: {len(data[name])} teams")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
