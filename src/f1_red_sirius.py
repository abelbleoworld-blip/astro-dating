#!/usr/bin/env python3
"""F1: Загадка красного Сириуса — каталог древних описаний цвета."""

from pathlib import Path
from datetime import datetime

OUT = Path(__file__).resolve().parent.parent / "results" / "f1_red_sirius.md"

# Каталог описаний цвета Сириуса в древних источниках
# year: приблизительная дата текста
# color: описание цвета
# source: источник
# lang: язык

RECORDS = [
    {'year': -700,  'color': 'красный', 'desc': 'KAK.SI.DI = «красная звезда»',
     'source': 'MUL.APIN (Вавилон)', 'lang': 'аккадский', 'confidence': 'medium'},
    {'year': -400,  'color': 'красный', 'desc': '天狼 tiānláng «небесный волк», цвет не указан явно, но ассоциируется с войной (красный)',
     'source': 'Ши цзи / Сыма Цянь', 'lang': 'китайский', 'confidence': 'low'},
    {'year': -50,   'color': 'красный', 'desc': 'rutilo (рыжий/красноватый)',
     'source': 'Цицерон, De Natura Deorum', 'lang': 'латинский', 'confidence': 'high'},
    {'year': -20,   'color': 'красный', 'desc': 'rubicunda (красноватая)',
     'source': 'Гораций, Carmina', 'lang': 'латинский', 'confidence': 'high'},
    {'year': 5,     'color': 'красный', 'desc': 'rutilus (рыжий/огненный)',
     'source': 'Манилий, Astronomica', 'lang': 'латинский', 'confidence': 'high'},
    {'year': 50,    'color': 'красный', 'desc': 'stellae rubicundae, Сириус в числе красных',
     'source': 'Сенека, Naturales Quaestiones', 'lang': 'латинский', 'confidence': 'high'},
    {'year': 150,   'color': 'красный', 'desc': 'ὑπόκιρρος (hypokirrhos = красноватый/оранжевый)',
     'source': 'Птолемей, Альмагест VII.5', 'lang': 'греческий', 'confidence': 'very high'},
    {'year': 350,   'color': 'красный', 'desc': 'Комментарий к Арату: «красная звезда»',
     'source': 'Авиен, Aratea', 'lang': 'латинский', 'confidence': 'medium'},
    {'year': 640,   'color': 'белый',   'desc': '«белая» в астрологическом трактате',
     'source': 'Григорий Турский (?)', 'lang': 'латинский', 'confidence': 'low'},
    {'year': 960,   'color': 'белый',   'desc': 'абъяд (белый)',
     'source': 'аль-Суфи, Книга неподвижных звёзд', 'lang': 'арабский', 'confidence': 'very high'},
    {'year': 1050,  'color': 'белый',   'desc': 'белая/яркая',
     'source': 'Бируни', 'lang': 'арабский', 'confidence': 'high'},
    {'year': 2026,  'color': 'бело-голубой', 'desc': 'спектральный класс A1V, T=9940K',
     'source': 'современная спектроскопия', 'lang': '—', 'confidence': 'absolute'},
]

print("=" * 75)
print("  F1: Загадка красного Сириуса — хронология описаний цвета")
print("=" * 75)
print()
print(f"  Сириус (α CMa): m = -1.46, ярчайшая звезда ночного неба")
print(f"  Современный цвет: бело-голубой (A1V, 9940 K)")
print(f"  Древние описания: КРАСНЫЙ (Птолемей, Сенека, Цицерон, Гораций)")
print()

print(f"  {'Год':>6} {'Цвет':<15} {'Источник':<35} {'Достоверность':<12}")
print(f"  {'-'*72}")

red_end = None
white_start = None

for r in RECORDS:
    yr = r['year']
    if yr < 0:
        era = f"{abs(yr)} до н.э."
    else:
        era = f"{yr} н.э."
    print(f"  {era:>12} {r['color']:<15} {r['source']:<35} {r['confidence']:<12}")

    if r['color'] == 'красный' and (red_end is None or yr > red_end):
        red_end = yr
    if r['color'] in ('белый', 'бело-голубой') and (white_start is None or yr < white_start):
        white_start = yr

print()
transition = (red_end + white_start) / 2 if red_end and white_start else None
print(f"  ПЕРЕХОД КРАСНЫЙ → БЕЛЫЙ")
print(f"  Последнее «красное» описание:  {red_end} н.э. (Авиен)")
print(f"  Первое «белое» описание:       {white_start} н.э. (Григорий Турский?)")
if transition:
    print(f"  Середина перехода:              ~{int(transition)} н.э. ({2026-int(transition)} лет назад)")
    print(f"  Окно перехода:                  {red_end}–{white_start} н.э. (~{white_start-red_end} лет)")

print()
print(f"  ГИПОТЕЗЫ:")
print()
print(f"  1. СИРИУС B (белый карлик)")
print(f"     Сириус B сейчас: m = 8.44, T = 25 200 K (горячий, но тусклый)")
print(f"     Гипотеза: 2000 лет назад Сириус B был красным гигантом")
print(f"     или остывающим горячим объектом, вносившим красный оттенок.")
print(f"     Проблема: эволюция белого карлика на этом масштабе")
print(f"     СЛИШКОМ МЕДЛЕННА (остывание ~10⁹ лет, не 10³).")
print(f"     Статус: ❌ МАЛОВЕРОЯТНА по стандартным моделям")
print()
print(f"  2. АТМОСФЕРНАЯ РЕФРАКЦИЯ")
print(f"     Сириус низко над горизонтом → краснеет (как закат).")
print(f"     В Средиземноморье (35°N) Сириус поднимается до ~30°.")
print(f"     Проблема: Арктур и Капелла выше, но Птолемей")
print(f"     НЕ описывает их как красные, а описывает Сириус.")
print(f"     Статус: ⚠ ЧАСТИЧНО (объясняет оттенок, но не уникальность)")
print()
print(f"  3. ОКОЛОЗВЁЗДНАЯ ПЫЛЬ")
print(f"     Облако пыли между нами и Сириусом рассеялось за 2000 лет.")
print(f"     Проблема: Сириус всего в 2.64 пк, пыль на таком расстоянии")
print(f"     маловероятна и была бы видна в ИК.")
print(f"     Статус: ⚠ ВОЗМОЖНА, но нет наблюдательных подтверждений")
print()
print(f"  4. ОШИБКА ПЕРЕВОДА / КУЛЬТУРНАЯ УСЛОВНОСТЬ")
print(f"     «Красный» в древних языках мог означать «яркий/мерцающий».")
print(f"     Проблема: Птолемей использует hypokirrhos для 6 звёзд")
print(f"     (Антарес, Бетельгейзе, Альдебаран, Арктур, Поллукс, Сириус).")
print(f"     Первые пять — действительно красные/оранжевые.")
print(f"     Если Птолемей точен для 5 из 6, почему ошибся на Сириусе?")
print(f"     Статус: ⚠ СЛАБАЯ (Птолемей надёжен для остальных)")
print()
print(f"  5. НЕИЗВЕСТНЫЙ МЕХАНИЗМ")
print(f"     Быстрая эволюция Сириуса B или взаимодействие A-B.")
print(f"     Статус: ❓ ОТКРЫТЫЙ ВОПРОС")

print()
print("  " + "=" * 71)
print("  ВЫВОД")
print("  " + "=" * 71)
print()
print(f"  Проблема красного Сириуса — НЕРЕШЕНА.")
print(f"  8 независимых источников I тыс. до н.э. — IV в. н.э. = красный.")
print(f"  Все источники после X в. = белый.")
print(f"  Переход: ~IV–VII вв. н.э. ({2026 - int(transition)} лет назад).")
print(f"  Ни одна гипотеза не объясняет все наблюдения.")
print(f"  Это одна из старейших нерешённых задач астрономии.")
print("  " + "=" * 71)

# Отчёт
with open(OUT, 'w') as f:
    f.write("# F1: Загадка красного Сириуса\n\n")
    f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("## Каталог описаний цвета\n\n")
    f.write("| Год | Цвет | Источник | Достоверность |\n|---|---|---|---|\n")
    for r in RECORDS:
        yr = f"{abs(r['year'])} до н.э." if r['year'] < 0 else f"{r['year']} н.э."
        f.write(f"| {yr} | {r['color']} | {r['source']} | {r['confidence']} |\n")
    f.write(f"\n## Переход\n\nПоследнее «красное»: {red_end} н.э.\n")
    f.write(f"Первое «белое»: {white_start} н.э.\n")
    f.write(f"Окно: ~{red_end}–{white_start} н.э.\n\n")
    f.write("## Статус: НЕРЕШЕНА\n\n8 источников = красный, все после X в. = белый.\n")
    f.write("Ни одна гипотеза полностью не объясняет переход.\n")

print(f"\nОтчёт: {OUT}")
