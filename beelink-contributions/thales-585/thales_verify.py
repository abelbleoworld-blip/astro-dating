#!/usr/bin/env python3
"""
thales_verify.py — Independent astronomical verification of the Eclipse of Thales (585 BCE)
Uses astropy to compute Sun-Moon angular separation for historical dates.

BCE dates use astronomical year numbering: 585 BCE = year -584, 609 BCE = year -608, etc.
Julian proleptic calendar dates are converted via Julian Day Number.
"""
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

from astropy.coordinates import EarthLocation, AltAz, get_body, get_sun
from astropy.time import Time
import astropy.units as u
import numpy as np


def julian_cal_to_jd(y, m, d):
    """Convert Julian calendar date to Julian Day Number.
    Works for negative years (astronomical numbering)."""
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    jdn = d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083
    return float(jdn)


def parse_iso_bce(date_str):
    """Parse ISO-style date like '-584-05-28' into (year, month, day)."""
    parts = date_str.strip().split("-")
    if date_str.startswith("-"):
        # Negative year
        year = -int(parts[1])
        month = int(parts[2])
        day = int(parts[3])
    else:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    return year, month, day


def compute_eclipse_params(year, month, day, lat, lon, label=""):
    """Compute Sun-Moon separation, altitude, and approximate magnitude
    for a given Julian calendar date at a given location."""
    base_jd = julian_cal_to_jd(year, month, day)
    observer = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=0 * u.m)

    best_sep = 999.0
    best_hour = 12
    best_sun_alt = 0.0
    best_moon_alt = 0.0

    # Scan each half-hour from 6 to 19 UTC
    for half_h in range(12, 38):  # 6.0 to 19.0 in 0.5 steps
        hour = half_h / 2.0
        t = Time(base_jd - 0.5 + hour / 24.0, format="jd", scale="utc")

        frame = AltAz(obstime=t, location=observer)
        sun_aa = get_body("sun", t, observer).transform_to(frame)
        moon_aa = get_body("moon", t, observer).transform_to(frame)

        sep = float(sun_aa.separation(moon_aa).degree)
        sun_alt = float(sun_aa.alt.degree)

        if sep < best_sep and sun_alt > 0:  # Only consider daylight hours
            best_sep = sep
            best_hour = hour
            best_sun_alt = sun_alt
            best_moon_alt = float(moon_aa.alt.degree)

    # Approximate magnitude: solar radius ~ 0.267°, lunar ~ 0.259°
    # If separation < solar_radius + lunar_radius, partial eclipse
    sun_r = 0.267
    moon_r = 0.259
    total_r = sun_r + moon_r

    if best_sep < total_r:
        # Approximate obscuration magnitude
        if best_sep <= abs(sun_r - moon_r):
            magnitude = 1.0  # Total or annular
        else:
            magnitude = round((total_r - best_sep) / (2 * sun_r), 3)
    else:
        magnitude = 0.0

    bce_year = abs(year) + 1 if year <= 0 else year
    greg_date = Time(base_jd, format="jd", scale="utc").iso[:10]

    return {
        "label": label,
        "julian_date": f"{bce_year} BCE {month:02d}-{day:02d}" if year <= 0 else f"{year} CE {month:02d}-{day:02d}",
        "astro_year": year,
        "gregorian_equiv": greg_date,
        "separation_deg": round(best_sep, 4),
        "magnitude": magnitude,
        "best_hour_utc": best_hour,
        "sun_altitude_deg": round(best_sun_alt, 1),
        "eclipse_possible": best_sep < total_r,
        "eclipse_type": (
            "total/annular" if best_sep <= abs(sun_r - moon_r) and best_sep < total_r
            else "partial" if best_sep < total_r
            else "none"
        ),
    }


def saros_check(year, month, day, lat, lon):
    """Check what eclipse occurred ~18 years 11 days before the given date.
    Saros = 6585.32 days ≈ 18 years 11.3 days."""
    base_jd = julian_cal_to_jd(year, month, day)
    saros_jd = base_jd - 6585.32

    # Convert back to find the date
    t_saros = Time(saros_jd, format="jd", scale="utc")

    # Scan a 5-day window around the Saros date
    best = None
    for delta_d in range(-2, 3):
        jd = saros_jd + delta_d
        t = Time(jd, format="jd", scale="utc")
        iso = t.iso[:10]
        parts = iso.split("-")

        # We need Julian calendar year/month/day from JD
        # Reverse conversion from JD to Julian calendar
        b = 0
        c = int(jd + 0.5) + 32082
        d_val = (4 * c + 3) // 1461
        e = c - (1461 * d_val // 4)
        m_val = (5 * e + 2) // 153
        day_j = e - (153 * m_val + 2) // 5 + 1
        month_j = m_val + 3 - 12 * (m_val // 10)
        year_j = d_val - 4800 + m_val // 10

        result = compute_eclipse_params(year_j, month_j, day_j, lat, lon,
                                         label=f"Saros-predecessor ({year_j})")
        if best is None or result["separation_deg"] < best["separation_deg"]:
            best = result

    return best


def main():
    if len(sys.argv) < 2:
        print("usage: thales_verify.py <event.json>")
        sys.exit(1)

    event = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    loc = event["location"]
    lat, lon = loc["lat"], loc["lon"]

    # Primary date
    primary_y, primary_m, primary_d = parse_iso_bce(event["traditional_date_iso"])

    results = []

    # 1. Check primary date: 585 BCE May 28 (Julian)
    r = compute_eclipse_params(primary_y, primary_m, primary_d, lat, lon,
                                label="585 BCE May 28 (traditional)")
    results.append(r)

    # 2. Check alternatives
    for alt_date in event.get("alternatives_to_check", []):
        ay, am, ad = parse_iso_bce(alt_date)
        r = compute_eclipse_params(ay, am, ad, lat, lon, label=f"Alternative {alt_date}")
        results.append(r)

    # 3. Saros predecessor
    saros = saros_check(primary_y, primary_m, primary_d, lat, lon)

    # 4. Check Ionia for Saros predecessor (Miletus: 37.5°N, 27.3°E)
    saros_ionia = None
    if saros:
        base_jd = julian_cal_to_jd(primary_y, primary_m, primary_d)
        saros_jd = base_jd - 6585.32
        # Find the best date from saros check
        # Recompute at Miletus
        c = int(saros_jd + 0.5) + 32082
        d_val = (4 * c + 3) // 1461
        e = c - (1461 * d_val // 4)
        m_val = (5 * e + 2) // 153
        day_j = e - (153 * m_val + 2) // 5 + 1
        month_j = m_val + 3 - 12 * (m_val // 10)
        year_j = d_val - 4800 + m_val // 10
        saros_ionia = compute_eclipse_params(year_j, month_j, day_j, 37.5, 27.3,
                                              label=f"Saros-pred at Miletus ({year_j})")

    output = {
        "event_id": event["id"],
        "traditional_date": event["traditional_date"],
        "primary_result": results[0],
        "alternatives": results[1:],
        "saros_predecessor_anatolia": saros,
        "saros_predecessor_ionia": saros_ionia,
        "best_candidate": min(results, key=lambda x: x["separation_deg"]),
        "verdict": "VERIFIED" if results[0]["eclipse_possible"] else (
            "PARTIAL" if any(r["eclipse_possible"] for r in results) else "REJECTED"
        ),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
