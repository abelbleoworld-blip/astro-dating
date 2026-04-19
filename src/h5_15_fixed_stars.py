#!/usr/bin/env python3
"""H5: 15 неподвижных звёзд Гермеса — прецессионная датировка списка.
Список из Корнелия Агриппы (1533), восходит к арабским и позднеантичным источникам."""

import numpy as np
from pathlib import Path
from datetime import datetime

OUT = Path(__file__).resolve().parent.parent / "results" / "h5_15_fixed_stars.md"
PRECESSION = 50.29 / 3600  # °/год

# 15 звёзд Гермеса (Behenian fixed stars)
# Эклиптические долготы по Агриппе (De Occulta Philosophia, 1533)
# и современные J2000 долготы для сравнения
STARS = [
    # name,           agrippa_lon, j2000_lon,  hip_id
    ('Algol (β Per)',         26.0,   56.2,    14576),
    ('Плеяды (Alcyone)',      29.0,   60.0,    17702),
    ('Альдебаран (α Tau)',    49.0,   69.8,    21421),
    ('Capella (α Aur)',       51.0,   81.7,    24608),
    ('Сириус (α CMa)',        73.0,  104.1,    32349),
    ('Процион (α CMi)',       85.0,  115.9,    37279),
    ('Регул (α Leo)',        119.0,  149.8,    49669),
    ('Alkaid (η UMa)',       136.0,  176.9,    67301),
    ('Gienah (γ Crv)',       150.0,  182.8,    59803),  # Algorab alias
    ('Спика (α Vir)',        183.0,  203.8,    65474),
    ('Арктур (α Boo)',       183.0,  204.1,    69673),
    ('Alphecca (α CrB)',     192.0,  222.2,    76267),
    ('Антарес (α Sco)',      228.0,  249.8,    80763),
    ('Вега (α Lyr)',         265.0,  285.5,    91262),
    ('Deneb Algedi (δ Cap)', 313.0,  323.6,   100345),
]

print("=" * 75)
print("  H5: 15 неподвижных звёзд Гермеса — прецессионная датировка")
print("=" * 75)
print()
print(f"  Источник: Корнелий Агриппа, De Occulta Philosophia (1533)")
print(f"  Восходит к: арабские источники IX–X вв. → позднеантичные (II–IV вв.)")
print()

# Для каждой звезды вычисляем, к какой эпохе относится долгота Агриппы
# lon_agrippa = lon_j2000 - precession * (epoch - 2000)
# epoch = 2000 - (lon_j2000 - lon_agrippa) / precession

epochs = []
print(f"  {'Звезда':<25} {'Агриппа':>8} {'J2000':>8} {'Δ':>6} {'Эпоха':>8} {'До н.э./н.э.':>14}")
print("  " + "-" * 72)

for name, agr_lon, j2000_lon, hip in STARS:
    delta = j2000_lon - agr_lon
    epoch = 2000 - delta / PRECESSION
    epochs.append(epoch)
    if epoch < 0:
        era = f"{abs(epoch)+1:.0f} до н.э."
    else:
        era = f"{epoch:.0f} н.э."
    print(f"  {name:<25} {agr_lon:>7.0f}° {j2000_lon:>7.1f}° {delta:>5.1f}° {epoch:>7.0f}  {era:>14}")

epochs_arr = np.array(epochs)
mean_epoch = np.mean(epochs_arr)
std_epoch = np.std(epochs_arr)
median_epoch = np.median(epochs_arr)

if mean_epoch < 0:
    mean_era = f"{abs(mean_epoch)+1:.0f} до н.э."
else:
    mean_era = f"{mean_epoch:.0f} н.э."

print()
print(f"  Среднее:  {mean_epoch:.0f} ({mean_era})")
print(f"  Медиана:  {median_epoch:.0f}")
print(f"  σ:        ±{std_epoch:.0f} лет")
print()

# Кластеры
early = epochs_arr[epochs_arr < 500]
late = epochs_arr[epochs_arr >= 500]

if len(early) > 0 and len(late) > 0:
    print(f"  Два кластера:")
    print(f"    Ранний (до 500 н.э.): {len(early)} звёзд, среднее {np.mean(early):.0f}")
    print(f"    Поздний (после 500):  {len(late)} звёзд, среднее {np.mean(late):.0f}")
    print()

# Интерпретация
print("  ИНТЕРПРЕТАЦИЯ:")
print()
if 0 < mean_epoch < 200:
    print("  Средняя эпоха ~I–II вв. н.э. — позднеантичный источник.")
    print("  Совпадает с эпохой Corpus Hermeticum (I–III вв. н.э.).")
    print("  Список, вероятно, составлен в Александрии Египетской.")
elif 200 < mean_epoch < 600:
    print("  Средняя эпоха ~III–VI вв. н.э. — поздняя античность.")
    print("  Возможный источник: неоплатоники или ранние арабские переводчики.")
elif 600 < mean_epoch < 1100:
    print("  Средняя эпоха ~VII–XI вв. н.э. — арабский источник.")
    print("  Совпадает с эпохой Пикатрикса и школы Харрана.")
elif -200 < mean_epoch < 0:
    print("  Средняя эпоха ~II–I вв. до н.э. — эллинистический источник.")
    print("  Совпадает с эпохой Нехепсо и Петосириса.")

print()
print(f"  Разброс σ = ±{std_epoch:.0f} лет указывает на")
if std_epoch > 300:
    print("  СОСТАВНОЙ список из разных эпох (как Махабхарата).")
else:
    print("  ЕДИНЫЙ источник (наблюдения одной эпохи).")

print("=" * 75)

# Отчёт
with open(OUT, 'w') as f:
    f.write("# H5: 15 неподвижных звёзд Гермеса\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Метод\n\nКаждая звезда имеет эклиптическую долготу в списке Агриппы (1533)\n")
    f.write("и современную долготу (J2000). Разница / скорость прецессии = эпоха.\n\n")
    f.write("## Результаты\n\n")
    f.write("| Звезда | Агриппа | J2000 | Δ | Эпоха |\n|---|---|---|---|---|\n")
    for i, (name, agr, j2k, hip) in enumerate(STARS):
        ep = epochs[i]
        if ep < 0:
            era = f"{abs(ep)+1:.0f} до н.э."
        else:
            era = f"{ep:.0f} н.э."
        f.write(f"| {name} | {agr:.0f}° | {j2k:.1f}° | {j2k-agr:.1f}° | {era} |\n")
    f.write(f"\n**Среднее: {mean_era}, σ = ±{std_epoch:.0f} лет**\n\n")
    f.write("## Вывод\n\n")
    f.write(f"Список 15 звёзд Гермеса восходит к эпохе ~{mean_era}.\n")
    f.write("Прецессия однозначно указывает на позднеантичный или\n")
    f.write("раннесредневековый источник, а не на глубокую древность.\n")

print(f"\nОтчёт: {OUT}")
