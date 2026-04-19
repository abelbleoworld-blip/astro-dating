#!/usr/bin/env python3
"""F4: Событие Мияке ~7176 до н.э. — поиск в C14 и Be10 данных.
Обнаружено в 2024 (Brehm et al.). Проверяем наш pipeline."""

import numpy as np
from pathlib import Path
from datetime import datetime
import os

OUT = Path(__file__).resolve().parent.parent / "results" / "f4_miyake_7176bce.md"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "solar"

# Известные события Мияке (суперспышки)
MIYAKE_EVENTS = [
    {'year': -7176, 'bce': 7176, 'name': 'Мияке 7176 до н.э.', 'discovered': 2024,
     'ref': 'Brehm et al. 2024'},
    {'year': -5259, 'bce': 5259, 'name': 'Мияке 5259 до н.э.', 'discovered': 2022,
     'ref': 'Miyake et al. 2022'},
    {'year': 774,   'bce': None, 'name': 'Мияке 774 н.э.', 'discovered': 2012,
     'ref': 'Miyake et al. 2012'},
    {'year': 993,   'bce': None, 'name': 'Мияке 993 н.э.', 'discovered': 2013,
     'ref': 'Miyake et al. 2013'},
]

print("=" * 70)
print("  F4: События Мияке — суперспышки в данных C14 и Be10")
print("=" * 70)
print()
print(f"  События Мияке — резкие скачки космогенных изотопов,")
print(f"  свидетельствующие о суперспышках (×10-100 Кэррингтона)")
print()
print(f"  Известные события:")
for e in MIYAKE_EVENTS:
    yr = f"{e['bce']} до н.э." if e['bce'] else f"{e['year']} н.э."
    ago = 2026 - e['year']
    print(f"    {yr:>15} ({ago:>5} лет назад) — {e['ref']}")
print()

# Проверяем C14 (IntCal20)
c14_path = DATA_DIR / "intcal20.14c"
c14_found = {}

if c14_path.exists():
    cal_bp, delta14c = [], []
    with open(c14_path) as f:
        for line in f:
            if line.startswith('#') or line.startswith('!') or not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) < 5:
                continue
            try:
                cal_bp.append(float(parts[0]))
                delta14c.append(float(parts[3]))
            except ValueError:
                continue

    cal_ce = 1950 - np.array(cal_bp)
    d14c = np.array(delta14c)
    idx = np.argsort(cal_ce)
    cal_ce, d14c = cal_ce[idx], d14c[idx]

    print(f"  Проверка IntCal20 ({len(cal_ce)} точек):")
    print()

    for event in MIYAKE_EVENTS:
        yr = event['year']
        window = 50  # ±50 лет
        mask = (cal_ce >= yr - window) & (cal_ce <= yr + window)
        if mask.sum() < 3:
            c14_found[yr] = ('нет данных', 0)
            continue

        local = d14c[mask]
        local_years = cal_ce[mask]
        baseline_mask = (cal_ce >= yr - 200) & (cal_ce <= yr + 200)
        baseline = d14c[baseline_mask].mean() if baseline_mask.sum() > 0 else 0
        peak = local.max()
        peak_year = local_years[np.argmax(local)]
        anomaly = peak - baseline

        name = f"{event['bce']} до н.э." if event['bce'] else f"{event['year']} н.э."
        if anomaly > 5:
            status = '✓ ОБНАРУЖЕН'
        elif anomaly > 2:
            status = '~ слабый сигнал'
        else:
            status = '✗ не виден'
        c14_found[yr] = (status, anomaly)

        print(f"    {name:>15}: пик Δ14C = {peak:.1f}‰ (базовая {baseline:.1f}‰, "
              f"аномалия {anomaly:+.1f}‰) → {status}")

else:
    print(f"  ⚠ Файл IntCal20 не найден: {c14_path}")

print()

# Проверяем Be10 (GISP2)
be10_path = DATA_DIR / "gisp2_be10_raw.txt"
be10_found = {}

if be10_path.exists():
    ages_bp, be10 = [], []
    in_data = False
    with open(be10_path) as f:
        for line in f:
            s = line.strip()
            if 'depth top' in s.lower():
                in_data = True
                continue
            if not in_data or not s:
                continue
            parts = s.split()
            if len(parts) < 6:
                continue
            try:
                val = float(parts[2])
                at = float(parts[4])
                ab = float(parts[5])
            except (ValueError, IndexError):
                continue
            if val > 900000:
                continue
            ages_bp.append((at + ab) / 2)
            be10.append(val)

    ages_ce = 1950 - np.array(ages_bp)
    be10 = np.array(be10)
    idx = np.argsort(ages_ce)
    ages_ce, be10 = ages_ce[idx], be10[idx]

    print(f"  Проверка GISP2 Be10 ({len(ages_ce)} точек, разрешение ~50-100 лет):")
    print()

    for event in MIYAKE_EVENTS:
        yr = event['year']
        window = 100
        mask = (ages_ce >= yr - window) & (ages_ce <= yr + window)
        if mask.sum() < 2:
            be10_found[yr] = ('нет данных', 0)
            name = f"{event['bce']} до н.э." if event['bce'] else f"{event['year']} н.э."
            print(f"    {name:>15}: нет данных в окне ±{window} лет")
            continue

        local = be10[mask]
        baseline_mask = (ages_ce >= yr - 500) & (ages_ce <= yr + 500)
        baseline = be10[baseline_mask].mean() if baseline_mask.sum() > 0 else local.mean()
        peak = local.max()
        ratio = peak / max(baseline, 1)

        name = f"{event['bce']} до н.э." if event['bce'] else f"{event['year']} н.э."
        if ratio > 1.3:
            status = '✓ пик'
        elif ratio > 1.1:
            status = '~ слабый'
        else:
            status = '✗ не виден'
        be10_found[yr] = (status, ratio)

        print(f"    {name:>15}: пик Be10 = {peak:.0f} (базовая {baseline:.0f}, "
              f"ratio {ratio:.2f}) → {status}")
else:
    print(f"  ⚠ Файл GISP2 не найден: {be10_path}")

print()

# Контекст для 7176 до н.э.
print(f"  КОНТЕКСТ МИЯКЕ 7176 до н.э. ({2026+7176} лет назад)")
print()
print(f"  Эпоха: ранний неолит (докерамический неолит B)")
print(f"  Ближайшие поселения:")
print(f"    Чатал-Хююк (Турция):     ~7500 до н.э. (основан)")
print(f"    Иерихон (Палестина):      ~8000 до н.э. (стены)")
print(f"    Гёбекли-Тепе (Турция):    ~9600 до н.э. (ещё функционирует)")
print(f"    Невали Чори (Турция):     ~8000 до н.э.")
print()
print(f"  Если суперспышка 7176 до н.э. была видна как аврора —")
print(f"  первые земледельцы Плодородного полумесяца наблюдали")
print(f"  небо, полыхающее красным. Но записей нет (до письменности")
print(f"  ещё ~4000 лет).")

print()
print("  " + "=" * 66)
print("  ВЫВОД")
print("  " + "=" * 66)
print()
print(f"  События Мияке — подтверждённые суперспышки.")
print(f"  774 и 993 н.э. — обнаружены в деревьях по всему миру.")
print(f"  7176 до н.э. — древнейшее, открыто в 2024.")
print(f"  Проверка через наш pipeline (C14 + Be10):")
for event in MIYAKE_EVENTS:
    yr = event['year']
    name = f"{event['bce']} до н.э." if event['bce'] else f"{event['year']} н.э."
    c14_status = c14_found.get(yr, ('?', 0))[0]
    be10_status = be10_found.get(yr, ('?', 0))[0]
    print(f"    {name:>15}: C14={c14_status:>15}, Be10={be10_status:>10}")
print("  " + "=" * 66)

# Отчёт
with open(OUT, 'w') as f:
    f.write("# F4: События Мияке — суперспышки\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Известные события\n\n")
    f.write("| Событие | Год | Лет назад | C14 | Be10 |\n|---|---|---|---|---|\n")
    for event in MIYAKE_EVENTS:
        yr = event['year']
        name = f"{event['bce']} до н.э." if event['bce'] else f"{event['year']} н.э."
        ago = 2026 - yr
        c14 = c14_found.get(yr, ('?', 0))[0]
        be10 = be10_found.get(yr, ('?', 0))[0]
        f.write(f"| {name} | {yr} | {ago} | {c14} | {be10} |\n")
    f.write("\n## Вывод\n\nСобытие 7176 до н.э. — древнейшая подтверждённая суперспышка.\n")
    f.write("Наш pipeline (SOL-1 E4/E5) позволяет искать неизвестные Мияке-события\n")
    f.write("по аномалиям C14 и Be10.\n")

print(f"\nОтчёт: {OUT}")
