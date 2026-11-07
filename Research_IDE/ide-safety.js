/* Rendering and credential helpers for the Research IDE. No network access, no storage writes. */
'use strict';
const IdeSafety = (() => {
  // Earlier IDE builds kept these entries in localStorage. API keys now live in page memory only.
  const STORED_KEY_ITEMS = ['gl_gemini_key', 'gl_openrouter_key'];
  const GEMINI_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/';
  const MATH_SPANS = /(\$\$[\s\S]*?\$\$)|(\\\[[\s\S]*?\\\])|(\\begin\{(equation\*?|align\*?|aligned|gather\*?|multline\*?|pmatrix|bmatrix|vmatrix|cases)\}[\s\S]*?\\end\{\4\})|(\\\([\s\S]*?\\\))|(\$(?!\$)[^\$\n]+?\$)/g;
  const MATH_TOKEN = /@@LATEX_TOKEN_(\d+)@@/g;

  // Markdown output is HTML only: no SVG/MathML, scripts, styles, forms or classes. KaTeX renders
  // math into the sanitised tree afterwards, from text nodes, so formulas still typeset.
  const SANITIZE_CONFIG = Object.freeze({
    USE_PROFILES: {html: true},
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'option'],
    FORBID_ATTR: ['style', 'class'],
    ALLOW_DATA_ATTR: false,
    SANITIZE_NAMED_PROPS: true
  });
  // Prefix the sanitiser adds to id and name values (SANITIZE_NAMED_PROPS).
  const NAMED_PROP_PREFIX = 'user-content-';
  const IMAGE_TAGS = new Set(['IMG', 'SOURCE']);

  function escapeHtml(value) {
    return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  // Cut LaTeX spans out before Markdown parsing so Markdown does not alter them.
  function protectMath(markdown) {
    const spans = [];
    const text = String(markdown).replace(MATH_SPANS, match => {
      spans.push(match);
      return `@@LATEX_TOKEN_${spans.length - 1}@@`;
    });
    return {text, spans};
  }

  // Put the spans back as text (escaped), never as markup.
  function restoreMath(html, spans) {
    return String(html).replace(MATH_TOKEN, (_, index) => escapeHtml(spans[Number(index)] ?? ''));
  }

  // The page's CSP (img-src 'self' data: blob:) refuses images from web addresses, so the preview never
  // asks the browser for them.
  function isWebAddress(url) {
    const value = String(url ?? '').replace(/[\t\n\r]/g, '').trim().replace(/\\/g, '/');
    return value.startsWith('//') || (/^[a-z][a-z0-9+.-]*:/i.test(value) && !/^(data|blob):/i.test(value));
  }

  // Markdown renderer changes, used on a private Marked instance.
  const MARKDOWN_RENDERER = Object.freeze({
    // GFM task markers become text: form controls are not allowed in the preview.
    checkbox({checked}) {
      return checked ? '\u2611 ' : '\u2610 ';
    },
    // An image from a web address becomes a link to it; other images render as usual.
    image({href, text}) {
      if (!isWebAddress(href)) return false;
      return `<a href="${escapeHtml(href)}" title="Image from another site, not loaded in the preview">` +
        `[image: ${escapeHtml(text || href)}]</a>`;
    }
  });

  const parsers = new WeakMap();
  function markdownParser(marked) {
    if (typeof marked.Marked !== 'function') return marked;
    if (!parsers.has(marked)) parsers.set(marked, new marked.Marked({renderer: MARKDOWN_RENDERER}));
    return parsers.get(marked);
  }

  const hooked = new WeakSet();
  function installHooks(purify) {
    if (hooked.has(purify) || typeof purify.addHook !== 'function') return;
    // Raw HTML images: a source from a web address is dropped (the alt text stays), and so is srcset.
    purify.addHook('uponSanitizeAttribute', (node, data) => {
      if (IMAGE_TAGS.has(node.tagName) &&
          (data.attrName === 'srcset' || (data.attrName === 'src' && isWebAddress(data.attrValue)))) {
        data.keepAttr = false;
      }
    });
    purify.addHook('afterSanitizeAttributes', node => {
      if (node.tagName !== 'A' || !node.hasAttribute('href')) return;
      const href = node.getAttribute('href').trim();
      if (href.startsWith('#')) {
        // A link within the document stays in this tab and points at the prefixed id.
        const id = href.slice(1);
        if (id && !id.startsWith(NAMED_PROP_PREFIX)) node.setAttribute('href', '#' + NAMED_PROP_PREFIX + id);
        node.removeAttribute('target');
        return;
      }
      // Other links open in a new tab so following one never discards the in-memory session.
      node.setAttribute('target', '_blank');
      node.setAttribute('rel', 'noopener noreferrer');
    });
    hooked.add(purify);
  }

  function plainText(text) {
    return '<pre class="whitespace-pre-wrap font-mono text-xs">' + escapeHtml(text) + '</pre>';
  }

  // Markdown + LaTeX source to sanitised HTML. If the parser or sanitiser is missing, the source is
  // shown as escaped text instead.
  function renderMarkdown(markdown, libs = {}) {
    const {marked, purify} = libs;
    if (!purify || typeof purify.sanitize !== 'function' || !marked || typeof marked.parse !== 'function') {
      return plainText(markdown);
    }
    installHooks(purify);
    const {text, spans} = protectMath(markdown);
    const html = markdownParser(marked).parse(text);
    if (typeof html !== 'string') return plainText(markdown);
    return String(purify.sanitize(restoreMath(html, spans), SANITIZE_CONFIG));
  }

  // Remove API keys saved by earlier builds. Returns the item names removed, never their values.
  function removeStoredApiKeys(storage) {
    const removed = [];
    try {
      for (const name of STORED_KEY_ITEMS) {
        if (storage.getItem(name) !== null) {
          storage.removeItem(name);
          removed.push(name);
        }
      }
    } catch (error) {
      // Storage unavailable (blocked or private mode): nothing can have been kept there.
    }
    return removed;
  }

  // Gemini request with the key in the x-goog-api-key header, never in the URL.
  function geminiRequest(model, apiKey, payload) {
    if (typeof model !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$/.test(model)) {
      throw new Error('Invalid Gemini model name');
    }
    const headers = {'Content-Type': 'application/json'};
    if (apiKey) headers['x-goog-api-key'] = apiKey;
    return {
      url: GEMINI_ENDPOINT + model + ':generateContent',
      init: {method: 'POST', headers, body: JSON.stringify(payload)}
    };
  }

  return {STORED_KEY_ITEMS, SANITIZE_CONFIG, MARKDOWN_RENDERER, escapeHtml, protectMath, restoreMath,
    isWebAddress, renderMarkdown, removeStoredApiKeys, geminiRequest};
})();
if (typeof module !== 'undefined' && module.exports) module.exports = IdeSafety;
