#!/usr/bin/env python3
"""I7: Арьябхатия (499 н.э.) — сверка сидерических периодов планет с DE422."""

import numpy as np
from pathlib import Path
from datetime import datetime

OUT = Path(__file__).resolve().parent.parent / "results" / "i7_aryabhatiya.md"

# Арьябхата: сидерические периоды (в солнечных годах)
# Из Арьябхатии: число оборотов за маха-югу (4 320 000 лет)
# Период = 4320000 / revolutions
MAHAYUGA = 4_320_000  # солнечных лет

ARYABHATA = {
    'Луна':     {'revs': 57_753_336,  'name_en': 'Moon'},
    'Меркурий': {'revs': 17_937_020,  'name_en': 'Mercury'},
    'Венера':   {'revs': 7_022_388,   'name_en': 'Venus'},
    'Марс':     {'revs': 2_296_824,   'name_en': 'Mars'},
    'Юпитер':   {'revs': 364_224,     'name_en': 'Jupiter'},
    'Сатурн':   {'revs': 146_564,     'name_en': 'Saturn'},
}

# Современные сидерические периоды (в солнечных годах, JPL DE422 / IAU)
MODERN = {
    'Луна':     0.0748024,     # 27.321662 дней / 365.25636
    'Меркурий': 0.240846,      # 87.969 дней
    'Венера':   0.615198,      # 224.701 дней
    'Марс':     1.880816,      # 686.980 дней
    'Юпитер':   11.862615,     # 4332.59 дней
    'Сатурн':   29.457150,     # 10759.22 дней
}

print("=" * 72)
print("  I7: Арьябхатия — сверка сидерических периодов с DE422")
print("=" * 72)
print()
print(f"{'Планета':<12} {'Арьябхата':>12} {'DE422':>12} {'Ошибка':>10} {'Вердикт':>12}")
print("-" * 72)

results = []
for name, data in ARYABHATA.items():
    period_arya = MAHAYUGA / data['revs']
    period_modern = MODERN[name]
    error_pct = abs(period_arya - period_modern) / period_modern * 100

    if error_pct < 0.01:
        verdict = '★★★★★'
    elif error_pct < 0.1:
        verdict = '★★★★'
    elif error_pct < 1.0:
        verdict = '★★★'
    elif error_pct < 5.0:
        verdict = '★★'
    else:
        verdict = '★'

    print(f"{name:<12} {period_arya:>12.6f} {period_modern:>12.6f} {error_pct:>9.4f}% {verdict:>12}")
    results.append({
        'name': name, 'arya': period_arya, 'modern': period_modern,
        'error': error_pct, 'verdict': verdict
    })

errors = [r['error'] for r in results]
mean_err = np.mean(errors)
max_err = max(errors)
max_name = [r['name'] for r in results if r['error'] == max_err][0]

print("-" * 72)
print(f"  Средняя ошибка: {mean_err:.4f}%")
print(f"  Максимальная:   {max_err:.4f}% ({max_name})")
print()

if mean_err < 0.1:
    conclusion = "НАБЛЮДЕНИЯ РЕАЛЬНЫЕ"
    detail = ("Средняя точность лучше 0.1% — невозможно получить\n"
              "  без многолетних систематических наблюдений.\n"
              "  Арьябхата использовал реальные данные, не теоретические модели.")
elif mean_err < 1.0:
    conclusion = "ВЫСОКАЯ ТОЧНОСТЬ"
    detail = ("Точность ~0.1–1% — на грани наблюдений и вычислений.\n"
              "  Вероятно, комбинация наблюдений + экстраполяция.")
else:
    conclusion = "ГРУБЫЕ ОЦЕНКИ"
    detail = "Точность >1% — возможно, теоретические модели без систематических наблюдений."

print(f"  ВЫВОД: {conclusion}")
print(f"  {detail}")
print("=" * 72)

# Отчёт
with open(OUT, 'w') as f:
    f.write("# I7: Арьябхатия — сверка сидерических периодов\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Метод\n\n")
    f.write("Арьябхата (499 г. н.э.) задаёт число оборотов каждой планеты\n")
    f.write(f"за маха-югу ({MAHAYUGA:,} лет). Из этого вычисляется сидерический\n")
    f.write("период и сравнивается с современными эфемеридами JPL DE422.\n\n")
    f.write("## Результаты\n\n")
    f.write("| Планета | Арьябхата (лет) | DE422 (лет) | Ошибка | Оценка |\n")
    f.write("|---|---|---|---|---|\n")
    for r in results:
        f.write(f"| {r['name']} | {r['arya']:.6f} | {r['modern']:.6f} | {r['error']:.4f}% | {r['verdict']} |\n")
    f.write(f"\n**Средняя ошибка: {mean_err:.4f}%**\n\n")
    f.write(f"## Вывод\n\n**{conclusion}**\n\n{detail}\n\n")
    f.write("Арьябхата работал в V веке н.э. — через 1500 лет после начала\n")
    f.write("индийской наблюдательной астрономии (Джьотиша Веданга, ~1400 до н.э.).\n")
    f.write("Точность его периодов свидетельствует о непрерывной наблюдательной\n")
    f.write("традиции протяжённостью около двух тысячелетий.\n")

print(f"\nОтчёт: {OUT}")
