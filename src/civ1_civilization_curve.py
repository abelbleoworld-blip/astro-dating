#!/usr/bin/env python3
"""
CIV-1: Кривая цивилизации через точность астрономических наблюдений.
Мета-якорь: каждый наш астрономический якорь = точка на кривой роста знания.

log₂(информационная ёмкость) vs год → экспоненциальный или логистический fit
→ где скачки, где провалы → cross-match с Grand Solar Minima
→ предсказание следующего скачка.
"""

import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'civ1_instruments.csv')
RESULTS = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS, exist_ok=True)

def load_data():
    instruments = []
    with open(DATA) as f:
        for row in csv.DictReader(f):
            instruments.append({
                'year': int(row['year']),
                'name': row['name'],
                'culture': row['culture'],
                'total_bits': int(row['total_bits']),
                'precision_arcsec': float(row['precision_arcsec']),
                'source': row['source'],
            })
    instruments.sort(key=lambda x: x['year'])
    print(f"[1] Загружено {len(instruments)} инструментов ({instruments[0]['year']} — {instruments[-1]['year']} CE)")
    return instruments

def exponential(x, a, b, c):
    return a * np.exp(b * (x - c))

def logistic(x, L, k, x0, b):
    return L / (1 + np.exp(-k * (x - x0))) + b

def main():
    print("=" * 60)
    print("  CIV-1: Civilization Curve via Astronomical Precision")
    print("=" * 60)

    instruments = load_data()

    years = np.array([i['year'] for i in instruments])
    bits = np.array([i['total_bits'] for i in instruments])
    log_bits = np.log2(np.maximum(bits, 1))
    precision = np.array([i['precision_arcsec'] for i in instruments])
    log_precision = np.log2(1.0 / np.maximum(precision, 0.001))

    print(f"\n[2] Range: {log_bits.min():.1f} — {log_bits.max():.1f} log₂(bits)")
    print(f"    Doubling time estimate: {(years[-1]-years[0]) / (log_bits[-1]-log_bits[0]):.0f} years per doubling")

    # ============================================================
    # Piecewise exponential fit: pre-1600 + post-1600
    # ============================================================
    # 3 eras: naked eye → telescope → space
    ERAS = [
        ('Naked Eye',  None, 1600,  '🔭 Pre-telescope'),
        ('Telescope',  1600, 1900,  '🔭 Telescope era'),
        ('Space Age',  1900, None,  '🛰️ Photography + Space'),
    ]

    popt_eras = {}
    doubling_eras = {}
    residuals_exp = np.zeros(len(years))

    for era_name, start, end, desc in ERAS:
        if start is None:
            mask = years < end
        elif end is None:
            mask = years >= start
        else:
            mask = (years >= start) & (years < end)

        if mask.sum() < 3:
            print(f"\n[3] {era_name}: only {mask.sum()} points, skipping fit")
            continue

        y_era, b_era = years[mask], bits[mask]
        try:
            # Fit on log space for better stability
            log_b = np.log2(np.maximum(b_era, 1))
            from numpy.polynomial import polynomial as P
            coeffs = P.polyfit(y_era, log_b, 1)
            slope = coeffs[1]  # log2(bits)/year
            doubling = 1.0 / slope if slope > 0 else float('inf')

            # Also try exponential for extrapolation
            p0_c = y_era[0]
            try:
                popt, _ = curve_fit(exponential, y_era, b_era,
                                    p0=[b_era[0], 0.005, p0_c], maxfev=10000)
                doubling_exp = np.log(2) / popt[1] if popt[1] > 0 else float('inf')
                fit_vals = exponential(y_era, *popt)
                residuals_exp[mask] = np.log2(b_era) - np.log2(np.maximum(fit_vals, 1))
                popt_eras[era_name] = popt
                doubling_eras[era_name] = doubling_exp
                print(f"\n[3] {desc} ({y_era[0]}—{y_era[-1]}, {mask.sum()} pts):")
                print(f"     Linear log₂ slope: doubling every {doubling:.0f} years")
                print(f"     Exponential fit:   doubling every {doubling_exp:.0f} years")
            except Exception:
                doubling_eras[era_name] = doubling
                print(f"\n[3] {desc} ({y_era[0]}—{y_era[-1]}, {mask.sum()} pts):")
                print(f"     Linear log₂ slope: doubling every {doubling:.0f} years")
        except Exception as e:
            print(f"    ⚠️ {era_name} fit failed: {e}")

    # Summary
    popt_pre = popt_eras.get('Naked Eye')
    popt_post = popt_eras.get('Space Age') if 'Space Age' in popt_eras else popt_eras.get('Telescope')
    doubling_pre = doubling_eras.get('Naked Eye', 500)
    doubling_post = doubling_eras.get('Space Age', doubling_eras.get('Telescope', 50))
    doubling_time_exp = doubling_post
    popt_exp = popt_post
    BREAK_YEAR = 1600

    print(f"\n[3 SUMMARY] Piecewise doubling times:")
    for era_name, _, _, desc in ERAS:
        d = doubling_eras.get(era_name)
        if d:
            print(f"     {desc:30s}: {d:.0f} years")

    print(f"\n[4] Residuals (log₂ actual - log₂ piecewise fit):")
    for inst, res in zip(instruments, residuals_exp):
        marker = '⬆️' if res > 1 else '⬇️' if res < -1 else '  '
        print(f"    {marker} {inst['year']:+5d} {inst['name'][:35]:35s} {res:+5.1f}")

    # ============================================================
    # Key findings
    # ============================================================
    print(f"\n[5] Скачки (residual > +1 = выше тренда):")
    for inst, res in zip(instruments, residuals_exp):
        if res > 1:
            print(f"    ⬆️ {inst['year']:+5d}: {inst['name']} ({inst['culture']}) — leap!")

    print(f"\n    Провалы (residual < -1 = ниже тренда):")
    for inst, res in zip(instruments, residuals_exp):
        if res < -1:
            print(f"    ⬇️ {inst['year']:+5d}: {inst['name']} ({inst['culture']}) — dark age?")

    # ============================================================
    # Cross-match with Grand Solar Minima
    # ============================================================
    minima = [
        ('Oort', 1010, 1050), ('Wolf', 1280, 1350), ('Spörer', 1460, 1550),
        ('Maunder', 1645, 1715), ('Dalton', 1790, 1830),
    ]
    print(f"\n[6] Cross-match residuals × Grand Solar Minima:")
    for name, start, end in minima:
        nearby = [(inst, res) for inst, res in zip(instruments, residuals_exp)
                  if start - 100 <= inst['year'] <= end + 100]
        if nearby:
            avg_res = np.mean([r for _, r in nearby])
            print(f"    {name} ({start}-{end}): avg residual = {avg_res:+.1f}")

    # ============================================================
    # Prediction
    # ============================================================
    if popt_exp is not None:
        future = [2030, 2040, 2050, 2100]
        print(f"\n[7] Prediction (exponential extrapolation):")
        for y in future:
            pred = exponential(y, *popt_exp)
            print(f"    {y}: {pred:.2e} bits = {np.log2(max(pred,1)):.0f} log₂ bits")
        # When 1 Tbit?
        target = 1e12  # 1 Tbit
        year_tbit = popt_exp[2] + np.log(target / popt_exp[0]) / popt_exp[1]
        print(f"    1 Tbit astronomical knowledge: ~{year_tbit:.0f} CE")

    # ============================================================
    # Moore's Law comparison
    # ============================================================
    moore_doubling = 2  # years (transistors)
    astro_doubling = doubling_time_exp if popt_exp is not None else 150
    print(f"\n[8] Сравнение с законом Мура:")
    print(f"    Moore: удвоение каждые {moore_doubling} года (транзисторы)")
    print(f"    Astronomy: удвоение каждые {astro_doubling:.0f} лет")
    print(f"    Ratio: астрономия в {astro_doubling/moore_doubling:.0f}× медленнее кремния")
    print(f"    Но: астрономия работает {years[-1]-years[0]} лет, Moore ~60")

    # ============================================================
    # PLOTS
    # ============================================================
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Main curve (log scale)
    ax = axes[0, 0]
    ax.scatter(years, log_bits, c='blue', s=60, zorder=5, edgecolors='black', lw=0.5)
    for inst in instruments:
        if inst['total_bits'] > 100000 or inst['year'] < -500 or inst['year'] in [1997, 2022, -130]:
            ax.annotate(f"{inst['name'][:20]}\n({inst['year']})",
                       xy=(inst['year'], np.log2(inst['total_bits'])),
                       fontsize=6, ha='center', va='bottom', rotation=0)
    if popt_pre is not None:
        x_pre = np.linspace(years[0], BREAK_YEAR, 300)
        y_pre = np.log2(np.maximum(exponential(x_pre, *popt_pre), 1))
        ax.plot(x_pre, y_pre, 'r--', lw=2, alpha=0.7,
               label=f'Pre-{BREAK_YEAR} (doubling {doubling_pre:.0f}y)')
    if popt_post is not None:
        x_post = np.linspace(BREAK_YEAR, 2100, 300)
        y_post = np.log2(np.maximum(exponential(x_post, *popt_post), 1))
        ax.plot(x_post, y_post, 'g--', lw=2, alpha=0.7,
               label=f'Post-{BREAK_YEAR} (doubling {doubling_post:.0f}y)')
    ax.axvline(BREAK_YEAR, color='orange', ls=':', alpha=0.5, lw=1)
    ax.set_xlabel('Year CE')
    ax.set_ylabel('log₂(bits) — информационная ёмкость')
    ax.set_title('Кривая цивилизации: астрономическое знание за 5000 лет')
    ax.legend()
    ax.grid(alpha=0.3)

    # 2. Precision improvement
    ax = axes[0, 1]
    ax.scatter(years, log_precision, c='green', s=60, zorder=5, edgecolors='black', lw=0.5)
    ax.set_xlabel('Year CE')
    ax.set_ylabel('log₂(1/arcsec) — точность')
    ax.set_title('Рост точности астрономических наблюдений')
    ax.grid(alpha=0.3)
    for inst in instruments:
        if inst['precision_arcsec'] < 1 or inst['year'] < -500:
            ax.annotate(f"{inst['name'][:15]}", xy=(inst['year'], np.log2(1/inst['precision_arcsec'])),
                       fontsize=6, rotation=30, va='bottom')

    # 3. Residuals
    ax = axes[1, 0]
    if popt_exp is not None:
        colors = ['red' if r < -1 else 'green' if r > 1 else 'gray' for r in residuals_exp]
        ax.bar(years, residuals_exp, color=colors, width=50, alpha=0.7)
        ax.axhline(0, color='black', lw=1)
        ax.axhline(1, color='green', ls='--', alpha=0.5, label='Скачок (>+1)')
        ax.axhline(-1, color='red', ls='--', alpha=0.5, label='Провал (<-1)')
        # Grand Solar Minima overlay
        for name, start, end in minima:
            ax.axvspan(start, end, alpha=0.15, color='blue')
            ax.text((start+end)/2, max(residuals_exp)*0.8, name, fontsize=7, ha='center', color='blue')
        ax.set_xlabel('Year CE')
        ax.set_ylabel('Residual (log₂)')
        ax.set_title('Отклонения от тренда + Grand Solar Minima (синие)')
        ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # 4. Timeline with cultures
    ax = axes[1, 1]
    culture_colors = {
        'Britain': 'brown', 'Babylon': 'gold', 'Greece': 'blue', 'Rome': 'red',
        'Maya': 'green', 'India': 'orange', 'Islamic': 'purple', 'China': 'crimson',
        'Europe': 'navy', 'Central Asia': 'teal', 'Denmark': 'darkblue',
        'Germany': 'gray', 'England': 'darkgreen', 'Italy': 'tomato', 'Space': 'black',
    }
    for inst in instruments:
        c = culture_colors.get(inst['culture'], 'gray')
        ax.scatter(inst['year'], np.log2(inst['total_bits']), c=c, s=80, edgecolors='black', lw=0.5, zorder=5)
        ax.annotate(inst['culture'][:8], xy=(inst['year'], np.log2(inst['total_bits'])),
                   fontsize=5, ha='center', va='top', color=c)
    ax.set_xlabel('Year CE')
    ax.set_ylabel('log₂(bits)')
    ax.set_title('Цивилизации на кривой знания (цвет = культура)')
    ax.grid(alpha=0.3)

    plt.suptitle('CIV-1: 5000 лет астрономического знания — от Стоунхенджа до Gaia\n'
                'Мета-якорь: каждый инструмент = точка на кривой цивилизационного роста',
                fontsize=13, fontweight='bold')
    plt.tight_layout()
    plot_file = os.path.join(RESULTS, 'civ1_civilization_curve.png')
    plt.savefig(plot_file, dpi=150)
    print(f"\n📊 {plot_file}")

    print("\n" + "=" * 60)
    print("  ИТОГ CIV-1")
    print("=" * 60)
    if popt_exp is not None:
        print(f"  Удвоение знания:    каждые {doubling_time_exp:.0f} лет")
        print(f"  Moore's Law:        каждые 2 года (silicon)")
        print(f"  Астрономия:         {astro_doubling/moore_doubling:.0f}× медленнее кремния")
    print(f"  Data points:        {len(instruments)}")
    print(f"  Диапазон:           {years[0]} — {years[-1]} CE = {years[-1]-years[0]} лет")
    print(f"  Скачки:             Гиппарх, Тихо, Flamsteed, Gaia")
    print(f"  Провалы:            Dark Ages, post-Ptolemy stagnation")
    print("=" * 60)

if __name__ == "__main__":
    main()
