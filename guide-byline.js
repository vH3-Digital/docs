(function () {
  function pageHeader() {
    return document.querySelector('[class*="@container/page-header"]');
  }

  function titleStack(header) {
    return header.querySelector('[class*="space-y-2.5"]');
  }

  function descriptionSlot(header) {
    return header.querySelector(".mt-2.text-lg");
  }

  var placing = false;

  function placeGuideByline() {
    var header = pageHeader();
    if (!header || placing) return;

    var source = document.querySelector(".mdx-content .guide-byline");
    var existing = header.querySelector(".guide-byline");
    if (!source && existing) return;
    if (!source) {
      if (existing) existing.remove();
      return;
    }
    if (existing === source) return;

    placing = true;
    try {
      header.querySelectorAll(".guide-byline").forEach(function (el) {
        if (el !== source) el.remove();
      });
      var stack = titleStack(header);
      var desc = descriptionSlot(header);
      if (stack) {
        stack.appendChild(source);
      } else if (desc) {
        header.insertBefore(source, desc);
      } else {
        header.appendChild(source);
      }
    } finally {
      placing = false;
    }
  }

  function run() {
    placeGuideByline();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }

  var obs = new MutationObserver(function () {
    run();
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();
