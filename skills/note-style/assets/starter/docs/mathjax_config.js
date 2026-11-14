const note_style_root_url = new URL(
  document.documentElement.getAttribute("data-content_root") || "./",
  document.baseURI,
);

window.MathJax = window.MathJax || {};
window.MathJax.output = {
  ...window.MathJax.output,
  font: "mathjax-newcm",
  fontPath: new URL("_static/vendor/mathjax_newcm_font", note_style_root_url).href,
};
