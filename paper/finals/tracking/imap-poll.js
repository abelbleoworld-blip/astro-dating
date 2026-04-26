// IMAP poller for a@aadmitrieff.com — checks for replies from SOL-1 recipients.
// Read-only by default. Logs new replies to inbox.jsonl.
//
// Usage:
//   IMAP_USER=a@aadmitrieff.com IMAP_PASS=... node imap-poll.js
//
// Cron-friendly: idempotent via UID tracking in seen-uids.json.

import { ImapFlow } from 'imapflow';
import { readFile, writeFile, appendFile, access, constants } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const STATE_PATH = resolve(HERE, 'seen-uids.json');
const LOG_PATH = resolve(HERE, 'inbox.jsonl');
const RECIPIENTS_PATH = resolve(HERE, '../send/recipients.json');

const cfg = {
  host: process.env.IMAP_HOST ?? 'imap.timeweb.ru',
  port: +(process.env.IMAP_PORT ?? 993),
  secure: (process.env.IMAP_SECURE ?? 'true') === 'true',
  user: process.env.IMAP_USER,
  pass: process.env.IMAP_PASS,
};
if (!cfg.user || !cfg.pass) { console.error('IMAP_USER / IMAP_PASS required'); process.exit(1); }

const recipients = JSON.parse(await readFile(RECIPIENTS_PATH, 'utf8'));
const watchAddrs = new Set(recipients.map(r => r.to.toLowerCase()));

const seen = await loadJson(STATE_PATH, []);
const seenSet = new Set(seen);

const client = new ImapFlow({
  host: cfg.host, port: cfg.port, secure: cfg.secure,
  auth: { user: cfg.user, pass: cfg.pass },
  logger: false,
});

await client.connect();
const lock = await client.getMailboxLock('INBOX');
try {
  const since = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
  for await (const msg of client.fetch({ since }, { uid: true, envelope: true, internalDate: true })) {
    if (seenSet.has(msg.uid)) continue;
    const from = msg.envelope?.from?.[0]?.address?.toLowerCase() ?? '';
    if (!watchAddrs.has(from)) { seenSet.add(msg.uid); continue; }
    const ev = {
      ts: new Date().toISOString(),
      uid: msg.uid,
      from,
      subject: msg.envelope?.subject ?? '',
      received: msg.internalDate?.toISOString() ?? null,
      message_id: msg.envelope?.messageId ?? null,
    };
    await appendFile(LOG_PATH, JSON.stringify(ev) + '\n');
    console.log('NEW reply:', ev);
    seenSet.add(msg.uid);
  }
} finally {
  lock.release();
  await client.logout();
  await writeFile(STATE_PATH, JSON.stringify([...seenSet]));
}

async function loadJson(p, def) {
  try { await access(p, constants.R_OK); }
  catch { return def; }
  return JSON.parse(await readFile(p, 'utf8'));
}
