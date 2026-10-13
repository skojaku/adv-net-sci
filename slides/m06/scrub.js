/* Frame scrubber for the m06 deck: the lecturer steps through a build himself.
 *
 * Markup (inside a slide):
 *
 *   <div class="fig scrub" data-at="1">
 *
 *   ![](figures/roma-to-graph.png)
 *
 *   </div>
 *
 * The image is the build's LAST frame, which is what the PDF/PNG export and the render gate
 * see. In the presentation (Marp's bespoke HTML), the script swaps in
 * figures/frames/<name>/00.png, adds a slider with ◀ ▶ under it, and lets the clicker step the
 * frames: Right / Down / PageDown / Space go forward, Left / Up / PageUp go back. Once the last
 * frame is shown, the keys move on as usual (the next bullet, then the next slide).
 *
 * data-at="k" (default 0): the frames start after the slide's first k bullets have been
 * revealed. So the order of clicks is: bullets 1..k, frames, the remaining bullets.
 *
 * Arriving at the slide from an earlier one starts at frame 0; coming back from a later one
 * shows the last frame, as Marp does with bullets.
 */
(function () {
  "use strict";

  var FWD = { ArrowRight: 1, ArrowDown: 1, PageDown: 1, " ": 1, Spacebar: 1 };
  var BACK = { ArrowLeft: 1, ArrowUp: 1, PageUp: 1 };
  var scrubs = [];

  function presenting() {
    return !!document.querySelector(".bespoke-marp-parent") ||
      document.body.hasAttribute("data-bespoke-view");
  }

  function probe(base, cb) {
    var urls = [];
    (function next(i) {
      if (i > 99) { cb(urls); return; }
      var u = base + (i < 10 ? "0" : "") + i + ".png";
      var im = new Image();
      im.onload = function () { urls.push(u); next(i + 1); };
      im.onerror = function () { cb(urls); };
      im.src = u;
    })(0);
  }

  function build(el) {
    var img = el.querySelector("img");
    if (!img) return;
    var src = img.getAttribute("src");
    var m = /^(.*\/)?([^\/]+)\.png$/.exec(src);
    if (!m) return;
    var base = (m[1] || "") + "frames/" + m[2] + "/";
    probe(base, function (urls) {
      if (urls.length < 2) return;
      var s = { el: el, img: img, urls: urls, i: urls.length - 1,
                at: parseInt(el.getAttribute("data-at") || "0", 10) };
      var bar = document.createElement("div");
      bar.className = "scrub-bar";
      var prev = document.createElement("button");
      prev.type = "button"; prev.className = "scrub-btn"; prev.textContent = "◀";
      prev.setAttribute("aria-label", "Previous frame");
      var range = document.createElement("input");
      range.type = "range"; range.min = "0"; range.max = String(urls.length - 1);
      range.step = "1"; range.className = "scrub-range";
      var nextb = document.createElement("button");
      nextb.type = "button"; nextb.className = "scrub-btn"; nextb.textContent = "▶";
      nextb.setAttribute("aria-label", "Next frame");
      var count = document.createElement("span");
      count.className = "scrub-count";
      bar.appendChild(prev); bar.appendChild(range); bar.appendChild(nextb); bar.appendChild(count);
      el.appendChild(bar);
      s.range = range; s.count = count;
      prev.addEventListener("click", function (e) { e.stopPropagation(); show(s, s.i - 1); });
      nextb.addEventListener("click", function (e) { e.stopPropagation(); show(s, s.i + 1); });
      range.addEventListener("input", function () { show(s, +range.value); });
      // keys pressed while the slider has focus belong to the deck, not to the slider
      range.addEventListener("keydown", function (e) { range.blur(); });
      scrubs.push(s);
      show(s, 0);
    });
  }

  function show(s, i) {
    i = Math.max(0, Math.min(s.urls.length - 1, i));
    s.i = i;
    s.img.src = s.urls[i];
    s.range.value = String(i);
    s.count.textContent = (i + 1) + "/" + s.urls.length;
  }

  function slideOf(el) {
    return el.closest("svg[data-marpit-svg]") || el.closest("section");
  }

  function isActive(s) {
    var sl = slideOf(s.el);
    return !!(sl && (sl.classList.contains("bespoke-marp-active") ||
                     (sl.closest && sl.closest(".bespoke-marp-active"))));
  }

  function activeScrub() {
    for (var k = 0; k < scrubs.length; k++) if (isActive(scrubs[k])) return scrubs[k];
    return null;
  }

  function fragments(s) {
    var sl = slideOf(s.el);
    var all = sl ? sl.querySelectorAll("[data-bespoke-marp-fragment]") : [];
    var on = 0;
    for (var k = 0; k < all.length; k++)
      if (all[k].getAttribute("data-bespoke-marp-fragment") === "active") on++;
    return on;
  }

  function onKey(e) {
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
    var s = activeScrub();
    if (!s) return;
    var on = fragments(s);
    if (FWD[e.key]) {
      if (on < s.at || s.i >= s.urls.length - 1) return;      // a bullet first, or done
      show(s, s.i + 1);
    } else if (BACK[e.key]) {
      if (on > s.at || s.i <= 0) return;                      // hide a later bullet first
      show(s, s.i - 1);
    } else {
      return;
    }
    e.preventDefault();
    e.stopImmediatePropagation();
    e.stopPropagation();
  }

  // Arriving from an earlier slide starts the build at frame 0; from a later one, at the end.
  var lastPage = null;
  function pageNow() {
    var m = /^#(\d+)/.exec(location.hash);
    return m ? +m[1] : 1;
  }
  function onSlideChange() {
    var p = pageNow();
    var forward = lastPage === null || p >= lastPage;
    lastPage = p;
    setTimeout(function () {
      var s = activeScrub();
      if (s) show(s, forward ? 0 : s.urls.length - 1);
    }, 0);
  }

  function init() {
    if (!presenting()) return;                     // the PDF/PNG export keeps the last frame
    var els = document.querySelectorAll(".scrub");
    for (var k = 0; k < els.length; k++) build(els[k]);
    window.addEventListener("keydown", onKey, true);
    window.addEventListener("hashchange", onSlideChange);
    lastPage = pageNow();
  }

  if (document.readyState === "complete") setTimeout(init, 50);
  else window.addEventListener("load", function () { setTimeout(init, 50); });
})();
