// LangCode 2027 shared-task pages: mobile menu, dates card and countdown,
// updates bar, Task 1 language demo, BibTeX copy button.

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
  var now = Date.now();

  // Dates card: grey out passed dates, flag the next one, count down to it.
  var nextIso = null, nextTitles = [];
  document.querySelectorAll(".dates-card li[data-date]").forEach(function (li) {
    var iso = li.getAttribute("data-date");
    if (endOfDayAoE(iso) < now) {
      li.classList.add("is-past");
    } else if (nextIso === null || iso === nextIso) {
      nextIso = iso;
      li.classList.add("is-next");
      nextTitles.push(li.querySelector(".dc-title").textContent);
    }
  });
  var countdown = document.querySelector(".dc-countdown");
  if (countdown && nextIso) {
    var days = Math.ceil((endOfDayAoE(nextIso) - 86399000 - now) / 86400000);
    // Lowercase the first letter but keep names such as CodaBench.
    var what = nextTitles.map(function (t) {
      return /^[A-Z][a-z]+[A-Z]/.test(t) ? t : t.charAt(0).toLowerCase() + t.slice(1);
    }).join(" and ");
    countdown.innerHTML = days <= 0
      ? "<strong>Today</strong> " + what
      : "<strong>" + days + " days</strong> until " + what;
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

  // Task 1 data page: one problem, its description in many languages.
  var doc = document.getElementById("demo-doc");
  if (doc) {
    var tabs = Array.prototype.slice.call(document.querySelectorAll(".demo-tabs .tab"));
    var current = 0, timer = null;
    var show = function (i) {
      current = i;
      tabs.forEach(function (t, j) {
        t.classList.toggle("active", j === i);
        t.setAttribute("aria-selected", j === i ? "true" : "false");
      });
      doc.classList.add("fade");
      setTimeout(function () {
        doc.textContent = tabs[i].getAttribute("data-doc");
        doc.dir = tabs[i].getAttribute("data-dir") || "ltr";
        doc.classList.remove("fade");
      }, reduceMotion ? 0 : 200);
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { clearInterval(timer); show(i); });
    });
    if (!reduceMotion) timer = setInterval(function () { show((current + 1) % tabs.length); }, 2600);
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
