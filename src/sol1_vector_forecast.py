#!/usr/bin/env python3
"""
SOL-1 VECTOR FORECAST — вероятностный прогноз по 7 векторам:
1. Солнечная активность (SOL-1 модель)
2. Глобальная температура (антропогенное + солнечное)
3. Сельское хозяйство (урожайность)
4. Энергетика (солнечная генерация, отопление)
5. Космические лучи и радиация
6. Геополитика / миграция
7. Технологическая адаптация

Горизонт: 2026—2250
Monte Carlo: 500 реализаций
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

# ═══════════════════════════════════════════
# Solar model (from SOL-1)
# ═══════════════════════════════════════════

CYCLES = [
    {'name': 'Schwabe',    'period': 11.0,   'sigma_p': 0.5,   'amp': 0.15, 'sigma_a': 0.03},
    {'name': 'Hale',       'period': 22.0,   'sigma_p': 1.0,   'amp': 0.10, 'sigma_a': 0.03},
    {'name': 'Gleissberg', 'period': 88.0,   'sigma_p': 6.0,   'amp': 0.25, 'sigma_a': 0.05},
    {'name': 'Suess',      'period': 207.0,  'sigma_p': 15.0,  'amp': 0.30, 'sigma_a': 0.06},
    {'name': 'Eddy',       'period': 1000.0, 'sigma_p': 80.0,  'amp': 0.20, 'sigma_a': 0.05},
    {'name': 'Hallstatt',  'period': 2300.0, 'sigma_p': 180.0, 'amp': 0.15, 'sigma_a': 0.04},
]

GSM_MIDS = np.array([1030, 1310, 1505, 1680, 1810])

def fit_base_phases():
    def cost(phases):
        total = 0
        for yr in GSM_MIDS:
            val = sum(c['amp'] * np.cos(2*np.pi*yr/c['period'] + phases[i]) for i, c in enumerate(CYCLES))
            total += val
        return total
    best = (np.inf, None)
    rng = np.random.RandomState(42)
    for _ in range(200):
        p0 = rng.uniform(0, 2*np.pi, len(CYCLES))
        res = minimize(cost, p0, method='Nelder-Mead', options={'maxiter': 3000})
        if res.fun < best[0]:
            best = (res.fun, res.x % (2*np.pi))
    return best[1]

def solar_activity(t, cycles, phases):
    return sum(c['amp'] * np.cos(2*np.pi*t/c['period'] + phases[i]) for i, c in enumerate(cycles))

# ═══════════════════════════════════════════
# Climate scenarios (IPCC AR6 based)
# ═══════════════════════════════════════════

CLIMATE_SCENARIOS = {
    'SSP1-2.6': {'name': 'Зелёный переход', 'rate_2030': 0.15, 'rate_2050': 0.08, 'rate_2100': 0.01, 'peak': 1.8, 'prob': 0.15},
    'SSP2-4.5': {'name': 'Средний путь',    'rate_2030': 0.20, 'rate_2050': 0.15, 'rate_2100': 0.10, 'peak': 2.7, 'prob': 0.45},
    'SSP3-7.0': {'name': 'Бездействие',     'rate_2030': 0.25, 'rate_2050': 0.22, 'rate_2100': 0.18, 'peak': 3.6, 'prob': 0.30},
    'SSP5-8.5': {'name': 'Ископаемый бум',  'rate_2030': 0.30, 'rate_2050': 0.28, 'rate_2100': 0.25, 'peak': 4.4, 'prob': 0.10},
}

def anthropogenic_warming(t, scenario):
    """Delta-T from preindustrial due to GHG, by year."""
    s = CLIMATE_SCENARIOS[scenario]
    result = np.zeros_like(t, dtype=float)
    for i, yr in enumerate(t):
        if yr <= 2026:
            result[i] = 1.2
        elif yr <= 2050:
            frac = (yr - 2026) / (2050 - 2026)
            rate = s['rate_2030'] + frac * (s['rate_2050'] - s['rate_2030'])
            result[i] = 1.2 + rate * (yr - 2026) / 10
        elif yr <= 2100:
            base = 1.2 + s['rate_2030'] * 2.4 / 10 + s['rate_2050'] * (2050-2026-24) / 10
            base = min(base, s['peak'] * 0.7)
            frac = (yr - 2050) / 50
            result[i] = base + frac * (s['peak'] - base)
        else:
            # Post-2100: plateau or slow rise
            result[i] = s['peak'] + (yr - 2100) * 0.002
        result[i] = min(result[i], s['peak'] * 1.1)
    return result

def solar_delta_t(solar_index):
    """Convert solar activity index to temperature forcing (°C)."""
    # Maunder (index -0.971) → -0.8°C. Linear scaling.
    return solar_index * 0.8 / 0.971

# ═══════════════════════════════════════════
# Vector models
# ═══════════════════════════════════════════

def agriculture_index(delta_t_total, solar_idx):
    """Crop yield index: 100 = normal. Affected by temperature extremes and UV."""
    # Optimal: +0.5 to +1.5°C from preindustrial
    # Too cold (<-0.5 from current): bad
    # Too hot (>+3°C from preindustrial): bad
    result = 100 - np.abs(delta_t_total - 1.0) * 15
    # Solar minimum → less UV → slight negative for some crops
    result += solar_idx * 5
    return np.clip(result, 50, 115)

def energy_impact(delta_t_total, solar_idx):
    """Energy demand index: 100 = current. Cold → more heating. Solar min → less PV."""
    heating = np.where(delta_t_total < 1.2, (1.2 - delta_t_total) * 8, 0)
    cooling = np.where(delta_t_total > 2.0, (delta_t_total - 2.0) * 5, 0)
    pv_loss = np.where(solar_idx < -0.3, np.abs(solar_idx) * 3, 0)  # TSI drop
    return 100 + heating + cooling + pv_loss

def cosmic_ray_index(solar_idx):
    """Cosmic ray flux index: 100 = current. High when solar activity low."""
    # GCR inversely proportional to solar activity
    return 100 - solar_idx * 30  # solar min → ~130, solar max → ~70

def geopolitical_stress(delta_t_total, agri_idx):
    """Geopolitical stress index: 0-100. High when food scarce or migration."""
    # Temperature extremes → migration → conflict
    temp_stress = np.where(delta_t_total > 2.5, (delta_t_total - 2.5) * 20, 0)
    food_stress = np.where(agri_idx < 85, (85 - agri_idx) * 2, 0)
    return np.clip(temp_stress + food_stress, 0, 100)

def tech_adaptation(t):
    """Technology adaptation capacity: 0-100. Grows with time (logistic)."""
    # S-curve: slow start, rapid 2040-2080, plateau
    return 100 / (1 + np.exp(-0.08 * (t - 2060)))

# ═══════════════════════════════════════════
# Monte Carlo
# ═══════════════════════════════════════════

def run_monte_carlo(n_runs=500):
    print("=" * 65)
    print("  VECTOR FORECAST — 7 векторов × 500 MC × 4 климат-сценария")
    print("=" * 65)

    base_phases = fit_base_phases()
    rng = np.random.RandomState(777)
    t = np.arange(2026, 2226, 1).astype(float)
    N = len(t)

    # Storage per climate scenario
    results = {}
    for scenario in CLIMATE_SCENARIOS:
        solar_all = np.zeros((n_runs, N))
        temp_all = np.zeros((n_runs, N))
        agri_all = np.zeros((n_runs, N))
        energy_all = np.zeros((n_runs, N))
        gcr_all = np.zeros((n_runs, N))
        geo_all = np.zeros((n_runs, N))
        tech_all = np.zeros((n_runs, N))

        for run in range(n_runs):
            # Perturb solar cycles
            perturbed = []
            for c in CYCLES:
                p = max(5, rng.normal(c['period'], c['sigma_p']))
                a = max(0.01, rng.normal(c['amp'], c['sigma_a']))
                perturbed.append({**c, 'period': p, 'amp': a})
            phases = base_phases + rng.normal(0, 0.15, len(base_phases))

            # Solar activity
            sol = np.array([solar_activity(ti, perturbed, phases) for ti in t])
            solar_all[run] = sol

            # Temperature: anthropogenic + solar
            anthro = anthropogenic_warming(t, scenario)
            solar_t = solar_delta_t(sol)
            # Add natural variability ±0.1°C
            noise = rng.normal(0, 0.1, N)
            total_t = anthro + solar_t + noise
            temp_all[run] = total_t

            # Derived vectors
            agri = agriculture_index(total_t, sol)
            agri_all[run] = agri + rng.normal(0, 3, N)  # noise

            energy_all[run] = energy_impact(total_t, sol) + rng.normal(0, 2, N)
            gcr_all[run] = cosmic_ray_index(sol) + rng.normal(0, 5, N)
            geo_all[run] = geopolitical_stress(total_t, agri) + rng.normal(0, 3, N)
            tech_all[run] = tech_adaptation(t) + rng.normal(0, 3, N)

        results[scenario] = {
            'solar': solar_all, 'temp': temp_all, 'agri': agri_all,
            'energy': energy_all, 'gcr': gcr_all, 'geo': geo_all, 'tech': tech_all,
        }

    return t, results


# ═══════════════════════════════════════════
# Analysis & Output
# ═══════════════════════════════════════════

def analyze_and_print(t, results):
    print(f"\n{'═'*65}")

    # Key decades
    decades = [2030, 2050, 2080, 2100, 2130, 2150, 2200]
    main_scenario = 'SSP2-4.5'
    data = results[main_scenario]

    print(f"  БАЗОВЫЙ СЦЕНАРИЙ: SSP2-4.5 (Средний путь, P=45%)")
    print(f"{'─'*65}")
    print(f"  {'Год':>6} │ {'ΔT (°C)':>10} │ {'Solar':>8} │ {'Урожай':>8} │ {'Энергия':>9} │ {'GCR':>6} │ {'Стресс':>8} │ {'Технол':>8}")
    print(f"  {'':>6} │ {'med(68%)':>10} │ {'index':>8} │ {'index':>8} │ {'demand':>9} │ {'flux':>6} │ {'index':>8} │ {'adapt':>8}")
    print(f"  {'─'*6}─┼{'─'*10}──┼{'─'*8}──┼{'─'*8}──┼{'─'*9}──┼{'─'*6}──┼{'─'*8}──┼{'─'*8}─")

    for decade in decades:
        idx = decade - 2026
        if idx < 0 or idx >= len(t):
            continue

        def pctl(arr, i):
            p16, p50, p84 = np.percentile(arr[:, i], [16, 50, 84])
            return p50, p16, p84

        sol_m, sol_lo, sol_hi = pctl(data['solar'], idx)
        tmp_m, tmp_lo, tmp_hi = pctl(data['temp'], idx)
        agr_m, _, _ = pctl(data['agri'], idx)
        ene_m, _, _ = pctl(data['energy'], idx)
        gcr_m, _, _ = pctl(data['gcr'], idx)
        geo_m, _, _ = pctl(data['geo'], idx)
        tch_m, _, _ = pctl(data['tech'], idx)

        print(f"  {decade:>6} │ {tmp_m:+.1f}({tmp_lo:+.1f}…{tmp_hi:+.1f}) │ {sol_m:+.2f}   │ {agr_m:5.0f}    │ {ene_m:6.0f}    │ {gcr_m:5.0f} │ {geo_m:5.0f}    │ {tch_m:5.0f}   ")

    # Scenario comparison at 2100
    print(f"\n{'═'*65}")
    print(f"  СРАВНЕНИЕ СЦЕНАРИЕВ НА 2100 CE")
    print(f"{'─'*65}")
    idx_2100 = 2100 - 2026

    print(f"  {'Сценарий':<22} │ {'P':>4} │ {'ΔT':>8} │ {'Урожай':>8} │ {'Стресс':>8} │ {'Verdict'}")
    print(f"  {'─'*22}─┼{'─'*4}──┼{'─'*8}──┼{'─'*8}──┼{'─'*8}──┼{'─'*20}")

    for sc_name, sc_data in CLIMATE_SCENARIOS.items():
        d = results[sc_name]
        tmp = np.median(d['temp'][:, idx_2100])
        agr = np.median(d['agri'][:, idx_2100])
        geo = np.median(d['geo'][:, idx_2100])
        prob = sc_data['prob'] * 100

        if tmp < 2.0:
            verdict = '🟢 Управляемо'
        elif tmp < 3.0:
            verdict = '🟡 Сложно'
        elif tmp < 4.0:
            verdict = '🔴 Опасно'
        else:
            verdict = '⛔ Критично'

        print(f"  {sc_data['name']:<22} │ {prob:3.0f}% │ {tmp:+5.1f}°C │ {agr:6.0f}   │ {geo:6.0f}   │ {verdict}")

    # GSM impact window
    print(f"\n{'═'*65}")
    print(f"  ОКНО ВЛИЯНИЯ GSM (когда солнечный минимум заметен)")
    print(f"{'─'*65}")

    sol_med = np.median(data['solar'], axis=0)
    gsm_mask = sol_med < -0.25
    if gsm_mask.any():
        gsm_start = t[np.argmax(gsm_mask)]
        gsm_end = t[len(gsm_mask) - 1 - np.argmax(gsm_mask[::-1])]
        gsm_depth = sol_med[gsm_mask].min()
        gsm_peak_yr = t[np.argmin(sol_med)]

        print(f"  Начало ощутимого снижения:  ~{gsm_start:.0f} CE")
        print(f"  Пик минимума:               ~{gsm_peak_yr:.0f} CE")
        print(f"  Конец:                       ~{gsm_end:.0f} CE")
        print(f"  Длительность:                ~{gsm_end - gsm_start:.0f} лет")
        print(f"  Глубина (медиана):           {gsm_depth:+.3f}")
        print(f"  Температурный эффект:        {solar_delta_t(gsm_depth):+.2f}°C")

        # Net effect
        anthro_at_peak = np.median(data['temp'][:, int(gsm_peak_yr - 2026)])
        print(f"\n  Суммарная температура в {gsm_peak_yr:.0f}:")
        print(f"    Антропогенное:  +{anthropogenic_warming(np.array([gsm_peak_yr]), main_scenario)[0]:.1f}°C")
        print(f"    Солнечное:      {solar_delta_t(gsm_depth):+.2f}°C")
        print(f"    Итого (медиана): {anthro_at_peak:+.1f}°C от доиндустриального")
    else:
        print(f"  GSM не достигает порога в медианном сценарии")

    # Probability matrix
    print(f"\n{'═'*65}")
    print(f"  МАТРИЦА ВЕРОЯТНОСТЕЙ (ключевые события)")
    print(f"{'─'*65}")

    events = [
        ('GSM начинается до 2060', lambda: np.mean(np.min(data['solar'][:, :34], axis=1) < -0.35)),
        ('GSM начинается до 2100', lambda: np.mean(np.min(data['solar'][:, :74], axis=1) < -0.35)),
        ('GSM начинается до 2150', lambda: np.mean(np.min(data['solar'][:, :124], axis=1) < -0.35)),
        ('ΔT > +2°C к 2060 (SSP2)', lambda: np.mean(data['temp'][:, 34] > 2.0)),
        ('ΔT > +2°C к 2100 (SSP2)', lambda: np.mean(data['temp'][:, 74] > 2.0)),
        ('Урожайность < 85 к 2100', lambda: np.mean(data['agri'][:, 74] < 85)),
        ('GCR > 130 (рад. фон ↑30%)', lambda: np.mean(data['gcr'][:, 74] > 130)),
        ('Технол. адаптация > 80%', lambda: np.mean(data['tech'][:, 74] > 80)),
        ('GSM + потепление > +3°C одновременно', lambda: np.mean(
            (np.min(data['solar'], axis=1) < -0.4) &
            (np.max(data['temp'][:, 50:], axis=1) > 3.0))),
    ]

    for desc, calc in events:
        prob = calc() * 100
        bar = '█' * int(prob / 5) + '░' * (20 - int(prob / 5))
        color = '🔴' if prob > 70 else '🟡' if prob > 30 else '🟢'
        print(f"  {color} {prob:5.1f}% │ {bar} │ {desc}")

    return data, sol_med


# ═══════════════════════════════════════════
# Plot
# ═══════════════════════════════════════════

def plot_vectors(t, results):
    fig, axes = plt.subplots(7, 1, figsize=(20, 28), facecolor='#0a0c0e')

    vectors = [
        ('solar',  'Solar Activity Index',    '#67e8f9', 'Активность Солнца'),
        ('temp',   'ΔT from preindustrial (°C)', '#f87171', 'Температура Земли'),
        ('agri',   'Crop Yield Index',        '#34d399', 'Урожайность'),
        ('energy', 'Energy Demand Index',     '#fbbf24', 'Спрос на энергию'),
        ('gcr',    'Cosmic Ray Flux Index',   '#a78bfa', 'Космические лучи'),
        ('geo',    'Geopolitical Stress',     '#f87171', 'Геополит. стресс'),
        ('tech',   'Technology Adaptation %', '#60a5fa', 'Технол. адаптация'),
    ]

    main = results['SSP2-4.5']

    for i, (key, ylabel, color, title_ru) in enumerate(vectors):
        ax = axes[i]
        ax.set_facecolor('#12141e')
        ax.tick_params(colors='#999', labelsize=8)
        for s in ax.spines.values():
            s.set_color('#333')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        data = main[key]
        p5 = np.percentile(data, 5, axis=0)
        p16 = np.percentile(data, 16, axis=0)
        p50 = np.percentile(data, 50, axis=0)
        p84 = np.percentile(data, 84, axis=0)
        p95 = np.percentile(data, 95, axis=0)

        ax.fill_between(t, p5, p95, alpha=0.08, color=color)
        ax.fill_between(t, p16, p84, alpha=0.20, color=color)
        ax.plot(t, p50, color=color, linewidth=1.5)

        # For temperature: overlay all scenarios
        if key == 'temp':
            for sc_name, sc_color in [('SSP1-2.6', '#34d399'), ('SSP3-7.0', '#fbbf24'), ('SSP5-8.5', '#f87171')]:
                sc_med = np.median(results[sc_name][key], axis=0)
                ax.plot(t, sc_med, color=sc_color, linewidth=0.8, alpha=0.6, linestyle='--')
            ax.axhline(1.5, color='#fbbf24', linewidth=0.5, linestyle=':', alpha=0.4)
            ax.axhline(2.0, color='#f87171', linewidth=0.5, linestyle=':', alpha=0.4)
            ax.text(2028, 1.55, '1.5°C Paris', fontsize=7, color='#fbbf24', alpha=0.6)
            ax.text(2028, 2.05, '2.0°C limit', fontsize=7, color='#f87171', alpha=0.6)

        ax.set_ylabel(ylabel, color='#ccc', fontsize=9)
        ax.set_title(f'V{i+1}: {title_ru}', color='#e0e2ec', fontsize=11, fontweight='bold', loc='left')
        ax.axvline(2026, color='#444', linewidth=0.5, linestyle=':')

    plt.tight_layout(pad=1.5)
    out = os.path.join(RESULTS_DIR, 'sol1_vector_forecast.png')
    plt.savefig(out, dpi=150, facecolor='#0a0c0e')
    print(f"\n  Plot saved: {out}")
    plt.close()


# ═══════════════════════════════════════════
# Main
# ═══════════════════════════════════════════

if __name__ == '__main__':
    t, results = run_monte_carlo(n_runs=500)
    data, sol_med = analyze_and_print(t, results)
    plot_vectors(t, results)

    print(f"\n{'═'*65}")
    print(f"  VECTOR FORECAST COMPLETE")
    print(f"  7 vectors × 4 scenarios × 500 MC = 14000 trajectories")
    print(f"{'═'*65}")
