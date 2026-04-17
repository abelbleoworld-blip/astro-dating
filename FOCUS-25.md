# FOCUS-25 — активное ядро 25% (что реально работает)
**ВАЖНО:** Этот файл будущие Claude-сессии читают **ПЕРВЫМ**.
Не тратьте токены на 75% archive (см. секцию ниже). Работаем только над 4 путями.
**Обновлено:** 2026-04-17. Ревью: каждое воскресенье.
## 4 экспоненциальных пути (что делаем)
| ID | Путь | Single Next Action | Дедлайн | Статус |
|---|---|---|---|---|
| **P1** | Astro-dating → reference | Письмо Дамбису + arXiv endorsement | 2026-04-19 | ◻ черновик готов в `letters/dambis-2026-04.md` |
| **P2** | 2ⁿ → personal OS | Применить к AILib биллингу (256 строк, 4×64) | 2026-04-22 | ◻ не начато |
| **P3** | PC → critical infra | Voice on-demand (`voice` команда) | 2026-04-17 ✅ | ✅ работает: `voice`, `v`, см. `pilot/day2/voice-on-demand.md` |
| **P4** | Thought leadership | Telegram-пост про ARCHITECTURE-2N + L8 | 2026-04-19 | ◻ черновик в `social/telegram-post-2n.md` |
## 25% активные артефакты (~10 файлов)
- `ARCHITECTURE-2N.md` — манифест 2ⁿ (требует фикса противоречия с L8, см. open issues)
- `docs/lectures/L8-multi-fractal.md` — главный концептуальный вклад
- `docs/lectures/INDEX.md` — навигационный хаб
- `docs/anchors/S1-iching-dna.md` — рабочий шаблон 64-строчного якоря
- `docs/L3-roadmap.md` — путь к peer-review (P1 критичный)
- `docs/PREDICTIVE-CONTEXT.md` — план PC v0.1 (scope урезать до Whisper-only)
- `pilot/day2/setup-whisper-mac.sh` + `whisper-loop.sh` + plist — единственный runnable PC компонент
- `letters/dambis-2026-04.md` — черновик ключевого письма (P1)
- `social/telegram-post-2n.md` — черновик публичного анонса (P4)
- Memory: `architecture_2n.md`, `feedback_external_verification.md`, `lectures_pilot_plus.md`
## 75% archive (НЕ работаем, но не удалено)
- `docs/discussion/coding-convergence.md` — спекулятивная обёртка UCC
- `docs/publishing/MATRIX.md` — преждевременная матрица 11×14, нет данных
- `docs/publishing/wikipedia/STRATEGY.md` — W2 откладывается на 6-12 мес
- `docs/MESH-DISTRIBUTION.md` — 8×8 mesh преждевременно (Boox нет, iMac не настроен)
- `docs/lectures/SESSION-2026-04-17.md` — самореференция, не actionable
- 48 placeholder-квестов в `.game/state.json` (anchor_new_17..64) — карго-культ числа
- `pilot/day2/setup-beelink.sh` — Beelink интеграция не critical для экспоненты
- `pilot/day2/com.user.pilot-day2-deadline.plist` — будильник работает в launchd, в repo не нужен
- D1 (anchors/D1-instrument-information-density.md) в текущей форме 61 строки
- `memory/astro-dating.md` — выводится из repo
## Open issues (требуют фикса)
- [ ] **ARCHITECTURE-2N.md секция «принцип»** убрать «только 2ⁿ стабильна», заменить на «оптимум для информационных иерархий, для других доменов см. L8»
- [ ] **PREDICTIVE-CONTEXT.md scope** урезать с 6 слоёв до v0.1 минимума (Whisper + ручной обзор)
- [ ] **Стоимость PC пересчитать** ($50/мес → реально $300/мес если Opus каждые 2 часа)
- [ ] **Boox**: купить или зафиксировать что P3 откладывается без устройства
## Решающие триггеры активации экспоненты
| Путь | Триггер «запустилась» | Если запустилась → следующий шаг |
|---|---|---|
| P1 | Дамбис ответил содержательно | arXiv submission → JHA → Med.Arch |
| P2 | AILib биллинг работает в 256 строк | Перенос принципа на FMone, AEC |
| P3 | Whisper неделю накапливает контекст без сбоев | Добавить второй слой (index или state) |
| P4 | Telegram-пост получил 10+ репостов/комментариев | Habr-статья на 2000 слов |
## Если ничего не запустилось через 30 дней
Пересмотр путей: возможно ставку нужно перенести на P2/P4 (быстрее активируются) и отказаться от P1 (peer-review цикл годами) и P3 (capital-intensive).
## Для будущих Claude-сессий — протокол
1. Прочитать ЭТОТ файл первым (FOCUS-25.md)
2. Если запрос пользователя касается 75% archive — спросить «зачем сейчас?» прежде чем работать
3. Если запрос касается 25% активного — работать без предисловий
4. Любое НОВОЕ предложение оценивать через призму P1-P4: усиливает ли путь экспоненты?
5. Если новое предложение не питает ни один из 4 путей — предложить отложить или применить к AILib/FMone (другие проекты)
