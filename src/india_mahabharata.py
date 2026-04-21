#!/usr/bin/env python3
"""I3: Mahabharata Kurukshetra war date — planetary cluster analysis.
Checks 5 astronomical markers from Bhishma Parva across 3500-500 BCE."""

import numpy as np
from skyfield.api import load
from skyfield.almanac import find_discrete
from pathlib import Path
import json, datetime

BSP = str(Path(__file__).resolve().parent.parent / "de422.bsp")
OUT = Path(__file__).resolve().parent.parent / "results" / "india_mahabharata.md"

ts = load.timescale()
eph = load(BSP)
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']
mars, jupiter, saturn = eph['mars barycenter'], eph['jupiter barycenter'], eph['saturn barycenter']

# Ecliptic longitude helper
def ecl_lon(body, t):
    """Ecliptic longitude in degrees at time t."""
    pos = earth.at(t).observe(body).apparent()
    lat, lon, _ = pos.ecliptic_latlon()
    return lon.degrees

def sun_moon_sep(t):
    """Angular separation Sun-Moon in degrees."""
    s = earth.at(t).observe(sun).apparent()
    m = earth.at(t).observe(moon).apparent()
    return s.separation_from(m).degrees

def check_markers(year):
    """Check 5 Mahabharata markers for Oct-Nov of given year. Returns dict of scores."""
    # Use astronomical year (0 = 1 BCE, -1 = 2 BCE, etc.)
    astro_year = -abs(year) + 1 if year > 0 else -abs(year)

    try:
        t_oct1 = ts.tt(astro_year, 10, 1)
        t_nov30 = ts.tt(astro_year, 11, 30)
        t_mid = ts.tt(astro_year, 10, 15)
    except Exception:
        return None

    results = {'year_bce': abs(year), 'score': 0, 'markers': {}}

    # M1: Saturn in Rohini (Aldebaran region, ~40-53° ecliptic longitude)
    try:
        sat_lon = ecl_lon(saturn, t_mid)
        in_rohini = 35 <= sat_lon <= 58
        results['markers']['saturn_rohini'] = {'lon': round(sat_lon, 1), 'match': in_rohini}
        if in_rohini:
            results['score'] += 1
    except:
        results['markers']['saturn_rohini'] = {'lon': None, 'match': False}

    # M2: Mars near Jyeshtha/Anuradha (~210-245° ecliptic longitude)
    try:
        mars_lon = ecl_lon(mars, t_mid)
        near_jyeshtha = 200 <= mars_lon <= 250
        results['markers']['mars_jyeshtha'] = {'lon': round(mars_lon, 1), 'match': near_jyeshtha}
        if near_jyeshtha:
            results['score'] += 1
    except:
        results['markers']['mars_jyeshtha'] = {'lon': None, 'match': False}

    # M3: Jupiter-Saturn close (within 30°)
    try:
        jup_lon = ecl_lon(jupiter, t_mid)
        sat_lon2 = ecl_lon(saturn, t_mid)
        sep = abs(jup_lon - sat_lon2)
        if sep > 180:
            sep = 360 - sep
        close = sep < 30
        results['markers']['jupiter_saturn'] = {'sep': round(sep, 1), 'match': close}
        if close:
            results['score'] += 1
    except:
        results['markers']['jupiter_saturn'] = {'sep': None, 'match': False}

    # M4: Lunar eclipse (full moon with Sun-Moon opposition < 1.5°) in Oct-Nov
    try:
        lunar_eclipse = False
        for day in range(0, 61, 1):
            t_day = ts.tt(astro_year, 10, 1 + day)
            sep = sun_moon_sep(t_day)
            if sep > 178.5:  # Near opposition = full moon, possible lunar eclipse
                lunar_eclipse = True
                break
        results['markers']['lunar_eclipse'] = {'match': lunar_eclipse}
        if lunar_eclipse:
            results['score'] += 1
    except:
        results['markers']['lunar_eclipse'] = {'match': False}

    # M5: Solar eclipse (Sun-Moon < 1.5°) within 15 days of lunar eclipse
    try:
        solar_eclipse = False
        for day in range(0, 75, 1):
            t_day = ts.tt(astro_year, 9, 15 + day)
            sep = sun_moon_sep(t_day)
            if sep < 1.5:
                solar_eclipse = True
                break
        results['markers']['solar_eclipse'] = {'match': solar_eclipse}
        if solar_eclipse:
            results['score'] += 1
    except:
        results['markers']['solar_eclipse'] = {'match': False}

    return results

def main():
    print("I3: Mahabharata Kurukshetra — planetary cluster scan")
    print(f"Range: 3500 BCE — 500 BCE, step 1 year")
    print(f"Ephemeris: {BSP}")
    print()

    all_results = []
    for bce_year in range(3500, 499, -1):
        if bce_year % 500 == 0:
            print(f"  scanning {bce_year} BCE...")
        r = check_markers(bce_year)
        if r and r['score'] >= 2:
            all_results.append(r)

    all_results.sort(key=lambda x: -x['score'])
    top = all_results[:20]

    print(f"\n=== TOP CANDIDATES (score >= 2) ===\n")
    print(f"{'Year BCE':>10} {'Score':>5}  Saturn  Mars  Jup-Sat  LunEcl  SolEcl")
    print("-" * 70)
    for r in top:
        m = r['markers']
        print(f"{r['year_bce']:>10} {r['score']:>5}  "
              f"{'✓' if m.get('saturn_rohini',{}).get('match') else '✗':>6}  "
              f"{'✓' if m.get('mars_jyeshtha',{}).get('match') else '✗':>4}  "
              f"{'✓' if m.get('jupiter_saturn',{}).get('match') else '✗':>7}  "
              f"{'✓' if m.get('lunar_eclipse',{}).get('match') else '✗':>6}  "
              f"{'✓' if m.get('solar_eclipse',{}).get('match') else '✗':>6}")

    # Traditional and scholarly dates check
    key_dates = [3067, 3102, 2449, 1478, 1397, 1193, 950, 836]
    print(f"\n=== KEY DATES CHECK ===\n")
    for yd in key_dates:
        r = check_markers(yd)
        if r:
            print(f"  {yd} BCE: score {r['score']}/5")

    # Write report
    with open(OUT, 'w') as f:
        f.write("# I3: Mahabharata Kurukshetra — Planetary Cluster Analysis\n\n")
        f.write(f"**Дата прогона:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Диапазон:** 3500–500 BCE, шаг 1 год\n")
        f.write(f"**Кандидатов (score ≥ 2):** {len(all_results)}\n\n")
        f.write("## Маркеры Бхишма Парвы\n\n")
        f.write("| # | Маркер | Критерий |\n|---|---|---|\n")
        f.write("| M1 | Сатурн в Рохини | ecl. lon. 35°–58° |\n")
        f.write("| M2 | Марс у Джьештхи | ecl. lon. 200°–250° |\n")
        f.write("| M3 | Юпитер-Сатурн сближение | sep < 30° |\n")
        f.write("| M4 | Лунное затмение Окт-Ноя | opposition > 178.5° |\n")
        f.write("| M5 | Солнечное затмение ±15 дн | conjunction < 1.5° |\n\n")
        f.write("## Лучшие кандидаты\n\n")
        f.write("| Год BCE | Score | Saturn | Mars | Jup-Sat | LunEcl | SolEcl |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in top:
            m = r['markers']
            f.write(f"| {r['year_bce']} | {r['score']}/5 | "
                    f"{'✓' if m.get('saturn_rohini',{}).get('match') else '✗'} | "
                    f"{'✓' if m.get('mars_jyeshtha',{}).get('match') else '✗'} | "
                    f"{'✓' if m.get('jupiter_saturn',{}).get('match') else '✗'} | "
                    f"{'✓' if m.get('lunar_eclipse',{}).get('match') else '✗'} | "
                    f"{'✓' if m.get('solar_eclipse',{}).get('match') else '✗'} |\n")
        f.write("\n## Традиционные и альтернативные даты\n\n")
        f.write("| Год BCE | Score | Источник |\n|---|---|---|\n")
        for yd in key_dates:
            r = check_markers(yd)
            src = {3067: 'Aryabhata calc', 3102: 'Kali Yuga start',
                   2449: 'Varahamihira', 1478: 'Sengupta 1947',
                   1397: 'Raghavan 1969', 1193: 'Trojan War parallel',
                   950: 'Max Müller', 836: 'Kochhar 2000'}.get(yd, '?')
            if r:
                f.write(f"| {yd} | {r['score']}/5 | {src} |\n")
        f.write("\n## Интерпретация\n\n")
        f.write("Кластерный анализ ищет годы, в которых максимальное число маркеров\n")
        f.write("из Бхишма Парвы совпадает одновременно. Score 5/5 = идеальное совпадение.\n")
        f.write("Score 3-4 = сильный кандидат. Score 2 = слабый.\n\n")
        f.write("Текст Махабхараты — составной (записан ~400 BCE–400 CE).\n")
        f.write("Астрономические описания могут отражать разные эпохи.\n")
        f.write("Кластеры дат = возможные слои текста.\n")

    print(f"\nReport saved: {OUT}")

if __name__ == '__main__':
    main()
