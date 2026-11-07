# Prebuilt Tailwind CSS for published pages

The Research IDE and the Circuit-SETH explorer used the Tailwind v3 runtime script
(`cdn.tailwindcss.com`), which generates styles in the browser and cannot carry an
integrity hash. They now load a stylesheet generated ahead of time with Tailwind CSS
v3.4.19 (the v3 long-term-support release):

| Page | Configuration | Output |
| :--- | :--- | :--- |
| `Research_IDE/index.html` | `research-ide.config.cjs` (default theme, as before) | `Research_IDE/ide-tailwind.css` |
| `site/circuit-seth/explorer.html` | `explorer.config.cjs` (the page's original inline theme) | `site/circuit-seth/explorer-tailwind.css` |

`input.css` holds the same three layers the runtime script produced.

## Regenerate

Run this after adding or changing Tailwind classes in either page (needs Node.js and
npm registry access):

```sh
sh tools/pages/tailwind/build.sh
make -C Research_IDE lock-ide      # records the new ide-tailwind.css hash
make -C Research_IDE check
python3 -m unittest discover -s tools/pages/tests
```

Commit the regenerated CSS with the page change. The generated files start with a
comment naming this script; do not edit them by hand.

## Coverage notes

The build scans each page's own source, including class names inside its scripts.
A few class names in the pages have no Tailwind v3 rule and so had no effect with the
runtime script either: `bg-ide-bg`, `bg-ide-panel`, `border-ide-border`, `h-13`,
`py-0.2`, `prose`, `prose-invert` (IDE) and `grid-cols-16`, `sm:grid-cols-32`
(explorer). They are left as they are.
