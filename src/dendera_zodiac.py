#!/usr/bin/env python3
"""
Датировка Дендерского зодиака по планетным позициям.

Знаменитый рельеф на потолке храма Хатхор в Дендере (Египет).
Содержит уникальный гороскоп — положения 5 планет в знаках зодиака.

Спор о датировке:
  • Традиция (Cauville 2001): 25 июня 50 BCE
  • Фоменко/Носовский: +1168 CE (новая хронология)
  • Морозов: одна из средневековых дат (+568, +1147, +1185)

Метод: перебор всех дат в диапазоне −1000..+1500, для каждой
вычисляем в каком знаке зодиака находится каждая планета.
Ищем даты, когда ВСЕ 5 планет в указанных знаках одновременно.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from skyfield.almanac import fraction_illuminated

RESULTS = Path(__file__).parent.parent / "results"
RESULTS.mkdir(exist_ok=True)


# ─────────────────────────────────────────────────────────────
# ДАНNЫЕ: положения планет на Дендерском зодиаке
# ─────────────────────────────────────────────────────────────
#
# Интерпретация рельефа (Cauville 2001, «Le zodiaque d'Osiris»):
#
# Меркурий    — в Близнецах (или Деве — спорно; у Cauville: Libra)
# Венера      — в Рыбах
# Марс        — в Козероге
# Юпитер      — в Раке
# Сатурн      — в Деве
# Солнце      — около перехода Рыбы/Овен (весеннее равноденствие)
#
# Это уникальная конфигурация — встречается очень редко.

EXPECTED = {
    # Атрибуция Aubourg 1995 / Cauville 2001 для 25 июня 50 BCE:
    "Mercury": "Gemini",      # Меркурий в Близнецах
    "Venus":   "Aquarius",    # Венера в Водолее
    "Mars":    "Capricornus", # Марс в Козероге
    "Jupiter": "Cancer",      # Юпитер в Раке
    "Saturn":  "Virgo",       # Сатурн в Деве
}

# Эклиптические долготы центров знаков (0° = 0° Овна)
SIGN_BOUNDARIES = {
    "Aries":        (0, 30),
    "Taurus":       (30, 60),
    "Gemini":       (60, 90),
    "Cancer":       (90, 120),
    "Leo":          (120, 150),
    "Virgo":        (150, 180),
    "Libra":        (180, 210),
    "Scorpius":     (210, 240),
    "Sagittarius":  (240, 270),
    "Capricornus":  (270, 300),
    "Aquarius":     (300, 330),
    "Pisces":       (330, 360),
}


def sign_of(longitude_deg):
    lon = longitude_deg % 360
    for s, (lo, hi) in SIGN_BOUNDARIES.items():
        if lo <= lon < hi:
            return s
    return "Aries"


# ─────────────────────────────────────────────────────────────
# АСТРОНОМИЯ
# ─────────────────────────────────────────────────────────────

def load_ephemeris():
    """Пробуем DE422 (широкий диапазон), падая в DE440s (узкий)."""
    for name in ("de422.bsp", "de440.bsp", "de440s.bsp"):
        try:
            eph = load(name)
            print(f"[*] Ephemeris: {name}")
            return eph
        except Exception:
            continue
    raise RuntimeError("No ephemeris could be loaded")


def parse_date_iso(date_iso):
    """Парсит '-49-06-25' или '50-06-25' в (year, month, day)."""
    s = date_iso.strip()
    neg = s.startswith('-')
    if neg: s = s[1:]
    parts = s.split('-')
    year = int(parts[0]) * (-1 if neg else 1)
    month = int(parts[1]) if len(parts) > 1 else 1
    day = int(parts[2]) if len(parts) > 2 else 1
    return year, month, day

def planet_longitudes(eph, ts, date_iso):
    """Эклиптические долготы планет с Земли на указанную дату."""
    try:
        y, m, d = parse_date_iso(date_iso)
        t = ts.utc(y, m, d)
    except Exception as e:
        return None
    earth = eph['earth']
    bodies = {
        "Mercury": eph['mercury'],
        "Venus":   eph['venus'],
        "Mars":    eph['mars'],
        "Jupiter": eph['jupiter barycenter'],
        "Saturn":  eph['saturn barycenter'],
        "Sun":     eph['sun'],
    }
    result = {}
    for name, body in bodies.items():
        apparent = earth.at(t).observe(body).apparent()
        # Эклиптика ДАТЫ (tropical zodiac — привязан к точке равноденствия эпохи T)
        lat, lon, dist = apparent.ecliptic_latlon(epoch='date')
        result[name] = lon.degrees % 360
    return result


def score_date(positions):
    """Сколько планет совпало со знаком зодиака на Дендере?"""
    if not positions:
        return 0
    score = 0
    details = {}
    for planet, expected_sign in EXPECTED.items():
        actual = sign_of(positions[planet])
        details[planet] = {"actual": actual, "expected": expected_sign, "match": actual == expected_sign}
        if actual == expected_sign:
            score += 1
    return score, details


def slow_planets_score(positions):
    """Только медленные планеты: Mars, Jupiter, Saturn. Они надёжно идентифицируют эпоху."""
    slow = ["Mars", "Jupiter", "Saturn"]
    score = 0
    for p in slow:
        if sign_of(positions[p]) == EXPECTED[p]:
            score += 1
    return score

def search_matches(eph, ts, year_from=-500, year_to=1500):
    """Ищем даты когда Mars+Jupiter+Saturn одновременно в ожидаемых знаках.
    Меркурий и Венера — слишком быстрые, используются как вторичный критерий."""
    matches = []
    years = list(range(year_from, year_to + 1, 2))
    total = len(years)

    print(f"[*] Поиск (Mars+Jupiter+Saturn) с {year_from} по {year_to}, шаг 2 года × 4 мес...")
    for i, y in enumerate(years):
        if i % 100 == 0 and i > 0:
            found = len([m for m in matches if m['slow_score'] == 3])
            print(f"    прогресс: {i}/{total} ({100*i//total}%), найдено 3/3: {found}")
        for month in (1, 4, 7, 10):
            date_iso = f"{y}-{month:02d}-15"
            pos = planet_longitudes(eph, ts, date_iso)
            if pos is None:
                continue
            slow = slow_planets_score(pos)
            if slow < 2:
                continue  # если даже 2/3 медленных не совпало — нет смысла дальше смотреть
            full, details = score_date(pos)
            matches.append({
                "year": y,
                "month": month,
                "slow_score": slow,
                "score": full,
                "details": details,
                "positions": pos,
            })
    return matches


# ─────────────────────────────────────────────────────────────
# ГЛАВНЫЙ АНАЛИЗ
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ДЕНДЕРСКИЙ ЗОДИАК — датировка по планетам")
    print("=" * 60)
    print(f"Ожидаемая конфигурация (по Cauville 2001):")
    for p, s in EXPECTED.items():
        print(f"  {p:<10} → {s}")
    print()

    eph = load_ephemeris()
    ts = load.timescale()

    # Проверяем три гипотезы по отдельности
    print("─" * 60)
    print("КЛЮЧЕВЫЕ ДАТЫ:")
    print("─" * 60)

    candidates = [
        ("Cauville 2001 (25 июн 50 BCE)", "-49-06-25"),
        ("Морозов 568", "568-06-25"),
        ("Морозов 1147", "1147-06-25"),
        ("Морозов 1185", "1185-06-25"),
        ("Фоменко 1168", "1168-06-25"),
    ]

    for label, date_iso in candidates:
        pos = planet_longitudes(eph, ts, date_iso)
        if not pos:
            print(f"  {label}: (не удалось — вне эфемерид?)")
            continue
        score, details = score_date(pos)
        status = "✅" if score == 5 else "⚠️" if score >= 3 else "❌"
        print(f"\n  {status} {label} [score={score}/5]")
        for p, d in details.items():
            mark = "✓" if d["match"] else "✗"
            print(f"      {mark} {p:<8} → {d['actual']:<15} (ожидался {d['expected']})")

    # Массовый поиск — Mars+Jupiter+Saturn (медленные планеты)
    print("\n─" * 60)
    print("МАССОВЫЙ ПОИСК: Mars+Jupiter+Saturn в ожидаемых знаках")
    print("─" * 60)
    matches = search_matches(eph, ts, year_from=-500, year_to=1500)

    perfect = [m for m in matches if m['slow_score'] == 3]
    near = [m for m in matches if m['slow_score'] == 2]

    print(f"\n[*] Точное совпадение 3/3 медленных планет: {len(perfect)} дат")
    print(f"[*] Близко 2/3: {len(near)} дат")

    if perfect:
        print(f"\nТоп-15 точных (3/3 medium planets; sorted by full score):")
        sorted_perfect = sorted(perfect, key=lambda m: (-m['score'], abs(m['year'] + 49)))
        for m in sorted_perfect[:15]:
            marker = ""
            if -55 <= m['year'] <= -45: marker = " ← Cauville window"
            if 560 <= m['year'] <= 580: marker = " ← Морозов-568 window"
            if 1140 <= m['year'] <= 1200: marker = " ← медиевалная гипотеза"
            print(f"  full={m['score']}/5 slow=3/3  {m['year']:5d}-{m['month']:02d}{marker}")
    best = perfect + near

    # Сохраняем результат
    import json
    with open(RESULTS / "dendera_matches.json", "w") as f:
        json.dump([{
            "year": m["year"],
            "month": m["month"],
            "score": m["score"],
            "details": m["details"],
        } for m in best[:50]], f, indent=2, ensure_ascii=False)

    # Отчёт
    perfect = [m for m in best if m["score"] == 5]
    near = [m for m in best if m["score"] == 4]

    with open(RESULTS / "dendera_zodiac.md", "w") as f:
        f.write(f"""# Датировка Дендерского зодиака по планетным позициям

## Ожидаемая конфигурация (Cauville 2001)

""")
        for p, s in EXPECTED.items():
            f.write(f"- {p}: {s}\n")
        f.write(f"""
## Результаты ключевых гипотез

| Гипотеза | Дата | Score | Статус |
|---|---|---|---|
""")
        for label, date_iso in candidates:
            pos = planet_longitudes(eph, ts, date_iso)
            if pos:
                score, _ = score_date(pos)
                status = "✅ Точное совпадение" if score == 5 else "⚠️ Частичное" if score >= 3 else "❌ Не совпадает"
                f.write(f"| {label} | {date_iso} | {score}/5 | {status} |\n")

        f.write(f"""
## Массовый поиск

Перебор с шагом 5 лет × 2 месяца в диапазоне −500 до +1500 CE.

- Точных совпадений (5/5): **{len(perfect)}**
- Близких совпадений (4/5): **{len(near)}**

Топ-10 кандидатов:

| # | Год | Месяц | Score |
|---|---|---|---|
""")
        for i, m in enumerate(best[:10], 1):
            f.write(f"| {i} | {m['year']} | {m['month']} | {m['score']}/5 |\n")

        f.write(f"""

## Интерпретация

Если грубый перебор (шаг 5 лет × 2 месяца) не находит точного совпадения
рядом с ожидаемыми датами, следующий шаг — более тонкий перебор (шаг 1 день)
вокруг лучших кандидатов.

## Примечания

- Интерпретация рельефа Дендеры неоднозначна. У разных авторов
  (Cauville, Aubourg, Leitz) разные атрибуции планет знакам.
- Наш расчёт использует атрибуцию Cauville 2001 для наиболее
  устоявшейся научной интерпретации.
- Для окончательного ответа нужна точная сетка дней и проверка
  альтернативных атрибуций.

## Ссылки

1. Cauville S. *Le zodiaque d'Osiris*. Peeters, Leuven 1997.
2. Aubourg É. *La date de conception du zodiaque du temple de Hathor à Dendara* // BIFAO 95 (1995).
3. Фоменко А.Т., Носовский Г.В. *Новая хронология Египта*. М. 2002.
4. Морозов Н.А. *Христос*. Т. 6.
""")
    print(f"\n[*] Отчёт: {RESULTS / 'dendera_zodiac.md'}")
    print(f"[*] JSON:  {RESULTS / 'dendera_matches.json'}")


if __name__ == "__main__":
    main()
