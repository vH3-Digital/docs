(function () {
  var SURFACE_TAGS = {
    Connie: "connie",
    Connect: "connect",
    API: "api",
    Integrations: "integrations",
    Platform: "platform",
  };

  function slugFor(text) {
    return SURFACE_TAGS[text.trim()] || null;
  }

  function paintFilters(root) {
    var scope = root || document;
    var nodes = scope.querySelectorAll(
      "#changelog-filters button, #changelog-filters [role='checkbox'], #changelog-filters label, #changelog-filters-content button, #changelog-filters-content label"
    );
    nodes.forEach(function (el) {
      var slug = slugFor(el.textContent || "");
      if (!slug) return;
      el.classList.add("vh3-changelog-tag", "vh3-changelog-tag--" + slug);
    });
  }

  function hidePlainUpdateTags(root) {
    var scope = root || document;
    scope.querySelectorAll('[data-component-part="update"]').forEach(function (update) {
      var label = update.querySelector('[data-component-part="update-label"]');
      var description = update.querySelector('[data-component-part="update-description"]');
      if (!label || !description) return;
      var node = label.nextElementSibling;
      while (node && node !== description) {
        var text = (node.textContent || "").replace(/\s+/g, " ").trim();
        var parts = text.split(" ").filter(Boolean);
        var allSurface = parts.length > 0 && parts.every(function (p) {
          return Object.prototype.hasOwnProperty.call(SURFACE_TAGS, p);
        });
        if (allSurface) {
          node.classList.add("vh3-hide-plain-update-tags");
        }
        node = node.nextElementSibling;
      }
    });
  }

  function run() {
    paintFilters(document);
    hidePlainUpdateTags(document);
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
