# Wikipedia: правила и стратегия для astro-dating

**Дата:** 2026-04-17
**Применимость:** en.wikipedia.org и ru.wikipedia.org (правила слегка отличаются, но принципы одни)

## Главное недоразумение, которое надо снять

Многие думают: «опубликовал научную работу — теперь напишу про неё в Wikipedia». **Это не так.**

Wikipedia — это **третичный источник** (encyclopedia). Она аккумулирует то, что **уже зафиксировано** во вторичных источниках (peer-review, признанные книги, качественная пресса). Сам автор первичного источника **не имеет права** писать энциклопедическую статью о своей работе.

Тебя не блокируют **за научное содержание** — тебя блокируют за **процедурные нарушения**. Нужно соблюдать процедуры.

## Три ключевых правила

### WP:NOR — No Original Research
> Wikipedia не публикует оригинальные исследования.

**Что это значит для нас:**
- Нельзя написать статью «Датировка каталога Альмагеста по методу астрономической кластеризации» — это оригинальное исследование автора.
- Можно сослаться на свою arXiv-статью в существующей статье «Almagest» только если эту arXiv-статью уже **процитировали независимые источники** (peer-review журнал, признанная монография).
- arXiv preprint **сам по себе не считается reliable source** для Wikipedia — он не прошёл peer-review.

### WP:RS — Reliable Sources
> Источники должны быть независимыми, авторитетными, проверяемыми.

**Иерархия для нас:**

| Источник | Wiki-статус |
|---|---|
| JHA, Nature, Med.Archaeometry, ВАК-журналы | ✅ Reliable Source (RS) |
| Книги издательств Springer, Cambridge, Brill, ИНФРА-М | ✅ RS |
| arXiv preprint **сам по себе** | ⚠ Допустим только если уже peer-reviewed где-то |
| GitHub, Habr, Telegram, YouTube собственный | ❌ Not RS |
| N+1, Naked Science, Элементы | ⚠ Допустимы как secondary (научная журналистика), но слабее |
| Постнаука, ScienceVideoLab | ⚠ Допустимы как secondary |

### WP:COI — Conflict of Interest
> Если редактируешь статью, в которой имеешь личный интерес — обязано раскрытие.

**Для автора проекта:**
- Любая правка в статье, где упоминается его работа → disclosure на user page и/или на talk page правки.
- Шаблон disclosure (en):
  > {{COI|article=Almagest}} I am the author of the cited paper. I am proposing this citation on talk page rather than adding it directly. — ~~~~
- Шаблон ru: `{{Конфликт интересов}}`
- Лучшая практика: **никогда не редактировать main space самому**, всегда через talk page proposal.

## Стратегия безопасной wiki-работы

### Шаг 0 — Регистрация
1. Создать аккаунт `abelbleoworld` (или нейм проекта) на en.wikipedia + ru.wikipedia.
2. Заполнить **user page** с честным disclosure:
   ```
   I am the author of [astro-dating GitHub project / arXiv:XXXX.XXXXX].
   When editing articles related to my work, I will disclose COI per WP:COI.
   I will propose citations on talk pages rather than editing directly.
   ```
3. Сделать ~30 **полезных правок** в **несвязанных** статьях (опечатки, ссылки) — это поднимает доверие community к аккаунту, прежде чем трогать спорное.

### Шаг 1 — Talk page proposal (никаких прямых правок)

Для каждой целевой статьи:
1. Открыть talk page (например `Talk:Almagest`).
2. Создать новую секцию `== Proposed citation: dating of Almagest ==`.
3. Текст:
   ```
   I am proposing the following citation for the "Dating" section.
   Disclosure: I am the author. Per WP:COI I am not editing the article directly.
   
   Proposed text: "Recent re-analysis using the Dambis-Efremov method
   on six fast-moving stars gives a date of −120 ± 100 CE
   (consistent with Hipparchus epoch).<ref>{{cite journal|...}}</ref>"
   
   Source: [link to peer-reviewed paper, NOT arXiv]
   
   I welcome any review or alternative formulation.
   ~~~~
   ```
4. Ждать **минимум 14 дней**. Если другой редактор внёс — отлично. Если нет — можно пинговать через WikiProject Astronomy.

### Шаг 2 — WikiProject engagement
- en: WikiProject Astronomy, WikiProject History, WikiProject Skepticism (для критики Фоменко)
- ru: Проект:Астрономия, Проект:История

Написать в talk страницу проекта: «есть peer-review citation для статьи X, прошу взгляда».

### Шаг 3 — Уровневые задачи (от безопасного к рискованному)

| Уровень | Задача | Риск отката |
|---|---|---|
| L0 | Исправить опечатку в статье «Almagest» | минимальный |
| L1 | Добавить citation на **чужую** работу (Dambis & Efremov 2000) в существующую статью | низкий |
| L2 | Через talk page предложить citation на **свою** peer-reviewed работу | средний |
| L3 | Через talk page предложить новый абзац с резюме своих результатов | высокий |
| L4 | Создать **новую** статью о своём методе | **очень высокий** — почти гарантированный AfD (Articles for Deletion) если делает автор |

**До W5 не идти выше L2.**

## Целевые статьи для citation injection (W2)

### English Wikipedia

| Статья | Секция для добавления | Тема | Источник |
|---|---|---|---|
| [Almagest](https://en.wikipedia.org/wiki/Almagest) | Dating / Composition | T1 A4 | peer-reviewed paper |
| [Hipparchus](https://en.wikipedia.org/wiki/Hipparchus) | Star catalog | T1 A4 | peer-reviewed paper |
| [Ptolemy](https://en.wikipedia.org/wiki/Ptolemy) | Astronomical works → Almagest | T1 A4 | peer-reviewed paper |
| [SN 1054](https://en.wikipedia.org/wiki/SN_1054) | Historical observations | T3 C1 | peer-reviewed paper |
| [Crab Nebula](https://en.wikipedia.org/wiki/Crab_Nebula) | History | T3 C1 | peer-reviewed paper |
| [Solar eclipse of June 15, 763 BC](https://en.wikipedia.org/wiki/Solar_eclipse_of_June_15,_763_BC) | Significance | T4 J1 | peer-reviewed paper |
| [Solar eclipse of May 28, 585 BC](https://en.wikipedia.org/wiki/Solar_eclipse_of_May_28,_585_BC) | Modern verification | T5 A1 | peer-reviewed paper |
| [MUL.APIN](https://en.wikipedia.org/wiki/MUL.APIN) | Dating | T4 | peer-reviewed paper |
| [Dendera zodiac](https://en.wikipedia.org/wiki/Dendera_zodiac) | Dating proposals | T6 E1 | peer-reviewed paper |
| [New Chronology (Fomenko)](https://en.wikipedia.org/wiki/New_Chronology_(Fomenko)) | Criticism | T10 | peer-reviewed paper |
| [Anatoly Fomenko](https://en.wikipedia.org/wiki/Anatoly_Fomenko) | Reception | T10 | peer-reviewed paper |
| [Igor Svyatoslavich](https://en.wikipedia.org/wiki/Igor_Svyatoslavich) | Eclipse during campaign | T2 R1 | peer-reviewed paper |

### Russian Wikipedia (зеркала плюс специфика)

| Статья | Секция | Особенность |
|---|---|---|
| [Альмагест](https://ru.wikipedia.org/wiki/Альмагест) | Датировка | в РФ-вики тема Фоменко горячая, нужна особая аккуратность |
| [Гиппарх](https://ru.wikipedia.org/wiki/Гиппарх) | Каталог звёзд | — |
| [Птолемей](https://ru.wikipedia.org/wiki/Птолемей) | Альмагест | — |
| [Сверхновая SN 1054](https://ru.wikipedia.org/wiki/SN_1054) | Исторические наблюдения | — |
| [Затмение 763 года до н. э.](https://ru.wikipedia.org/wiki/Затмение_15_июня_763_года_до_н._э.) | если статья есть | проверить существование |
| [Дендерский зодиак](https://ru.wikipedia.org/wiki/Дендерский_зодиак) | Датировка | — |
| [Новая хронология](https://ru.wikipedia.org/wiki/Новая_хронология_(Фоменко)) | Критика | очень спорная статья, готовиться к войне правок |
| [Анатолий Фоменко](https://ru.wikipedia.org/wiki/Фоменко,_Анатолий_Тимофеевич) | Критика | — |

⚠ В русской Wikipedia статьи о Фоменко — **долгоиграющие конфликтные зоны**. Любая правка вызовет реакцию. Готовиться к talk-page дискуссии в стиле peer-review. Не переходить на личности.

## Как НЕ делать (типичные ошибки)

1. ❌ Создать аккаунт «AstroDatingProject» — выглядит как проектный SPA (single-purpose account), удалят
2. ❌ Сразу редактировать main space без disclosure — блокировка
3. ❌ Использовать в качестве источника свой GitHub README — not RS, откатят
4. ❌ Цитировать только себя в статье — выглядит как спам, откатят
5. ❌ Удалять чужие критические citation в ответ на критику своих — block
6. ❌ Писать с нескольких аккаунтов — sock-puppet, permanent block
7. ❌ Просить друзей/коллег добавить citation без их собственной оценки — meatpuppet, block

## Чек-лист перед каждой wiki-правкой

- [ ] Аккаунт зарегистрирован под реальным именем или прозрачным проектным
- [ ] User page содержит COI disclosure
- [ ] Источник — peer-reviewed (не arXiv-only, не GitHub, не Habr)
- [ ] Я предлагаю на talk page, не редактирую main space сам
- [ ] Tone правки — нейтральный (NPOV), без «доказали», «опровергли», «впервые»
- [ ] Формулировка приписывает результат именно тому, кто его получил, не «современная наука» вообще
- [ ] Не удаляю существующие citation, только добавляю свои
- [ ] Готов к ответу: что делать если откатили (talk page → discussion → если консенсус не за — отступаю)

## Метрика успеха W2

| Метрика | Значение |
|---|---|
| Talk page proposals поданы | 12 (en) + 8 (ru) |
| Citations внесены community-редактором | ≥ 6 |
| Citations не откачены за 14 дней | ≥ 4 |
| Нет блокировок аккаунта | обязательно |
| Нет AfD против связанных статей | обязательно |

Если по итогам 3 месяцев откачено всё → пересмотр стратегии: возможно работы недостаточно процитированы извне для wiki-инклюзии, нужно вернуться в W1 за большей peer-review базой.
