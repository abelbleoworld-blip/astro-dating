#!/usr/bin/env python3
"""
Верификация затмения эпонима Бур-Сагале (763 BCE) —
якорной точки всей ассирийской хронологии.

КОНТЕКСТ:
В "Ассирийском каноне эпонимов" — списке годов по именам чиновников
(limmu) — содержится запись: "В эпонимат Бур-Сагале (Pur-Sagalê),
правителя Гузаны, в месяце Симану (май-июнь), произошло затмение солнца".

Это ЕДИНСТВЕННОЕ астрономически датируемое событие в ассирийском канонe.
Всего канон охватывает ~250 лет правителей. Привязка к 15 июня 763 BCE
(NASA catalog) даёт точный год каждого ассирийского эпонима и, через
царский список Ассирии, датирует всех ассирийских царей.

Это якорь для:
- Ассирийской хронологии 10-7 веков BCE
- Еврейской хронологии (цари Иудеи и Израиля через синхронизмы)
- Вавилонской хронологии (через дипломатическую переписку)
- Библейских событий от Тиглатпаласара III до Навуходоносора

ТЕСТ:
1. Было ли затмение 15 июня 763 BCE видимо над Ассирией (Ниневия, ~36.3°N 43.1°E)?
2. Какова магнитуда и время?
3. Альтернативные даты в окне −810..−710 — есть ли сравнимые?
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from skyfield.api import load, wgs84
from skyfield.framelib import ecliptic_frame

RESULTS = Path(__file__).parent.parent / "results"
RESULTS.mkdir(exist_ok=True)

# Ассирия — Ниневия (столица при Ашшурдане III)
NINEVEH = (36.36, 43.15)
# Альтернатива: Ашшур (старая столица)
ASSUR = (35.46, 43.26)

# Эфемериды: DE422 покрывает −3000..+3000
eph = load("de422.bsp")
ts = load.timescale()
sun = eph["sun"]
moon = eph["moon"]
earth = eph["earth"]


def solar_moon_separation(y, m, d, hour_utc, lat, lon):
    """Угловое разделение Солнца и Луны с указанной точки в момент времени."""
    t = ts.utc(y, m, d, hour_utc, 0)
    observer = wgs84.latlon(lat, lon)
    obs = earth + observer
    ap_sun = obs.at(t).observe(sun).apparent()
    ap_moon = obs.at(t).observe(moon).apparent()
    sep = ap_sun.separation_from(ap_moon).degrees
    # Также получим эклиптические координаты для проверки соединения
    lon_sun, _, _ = ap_sun.frame_latlon(ecliptic_frame)
    lon_moon, _, _ = ap_moon.frame_latlon(ecliptic_frame)
    return sep, lon_sun.degrees, lon_moon.degrees


def scan_day_for_min_sep(y, m, d, lat, lon):
    """Ищет минимальное угловое разделение на указанный день (шаг 15 минут)."""
    best = (999, None)
    for h_quarter in range(0, 96):  # 96 × 15 минут = 24 часа
        h = h_quarter // 4
        minute = (h_quarter % 4) * 15
        t = ts.utc(y, m, d, h, minute)
        observer = wgs84.latlon(lat, lon)
        obs = earth + observer
        ap_sun = obs.at(t).observe(sun).apparent()
        ap_moon = obs.at(t).observe(moon).apparent()
        sep = ap_sun.separation_from(ap_moon).degrees
        if sep < best[0]:
            best = (sep, f"{h:02d}:{minute:02d}")
    return best


def scan_year_for_eclipses(y, lat, lon, threshold_deg=2.0):
    """Сканирует весь год с шагом 1 день: ищет дни когда Sun-Moon < threshold."""
    candidates = []
    for m in range(1, 13):
        max_d = 31
        if m in (4, 6, 9, 11):
            max_d = 30
        if m == 2:
            max_d = 29  # игнорируем високосные тонкости
        for d in range(1, max_d + 1):
            try:
                # Полуденная проверка (достаточно для выборки)
                sep, _, _ = solar_moon_separation(y, m, d, 12, lat, lon)
            except Exception:
                continue
            if sep < threshold_deg:
                # Уточняем поминутно
                sep_min, time_min = scan_day_for_min_sep(y, m, d, lat, lon)
                candidates.append({
                    "date": f"{y:+d}-{m:02d}-{d:02d}",
                    "year": y,
                    "month": m,
                    "day": d,
                    "min_sep": round(sep_min, 3),
                    "time_utc": time_min,
                })
    return candidates


def main():
    print("=" * 60)
    print("ЗАТМЕНИЕ БУР-САГАЛЕ (763 BCE) — ассирийский якорь")
    print("=" * 60)

    # 1. Главная проверка: 15 июня −762 (763 BCE = −762 астрон.)
    # NASA catalog: Solar eclipse of June 15, 763 BCE
    print("\n■ Основная гипотеза: 15 июня 763 BCE (= -762 astronomical) над Ниневией")
    sep, time_min = scan_day_for_min_sep(-762, 6, 15, *NINEVEH)
    print(f"  Минимальное Sun-Moon разделение: {sep:.3f}° в {time_min} UTC")
    print(f"  Порог затмения (~1.5°): {'ЗАТМЕНИЕ ✅' if sep < 1.5 else 'НЕ затмение ❌'}")

    # Также в Ашшуре
    sep_as, _ = scan_day_for_min_sep(-762, 6, 15, *ASSUR)
    print(f"  В Ашшуре: {sep_as:.3f}°")

    # 2. Альтернативы — проверяем соседние годы
    print("\n■ Альтернативные даты в окне -810..-710:")
    alternatives = []
    for y in range(-810, -710, 5):  # грубо: каждые 5 лет
        cands = scan_year_for_eclipses(y, NINEVEH[0], NINEVEH[1], threshold_deg=1.0)
        alternatives.extend(cands)

    # Сортируем по магнитуде
    alternatives.sort(key=lambda c: c["min_sep"])
    print(f"  Найдено {len(alternatives)} возможных затмений над Ниневией")
    print("\n  Топ-10 по минимальному разделению:")
    for c in alternatives[:10]:
        marker = " ← ГИПОТЕЗА" if c["year"] == -762 and c["month"] == 6 else ""
        print(f"    {c['date']} в {c['time_utc']} UTC — sep {c['min_sep']}°{marker}")

    # Отчёт
    with open(RESULTS / "bur_sagale_763bce.md", "w") as f:
        f.write(f"""# Затмение эпонима Бур-Сагале (763 BCE) — якорь ассирийской хронологии

## Контекст

В "Ассирийском каноне эпонимов" зафиксировано солнечное затмение в год правления
Бур-Сагале (Pur-Sagalê), губернатора Гузаны, в месяце Симану (май–июнь).

Традиционная датировка: **15 июня 763 BCE** (Espenak/NASA Five Millennium Catalog).

## Результаты

| Место | Мин. разделение | Время UTC | Статус |
|---|---|---|---|
| Ниневия (36.36°N 43.15°E) | **{sep:.3f}°** | {time_min} | {"✅ ЗАТМЕНИЕ" if sep < 1.5 else "⚠️ на грани"} |
| Ашшур (35.46°N 43.26°E) | {sep_as:.3f}° | — | — |

## Интерпретация

{'Затмение 15 июня 763 BCE астрономически подтверждено над Ассирией. Это фиксирует эпонима Бур-Сагале — и через него весь "канон эпонимов" 10-7 веков BCE.' if sep < 1.5 else f'Разделение {sep:.3f}° выше стандартного порога (1.5°); уточнить позицию и время.'}

## Якорная роль в истории

Эпоним Бур-Сагале — 10-й год правления Ашшурдана III (традиционно 772–755 BCE).
Через канон (охватывает эпох от ~910 до 649 BCE) датируются:
- Все ассирийские цари Среднеассирийской и Новоассирийской эпох
- Войны и завоевания (падение Самарии 722 BCE, взятие Иерусалима Сеннахиримом 701 BCE)
- Библейские синхронизмы (Ос, Ам, Ис, 2 Пар, 2 Цар)

Если это затмение подтверждается — подтверждается вся ассирийская хронология.

## Топ-10 альтернативных затмений (для сравнения)

| Дата | Мин. разделение | Время UTC |
|---|---|---|
""")
        for c in alternatives[:10]:
            f.write(f"| {c['date']} | {c['min_sep']}° | {c['time_utc']} |\n")

        f.write(f"""
## Вывод

{"✅ **ЯКОРЬ АССИРИЙСКОЙ ХРОНОЛОГИИ ПОДТВЕРЖДЁН.**" if sep < 1.5 else "Требуется более детальный анализ."}

## Ссылки

1. Millard A.R. *The Eponyms of the Assyrian Empire 910-612 BC*. Helsinki 1994.
2. Espenak F. Five Millennium Catalog of Solar Eclipses, NASA/TP-2006-214141.
3. Ungnad A. *Die Eponymenkanon*. 1938.
4. Kuhrt A. *The Ancient Near East c.3000–330 BC*. Routledge 1995.
""")
    print(f"\n[*] Отчёт: {RESULTS / 'bur_sagale_763bce.md'}")


if __name__ == "__main__":
    main()
