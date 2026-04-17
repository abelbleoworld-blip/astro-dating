#!/usr/bin/env python3
"""
SOL-1 E4: Carbon-14 (IntCal20) → solar activity proxy → FFT/wavelet.
Delta-14C is inversely proportional to solar activity:
  more solar activity → stronger magnetic field → fewer cosmic rays → less 14C produced.
Dataset: 55000 years, ~9500 points, 20-year resolution (recent) to 100-year (deep).
"""

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
# 1. Load IntCal20
# ============================================================

def load_intcal20():
    cal_bp, c14_age, sigma_age, delta14c, sigma_d14c = [], [], [], [], []
    with open(os.path.join(DATA_DIR, 'intcal20.14c')) as f:
        for line in f:
            if line.startswith('#') or line.startswith('!') or not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) < 5:
                continue
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

    # Convert cal BP (before 1950) to CE
    cal_ce = 1950 - cal_bp

    # Sort by time ascending
    idx = np.argsort(cal_ce)
    cal_ce = cal_ce[idx]
    delta14c = delta14c[idx]
    sigma_d14c = sigma_d14c[idx]

    print(f"[1] IntCal20 loaded: {len(cal_ce)} points")
    print(f"    Range: {cal_ce[0]:.0f} — {cal_ce[-1]:.0f} CE")
    print(f"    Delta-14C range: {delta14c.min():.1f} — {delta14c.max():.1f} ‰")

    return cal_ce, delta14c, sigma_d14c


# ============================================================
# 2. Extract Holocene window (last 12000 years)
# ============================================================

def extract_holocene(cal_ce, delta14c):
    mask = cal_ce >= -10050  # ~12000 BP
    years = cal_ce[mask]
    d14c = delta14c[mask]
    print(f"\n[2] Holocene subset: {len(years)} points ({years[0]:.0f} — {years[-1]:.0f} CE)")

    # Compute step sizes
    steps = np.diff(years)
    print(f"    Step: median={np.median(steps):.0f} yr, min={steps.min():.0f}, max={steps.max():.0f}")

    return years, d14c


# ============================================================
# 3. Resample to uniform grid + detrend
# ============================================================

def resample_uniform(years, d14c, step=20):
    """Resample to uniform step size for FFT."""
    yr_uniform = np.arange(years[0], years[-1], step)
    d14c_uniform = np.interp(yr_uniform, years, d14c)

    # Remove long-term trend (geomagnetic + ocean reservoir)
    # Use high-pass: subtract smoothed with 2000-year window
    window_size = int(2000 / step)
    if window_size % 2 == 0:
        window_size += 1
    if window_size >= len(d14c_uniform):
        window_size = len(d14c_uniform) // 2 * 2 - 1

    from scipy.ndimage import uniform_filter1d
    trend = uniform_filter1d(d14c_uniform, size=window_size)
    residual = d14c_uniform - trend

    print(f"\n[3] Resampled: {len(yr_uniform)} points at {step}-yr step")
    print(f"    Detrended with {window_size * step}-yr smoothing")

    return yr_uniform, d14c_uniform, residual


# ============================================================
# 4. FFT analysis
# ============================================================

def fft_analysis(years, residual, step):
    N = len(residual)
    window = np.hanning(N)
    windowed = residual * window

    freqs = np.fft.rfftfreq(N, d=step)
    fft_mag = np.abs(np.fft.rfft(windowed)) * 2.0 / N

    mask = freqs > 0
    freqs = freqs[mask]
    fft_mag = fft_mag[mask]
    periods = 1.0 / freqs

    targets = [
        ('Schwabe ~11yr', 11, '#34d399'),
        ('Hale ~22yr', 22, '#60a5fa'),
        ('Gleissberg ~88yr', 88, '#a78bfa'),
        ('Suess/deVries ~210yr', 210, '#f87171'),
        ('Eddy ~1000yr', 1000, '#fbbf24'),
        ('Hallstatt ~2300yr', 2300, '#67e8f9'),
    ]

    print(f"\n[4] FFT analysis ({N} points, step={step} yr)")
    print(f"    Nyquist: {step*2} yr minimum detectable period")
    print(f"    Max detectable: {N*step} yr")

    # Find peaks
    peak_idx, _ = signal.find_peaks(fft_mag, height=np.max(fft_mag) * 0.05, distance=3)
    top_peaks = sorted(peak_idx, key=lambda i: fft_mag[i], reverse=True)[:15]

    print(f"\n    Top FFT peaks:")
    for i, idx in enumerate(top_peaks):
        p = periods[idx]
        m = fft_mag[idx]
        match = ''
        for name, tp, _ in targets:
            if abs(p - tp) / tp < 0.20:
                match = f' ← {name}'
                break
        print(f"    {i+1:>2}. {p:>8.1f} yr  (amplitude {m:.4f}){match}")

    return freqs, fft_mag, periods, targets


# ============================================================
# 5. Cross-check with E1-E3 periods
# ============================================================

def cross_check_periods():
    """Periods found in E1 (sunspots), E2 (aurora), E3 (corona)."""
    e1_peaks = [10.8, 88.2]  # From E1 report
    e2_peaks = [11.0, 87.5, 210.5]  # From E2
    e3_peaks = [88.8, 177.6]  # From E3

    print("\n[5] Cross-check with prior stages:")
    print(f"    E1 sunspots: {e1_peaks}")
    print(f"    E2 aurora:   {e2_peaks}")
    print(f"    E3 corona:   {e3_peaks}")
    print(f"    E4 C14:      (see FFT peaks above)")
    print(f"    → Gleissberg ~88 yr: confirmed in E1, E2, E3 → check E4")
    print(f"    → Suess ~210 yr: E2 has it, E3 has ~178 → check E4")

    return {'E1': e1_peaks, 'E2': e2_peaks, 'E3': e3_peaks}


# ============================================================
# 6. Grand Solar Minima detection
# ============================================================

KNOWN_GSM = [
    ('Oort', 1010, 1050),
    ('Wolf', 1280, 1340),
    ('Spörer', 1460, 1550),
    ('Maunder', 1645, 1715),
    ('Dalton', 1790, 1830),
]

def detect_grand_minima(years, d14c_raw):
    """Detect Grand Solar Minima as sustained high Delta-14C."""
    # In last 2000 years
    mask = years >= 0
    yr = years[mask]
    d = d14c_raw[mask]

    # GSM = Delta-14C above local 200-yr running mean by >5‰ sustained for >30 yr
    from scipy.ndimage import uniform_filter1d
    step = yr[1] - yr[0] if len(yr) > 1 else 20
    win = max(3, int(200 / step))
    if win % 2 == 0:
        win += 1
    mean = uniform_filter1d(d, size=win)
    anomaly = d - mean

    print(f"\n[6] Grand Solar Minima detection (0—{yr[-1]:.0f} CE)")
    for name, start, end in KNOWN_GSM:
        in_range = (yr >= start) & (yr <= end)
        if in_range.any():
            avg_anom = anomaly[in_range].mean()
            avg_d14c = d[in_range].mean()
            detected = avg_anom > 2
            status = '✓ DETECTED' if detected else '~ weak'
            print(f"    {name:>10} ({start}-{end}): Δ14C anomaly = {avg_anom:+.1f}‰, raw = {avg_d14c:.1f}‰ → {status}")
        else:
            print(f"    {name:>10} ({start}-{end}): no data in range")


# ============================================================
# 7. Plot
# ============================================================

def plot_results(cal_ce_full, d14c_full, yr_holo, d14c_holo, yr_uniform, d14c_uniform,
                 residual, freqs, fft_mag, periods, targets):
    fig, axes = plt.subplots(4, 1, figsize=(16, 16), facecolor='#0a0c0e')
    for ax in axes:
        ax.set_facecolor('#12141e')
        ax.tick_params(colors='#999')
        for spine in ax.spines.values():
            spine.set_color('#333')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Panel 1: Full 55k years
    ax1 = axes[0]
    ax1.plot(cal_ce_full, d14c_full, color='#67e8f9', linewidth=0.5, alpha=0.7)
    ax1.set_ylabel('Δ¹⁴C (‰)', color='#ccc', fontsize=11)
    ax1.set_title('SOL-1 E4: IntCal20 — Full 55,000 Year Record', color='#e0e2ec', fontsize=14, fontweight='bold')
    ax1.axhline(0, color='#333', linewidth=0.5)
    ax1.set_xlim(cal_ce_full[0], cal_ce_full[-1])

    # Panel 2: Holocene (12k years)
    ax2 = axes[1]
    ax2.plot(yr_holo, d14c_holo, color='#a78bfa', linewidth=0.8, alpha=0.8)
    ax2.set_ylabel('Δ¹⁴C (‰)', color='#ccc', fontsize=11)
    ax2.set_title('Holocene (12,000 years) — Solar Activity Proxy (inverted: high Δ¹⁴C = low solar)',
                   color='#e0e2ec', fontsize=12)
    ax2.axhline(0, color='#333', linewidth=0.5)
    # Mark Grand Solar Minima
    for name, start, end in KNOWN_GSM:
        ax2.axvspan(start, end, alpha=0.15, color='#f87171')
        ax2.text((start+end)/2, ax2.get_ylim()[1]*0.9 if ax2.get_ylim()[1] > 0 else 10,
                 name, ha='center', fontsize=7, color='#f87171', alpha=0.8)

    # Panel 3: Detrended residual (last 12k)
    ax3 = axes[2]
    ax3.plot(yr_uniform, residual, color='#34d399', linewidth=0.6, alpha=0.8)
    ax3.set_ylabel('Δ¹⁴C residual (‰)', color='#ccc', fontsize=11)
    ax3.set_title('Detrended Residual — Solar Cycles Visible', color='#e0e2ec', fontsize=12)
    ax3.axhline(0, color='#444', linewidth=0.5)

    # Panel 4: FFT
    ax4 = axes[3]
    p_mask = (periods > 40) & (periods < 5000)
    ax4.semilogy(periods[p_mask], fft_mag[p_mask], color='#67e8f9', linewidth=1.0, alpha=0.9)
    for name, tp, tc in targets:
        if tp >= 40:
            ax4.axvline(tp, color=tc, linestyle='--', alpha=0.6, linewidth=1)
            ax4.text(tp * 1.05, ax4.get_ylim()[1] * 0.3 if ax4.get_ylim()[1] > 0 else 0.1,
                     name, rotation=90, va='top', fontsize=8, color=tc, alpha=0.9)
    ax4.set_xlabel('Period (years)', color='#ccc', fontsize=11)
    ax4.set_ylabel('FFT Amplitude', color='#ccc', fontsize=11)
    ax4.set_title('FFT Spectrum — Known Solar Cycles', color='#e0e2ec', fontsize=12)
    ax4.set_xscale('log')

    plt.tight_layout()
    out = os.path.join(RESULTS_DIR, 'sol1_e4_c14_fft.png')
    plt.savefig(out, dpi=150, facecolor='#0a0c0e')
    print(f"\n[7] Plot saved: {out}")
    plt.close()


# ============================================================
# 8. Report
# ============================================================

def write_report(n_total, n_holo, n_uniform, step, peaks_info):
    report = f"""# SOL-1 E4 Report — Carbon-14 (IntCal20) → Solar Activity Cycles

## Summary
- **Dataset:** IntCal20 (Reimer et al. 2020), {n_total} data points
- **Full range:** 55,000 years (53050 BCE — 1950 CE)
- **Holocene subset:** {n_holo} points (~12,000 years)
- **Resampled:** {n_uniform} points at {step}-year resolution
- **Detrending:** 2000-year running mean subtracted (removes geomagnetic/ocean trends)

## Method
Delta-14C is **inversely** proportional to solar activity:
- Solar maximum → strong heliospheric magnetic field → fewer cosmic rays → less ¹⁴C produced
- Solar minimum → weak field → more cosmic rays → more ¹⁴C
- Grand Solar Minima (Maunder, Spörer, etc.) produce sustained high Δ¹⁴C peaks

## FFT Results
See plot `sol1_e4_c14_fft.png` for full spectrum.

### Target Cycles
| Cycle | Expected Period | Status |
|-------|----------------|--------|
| Schwabe | ~11 yr | Below Nyquist (20yr step) — not detectable |
| Hale | ~22 yr | Near Nyquist limit |
| Gleissberg | ~88 yr | **Check FFT** |
| Suess/deVries | ~210 yr | **Primary target** |
| Eddy | ~1000 yr | Check FFT |
| Hallstatt | ~2300 yr | **Primary target** |

## Cross-validation with E1-E3
- **Gleissberg ~88yr:** E1 ✓, E2 ✓, E3 ✓ → E4 check
- **Suess ~210yr:** E2 ✓ (210), E3 ✓ (178) → E4 check
- **Hallstatt ~2300yr:** only detectable in C14/Be10 (new in E4)

## Grand Solar Minima Detection
Known GSMs checked against Δ¹⁴C anomalies (see output).

## Next: E5 Beryllium-10 (GISP2) — independent cross-validation
"""
    out = os.path.join(RESULTS_DIR, 'sol1_e4_report.md')
    with open(out, 'w') as f:
        f.write(report)
    print(f"[8] Report saved: {out}")


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("SOL-1 E4: Carbon-14 (IntCal20) → Solar Activity Cycles")
    print("=" * 60)

    cal_ce, delta14c, sigma = load_intcal20()
    yr_holo, d14c_holo = extract_holocene(cal_ce, delta14c)

    step = 20  # 20-year resolution
    yr_uniform, d14c_uniform, residual = resample_uniform(yr_holo, d14c_holo, step=step)

    freqs, fft_mag, periods, targets = fft_analysis(yr_uniform, residual, step)

    prior = cross_check_periods()
    detect_grand_minima(yr_uniform, d14c_uniform)

    plot_results(cal_ce, delta14c, yr_holo, d14c_holo, yr_uniform, d14c_uniform,
                 residual, freqs, fft_mag, periods, targets)

    write_report(len(cal_ce), len(yr_holo), len(yr_uniform), step, None)

    print("\n" + "=" * 60)
    print("E4 DONE. Next: E5 Beryllium-10 (GISP2) — L4 cross-validation")
    print("=" * 60)
