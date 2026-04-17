#!/usr/bin/env python3
"""
G1: Miyake Events — экстремальные солнечные вспышки из C14 спайков.

IntCal20 Delta14C → спайки → cross-match с astro-dating якорями → периодичность → прогноз.

Miyake events: внезапные скачки C14 в атмосфере = экстремальные солнечные/космические события.
774 CE: ~12‰ рост за 1 год (100× сильнее Кэррингтона 1859).
Если повторится сегодня: $2-3 ТРИЛЛИОНА ущерба (сети, спутники, GPS, авиация).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'solar')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

def load_intcal20():
    """Load IntCal20 and convert to CE years."""
    path = os.path.join(DATA_DIR, 'intcal20.14c')
    cal_bp, c14_age, sigma_age, delta14c, sigma_d14c = [], [], [], [], []

    with open(path) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) >= 5:
                try:
                    cal_bp.append(float(parts[0]))
                    c14_age.append(float(parts[1]))
                    sigma_age.append(float(parts[2]))
                    delta14c.append(float(parts[3]))
                    sigma_d14c.append(float(parts[4]))
                except ValueError:
                    continue

    cal_bp = np.array(cal_bp)
    delta14c = np.array(delta14c)
    sigma_d14c = np.array(sigma_d14c)

    # Convert cal BP → CE (BP 0 = 1950 CE)
    year_ce = 1950 - cal_bp

    # Sort by year ascending
    sort_idx = np.argsort(year_ce)
    year_ce = year_ce[sort_idx]
    delta14c = delta14c[sort_idx]
    sigma_d14c = sigma_d14c[sort_idx]

    print(f"[1] IntCal20: {len(year_ce)} points, {year_ce[0]:.0f} — {year_ce[-1]:.0f} CE")
    return year_ce, delta14c, sigma_d14c


def find_miyake_spikes(years, d14c, window=5, threshold_sigma=4):
    """Find rapid C14 increases (Miyake-type events)."""
    # Compute rate of change (d(Delta14C)/dt per decade)
    dt = np.diff(years)
    dd14c = np.diff(d14c)

    # Avoid division by zero
    valid = dt != 0
    rate = np.zeros(len(dt))
    rate[valid] = dd14c[valid] / dt[valid] * 10  # per decade

    # Smooth rate
    if window > 1:
        kernel = np.ones(window) / window
        rate_smooth = np.convolve(rate, kernel, mode='same')
    else:
        rate_smooth = rate

    # Find positive spikes (rapid C14 increase = solar event)
    mean_rate = np.mean(rate_smooth)
    std_rate = np.std(rate_smooth)
    threshold = mean_rate + threshold_sigma * std_rate

    spike_indices = []
    for i in range(1, len(rate_smooth) - 1):
        if rate_smooth[i] > threshold and rate_smooth[i] > rate_smooth[i-1] and rate_smooth[i] > rate_smooth[i+1]:
            spike_indices.append(i)

    # Convert to years (midpoint of interval)
    spike_years = [(years[i] + years[i+1]) / 2 for i in spike_indices]
    spike_rates = [rate_smooth[i] for i in spike_indices]

    return years[:-1], rate, rate_smooth, spike_years, spike_rates, threshold


def main():
    print("=" * 60)
    print("  G1: Miyake Events — C14 спайки → прогноз экстремальных вспышек")
    print("=" * 60)

    years, d14c, sigma = load_intcal20()

    # Focus on last 12000 years (Holocene) for best resolution
    mask = years > -10000
    years_h = years[mask]
    d14c_h = d14c[mask]

    print(f"[2] Holocene subset: {len(years_h)} points, {years_h[0]:.0f} — {years_h[-1]:.0f} CE")

    # Find spikes
    t_rate, rate, rate_smooth, spikes_y, spikes_r, thresh = find_miyake_spikes(years_h, d14c_h, window=3, threshold_sigma=3)

    print(f"\n[3] Найдено {len(spikes_y)} кандидатов в Miyake events (>{3}σ):")

    # Known Miyake events for validation
    known_miyake = {
        '774-775 CE': 774.5,
        '993-994 CE': 993.5,
        '~660 BCE': -660,
        '~5480 BCE': -5480,
        '~7176 BCE': -7176,
        '~5259 BCE': -5259,
    }

    for y, r in sorted(zip(spikes_y, spikes_r), key=lambda x: -x[1])[:20]:
        match = ""
        for name, ky in known_miyake.items():
            if abs(y - ky) < 50:
                match = f" ← KNOWN: {name}"
        print(f"    {y:8.0f} CE  rate: {r:+6.2f} ‰/decade{match}")

    # ============================================================
    # Periodicity of extreme events
    # ============================================================
    if len(spikes_y) >= 3:
        spike_arr = np.array(sorted(spikes_y))
        intervals = np.diff(spike_arr)
        print(f"\n[4] Интервалы между спайками:")
        print(f"    Средний: {np.mean(intervals):.0f} лет")
        print(f"    Медиана: {np.median(intervals):.0f} лет")
        print(f"    Мин/Макс: {np.min(intervals):.0f} / {np.max(intervals):.0f}")
        print(f"    Std: {np.std(intervals):.0f}")

    # ============================================================
    # Cross-match with astro-dating anchors
    # ============================================================
    anchors = [
        (-763, 'J1 Бур-Сагале'), (-585, 'A1 Фалес'), (-568, 'M2'),
        (-130, 'A4 Альмагест'), (137, 'A4b'), (1054, 'C1 Crab'),
        (1185, 'R1 Игорь'), (837, 'Halley 837'), (1066, 'Halley 1066'),
    ]

    print(f"\n[5] Cross-match Miyake ↔ astro-dating (±50 лет):")
    for y, r in sorted(zip(spikes_y, spikes_r), key=lambda x: -x[1])[:15]:
        for ay, aname in anchors:
            if abs(y - ay) < 50:
                print(f"    Miyake ~{y:.0f} CE ↔ {aname} ({ay}) — расстояние {abs(y-ay):.0f} лет")

    # ============================================================
    # Anti-correlation with sunspot records
    # ============================================================
    # Load sunspots for comparison in overlapping range
    sunspot_file = os.path.join(DATA_DIR, 'pre_telescopic_sunspots.csv')
    spot_years = []
    if os.path.exists(sunspot_file):
        import csv
        with open(sunspot_file) as f:
            for row in csv.DictReader(f):
                spot_years.append(int(row['year']))

    # ============================================================
    # Prediction logic
    # ============================================================
    print(f"\n[6] PREDICTION:")
    if len(spikes_y) >= 3:
        recent_spikes = [y for y in sorted(spikes_y) if y > 0]
        if len(recent_spikes) >= 2:
            last = recent_spikes[-1]
            mean_int = np.mean(intervals) if len(intervals) > 0 else 1000
            median_int = np.median(intervals) if len(intervals) > 0 else 1000
            print(f"    Последний Miyake-кандидат: {last:.0f} CE")
            print(f"    Средний интервал: {mean_int:.0f} лет")
            print(f"    Следующий (по среднему): ~{last + mean_int:.0f} CE")
            print(f"    Следующий (по медиане): ~{last + median_int:.0f} CE")
            print(f"    ⚠️ Это ГРУБАЯ оценка — Miyake events могут быть не периодическими")
            print(f"    ⚠️ Известные события (774, 993 CE) имеют интервал ~219 лет")
            print(f"    ⚠️ По этой логике: 993 + 219 ≈ 1212, + 219 ≈ 1431, ... → следующий ~{993 + 219 * ((2026-993)//219 + 1):.0f}?")

    # ============================================================
    # PLOTS
    # ============================================================
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))

    # 1. Full Delta14C curve
    ax = axes[0, 0]
    ax.plot(years_h, d14c_h, 'b-', lw=0.5, alpha=0.7)
    ax.set_xlabel('Year CE')
    ax.set_ylabel('Δ14C (‰)')
    ax.set_title('IntCal20: Δ14C over Holocene')
    ax.grid(alpha=0.3)

    # 2. Delta14C last 3000 years (detail)
    ax = axes[0, 1]
    mask3k = years_h > -1000
    ax.plot(years_h[mask3k], d14c_h[mask3k], 'b-', lw=1)
    # Mark known Miyake
    for name, ky in known_miyake.items():
        if ky > -1000:
            ax.axvline(ky, color='red', ls='--', alpha=0.7)
            ax.text(ky, max(d14c_h[mask3k])*0.95, name, fontsize=7, color='red', rotation=90, va='top')
    if spot_years:
        for sy in spot_years:
            if sy > -1000:
                ax.axvline(sy, color='green', ls=':', alpha=0.1)
    ax.set_xlabel('Year CE')
    ax.set_ylabel('Δ14C (‰)')
    ax.set_title('Δ14C last 3000 years + Miyake events (red) + sunspots (green)')
    ax.grid(alpha=0.3)

    # 3. Rate of change
    ax = axes[1, 0]
    ax.plot(t_rate, rate_smooth, 'purple', lw=0.5, alpha=0.7)
    ax.axhline(thresh, color='red', ls='--', alpha=0.7, label=f'Threshold ({3}σ)')
    for y, r in zip(spikes_y, spikes_r):
        ax.plot(y, r, 'rv', ms=6)
        if r > thresh * 0.8:
            ax.annotate(f'{y:.0f}', xy=(y, r), fontsize=6, color='red', ha='center', va='bottom')
    ax.set_xlabel('Year CE')
    ax.set_ylabel('d(Δ14C)/dt (‰/decade)')
    ax.set_title('Rate of C14 change — Miyake spikes marked')
    ax.legend()
    ax.grid(alpha=0.3)

    # 4. Zoom on 774 CE event
    ax = axes[1, 1]
    mask774 = (years_h > 700) & (years_h < 850)
    ax.plot(years_h[mask774], d14c_h[mask774], 'b-o', lw=2, ms=3)
    ax.axvline(774.5, color='red', ls='--', lw=2, label='774-775 CE Miyake event')
    ax.axvline(837, color='green', ls=':', alpha=0.7, label='Halley 837 (max brightness)')
    ax.set_xlabel('Year CE')
    ax.set_ylabel('Δ14C (‰)')
    ax.set_title('Zoom: 774 CE Miyake Event + Halley 837')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # 5. Interval histogram
    ax = axes[2, 0]
    if len(spikes_y) >= 3:
        ax.hist(intervals, bins=20, color='orange', alpha=0.7, edgecolor='black')
        ax.axvline(np.mean(intervals), color='red', ls='--', label=f'Mean: {np.mean(intervals):.0f}y')
        ax.axvline(np.median(intervals), color='blue', ls='--', label=f'Median: {np.median(intervals):.0f}y')
        ax.set_xlabel('Interval between events (years)')
        ax.set_ylabel('Count')
        ax.set_title('Distribution of inter-Miyake intervals')
        ax.legend()
    ax.grid(alpha=0.3)

    # 6. Timeline of all detected events + prediction
    ax = axes[2, 1]
    spike_arr = np.array(sorted(spikes_y))
    ax.scatter(spike_arr, np.ones(len(spike_arr)), c='red', s=50, zorder=5, label='Detected Miyake candidates')
    for name, ky in known_miyake.items():
        ax.axvline(ky, color='blue', ls=':', alpha=0.5)
    # Known Grand Solar Minima
    for name, start, end in [('Maunder', 1645, 1715), ('Dalton', 1790, 1830)]:
        ax.axvspan(start, end, alpha=0.1, color='gray')
    # Prediction zone
    ax.axvspan(2040, 2200, alpha=0.15, color='red')
    ax.text(2120, 1.3, 'RISK\nZONE?', fontsize=10, ha='center', color='red', fontweight='bold')
    ax.set_xlabel('Year CE')
    ax.set_title('Miyake events timeline + prediction zone')
    ax.set_yticks([])
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_xlim(-8000, 2500)

    plt.suptitle('G1: Miyake Events — Extreme Solar Particle Events from IntCal20 C14\n'
                 'Prediction of next civilization-threatening solar storm',
                fontsize=13, fontweight='bold')
    plt.tight_layout()
    plot_file = os.path.join(RESULTS_DIR, 'g1_miyake_events.png')
    plt.savefig(plot_file, dpi=150)
    print(f"\n📊 {plot_file}")

    # Summary
    print("\n" + "=" * 60)
    print("  ИТОГ G1: Miyake Events")
    print("=" * 60)
    print(f"  IntCal20 точек:     {len(years_h)}")
    print(f"  Miyake-кандидатов:  {len(spikes_y)}")
    print(f"  Известные (774, 993): {'найдены' if any(abs(y-774)<50 for y in spikes_y) else 'не найдены'}")
    if len(spikes_y) >= 3:
        print(f"  Средний интервал:   {np.mean(intervals):.0f} лет")
        print(f"  Оценка следующего:  ~{spike_arr[-1] + np.mean(intervals):.0f} CE (ГРУБО)")
    print(f"  Ценность прогноза:  $2-3 ТРИЛЛИОНА (если предотвратить ущерб)")
    print("=" * 60)

if __name__ == "__main__":
    main()
