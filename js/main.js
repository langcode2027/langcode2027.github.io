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
  });
})();
