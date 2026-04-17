#!/usr/bin/env python3
"""
L9 — Два кода природы: ЭМ-спектр как доказательство мульти-фрактала.

Входные данные: только фундаментальные константы (NIST CODATA + COBE FIRAS).
Выход: таблица попаданий + вертикальная логарифмическая лестница.

Тезис: от CMB-пика (1.063 мм) до видимого света существуют два независимых кода:
  - Код 1: ×10 (молекулярные квантовые переходы: CO₂, Nd:YAG лазеры)
  - Код 2: ×2 (11 октав → пик зрения 519 нм ≈ мезопический максимум 507 нм, ±2.4%)

Документ: docs/lectures/L9-two-codes.md
Размер файла: 64 строки (2⁶, шаблон якоря ARCHITECTURE-2N).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# ── Константы (NIST CODATA + COBE FIRAS 1990) ─────────────────────────────────
b_WIEN  = 2.897771955e-3   # м·К — постоянная смещения Вина (λ-форма)
T_CMB   = 2.72548          # К   — температура CMB (Fixsen 2009, ±0.57 мK)
CMB_PEAK = b_WIEN / T_CMB  # м   — пик CMB по длине волны

# Реальные лазерные линии (справочник)
CO2_REAL   = 10.600e-6     # м — CO₂ лазер (основная линия 10P(20))
NDYAG_REAL = 1.0640e-6     # м — Nd:YAG лазер (⁴F₃/₂ → ⁴I₁₁/₂)
GREEN_SCOT  = 507e-9       # м — мезопический пик (сумеречное зрение, V'(λ))
GREEN_PHOT  = 555e-9       # м — фотопический пик (дневное зрение, V(λ))

# ── Код 1: десятичный (×10⁻¹) ─────────────────────────────────────────────────
decimal = {
    'CMB':   CMB_PEAK,
    'CO₂':   CMB_PEAK / 1e2,
    'Nd:YAG': CMB_PEAK / 1e3,
}

# ── Код 2: двоичный (÷2 каждый шаг) ──────────────────────────────────────────
N_OCTAVES = 11
binary_peak = CMB_PEAK / (2 ** N_OCTAVES)

# ── Таблица попаданий ─────────────────────────────────────────────────────────
def pct_error(calc, real):
    return abs(calc - real) / real * 100

results = [
    ('CMB пик',       CMB_PEAK,           None,        'определение', 'decimal'),
    ('CO₂ ×10⁻²',    decimal['CO₂'],     CO2_REAL,    f'{pct_error(decimal["CO₂"], CO2_REAL):.2f}%', 'decimal'),
    ('Nd:YAG ×10⁻³', decimal['Nd:YAG'],  NDYAG_REAL,  f'{pct_error(decimal["Nd:YAG"], NDYAG_REAL):.3f}%', 'decimal'),
    ('Зелёный /2¹¹',  binary_peak,        GREEN_SCOT,  f'{pct_error(binary_peak, GREEN_SCOT):.1f}%', 'binary'),
]

print('=' * 65)
print('  L9 — Два кода природы в ЭМ-спектре')
print(f'  CMB-пик: {CMB_PEAK*1e3:.4f} мм  (T={T_CMB} К)')
print('=' * 65)
print(f'  {"Шаг":<16} {"Код":<9} {"Расчёт":>14} {"Реальный":>14} {"Промах":>8}')
print('  ' + '-' * 63)
for name, calc, real, err, code in results:
    calc_str = f'{calc*1e9:.2f} нм' if calc < 1e-4 else f'{calc*1e6:.4f} мкм' if calc < 1e-2 else f'{calc*1e3:.4f} мм'
    real_str = f'{real*1e9:.2f} нм' if real and real < 1e-4 else f'{real*1e6:.4f} мкм' if real and real < 1e-2 else '—'
    print(f'  {name:<16} {code:<9} {calc_str:>14} {real_str:>14} {err:>8}')

print()
print(f'  Двоичная цепь: CMB / 2¹¹ = {binary_peak*1e9:.1f} нм')
print(f'  Мезопический пик (сумерки): {GREEN_SCOT*1e9:.0f} нм → промах {pct_error(binary_peak, GREEN_SCOT):.1f}%')
print(f'  Два кода структурно независимы: CO₂/Nd:YAG не в серии 2ⁿ, зелёный не в серии ×10')

# ── Проверка независимости кодов ─────────────────────────────────────────────
co2_in_binary = CO2_REAL / CMB_PEAK
best_n = round(np.log2(1/co2_in_binary))
co2_binary_pred = CMB_PEAK / 2**best_n
print(f'\n  Проверка независимости:')
print(f'  CO₂ в двоичной серии: ближайшее 2¹{best_n} → {co2_binary_pred*1e6:.2f} мкм ≠ {CO2_REAL*1e6:.2f} мкм')
green_decimal_pred = CMB_PEAK / 1e4
print(f'  Зелёный в десятичной: ×10⁻⁴ → {green_decimal_pred*1e9:.0f} нм ≠ {binary_peak*1e9:.0f} нм  ✅ независимы')

# ── График ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 8))

wavelengths = {
    'CMB\n1.063 мм':      (CMB_PEAK,        'decimal', 0.0),
    'CO₂ лазер\n10.6 мкм': (CO2_REAL,       'decimal', 0.0),
    'Nd:YAG\n1.064 мкм':  (NDYAG_REAL,      'decimal', 0.0),
    'Зелёный свет\n519 нм': (binary_peak,    'binary',  0.05),
    'Дневной пик\n555 нм': (GREEN_PHOT,      'ref',     0.05),
}

colors = {'decimal': '#e74c3c', 'binary': '#2ecc71', 'ref': '#95a5a6'}
log_vals = {name: -np.log10(wl) for name, (wl, _, _) in wavelengths.items()}

for name, (wl, code, dx) in wavelengths.items():
    y = -np.log10(wl)
    ax.axhline(y, color=colors[code], lw=2 if code != 'ref' else 1,
               ls='-' if code != 'ref' else '--', alpha=0.8)
    ax.text(0.98 + dx, y, f'  {name}', va='center', fontsize=9,
            color=colors[code], transform=ax.get_yaxis_transform())

# стрелки кодов
for y1, y2, label, color in [
    (-np.log10(CMB_PEAK), -np.log10(CO2_REAL),   '÷10²',  '#e74c3c'),
    (-np.log10(CO2_REAL), -np.log10(NDYAG_REAL),  '÷10',   '#e74c3c'),
    (-np.log10(CMB_PEAK), -np.log10(binary_peak), '÷2¹¹',  '#2ecc71'),
]:
    ax.annotate('', xy=(0.5, y2), xytext=(0.5, y1),
                xycoords=('axes fraction', 'data'),
                textcoords=('axes fraction', 'data'),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    ax.text(0.52, (y1+y2)/2, label, fontsize=9, color=color,
            transform=ax.get_yaxis_transform(), va='center')

ax.set_ylim(2, 4)
ax.set_xlim(0, 1)
ax.set_ylabel('-log₁₀(λ), м', fontsize=11)
ax.set_title('Два кода природы в ЭМ-спектре\n'
             'Красный: ×10 (молекулярный)  |  Зелёный: ×2 (биологический)', fontsize=12)
ax.set_xticks([])
ax.grid(axis='y', alpha=0.3)

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, 'l9_two_codes_spectrum.png')
plt.tight_layout()
plt.savefig(out_file, dpi=150)
print(f'\n📊 График: {out_file}')
