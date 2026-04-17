# SOL-1 E4 Report — Carbon-14 (IntCal20) → Solar Activity Cycles

## Summary
- **Dataset:** IntCal20 (Reimer et al. 2020), 9501 data points
- **Full range:** 55,000 years (53050 BCE — 1950 CE)
- **Holocene subset:** 6401 points (~12,000 years)
- **Resampled:** 600 points at 20-year resolution
- **Detrending:** 2000-year running mean subtracted (removes geomagnetic/ocean trends)

## Method
Delta-14C is **inversely** proportional to solar activity:
- Solar maximum → strong heliospheric magnetic field → fewer cosmic rays → less ¹⁴C produced
- Solar minimum → weak field → more cosmic rays → more ¹⁴C
- Grand Solar Minima (Maunder, Spörer, etc.) produce sustained high Δ¹⁴C peaks

## FFT Results
See plot `sol1_e4_c14_fft.png` for full spectrum.

### Target Cycles
| Cycle | Expected Period | Status |
|-------|----------------|--------|
| Schwabe | ~11 yr | Below Nyquist (20yr step) — not detectable |
| Hale | ~22 yr | Near Nyquist limit |
| Gleissberg | ~88 yr | **Check FFT** |
| Suess/deVries | ~210 yr | **Primary target** |
| Eddy | ~1000 yr | Check FFT |
| Hallstatt | ~2300 yr | **Primary target** |

## Cross-validation with E1-E3
- **Gleissberg ~88yr:** E1 ✓, E2 ✓, E3 ✓ → E4 check
- **Suess ~210yr:** E2 ✓ (210), E3 ✓ (178) → E4 check
- **Hallstatt ~2300yr:** only detectable in C14/Be10 (new in E4)

## Grand Solar Minima Detection
Known GSMs checked against Δ¹⁴C anomalies (see output).

## Next: E5 Beryllium-10 (GISP2) — independent cross-validation
