# /imperial — Имперский Звездочёт / Звездачёт

Активация полной базы знаний проекта вычислительной археоастрономии.

## Описание

По команде `/imperial` Claude входит в режим «Имперского Звездочёта» — загружает контекст всех астрономических, хронологических и вычислительных данных проекта.

## Триггер

Пользователь вводит `/imperial` или говорит «имперский звездочёт/звездачёт».

## Инструкции

При активации — прочитай и загрузи следующие документы по порядку:

### 1. Навигация (быстрый вход)
```
Read ~/Documents/Projects/astro-dating/FOCUS-25.md
Read ~/Documents/Projects/astro-dating/JOURNEY.md
```

### 2. Архитектура и принципы
```
Read ~/Documents/Projects/astro-dating/docs/ARCHITECTURE-2N.md
Read ~/Documents/Projects/astro-dating/docs/ORIGINS.md
Read ~/Documents/Projects/astro-dating/docs/INFORMATION-PLATEAU.md
```

### 3. Научные результаты
```
Read ~/Documents/Projects/astro-dating/results/almagest_1022_report.md
Read ~/Documents/Projects/astro-dating/docs/REPORT.md (первые 60 строк)
```

### 4. Звёздный каталог и данные
```
Read ~/Documents/Projects/astro-dating/data/almagest-veselovsky-INDEX.md
Read ~/Documents/Projects/astro-dating/data/solar-activity-2026.md
```

### 5. Люди и коммуникации
```
Read ~/Documents/Projects/astro-dating/docs/OUTREACH.md (контакты 12 исследователей)
```

### 6. Pilot и mesh
```
Read ~/Documents/Projects/astro-dating/docs/MESH-DISTRIBUTION.md
Read ~/Documents/Projects/astro-dating/docs/PREDICTIVE-CONTEXT.md
```

### 7. Memory (из прошлых сессий)
```
Read ~/.claude/projects/-Users-macbookpro14/memory/astro-dating-citation-graph.md
Read ~/.claude/projects/-Users-macbookpro14/memory/astro-dating-1022-breakthrough.md
Read ~/.claude/projects/-Users-macbookpro14/memory/astro-dating-info-plateau.md
Read ~/.claude/projects/-Users-macbookpro14/memory/almagest-veselovsky-1998.md
Read ~/.claude/projects/-Users-macbookpro14/memory/project-imperial-stargazer.md
```

### 8. Живые данные (fetch при каждом входе)
```bash
# Солнечная активность (SILSO — последние 3 месяца)
curl -s 'https://www.sidc.be/SILSO/INFO/snmtotcsv.php' | tail -3

# A-Router health
curl -s http://localhost:3400/api/health | head -c 300

# Git status проекта
cd ~/Documents/Projects/astro-dating && git log --oneline -5
```

## После загрузки — доложить

Выведи краткую сводку:
```
🌟 Имперский Звездочёт активирован
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Проект: astro-dating | 9 цивилизаций | 1022 звезды
Результат A4: 50 CE (RMS 1.23°)
Цикл 25: [текущее число Вольфа] (фаза спада)
Последний коммит: [hash] [message]
Оцифровка Альмагеста: [N/672] страниц
Outreach: [N/12] писем отправлено
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Три части: человек + машина + 2000 лет наблюдений
```

## Доступные подкоманды

После активации доступны:
- **«солнце»** / **«solar»** — текущая солнечная активность (fetch SILSO + NOAA)
- **«каталог»** / **«catalogue»** — работа со звёздным каталогом Альмагеста
- **«граф»** / **«citations»** — граф цитирования Dambis-Efremov
- **«письма»** / **«outreach»** — статус рассылки исследователям
- **«якоря»** / **«anchors»** — 9 хронологических сюжетов
- **«плато»** / **«plateau»** — S-кривая информационной ёмкости
- **«OCR»** — статус оцифровки Альмагеста Веселовского
- **«расчёт [эпоха]»** — запуск dating pipeline для указанной эпохи

## Файлы проекта

```
~/Documents/Projects/astro-dating/
├── src/                          — Python-скрипты (9 сюжетов)
│   ├── almagest_date.py          — оригинал (6 звёзд)
│   ├── almagest_1022.py          — полный каталог (1022 звезды)
│   ├── babylonian_astronomy.py
│   ├── bur_sagale_763bce.py
│   ├── china_chronology.py
│   ├── crab_supernova_1054.py
│   ├── dendera_zodiac.py
│   ├── halley_chronology.py
│   ├── maya_dresden.py
│   └── mul_apin.py
├── data/
│   ├── almagest_fast_stars.csv   — 6 быстрых звёзд
│   ├── ptolemy_verbunt2012.csv   — 1022 звезды (Verbunt cross-match)
│   ├── hipparcos_pm.csv          — собственные движения
│   ├── almagest-veselovsky-catalogue.csv  — РУЧНАЯ оцифровка (в процессе)
│   ├── almagest-veselovsky-INDEX.md       — индекс 672 страниц
│   ├── almagest-veselovsky-1998.txt       — OCR полного текста
│   ├── almagest-ocr/                      — постраничный OCR
│   └── solar-activity-2026.md
├── results/                      — графики и отчёты
├── docs/                         — документация
│   ├── ORIGINS.md                — генезис науки
│   ├── OUTREACH.md               — письма исследователям
│   ├── INFORMATION-PLATEAU.md    — S-кривая
│   ├── CITATION-MAP (в графе)
│   └── lectures/                 — 8 лекций PILOT++
├── de422.bsp                     — JPL эфемериды (653 MB)
└── scripts/
    └── ocr-almagest.sh           — batch OCR pipeline
```
