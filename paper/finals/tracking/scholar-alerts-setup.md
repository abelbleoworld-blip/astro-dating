# Tracking: ловим упоминания и цитирования SOL-1

**Цель:** автоматически узнавать о любом упоминании работы (цитата, репост, обсуждение) на разных языках и площадках.

## Слой 1 — Email replies (автоматизировано)

**Скрипт:** `imap-poll.js` рядом с этим файлом.
**Что делает:** раз в час подключается к `imap.timeweb.ru:993` под `a@aadmitrieff.com`, фильтрует входящие за 30 дней по списку адресатов из `../send/recipients.json`, новые ответы пишет в `inbox.jsonl`.
**Как запустить:**

```bash
cd ~/Documents/Projects/astro-dating/paper/finals/tracking
npm i imapflow
IMAP_USER=a@aadmitrieff.com IMAP_PASS=<from-timeweb> node imap-poll.js
```

**Cron:** `0 * * * * cd .../tracking && IMAP_USER=... IMAP_PASS=... node imap-poll.js >> imap.log 2>&1`

## Слой 2 — Google Scholar Alerts (ручная настройка, бесплатно)

В Google Scholar нет публичного API, но есть Alerts через RSS/email.

**Создать алерты** (по одному, на каждое):
1. Открыть https://scholar.google.com/
2. Зайти в Settings → Alerts
3. Создать 3 alert:
   - запрос: `"SOL-1" Dmitriev`
   - запрос: `"55 kyr" "five proxies" OR "5 proxies" solar`
   - запрос: `"2126 CE" Grand Solar Minimum`
4. Доставка — на a@aadmitrieff.com или в RSS-фид
5. Если RSS — URL вида `https://scholar.google.com/scholar_alerts?view_op=feed&hl=en&alert_id=...` — прокидывается в `imap-poll.js` (Gmail-стиль) или в отдельный RSS-poller.

## Слой 3 — Semantic Scholar API (бесплатно, до 100 RPS)

```bash
# Поиск по DOI Zenodo:
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=Dmitriev+SOL-1+solar+activity&fields=citationCount,influentialCitationCount,year"

# Прямая проверка цитирований Zenodo DOI:
curl "https://api.semanticscholar.org/graph/v1/paper/DOI:10.5281/zenodo.19638005?fields=citations"
```

Скрипт `scholar-poll.js` (TODO) дёргает раз в день, пишет дельту цитирований в `citations.jsonl`.

## Слой 4 — Web mentions (бесплатно через DuckDuckGo HTML)

Мониторинг упоминаний без API:

```bash
# Поиск по точной ссылке:
curl -s "https://duckduckgo.com/html/?q=%22aadmitrieff.com%2Fresearch%2Fsol1%22" | grep -oE 'https?://[^"]+' | sort -u

# Поиск автора+темы на разных языках:
for q in "Dmitriev SOL-1" "Дмитриев SOL-1" "ГПНТБ Дмитриев солнечная активность" "GPNTB Dmitriev solar minimum 2126"; do
  curl -s "https://duckduckgo.com/html/?q=$(jq -rn --arg s "$q" '$s|@uri')"
done
```

Скрипт `web-mentions.js` (TODO) — ежедневный краулер DDG-результатов, дельта в `mentions.jsonl`.

## Слой 5 — Backlinks через Yandex.Webmaster (для русского сегмента)

В кабинете Я.Вебмастера для домена aadmitrieff.com:
- Раздел «Внешние ссылки» → видно все сайты, которые сослались на нас
- Алерты включить «Уведомлять по почте о новых внешних ссылках»

## Слой 6 — Mention counts в социальных сетях (опционально)

- **Telegram:** парсинг публичных каналов через @ContextSearchBot или brand-monitoring сервисы (mention.com и пр. — платно)
- **Twitter/X:** API закрыт, бесплатно — только web-поиск (см. слой 4)
- **VK:** через VK API search (бесплатно с авторизацией)

## Сводная страница (Phase 2)

`paper/finals/tracking/dashboard.html` — простая HTML-страница, читает все `*.jsonl` через bridge (адаптик-стиль) или серверным скриптом, показывает таймлайн событий: ответ от X, упоминание Y, цитирование Z.

## Языки запросов

Для поиска упоминаний на разных языках использовать кириллицу + латиницу + транслит фамилий:

- RU: «Дмитриев», «ГПНТБ», «солнечный минимум 2126», «Альмагест 1022 звезды»
- EN: «Dmitriev», «GPNTB Russia», «SOL-1», «next Grand Solar Minimum 2126»
- DE: «Sonnenminimum 2126», «Dmitriev kosmogene»
- ES, FR, JA, AR, ZH — добавлять по мере появления первых упоминаний

## Что должно появиться в `paper/finals/tracking/` после первой недели

- `inbox.jsonl` — ответы экспертов
- `citations.jsonl` — Semantic Scholar дельты
- `mentions.jsonl` — DDG-краулер
- `seen-uids.json` — состояние IMAP-поллера
