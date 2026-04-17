## 1. Тезис SOL-1 — верификация древних солнечных записей → прогноз активности
Класс: солнечно-хронологический якорь. Дата: 2026-04-17. Размер: 64 строки (4×16).
Базлайн солнечных данных: 416 лет (1610-2026, телескопы) = 38 циклов Швабе.
Китайские bare-eye sunspot записи: 28 BCE — 1610 CE = ещё 1638 лет = 149 циклов.
Если astro-dating верифицирует ДАТЫ этих записей → базлайн растёт до 2054 лет = 187 циклов.
5× больше данных для прогноза Grand Solar Minimum, Gleissberg, Suess, Hallstatt.
Никто не применял independent астрономический метод верификации дат к солнечным записям.
Гелиофизики берут хронологию «как есть». Историки не проверяют через эфемериды.
Astro-dating закрывает разрыв: верифицированная хронология → надёжные солнечные данные.
Практическое применение: NASA/ESA space weather, энергосети, авиация, климат, страхование.
Связь с существующими якорями: J1 (Ассирия), C1 (Crab 1054), China, Halley — те же хроники.
Связь с A4 Альмагест 1022: доказывает что древняя астрономия ТОЧНА → солнечные записи тоже.
Связь с L1-L4: SOL-1 изначально на L1, mesh-проверка поднимет до L2, peer-review → L3.
Если C14/Be10 прокси совпадут с верифицированными летописями → L4 (независимые методы).
Это «застолбленная» ниша: верификация + прогноз = уникальная позиция проекта.
Финальная цель: предсказание следующего Grand Solar Minimum (ожидается ~2030-2060).
## 2. Метод проверки (7 шагов pipeline)
Шаг 1. Взять 112 записей bare-eye sunspot из китайских хроник (Хань шу → Мин ши).
Источник: Yau & Stephenson 1988 «A Revised Catalogue of Far Eastern Sunspot Records».
Шаг 2. Для каждой записи проверить: есть ли ±10 лет верифицированный якорь astro-dating?
Якоря: затмения (Saros), кометы (Галлея), сверхновые (Crab), звёздные каталоги.
Шаг 3. Если да → дата пятна ПОДТВЕРЖДЕНА через independent astronomical dating.
Если нет → дата остаётся «летописной» (не верифицированной), маркируется отдельно.
Шаг 4. Собрать верифицированные записи в dataset: дата + тип пятна + источник + якорь-верификатор.
Формат CSV: `year,month,source,spot_description,verification_anchor,confidence`.
Шаг 5. FFT / wavelet analysis верифицированного dataset → долгопериодные циклы.
Целевые: Schwabe 11, Hale 22, Gleissberg 88, Suess/de Vries 210, Hallstatt 2400.
Шаг 6. Сравнить с C14 (IntCal20 дендрохронология) и Be10 (GISP2 ледяной керн).
Совпадение периодов → L4 cross-validation. Расхождение → пересмотр хронологии или прокси.
Шаг 7. Экстраполяция: предсказать фазу следующих Gleissberg/Suess/Hallstatt циклов.
Если Hallstatt ~2400 лет и последний максимум ~0 CE → следующий минимум ~1200 CE (прошёл).
Но суперпозиция циклов даёт уточнение. Mesh-check: Mac FFT vs Beelink wavelet независимо.
Стек: Python + numpy FFT + pywt wavelets + IntCal20 CSV + Yau-Stephenson CSV.
Время реализации: ~1-2 недели кода + 1 неделя анализа результатов.
Стоимость: $0 (все данные открытые, код локальный).
## 3. Литература и данные
Солнечные пятна (исторические записи):
1. Yau K.K.C., Stephenson F.R. *A Revised Catalogue of Far Eastern Sunspot Records*. QJRAS 1988.
2. Vaquero J.M., Vázquez M. *The Sun Recorded Through History*. Springer 2009.
3. Hayakawa H. et al. *Sunspot observations in 1727-1748*. ApJ 2021 (+ ссылки на каталоги).
Солнечные циклы и прогноз:
4. Usoskin I.G. *A History of Solar Activity over Millennia*. Living Rev. Solar Phys. 2017.
5. Steinhilber F. et al. *9,400 years of cosmic radiation and solar activity*. PNAS 2012.
6. Solanki S.K. et al. *Unusual activity of the Sun during recent decades*. Nature 2004.
Прокси-данные:
7. Reimer P.J. et al. *IntCal20: Northern Hemisphere radiocarbon calibration*. Radiocarbon 2020.
8. Finkel R.C., Nishiizumi K. *Beryllium 10 concentrations in GISP2 ice core*. JGR 1997.
Верификация хронологии (связь с astro-dating):
9. Stephenson F.R. *Historical Eclipses and Earth's Rotation*. Cambridge 1997.
10. Dambis A.K., Efremov Yu.N. *Dating Ptolemy's star catalogue*. JHA 2000.
Ограничения: bare-eye sunspots видны только при ≥0.04% площади диска (крупные группы).
Записи неоднородны: китайские хроники густые, европейские до XVI в. — редкие.
## 4. TODO и связи проекта
TODO кода (pipeline SOL-1):
- [ ] Скачать Yau-Stephenson 1988 каталог (112 записей) → `data/sunspots_yau1988.csv`
- [ ] Скачать IntCal20 C14 данные → `data/intcal20.csv`
- [ ] `src/sol1_verify.py` — cross-match sunspot dates с astro-dating якорями (≤64 строки)
- [ ] `src/sol1_fft.py` — FFT/wavelet analysis верифицированного dataset (≤256 строк)
TODO публикации:
- [ ] Добавить абзац про SOL-1 в письмо Дамбису (перспектива, не основная тема)
- [ ] Отдельное письмо в Solar Physics или Living Reviews (после L3 на основном)
- [ ] Контакт: Usoskin I.G. (Oulu, Finland) — ведущий по исторической солнечной активности
Cross-links:
- ↑ ВВЕРХ: Usoskin 2017 (Living Rev.), Steinhilber 2012 (PNAS), Yau-Stephenson 1988
- ↓ ВНИЗ: Habr «Как древние китайцы помогут предсказать следующий солнечный минимум»
- ↔ ПОПЕРЁК: C1 (Crab 1054, Китай), China chronology, Halley (солнечный ветер → хвост)
- ↔ ПОПЕРЁК: D1 (информационная плотность) — солнечные записи как «инструмент»
Дата следующего ревью SOL-1: 2026-05-17 (через месяц, по итогам реализации кода).
