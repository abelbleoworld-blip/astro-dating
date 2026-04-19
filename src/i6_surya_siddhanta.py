#!/usr/bin/env python3
"""I6: Сурья-сиддханта — анализ заявленных астрономических параметров.
Прецессия 54"/год vs 50.3", наклон эклиптики, планетные периоды."""

import numpy as np
from pathlib import Path
from datetime import datetime

OUT = Path(__file__).resolve().parent.parent / "results" / "i6_surya_siddhanta.md"

# === 1. Прецессия ===
SS_PRECESSION = 54.0       # угловых секунд в год (Сурья-сиддханта)
MODERN_PRECESSION = 50.29  # угловых секунд в год (IAU 2006)
prec_error = abs(SS_PRECESSION - MODERN_PRECESSION) / MODERN_PRECESSION * 100

# === 2. Наклон эклиптики ===
SS_OBLIQUITY = 24.0        # градусов (Сурья-сиддханта)
# Наклон меняется со временем: ~23.44° (2000 н.э.), ~23.69° (500 до н.э.), ~24.0° (~2500 до н.э.)
# ε(t) ≈ 23.4393 - 0.013004 * T - 1.64e-7 * T² + 5.04e-7 * T³ (T в столетиях от J2000)
# Найдём, когда ε = 24.0°
# 24.0 = 23.4393 - 0.013004 * T → T = (23.4393 - 24.0) / 0.013004 = -43.1 столетий = ~2310 до н.э.

def obliquity(year):
    T = (year - 2000) / 100
    return 23.4393 - 0.013004 * T - 1.64e-7 * T**2 + 5.04e-7 * T**3

# Найдём год, когда наклон = 24.0°
for y in range(-4000, 2100):
    if abs(obliquity(y) - SS_OBLIQUITY) < 0.01:
        obliquity_year = y
        break

MODERN_OBLIQUITY = obliquity(2000)
obl_error = abs(SS_OBLIQUITY - MODERN_OBLIQUITY) / MODERN_OBLIQUITY * 100

# === 3. Сидерические периоды ===
# Сурья-сиддханта: обороты за маха-югу (4 320 000 лет)
MAHAYUGA = 4_320_000

SS_REVS = {
    'Луна':     57_753_336,
    'Меркурий': 17_937_000,
    'Венера':   7_022_388,
    'Марс':     2_296_824,
    'Юпитер':   364_220,
    'Сатурн':   146_564,
}

MODERN_PERIODS = {
    'Луна':     0.0748024,
    'Меркурий': 0.240846,
    'Венера':   0.615198,
    'Марс':     1.880816,
    'Юпитер':   11.862615,
    'Сатурн':   29.457150,
}

# === 4. Длина года ===
SS_YEAR_DAYS = 365 + 15/60 + 31/3600 + 31.4/216000  # 365;15,31,31,24 (шестидесятеричная)
# = 365.258756... дней
MODERN_SIDEREAL_YEAR = 365.256363  # дней (сидерический)
MODERN_TROPICAL_YEAR = 365.242190  # дней (тропический)
year_sid_err = abs(SS_YEAR_DAYS - MODERN_SIDEREAL_YEAR) / MODERN_SIDEREAL_YEAR * 100
year_trop_err = abs(SS_YEAR_DAYS - MODERN_TROPICAL_YEAR) / MODERN_TROPICAL_YEAR * 100

# === Вывод ===
print("=" * 68)
print("  I6: Сурья-сиддханта — анализ астрономических параметров")
print("=" * 68)

print("\n  1. ПРЕЦЕССИЯ")
print(f"     Сурья-сиддханта:  {SS_PRECESSION}\"/год")
print(f"     Современное:      {MODERN_PRECESSION}\"/год")
print(f"     Ошибка:           {prec_error:.1f}%")
print(f"     Завышена на:      {SS_PRECESSION - MODERN_PRECESSION:.2f}\"/год")

print("\n  2. НАКЛОН ЭКЛИПТИКИ")
print(f"     Сурья-сиддханта:  {SS_OBLIQUITY}°")
print(f"     Современный:      {MODERN_OBLIQUITY:.4f}°")
print(f"     Когда было 24.0°: ~{-obliquity_year + 1} г. до н.э. ({2026 - obliquity_year} лет назад)")
print(f"     Это может указывать на эпоху исходных наблюдений")

print("\n  3. ДЛИНА ГОДА")
print(f"     Сурья-сиддханта:     {SS_YEAR_DAYS:.6f} дней")
print(f"     Сидерический (DE422): {MODERN_SIDEREAL_YEAR:.6f} дней")
print(f"     Тропический:          {MODERN_TROPICAL_YEAR:.6f} дней")
print(f"     Ошибка (сидерич.):    {year_sid_err:.4f}%")
print(f"     Ошибка (тропич.):     {year_trop_err:.4f}%")
print(f"     Ближе к:              {'сидерическому' if year_sid_err < year_trop_err else 'тропическому'}")

print("\n  4. ПЛАНЕТНЫЕ ПЕРИОДЫ")
print(f"     {'Планета':<12} {'СС (лет)':>12} {'DE422':>12} {'Ошибка':>10}")
print("     " + "-" * 50)

period_errors = []
for name, revs in SS_REVS.items():
    ss_period = MAHAYUGA / revs
    modern = MODERN_PERIODS[name]
    err = abs(ss_period - modern) / modern * 100
    period_errors.append(err)
    print(f"     {name:<12} {ss_period:>12.6f} {modern:>12.6f} {err:>9.4f}%")

mean_period_err = np.mean(period_errors)
print(f"\n     Средняя ошибка периодов: {mean_period_err:.4f}%")

# Общая оценка
print("\n" + "=" * 68)
print("  ОБЩАЯ ОЦЕНКА СУРЬЯ-СИДДХАНТЫ")
print("=" * 68)
print(f"\n  Прецессия:        7.4% ошибка — знали о явлении, но неточно")
print(f"  Наклон 24.0°:     соответствует ~{-obliquity_year+1} г. до н.э. — возможная")
print(f"                    эпоха первичных наблюдений")
print(f"  Длина года:       {year_sid_err:.4f}% — превосходная точность")
print(f"  Периоды планет:   {mean_period_err:.4f}% — превосходная точность")
print(f"\n  Текст содержит СМЕСЬ:")
print(f"  — Древние наблюдения (наклон ~2500 до н.э.)")
print(f"  — Точные периоды (многовековые наблюдения)")
print(f"  — Теоретическую прецессию (завышена на 7%)")
print(f"\n  Финальная редакция: IV–V вв. н.э. (по филологическим данным)")
print(f"  Наблюдательная база: ~2500 до н.э. — V в. н.э. (~3000 лет)")
print("=" * 68)

# Отчёт
with open(OUT, 'w') as f:
    f.write("# I6: Сурья-сиддханта — анализ параметров\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Результаты\n\n")
    f.write("| Параметр | Сурья-сиддханта | Современное | Ошибка |\n")
    f.write("|---|---|---|---|\n")
    f.write(f"| Прецессия | {SS_PRECESSION}\"/год | {MODERN_PRECESSION}\"/год | {prec_error:.1f}% |\n")
    f.write(f"| Наклон эклиптики | {SS_OBLIQUITY}° | {MODERN_OBLIQUITY:.2f}° | {obl_error:.1f}% |\n")
    f.write(f"| Длина года | {SS_YEAR_DAYS:.6f} дн | {MODERN_SIDEREAL_YEAR:.6f} дн | {year_sid_err:.4f}% |\n")
    f.write(f"| Средняя ошибка периодов | — | — | {mean_period_err:.4f}% |\n\n")
    f.write("## Планетные периоды\n\n")
    f.write("| Планета | СС (лет) | DE422 (лет) | Ошибка |\n|---|---|---|---|\n")
    for name, revs in SS_REVS.items():
        ss_p = MAHAYUGA / revs
        mod = MODERN_PERIODS[name]
        err = abs(ss_p - mod) / mod * 100
        f.write(f"| {name} | {ss_p:.6f} | {mod:.6f} | {err:.4f}% |\n")
    f.write(f"\n## Датировка по наклону эклиптики\n\n")
    f.write(f"Наклон 24.0° соответствует ~{-obliquity_year+1} г. до н.э.\n")
    f.write(f"Это может указывать на эпоху древнейших наблюдений,\n")
    f.write(f"использованных при составлении текста.\n\n")
    f.write("## Вывод\n\nСурья-сиддханта — многослойный текст:\n")
    f.write(f"- Древние наблюдения (~2500 до н.э., наклон)\n")
    f.write(f"- Точные периоды (многовековая база, ошибка {mean_period_err:.4f}%)\n")
    f.write(f"- Теоретическая прецессия (завышена на 7%)\n")
    f.write(f"- Финальная редакция: IV–V вв. н.э.\n")

print(f"\nОтчёт: {OUT}")
