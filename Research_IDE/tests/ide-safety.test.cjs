const test = require('node:test');
const assert = require('node:assert/strict');
const safety = require('../ide-safety.js');

// A stand-in for marked: paragraphs only, raw HTML passed through (as marked does).
const marked = {parse: text => text.split(/\n{2,}/).map(block => '<p>' + block + '</p>').join('\n')};
function recordingPurify() {
  const calls = [];
  return {calls, addHook() {}, sanitize(html, config) { calls.push({html, config}); return '[clean]' + html; }};
}

test('math spans are cut out before Markdown and restored as escaped text', () => {
  const source = 'Inline $a<b$ and $$\\frac{1}{2} <img src=x onerror=alert(1)>$$ end';
  const {text, spans} = safety.protectMath(source);
  assert.equal(spans.length, 2);
  assert.ok(!text.includes('<img'));
  const restored = safety.restoreMath('<p>' + text + '</p>', spans);
  assert.ok(restored.includes('$a&lt;b$'));
  assert.ok(restored.includes('&lt;img src=x onerror=alert(1)&gt;'));
  assert.ok(!restored.includes('<img'));
});

test('a forged token in the source cannot reinsert markup', () => {
  const {text, spans} = safety.protectMath('@@LATEX_TOKEN_0@@ $<b>x</b>$ @@LATEX_TOKEN_9@@');
  const restored = safety.restoreMath(text, spans);
  assert.equal(restored, '$&lt;b&gt;x&lt;/b&gt;$ $&lt;b&gt;x&lt;/b&gt;$ ');
});

test('rendered Markdown always passes through the sanitiser last, with the HTML-only profile', () => {
  const purify = recordingPurify();
  const out = safety.renderMarkdown('# T\n\n<img src=x onerror=alert(1)>\n\n$<script>x</script>$', {marked, purify});
  assert.equal(purify.calls.length, 1);
  const {html, config} = purify.calls[0];
  assert.ok(out.startsWith('[clean]'));
  assert.ok(html.includes('$&lt;script&gt;x&lt;/script&gt;$'), 'math restored as text before sanitising');
  assert.deepEqual(config.USE_PROFILES, {html: true});
  for (const tag of ['style', 'form', 'input', 'button', 'textarea', 'select']) assert.ok(config.FORBID_TAGS.includes(tag));
  for (const attr of ['style', 'class']) assert.ok(config.FORBID_ATTR.includes(attr));
  assert.equal(config.SANITIZE_NAMED_PROPS, true);
  assert.equal(config.ALLOW_DATA_ATTR, false);
});

test('without the sanitiser or parser the source is shown as escaped text', () => {
  const source = '<img src=x onerror=alert(1)> $x$';
  for (const libs of [{marked}, {purify: recordingPurify()}, {}, {marked: {parse: async () => '<p>x</p>'}, purify: recordingPurify()}]) {
    const out = safety.renderMarkdown(source, libs);
    assert.ok(out.startsWith('<pre'), JSON.stringify(Object.keys(libs)));
    assert.ok(out.includes('&lt;img src=x onerror=alert(1)&gt;'));
    assert.ok(!out.includes('<img'));
  }
});

// A sanitiser stand-in that records its hooks, and a minimal element for calling them.
function hookingPurify() {
  const hooks = {};
  return {hooks, addHook(name, fn) { (hooks[name] ||= []).push(fn); }, sanitize: html => html};
}
function element(tagName, attributes = {}) {
  const values = new Map(Object.entries(attributes));
  return {tagName, hasAttribute: n => values.has(n), getAttribute: n => (values.has(n) ? values.get(n) : null),
    setAttribute: (n, v) => values.set(n, String(v)), removeAttribute: n => values.delete(n)};
}

test('task-list markers render as text through one private Marked instance', () => {
  const made = [];
  class Marked { constructor(options) { made.push(options); } parse(text) { return '<p>' + text + '</p>'; } }
  const lib = {Marked, parse() { throw new Error('the shared parser must not be used'); }};
  safety.renderMarkdown('- [x] done', {marked: lib, purify: recordingPurify()});
  safety.renderMarkdown('- [ ] open', {marked: lib, purify: recordingPurify()});
  assert.equal(made.length, 1, 'instance reused');
  assert.equal(made[0].renderer, safety.MARKDOWN_RENDERER);
  assert.equal(safety.MARKDOWN_RENDERER.checkbox({checked: true}), '☑ ');
  assert.equal(safety.MARKDOWN_RENDERER.checkbox({checked: false}), '☐ ');
  assert.ok(safety.SANITIZE_CONFIG.FORBID_TAGS.includes('input'), 'form controls stay forbidden');
});

test('Markdown images from web addresses become links; local and data images stay images', () => {
  const {image} = safety.MARKDOWN_RENDERER;
  for (const href of ['figure.png', './a/b.png', '/img/c.png', 'data:image/png;base64,AAAA', 'blob:http://127.0.0.1/1']) {
    assert.equal(image({href, text: 'f'}), false, href);
  }
  const out = image({href: 'https://images.example.org/f.png?a=1&b="2"', text: '<b>fig</b>'});
  assert.ok(out.startsWith('<a href="https://images.example.org/f.png?a=1&amp;b=&quot;2&quot;"'), out);
  assert.ok(out.endsWith('[image: &lt;b&gt;fig&lt;/b&gt;]</a>'), out);
  for (const href of ['//images.example.org/f.png', 'HTTP://x/f.png', ' https://x/f.png', '\\\\x/f.png', 'ht\ntps://x/f.png', 'ftp://x/f.png']) {
    assert.ok(safety.isWebAddress(href), JSON.stringify(href));
  }
});

test('links within the document stay in the tab and point at the prefixed ids', () => {
  const purify = hookingPurify();
  safety.renderMarkdown('x', {marked, purify});
  safety.renderMarkdown('y', {marked, purify});
  assert.equal(purify.hooks.afterSanitizeAttributes.length, 1, 'hooks installed once per sanitiser');
  const [after] = purify.hooks.afterSanitizeAttributes;
  const local = element('A', {href: '#s1'}); after(local);
  assert.equal(local.getAttribute('href'), '#user-content-s1');
  assert.ok(!local.hasAttribute('target'));
  const prefixed = element('A', {href: '#user-content-s1'}); after(prefixed);
  assert.equal(prefixed.getAttribute('href'), '#user-content-s1');
  const outside = element('A', {href: 'https://example.org/page#s1'}); after(outside);
  assert.equal(outside.getAttribute('href'), 'https://example.org/page#s1');
  assert.equal(outside.getAttribute('target'), '_blank');
  assert.equal(outside.getAttribute('rel'), 'noopener noreferrer');
  assert.equal(safety.SANITIZE_CONFIG.SANITIZE_NAMED_PROPS, true, 'ids carry the user-content- prefix');
});

test('raw HTML images from web addresses lose their source; the alt text stays', () => {
  const purify = hookingPurify();
  safety.renderMarkdown('x', {marked, purify});
  const [upon] = purify.hooks.uponSanitizeAttribute;
  const kept = (tag, attrName, attrValue) => {
    const data = {attrName, attrValue, keepAttr: true}; upon(element(tag), data); return data.keepAttr;
  };
  assert.equal(kept('IMG', 'src', 'https://images.example.org/f.png'), false);
  assert.equal(kept('IMG', 'src', '//images.example.org/f.png'), false);
  assert.equal(kept('IMG', 'srcset', 'a.png 1x'), false);
  assert.equal(kept('SOURCE', 'srcset', 'https://images.example.org/f.png'), false);
  assert.equal(kept('IMG', 'src', 'data:image/png;base64,AAAA'), true);
  assert.equal(kept('IMG', 'src', 'figure.png'), true);
  assert.equal(kept('IMG', 'alt', 'figure'), true);
  assert.equal(kept('A', 'href', 'https://example.org/'), true);
});

test('stored API keys from earlier builds are removed; preferences stay', () => {
  const items = new Map([['gl_gemini_key', 'k1'], ['gl_openrouter_key', 'k2'], ['gl_ai_provider', 'gemini'], ['gl_ollama_url', 'http://localhost:11434/api/generate']]);
  const storage = {getItem: k => items.has(k) ? items.get(k) : null, removeItem: k => items.delete(k)};
  assert.deepEqual(safety.removeStoredApiKeys(storage), ['gl_gemini_key', 'gl_openrouter_key']);
  assert.deepEqual([...items.keys()], ['gl_ai_provider', 'gl_ollama_url']);
  assert.deepEqual(safety.removeStoredApiKeys(storage), [], 'nothing left to remove, so the notice is not repeated');
});

test('unavailable storage is tolerated', () => {
  assert.deepEqual(safety.removeStoredApiKeys(null), []);
  const blocked = {getItem() { throw new Error('SecurityError'); }, removeItem() { throw new Error('SecurityError'); }};
  assert.deepEqual(safety.removeStoredApiKeys(blocked), []);
});

test('Gemini requests carry the key in x-goog-api-key, never in the URL', () => {
  const {url, init} = safety.geminiRequest('example-model-1.0', 'fixture-key', {contents: []});
  assert.equal(url, 'https://generativelanguage.googleapis.com/v1beta/models/example-model-1.0:generateContent');
  assert.ok(!url.includes('fixture-key') && !url.includes('?'));
  assert.equal(init.method, 'POST');
  assert.equal(init.headers['x-goog-api-key'], 'fixture-key');
  assert.equal(init.body, '{"contents":[]}');
  assert.ok(!('x-goog-api-key' in safety.geminiRequest('example-model-1.0', '', {}).init.headers));
});

test('model names that could change the request path are refused', () => {
  for (const model of ['', '../files', 'a/b', 'a?b=c', 'a#b', 'a b', '.hidden', 'x'.repeat(101), null, 42]) {
    assert.throws(() => safety.geminiRequest(model, 'k', {}), /Invalid Gemini model name/, String(model));
  }
});
