# langcode2027.github.io

Website for **LangCode 2027 — The First Language and Code Workshop**
(*Towards Secure, Trustworthy, Robust, and Multilingual Code Generation*),
proposed for the joint EACL/COLING/NAACL/ACL/EMNLP 2027 workshop cycle.

Live at: <https://langcode2027.github.io>

## Structure

- `index.html` — single-page site (At a glance, About, Call for Papers,
  Shared Tasks, Dates, Speakers, Organizers, Program Committee)
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

Edit `index.html` and push to `main`; Pages redeploys automatically.
Preview locally by opening `index.html` in a browser — no tooling required.
Bump the `?v=` query on the `css/style.css` and `js/main.js` links when changing
those files, so returning visitors do not get a stale cached copy.

Maintained by the LangCode 2027 organizers.
