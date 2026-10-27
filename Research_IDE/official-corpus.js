/* Official publication metadata only. Local imports never join this collection. */
'use strict';
const OfficialCorpus = (() => {
  function validate(data) {
    if (!data || data.schema !== 'geometric-labs.official-corpus.v1' || !Array.isArray(data.documents)) {
      throw new Error('Unsupported official catalog');
    }
    const ids = new Set(), publications = new Set();
    for (const doc of data.documents) {
      if (!/^RP-\d{4}$/.test(doc.id) || ids.has(doc.id) || doc.release_status !== 'official-release' ||
          typeof doc.title !== 'string' || !doc.title.trim() || !/^[a-f0-9]{64}$/.test(doc.source_sha256)) {
        throw new Error('Invalid official document identity');
      }
      const publication = new URL(doc.publication_url);
      if (publication.protocol !== 'https:' || publication.host !== 'www.academia.edu' ||
          !publication.pathname.startsWith('/' + doc.publication_id + '/') ||
          !/^\d+$/.test(doc.publication_id) || publications.has(doc.publication_id) || publication.username || publication.password) {
        throw new Error('Invalid publication URL');
      }
      const path = decodeURIComponent(doc.pdf_path);
      if (!path.startsWith('papers/') || path.includes('\\') || /[?#\x00-\x1f]/.test(path) ||
          path.split('/').some(part => !part || part === '.' || part === '..') || !path.endsWith('.pdf') ||
          !Array.isArray(doc.tags) || !Array.isArray(doc.topics) || !Array.isArray(doc.relevance)) {
        throw new Error('Invalid official PDF path or labels');
      }
      ids.add(doc.id); publications.add(doc.publication_id);
    }
    return data.documents;
  }

  function metadata(doc) {
    const text = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return '# ' + text(doc.title) + '\n\n' +
      '> Official ecosystem publication, designated by the repository owner.\n' +
      '> This entry is source metadata, not an audited transcription. Open the PDF to inspect it.\n\n' +
      '[Academia publication](' + doc.publication_url + ')\n\n' +
      'Source SHA-256: `' + doc.source_sha256 + '`\n\n' +
      'Repositories: ' + doc.relevance.map(rel => text(rel.repository) + ' (' + text(rel.role) + ')').join(', ') + '\n\n' +
      'Labels: ' + [...new Set([...doc.tags, ...doc.topics])].map(text).join(', ') + '\n\n' +
      'Scientific review: ' + text(doc.review_level) + '. Lean: ' + text(doc.lean_status) + '.\n\n' +
      text(doc.source_note);
  }

  async function verifiedBytes(response, expectedHash, cryptoApi = globalThis.crypto) {
    if (!response.ok) throw new Error('PDF download failed (HTTP ' + response.status + ')');
    if (!cryptoApi || !cryptoApi.subtle) throw new Error('PDF hash checks require HTTPS or localhost');
    const bytes = await response.arrayBuffer();
    const digest = await cryptoApi.subtle.digest('SHA-256', bytes);
    const actual = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
    if (actual !== expectedHash) throw new Error('PDF source hash mismatch; import stopped');
    return bytes;
  }

  return {validate, metadata, verifiedBytes};
})();
if (typeof module !== 'undefined' && module.exports) module.exports = OfficialCorpus;
