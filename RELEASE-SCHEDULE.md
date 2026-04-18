# Release Schedule — стадированная публикация

**Принцип:** каждая публикация усиливает предыдущую. Не всё сразу.

| Волна | Дата | Что | GitHub tag | Каналы |
|---|---|---|---|---|
| **R1** | 2026-04-18 | A4 Almagest 1022 stars (+50 CE, RMS 1.23°) | v1.0-almagest | GitHub Release + Zenodo DOI + сайт |
| **R2** | 2026-05-02 | SOL-1 Gleissberg 88y + Suess 210y (4 sources) | v1.1-solar-cycles | GitHub + arXiv draft + сайт |
| **R3** | 2026-05-16 | G2 Halley tail = solar wind proxy (NOVEL) | v1.2-halley-novel | GitHub + arXiv + press release |
| **R4** | 2026-05-30 | Combined: Grand Solar Minimum prediction | v1.3-prediction | GitHub + arXiv + Habr + Telegram |

## Почему этот порядок

R1 (Almagest) = **фундамент**. Показывает что метод работает, данные открытые, код воспроизводим.
Без R1 остальные повисают в воздухе — «кто вы такие чтобы предсказывать Солнце?»

R2 (Gleissberg/Suess) = **результат**. 4 independent sources подтверждают одни и те же циклы.
Строится на R1 — «мы уже доказали что умеем датировать, теперь вот что нашли.»

R3 (Halley) = **новизна**. Никто не использовал хвост Галлея как прокси. Это PR-worthy.
Строится на R1+R2 — «наш метод + наши циклы + совершенно новый подход.»

R4 (Prediction) = **impact**. Grand Solar Minimum, Mars radiation, Carrington.
Строится на R1+R2+R3 — полная картина, практическая ценность.

## Что НЕ публикуем пока

- Miyake (G1) — S/N слабый, нужен wavelet rewrite
- Hale 22y — 1 source, не confirmed
- ~400y cycle — spread 24%, exploratory
- CIV-1 — визуализация, не scientific result

## Каналы для каждой волны

| Канал | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| GitHub Release | ✅ | ✅ | ✅ | ✅ |
| Zenodo DOI | ✅ | ✅ | ✅ | ✅ |
| 24gpntb.ru site | ✅ | ✅ | ✅ | ✅ |
| arXiv preprint | — | ✅ | ✅ | ✅ |
| Habr article | — | — | — | ✅ |
| Telegram channel | — | — | ✅ | ✅ |
| Letter to Дамбис | — | — | — | ✅ (после R4) |
