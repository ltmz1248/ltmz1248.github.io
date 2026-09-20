import test from 'node:test';
import assert from 'node:assert/strict';
import { ArticleLikes } from '../dist/likes.mjs';

function memoryStorage() {
  const values = new Map();
  return { getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value), removeItem: key => values.delete(key) };
}
const reply = (data, status = 200) => ({ ok: status >= 200 && status < 300, status, json: async () => data });

test('reading a missing article counter shows zero without creating a like', async () => {
  const calls = [];
  const counter = new ArticleLikes('test_missing', { fetcher: async url => { calls.push(url); return reply({ error: 'Key not found' }, 404); } });
  assert.equal(await counter.read(), 0);
  assert.equal(calls.length, 1);
  assert.match(calls[0], /\/get\//);
  assert.equal(counter.state(), null);
});

test('a new visitor reads the same server total; loading never increments it', async () => {
  let total = 0;
  const fetcher = async url => reply({ value: String(url.includes('/hit/') ? ++total : total) });
  const first = new ArticleLikes('test_shared', { fetcher, storage: memoryStorage() });
  assert.equal((await first.like()).count, 1);
  const second = new ArticleLikes('test_shared', { fetcher, storage: memoryStorage() });
  assert.equal(await second.read(), 1);
  assert.equal(total, 1);
  assert.equal((await second.like()).count, 2);
  assert.equal(await first.read(), 2);
});

test('double clicks and a page reload do not submit a second like', async () => {
  let hits = 0;
  const storage = memoryStorage();
  const fetcher = async url => { if (url.includes('/hit/')) hits++; return reply({ value: String(hits) }); };
  const counter = new ArticleLikes('test_dedup', { fetcher, storage });
  await Promise.all([counter.like(), counter.like()]);
  const reloaded = new ArticleLikes('test_dedup', { fetcher, storage });
  assert.equal(reloaded.state(), 'liked');
  await reloaded.like();
  assert.equal(hits, 1);
});

test('an explicit rate-limit rejection permits retry without recording a like', async () => {
  const counter = new ArticleLikes('test_rejected', { storage: memoryStorage(), fetcher: async () => reply({ error: 'Too many requests' }, 429) });
  await assert.rejects(counter.like());
  assert.equal(counter.state(), null);
});

test('a lost increment reply is not silently retried after a reload', async () => {
  let hits = 0;
  const storage = memoryStorage();
  const fetcher = async url => { if (url.includes('/hit/')) { hits++; throw new Error('Connection lost'); } return reply({ value: 1 }); };
  const first = new ArticleLikes('test_uncertain', { storage, fetcher });
  await assert.rejects(first.like());
  const reloaded = new ArticleLikes('test_uncertain', { storage, fetcher });
  assert.equal(reloaded.state(), 'pending');
  assert.equal((await reloaded.like()).count, 1);
  assert.equal(hits, 1);
});

test('bad service data is shown as an error instead of a fabricated zero', async () => {
  const counter = new ArticleLikes('test_invalid', { fetcher: async () => reply({ value: 'unavailable' }) });
  await assert.rejects(counter.read());
});

test('browser storage restrictions still permit a like and prevent session duplicates', async () => {
  let hits = 0;
  const storage = { getItem() { throw new Error('Blocked'); }, setItem() { throw new Error('Blocked'); } };
  const counter = new ArticleLikes('test_private', { storage, fetcher: async url => reply({ value: url.includes('/hit/') ? ++hits : hits }) });
  await counter.like();
  await counter.like();
  assert.equal(hits, 1);
  assert.equal(counter.state(), 'liked');
});
