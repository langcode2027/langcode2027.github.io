"""Copy the Task 1 CodaBench leaderboards into data/task1_leaderboard.json (run daily by .github/workflows/leaderboard.yml).

Reads the public leaderboard API of the Development and Test phases of competition 18470, keeps each
team's entry (team name and affiliation from the submission form, Pass@1), sorts by Pass@1 and writes
data/task1_leaderboard.json with the time of the update. task-src/build.py turns that file into the two
boards on /task1/leaderboard/. Submissions from the organizers' accounts are never shown.
Since Nov 2026 CodaBench's bot check (Anubis) answers scripts with an HTML page
(since Nov 24, a 302 that sets a cookie and has no Location header). The script then leaves
the file unchanged, prints a warning and exits without an error, so the Action stays green. The board is
refreshed from the organizer's own Chrome by a daily scheduled task, which reads the same API in the
browser and runs:  python3 <this script> --from-browser FILE
FILE holds JSON {"<dev phase id>": [[owner, team_name, affiliation, {column_key: score, ...}], ...],
"<test phase id>": [...]}, one row per API submission.
Sends the CODABENCH_TOKEN secret as `Authorization: Token ...` if one is ever set (none is now).
Standard library only. Exits with an error, and leaves the file unchanged, if CodaBench cannot be read.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "task1_leaderboard.json"
API = "https://www.codabench.org/api/phases/{}/get_leaderboard/?page_size=all"   # default page is 50 rows
PHASES = {"dev": 31135, "test": 31136}
KEY = "score"                                       # Pass@1, the ranking column
ORGANIZERS = {"raihan_nishad"}                      # our own CodaBench accounts: never shown on the site boards


class BotCheck(Exception):
    """CodaBench sent its HTML bot-check page instead of JSON."""


def fetch(phase_id):
    headers = {"Accept": "application/json"}
    if os.environ.get("CODABENCH_TOKEN"):
        headers["Authorization"] = "Token " + os.environ["CODABENCH_TOKEN"].strip()
    req = urllib.request.Request(API.format(phase_id), headers=headers)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            if body.lstrip()[:1] == b"<":
                raise BotCheck(f"phase {phase_id}: CodaBench answered with an HTML page (bot check)")
            return json.loads(body)
        except BotCheck:                            # retrying does not help: the check stays up
            raise
        except urllib.error.HTTPError as e:         # since Nov 24 the check answers with a bare 302
            if 300 <= e.code < 400 or "anubis" in (e.headers.get("Set-Cookie") or "").lower():
                raise BotCheck(f"phase {phase_id}: CodaBench answered HTTP {e.code} (bot check)") from None
            if attempt == 3:
                raise
            print(f"phase {phase_id}: {e}; retrying", file=sys.stderr)
            time.sleep(30 * (attempt + 1))
        except Exception as e:                      # network hiccup or CodaBench busy: wait and retry
            if attempt == 3:
                raise
            print(f"phase {phase_id}: {e}; retrying", file=sys.stderr)
            time.sleep(10 * (attempt + 1))


def entries(submissions):
    out = []
    for s in submissions:
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
    if len(sys.argv) == 3 and sys.argv[1] == "--from-browser":
        raw = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8").strip())
        boards = {name: [{"owner": o, "fact_sheet_answers": {"team_name": t, "affiliation": a},
                          "scores": [{"column_key": k, "score": v} for k, v in (sc or {}).items() if v is not None]}
                         for o, t, a, sc in raw[str(phase_id)]]
                  for name, phase_id in PHASES.items()}
    else:
        try:
            boards = {name: fetch(phase_id).get("submissions", []) for name, phase_id in PHASES.items()}
        except BotCheck as e:
            print(f"::warning::{e}. Kept the last {OUT.name}; the daily browser task refreshes it.")
            return
    for name in PHASES:
        data[name] = entries(boards[name])
        print(f"{name}: {len(data[name])} teams")
    if not data["dev"] and OUT.exists() and json.loads(OUT.read_text(encoding="utf-8")).get("dev"):
        sys.exit("dev board came back empty; leaving the file unchanged")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
