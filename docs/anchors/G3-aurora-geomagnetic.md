## 1. Тезис G3 — аврора как прокси геомагнитных бурь → прогноз Кэррингтона
Класс: солнечно-геомагнитный якорь. Дата: 2026-04-17. Размер: 64 строки (4×16).
~2000 записей северных сияний (567 CE — 1900 CE) в китайских, корейских, европейских хрониках.
Аврора на низких широтах (Китай 30°N, Корея 37°N) = только сильные геомагнитные бури.
Кэррингтон 1859 — самая сильная задокументированная буря. Если повторится: $1-2 трлн ущерба.
Предсказание следующего Кэррингтон-class события = прямая коммерческая ценность.
Частота аврор ∝ солнечная активность. FFT на 1300-летнем ряде → периоды бурь.
Cross-match с SOL-1 (sunspots) и G2 (Halley) → тройная independent валидация.
Связь с G1 (Miyake events): экстремальные аврора = proxy super-flares.
774 CE Miyake event → должна быть мощнейшая аврора в записях около этой даты.
Связь с CIV-1: аврора-записи = ещё один data point информационной ёмкости цивилизации.
Практическое применение: энергосети, страхование, спутниковые операторы, авиация.
Уникальность: cross-match aurora × astro-dating якоря → verified dates → надёжный FFT.
Базлайн: 1300 лет (хроники) + 170 лет (магнитометры) = 1470 лет геомагнитных данных.
Для сравнения: без наших verified dates базлайн ненадёжен (даты из хронологии «как есть»).
С нашим cross-match: verified aurora dates × Halley/eclipses = trustworthy baseline.
Целевые циклы FFT: Schwabe 11, Hale 22, Gleissberg 88, Suess 210 (ожидаем из SOL-1+G2).
## 2. Метод (pipeline E2 из SOL1-PIPELINE.md)
Шаг 1. Скачать каталог аврор: Silverman 1992 + Keimatsu 1970-76 + Fritz 1873.
Формат: год, месяц, широта наблюдения, источник, описание, интенсивность (1-5).
Шаг 2. Cross-match с astro-dating якорями (±10 лет) — те же 36 якорей что в SOL-1 E1.
Halley (30 появлений) даёт покрытие каждые ~76 лет → ~60-70% аврор verified.
Шаг 3. Построить time series: число аврор / декада (10-летний бин).
Разделить на: все / verified / low-latitude-only (сильные бури).
Шаг 4. FFT/wavelet → периоды. Сравнить с SOL-1 (sunspots) и G2 (Halley).
Если Gleissberg/Suess появятся ЧЕТВЁРТЫЙ раз → L4 cross-validation усилится.
Шаг 5. Extreme events: найти самые интенсивные аврора-записи → cross-match с Miyake (G1).
774 CE, 993 CE → ожидаем мощнейшие аврора в ±5 лет от этих дат.
Шаг 6. Recurrence interval для extreme auroras → прогноз следующей Кэррингтон-class.
Если средний интервал ~150-500 лет → следующая между 2010 и 2360 (Кэррингтон 1859 + interval).
Шаг 7. Mesh peer-review: Mac FFT vs Beelink wavelet independently.
Стек: Python + numpy + scipy + pywt + matplotlib. $0 (все данные open).
Время реализации: ~3-4 часа кода (каталог аврор объёмнее sunspots).
Основной каталог: Hayakawa et al. 2015-2021 (обновлённые compilations с HIP cross-refs).
Альтернатива: Willis et al. 2005 «A catalogue of large geomagnetic storms 1500-1899».
## 3. Литература и данные
Каталоги аврор (primary sources):
1. Silverman S.M. *Secular variation of aurora for the past 500 years*. Rev.Geophys. 1992.
2. Keimatsu M. *Chronological table of aurora in China, Korea, Japan*. 1970-1976 (5 vols).
3. Fritz H. *Verzeichniss Beobachteter Polarlichter*. Wien 1873 (первый систематический).
4. Hayakawa H. et al. *East Asian observations of low-latitude aurora*. ApJ 2015-2021.
5. Willis D.M. et al. *A catalogue of large geomagnetic storms*. Ann.Geophys. 2005.
Геомагнитные бури и прогнозирование:
6. Tsurutani B.T. et al. *The extreme magnetic storm of 1-2 September 1859*. JGR 2003.
7. Riley P. *On probability of occurrence of extreme space weather events*. Space Weather 2012.
8. Hapgood M. *Prepare for the coming space weather storm*. Nature 2012.
9. Lloyds. *Solar storm risk to the North American electric grid*. 2013. ($0.6-2.6 trillion).
Связь с astro-dating:
10. Stephenson F.R. *Historical Eclipses and Earth's Rotation*. Cambridge 1997.
11. Dambis A.K., Efremov Yu.N. *Dating Ptolemy's star catalogue*. JHA 2000.
Ограничения: записи неоднородны (Китай густой, Европа до 1100 CE — редкий).
Широта наблюдения критична: аврора на 30°N = только extreme storms (selection bias для сильных).
Интенсивность — субъективная оценка (нет стандартной шкалы до XIX века).
## 4. TODO и связи проекта
TODO кода (pipeline E2):
- [ ] Скачать/компилировать aurora каталог → `data/solar/aurora_catalog.csv` (~2000 записей).
- [ ] `src/g3_aurora_storms.py` — cross-match + FFT + extreme events (≤256 строк).
- [ ] `results/g3_aurora_fft.png` — графики (6 панелей как в SOL-1 E1).
- [ ] `results/g3_aurora_report.md` — отчёт с Carrington prediction.
TODO публикации (после результатов):
- [ ] Сравнить наши FFT-пики с SOL-1 + G2 → если 4/4 совпадают → write-up для Space Weather journal.
- [ ] Контакт: Hapgood M. (RAL Space, UK) — ведущий по space weather policy.
- [ ] Контакт: Hayakawa H. (Nagoya, Japan) — ведущий по historical aurora catalogs.
- [ ] Если Кэррингтон-прогноз конкретный → страховые компании (Lloyds, Swiss Re).
Cross-links:
- ↑ ВВЕРХ: Riley 2012 (Space Weather), Hapgood 2012 (Nature), Lloyds 2013 (risk report).
- ↓ ВНИЗ: Habr «Когда повторится Кэррингтон: 1300 лет аврор говорят...».
- ↔ ПОПЕРЁК: SOL-1 E1 (sunspots), G1 (Miyake C14), G2 (Halley tail) — все прокси одного.
- ↔ ПОПЕРЁК: G6 (Mars radiation) — aurora peaks = worst Mars transit windows.
- ↔ ПОПЕРЁК: CIV-1 (civilization curve) — aurora gaps = dark ages on CIV-1?
Дата следующего ревью G3: 2026-05-01 (2 недели, после скачивания aurora catalog).
