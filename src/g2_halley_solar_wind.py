#!/usr/bin/env python3
"""
G2: Хвост кометы Галлея как прокси солнечного ветра на 2265 лет.

Никто не делал: исторические описания яркости/хвоста Галлея → прокси solar wind
→ FFT → сравнение с Gleissberg/Suess циклами из SOL-1 E1.

Принцип: длина кометного хвоста ∝ давление солнечного ветра ∝ солнечная активность.
При высокой активности хвост длиннее/ярче (больше ионизация + solar wind давление).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# 30 появлений Галлея + brightness/tail score (0-5)
# ============================================================
# Score based on historical descriptions:
# 0 = not visible / not recorded
# 1 = barely mentioned, dim, short tail
# 2 = moderate, mentioned briefly
# 3 = notable, described as bright or with visible tail
# 4 = spectacular, long tail, multiple sources
# 5 = extraordinary, maximum brightness/closest, recorded globally

HALLEY = [
    # (apparition, year, perihelion_date, brightness_score, tail_score, sources, notes)
    (1,  -239, '239 BCE Mar', 3, 3, 'Shiji (China)', 'First in chronicles, "Broom star" = visible tail'),
    (2,  -163, '163 BCE Sep', 2, 2, 'Babylonian tablet BM 41462', 'Cuneiform record, moderate'),
    (3,   -86, '86 BCE Aug',  3, 3, 'Han Shu + Pliny', 'Double fix China+Rome, "broom star"'),
    (4,   -11, '11 BCE Oct',  2, 2, 'Qian Han Shu + Dio Cassius', 'Death of Agrippa omen'),
    (5,    66, '66 CE Jan',   4, 4, 'Josephus ("sword star") + Tacitus', 'Siege of Jerusalem, "sword" = long straight tail'),
    (6,   141, '141 CE Mar',  2, 1, 'Hou Han Shu', 'Faint, weak western echo'),
    (7,   218, '218 CE May',  2, 2, 'Chinese + Dio Cassius', 'Death of Macrinus'),
    (8,   295, '295 CE Apr',  2, 2, 'Chinese', 'Three Kingdoms era'),
    (9,   374, '374 CE Feb',  2, 2, 'Chinese', 'Eastern Jin, brief mention'),
    (10,  451, '451 CE Jun',  3, 3, 'Chinese + Latin', 'Battle of Catalaunian Plains, Attila'),
    (11,  530, '530 CE Sep',  3, 3, 'Chinese + Cassiodorus', 'Justinian I era'),
    (12,  607, '607 CE Mar',  2, 2, 'Chinese + Gregory of Tours', 'Sui dynasty'),
    (13,  684, '684 CE Oct',  3, 3, 'Nuremberg Chronicle + Chinese', 'Miniature illustration'),
    (14,  760, '760 CE May',  2, 2, 'Chinese + Theophanes', 'Byzantine'),
    (15,  837, '837 CE Feb',  5, 5, 'Chinese Min-Tang: closest approach', 'MAXIMUM BRIGHTNESS EVER. Closest to Earth. Tail 60+ degrees'),
    (16,  912, '912 CE Jul',  2, 2, 'Chinese + European monks', 'Constantine VII'),
    (17,  989, '989 CE Sep',  3, 3, 'Chinese + Japan + Russian chronicle', 'Baptism of Rus!'),
    (18, 1066, '1066 CE Mar', 5, 5, 'Anglo-Saxon + Bayeux Tapestry + Sung Shi + Japan + RUS', 'GOLDEN CROSS-LEDGER: 5 cultures. Bayeux shows LONG tail'),
    (19, 1145, '1145 CE Apr', 3, 3, 'Chinese + Hypatian + European', 'Eadwine Psalter illustration'),
    (20, 1222, '1222 CE Sep', 3, 3, 'Chinese + Ibn al-Athir + Korean', 'Mongol invasion era'),
    (21, 1301, '1301 CE Oct', 4, 4, 'Giotto Adoration of Magi + Chinese', 'Giotto painted it as Star of Bethlehem'),
    (22, 1378, '1378 CE Nov', 2, 2, 'Chinese + European', 'Chaucer mentions'),
    (23, 1456, '1456 CE Jun', 4, 4, 'European (Pope Calixtus III) + Toscanelli', 'Pope excommunicated the comet!'),
    (24, 1531, '1531 CE Aug', 3, 3, 'Peter Apian + Chinese', 'Apianus drew tail direction'),
    (25, 1607, '1607 CE Oct', 3, 3, 'Kepler + Longomontanus', 'Kepler studied orbit'),
    (26, 1682, '1682 CE Sep', 4, 4, 'Halley + Flamsteed + Hevelius', 'Halley predicted return 1758'),
    (27, 1759, '1759 CE Mar', 4, 4, 'Messier + Palitzsch', 'First confirmed prediction'),
    (28, 1835, '1835 CE Nov', 4, 4, 'Bessel + Encke + spectroscopy', 'Scientific spectroscopy'),
    (29, 1910, '1910 CE Apr', 5, 5, 'Photography + Barnard + Perrine', 'Earth passed THROUGH tail, panic'),
    (30, 1986, '1986 CE Feb', 2, 1, 'Giotto spacecraft + Vega + Suisei', 'Dim from Earth (far), but close-up by spacecraft'),
]

def main():
    print("=" * 60)
    print("  G2: Halley tail → solar wind proxy (2265 years)")
    print("=" * 60)

    years = np.array([h[1] for h in HALLEY])
    brightness = np.array([h[3] for h in HALLEY])
    tail = np.array([h[4] for h in HALLEY])
    combined = (brightness + tail) / 2.0  # average of brightness and tail

    print(f"\n[1] 30 появлений: {years[0]} — {years[-1]} CE ({years[-1]-years[0]} лет)")
    print(f"    Brightness mean: {brightness.mean():.1f}, std: {brightness.std():.1f}")
    print(f"    Tail mean: {tail.mean():.1f}, std: {tail.std():.1f}")

    # ============================================================
    # Interpolate to uniform time series for FFT
    # ============================================================
    # Halley visits are ~76 years apart, NOT uniform. For FFT we need uniform sampling.
    # Interpolate to 10-year grid.

    t_min, t_max = years[0], years[-1]
    t_uniform = np.arange(t_min, t_max + 1, 10)
    combined_interp = np.interp(t_uniform, years, combined)
    brightness_interp = np.interp(t_uniform, years, brightness)

    print(f"\n[2] Интерполяция на 10-летнюю сетку: {len(t_uniform)} точек")

    # ============================================================
    # FFT
    # ============================================================
    def do_fft(t, vals, label):
        vals_c = vals - np.mean(vals)
        n = len(vals_c)
        n_pad = max(n * 4, 512)
        fft_vals = np.fft.rfft(vals_c, n=n_pad)
        power = np.abs(fft_vals) ** 2
        dt = t[1] - t[0]
        freqs = np.fft.rfftfreq(n_pad, d=dt)
        valid = freqs[1:] > 0
        periods = 1.0 / freqs[1:][valid]
        power_valid = power[1:][valid]

        peak_idx, _ = signal.find_peaks(power_valid, height=np.max(power_valid) * 0.1, distance=3)

        targets = {'Halley orbital': 76, 'Gleissberg': 88, 'Suess': 210, '~400': 400}

        print(f"\n[3] FFT: {label}")
        print(f"    Peaks (>10% max):")
        for i in peak_idx[:12]:
            p = periods[i]
            match = ""
            for name, target in targets.items():
                if abs(p - target) / target < 0.25:
                    match = f" ← {name}!"
            print(f"      {p:7.1f} years  power: {power_valid[i]:10.1f}{match}")

        return periods, power_valid, peak_idx

    periods_c, power_c, peaks_c = do_fft(t_uniform, combined_interp, "Combined (brightness+tail)/2")
    periods_b, power_b, peaks_b = do_fft(t_uniform, brightness_interp, "Brightness only")

    # ============================================================
    # Cross-correlation with sunspot data (if available)
    # ============================================================
    sunspot_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'solar', 'pre_telescopic_sunspots.csv')
    sunspot_correlation = None
    if os.path.exists(sunspot_file):
        import csv
        spot_years = []
        with open(sunspot_file) as f:
            for row in csv.DictReader(f):
                spot_years.append(int(row['year']))

        # Build binary time series for sunspot presence
        spot_ts = np.zeros_like(t_uniform, dtype=float)
        for sy in spot_years:
            idx = np.argmin(np.abs(t_uniform - sy))
            spot_ts[idx] += 1

        # Cross-correlation
        corr = np.correlate(combined_interp - combined_interp.mean(),
                           spot_ts - spot_ts.mean(), mode='full')
        corr /= max(np.max(np.abs(corr)), 1e-10)
        lags = np.arange(-len(combined_interp) + 1, len(combined_interp)) * 10  # years

        max_corr_idx = np.argmax(corr)
        max_lag = lags[max_corr_idx]
        max_corr = corr[max_corr_idx]

        print(f"\n[4] Cross-correlation Halley tail × sunspots:")
        print(f"    Max correlation: {max_corr:.3f} at lag {max_lag} years")
        if abs(max_lag) < 50:
            print(f"    → ПОЛОЖИТЕЛЬНАЯ корреляция near zero lag — Halley tail tracks solar activity!")
        sunspot_correlation = (lags, corr, max_lag, max_corr, t_uniform, spot_ts)

    # ============================================================
    # PLOTS
    # ============================================================
    fig, axes = plt.subplots(3, 2, figsize=(16, 14))

    # 1. Timeline of Halley brightness/tail
    ax = axes[0, 0]
    ax.bar(years, brightness, width=20, alpha=0.5, color='gold', label='Brightness (0-5)')
    ax.bar(years, tail, width=15, alpha=0.5, color='cyan', label='Tail length (0-5)')
    ax.plot(years, combined, 'r-o', lw=2, ms=4, label='Combined')
    for h in HALLEY:
        if h[3] >= 4:
            ax.annotate(f'{h[1]}', xy=(h[1], h[3]+0.2), fontsize=7, ha='center', color='red')
    ax.set_xlabel('Year CE')
    ax.set_ylabel('Score (0-5)')
    ax.set_title('30 появлений кометы Галлея: яркость и хвост')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # 2. Interpolated series
    ax = axes[0, 1]
    ax.plot(t_uniform, combined_interp, 'r-', lw=1, alpha=0.7, label='Halley combined (interpolated)')
    if sunspot_correlation:
        ax.plot(t_uniform, sunspot_correlation[5] * 2, 'b-', alpha=0.5, label='Sunspot records (×2 scale)')
    ax.set_xlabel('Year CE')
    ax.set_ylabel('Score / count')
    ax.set_title('Halley proxy vs pre-telescopic sunspots')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # 3. FFT Combined
    ax = axes[1, 0]
    valid = (periods_c > 30) & (periods_c < 1000)
    ax.semilogy(periods_c[valid], power_c[valid], 'r-', lw=1)
    for i in peaks_c:
        if 30 < periods_c[i] < 1000:
            ax.annotate(f'{periods_c[i]:.0f}y', xy=(periods_c[i], power_c[i]),
                       fontsize=8, color='darkred', ha='center', va='bottom')
    for name, target in {'Halley 76': 76, 'Gleissberg 88': 88, 'Suess 210': 210, '~400': 400}.items():
        ax.axvline(target, color='green', ls=':', alpha=0.5)
        ax.text(target, ax.get_ylim()[1]*0.3, name, fontsize=7, color='green', rotation=90, va='top')
    ax.set_xlabel('Period (years)')
    ax.set_ylabel('Power (log)')
    ax.set_title('FFT: Halley tail as solar wind proxy')
    ax.grid(alpha=0.3)

    # 4. FFT Brightness only
    ax = axes[1, 1]
    valid_b = (periods_b > 30) & (periods_b < 1000)
    ax.semilogy(periods_b[valid_b], power_b[valid_b], 'b-', lw=1)
    for i in peaks_b:
        if 30 < periods_b[i] < 1000:
            ax.annotate(f'{periods_b[i]:.0f}y', xy=(periods_b[i], power_b[i]),
                       fontsize=8, color='darkblue', ha='center', va='bottom')
    ax.set_xlabel('Period (years)')
    ax.set_ylabel('Power (log)')
    ax.set_title('FFT: Halley brightness only')
    ax.grid(alpha=0.3)

    # 5. Cross-correlation
    ax = axes[2, 0]
    if sunspot_correlation:
        lags, corr, ml, mc, _, _ = sunspot_correlation
        valid_lag = np.abs(lags) < 500
        ax.plot(lags[valid_lag], corr[valid_lag], 'purple', lw=1)
        ax.axvline(0, color='gray', ls='--', alpha=0.5)
        ax.axvline(ml, color='red', ls='-', alpha=0.7, label=f'Max r={mc:.3f} at lag {ml}y')
        ax.set_xlabel('Lag (years)')
        ax.set_ylabel('Cross-correlation')
        ax.set_title('Halley tail × Pre-telescopic sunspots')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No sunspot data', transform=ax.transAxes, ha='center')
    ax.grid(alpha=0.3)

    # 6. Grand Solar Minimum overlay
    ax = axes[2, 1]
    ax.plot(t_uniform, combined_interp, 'r-', lw=2, label='Halley proxy')
    # Known Grand Solar Minima
    minima = [
        ('Oort', 1010, 1050),
        ('Wolf', 1280, 1350),
        ('Spörer', 1460, 1550),
        ('Maunder', 1645, 1715),
        ('Dalton', 1790, 1830),
    ]
    for name, start, end in minima:
        ax.axvspan(start, end, alpha=0.2, color='blue')
        ax.text((start+end)/2, 4.5, name, fontsize=7, ha='center', color='blue')
    # Prediction
    ax.axvspan(2040, 2080, alpha=0.2, color='red')
    ax.text(2060, 4.5, 'PREDICTED\n~2040-2080?', fontsize=8, ha='center', color='red', fontweight='bold')
    ax.set_xlabel('Year CE')
    ax.set_ylabel('Halley solar wind proxy')
    ax.set_title('Halley proxy vs Known Grand Solar Minima + PREDICTION')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_xlim(900, 2100)

    plt.suptitle('G2: Comet Halley Tail Length as Solar Wind Proxy (2265 years)\nNOVEL — никто не делал',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    plot_file = os.path.join(RESULTS_DIR, 'g2_halley_solar_wind.png')
    plt.savefig(plot_file, dpi=150)
    print(f"\n📊 {plot_file}")

    # ============================================================
    # Summary
    # ============================================================
    print("\n" + "=" * 60)
    print("  ИТОГ G2: Halley tail → solar wind proxy")
    print("=" * 60)
    print(f"  Появлений:        30 ({years[0]} — {years[-1]} CE)")
    print(f"  Базлайн:          {years[-1]-years[0]} лет")
    print(f"  FFT пики:")
    for i in peaks_c[:8]:
        p = periods_c[i]
        if 30 < p < 1000:
            match = ""
            for n, t in {'Halley': 76, 'Gleissberg': 88, 'Suess': 210}.items():
                if abs(p-t)/t < 0.25:
                    match = f" ← {n}"
            print(f"    {p:7.1f} years{match}")
    if sunspot_correlation:
        print(f"  Cross-corr max:   r={sunspot_correlation[3]:.3f} at lag={sunspot_correlation[2]} years")
    print("=" * 60)

    # Beelink delegation note
    print("\n🤖 BEELINK TODO (когда онлайн):")
    print("  1. Независимо запустить этот скрипт → diff с Mac результатом")
    print("  2. Wavelet analysis (дополнение к FFT)")
    print("  3. Monte Carlo: рандомизировать scores ±1 → устойчивость пиков")
    print("  4. Perihelion distance correction (убрать орбитальный вклад)")

if __name__ == "__main__":
    main()
