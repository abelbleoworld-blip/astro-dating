# PC Predictor v0.1 — слой 4 Predictive Context

**Калибровано:** 2026-04-17 на твоей сессии — учитывает 7 паттернов твоей работы.
**Стек:** bash + curl + jq + Anthropic API (Claude Sonnet 4.6).

## Что делает

Каждые 2 часа (или по запросу):
1. Собирает контекст: git log + active quests + voice transcript last 4h + FOCUS-25 paths
2. Шлёт в Claude с calibrated PROMPT.md
3. Получает 1-3 next-best-actions в формате A/B/C (Min/Med/Max scope)
4. Сохраняет в `~/Documents/Projects/mesh-memory/predictions/yyyy-mm-dd-hh.md`
5. Опционально пушит preview в Telegram

## Запуск ручной (тест сейчас)

### 1. Установить jq (если нет)
```bash
brew install jq
```

### 2. Установить API ключ
```bash
export ANTHROPIC_API_KEY="sk-ant-..."  # твой ключ
# Чтобы постоянно — добавить в ~/.zshrc
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
```

### 3. Прогон
```bash
bash ~/Documents/Projects/astro-dating/predictor/predictor.sh
```

Output появится в `~/Documents/Projects/mesh-memory/predictions/yyyy-mm-dd_HH-MM.md`.

## Запуск автоматический (cron)

```bash
crontab -e
# Добавить строку:
0 */2 * * * ANTHROPIC_API_KEY=sk-ant-... bash /Users/macbookpro14/Documents/Projects/astro-dating/predictor/predictor.sh >> /tmp/predictor.log 2>&1
```

Каждые 2 часа предсказание появится в predictions/.

## Запуск на VPS Abel-HQ (production)

1. Скопировать на VPS:
   ```bash
   scp -i ~/.ssh/abel_hq_key -r ~/Documents/Projects/astro-dating/predictor root@72.56.107.21:/opt/
   ```
2. На VPS — clone mesh-memory + astro-dating, cron как выше
3. Telegram интеграция: установить TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID env vars

## Что в PROMPT.md калибровано

Из анализа 4-часовой сессии 2026-04-17 — 7 поведенческих паттернов:

| Паттерн | Predictor применение |
|---|---|
| Цикл предложить→выбрать | Всегда **3 варианта** A/B/C |
| Шкала 4-8 уровней | Структурирование в N-step ladder |
| Метатекст-копирование | Output в виде таблиц |
| Pivot к минимуму | Сразу Min+Med+Max scope |
| Запрос самооценки | Воскресенье утром — критический ревью |
| Концепт→практика | Каждое решение + Single Next Action ≤1ч |
| Время-критика | Без preambles, сразу действие |

## Output формат (что увидишь)

```markdown
## Контекст (1 предложение)
...

## Top 3 next actions

### A. [≤30 мин] ...
**Зачем:** ...
**Single next action:** `команда`

### B. [≤2ч] ...
### C. [≤1 день] ...

## ⚠️ Забытые обещания (если есть)
- ...

## 🔍 Critical week review (только воскресенье)
- ...
```

## Стоимость

- Sonnet 4.6: ~$3/M input + ~$15/M output
- Контекст: ~3000 input tokens
- Output: ~500 tokens
- 1 запуск ≈ $0.017
- 12 запусков/день × 30 дней = 360 запусков ≈ **$6/мес**

(Дешевле чем я раньше прикинул, потому что Sonnet, не Opus)

## Если переключить на Opus 4.6 для лучшего качества

- Opus: ~$15/M input + ~$75/M output
- 1 запуск ≈ $0.085
- 360/мес ≈ **$30/мес**

В PROMPT.md изменить `claude-sonnet-4-6` → `claude-opus-4-6`.

## Расширения (после v0.1)

- v0.2: добавить screen capture context (vision LLM описание скринов)
- v0.3: добавить calendar (EventKit) и упоминания в письмах
- v0.4: feedback loop (твои accept/reject влияют на промпт через auto-tuning)
- v0.5: cross-project context (знает про AILib, FMone, AEC одновременно)

## Откат / отключение

```bash
# Убрать cron
crontab -l | grep -v predictor.sh | crontab -

# Удалить файлы
rm -rf ~/Documents/Projects/astro-dating/predictor
rm -rf ~/Documents/Projects/mesh-memory/predictions
```
