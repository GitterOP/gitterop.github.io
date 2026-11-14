(() => {
  "use strict";

  const storageKey = "jd-color-theme";
  const root = document.documentElement;
  const colors = { light: "#f8f8f3", dark: "#141b1b" };
  let theme = "dark";

  try {
    const saved = localStorage.getItem(storageKey);
    if (saved === "light" || saved === "dark") theme = saved;
  } catch {
    // The theme remains usable when browser storage is unavailable.
  }

  function applyTheme(value) {
    root.dataset.theme = value;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = colors[value];

    const button = document.getElementById("theme-toggle");
    if (button) {
      const next = value === "dark" ? "light" : "dark";
      const label = `Switch to ${next} theme`;
      button.setAttribute("aria-label", label);
      button.title = label;
      button.querySelector(".theme-toggle-label").textContent = next === "light" ? "Light" : "Dark";
    }
  }

  // Apply the saved palette before the stylesheet is loaded to avoid a flash.
  applyTheme(theme);

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("theme-toggle");
    if (!button) return;
    button.hidden = false;
    applyTheme(theme);

    button.addEventListener("click", () => {
      theme = root.dataset.theme === "dark" ? "light" : "dark";
      applyTheme(theme);
      try {
        localStorage.setItem(storageKey, theme);
      } catch {
        // Switching still works for this page without persistent storage.
      }
    });
  });
})();
