#!/usr/bin/env python3
"""F3: Затмение Угарита (KTU 1.78) — якорь Бронзового коллапса.
Кандидаты: 1223 и 1178 до н.э. Какое видно из Угарита?"""

from skyfield.api import load
import numpy as np
from pathlib import Path
from datetime import datetime

BSP = str(Path(__file__).resolve().parent.parent / "de422.bsp")
OUT = Path(__file__).resolve().parent.parent / "results" / "f3_ugarit_eclipse.md"

ts = load.timescale()
eph = load(BSP)
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

# Угарит (Рас-Шамра): 35.6°N, 35.78°E
LAT, LON = 35.6, 35.78

def sun_moon_sep(year, month, day, hour=12):
    """Угловое расстояние Солнце-Луна в градусах."""
    t = ts.tt(year, month, day, hour)
    s = earth.at(t).observe(sun).apparent()
    m = earth.at(t).observe(moon).apparent()
    return s.separation_from(m).degrees

def scan_eclipses(start_year, end_year, lat, lon):
    """Найти все солнечные затмения (sep < 1.5°) в диапазоне."""
    results = []
    for year in range(start_year, end_year):
        for month in range(1, 13):
            for day in [1, 5, 10, 15, 20, 25, 28]:
                try:
                    sep = sun_moon_sep(year, month, day, 12)
                    if sep < 5.0:
                        # Уточняем по часам
                        best_sep = sep
                        best_hour = 12
                        for h in range(6, 19):
                            s = sun_moon_sep(year, month, day, h)
                            if s < best_sep:
                                best_sep = s
                                best_hour = h
                        if best_sep < 1.5:
                            results.append({
                                'year': year, 'month': month, 'day': day,
                                'hour': best_hour, 'sep': best_sep
                            })
                except:
                    pass
    return results

print("=" * 70)
print("  F3: Затмение Угарита — якорь Бронзового коллапса")
print("=" * 70)
print()
print(f"  Место: Угарит (Рас-Шамра), {LAT}°N, {LON}°E")
print(f"  Табличка: KTU 1.78 — «Солнце зашло с Решеф (Марс) как стражем»")
print(f"  Кандидаты: 5 мая 1223 до н.э. | 21 января 1178 до н.э.")
print()

# Проверяем оба кандидата
candidates = [
    {'name': '1223 BCE (5 мая)', 'year': -1222, 'month': 5, 'day': 5},
    {'name': '1178 BCE (21 янв)', 'year': -1177, 'month': 1, 'day': 21},
]

print(f"  Прямая проверка кандидатов:")
print(f"  {'Кандидат':<25} {'Sep':>8} {'Час':>5} {'Затмение':>10}")
print(f"  {'-'*52}")

for c in candidates:
    best_sep = 999
    best_h = 12
    for h in range(5, 20):
        try:
            s = sun_moon_sep(c['year'], c['month'], c['day'], h)
            if s < best_sep:
                best_sep = s
                best_h = h
        except:
            pass
    eclipse = '✓ ДА' if best_sep < 1.5 else ('~ возможно' if best_sep < 3.0 else '✗ НЕТ')
    c['sep'] = best_sep
    c['best_hour'] = best_h
    c['eclipse'] = best_sep < 1.5
    print(f"  {c['name']:<25} {best_sep:>7.3f}° {best_h:>4}h {eclipse:>10}")

print()

# Полное сканирование 1250-1150 до н.э.
print(f"  Полное сканирование 1250–1150 до н.э....")
eclipses = scan_eclipses(-1249, -1149, LAT, LON)
print(f"  Найдено затмений (sep < 1.5°): {len(eclipses)}")
print()

if eclipses:
    print(f"  {'Год':>6} {'Мес':>4} {'День':>5} {'Час':>5} {'Sep':>8}")
    print(f"  {'-'*32}")
    for e in sorted(eclipses, key=lambda x: x['sep']):
        yr_bce = abs(e['year']) + 1 if e['year'] < 0 else e['year']
        print(f"  {yr_bce:>5}  {e['month']:>3}  {e['day']:>4}  {e['hour']:>4}h {e['sep']:>7.3f}°")

print()

# Марс — «Решеф как страж»
# Проверяем, виден ли Марс вечером в обе даты
mars = eph['mars barycenter']
print(f"  Марс («Решеф») — проверка видимости:")
for c in candidates:
    try:
        t = ts.tt(c['year'], c['month'], c['day'], 18)  # вечер
        m_pos = earth.at(t).observe(mars).apparent()
        s_pos = earth.at(t).observe(sun).apparent()
        mars_sun_sep = m_pos.separation_from(s_pos).degrees
        visible = mars_sun_sep > 15
        print(f"  {c['name']:<25} Марс-Солнце: {mars_sun_sep:.1f}° "
              f"{'✓ виден вечером' if visible else '✗ слишком близко к Солнцу'}")
    except:
        print(f"  {c['name']:<25} ошибка вычисления")

print()
print("  " + "=" * 66)
print("  ВЫВОД")
print("  " + "=" * 66)

winner = None
for c in candidates:
    if c['eclipse']:
        winner = c
        break

if winner:
    yr_bce = abs(winner['year']) + 1
    print(f"\n  Затмение Угарита: **{winner['name']}**")
    print(f"  Separation: {winner['sep']:.3f}°")
    print(f"  Время максимума: ~{winner['best_hour']}:00 UTC")
    print(f"  Лет назад от 2026: {2026 + yr_bce}")
    print(f"\n  Это фиксирует дату разрушения Угарита")
    print(f"  и якорь Бронзового коллапса.")
else:
    print(f"\n  Ни один кандидат не дал полного затмения над Угаритом.")
    print(f"  Возможно, нужен более тонкий шаг сканирования")
    print(f"  или альтернативная дата.")

print("  " + "=" * 66)

# Отчёт
with open(OUT, 'w') as f:
    f.write("# F3: Затмение Угарита — якорь Бронзового коллапса\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(f"## Кандидаты\n\n")
    f.write("| Кандидат | Separation | Час | Затмение |\n|---|---|---|---|\n")
    for c in candidates:
        ecl = '✓' if c['eclipse'] else '✗'
        f.write(f"| {c['name']} | {c['sep']:.3f}° | {c['best_hour']}h | {ecl} |\n")
    f.write(f"\n## Все затмения 1250–1150 до н.э. (sep < 1.5°)\n\n")
    if eclipses:
        f.write("| Год до н.э. | Месяц | День | Час | Sep |\n|---|---|---|---|---|\n")
        for e in sorted(eclipses, key=lambda x: x['sep']):
            yr_bce = abs(e['year']) + 1
            f.write(f"| {yr_bce} | {e['month']} | {e['day']} | {e['hour']}h | {e['sep']:.3f}° |\n")
    f.write(f"\n## Вывод\n\n")
    if winner:
        f.write(f"Затмение Угарита = **{winner['name']}**, sep {winner['sep']:.3f}°.\n")
    else:
        f.write(f"Требуется уточнение с более тонким шагом.\n")

print(f"\nОтчёт: {OUT}")
