# langcode2027.github.io

Website for **LangCode 2027 — The First Language and Code Workshop**
(*Towards Secure, Trustworthy, Robust, and Multilingual Code Generation*),
accepted as a one-day workshop co-located with NAACL 2027.

Live at: <https://langcode2027.github.io>

## Structure

- `index.html` — main page (At a glance, About, Call for Papers,
  Shared Tasks, Dates, Speakers, Organizers, Program Committee)
- `submission/index.html` — Paper Submission page: formal guidelines (paper types
  and limits, ACL format, anonymity, ARR commitment, policies, presentation) and a
  pre-submission checklist.
- `media/logo.svg` — the logo (terminal "lc" monogram with a cursor); also the
  favicon. The nav uses an inline copy that follows the light/dark theme.
- `task1/index.html`, `task2/index.html` — one page per shared task
  (Multilingual Code Generation; Adversarial Prompt Detection). Task 2 uses a
  rose accent via `body.t2`. Each hero has a live demo driven by `js/main.js`.
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
Bump the `?v=` query on the `css/style.css` and `js/main.js` links (in all four pages) when changing
those files, so returning visitors do not get a stale cached copy.

Maintained by the LangCode 2027 organizers.
