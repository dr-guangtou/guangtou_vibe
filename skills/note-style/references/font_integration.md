# Preferred Chinese Font Integration

The owner prefers XiQueSongTiJF_std, also named XiquesongtiJF in its PostScript
metadata. The supplied file is a Regular TrueType font containing Simplified and
Traditional Chinese. Its source is `~/Documents/fonts/喜鹊宋体简繁版.ttf`.

The supplied two-page authorization dated 2024-01-21 grants a perpetual personal
commercial license. Section 2 includes website publishing among permitted uses.
Section 3 restricts modification/distribution of font files and directs embedded
uses to the foundry. These clauses leave downloadable webfont delivery and WOFF2
conversion/subsetting unclear. Obtain the foundry's clarification for those uses
before including the binary in public assets or a redistributed skill.

The authorization itself is a private document retained by the owner. Its personal
identifiers and document binary are kept outside this transferable package.

## Web delivery

When the license permits it, serve the webfont from the publication's own static
assets using `@font-face`. WOFF2 conversion and text-based subsetting can reduce
transfer size if the license allows those transformations. Measure the resulting
files and verify that punctuation, mathematical context, and all required Chinese
characters remain covered.

A font-face declaration would take the following shape after an authorized WOFF2
file is placed at `_static/fonts/xique_songti.woff2`.

```css
@font-face {
  font-family: "note_style_songti";
  src: url("fonts/xique_songti.woff2") format("woff2");
  font-style: normal;
  font-weight: 400;
  font-display: swap;
}
```

This URL assumes the declaration is in `_static/note_style.css`. Configure Furo's
body font stack to include this family and retain suitable Latin and Chinese
fallbacks. Use the supplied Regular face at its actual weight. Assess headings
and bold text separately when additional licensed weights are unavailable.

Publishing a webfont delivers the font data to visitors' browsers. The license
must cover that delivery. A font's embedded family names and technical embedding
flags help with implementation, while the actual authorization terms govern use.

The current skill includes the configuration example and fallback fonts. The
preferred font file is supplied separately under the applicable license.

A focused licensing question for the foundry is whether the personal license
covers serving this font through `@font-face` on the owner's website, including
browser downloads, WOFF2 conversion, and project-specific subsetting.
