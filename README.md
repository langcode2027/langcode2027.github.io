# langcode2027.github.io

Website for **LangCode 2027 — The First Language and Code Workshop**
(*Towards Secure, Trustworthy, Robust, and Multilingual Code Generation*),
accepted as a one-day workshop co-located with NAACL 2027.

Live at: <https://langcode2027.github.io>

## Structure

- `index.html` — home page: hero, Updates ticker, and Call for Papers (five topic
  areas, the two ways to submit — direct OpenReview submission or ARR commitment —
  and the archival note: every accepted paper is archival, in the ACL Anthology).
- `submission/index.html` — Paper Submission page: six-step how-to, paper types,
  and official resources. Its step 6 links back to the ARR option on the home page.
- `organizers/index.html` — Organizing Committee, then Invited Speakers, then
  Program Committee (moved off the home page; the nav item is just "Organizers").
- `media/photos/` — real San Francisco hero photos from Wikimedia Commons
  (Golden Gate from Baker Beach on Home, Embarcadero on Submission, Painted Ladies
  on Organizers), 2400px wide. CC BY / CC BY-SA, credited in each page's footer.
  A theme-aware scrim in style.css (`.hero-photo`) keeps the hero text readable.
- `media/banner/` — the earlier drawn SF banners (SVG + PNG/PDF exports, light and
  dark); no longer used by the site, kept as standalone graphics.
- `media/announce/` — announcements, PNG + PDF: dark portrait (`langcode2027-announcement`),
  light portrait (`-light`), and light landscape 1920x1080 (`-landscape`), all at 2x,
  with QR codes to the home page and the submission page.
- `media/logo.svg` — the logo (terminal "lc" monogram with a cursor); also the
  favicon. The nav uses an inline copy that follows the light/dark theme.
- `task1/`, `task2/` — one small site per shared task, laid out like
  <https://banglaknight.github.io/>: a home page (banner with the Important Dates card,
  updates bar, the task, phases, next steps) plus `data/`, `leaderboard/`,
  `participate/` and `paper/`. Task 1 is green, Task 2 is red (`body.t1` / `body.t2`
  tokens in `css/task.css`; behavior in `js/task.js`).
  **These pages are generated.** Edit the bodies in `task-src/task1/*.html` and
  `task-src/task2/*.html`, or the shared dates in `DATES` at the top of
  `task-src/build.py` (the same schedule as BanglaKnight), then run
  `python3 task-src/build.py`. Hand edits to `task1/` or `task2/` are overwritten.
- `css/style.css` — styles; light/dark follows the visitor's system theme and can
  be overridden with the nav toggle (persisted in `localStorage` under `theme`)
- `js/main.js` — theme toggle, reading-progress bar, scroll reveals, stat
  count-ups, nav scrollspy, the polyglot typewriter in the hero, and the
  initials fallback for missing organizer photos.
  Everything degrades gracefully and is disabled under `prefers-reduced-motion`.
- No build step: plain HTML/CSS/JS served by GitHub Pages (`.nojekyll` disables Jekyll)

- `media/organizers/` — organizer headshots, square, referenced by the `<img>`
  in each card. A card with no `<img>` (or one whose file fails to load) shows
  the person's initials instead, so photos can be added one at a time.

Content mirrors the submitted workshop proposal (September 2026). Keep the two in
sync when the proposal changes — in particular the topic list, shared task
descriptions, organizer and program committee rosters, and expected attendance.

## Editing

Edit the HTML pages and push to `main`; Pages redeploys automatically.
Preview locally by opening `index.html` in a browser — no tooling required.
Bump the `?v=` query on the `css/style.css` and `js/main.js` links (in all five pages) when changing
those files, so returning visitors do not get a stale cached copy.

Maintained by the LangCode 2027 organizers.
