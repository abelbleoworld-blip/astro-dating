#!/usr/bin/env python3
"""
SOL-1 E1: Cross-match pre-telescopic sunspots с astro-dating якорями + FFT analysis.
"""

import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'solar')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# 1. Load pre-telescopic sunspots
# ============================================================

def load_sunspots():
    spots = []
    with open(os.path.join(DATA_DIR, 'pre_telescopic_sunspots.csv')) as f:
        for row in csv.DictReader(f):
            spots.append({
                'year': int(row['year']),
                'country': row['country'],
                'source': row['source'],
                'desc': row['description'],
            })
    print(f"[1] Загружено {len(spots)} записей пятен ({spots[0]['year']} — {spots[-1]['year']} CE)")
    return spots

# ============================================================
# 2. Astro-dating anchors for cross-match
# ============================================================

ANCHORS = [
    {'id': 'J1', 'year': -763, 'name': 'Бур-Сагале eclipse', 'type': 'eclipse'},
    {'id': 'A1', 'year': -585, 'name': 'Фалес eclipse', 'type': 'eclipse'},
    {'id': 'M2', 'year': -568, 'name': 'Навуходоносор VAT4956', 'type': 'diary'},
    {'id': 'A4', 'year': -130, 'name': 'Альмагест Гиппарх', 'type': 'catalog'},
    {'id': 'A4b', 'year': 137, 'name': 'Альмагест Птолемей', 'type': 'catalog'},
    {'id': 'C1', 'year': 1054, 'name': 'Crab Supernova SN1054', 'type': 'supernova'},
    {'id': 'R1', 'year': 1185, 'name': 'Игорь eclipse', 'type': 'eclipse'},
    # Halley comet appearances (Yeomans & Kiang 1981)
    {'id': 'H01', 'year': -240, 'name': 'Halley -240', 'type': 'comet'},
    {'id': 'H02', 'year': -164, 'name': 'Halley -164', 'type': 'comet'},
    {'id': 'H03', 'year': -87, 'name': 'Halley -87', 'type': 'comet'},
    {'id': 'H04', 'year': -12, 'name': 'Halley -12', 'type': 'comet'},
    {'id': 'H05', 'year': 66, 'name': 'Halley 66', 'type': 'comet'},
    {'id': 'H06', 'year': 141, 'name': 'Halley 141', 'type': 'comet'},
    {'id': 'H07', 'year': 218, 'name': 'Halley 218', 'type': 'comet'},
    {'id': 'H08', 'year': 295, 'name': 'Halley 295', 'type': 'comet'},
    {'id': 'H09', 'year': 374, 'name': 'Halley 374', 'type': 'comet'},
    {'id': 'H10', 'year': 451, 'name': 'Halley 451', 'type': 'comet'},
    {'id': 'H11', 'year': 530, 'name': 'Halley 530', 'type': 'comet'},
    {'id': 'H12', 'year': 607, 'name': 'Halley 607', 'type': 'comet'},
    {'id': 'H13', 'year': 684, 'name': 'Halley 684', 'type': 'comet'},
    {'id': 'H14', 'year': 760, 'name': 'Halley 760', 'type': 'comet'},
    {'id': 'H15', 'year': 837, 'name': 'Halley 837', 'type': 'comet'},
    {'id': 'H16', 'year': 912, 'name': 'Halley 912', 'type': 'comet'},
    {'id': 'H17', 'year': 989, 'name': 'Halley 989', 'type': 'comet'},
    {'id': 'H18', 'year': 1066, 'name': 'Halley 1066 (Hastings)', 'type': 'comet'},
    {'id': 'H19', 'year': 1145, 'name': 'Halley 1145', 'type': 'comet'},
    {'id': 'H20', 'year': 1222, 'name': 'Halley 1222', 'type': 'comet'},
    {'id': 'H21', 'year': 1301, 'name': 'Halley 1301 (Giotto)', 'type': 'comet'},
    {'id': 'H22', 'year': 1378, 'name': 'Halley 1378', 'type': 'comet'},
    {'id': 'H23', 'year': 1456, 'name': 'Halley 1456', 'type': 'comet'},
    {'id': 'H24', 'year': 1531, 'name': 'Halley 1531', 'type': 'comet'},
    {'id': 'H25', 'year': 1607, 'name': 'Halley 1607', 'type': 'comet'},
]

# ============================================================
# 3. Cross-match: sunspot ± 10 years from anchor
# ============================================================

def cross_match(spots, anchors, window=10):
    verified = []
    unverified = []
    for s in spots:
        matched = []
        for a in anchors:
            if abs(s['year'] - a['year']) <= window:
                matched.append(a)
        if matched:
            s['anchors'] = matched
            s['verified'] = True
            verified.append(s)
        else:
            s['anchors'] = []
            s['verified'] = False
            unverified.append(s)

    print(f"\n[2] Cross-match (±{window} лет):")
    print(f"    Верифицированных: {len(verified)} / {len(spots)} ({100*len(verified)/len(spots):.0f}%)")
    print(f"    Не верифицированных: {len(unverified)}")

    print(f"\n    Примеры верифицированных:")
    for s in verified[:10]:
        anchors_str = ', '.join(a['id'] for a in s['anchors'])
        print(f"      {s['year']:5d} CE ({s['country']:6s}) ← якоря: {anchors_str}")

    return verified, unverified

# ============================================================
# 4. Build time series + FFT
# ============================================================

def build_time_series(spots, year_min=-50, year_max=1610, bin_size=10):
    """Count sunspot records per decade."""
    bins = np.arange(year_min, year_max + bin_size, bin_size)
    counts = np.zeros(len(bins) - 1)
    for s in spots:
        idx = np.searchsorted(bins, s['year']) - 1
        if 0 <= idx < len(counts):
            counts[idx] += 1
    centers = (bins[:-1] + bins[1:]) / 2
    return centers, counts

def fft_analysis(years, counts, label=""):
    """Run FFT and find dominant periods."""
    # Remove mean
    counts_centered = counts - np.mean(counts)
    # Zero-pad for better resolution
    n = len(counts_centered)
    n_pad = max(n * 4, 1024)

    # FFT
    fft_vals = np.fft.rfft(counts_centered, n=n_pad)
    power = np.abs(fft_vals) ** 2

    dt = years[1] - years[0] if len(years) > 1 else 10  # bin size in years
    freqs = np.fft.rfftfreq(n_pad, d=dt)

    # Convert to periods (skip DC component)
    valid = freqs[1:] > 0
    periods = 1.0 / freqs[1:][valid]
    power_valid = power[1:][valid]

    # Find peaks
    peak_indices, props = signal.find_peaks(power_valid, height=np.max(power_valid) * 0.1, distance=3)

    target_periods = {
        'Schwabe': 11,
        'Hale': 22,
        'Gleissberg': 88,
        'Suess/de Vries': 210,
        'Unknown ~400': 400,
    }

    print(f"\n[3] FFT Analysis ({label}):")
    print(f"    Data points: {len(counts)}, bin size: {dt} years, span: {years[0]:.0f}—{years[-1]:.0f}")
    print(f"\n    Найденные пики (>10% max power):")
    for i in peak_indices[:15]:
        p = periods[i]
        pw = power_valid[i]
        # Check if near known cycle
        match = ""
        for name, target in target_periods.items():
            if abs(p - target) / target < 0.25:
                match = f" ← {name}!"
        print(f"      Period: {p:7.1f} years  Power: {pw:12.1f}{match}")

    return periods, power_valid, peak_indices

# ============================================================
# 5. Combined analysis with SILSO
# ============================================================

def load_silso_yearly():
    """Load SILSO yearly sunspot numbers."""
    years, ssn = [], []
    path = os.path.join(DATA_DIR, 'silso_yearly.csv')
    with open(path) as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) >= 2:
                try:
                    y = int(float(parts[0].strip()))
                    s = float(parts[1].strip())
                    if s >= 0:
                        years.append(y)
                        ssn.append(s)
                except ValueError:
                    continue
    print(f"\n[4] SILSO yearly: {len(years)} years ({years[0]}—{years[-1]})")
    return np.array(years), np.array(ssn)

# ============================================================
# 6. Main
# ============================================================

def main():
    print("=" * 60)
    print("  SOL-1 E1: Pre-telescopic sunspots × astro-dating anchors")
    print("=" * 60)

    # Load
    spots = load_sunspots()

    # Cross-match
    verified, unverified = cross_match(spots, ANCHORS, window=10)

    # Time series ALL
    years_all, counts_all = build_time_series(spots)

    # Time series VERIFIED only
    years_ver, counts_ver = build_time_series(verified)

    # FFT on all pre-telescopic
    periods_all, power_all, peaks_all = fft_analysis(years_all, counts_all, "All pre-telescopic")

    # FFT on verified only
    if len(verified) > 10:
        periods_ver, power_ver, peaks_ver = fft_analysis(years_ver, counts_ver, "Verified only")

    # Load SILSO for comparison
    silso_years, silso_ssn = load_silso_yearly()

    # FFT on SILSO (modern baseline)
    # Decadal bins for comparison
    silso_decades = np.arange(1700, 2030, 10)
    silso_counts = np.zeros(len(silso_decades) - 1)
    for i, y in enumerate(silso_years):
        idx = np.searchsorted(silso_decades, y) - 1
        if 0 <= idx < len(silso_counts):
            silso_counts[idx] += silso_ssn[i]
    silso_centers = (silso_decades[:-1] + silso_decades[1:]) / 2
    periods_silso, power_silso, peaks_silso = fft_analysis(silso_centers, silso_counts, "SILSO 1700-2025")

    # ============================================================
    # PLOTS
    # ============================================================

    fig, axes = plt.subplots(3, 2, figsize=(16, 14))

    # 1. Timeline of all sunspot records
    ax = axes[0, 0]
    spot_years_all = [s['year'] for s in spots]
    spot_years_ver = [s['year'] for s in verified]
    ax.hist(spot_years_all, bins=50, alpha=0.5, color='blue', label=f'Все ({len(spots)})')
    ax.hist(spot_years_ver, bins=50, alpha=0.7, color='red', label=f'Верифицированные ({len(verified)})')
    ax.set_xlabel('Год CE')
    ax.set_ylabel('Записей / бин')
    ax.set_title('Записи пятен: все vs верифицированные якорями')
    ax.legend()
    ax.grid(alpha=0.3)

    # 2. Time series decadal
    ax = axes[0, 1]
    ax.bar(years_all, counts_all, width=8, alpha=0.5, color='blue', label='Все')
    ax.bar(years_ver, counts_ver, width=6, alpha=0.7, color='red', label='Верифицированные')
    ax.set_xlabel('Год CE (бины по 10 лет)')
    ax.set_ylabel('Записей / декада')
    ax.set_title('Декадная серия записей пятен')
    ax.legend()
    ax.grid(alpha=0.3)

    # 3. FFT pre-telescopic (all)
    ax = axes[1, 0]
    valid_range = (periods_all > 5) & (periods_all < 800)
    ax.semilogy(periods_all[valid_range], power_all[valid_range], 'b-', lw=1, alpha=0.7)
    for i in peaks_all:
        if 5 < periods_all[i] < 800:
            ax.annotate(f'{periods_all[i]:.0f}y', xy=(periods_all[i], power_all[i]),
                       fontsize=8, color='red', ha='center', va='bottom')
    for name, target in {'Schwabe 11': 11, 'Hale 22': 22, 'Gleissberg 88': 88, 'Suess 210': 210}.items():
        ax.axvline(target, color='green', ls=':', alpha=0.5)
        ax.text(target, ax.get_ylim()[1] * 0.5, name, fontsize=7, color='green', rotation=90, va='top')
    ax.set_xlabel('Период (лет)')
    ax.set_ylabel('Мощность (log)')
    ax.set_title('FFT: Pre-telescopic sunspots (все)')
    ax.grid(alpha=0.3)

    # 4. FFT SILSO (modern)
    ax = axes[1, 1]
    valid_range_s = (periods_silso > 5) & (periods_silso < 200)
    ax.semilogy(periods_silso[valid_range_s], power_silso[valid_range_s], 'r-', lw=1, alpha=0.7)
    for i in peaks_silso:
        if 5 < periods_silso[i] < 200:
            ax.annotate(f'{periods_silso[i]:.0f}y', xy=(periods_silso[i], power_silso[i]),
                       fontsize=8, color='darkred', ha='center', va='bottom')
    for name, target in {'Schwabe 11': 11, 'Hale 22': 22, 'Gleissberg 88': 88}.items():
        ax.axvline(target, color='green', ls=':', alpha=0.5)
        ax.text(target, ax.get_ylim()[1] * 0.5, name, fontsize=7, color='green', rotation=90, va='top')
    ax.set_xlabel('Период (лет)')
    ax.set_ylabel('Мощность (log)')
    ax.set_title('FFT: SILSO 1700-2025 (modern baseline)')
    ax.grid(alpha=0.3)

    # 5. Cross-match map
    ax = axes[2, 0]
    for a in ANCHORS:
        color = {'eclipse': 'red', 'comet': 'blue', 'supernova': 'orange',
                 'catalog': 'green', 'diary': 'purple'}.get(a['type'], 'gray')
        ax.axvline(a['year'], color=color, alpha=0.3, lw=1)
    ax.scatter(spot_years_all, [1]*len(spot_years_all), c='blue', s=10, alpha=0.5, label='Все пятна')
    ax.scatter(spot_years_ver, [1.1]*len(spot_years_ver), c='red', s=20, alpha=0.8, label='Верифицированные')
    ax.set_xlabel('Год CE')
    ax.set_title('Карта cross-match: якоря (вертикали) × пятна (точки)')
    ax.legend(fontsize=8)
    ax.set_yticks([])
    ax.grid(alpha=0.3)

    # 6. Combined SILSO + pre-telescopic
    ax = axes[2, 1]
    ax.bar(years_all, counts_all * 10, width=8, alpha=0.4, color='blue', label='Pre-telescopic (×10 scale)')
    ax.plot(silso_years, silso_ssn, 'r-', lw=0.5, alpha=0.7, label='SILSO SSN 1700-2025')
    ax.set_xlabel('Год CE')
    ax.set_ylabel('Sunspot Number / scaled count')
    ax.set_title('2054 лет солнечной активности (pre-telescopic + SILSO)')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    plt.suptitle('SOL-1 E1: Pre-telescopic Sunspots × Astro-dating Verification + FFT',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plot_file = os.path.join(RESULTS_DIR, 'sol1_e1_sunspots_fft.png')
    plt.savefig(plot_file, dpi=150)
    print(f"\n📊 Графики: {plot_file}")

    # Report
    report_file = os.path.join(RESULTS_DIR, 'sol1_e1_report.md')
    with open(report_file, 'w') as f:
        f.write("# SOL-1 E1: Pre-telescopic sunspots — cross-match + FFT\n\n")
        f.write(f"**Дата:** {__import__('datetime').datetime.now().isoformat()[:19]}\n\n")
        f.write(f"## Данные\n- Pre-telescopic: {len(spots)} записей ({spots[0]['year']}—{spots[-1]['year']})\n")
        f.write(f"- SILSO: {len(silso_years)} лет ({silso_years[0]}—{silso_years[-1]})\n")
        f.write(f"- Якорей для cross-match: {len(ANCHORS)}\n\n")
        f.write(f"## Cross-match (±10 лет)\n")
        f.write(f"- Верифицированных: **{len(verified)}** / {len(spots)} ({100*len(verified)/len(spots):.0f}%)\n")
        f.write(f"- Не верифицированных: {len(unverified)}\n\n")
        f.write("## Верифицированные записи\n\n| Year | Country | Source | Anchor |\n|---|---|---|---|\n")
        for s in verified:
            anchors_str = ', '.join(a['id'] for a in s['anchors'])
            f.write(f"| {s['year']} | {s['country']} | {s['source']} | {anchors_str} |\n")
        f.write("\n## FFT выводы\nСм. графики.\n")
    print(f"📋 Отчёт: {report_file}")

    # Summary
    print("\n" + "=" * 60)
    print("  ИТОГ SOL-1 E1")
    print("=" * 60)
    print(f"  Записей пятен:    {len(spots)}")
    print(f"  Верифицированных: {len(verified)} ({100*len(verified)/len(spots):.0f}%)")
    print(f"  SILSO лет:        {len(silso_years)}")
    print(f"  Общий базлайн:    {spots[0]['year']} — {silso_years[-1]} = {silso_years[-1] - spots[0]['year']} лет")
    print("=" * 60)

if __name__ == "__main__":
    main()
