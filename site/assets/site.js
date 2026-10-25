'use strict';
const el = id => document.getElementById(id);
let snapshot = null;
let activeFilter = 'all';
let focusedSection = null;
function node(tag, text, cls) { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (cls) n.className = cls; return n; }
function link(text, href) { const a = node('a', text); a.href = href; return a; }
function renderAreas() {
  if (!snapshot) return;
  const query = el('search').value.trim().toLowerCase();
  const matchingPaths = snapshot.files.filter(f => f.path.toLowerCase().includes(query));
  const sectionsWithPaths = new Set(matchingPaths.map(f => f.section));
  const areas = snapshot.sections.filter(s => (activeFilter === 'all' || s.status === activeFilter) &&
    (!focusedSection || s.id === focusedSection) && (!query || (s.title + ' ' + s.role).toLowerCase().includes(query) || sectionsWithPaths.has(s.id)));
  const grid = el('section-grid'); grid.replaceChildren();
  for (const [index, section] of areas.entries()) {
    const card = node('article', undefined, 'project-card');
    const top = node('div', undefined, 'card-top'); top.append(node('span', String(snapshot.sections.indexOf(section) + 1).padStart(2, '0'), 'card-number'), node('span', section.status, 'badge ' + section.status));
    card.append(top, node('h3', section.title), node('p', section.role));
    const details = node('details'); details.append(node('summary', 'Scope & limitations'), node('p', section.limits)); card.append(details);
    const footer = node('div', undefined, 'card-footer'); footer.append(node('span', section.file_count + ' tracked files'), link('Explore source →', section.url)); card.append(footer); grid.append(card);
  }
  el('no-results').hidden = areas.length > 0;
  el('result-count').textContent = `${areas.length} of ${snapshot.sections.length} areas${focusedSection ? ' · selected from the development loop; choose All areas to reset' : ''}`;
  const allowed = new Set(areas.map(s => s.id)); const files = matchingPaths.filter(f => allowed.has(f.section));
  const list = el('file-list'); list.replaceChildren();
  for (const f of files) { const li = node('li'); li.append(link(f.path, f.url)); list.append(li); }
  el('path-count').textContent = `(${files.length} paths)`;
}
function activateFilter(value) {
  activeFilter = value; focusedSection = null;
  document.querySelectorAll('[data-filter]').forEach(b => { const on = b.dataset.filter === value; b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
  renderAreas();
}
function render(data) {
  snapshot = data;
  el('file-count').textContent = data.tracked_files;
  el('section-count').textContent = data.sections.length;
  el('paper-count').textContent = data.paper_entries;
  const evidence = data.evidence;
  el('recorded-tests').textContent = evidence.state === 'recorded' ? evidence.test_methods : '—';
  const line = el('source-line'); line.replaceChildren();
  line.append(node('span', data.preview_with_uncommitted_changes ? 'Uncommitted preview · ' : 'Source snapshot · '), link(data.source_commit.slice(0, 12), data.source_url), node('span', ' · scanned at build time'));
  if (evidence.state === 'recorded') {
    el('evidence-title').textContent = `${evidence.test_methods} test methods · ${evidence.packet_cases} packet cases`;
    el('evidence-description').textContent = `Saved ${evidence.date}. ${evidence.same_revision ? 'Evidence describes this source revision.' : 'Evidence describes an earlier audited revision; it is not a pass for this build.'}`;
    el('evidence-sha').textContent = evidence.source_commit.slice(0, 12);
    el('evidence-link').href = evidence.url;
  } else { el('evidence-title').textContent = 'Evidence not recorded'; el('evidence-description').textContent = evidence.message; }
  el('build-time').textContent = new Date(data.built_at).toLocaleString(undefined, { timeZone: 'America/Chicago', timeZoneName: 'short' });
  const activity = el('activity'); activity.replaceChildren();
  for (const commit of data.recent_commits) {
    const li = node('li'); const date = node('time', new Date(commit.date).toLocaleDateString(undefined, { timeZone: 'America/Chicago', month: 'short', day: 'numeric' })); date.dateTime = commit.date;
    li.append(date, link(commit.subject, commit.url), node('code', commit.sha.slice(0, 7))); activity.append(li);
  }
  renderAreas();
}
document.querySelectorAll('[data-filter]').forEach(b => b.addEventListener('click', () => activateFilter(b.dataset.filter)));
document.querySelectorAll('[data-focus]').forEach(b => b.addEventListener('click', () => {
  activateFilter('all'); focusedSection = b.dataset.focus; el('search').value = ''; renderAreas(); el('section-grid').scrollIntoView({ block: 'start', behavior: 'smooth' });
}));
el('search').addEventListener('input', renderAreas);
fetch('data/status.json').then(r => { if (!r.ok) throw new Error('snapshot unavailable'); return r.json(); }).then(render).catch(() => { el('load-error').hidden = false; el('source-line').textContent = 'Snapshot unavailable · source links remain available.'; });
