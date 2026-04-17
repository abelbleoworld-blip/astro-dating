#!/usr/bin/env python3
"""
G3: Aurora → геомагнитные бури → прогноз Кэррингтон-class событий.
104 записи (567-2003 CE) × cross-match с astro-dating якорями → FFT → prediction.
"""
import csv, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'solar')
RESULTS = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS, exist_ok=True)

ANCHORS = [
    (-763,'J1'), (-585,'A1'), (-568,'M2'), (-130,'A4'), (137,'A4b'),
    (1054,'C1'), (1185,'R1'),
    (-239,'H01'), (-163,'H02'), (-86,'H03'), (-11,'H04'), (66,'H05'),
    (141,'H06'), (218,'H07'), (295,'H08'), (374,'H09'), (451,'H10'),
    (530,'H11'), (607,'H12'), (684,'H13'), (760,'H14'), (837,'H15'),
    (912,'H16'), (989,'H17'), (1066,'H18'), (1145,'H19'), (1222,'H20'),
    (1301,'H21'), (1378,'H22'), (1456,'H23'), (1531,'H24'), (1607,'H25'),
    (1682,'H26'), (1759,'H27'), (1835,'H28'), (1910,'H29'), (1986,'H30'),
]

def load_aurora():
    rows = []
    with open(os.path.join(DATA, 'aurora_catalog.csv')) as f:
        for r in csv.DictReader(f):
            rows.append({'year': int(r['year']), 'intensity': int(r['intensity']),
                        'country': r['country'], 'desc': r['description']})
    print(f"[1] Aurora: {len(rows)} records ({rows[0]['year']}—{rows[-1]['year']} CE)")
    return rows

def cross_match(auroras, window=10):
    verified, unverified = [], []
    for a in auroras:
        matches = [anc for ay, anc in ANCHORS if abs(a['year'] - ay) <= window]
        a['anchors'] = matches
        (verified if matches else unverified).append(a)
    pct = 100 * len(verified) / len(auroras)
    print(f"[2] Cross-match ±{window}y: verified {len(verified)}/{len(auroras)} ({pct:.0f}%)")
    return verified, unverified

def build_ts(auroras, year_min=560, year_max=2010, binsz=10):
    bins = np.arange(year_min, year_max + binsz, binsz)
    counts = np.zeros(len(bins)-1)
    intensity_sum = np.zeros(len(bins)-1)
    for a in auroras:
        idx = np.searchsorted(bins, a['year']) - 1
        if 0 <= idx < len(counts):
            counts[idx] += 1
            intensity_sum[idx] += a['intensity']
    centers = (bins[:-1] + bins[1:]) / 2
    return centers, counts, intensity_sum

def do_fft(t, vals, label):
    vals_c = vals - np.mean(vals)
    n_pad = max(len(vals_c) * 4, 512)
    fft = np.fft.rfft(vals_c, n=n_pad)
    power = np.abs(fft)**2
    dt = t[1] - t[0]
    freqs = np.fft.rfftfreq(n_pad, d=dt)
    valid = freqs[1:] > 0
    periods = 1.0 / freqs[1:][valid]
    pwr = power[1:][valid]
    peaks, _ = signal.find_peaks(pwr, height=np.max(pwr)*0.1, distance=3)
    targets = {'Schwabe': 11, 'Hale': 22, 'Gleissberg': 88, 'Suess': 210, '~400': 400}
    print(f"\n[FFT] {label}:")
    for i in peaks[:12]:
        p = periods[i]
        if 10 < p < 800:
            match = next((f" ← {n}!" for n,t in targets.items() if abs(p-t)/t < 0.25), "")
            print(f"    {p:7.1f} years  power: {pwr[i]:10.1f}{match}")
    return periods, pwr, peaks

def extreme_analysis(auroras):
    extreme = [a for a in auroras if a['intensity'] >= 5]
    print(f"\n[3] Extreme events (intensity ≥ 5): {len(extreme)}")
    for e in extreme:
        anc = ', '.join(e.get('anchors', []))
        print(f"    {e['year']} CE ({e['country']}) {e['desc'][:50]}  anchors: {anc or 'none'}")
    if len(extreme) >= 2:
        eyears = sorted(e['year'] for e in extreme)
        intervals = np.diff(eyears)
        print(f"\n    Extreme intervals: {list(intervals)}")
        print(f"    Mean: {np.mean(intervals):.0f} years")
        print(f"    Median: {np.median(intervals):.0f} years")
        print(f"    Last extreme: {eyears[-1]}")
        print(f"    Next by mean: ~{eyears[-1] + np.mean(intervals):.0f}")
        print(f"    Next by median: ~{eyears[-1] + np.median(intervals):.0f}")

        # Carrington prediction
        print(f"\n[4] CARRINGTON PREDICTION:")
        print(f"    7 extreme events over {eyears[-1]-eyears[0]} years = 1 per {(eyears[-1]-eyears[0])/len(extreme):.0f} years")
        recurrence = (eyears[-1] - eyears[0]) / (len(extreme) - 1)
        print(f"    Recurrence interval: {recurrence:.0f} years")
        print(f"    Last: {eyears[-1]}, next expected: ~{eyears[-1] + recurrence:.0f} CE")
        print(f"    Probability in next 30 years (2026-2056): ~{min(30/recurrence*100, 100):.0f}%")
        return eyears, intervals, recurrence
    return [], [], 0

def main():
    print("=" * 60)
    print("  G3: Aurora → Geomagnetic Storms → Carrington Prediction")
    print("=" * 60)

    auroras = load_aurora()
    verified, unverified = cross_match(auroras)
    eyears, intervals, recurrence = extreme_analysis(auroras)

    # Time series
    t_all, c_all, i_all = build_ts(auroras)
    t_ver, c_ver, i_ver = build_ts(verified)

    # FFT all
    p_all, pw_all, pk_all = do_fft(t_all, c_all, "All aurora (count)")
    p_int, pw_int, pk_int = do_fft(t_all, i_all, "All aurora (intensity-weighted)")
    if len(verified) > 20:
        p_ver, pw_ver, pk_ver = do_fft(t_ver, c_ver, "Verified only (count)")

    # Load sunspot data for cross-correlation
    spot_years = []
    sf = os.path.join(DATA, 'pre_telescopic_sunspots.csv')
    if os.path.exists(sf):
        with open(sf) as f:
            for r in csv.DictReader(f):
                spot_years.append(int(r['year']))

    # ============================================================
    # PLOTS
    # ============================================================
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))

    # 1. Timeline
    ax = axes[0, 0]
    colors_i = {1:'lightblue', 2:'blue', 3:'orange', 4:'red', 5:'darkred'}
    for a in auroras:
        ax.scatter(a['year'], a['intensity'], c=colors_i.get(a['intensity'],'gray'), s=30, alpha=0.7, zorder=3)
    ax.plot(t_all, c_all, 'b-', alpha=0.3, lw=1)
    for e in eyears:
        ax.axvline(e, color='red', ls='--', alpha=0.3)
    ax.set_xlabel('Year CE')
    ax.set_ylabel('Intensity (1-5) / count per decade')
    ax.set_title(f'104 aurora records — 7 extreme (red dashed)')
    ax.grid(alpha=0.3)

    # 2. Decadal activity
    ax = axes[0, 1]
    ax.bar(t_all, i_all, width=8, alpha=0.5, color='purple', label='Intensity-weighted')
    ax.bar(t_ver, i_ver, width=6, alpha=0.7, color='red', label='Verified')
    # Grand Solar Minima
    for name, s, e in [('Spörer',1460,1550),('Maunder',1645,1715),('Dalton',1790,1830)]:
        ax.axvspan(s, e, alpha=0.1, color='blue')
        ax.text((s+e)/2, max(i_all)*0.9, name, fontsize=7, ha='center', color='blue')
    ax.set_xlabel('Year CE (10-year bins)')
    ax.set_ylabel('Intensity sum / decade')
    ax.set_title('Aurora activity + Grand Solar Minima')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # 3. FFT all
    ax = axes[1, 0]
    v = (p_all > 10) & (p_all < 600)
    ax.semilogy(p_all[v], pw_all[v], 'b-', lw=1)
    for i in pk_all:
        if 10 < p_all[i] < 600:
            ax.annotate(f'{p_all[i]:.0f}y', xy=(p_all[i], pw_all[i]), fontsize=7, color='red')
    for n,t in {'Gleissberg 88':88, 'Suess 210':210, '~400':400}.items():
        ax.axvline(t, color='green', ls=':', alpha=0.5)
    ax.set_xlabel('Period (years)')
    ax.set_ylabel('Power')
    ax.set_title('FFT: Aurora count')
    ax.grid(alpha=0.3)

    # 4. FFT intensity
    ax = axes[1, 1]
    v2 = (p_int > 10) & (p_int < 600)
    ax.semilogy(p_int[v2], pw_int[v2], 'purple', lw=1)
    for i in pk_int:
        if 10 < p_int[i] < 600:
            ax.annotate(f'{p_int[i]:.0f}y', xy=(p_int[i], pw_int[i]), fontsize=7, color='darkred')
    for n,t in {'Gleissberg 88':88, 'Suess 210':210}.items():
        ax.axvline(t, color='green', ls=':', alpha=0.5)
    ax.set_xlabel('Period (years)')
    ax.set_ylabel('Power')
    ax.set_title('FFT: Aurora intensity-weighted')
    ax.grid(alpha=0.3)

    # 5. Extreme events timeline + prediction
    ax = axes[2, 0]
    if eyears:
        ax.scatter(eyears, [1]*len(eyears), c='red', s=100, zorder=5, marker='*')
        for y in eyears:
            ax.annotate(f'{y}', xy=(y, 1.05), fontsize=8, ha='center', color='red')
        # Prediction zone
        if recurrence > 0:
            pred = eyears[-1] + recurrence
            ax.axvspan(pred - 30, pred + 30, alpha=0.2, color='red')
            ax.text(pred, 0.8, f'NEXT\n~{pred:.0f}?', fontsize=10, ha='center', color='red', fontweight='bold')
    ax.set_xlabel('Year CE')
    ax.set_title('Extreme aurora events (Carrington-class) + prediction')
    ax.set_yticks([])
    ax.grid(alpha=0.3)
    ax.set_xlim(1500, 2150)

    # 6. Interval histogram
    ax = axes[2, 1]
    if len(intervals) > 2:
        ax.hist(intervals, bins=10, color='orange', alpha=0.7, edgecolor='black')
        ax.axvline(np.mean(intervals), color='red', ls='--', label=f'Mean {np.mean(intervals):.0f}y')
        ax.axvline(np.median(intervals), color='blue', ls='--', label=f'Median {np.median(intervals):.0f}y')
        ax.set_xlabel('Interval between extreme events (years)')
        ax.set_ylabel('Count')
        ax.set_title('Extreme aurora recurrence intervals')
        ax.legend()
    ax.grid(alpha=0.3)

    plt.suptitle('G3: Aurora as Geomagnetic Storm Proxy — Carrington Prediction\n'
                 '104 records, 1436 years, 7 extreme events, 4th independent solar proxy',
                fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS, 'g3_aurora_storms.png'), dpi=150)
    print(f"\n📊 {os.path.join(RESULTS, 'g3_aurora_storms.png')}")

    # Summary
    print("\n" + "=" * 60)
    print("  ИТОГ G3")
    print("=" * 60)
    print(f"  Aurora records:     {len(auroras)}")
    print(f"  Verified:           {len(verified)} ({100*len(verified)/len(auroras):.0f}%)")
    print(f"  Extreme events:     {len(eyears)}")
    if recurrence:
        print(f"  Recurrence:         {recurrence:.0f} years")
        print(f"  Last extreme:       {eyears[-1]}")
        print(f"  Next predicted:     ~{eyears[-1]+recurrence:.0f} CE")
        print(f"  P(next 30 years):   ~{min(30/recurrence*100,100):.0f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
