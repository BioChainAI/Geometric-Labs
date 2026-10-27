const test = require('node:test');
const assert = require('node:assert/strict');
const {webcrypto} = require('node:crypto');
const corpus = require('../official-corpus.js');
const fs = require('node:fs');
const catalog = JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'../official/CATALOG.json')));

test('actual catalog contains official releases and no archived predecessors', () => {
  const docs = corpus.validate(catalog);
  assert.equal(docs.length, 15);
  assert.ok(!docs.some(d => ['RP-0006','RP-0011'].includes(d.id)));
});
test('unofficial entries, duplicate identities and escaping source paths fail', () => {
  for (const mutate of [d => d.documents[0].release_status = 'research-draft',
      d => d.documents.push(d.documents[0]), d => d.documents[0].pdf_path = 'papers/%2e%2e/secret.pdf',
      d => d.documents[0].pdf_path = 'https://example.com/paper.pdf',
      d => d.documents[0].publication_url = 'javascript:alert(1)']) {
    const data = structuredClone(catalog); mutate(data);
    assert.throws(() => corpus.validate(data));
  }
});
test('metadata escapes source titles and does not claim audited baseline', () => {
  const doc = {...catalog.documents[0], title:'<img src=x onerror=alert(1)>'};
  const md = corpus.metadata(doc);
  assert.ok(!md.includes('<img'));
  assert.ok(md.includes('not an audited transcription'));
});
test('original PDF bytes require a matching SHA-256 and successful response', async () => {
  const bytes = Buffer.from('source fixture');
  const hash = Buffer.from(await webcrypto.subtle.digest('SHA-256', bytes)).toString('hex');
  const response = {ok:true, arrayBuffer:async()=>bytes};
  await corpus.verifiedBytes(response, hash, webcrypto);
  await assert.rejects(corpus.verifiedBytes(response, '0'.repeat(64), webcrypto), /mismatch/);
  await assert.rejects(corpus.verifiedBytes({ok:false,status:404}, hash, webcrypto), /404/);
});
