"""Build the LangCode 2027 shared-task pages.

Layout follows banglaknight.github.io. Page bodies live in task-src/<task>/<slug>.html.
This script wraps each one in the shared menu, banner, updates bar and footer, fills in
the dates, and writes task1/index.html, task1/data/index.html, and so on (same for task2).

Run after any edit:  python3 task-src/build.py
Change a date:       edit DATES below (shared) or a task's "open" date, then run the script.
Don't edit the generated task*/ pages by hand; the next build overwrites them.
"""

from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# Shared schedule. The test phase matches BanglaKnight (BLP 2027 Task 1).
# (ISO date used for the countdown, label shown, milestone, phase)
DATES = [
    ("2027-01-08", "Jan 8, 2027", "Test data release / test phase begins", "eval"),
    ("2027-01-17", "Jan 17, 2027", "CodaBench registration deadline", "eval"),
    ("2027-01-24", "Jan 24, 2027", "System submission deadline", "eval"),
    ("2027-02-03", "Feb 3, 2027", "Official results released", "after"),
    ("2027-02-15", "Feb 15, 2027", "Shared-task paper submission deadline", "after"),
    ("2027-03-26", "Mar 26, 2027", "Notification of acceptance", "after"),
    ("2027-04-16", "Apr 16, 2027", "Camera-ready paper due", "after"),
    ("2027-06-01", "Jun 1–5, 2027", "Workshop at NAACL 2027, San Francisco", "after"),
]

PHASE_NAMES = {
    "dev": ("Development phase", "{open} – Jan 7"),
    "eval": ("Test phase", "Jan 8 – Jan 24"),
    "after": ("Results and papers", ""),
}

TASKS = {
    "task1": {
        "n": 1,
        "cls": "t1",
        "name": "Multilingual Code Generation",
        "open": ("2026-10-27", "Oct 27, 2026", "Trial and development data release"),
        "short": "Code generation from 50 natural languages",
        "theme": "#0E8A5F",
        "test_note": "",
        "eval_data": "1,000 test problems, released Jan 8, each with 2 of its 5 test cases shown",
        "dev_data": "Trial and dev sets, the scorer and the submission format",
        "questions": 'Questions: ask in the <a href="https://www.codabench.org/competitions/18470/#/forum" target="_blank" rel="noopener">Forum</a> of the CodaBench competition.',
        "eval_submit": "Submit your test solutions by Jan 24. These decide the official ranking, published Feb 3.",
        "dev_codabench": "Submit solutions for the dev problems to see your Pass@1 and check your file format. Practice only: it does not count toward the final ranking.",
        "data_desc": "The trial, dev and test sets, the scorer, and one problem in several languages.",
        "other": "task2",
    },
    "task2": {
        "n": 2,
        "cls": "t2",
        "name": "Adversarial Prompt Detection",
        "open": ("2026-10-29", "Oct 29, 2026", "Train, dev and dev-test data release"),
        "short": "Guardrails for code-mixed and transliterated prompts",
        "theme": "#D93A43",
        "test_note": "",
        "eval_data": "30,000 test prompts, released Jan 8, without labels",
        "dev_data": "Train, dev and dev-test sets, the scorer and a starter notebook",
        "questions": 'Questions: ask in the <a href="https://www.codabench.org/competitions/18479/#/forum" target="_blank" rel="noopener">Forum</a> of the CodaBench competition.',
        "eval_submit": "Submit your test labels by Jan 24. These decide the official ranking, published Feb 3.",
        "dev_codabench": "Submit labels for the dev-test set to see your Safety Score and check your file format. Practice only: it does not count toward the final ranking.",
        "data_desc": "The train, dev and dev-test sets, the scorer, a starter notebook and the MALICE citation.",
        "other": "task1",
    },
}

# slug, menu label, page title, one-line description (None: the task's own data_desc), header photo, icon
PAGES = [
    ("home", "Home", "", "", "sf-golden-gate.jpg", None),
    ("data", "Data", "Data", None, "sf-embarcadero.jpg", "data"),
    ("leaderboard", "Leaderboard", "Leaderboard", "The dev and test leaderboards, and how teams are ranked.", "sf-painted-ladies.jpg", "trophy"),
    ("participate", "Participate", "Participate", "Two phases on CodaBench: practice on the dev set, then submit on the test set.", "sf-golden-gate.jpg", "flag"),
    ("paper", "Paper Submission", "Paper Submission", "How to write and submit your system description paper.", "sf-painted-ladies.jpg", "paper"),
]

# Line icons (24x24, drawn with the current text color). In page sources, {{i:name}} becomes the icon.
ICONS = {
    "data": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "trophy": '<path d="M8 21h8"/><path d="M12 16v5"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 5h3v2a3 3 0 0 1-3 3"/><path d="M7 5H4v2a3 3 0 0 0 3 3"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h13l-2.5 4.5L18 13H5"/>',
    "paper": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h6"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.6-3.4 3-5.4 6-5.4s5.4 2 6 5.4"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 14.7c2.4.2 4 1.9 4.5 4.8"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    "upload": '<path d="M12 15V4"/><path d="M7.5 8.5 12 4l4.5 4.5"/><path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    "download": '<path d="M12 4v11"/><path d="M7.5 10.5 12 15l4.5-4.5"/><path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "inbox": '<path d="M3 13h5l1.5 2.5h5L16 13h5"/><path d="M5.5 5h13L21 13v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5z"/>',
    "tag": '<path d="M3 12V4h8l9.5 9.5-8 8z"/><circle cx="7.5" cy="8.5" r="1.4"/>',
    "book": '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H20v15H5.5A1.5 1.5 0 0 0 4 19.5z"/><path d="M4 19.5A1.5 1.5 0 0 0 5.5 21H20v-3"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/>',
    "shield-check": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    "message": '<path d="M4 5h16v11H9l-5 4z"/><path d="M9 9l4 4M13 9l-4 4"/>',
    "alert": '<path d="M12 3.5 2.5 20h19z"/><path d="M12 10v4.5M12 17.3v.1"/>',
    "octagon": '<path d="M8.2 3h7.6L21 8.2v7.6L15.8 21H8.2L3 15.8V8.2z"/><path d="M12 8v4.5M12 15.8v.1"/>',
    "gauge": '<path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 17 4-5"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "tool": '<path d="M15 4a5 5 0 0 0-4.8 6.4L4 16.6V20h3.4l6.2-6.2A5 5 0 0 0 20 9l-3 1-2-2 1-3z"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.7 5.4 3.7 8.5s-1.2 5.9-3.7 8.5c-2.5-2.6-3.7-5.4-3.7-8.5s1.2-5.9 3.7-8.5z"/>',
    "package": '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
    "code": '<path d="m8.5 7-5 5 5 5M15.5 7l5 5-5 5"/>',
    "file-code": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/>',
    "file-check": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m9 14.5 2 2 4-4"/>',
    "table": '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M3.5 14.5h17M9.5 9.5v10"/>',
    "user": '<circle cx="12" cy="8" r="3.8"/><path d="M4.5 20.5c.8-4 3.8-6.2 7.5-6.2s6.7 2.2 7.5 6.2"/>',
    "user-plus": '<circle cx="10" cy="8" r="3.5"/><path d="M3.5 20c.7-3.6 3.3-5.6 6.5-5.6s5.8 2 6.5 5.6"/><path d="M19 8v6M16 11h6"/>',
    "play": '<circle cx="12" cy="12" r="8.5"/><path d="m10 8.5 5.5 3.5-5.5 3.5z"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2.5v3.5M15 2.5v3.5M9 18v3.5M15 18v3.5M2.5 9h3.5M2.5 15h3.5M18 9h3.5M18 15h3.5"/>',
    "pen": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
    "check": '<circle cx="12" cy="12" r="8.5"/><path d="m8.5 12.2 2.4 2.4 4.6-4.8"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "present": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8 20h8"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    "eye-off": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/><path d="M4 4l16 16"/>',
    "scale": '<path d="M12 4v16M7 20h10M5 7h14"/><path d="m5 7-2.5 6a2.8 2.8 0 0 0 5 0zM19 7l-2.5 6a2.8 2.8 0 0 0 5 0z"/>',
    "type": '<path d="M4 7V5h16v2M12 5v14M9 19h6"/>',
    "question": '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.4 2.3c-.6.3-1 .8-1 1.5v.7M12 16.8v.1"/>',
    "shuffle": '<path d="M3 7h3.5c4.5 0 6.5 10 11 10H21M3 17h3.5c1.6 0 2.8-1.2 3.8-2.8M13.7 9.8c1-1.6 2.2-2.8 3.8-2.8H21"/><path d="m18 4 3 3-3 3M18 14l3 3-3 3"/>',
    "route": '<circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="5" r="2.2"/><path d="M8.2 19H16a3.5 3.5 0 0 0 0-7H8a3.5 3.5 0 0 1 0-7h7.8"/>',
    "chart": '<path d="M4 4v16h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
}

ICON_RE = __import__("re").compile(r"\{\{i:([a-z-]+)\}\}")
# Milestones that open something (a data release, a phase start). The dates card counts down to them
# from 00:00 UTC, when CodaBench opens the phase; deadlines count to the end of the day AoE.
OPENING_RE = __import__("re").compile(r"release|opens|begins", __import__("re").I)
LB_EMPTY_RE = __import__("re").compile(r"\{\{LB_EMPTY:([ts]+)\}\}")
LEADERBOARD_ROWS = 10   # placeholder rows per board until results come in (Task 2)
# Task 1 leaderboard data, written once a day by scripts/update_leaderboard.py (GitHub Action)
LEADERBOARD_JSON = ROOT / "data" / "task1_leaderboard.json"
TASK1_LB_ROWS = 30
# Task 2 leaderboard data, written once a day by scripts/update_task2_leaderboard.py (GitHub Action)
LEADERBOARD2_JSON = ROOT / "data" / "task2_leaderboard.json"
TASK2_LB_ROWS = 30


def lb_empty(spec):
    """Placeholder rows: the rank, then one dash per column after it (t = text, s = score, right-aligned)."""
    cells = "".join('<td class="lb-score">&mdash;</td>' if c == "s" else "<td>&mdash;</td>" for c in spec)
    return "\n          ".join(
        f'<tr><td class="lb-rank">{k}</td>{cells}</tr>'
        for k in range(1, LEADERBOARD_ROWS + 1))


def leaderboard_parts():
    """Task 1: rows for the dev and test boards and the 'Last updated' line, from data/task1_leaderboard.json."""
    import json
    from datetime import datetime, timedelta, timezone
    data = json.loads(LEADERBOARD_JSON.read_text(encoding="utf-8")) if LEADERBOARD_JSON.exists() else {}

    def rows(entries):
        out = []
        for k in range(max(TASK1_LB_ROWS, len(entries))):
            if k < len(entries):
                e = entries[k]
                out.append(f'<tr><td class="lb-rank">{k + 1}</td><td class="lb-team">{escape(e["team"])}</td>'
                           f'<td class="lb-aff">{escape(e["affiliation"])}</td><td class="lb-score">{e["score"]:.2f}</td></tr>')
            else:
                out.append(f'<tr><td class="lb-rank">{k + 1}</td><td class="lb-team">&mdash;</td>'
                           f'<td class="lb-aff">&mdash;</td><td class="lb-score">&mdash;</td></tr>')
        return "\n          ".join(out)

    if data.get("updated"):
        t = datetime.fromisoformat(data["updated"]).astimezone(timezone(timedelta(hours=-5)))
        stamp = f"{t:%b} {t.day}, {t.year}, {t:%I:%M %p}".replace(" 0", " ")
        updated = (f"<strong>Last updated: {stamp} EST (UTC&minus;5).</strong> "
                   "The leaderboards on this page refresh every day at 12:00 AM EST.")
    else:
        updated = "The leaderboards on this page refresh every day at 12:00 AM EST (UTC&minus;5)."
    return rows(data.get("dev", [])), rows(data.get("test", [])), updated


def task2_leaderboard_parts():
    """Task 2: rows (Safety Score, R_U, R_S) for the dev and test boards and the 'Last updated' line."""
    import json
    from datetime import datetime, timedelta, timezone
    data = json.loads(LEADERBOARD2_JSON.read_text(encoding="utf-8")) if LEADERBOARD2_JSON.exists() else {}

    def rows(entries):
        out = []
        for k in range(max(TASK2_LB_ROWS, len(entries))):
            if k < len(entries):
                e = entries[k]
                out.append(f'<tr><td class="lb-rank">{k + 1}</td><td class="lb-team">{escape(e["team"])}</td>'
                           f'<td class="lb-aff">{escape(e["affiliation"])}</td><td class="lb-score">{e["score"]:.2f}</td>'
                           f'<td class="lb-score">{e["unsafe_recall"]:.2f}</td><td class="lb-score">{e["safe_recall"]:.2f}</td></tr>')
            else:
                out.append(f'<tr><td class="lb-rank">{k + 1}</td><td class="lb-team">&mdash;</td><td class="lb-aff">&mdash;</td>'
                           + '<td class="lb-score">&mdash;</td>' * 3 + '</tr>')
        return "\n          ".join(out)

    if data.get("updated"):
        t = datetime.fromisoformat(data["updated"]).astimezone(timezone(timedelta(hours=-5)))
        stamp = f"{t:%b} {t.day}, {t.year}, {t:%I:%M %p}".replace(" 0", " ")
        updated = (f"<strong>Last updated: {stamp} EST (UTC&minus;5).</strong> "
                   "The leaderboards on this page refresh every day at 12:00 AM EST.")
    else:
        updated = "The leaderboards on this page refresh every day at 12:00 AM EST (UTC&minus;5)."
    return rows(data.get("dev", [])), rows(data.get("test", [])), updated


def icons_in(html):
    """Replace {{i:name}} placeholders with inline icons."""
    return ICON_RE.sub(lambda m: icon(m.group(1)), html)

LOGO = ('<svg class="logo" viewBox="0 0 64 64" aria-hidden="true"><rect class="lg-tile" x="2" y="2" width="60" height="60" rx="14"/>'
        '<path class="lg-glyph" d="M14 17h6v24M14 41h12"/><path class="lg-glyph" d="M40.5 29.2a7.6 7.6 0 1 0 0 11.6"/>'
        '<rect class="lg-caret" x="45" y="21" width="7.5" height="21" rx="1.2"/></svg>')


def icon(name, cls="ico"):
    if not name:
        return ""
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def url(task, slug):
    return f"/{task}/" if slug == "home" else f"/{task}/{slug}/"


def task_dates(t):
    """The shared schedule with the task's own opening date for the development phase."""
    iso, label, release = t["open"]
    first = [(iso, label, release, "dev"), (iso, label, "CodaBench registration opens", "dev")]
    return first + [d for d in DATES if d[3] != "dev"]


def dates_card(t):
    groups = []
    dates = task_dates(t)
    for phase in dict.fromkeys(p for *_, p in dates):
        name, span = PHASE_NAMES[phase]
        span = span.format(open=t["open"][1].rsplit(",", 1)[0])
        items = "\n".join(
            f'        <li data-date="{iso}"{" data-open" if OPENING_RE.search(title) else ""}><span class="dc-date">{label}</span>'
            f'<span class="dc-title">{escape(title + (t["test_note"] if iso == "2027-01-08" else ""))}</span></li>'
            for iso, label, title, p in dates if p == phase
        )
        span_html = f'<span class="dc-span">{span}</span>' if span else ""
        groups.append(f"""    <section class="dc-group dc-group-{phase}">
      <h3 class="dc-phase-head"><span class="dc-pill">{name}</span>{span_html}</h3>
      <ol class="dc-list">
{items}
      </ol>
    </section>""")
    body = "\n".join(groups)
    return f"""<aside class="dates-card" aria-label="Important dates">
  <div class="dc-head"><h2>{icon("calendar")}Important Dates</h2><span class="dc-tag">AoE</span></div>
{body}
  <p class="dc-countdown" hidden></p>
  <p class="dc-note">Dates may change. Deadlines are 11:59 PM AoE.</p>
</aside>"""


def phases_block(t):
    return f"""<div class="phases">
  <article class="phase phase-dev">
    <p class="phase-tag">Phase 1</p>
    <h3>{icon("tool")}Development phase</h3>
    <p class="phase-when">{t["open"][1]} – Jan 7, 2027</p>
    <dl>
      <dt>{icon("data")}Data</dt><dd>{t["dev_data"]}</dd>
      <dt>{icon("user")}You</dt><dd>Build and tune your system</dd>
      <dt>{icon("upload")}CodaBench</dt><dd>{t["dev_codabench"]}</dd>
    </dl>
  </article>
  <article class="phase phase-eval">
    <p class="phase-tag">Phase 2 · Final</p>
    <h3>{icon("target")}Test phase</h3>
    <p class="phase-when">Jan 8 – Jan 24, 2027</p>
    <dl>
      <dt>{icon("data")}Data</dt><dd>{t["eval_data"]}</dd>
      <dt>{icon("user")}You</dt><dd>Run your final system on it</dd>
      <dt>{icon("upload")}CodaBench</dt><dd>{t["eval_submit"]}</dd>
    </dl>
  </article>
</div>"""


def ticker(key, t):
    """Rolling updates bar: the dates still ahead, then news. task.js loops it."""
    items, last = [], None
    for iso, label, title, _p in task_dates(t):
        title = title + (t["test_note"] if iso == "2027-01-08" else "")
        if label == last:   # two milestones on one day share one item
            items[-1] = items[-1].replace("</span>", f"; {escape(title)}</span>")
            continue
        last = label
        items.append(f'<span class="tk" data-date="{iso}"><b>{label}</b>{escape(title)}</span>')
    o = TASKS[t["other"]]
    items += [
        '<span class="tk"><b>LangCode 2027</b>Co-located with NAACL 2027 · June 1–5, 2027 · San Francisco, California</span>',
        f'<span class="tk"><b>Also</b><a href="{url(t["other"], "home")}">Shared Task {o["n"]}: {o["name"]}</a></span>',
        '<span class="tk" data-date="2027-02-05"><b>Feb 5, 2027</b>Regular workshop papers due. See the <a href="/#cfp">Call for Papers</a></span>',
    ]
    body = "\n          ".join(items)
    return f"""<div class="ticker" role="region" aria-label="Updates and important dates">
  <div class="wrap ticker-in">
    <span class="ticker-label"><span class="dot" aria-hidden="true"></span>Updates</span>
    <div class="ticker-view">
      <div class="ticker-track">
        <div class="tk-set">
          {body}
        </div>
      </div>
    </div>
  </div>
</div>"""


def nav(key, t, active):
    o = TASKS[t["other"]]
    current = ' class="active" aria-current="page"'
    links = "\n".join(
        f'      <a href="{url(key, s)}"{current if s == active else ""}>{icon(ico)}{label}</a>'
        for s, label, _t, _d, _p, ico in PAGES if s != "home"
    )
    return f"""<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="{url(key, "home")}" aria-label="Shared Task {t["n"]} home">
      {LOGO}
      <span class="brand-text"><span class="brand-name">LangCode<span>'27</span></span><span class="brand-sub">Shared Task {t["n"]}</span></span>
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links">
      <span></span><span></span><span></span>
    </button>
    <nav id="nav-links" class="nav-links">
{links}
      <a href="/organizers/">{icon("people")}Organizers</a>
      <a class="nav-other" href="{url(t["other"], "home")}" style="--other: {o["theme"]}" title="Shared Task {o["n"]}: {o["name"]}">Task {o["n"]} <span aria-hidden="true">→</span></a>
      <a class="nav-cta" href="/">LangCode 2027</a>
    </nav>
  </div>
</header>"""


def page_header(key, t, title, desc, photo, ico):
    return f"""<section class="page-head" style="--photo: url('/media/photos/{photo}')">
  <div class="wrap">
    <p class="crumbs"><a href="/">LangCode 2027</a> <span aria-hidden="true">/</span> <a href="{url(key, "home")}">Task {t["n"]}</a> <span aria-hidden="true">/</span> {escape(title)}</p>
    <h1>{icon(ico, "ico ico-h1")}{escape(title)}</h1>
    <p class="page-desc">{escape(desc)}</p>
  </div>
</section>"""


def pager(key, i):
    inner = [p for p in PAGES if p[0] != "home"]
    slugs = [p[0] for p in inner]
    slug = PAGES[i][0]
    if slug not in slugs:
        return ""
    j = slugs.index(slug)
    prev_html = f'<a class="pg-prev" href="{url(key, inner[j-1][0])}"><span>Previous</span>{inner[j-1][1]}</a>' if j > 0 else "<span></span>"
    next_html = f'<a class="pg-next" href="{url(key, inner[j+1][0])}"><span>Next</span>{inner[j+1][1]}</a>' if j < len(inner) - 1 else "<span></span>"
    return f'<nav class="pager wrap" aria-label="Page navigation">{prev_html}{next_html}</nav>'


def footer(t):
    o = TASKS[t["other"]]
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-inner">
      <div class="footer-brand">
        {LOGO}
        <p><strong>Shared Task {t["n"]}: {t["name"]}</strong> is part of <a href="/">LangCode 2027, the First Language and Code Workshop</a>, co-located with NAACL 2027 in San Francisco. {t["questions"]}</p>
      </div>
      <p class="footer-also">Also at LangCode 2027: <a href="{url(t["other"], "home")}">Task {o["n"]}: {o["name"]} →</a></p>
    </div>
    <p class="credits">Photos from Wikimedia Commons:
      <a href="https://commons.wikimedia.org/wiki/File:GoldenGateBridge_BakerBeach_MC.jpg" target="_blank" rel="noopener">Golden Gate Bridge</a> by Christian Mehlführer (CC BY 3.0);
      <a href="https://commons.wikimedia.org/wiki/File:Painted_Ladies_San_Francisco_January_2013_panorama_2.jpg" target="_blank" rel="noopener">Painted Ladies</a> by King of Hearts (CC BY-SA 3.0);
      <a href="https://commons.wikimedia.org/wiki/File:San_Francisco_from_Pier_7_September_2013_panorama_edit.jpg" target="_blank" rel="noopener">San Francisco from Pier 7</a> by King of Hearts (CC BY-SA 3.0). Tinted.</p>
  </div>
</footer>"""


def render(key, i):
    t = TASKS[key]
    slug, label, title, desc, photo, ico = PAGES[i]
    body = (HERE / key / f"{slug}.html").read_text(encoding="utf-8")
    body = (body.replace("{{DATES_CARD}}", dates_card(t))
                .replace("{{PHASES}}", phases_block(t))
                .replace("{{TICKER}}", ticker(key, t)))
    body = LB_EMPTY_RE.sub(lambda m: lb_empty(m.group(1)), body)
    if "{{LB_DEV_ROWS}}" in body:
        dev_rows, test_rows, updated = leaderboard_parts()
        body = body.replace("{{LB_DEV_ROWS}}", dev_rows).replace("{{LB_TEST_ROWS}}", test_rows).replace("{{LB_UPDATED}}", updated)
    if "{{LB2_DEV_ROWS}}" in body:
        dev_rows, test_rows, updated = task2_leaderboard_parts()
        body = body.replace("{{LB2_DEV_ROWS}}", dev_rows).replace("{{LB2_TEST_ROWS}}", test_rows).replace("{{LB2_UPDATED}}", updated)
    desc = desc or t["data_desc"]
    if slug == "home":
        full_title = f"Shared Task {t['n']}: {t['name']} · LangCode 2027"
        desc = f"LangCode 2027 Shared Task {t['n']}: {t['short']}. Co-located with NAACL 2027."
        head_html = ""
    else:
        full_title = f"{title} · Task {t['n']}: {t['name']} · LangCode 2027"
        head_html = page_header(key, t, title, desc, photo, ico) + "\n" + ticker(key, t)
    return icons_in(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(full_title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="theme-color" content="{t["theme"]}">
  <link rel="canonical" href="https://langcode2027.github.io{url(key, slug)}">
  <link rel="icon" type="image/svg+xml" href="/media/logo.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/task.css?v=12">
</head>
<body class="{t["cls"]} page-{slug}">

{nav(key, t, slug)}

<main>
{head_html}
{body}
{pager(key, i)}
</main>

{footer(t)}

<script src="/js/task.js?v=4"></script>
</body>
</html>
""")


def main():
    for key in TASKS:
        for i, (slug, *_rest) in enumerate(PAGES):
            out = ROOT / key / ("index.html" if slug == "home" else f"{slug}/index.html")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(key, i), encoding="utf-8")
            print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
