// LangCode 2027 shared-task pages: mobile menu, dates card and countdown,
// updates bar, Task 1 language example, BibTeX copy button.

(function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Mobile menu.
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Dates: a date counts as passed at the end of that day, Anywhere on Earth (UTC-12).
  function endOfDayAoE(iso) {
    var p = iso.split("-").map(Number);
    return Date.UTC(p[0], p[1] - 1, p[2], 23, 59, 59) + 12 * 3600 * 1000;
  }
  // Openings (data releases, phase starts; data-open) happen at 00:00 UTC, when CodaBench opens the phase.
  function startOfDayUTC(iso) {
    var p = iso.split("-").map(Number);
    return Date.UTC(p[0], p[1] - 1, p[2]);
  }
  var now = Date.now();

  // Dates card: grey out passed dates, flag the next one, count down to it.
  var nextIso = null, nextTitles = [], nextOpen = false;
  document.querySelectorAll(".dates-card li[data-date]").forEach(function (li) {
    var iso = li.getAttribute("data-date");
    if (endOfDayAoE(iso) < now) {
      li.classList.add("is-past");
    } else if (nextIso === null || iso === nextIso) {
      nextIso = iso;
      li.classList.add("is-next");
      nextTitles.push(li.querySelector(".dc-title").textContent);
      nextOpen = nextOpen || li.hasAttribute("data-open");
    }
  });
  var countdown = document.querySelector(".dc-countdown");
  if (countdown && nextIso) {
    var target = nextOpen ? startOfDayUTC(nextIso) : endOfDayAoE(nextIso) - 86399000;
    var days = Math.ceil((target - now) / 86400000);
    // Lowercase the first letter but keep names such as CodaBench.
    var what = nextTitles.map(function (t) {
      return /^[A-Z][a-z]+[A-Z]/.test(t) ? t : t.charAt(0).toLowerCase() + t.slice(1);
    }).join(" and ");
    countdown.innerHTML = days <= 0
      ? "<strong>Today</strong> " + what
      : "<strong>" + days + (days === 1 ? " day" : " days") + "</strong> until " + what;
    countdown.hidden = false;
  }

  // Updates bar: hide dates that have passed, then add a second copy so the loop is seamless.
  var tset = document.querySelector(".ticker .tk-set");
  if (tset) {
    tset.querySelectorAll(".tk[data-date]").forEach(function (tk) {
      if (endOfDayAoE(tk.getAttribute("data-date")) < now) tk.remove();
    });
    if (!reduceMotion) {
      var copy = tset.cloneNode(true);
      copy.setAttribute("aria-hidden", "true");
      copy.querySelectorAll("a").forEach(function (a) { a.setAttribute("tabindex", "-1"); });
      tset.parentNode.appendChild(copy);
    }
  }

  // Task 1 data page: one problem, its description in many natural languages
  // (top tabs) and its code in several programming languages (bottom tabs).
  var nlTabs = Array.prototype.slice.call(document.querySelectorAll(".demo-tabs.many .tab"));
  if (nlTabs.length) {
    var docs = document.querySelectorAll(".code-demo .doc");
    var plTabs = Array.prototype.slice.call(document.querySelectorAll(".pl-tabs .tab"));
    var codes = document.querySelectorAll(".code-demo[data-pl]");
    var current = 0, timer = null;
    var select = function (tabs, active) {
      tabs.forEach(function (t) {
        t.classList.toggle("active", t === active);
        t.setAttribute("aria-selected", t === active ? "true" : "false");
      });
    };
    var showNl = function (i) {
      current = i;
      select(nlTabs, nlTabs[i]);
      docs.forEach(function (d) { d.classList.add("fade"); });
      setTimeout(function () {
        docs.forEach(function (d) {
          d.textContent = nlTabs[i].getAttribute("data-doc");
          d.dir = nlTabs[i].getAttribute("data-dir") || "ltr";
          d.classList.remove("fade");
        });
      }, reduceMotion ? 0 : 200);
    };
    nlTabs.forEach(function (t, i) {
      t.addEventListener("click", function () { clearInterval(timer); showNl(i); });
    });
    plTabs.forEach(function (t) {
      t.addEventListener("click", function () {
        clearInterval(timer);
        select(plTabs, t);
        codes.forEach(function (c) { c.hidden = c.getAttribute("data-pl") !== t.getAttribute("data-pl"); });
      });
    });
    if (!reduceMotion) timer = setInterval(function () { showNl((current + 1) % nlTabs.length); }, 2600);
  }

  // Copy BibTeX.
  document.querySelectorAll(".copy-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      var pre = b.parentNode.querySelector("pre");
      if (!pre || !navigator.clipboard) return;
      navigator.clipboard.writeText(pre.textContent).then(function () {
        b.textContent = "copied";
        setTimeout(function () { b.textContent = "copy"; }, 1500);
      });
    });
  });
})();
