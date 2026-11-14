# Bundled MathJax Assets

This directory contains MathJax 4.1.3 from the `mathjax` npm package and browser
assets from `@mathjax/mathjax-newcm-font` 4.1.3. Their package metadata declares
Apache-2.0 licensing. License files accompany the runtime and font package.

The runtime package is preserved as distributed. The font package includes its
CHTML and SVG browser assets and entry points. Build source files and example
applications from the font package are omitted. Package contents are otherwise
unmodified. `package-lock.json` records package versions and download integrity.

The ordinary Sphinx build copies these files into `_static/vendor/`. The MathJax
configuration points both the runtime and math-font paths at this publication.

Sources are [MathJax](https://github.com/mathjax/MathJax) and
[MathJax fonts](https://github.com/mathjax/MathJax-fonts). Retain the accompanying
license notices when copying or publishing the documentation.
