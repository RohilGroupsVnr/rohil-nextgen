
/**
 * Rohil NextGen - Performance Optimizer
 * Safe image loading and rendering optimizations
 */

(function () {
  "use strict";

  function optimizeImages() {
    const images = document.querySelectorAll("img");

    images.forEach((img) => {
      // Preserve images that already have explicit loading settings
      const rect = img.getBoundingClientRect();

      // Images below the initial viewport can load lazily
      const isBelowFold = rect.top > window.innerHeight;

      if (
        isBelowFold &&
        !img.hasAttribute("loading")
      ) {
        img.setAttribute("loading", "lazy");
      }

      // Async decoding helps avoid blocking rendering
      if (!img.hasAttribute("decoding")) {
        img.setAttribute("decoding", "async");
      }
    });
  }

  function optimizeAnimations() {
    // Respect users who prefer reduced motion
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      document.documentElement.classList.add("reduce-motion");
    }
  }

  function initializeOptimizer() {
    optimizeImages();
    optimizeAnimations();
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      initializeOptimizer,
      { once: true }
    );
  } else {
    initializeOptimizer();
  }
})();
