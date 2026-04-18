## 1. Тезис MAU1 — верификация Grand Solar Minima через ¹⁴C × sunspot records
Класс: солнечно-верификационный якорь (мост SOL-1↔astro-dating). Дата: 2026-04-18. 64 строк.
SOL-1 **предсказывает** будущее (Grand Solar Minimum ~2286). MAU1 **верифицирует** прошлое.
Два проекта — одна система: SOL-1 prediction + MAU1 verification = замкнутый цикл.
5 известных Grand Solar Minima за последние 1000 лет (по Usoskin 2017):
| Минимум | Период | ¹⁴C spike | Sunspot drop | Aurora gap |
|---|---|---|---|---|
| Oort | 1010-1050 | ✅ IntCal20 | ⚠️ мало данных | ⚠️ мало данных |
| Wolf | 1280-1350 | ✅ IntCal20 | ⚠️ bare-eye only | ✅ aurora gap |
| Spörer | 1460-1550 | ✅ IntCal20 | ⚠️ bare-eye only | ✅ aurora gap |
| Maunder | 1645-1715 | ✅ IntCal20 | ✅ telescopic | ✅ aurora gap (Halley 1716 = first post) |
| Dalton | 1790-1830 | ✅ IntCal20 | ✅ telescopic | ✅ fewer aurora |
Cross-validation: ¹⁴C (IntCal20 E4) × sunspot records (E1) × aurora gaps (G3) × Halley brightness (G2).
Maunder = самый сильный якорь: 3/3 прокси совпадают + telescopic confirmation + Halley 1716.
Связь с CIV-1: Maunder Minimum = «тёмный участок» на кривой? (нет — телескоп уже был).
MAU1 замыкает петлю: prediction (SOL-1) ↔ verification (MAU1) ↔ anchors (astro-dating).
Текущий прогноз SOL-1: next GSM ~2286 CE (68% CI: 2082-2444), 6 циклов суперпозиция.
## 2. Метод (cross-match ¹⁴C × sunspot × aurora × Halley для каждого минимума)
Шаг 1. Определить границы каждого GSM по ¹⁴C (IntCal20, уже скачан: data/solar/intcal20.14c).
Criterion: Δ¹⁴C > mean + 1σ continuously for ≥ 30 лет = Grand Minimum candidate.
Шаг 2. Cross-match с sunspot records (data/solar/pre_telescopic_sunspots.csv).
В периоды GSM ожидаем: 0 или near-0 sunspot records (подтверждение через отсутствие).
Шаг 3. Cross-match с aurora records (data/solar/aurora_catalog.csv).
В периоды GSM ожидаем: gap в aurora records (меньше геомагнитных бурь).
Шаг 4. Cross-match с Halley brightness scores (G2 data).
Halley в GSM period ожидаем: reduced tail (меньше solar wind давление).
Halley 1378 (Wolf), 1456 (Spörer), 1607 (start Maunder) — проверить brightness.
Шаг 5. Для каждого GSM: подсчитать confirmation score (0-4 по числу совпавших прокси).
Шаг 6. Если score ≥ 3/4 для всех 5 GSM → верификация замкнута → SOL-1 prediction trust↑.
Реализация: `src/mau1_grand_minima.py` (≤64 строки), reuse data из SOL-1 E1-E5.
Время: < 1 сек (все данные уже в CSV, только cross-match + count).
Mesh: Mac vs Beelink — одинаковый score для каждого GSM? Если да → verified.
Ключевое: MAU1 НЕ новый анализ, а **синтез** всех предыдущих (E1-E5 + G2 + G3).
Публикация: включить в R4 (Combined Prediction, 30 мая) как verification section.
Adversarial test: что если shuffled dates дают тот же score? Monte Carlo 1000×.
## 3. Литература и ограничения
1. Usoskin I.G. *A History of Solar Activity over Millennia*. Living Rev. Solar Phys. 2017.
2. Eddy J.A. *The Maunder Minimum*. Science 192:1189-1202 (1976). Landmark paper.
3. Steinhilber F. et al. *9,400 years of cosmic radiation*. PNAS 2012 (Be10 + ¹⁴C).
4. Miyahara H. et al. *Cyclicity of solar activity during the Maunder Minimum*. Solar Phys. 2004.
5. Vaquero J.M. *Historical sunspot observations: a review*. Adv. Space Res. 2007.
6. Beer J. et al. *The role of the sun in climate forcing*. Quaternary Sci. Rev. 2000.
Ограничение 1: Oort (1010-1050) плохо документирован (мало sunspot/aurora записей).
Ограничение 2: «aurora gap» может быть gap в хрониках (не в aurora) — selection bias.
Ограничение 3: Halley brightness зависит от расстояния до Земли (orbital + solar wind).
Ограничение 4: ¹⁴C dating precision ±20 лет → boundaries GSM размыты.
Митигация: использовать ТОЛЬКО периоды с ≥ 2 прокси; Oort → «tentative».
Связь с G1 Miyake: GSM ≠ Miyake (GSM = low activity, Miyake = extreme event); РАЗНЫЕ.
Связь с G6 Mars: GSM → increased GCR → worse Mars radiation (нашли в G6!).
Связь с L1-L4: MAU1 поднимает SOL-1 prediction с L2 (mesh) до L2.5 (self-verified cycle).
## 4. TODO и связи проекта
- [ ] `src/mau1_grand_minima.py` — cross-match 5 GSM × 4 прокси (≤64 строки).
- [ ] `results/mau1_grand_minima_matrix.png` — 5×4 heatmap verification matrix.
- [ ] `results/mau1_report.md` — confirmation scores + SOL-1 trust assessment.
- [ ] Monte Carlo: shuffled dates → score? Если random score < real → method valid.
- [ ] Интегрировать в R4 (Combined Prediction, 30 мая) как verification section.
- [ ] Объединить SOL-1 + MAU1 на сайте 24gpntb.ru в одну секцию «Solar: Past & Future».
↑ ВВЕРХ: Usoskin 2017, Eddy 1976, Steinhilber 2012 (definitive solar history papers).
↓ ВНИЗ: Habr «5 раз Солнце замолкало: что это значит для будущего».
↔ ПОПЕРЁК: SOL-1 (prediction), G2 (Halley), G3 (aurora), G1 (Miyake — different!).
↔ ПОПЕРЁК: CIV-1 (Maunder Minimum ≈ Scientific Revolution — correlation or causation?).
Дата следующего ревью MAU1: 2026-05-01 (2 недели, перед R2 публикацией).
