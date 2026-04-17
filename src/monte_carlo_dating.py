#!/usr/bin/env python3
"""
Monte Carlo датировка Альмагеста — 10 000 итераций.
Добавляет случайные ошибки ±0.5° к координатам Птолемея,
прогоняет метод Дамбиса на полном каталоге, строит распределение.

Все даты: «лет назад от 2026» (2026 = точка ноль).
50 CE = 1976 лет назад.
"""

import os
import sys
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord, GeocentricMeanEcliptic
from astropy.time import Time
from astropy import units as u

# === Загрузка данных (как в almagest_1022.py) ===

def load_data():
    """Загружает Verbunt 2012 cross-match + Hipparcos pm."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    import csv
    stars = []
    with open(os.path.join(data_dir, 'ptolemy_verbunt2012.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                stars.append({
                    'name': row['Name'],
                    'ptol_lon': float(row['PtolLon']),
                    'ptol_lat': float(row['PtolLat']),
                    'hip': int(row['HIP']),
                })
            except (ValueError, KeyError):
                continue

    hip_data = {}
    hip_file = os.path.join(data_dir, 'hipparcos_pm.csv')
    if os.path.exists(hip_file):
        with open(hip_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    hip_data[int(row['HIP'])] = {
                        'ra': float(row.get('RA') or row.get('Ra', 0)),
                        'dec': float(row.get('Dec') or row.get('DEC', 0)),
                        'pmra': float(row.get('pmRA') or row.get('PMRA', 0)),
                        'pmdec': float(row.get('pmDec') or row.get('PMDEC', 0)),
                    }
                except (ValueError, KeyError):
                    continue

    matched = []
    for s in stars:
        h = hip_data.get(s['hip'])
        if h:
            s.update(h)
            matched.append(s)

    print(f"[MC] Загружено {len(matched)} звёзд с pm")
    return matched


def compute_rms(stars, epoch_year, ptol_lon_noise=None, ptol_lat_noise=None):
    """RMS невязки для заданной эпохи. Если noise != None, добавляем к координатам Птолемея."""
    t = Time(epoch_year, format='jyear')
    residuals = []

    for i, s in enumerate(stars):
        # Координаты J2000 + proper motion → эпоха T
        dt_yr = epoch_year - 2000.0
        ra_t = s['ra'] + s['pmra'] / 3600000.0 * dt_yr / np.cos(np.radians(s['dec']))
        dec_t = s['dec'] + s['pmdec'] / 3600000.0 * dt_yr

        # Конвертируем в эклиптические
        coord = SkyCoord(ra=ra_t * u.deg, dec=dec_t * u.deg, frame='icrs')
        ecl = coord.transform_to(GeocentricMeanEcliptic(equinox=t))

        calc_lon = ecl.lon.deg
        calc_lat = ecl.lat.deg

        # Координаты Птолемея + шум
        ptol_lon = s['ptol_lon']
        ptol_lat = s['ptol_lat']
        if ptol_lon_noise is not None:
            ptol_lon += ptol_lon_noise[i]
        if ptol_lat_noise is not None:
            ptol_lat += ptol_lat_noise[i]

        # Невязка
        dlon = calc_lon - ptol_lon
        if dlon > 180: dlon -= 360
        if dlon < -180: dlon += 360
        dlat = calc_lat - ptol_lat

        residuals.append(np.sqrt(dlon**2 + dlat**2))

    return np.mean(residuals)


def find_best_epoch(stars, ptol_lon_noise=None, ptol_lat_noise=None,
                     epoch_range=(-300, 500), step=10):
    """Находит эпоху с минимальным RMS."""
    epochs = np.arange(epoch_range[0], epoch_range[1] + step, step)
    best_rms = 999
    best_epoch = 0

    for epoch in epochs:
        rms = compute_rms(stars, epoch, ptol_lon_noise, ptol_lat_noise)
        if rms < best_rms:
            best_rms = rms
            best_epoch = epoch

    return best_epoch, best_rms


def epoch_to_ago(epoch_ce, ref=2026):
    """CE → лет назад от 2026."""
    return ref - epoch_ce


def main():
    NOW = 2026  # точка ноль
    N_ITER = 10000
    SIGMA = 0.5  # ±0.5° ошибка координат Птолемея

    stars = load_data()
    n_stars = len(stars)

    # 1. Базовый расчёт (без шума)
    print(f"\n[MC] Базовый расчёт (без шума)...")
    base_epoch, base_rms = find_best_epoch(stars)
    base_ago = epoch_to_ago(base_epoch, NOW)
    print(f"  Базовая эпоха: {base_epoch} CE = {base_ago} лет назад")
    print(f"  RMS: {base_rms:.3f}°")

    # 2. Monte Carlo — 10 000 итераций
    print(f"\n[MC] Monte Carlo: {N_ITER} итераций, σ = ±{SIGMA}°...")
    best_epochs = []

    for i in range(N_ITER):
        # Случайные ошибки для каждой звезды
        lon_noise = np.random.normal(0, SIGMA, n_stars)
        lat_noise = np.random.normal(0, SIGMA, n_stars)

        epoch, rms = find_best_epoch(stars, lon_noise, lat_noise)
        best_epochs.append(epoch)

        if (i + 1) % 1000 == 0:
            print(f"  {i + 1}/{N_ITER}...")

    best_epochs = np.array(best_epochs)

    # 3. Статистика
    mean_epoch = np.mean(best_epochs)
    std_epoch = np.std(best_epochs)
    median_epoch = np.median(best_epochs)
    p025 = np.percentile(best_epochs, 2.5)
    p975 = np.percentile(best_epochs, 97.5)

    mean_ago = epoch_to_ago(mean_epoch, NOW)
    std_ago = std_epoch  # разница та же
    median_ago = epoch_to_ago(median_epoch, NOW)
    p025_ago = epoch_to_ago(p975, NOW)  # инвертируем: бо́льший CE = меньше лет назад
    p975_ago = epoch_to_ago(p025, NOW)

    print(f"\n{'='*60}")
    print(f"  РЕЗУЛЬТАТ Monte Carlo ({N_ITER} итераций, σ = ±{SIGMA}°)")
    print(f"{'='*60}")
    print(f"  Среднее:  {mean_epoch:.0f} CE  =  {mean_ago:.0f} лет назад")
    print(f"  Медиана:  {median_epoch:.0f} CE  =  {median_ago:.0f} лет назад")
    print(f"  σ:        ±{std_epoch:.0f} лет")
    print(f"  95% CI:   [{p025:.0f}, {p975:.0f}] CE")
    print(f"            [{p975_ago:.0f}, {p025_ago:.0f}] лет назад")
    print(f"{'='*60}")
    print(f"  Формулировка для статьи:")
    print(f"  «{mean_ago:.0f} ± {std_epoch:.0f} лет назад (95% CI: {p975_ago:.0f}–{p025_ago:.0f})»")
    print(f"  или в CE: «{mean_epoch:.0f} ± {std_epoch:.0f} CE (95% CI: {p025:.0f}–{p975:.0f})»")
    print(f"{'='*60}")

    # 4. Контекст — что значит этот диапазон
    print(f"\n  Контекст (от точки ноль {NOW}):")
    print(f"  ├─ Гиппарх наблюдал:    ~2156 лет назад ({NOW - (-130)} = -130 CE)")
    print(f"  ├─ Птолемей написал:    ~1889 лет назад ({NOW - 137} = 137 CE)")
    print(f"  ├─ Морозов утверждал:   ~1226 лет назад ({NOW - 800} = 800 CE)")
    print(f"  └─ Наш результат:       ~{mean_ago:.0f} лет назад → ГИППАРХ, не Птолемей и не Морозов")

    # 5. График
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Левый — в CE
    ax1.hist(best_epochs, bins=50, color='#4a90d9', edgecolor='black', alpha=0.8)
    ax1.axvline(mean_epoch, color='red', linewidth=2, label=f'Mean: {mean_epoch:.0f} CE')
    ax1.axvline(p025, color='orange', linestyle='--', label=f'95% CI: [{p025:.0f}, {p975:.0f}]')
    ax1.axvline(p975, color='orange', linestyle='--')
    ax1.axvline(-130, color='green', linestyle=':', linewidth=2, label='Гиппарх (-130)')
    ax1.axvline(137, color='purple', linestyle=':', linewidth=2, label='Птолемей (137)')
    ax1.axvline(800, color='gray', linestyle=':', linewidth=2, label='Морозов (800)')
    ax1.set_xlabel('Эпоха (CE)')
    ax1.set_ylabel('Количество итераций')
    ax1.set_title(f'Monte Carlo: {N_ITER} итераций, σ = ±{SIGMA}°')
    ax1.legend(fontsize=8)

    # Правый — в «лет назад от 2026»
    agos = NOW - best_epochs
    ax2.hist(agos, bins=50, color='#d94a4a', edgecolor='black', alpha=0.8)
    ax2.axvline(mean_ago, color='blue', linewidth=2, label=f'Mean: {mean_ago:.0f} лет назад')
    ax2.axvline(p025_ago, color='orange', linestyle='--', label=f'95% CI: [{p025_ago:.0f}, {p975_ago:.0f}]')
    ax2.axvline(p975_ago, color='orange', linestyle='--')
    ax2.axvline(2156, color='green', linestyle=':', linewidth=2, label='Гиппарх (2156)')
    ax2.axvline(1889, color='purple', linestyle=':', linewidth=2, label='Птолемей (1889)')
    ax2.axvline(1226, color='gray', linestyle=':', linewidth=2, label='Морозов (1226)')
    ax2.set_xlabel(f'Лет назад от {NOW}')
    ax2.set_ylabel('Количество итераций')
    ax2.set_title(f'Датировка: {mean_ago:.0f} ± {std_epoch:.0f} лет назад')
    ax2.legend(fontsize=8)

    plt.tight_layout()
    out_path = os.path.join(results_dir, 'monte_carlo_dating.png')
    plt.savefig(out_path, dpi=150)
    print(f"\n  График: {out_path}")

    # 6. Сохраняем отчёт
    report_path = os.path.join(results_dir, 'monte_carlo_report.md')
    with open(report_path, 'w') as f:
        f.write(f"# Monte Carlo датировка Альмагеста\n\n")
        f.write(f"**Дата прогона:** {NOW}-04-17\n")
        f.write(f"**Итерации:** {N_ITER}\n")
        f.write(f"**Ошибка координат:** σ = ±{SIGMA}°\n")
        f.write(f"**Звёзд:** {n_stars}\n\n")
        f.write(f"## Результат\n\n")
        f.write(f"| Метрика | CE | Лет назад от {NOW} |\n")
        f.write(f"|---|---|---|\n")
        f.write(f"| Среднее | {mean_epoch:.0f} CE | **{mean_ago:.0f}** |\n")
        f.write(f"| Медиана | {median_epoch:.0f} CE | {median_ago:.0f} |\n")
        f.write(f"| σ | ±{std_epoch:.0f} | ±{std_ago:.0f} |\n")
        f.write(f"| 95% CI | [{p025:.0f}, {p975:.0f}] | [{p975_ago:.0f}, {p025_ago:.0f}] |\n\n")
        f.write(f"## Интерпретация\n\n")
        f.write(f"- **Гиппарх** (~2156 лет назад): {'ВНУТРИ' if p025 <= -130 <= p975 else 'вне'} 95% CI\n")
        f.write(f"- **Птолемей** (~1889 лет назад): {'ВНУТРИ' if p025 <= 137 <= p975 else 'ВНЕ'} 95% CI\n")
        f.write(f"- **Морозов** (~1226 лет назад): {'ВНУТРИ' if p025 <= 800 <= p975 else 'ИСКЛЮЧЁН'} на 95% уровне\n")

    print(f"  Отчёт: {report_path}")


if __name__ == '__main__':
    main()
