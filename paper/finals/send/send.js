import { readFile, appendFile, access, constants } from 'node:fs/promises';
import { resolve, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { setTimeout as sleep } from 'node:timers/promises';
import nodemailer from 'nodemailer';

const HERE = dirname(fileURLToPath(import.meta.url));
const ARGV = new Set(process.argv.slice(2));
const DRY_RUN = !ARGV.has('--send');
const ONLY_ID = process.argv.find(a => a.startsWith('--only='))?.split('=')[1];

await loadEnvFile(resolve(HERE, '.env'));
const cfg = {
  host: process.env.SMTP_HOST,
  port: +process.env.SMTP_PORT,
  secure: process.env.SMTP_SECURE === 'true',
  user: process.env.SMTP_USER,
  pass: process.env.SMTP_PASS,
  senderName: process.env.SENDER_NAME ?? 'Alexander A. Dmitriev',
  attachmentPath: resolve(HERE, process.env.ATTACHMENT_PATH ?? '../../SOL1-Publication.pdf'),
  sendDelayMs: +(process.env.SEND_DELAY_MS ?? 60000),
  logPath: resolve(HERE, process.env.LOG_PATH ?? '../sent.jsonl'),
};

const recipients = JSON.parse(await readFile(resolve(HERE, 'recipients.json'), 'utf8'));
const queue = ONLY_ID ? recipients.filter(r => r.id === ONLY_ID) : recipients;

console.log(`mode: ${DRY_RUN ? 'DRY-RUN' : 'LIVE SEND'}`);
console.log(`recipients in queue: ${queue.length}`);
console.log('');

const blockers = await preflight(queue, cfg);
if (blockers.length) {
  console.error('blockers detected — aborting:');
  for (const b of blockers) console.error('  -', b);
  process.exit(1);
}

const transporter = DRY_RUN ? null : nodemailer.createTransport({
  host: cfg.host, port: cfg.port, secure: cfg.secure,
  auth: { user: cfg.user, pass: cfg.pass },
});
if (transporter) await transporter.verify();

let i = 0;
for (const r of queue) {
  i++;
  const cover = await readFile(resolve(HERE, r.cover_md), 'utf8');
  const body = stripFrontmatter(cover);
  const mail = {
    from: `"${cfg.senderName}" <${cfg.user}>`,
    to: r.to,
    subject: r.subject,
    text: body,
    attachments: [{ filename: basename(cfg.attachmentPath), path: cfg.attachmentPath }],
    headers: { 'X-Adaptiv-Campaign': 'sol1-2026-04', 'X-Adaptiv-Recipient-Id': r.id },
  };

  console.log(`[${i}/${queue.length}] ${r.id} → ${r.to}`);
  console.log(`  subject: ${r.subject}`);
  console.log(`  body: ${body.length} chars · attachment: ${basename(cfg.attachmentPath)}`);

  if (DRY_RUN) {
    console.log('  DRY-RUN — not transmitting');
    await audit(cfg.logPath, { ts: ts(), id: r.id, to: r.to, status: 'dry-run' });
  } else {
    try {
      const info = await transporter.sendMail(mail);
      console.log(`  sent · messageId=${info.messageId} · accepted=${info.accepted.join(',')} · rejected=${info.rejected.join(',') || 'none'}`);
      await audit(cfg.logPath, { ts: ts(), id: r.id, to: r.to, status: 'sent', messageId: info.messageId, accepted: info.accepted, rejected: info.rejected });
    } catch (e) {
      console.error(`  FAIL: ${e.message}`);
      await audit(cfg.logPath, { ts: ts(), id: r.id, to: r.to, status: 'fail', error: e.message });
    }
    if (i < queue.length) {
      console.log(`  sleeping ${cfg.sendDelayMs / 1000}s before next…`);
      await sleep(cfg.sendDelayMs);
    }
  }
  console.log('');
}

if (transporter) transporter.close();
console.log('done.');

// --- helpers ---

async function loadEnvFile(p) {
  try { await access(p, constants.R_OK); } catch { return; }
  const content = await readFile(p, 'utf8');
  for (const line of content.split('\n')) {
    const m = line.match(/^([A-Z_]+)=(.*)$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
}

async function preflight(queue, cfg) {
  const out = [];
  if (queue.length === 0) out.push('queue is empty (check --only=<id> or recipients.json)');
  for (const r of queue) {
    if (r.verified === false) out.push(`recipient ${r.id} marked verified=false (${r.verified_source})`);
  }
  if (!DRY_RUN) {
    if (!cfg.host || !cfg.user || !cfg.pass) out.push('SMTP_HOST / SMTP_USER / SMTP_PASS required for --send');
    try { await access(cfg.attachmentPath, constants.R_OK); }
    catch { out.push(`attachment not readable: ${cfg.attachmentPath}`); }
  }
  return out;
}

function stripFrontmatter(md) {
  const lines = md.split('\n');
  let i = 0;
  while (i < lines.length && (lines[i].startsWith('**') || lines[i].trim() === '' || lines[i].trim() === '---')) i++;
  return lines.slice(i).join('\n').trim();
}

async function audit(p, ev) {
  await appendFile(p, JSON.stringify(ev) + '\n');
}

function ts() { return new Date().toISOString(); }
