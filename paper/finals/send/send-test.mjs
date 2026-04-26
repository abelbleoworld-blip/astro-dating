#!/usr/bin/env node
import nodemailer from 'nodemailer';
import readline from 'node:readline';
import { Writable } from 'node:stream';

const TO = process.env.TEST_TO ?? 'turbo.a.turbo@gmail.com';
const FROM_USER = 'a@aadmitrieff.com';
const FROM_NAME = 'Alexander A. Dmitriev';
const HOST = 'smtp.timeweb.ru';
const PORT = 465;

async function promptHidden(question) {
  let muted = false;
  const muteStream = new Writable({
    write(chunk, encoding, cb) {
      if (!muted) process.stdout.write(chunk, encoding);
      cb();
    },
  });
  muteStream.isTTY = true;
  const rl = readline.createInterface({ input: process.stdin, output: muteStream, terminal: true });
  process.stdout.write(question);
  muted = true;
  return new Promise((resolve) => {
    rl.question('', (answer) => {
      rl.close();
      process.stdout.write('\n');
      resolve(answer);
    });
  });
}

const pass = process.env.SMTP_PASS || await promptHidden(`SMTP password for ${FROM_USER}: `);
if (!pass) { console.error('no password — abort'); process.exit(1); }

console.log(`\nconnecting ${HOST}:${PORT} as ${FROM_USER}…`);
const tx = nodemailer.createTransport({
  host: HOST, port: PORT, secure: true,
  auth: { user: FROM_USER, pass },
});

try {
  await tx.verify();
  console.log('SMTP auth OK');
} catch (e) {
  console.error(`SMTP auth FAILED: ${e.message}`);
  process.exit(2);
}

const now = new Date().toISOString();
const info = await tx.sendMail({
  from: `"${FROM_NAME}" <${FROM_USER}>`,
  to: TO,
  subject: `Test · aadmitrieff.com SMTP · ${now.slice(0, 16).replace('T', ' ')}Z`,
  text: [
    'Тестовое сообщение для проверки SMTP домена aadmitrieff.com.',
    '',
    `Отправитель:  ${FROM_USER}`,
    `Получатель:   ${TO}`,
    `SMTP:         ${HOST}:${PORT} (SSL)`,
    `Время (UTC):  ${now}`,
    '',
    'Если письмо дошло — DNS, MX, SPF, DKIM и SMTP-аутентификация работают.',
    'Конвейер рассылки экспертам (paper/finals/send/send.js) готов к работе.',
  ].join('\n'),
  headers: { 'X-Adaptiv-Test': 'sol1-smtp-verify' },
});

console.log(`\nsent · messageId=${info.messageId}`);
console.log(`accepted: ${info.accepted.join(',')}`);
console.log(`rejected: ${info.rejected.join(',') || '(none)'}`);
console.log(`response: ${info.response}`);
tx.close();
