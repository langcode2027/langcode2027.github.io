/* LangCode 2027 — site behaviour.
   Loaded synchronously in <head> so the theme is applied before first paint;
   everything else waits for DOMContentLoaded. No dependencies, no build step. */
(function () {
  "use strict";

  /* ---- theme, applied pre-paint to avoid a flash of the wrong palette ---- */
  var stored = null;
  try { stored = localStorage.getItem("theme"); } catch (e) {}
  if (stored === "light" || stored === "dark") {
    document.documentElement.setAttribute("data-theme", stored);
  }

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {

    /* ---------------------------------------------------- theme toggle ---- */
    var toggle = document.querySelector(".theme-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        var attr = document.documentElement.getAttribute("data-theme");
        var dark = attr
          ? attr === "dark"
          : window.matchMedia("(prefers-color-scheme: dark)").matches;
        var next = dark ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        try { localStorage.setItem("theme", next); } catch (e) {}
      });
    }

    /* ------------------------------------------------- reading progress ---- */
    var bar = document.getElementById("progress");
    if (bar) {
      var tick = false;
      var paint = function () {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        var p = h > 0 ? Math.min(1, Math.max(0, window.scrollY / h)) : 0;
        bar.style.transform = "scaleX(" + p + ")";
        tick = false;
      };
      window.addEventListener("scroll", function () {
        if (!tick) { tick = true; window.requestAnimationFrame(paint); }
      }, { passive: true });
      window.addEventListener("resize", paint, { passive: true });
      paint();
    }

    /* ------------------------------------------------- reveal on scroll ---- */
    var revealables = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
    if (!("IntersectionObserver" in window) || reduce) {
      revealables.forEach(function (el) { el.classList.add("in"); });
    } else {
      var ro = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.classList.add("in");
          ro.unobserve(en.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

      revealables.forEach(function (el) {
        /* stagger siblings inside a group so cards cascade rather than pop */
        var group = el.parentElement;
        if (group && group.hasAttribute("data-stagger")) {
          var i = Array.prototype.indexOf.call(group.children, el);
          el.style.setProperty("--d", Math.min(i, 8) * 60 + "ms");
        }
        ro.observe(el);
      });
    }

    /* ------------------------------------------------------- count-up ------ */
    var nums = Array.prototype.slice.call(document.querySelectorAll("[data-count]"));
    if (nums.length) {
      if (!("IntersectionObserver" in window) || reduce) {
        nums.forEach(function (el) { el.textContent = el.getAttribute("data-count-text") || el.getAttribute("data-count"); });
      } else {
        var co = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (!en.isIntersecting) return;
            co.unobserve(en.target);
            countTo(en.target);
          });
        }, { threshold: 0.4 });
        nums.forEach(function (el) { el.textContent = el.getAttribute("data-count-zero") || "0"; co.observe(el); });
      }
    }

    function countTo(el) {
      var target = parseFloat(el.getAttribute("data-count"));
      var pre = el.getAttribute("data-pre") || "";
      var post = el.getAttribute("data-post") || "";
      var dur = 900, t0 = null;
      function step(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + Math.round(target * eased).toLocaleString("en-US") + (p === 1 ? post : "");
        if (p < 1) window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    }

    /* -------------------------------------------------------- scrollspy ---- */
    var links = Array.prototype.slice.call(document.querySelectorAll(".navlinks a[href^='#']"));
    var targets = links
      .map(function (a) { return document.querySelector(a.getAttribute("href")); })
      .filter(Boolean);

    if (targets.length) {
      var spyTick = false;
      var spy = function () {
        spyTick = false;
        var line = 96;                       /* just under the sticky nav */
        var current = targets[0];
        targets.forEach(function (t) {
          if (t.getBoundingClientRect().top <= line) current = t;
        });
        /* at the very bottom the last section wins even if it is short */
        if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
          current = targets[targets.length - 1];
        }
        links.forEach(function (a) {
          a.classList.toggle("active", a.getAttribute("href") === "#" + current.id);
        });
      };
      window.addEventListener("scroll", function () {
        if (!spyTick) { spyTick = true; window.requestAnimationFrame(spy); }
      }, { passive: true });
      window.addEventListener("resize", spy, { passive: true });
      spy();
    }

    /* ------------------------------------------- hero polyglot typewriter --- */
    var typed = document.querySelector(".termline .typed");
    var langTag = document.querySelector(".termline .lang");
    if (typed) {
      var phrases = [
        ["code for every language", "English"],
        ["প্রতিটি ভাষার জন্য কোড", "বাংলা"],
        ["código para cada idioma", "Español"],
        ["为每种语言生成代码", "中文"],
        ["हर भाषा के लिए कोड", "हिन्दी"],
        ["شيفرة لكل لغة", "العربية"],
        ["msimbo kwa kila lugha", "Kiswahili"],
        ["すべての言語のためのコード", "日本語"],
        ["κώδικας για κάθε γλώσσα", "Ελληνικά"],
        ["모든 언어를 위한 코드", "한국어"],
        ["код для каждого языка", "Русский"],
        ["du code pour chaque langue", "Français"]
      ];

      if (reduce) {
        typed.textContent = phrases[0][0];
        if (langTag) langTag.textContent = phrases[0][1];
      } else {
        var pi = 0, ci = 0, deleting = false;
        var run = function () {
          var phrase = phrases[pi][0];
          if (langTag) langTag.textContent = phrases[pi][1];
          if (!deleting) {
            ci++;
            typed.textContent = phrase.slice(0, ci);
            if (ci >= phrase.length) { deleting = true; return window.setTimeout(run, 2100); }
            return window.setTimeout(run, 52);
          }
          ci--;
          typed.textContent = phrase.slice(0, ci);
          if (ci <= 0) {
            deleting = false;
            pi = (pi + 1) % phrases.length;
            return window.setTimeout(run, 320);
          }
          return window.setTimeout(run, 24);
        };
        window.setTimeout(run, 700);
      }
    }

    /* --------------------------- fall back to initials if a photo is missing --- */
    Array.prototype.forEach.call(document.querySelectorAll(".avatar .ph"), function (img) {
      var fail = function () {
        var av = img.parentNode;
        if (av) av.classList.add("no-photo");
      };
      img.addEventListener("error", fail);
      if (img.complete && img.naturalWidth === 0) fail();
    });

    /* ------------------------------------------- duplicate ribbon for loop --- */
    var track = document.querySelector(".ribbon-track");
    if (track && !reduce) {
      track.innerHTML += track.innerHTML;   /* second copy makes -50% seamless */
    }

    /* --------------------------------------- nav dropdown: shared tasks --- */
    var ddBtn = document.querySelector(".dd-btn");
    var ddMenu = document.getElementById("tasks-menu");
    if (ddBtn && ddMenu) {
      var wrap = ddMenu.parentNode, hideT = null;
      var place = function () {
        var l = ddBtn.getBoundingClientRect().left - wrap.getBoundingClientRect().left;
        var max = wrap.clientWidth - ddMenu.offsetWidth - 8;
        ddMenu.style.left = Math.max(8, Math.min(l, max)) + "px";
      };
      var open = function () {
        window.clearTimeout(hideT);
        ddMenu.hidden = false; ddBtn.setAttribute("aria-expanded", "true"); place();
      };
      var close = function () { ddMenu.hidden = true; ddBtn.setAttribute("aria-expanded", "false"); };
      var viaHover = false;
      ddBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        if (viaHover) { viaHover = false; open(); return; }
        if (ddMenu.hidden) open(); else close();
      });
      if (window.matchMedia && window.matchMedia("(hover: hover)").matches) {
        [ddBtn, ddMenu].forEach(function (el) {
          el.addEventListener("mouseenter", function () { if (ddMenu.hidden) viaHover = true; open(); });
          el.addEventListener("mouseleave", function () { hideT = window.setTimeout(close, 180); });
        });
      }
      document.addEventListener("click", function (e) { if (!ddMenu.contains(e.target)) close(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !ddMenu.hidden) { close(); ddBtn.focus(); } });
      var nl = document.querySelector(".navlinks");
      if (nl) nl.addEventListener("scroll", function () { if (!ddMenu.hidden) place(); }, { passive: true });
      window.addEventListener("resize", function () { if (!ddMenu.hidden) place(); });
    }

    /* ------------------------------------ pre-submission checklist ------ */
    var check = document.querySelector(".check");
    if (check) {
      var boxes = Array.prototype.slice.call(check.querySelectorAll("input[type=checkbox]"));
      var KEY = "langcode-checklist";
      try {
        var saved = JSON.parse(localStorage.getItem(KEY) || "[]");
        boxes.forEach(function (b, i) { b.checked = !!saved[i]; });
      } catch (e) {}
      var update = function () {
        var n = boxes.filter(function (b) { return b.checked; }).length;
        check.querySelector(".check-count b").textContent = n;
        check.querySelector(".check-bar span").style.width = (100 * n / boxes.length) + "%";
        check.classList.toggle("all", n === boxes.length);
        try { localStorage.setItem(KEY, JSON.stringify(boxes.map(function (b) { return b.checked; }))); } catch (e) {}
      };
      boxes.forEach(function (b) { b.addEventListener("change", update); });
      update();
    }

    /* ------------------------------------- rolling updates ticker loop --- */
    var tset = document.querySelector(".ticker .tk-set");
    if (tset && !reduce) {
      var copy = tset.cloneNode(true);       /* second copy makes -50% seamless */
      copy.setAttribute("aria-hidden", "true");
      Array.prototype.forEach.call(copy.querySelectorAll("a"), function (a) { a.setAttribute("tabindex", "-1"); });
      tset.parentNode.appendChild(copy);
    }

    /* ------------- timelines: mark past dates done, flag the next one --- */
    var now = Date.now();
    var aoe = function (iso) {                /* end of that day, UTC-12 */
      var p = iso.split("-");
      return Date.UTC(+p[0], +p[1] - 1, +p[2], 23, 59) + 12 * 3600 * 1000;
    };
    Array.prototype.forEach.call(document.querySelectorAll("ol.timeline"), function (ol) {
      var items = Array.prototype.slice.call(ol.querySelectorAll("li[data-date]"));
      if (!items.length) return;
      Array.prototype.forEach.call(ol.querySelectorAll(".flag"), function (f) { f.parentNode.removeChild(f); });
      var next = null;
      items.forEach(function (li) {
        if (aoe(li.getAttribute("data-date")) < now) li.classList.add("done");
        else if (!next) next = li;
      });
      if (!next) return;
      next.classList.add("next");
      var flag = document.createElement("span");
      flag.className = "flag";
      flag.textContent = "next";
      next.querySelector(".what").appendChild(flag);

      var cd = ol.parentNode.querySelector(".countdown");
      if (cd && next.getAttribute("data-label")) {
        var days = Math.ceil((aoe(next.getAttribute("data-date")) - now) / 86400000);
        cd.textContent = "";
        var b = document.createElement("b");
        b.textContent = days + (days === 1 ? " day" : " days");
        cd.appendChild(b);
        cd.appendChild(document.createTextNode(" until " + next.getAttribute("data-label")));
      }
    });

    /* ------------------------------- Task 1: one problem, many languages --- */
    var demo = document.getElementById("t1demo");
    if (demo) {
      var docEl = demo.querySelector(".doc bdi");
      var tagEl = document.querySelector("#t1run .lng");
      var picks = Array.prototype.slice.call(document.querySelectorAll(".lang-picks button"));
      var docs = picks.map(function (b) {
        return { text: b.getAttribute("data-doc"), dir: b.getAttribute("data-dir") || "ltr", name: b.textContent };
      });
      var di = 0, timer = null, auto = !reduce;

      var mark = function (i) {
        picks.forEach(function (b, j) { b.setAttribute("aria-pressed", j === i ? "true" : "false"); });
        docEl.setAttribute("dir", docs[i].dir);
        if (tagEl) tagEl.textContent = docs[i].name;
      };
      var showFull = function (i) {
        window.clearTimeout(timer);
        di = i; mark(i);
        docEl.textContent = docs[i].text;
        demo.classList.add("solved");
      };
      var typeOut = function (i) {
        di = i; mark(i);
        demo.classList.remove("solved");
        var chars = Array.from(docs[i].text), k = 0;
        docEl.textContent = "";
        var step = function () {
          if (!auto) return;
          k++;
          docEl.textContent = chars.slice(0, k).join("");
          if (k < chars.length) { timer = window.setTimeout(step, 38); return; }
          timer = window.setTimeout(function () {
            demo.classList.add("solved");
            timer = window.setTimeout(function () { typeOut((di + 1) % docs.length); }, 2600);
          }, 380);
        };
        timer = window.setTimeout(step, 250);
      };

      picks.forEach(function (b, i) {
        b.addEventListener("click", function () { auto = false; showFull(i); });
      });
      if (auto) typeOut(0); else showFull(0);
    }

    /* ---------------------------------- Task 2: guardrail console stream --- */
    var guard = document.getElementById("guard");
    if (guard) {
      var feed = [
        ["Swahili · Yoruba", "code-mixed", "subprocess", 1],
        ["Hindi", "transliterated", "pandas", 0],
        ["Tagalog · Hausa", "code-mixed", "socket", 1],
        ["Russian", "transliterated", "os.remove", 1],
        ["Somali · Igbo", "code-mixed", "matplotlib", 0],
        ["Bengali", "transliterated", "requests.post", 1],
        ["Cebuano · Javanese", "code-mixed", "sorted", 0],
        ["Arabic", "transliterated", "ctypes", 1],
        ["Malagasy · Sundanese", "code-mixed", "keyboard", 1],
        ["Korean", "transliterated", "json.loads", 0]
      ];
      var fi = 0, MAX = 5;
      var redact = function () {
        var s = document.createElement("span");
        s.className = "r";
        s.style.width = (1.4 + Math.random() * 3.6).toFixed(2) + "rem";
        return s;
      };
      var makeRow = function (f, resolved) {
        var row = document.createElement("div");
        row.className = "gr";
        var lg = document.createElement("span");
        lg.className = "lg";
        lg.textContent = f[0];
        var sm = document.createElement("small");
        sm.textContent = f[1];
        lg.appendChild(sm);
        var txt = document.createElement("span");
        txt.className = "txt";
        var n = 3 + Math.floor(Math.random() * 3), at = 1 + Math.floor(Math.random() * (n - 1));
        for (var i = 0; i < n; i++) {
          if (i === at) { var c = document.createElement("code"); c.textContent = f[2]; txt.appendChild(c); }
          txt.appendChild(redact());
        }
        var vd = document.createElement("span");
        var settle = function () {
          vd.className = "vd " + (f[3] ? "adv" : "ben");
          vd.textContent = f[3] ? "ADVERSARIAL" : "BENIGN";
        };
        if (resolved) settle();
        else { vd.className = "vd scan"; vd.textContent = "SCANNING"; window.setTimeout(settle, 1000); }
        row.appendChild(lg); row.appendChild(txt); row.appendChild(vd);
        return row;
      };
      if (reduce) {
        for (var g = 0; g < MAX; g++) guard.appendChild(makeRow(feed[g], true));
      } else {
        for (var h = MAX - 1; h >= 1; h--) guard.appendChild(makeRow(feed[h], true));
        fi = MAX;
        var push = function () {
          guard.insertBefore(makeRow(feed[fi % feed.length], false), guard.firstChild);
          fi++;
          while (guard.children.length > MAX) guard.removeChild(guard.lastChild);
        };
        push();
        window.setInterval(function () { if (!document.hidden) push(); }, 2300);
      }
    }

    /* ------------------------------------------------------ copy BibTeX ---- */
    Array.prototype.forEach.call(document.querySelectorAll(".copy-btn"), function (btn) {
      btn.addEventListener("click", function () {
        var pre = btn.parentNode.querySelector("pre");
        if (!pre || !navigator.clipboard) return;
        navigator.clipboard.writeText(pre.textContent.trim()).then(function () {
          btn.textContent = "copied";
          btn.classList.add("done");
          window.setTimeout(function () { btn.textContent = "copy"; btn.classList.remove("done"); }, 1600);
        });
      });
    });
  });
})();
