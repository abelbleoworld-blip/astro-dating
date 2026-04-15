#!/usr/bin/env python3
"""
Датировка каталога Альмагеста Птолемея методом Морозова-Дамбиса.

Принцип: берём звёзды с большим собственным движением (pm). За 2000 лет
они сдвинулись заметно. Ищем эпоху T, при которой современные координаты,
проэволюционированные к T, максимально совпадают с координатами Альмагеста.

Ссылки:
  - G.J. Toomer "Ptolemy's Almagest" (1984) — стандартный перевод.
  - A.K. Dambis, Yu.N. Efremov (1999) "Dating Ptolemy's star catalogue",
    Journal for the History of Astronomy 31:115-134.
  - N.A. Morozov (1924-1932) "Христос" том 4.
  - Hipparcos main catalog (ESA 1997) — современные pm.

Дата каталога из предисловия Альмагеста: +137 CE.
Результат Дамбиса: -60..+60 (= эпоха Гиппарха).
Результат Морозова: +700..+900 (только прецессия, без pm).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, FK5, GeocentricMeanEcliptic
from astropy.time import Time
from astropy import units as u


# =============================================================================
# ДАТАСЕТ
# =============================================================================
#
# Координаты Альмагеста: эклиптические (λ, β) на эпоху каталога.
# Источник: Toomer 1984, Star Catalogue (Appendix A), координаты даны
# относительно знаков зодиака от 0° до 30°. Мы конвертируем в абсолютные
# долготы (0° = 0° Aries, +30 = 30° Aries = 0° Taurus, ...).
#
# Современные координаты: ICRS J2000 из Hipparcos (ESA 1997).
# Proper motions: ra_cos(δ) и dec в mas/yr.
#
# Выбраны 15 самых быстрых и надёжно отождествлённых звёзд Альмагеста.

ZODIAC_OFFSET = {
    'Ari': 0, 'Tau': 30, 'Gem': 60, 'Cnc': 90, 'Leo': 120, 'Vir': 150,
    'Lib': 180, 'Sco': 210, 'Sgr': 240, 'Cap': 270, 'Aqr': 300, 'Psc': 330,
}

def ptol_lon(zodiac_sign, deg, arcmin=0):
    return ZODIAC_OFFSET[zodiac_sign] + deg + arcmin / 60.0


# Формат: (имя, Альмагест_λ_deg, Альмагест_β_deg, ra_deg J2000, dec_deg J2000, pmRA*cos(δ) mas/yr, pmDec mas/yr)
# Источник Almagest: Toomer 1984. Источник modern: Hipparcos.
STARS = [
    # Очень быстрые (>500 mas/yr) — ключевые для Дамбиса
    ("Arcturus α Boo",
     ptol_lon('Vir', 27, 0),   31.5,   213.91531,  19.18241,  -1093.45, -1999.40),
    ("Sirius α CMa",
     ptol_lon('Gem', 17, 40), -39.17,  101.28716, -16.71612,   -546.05, -1223.14),
    ("Procyon α CMi",
     ptol_lon('Gem', 22, 30), -14.00,  114.82550,   5.22500,   -714.59, -1036.80),
    ("61 Cygni (Piazzi)",  # Нет в Альмагесте
     None, None, None, None, None, None),

    # Быстрые (100-500 mas/yr)
    ("Aldebaran α Tau",
     ptol_lon('Tau', 12, 40),  -5.17,   68.98016,  16.50930,     63.45,  -188.94),
    ("Pollux β Gem",
     ptol_lon('Gem',  3, 40),   6.17,  116.32896,  28.02620,   -625.69,  -45.95),
    ("Regulus α Leo",
     ptol_lon('Leo',  2, 30),   0.17,  152.09296,  11.96720,   -249.40,    4.91),
    ("Altair α Aql",
     ptol_lon('Cap',  3, 50),  29.17,  297.69582,   8.86832,    536.82,  385.54),
    ("Capella α Aur",
     ptol_lon('Gem', 10,  0),  22.5,    79.17232,  45.99800,     75.52, -427.11),
    ("Vega α Lyr",
     ptol_lon('Sgr',  7, 10),  62.0,   279.23473,  38.78368,    200.94,  286.23),
    ("Spica α Vir",
     ptol_lon('Lib',  6, 40),  -2.0,   201.29824, -11.16132,    -42.50,  -31.73),
    ("Antares α Sco",
     ptol_lon('Sco',  5, 40),  -4.0,   247.35191, -26.43200,    -10.16,  -23.21),
    ("Fomalhaut α PsA",
     ptol_lon('Aqr', 27, 0),  -23.17,  344.41269, -29.62224,    329.22, -164.22),
    ("Deneb α Cyg",
     ptol_lon('Cap',  4, 40),  60.0,   310.35798,  45.28034,      1.56,    1.55),
    ("Rigel β Ori",
     ptol_lon('Tau', 19, 30), -31.5,    78.63447,  -8.20164,      1.87,   -0.56),
    ("Betelgeuse α Ori",
     ptol_lon('Gem',  2,  0), -17.0,    88.79294,   7.40706,     27.54,   11.30),
]

# Фильтруем реальные
STARS = [s for s in STARS if s[1] is not None]
print(f"[*] Звёзд в датасете: {len(STARS)}")


# =============================================================================
# АЛГОРИТМ
# =============================================================================

def star_position_at_epoch(ra0, dec0, pm_ra_cos_dec, pm_dec, epoch_year):
    """
    Проецирует J2000 координаты звезды на эпоху epoch_year, учитывая pm.
    Возвращает эклиптические долготу λ и широту β в ЭТОЙ эпохе (с прецессией).

    Формула: α(T) = α(2000) + μα*(T-2000)/cos(δ)  (упрощ. для малых dt)
             δ(T) = δ(2000) + μδ*(T-2000)

    Затем преобразуем в эклиптику этой даты.
    """
    dt_yr = epoch_year - 2000.0  # годы
    # Сдвиг с proper motion
    ra_t = ra0 + (pm_ra_cos_dec / 3_600_000.0) * dt_yr / np.cos(np.deg2rad(dec0))
    dec_t = dec0 + (pm_dec / 3_600_000.0) * dt_yr

    # SkyCoord в ICRS (FK5 эквивалент для точности)
    c = SkyCoord(ra=ra_t * u.deg, dec=dec_t * u.deg, frame='icrs')
    # Преобразуем в эклиптику эпохи T (jyear — десятичный год, работает для -3000..+3000)
    ep = Time(float(epoch_year), format='jyear', scale='tt')
    ec = c.transform_to(GeocentricMeanEcliptic(equinox=ep))
    return ec.lon.wrap_at(360 * u.deg).deg, ec.lat.deg


def rms_for_epoch(stars, epoch_year):
    """RMS невязка между Альмагестом и пересчитанными координатами на эпоху."""
    residuals = []
    for name, alm_lon, alm_lat, ra, dec, pmra, pmdec in stars:
        lon_t, lat_t = star_position_at_epoch(ra, dec, pmra, pmdec, epoch_year)
        # разница долгот с учётом wrap
        d_lon = (alm_lon - lon_t + 180) % 360 - 180
        d_lat = alm_lat - lat_t
        residuals.append(d_lon**2 + d_lat**2)
    return np.sqrt(np.mean(residuals))


def find_best_epoch(stars, t_min=-300, t_max=500, step=10):
    """Перебором эпох ищем минимум RMS."""
    epochs = np.arange(t_min, t_max + step, step)
    rms_vals = np.array([rms_for_epoch(stars, t) for t in epochs])
    best_idx = np.argmin(rms_vals)
    return epochs, rms_vals, epochs[best_idx], rms_vals[best_idx]


# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == "__main__":
    print("[*] Расчёт с полным набором (15 звёзд) — метод усреднения...")
    epochs_all, rms_all, t_all, r_all = find_best_epoch(STARS)
    print(f"    Минимум RMS = {r_all:.3f}° на эпоху {t_all} CE")

    # Только быстрые (топ-6 по pm): как у Дамбиса
    fast_stars = sorted(STARS, key=lambda s: -(abs(s[5]) + abs(s[6])))[:6]
    print(f"[*] Быстрые звёзды (top 6):")
    for s in fast_stars:
        print(f"    - {s[0]}: pm=({s[5]:.1f}, {s[6]:.1f}) mas/yr")
    epochs_fast, rms_fast, t_fast, r_fast = find_best_epoch(fast_stars)
    print(f"    Минимум RMS = {r_fast:.3f}° на эпоху {t_fast} CE")

    # Только медленные: близко к Морозову
    slow_stars = sorted(STARS, key=lambda s: abs(s[5]) + abs(s[6]))[:6]
    print(f"[*] Медленные звёзды (top 6):")
    epochs_slow, rms_slow, t_slow, r_slow = find_best_epoch(slow_stars)
    print(f"    Минимум RMS = {r_slow:.3f}° на эпоху {t_slow} CE")

    # График
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(epochs_all, rms_all, 'b-', lw=2, label=f'Все 15 звёзд (min {t_all} CE)')
    ax.plot(epochs_fast, rms_fast, 'r-', lw=2, label=f'6 быстрых, Дамбис (min {t_fast} CE)')
    ax.plot(epochs_slow, rms_slow, 'g-', lw=2, label=f'6 медленных (min {t_slow} CE)')
    ax.axvline(137, color='gray', linestyle='--', alpha=0.7, label='Птолемей +137')
    ax.axvline(-130, color='purple', linestyle=':', alpha=0.7, label='Гиппарх -130')
    ax.axvline(800, color='orange', linestyle=':', alpha=0.7, label='Морозов ~+800')
    ax.set_xlabel('Эпоха (год CE)')
    ax.set_ylabel('RMS невязка, градусы')
    ax.set_title('Датировка каталога Альмагеста методом Морозова-Дамбиса')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/macbookpro14/Documents/Projects/astro-dating/almagest_dating.png', dpi=120)
    print("[*] График: /Users/macbookpro14/Documents/Projects/astro-dating/almagest_dating.png")

    # Отчёт
    with open('/Users/macbookpro14/Documents/Projects/astro-dating/almagest_dating.md', 'w') as f:
        f.write(f"""# Датировка каталога Альмагеста

Метод Морозова-Дамбиса: минимум RMS невязки координат при переборе эпох.

## Результаты

| Набор звёзд | Лучшая эпоха | RMS, ° | Совпадение с традицией |
|---|---|---|---|
| Все 15 | **{t_all} CE** | {r_all:.3f} | {'Близко к Птолемею +137' if abs(t_all - 137) < 100 else 'Сдвиг от Птолемея'} |
| 6 быстрых (Дамбис) | **{t_fast} CE** | {r_fast:.3f} | {'Эпоха Гиппарха' if abs(t_fast + 130) < 150 else 'Эпоха Птолемея' if abs(t_fast - 137) < 100 else 'Аномалия'} |
| 6 медленных | **{t_slow} CE** | {r_slow:.3f} | Сильно шумит из-за малых pm |

## Интерпретация

Быстрые звёзды дают {t_fast} CE.
- Если это близко к -130 (Гиппарх) → Птолемей скопировал каталог Гиппарха (Дамбис прав).
- Если это близко к +137 (Птолемей) → каталог оригинальный (Грассхоф прав).
- Если это >+500 → версия Морозова о средневековой датировке.

Наш результат: **{t_fast} CE** — {'поддерживает гипотезу Дамбиса (Гиппарх)' if abs(t_fast + 130) < 150 else 'поддерживает традицию (Птолемей сам)' if abs(t_fast - 137) < 100 else 'спорный'}.

## Исходные данные

{len(STARS)} звёзд из Альмагеста (Toomer 1984) + Hipparcos современные pm.

""")
    print("[*] Отчёт: /Users/macbookpro14/Documents/Projects/astro-dating/almagest_dating.md")
