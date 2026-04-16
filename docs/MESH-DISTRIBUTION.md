# MESH-DISTRIBUTION — план распределения работ по 8 машинам и 8 ролям

**Статус:** принят 2026-04-17. Пилот: 1 неделя.
**Связан с:** `ARCHITECTURE-2N.md` (принцип), mesh-memory (канал синхронизации).
**Размер:** ~256 строк (модуль документации).

## 1. Принцип распределения

Mesh из 8 машин × 8 ролей = 64 ячейки. Никакая отдельная машина не делает всё. Каждая занимает свою нишу по 3 параметрам: время суток, тип работы, контактная зона с пользователем.

**Время:** Mac работает с тобой (9-18). Beelink работает за тебя (ночь). VPS работает всегда. Mobile ловит моменты.

**Тип:** креатив (Mac), исполнение (Beelink), дублирование (iMac), оркестрация (VPS), capture (Mobile).

**Контакт:** Mac — основной. iPhone — голосовой. OPPO — mesh-фон. VPS — невидимы, только digest. Beelink — отчёт утром.

## 2. Карта 8×8

| Роль / Машина | Mac | iMac | Beelink | Boox | VPS-HQ | VPS-2 | iPhone | OPPO |
|---|---|---|---|---|---|---|---|---|
| **R1 Research** | Claude Opus deep | резерв Mac | data fetches | **PDF чтение peer-review** | Ollama | — | voice→AbelApp | Termux web/curl |
| **R2 Code** | Claude новые скрипты | резерв | execute + peer | — | batch long | hosting code | — | Termux mini-tasks |
| **R3 Review** | Claude content | dual-check | tests/lint/fmt | **длинные доки + рукописные пометки** | Grok+Gemini cross | — | mobile approve | screenshot annotate |
| **R4 Publish** | EN-перевод, статьи | — | build PDF/HTML | — | nginx host | nginx host | TG push consume | TG bot relay |
| **R5 Capture** | — | — | — | **рукописные заметки стилусом → mesh** | — | — | голос, фото | фото-бэкап ✅ |
| **R6 Notify** | — | — | — | — | dispatch | API relay | push consume | push relay |
| **R7 Backup** | mesh pull ✅ | mesh pull | mesh pull | git mirror Termux | mesh bare repo ✅ | git mirror | — | git mirror Termux |
| **R8 Orchestrate** | — | — | cron-batch | — | A-Router брат | — | — | turbo-tiles |

✅ = уже работает. Пустые ячейки = роль не подходит этой машине, не нагружаем.

## 3. Загрузка по машинам (фактическая, не теоретическая)

| Машина | Активных ролей | Когда работает | Контакт с тобой |
|---|---|---|---|
| Mac M1 Pro | 5 (R1,R2,R3,R4,R7) | 9-18 + вечер | прямой, постоянный |
| iMac 2015 | 4 (R1,R2,R3,R7) | по cron, 24/7 | невидимый, dual-check |
| Beelink SER9 | 6 (R1,R2,R3,R4,R7,R8) | вечер + ночь | morning digest |
| **Boox eInk** | **4 (R1,R3,R5,R7)** | **вечер для чтения, момент для пометок** | **прямой, медленный/глубокий** |
| VPS Abel-HQ | 6 (R1,R3,R4,R6,R7,R8) | 24/7 | невидимый, оркестрация |
| VPS Abel | 4 (R2,R4,R6,R7) | 24/7 | невидимый, hosting |
| iPhone | 4 (R1,R3,R4,R6) | моменты | voice + push |
| OPPO Find N3 | 7 (R1,R2,R3,R4,R5,R6,R7) | 24/7 фон + момент | push + Termux |

OPPO самая загруженная мобильная нода — потому что Termux+root даёт ей возможности почти как у мини-VPS.

**Boox eInk — медленная глубокая нода.** Не быстрая (eInk refresh), но критическая для **L3-чтения** чужих peer-review статей без усталости глаз и для рукописного capture идей. Закрывает 2 дыры системы: чтение и стационарный handwriting capture. На Boox можно поставить Termux для git mirror, Calibre для библиотеки PDF.

## 4. Временная сетка дня

```
00:00 — 03:00  ╔═══════════════════════════════════════════╗
               ║ Beelink R2/R3: ночные тесты всех якорей    ║
               ║ VPS-HQ R3: AI cross-review (Grok+Gemini)   ║
               ║ OPPO R7: git mirror push к двум VPS        ║
03:00 — 06:00  ╠═══════════════════════════════════════════╣
               ║ Beelink R3: diff Mac vs iMac результатов   ║
               ║ VPS-HQ R6: morning report генерация        ║
               ║ Telegram-бот сборка дайджеста              ║
06:00 — 09:00  ╠═══════════════════════════════════════════╣
               ║ Telegram @abelworldbot: дайджест приходит  ║
               ║ iPhone push: «4 якоря готовы за ночь»      ║
               ║ Ты: смотришь в кофе 15 минут               ║
09:00 — 18:00  ╠═══════════════════════════════════════════╣
               ║ Mac: основная креативная работа            ║
               ║ iPhone/OPPO R5: capture идей в moment      ║
               ║ Beelink: idle, готов к командам Mac        ║
               ║ VPS: idle, фон                             ║
18:00 — 22:00  ╠═══════════════════════════════════════════╣
               ║ Mac+Beelink R3 параллельно: peer-review     ║
               ║ дневных коммитов                            ║
               ║ Mac: подготовка ночных задач для Beelink   ║
22:00 — 24:00  ╠═══════════════════════════════════════════╣
               ║ status skill: XP, ачивки, отчёт за день   ║
               ║ Quest skill: загрузка ночных квестов       ║
               ║ Mac засыпает, Beelink включается           ║
               ╚═══════════════════════════════════════════╝
```

## 5. Mesh-memory как нервная система

`~/Documents/Projects/mesh-memory/` — git-synced между всеми машинами через bare repo на Abel-HQ. Автопул каждые 60 сек.

Структура (после pilot):
```
mesh-memory/
├── knowledge/                    — общая база
│   └── architecture-2n.md        — копия принципа
├── tasks/                        — очередь задач
│   ├── pending/                  — ждут исполнителя
│   ├── in-progress/              — взяты, выполняются
│   └── done/                     — выполнены, ждут review
├── reports/                      — что сделано за день/ночь
│   └── 2026-04-17.md
└── digest/                       — материал для morning push
    └── latest.md
```

Машина проверяет `pending/`, берёт подходящую её роли задачу, перекладывает в `in-progress/`, выполняет, перекладывает в `done/` с отчётом. Telegram-бот собирает `done/` за период в `digest/latest.md`.

## 6. SSH-связность (то что уже есть)

| Откуда | Куда | Способ | Готово? |
|---|---|---|---|
| Mac | Beelink | `ssh azw-ser9` | ✅ |
| Mac | iMac | `ssh imac` | ✅ |
| Mac | VPS Abel-HQ | `ssh -i ~/.ssh/abel_hq_key root@72.56.107.21` | ✅ |
| Mac | VPS Abel | `ssh -i ~/.ssh/vps_abel_key root@5.129.220.96` | ✅ |
| Mac | OPPO | через Tailscale 100.113.70.61 + ADB | ✅ |
| Mac | Boox | через Tailscale + Termux (после установки) | ◻ |
| Beelink | Mac | нужно настроить (~/.ssh/authorized_keys) | ◻ |
| Beelink | mesh-memory | git pull через github.com | ◻ |
| OPPO Termux | mesh-memory | git pull через github.com | ◻ |
| iMac | mesh-memory | git pull через github.com | ◻ |

## 7. Quest skill — игровой слой

64 квеста = 64 якоря. Каждый квест:
- ID: A1, A4, R1, C1, J1, M2, M3, E1, I3, I4, S1, D1, ... (текущие 16) + 48 future
- Награда: XP, ачивка, разблокировка следующего уровня
- Owner-machine: какая машина выполняет (распределяется автоматически или вручную)
- Формат: 64-строчный якорь
- Дедлайн: гибкий, цель 64 якоря к концу 2026

Достижения (на 2ⁿ-станциях):
- 🥉 «4 якоря в формате» — первый кластер
- 🥈 «16 якорей в формате» — модуль закрыт ✅ (близко)
- 🥇 «64 якоря в формате» — система готова
- 🏆 «256 якорей» — большой проект

## 8. Pilot 1 неделя — конкретные шаги

**Это PILOT++** — объединение 2ⁿ-задач (структура) и PC-задач (движок). Детали PC см. `PREDICTIVE-CONTEXT.md`.

**День 1 (сегодня, 2026-04-17):** 2ⁿ: ◻ ARCHITECTURE-2N.md ✅ ◻ MESH-DISTRIBUTION.md ✅ ◻ S1 в 64 строки ✅ ◻ D1 в 64 строки ◻ 64 квеста через quest skill. PC: ◻ PREDICTIVE-CONTEXT.md ✅ ◻ commit + push.

**День 2 (2026-04-18):** 2ⁿ: ◻ Beelink онлайн через `ssh azw-ser9` ◻ клонирует astro-dating + mesh-memory ◻ тест pending → in-progress → done. PC: ◻ Whisper.cpp на Mac, launchd `com.user.whisper-capture` → `mesh-memory/voice/`.

**День 3 (2026-04-19):** 2ⁿ: ◻ OPPO Termux + SSH-ключ + micro-task тест ◻ Boox онлайн с Termux+git+Calibre, первый PDF. PC: ◻ Screen capture cron `*/5` → vision LLM → `mesh-memory/screen/`. Тест: 96 скриншотов за день, поиск работает.

**День 4 (2026-04-20):** 2ⁿ: ◻ Cron VPS Abel-HQ: AI cross-review через Grok/Gemini. PC: ◻ Indexer на Beelink — sentence-transformers + FAISS, ночной job → `mesh-memory/index/hot.faiss`. Тест: запрос «вспомни про D1» возвращает voice-фрагменты.

**День 5 (2026-04-21):** 2ⁿ: ◻ iMac dual-check, cron каждый коммит Mac → iMac тесты → diff. PC: ◻ State estimator на VPS-HQ ежечасно, читает 4ч capture + active_quests → `state.md`.

**День 6 (2026-04-22):** 2ⁿ: ◻ Замер метрик pilot, опрос «играючи?». PC: ◻ Predictor на VPS-HQ каждые 2 часа → predictions.md ◻ Telegram digest 7:00 первый раз — содержательный.

**День 7 (2026-04-23):** 2ⁿ: ◻ Финальный отчёт, решение о масштабировании на C. PC: ◻ Feedback loop активен — accept/reject → `mesh-memory/feedback/` ◻ Beelink анализ feedback ночью.

## 9. Метрики pilot

| Метрика | Цель к концу 7 дней |
|---|---|
| Якорей в формате 64 строк | ≥ 4 (S1, D1, +2 переоформленных) |
| Beelink committer в git log | ≥ 5 коммитов |
| OPPO выполнил micro-tasks | ≥ 3 |
| **Boox прочитал peer-review PDF** | **≥ 1 с рукописными пометками, синхронизированными в mesh** |
| iMac dual-check работает | да, хотя бы 1 раз diff |
| **PC: Voice capture (часов)** | **≥ 50 часов, ≥ 80% распознано** |
| **PC: Screen capture (скриншотов)** | **≥ 1500 описано** |
| **PC: Predictor предсказаний** | **≥ 84 за неделю (12/день)** |
| **PC: Telegram morning digest** | **≥ 5 за 7 дней** |
| **PC: Принятые квесты от predictor** | **≥ 10** |
| Telegram morning digest | ≥ 5 за неделю (не каждый день обязательно) |
| Mac работает 9-18, ничего после | да (без перегрузки) |
| Subjective: «играючи?» | 7+ из 10 |
| Subjective: «контроль есть?» | 7+ из 10 |
| Новых багов в astro-dating | 0 (mesh не должна ломать науку) |

## 10. Если pilot не зайдёт

| Сценарий | Действие |
|---|---|
| Чувство потери контроля | Снизить автономию Beelink — все коммиты только через ручное одобрение Mac |
| Слишком много уведомлений | Дайджест 1 раз в день вместо 3 раз |
| Beelink делает мусор | Pause Beelink, ввести check-list pre-commit |
| OPPO Termux нестабилен | Убрать из mesh, оставить только iPhone capture |
| iMac dual-check шумит | Снизить частоту до 1 раз в неделю |
| Сложно понимать что происходит | Status skill — большой дашборд с картой mesh |
| Принцип 2ⁿ давит | Релакс — 64 строки как **цель**, не закон. Допуск ±15% |

## 11. Если pilot зайдёт — что дальше

- Копия `ARCHITECTURE-2N.md` и `MESH-DISTRIBUTION.md` в `mesh-memory/knowledge/` → распространение на все сессии
- Аудит остальных проектов (Explore-агент) против шкалы 2ⁿ
- Запуск pilot v0.2 — расширение на другие проекты (mesh-memory, A-Router, AILib)
- Публичный пост в Telegram-канале «Хронозвёзды» о методе
- Если интересно community — Habr-статья «Как я организовал работу по фрактальной шкале 2ⁿ»

## 12. Связанные документы

- `ARCHITECTURE-2N.md` — манифест принципа
- `docs/anchors/S1-iching-dna.md` — пилот шаблона якоря
- `docs/L3-roadmap.md` — путь к peer-review
- `docs/publishing/MODEL.md` — модель кросс-публикаций (требует пересмотра в 8×8)
- `docs/publishing/MATRIX.md` — матрица публикаций (требует пересмотра в 8×8)
- `~/Documents/Projects/mesh-memory/` — нервная система mesh
- `~/.claude/projects/-Users-macbookpro14/memory/architecture_2n.md` — копия принципа в memory

Дата следующего ревью: **2026-04-24** (через 7 дней, итог pilot).
