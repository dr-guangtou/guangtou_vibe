function apply_theme(selected_theme) {
  const valid_theme = ["dark", "light", "auto"].includes(selected_theme)
    ? selected_theme
    : "dark";
  document.body.dataset.theme = valid_theme;
  document.querySelector('meta[name="color-scheme"]').content =
    valid_theme === "auto" ? "light dark" : valid_theme;
}

document.addEventListener("click", (event) => {
  if (!event.target.closest("button.theme-toggle")) return;
  event.stopImmediatePropagation();
  const next_theme = { dark: "light", light: "auto", auto: "dark" };
  const selected_theme = next_theme[document.body.dataset.theme] || "dark";
  apply_theme(selected_theme);
  try {
    localStorage.setItem("theme", selected_theme);
  } catch {}
}, true);

window.addEventListener("storage", (event) => {
  if (event.key === "theme" || event.key === null) {
    apply_theme(event.newValue);
  }
});
