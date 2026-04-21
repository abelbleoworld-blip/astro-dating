#!/usr/bin/env python3
"""MAU-1: Verify 5 Grand Solar Minima against SOL-1 pipeline data.
5 GSM × 5 evidence sources = 25-cell verification matrix."""

import numpy as np
import os, sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data" / "solar"
RESULTS_DIR = BASE / "results"

GSM = [
    {'name': 'Oort',    'start': 1010, 'end': 1050},
    {'name': 'Wolf',    'start': 1280, 'end': 1340},
    {'name': 'Spörer',  'start': 1460, 'end': 1550},
    {'name': 'Maunder', 'start': 1645, 'end': 1715},
    {'name': 'Dalton',  'start': 1790, 'end': 1830},
]
SOURCES = ['E1 Sunspots', 'E2 Aurora', 'E3 Corona', 'E4 C14', 'E5 Be10']


def _ratio_check(in_gsm, before, after, threshold=0.7):
    baseline = (before + after) / 2
    if baseline == 0 and in_gsm == 0:
        return 'no data', 'no records'
    ratio = in_gsm / max(baseline, 0.1)
    return ('confirmed' if ratio < threshold else 'not detected',
            f'ratio={ratio:.2f} ({in_gsm}/{baseline:.0f})')


def check_e1():
    """Pre-telescopic sunspots + SILSO."""
    # Build synthetic yearly series
    pre_tele = []
    csv_path = DATA_DIR / "pre_telescopic_sunspots.csv"
    if csv_path.exists():
        import csv
        with open(csv_path) as f:
            for row in csv.DictReader(f):
                pre_tele.append(int(row['year']))

    silso_path = DATA_DIR / "silso_yearly.csv"
    silso = {}
    if silso_path.exists():
        with open(silso_path) as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 2:
                    try:
                        silso[int(float(parts[0].strip()))] = float(parts[1].strip())
                    except ValueError:
                        pass

    results = {}
    for g in GSM:
        s, e, m = g['start'], g['end'], g['end'] - g['start']
        if s >= 1700 and silso:
            gsm_v = [v for y, v in silso.items() if s <= y <= e]
            bef_v = [v for y, v in silso.items() if s - m <= y < s]
            aft_v = [v for y, v in silso.items() if e < y <= e + m]
            if gsm_v and (bef_v or aft_v):
                gm = np.mean(gsm_v)
                bm = np.mean(bef_v) if bef_v else 0
                am = np.mean(aft_v) if aft_v else 0
                base = (bm + am) / 2
                ratio = gm / max(base, 0.1)
                results[g['name']] = ('confirmed' if ratio < 0.7 else 'not detected',
                                      f'SSN: gsm={gm:.0f}, base={base:.0f}, r={ratio:.2f}')
            else:
                results[g['name']] = ('no data', 'insufficient SILSO')
        elif pre_tele:
            ic = sum(1 for y in pre_tele if s <= y <= e)
            bc = sum(1 for y in pre_tele if s - m <= y < s)
            ac = sum(1 for y in pre_tele if e < y <= e + m)
            results[g['name']] = _ratio_check(ic, bc, ac)
        else:
            results[g['name']] = ('no data', 'no sunspot files')
    return results


def check_e2():
    """Aurora records from SOL-1 E2."""
    try:
        sys.path.insert(0, str(BASE / "src"))
        from sol1_e2_aurora_fft import AURORA_DATA
        years = np.array([a[0] for a in AURORA_DATA])
    except Exception:
        return {g['name']: ('no data', 'cannot import aurora') for g in GSM}

    results = {}
    for g in GSM:
        s, e, m = g['start'], g['end'], max(g['end'] - g['start'], 40)
        ic = ((years >= s) & (years <= e)).sum()
        bc = ((years >= s - m) & (years < s)).sum()
        ac = ((years > e) & (years <= e + m)).sum()
        dur = e - s
        rate_g = ic / max(dur, 1) * 10
        rate_b = ((bc + ac) / 2) / max(m, 1) * 10
        ratio = rate_g / max(rate_b, 0.01)
        if bc + ac + ic == 0:
            results[g['name']] = ('no data', 'no aurora in window')
        else:
            results[g['name']] = ('confirmed' if ratio < 0.7 else 'not detected',
                                  f'{ic} events, rate_ratio={ratio:.2f}')
    return results


def check_e3():
    """Eclipse corona morphology."""
    csv_path = DATA_DIR / "eclipse_corona.csv"
    if not csv_path.exists():
        return {g['name']: ('no data', 'no corona file') for g in GSM}

    import csv
    eclipses = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            eclipses.append({'year': int(row['year']),
                             'phase': row['corona_phase'].strip()})

    results = {}
    for g in GSM:
        s, e = g['start'], g['end']
        gsm_ec = [ec for ec in eclipses if s <= ec['year'] <= e and ec['phase'] != 'unknown']
        if not gsm_ec:
            results[g['name']] = ('no data', 'no classified eclipses')
        else:
            mins = sum(1 for ec in gsm_ec if ec['phase'] == 'min')
            frac = mins / len(gsm_ec)
            results[g['name']] = ('confirmed' if frac > 0.5 else 'not detected',
                                  f'{mins}/{len(gsm_ec)} min-phase')
    return results


def check_e4():
    """IntCal20 delta-14C (inverted proxy)."""
    path = DATA_DIR / "intcal20.14c"
    if not path.exists():
        return {g['name']: ('no data', 'no intcal20 file') for g in GSM}

    cal_bp, d14c = [], []
    with open(path) as f:
        for line in f:
            if line.startswith('#') or line.startswith('!') or not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) < 5:
                continue
            try:
                cal_bp.append(float(parts[0]))
                d14c.append(float(parts[3]))
            except ValueError:
                continue

    cal_ce = 1950 - np.array(cal_bp)
    d14c = np.array(d14c)
    idx = np.argsort(cal_ce)
    cal_ce, d14c = cal_ce[idx], d14c[idx]

    results = {}
    for g in GSM:
        s, e = g['start'], g['end']
        m = max(e - s, 50)
        gm = (cal_ce >= s) & (cal_ce <= e)
        bm = (cal_ce >= s - m * 2) & (cal_ce < s)
        am = (cal_ce > e) & (cal_ce <= e + m * 2)
        if gm.sum() == 0:
            results[g['name']] = ('no data', 'no C14 points')
            continue
        g_mean = d14c[gm].mean()
        bv = np.concatenate([d14c[bm], d14c[am]])
        b_mean = bv.mean() if len(bv) > 0 else g_mean
        diff = g_mean - b_mean
        results[g['name']] = ('confirmed' if diff > 1.0 else 'not detected',
                              f'Δ14C: gsm={g_mean:.1f}, base={b_mean:.1f}, Δ={diff:+.1f}')
    return results


def check_e5():
    """GISP2 Be10 (inverted proxy)."""
    path = DATA_DIR / "gisp2_be10_raw.txt"
    if not path.exists():
        return {g['name']: ('no data', 'no Be10 file') for g in GSM}

    ages_bp, be10 = [], []
    in_data = False
    with open(path) as f:
        for line in f:
            s = line.strip()
            if 'depth top' in s.lower():
                in_data = True
                continue
            if not in_data or not s:
                continue
            parts = s.split()
            if len(parts) < 6:
                continue
            try:
                val = float(parts[2])
                at = float(parts[4])
                ab = float(parts[5])
            except (ValueError, IndexError):
                continue
            if val > 900000:
                continue
            ages_bp.append((at + ab) / 2)
            be10.append(val)

    ages_ce = 1950 - np.array(ages_bp)
    be10 = np.array(be10)
    idx = np.argsort(ages_ce)
    ages_ce, be10 = ages_ce[idx], be10[idx]

    results = {}
    for g in GSM:
        s, e = g['start'], g['end']
        m = max(e - s, 50)
        gm = (ages_ce >= s) & (ages_ce <= e)
        bm = (ages_ce >= s - m * 2) & (ages_ce < s)
        am = (ages_ce > e) & (ages_ce <= e + m * 2)
        if gm.sum() == 0:
            results[g['name']] = ('no data', 'no Be10 points')
            continue
        g_mean = be10[gm].mean()
        bv = np.concatenate([be10[bm], be10[am]])
        b_mean = bv.mean() if len(bv) > 0 else g_mean
        ratio = g_mean / max(b_mean, 0.01)
        results[g['name']] = ('confirmed' if ratio > 1.1 else 'not detected',
                              f'Be10: gsm={g_mean:.0f}, base={b_mean:.0f}, r={ratio:.2f}')
    return results


def main():
    print("=" * 65)
    print("  MAU-1: Grand Solar Minima verification (5 GSM × 5 sources)")
    print("=" * 65)

    checks = [
        ('E1', check_e1), ('E2', check_e2), ('E3', check_e3),
        ('E4', check_e4), ('E5', check_e5)
    ]
    evidence = []
    for label, fn in checks:
        try:
            r = fn()
            print(f"  [{label}] done")
        except Exception as ex:
            r = {g['name']: ('no data', str(ex)[:40]) for g in GSM}
            print(f"  [{label}] error: {ex}")
        evidence.append(r)

    # Matrix
    print(f"\n{'GSM':<12}" + "".join(f"{'E'+str(i+1):^12}" for i in range(5)) + " SCORE")
    print("-" * 75)
    scores = {}
    for g in GSM:
        row = f"{g['name']:<12}"
        cc, td = 0, 0
        for ev in evidence:
            st, _ = ev.get(g['name'], ('no data', ''))
            sym = {'confirmed': '✓', 'not detected': '✗', 'no data': '·'}[st]
            row += f"{sym:^12}"
            if st == 'confirmed': cc += 1; td += 1
            elif st == 'not detected': td += 1
        scores[g['name']] = (cc, td)
        row += f" {cc}/{td}"
        print(row)

    tc = sum(s[0] for s in scores.values())
    tt = sum(s[1] for s in scores.values())
    print(f"\nTotal: {tc}/{tt} confirmed ({100*tc/max(tt,1):.0f}%)")

    # Report
    rpt = f"# MAU-1: Grand Solar Minima Verification\n\n**Date:** {datetime.now().isoformat()[:19]}\n\n"
    rpt += "## Matrix\n\n| GSM | Period | E1 | E2 | E3 | E4 | E5 | Score |\n"
    rpt += "|---|---|---|---|---|---|---|---|\n"
    for g in GSM:
        c, t = scores[g['name']]
        cells = []
        for ev in evidence:
            st, _ = ev.get(g['name'], ('no data', ''))
            cells.append({'confirmed': '✓', 'not detected': '✗', 'no data': '·'}[st])
        rpt += f"| {g['name']} | {g['start']}–{g['end']} | " + " | ".join(cells) + f" | {c}/{t} |\n"
    rpt += f"\n**Total: {tc}/{tt} ({100*tc/max(tt,1):.0f}%)**\n\n## Details\n\n"
    for g in GSM:
        rpt += f"### {g['name']} ({g['start']}–{g['end']})\n\n"
        for src, ev in zip(SOURCES, evidence):
            st, detail = ev.get(g['name'], ('no data', ''))
            rpt += f"- **{src}:** {st} — {detail}\n"
        rpt += "\n"

    out = RESULTS_DIR / "mau1_report.md"
    with open(out, 'w') as f:
        f.write(rpt)
    print(f"\nReport: {out}")


if __name__ == '__main__':
    main()
