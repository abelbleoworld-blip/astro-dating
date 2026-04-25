# Astro-Dating — Computational Archaeoastronomy & Solar Prediction

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19638005.svg)](https://doi.org/10.5281/zenodo.19638005)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--6164--8474-green.svg)](https://orcid.org/0009-0000-6164-8474)

**16 civilizations. 5 continents. 55,000 years of data. 60 Python scripts. All open source.**

Independent verification of historical chronology through astronomical calculations, and a probabilistic forecast of the next Grand Solar Minimum using multi-proxy spectral analysis.

---

## Key Results

### SOL-1: Grand Solar Minimum Forecast

Five independent solar activity proxies spanning 55,000 years converge on a consistent prediction:

| Parameter | Value |
|-----------|-------|
| **Median next GSM** | **~2126 CE** |
| 68% CI | 2058–2206 CE |
| P(Deep + Grand Minimum) | **95.4%** |
| P(nothing significant) | **0.0%** |
| Gleissberg cycle (~88 yr) | confirmed in **4/4 proxies** |
| Be10 x C14 correlation | r = 0.47 (37,000 yr overlap) |

Most consistent with Steinhilber & Beer 2013 (2090 +/- 30), but using 5 proxies instead of 2.

### Almagest Dating

The star catalog of Ptolemy's Almagest dated to **~120 BCE** (Hipparchus epoch) via proper motion analysis of 1,022 stars. Morozov's hypothesis (+800 CE) statistically excluded. Confirms Dambis & Efremov (2000).

### 16 Civilizations Verified

| # | Civilization | Key Finding |
|---|-------------|-------------|
| 1 | Babylon | Bur-Sagale eclipse 763 BCE: separation 0.028 deg |
| 2 | Egypt | Decans ~2100 BCE; Sothic cycle chain verified |
| 3 | India | Shatapatha ~3000 BCE; Aryabhatiya orbital errors <0.5% |
| 4 | Greece/Rome | Almagest 1,022 stars: Hipparchus epoch confirmed |
| 5 | China | SN 1054 Crab Nebula: 6 cultures + HST confirmation |
| 6 | Maya | Dresden Codex: Venus 583.92 days (0.02% error) |
| 7 | Paleolithic | Lascaux, Gobekli Tepe, Lebombo: consistent, not proven |
| 8 | Korea | Star map precession: Goguryeo era (I-IV CE), not 1395 |
| 9 | Aboriginal Australia | Dark constellations converge with Inca (zero contact!) |
| 10 | Khmer Empire | Angkor Wat: precessional numbers 72/108/54 encoded |
| 11 | Dogon (Mali) | Sirius B: **DEBUNKED** (m=8.44, 20th-century contamination) |
| 12 | Aztec | Venus 584d (0.02% error), 5/6 params identical to Maya |
| 13 | Inca | 328 huacas = sidereal lunar year (0.03% error) |
| 14 | Arab-Persian | Al-Sufi: 1,094-year precession chain, error <1 deg |
| 15 | Vietnam | 11/15 events verified (73%), Halley's Comet 5/5 |
| 16 | Japan | SN 1054, SN 1181 / Pa 30 confirmed |

**Overall verification rate: >80%. Traditional chronology confirmed at every tested point.**

### Five Frontier Problems

| Problem | Result |
|---------|--------|
| Red Sirius | 12 historical descriptions, transition IV-VII CE |
| Ugarit eclipse | **~1190 BCE** (neither 1223 nor 1178 confirmed) |
| Miyake events | 3/4 superflares detected in IntCal20 |
| SN 1181 / Pa 30 | Kinematic age consistent with chronicle date |
| Pleiades and ENSO | Inca method confirmed (Nature 2000, Orlove et al.) |

---

## Data Sources

| Proxy | Records | Timespan | Reference |
|-------|---------|----------|-----------|
| E1: Sunspots (naked-eye) | 112 | 28 BCE - 1610 CE | Yau & Stephenson 1988 |
| E2: Aurora catalog | ~2,000 | 567-1900 CE | Silverman 1992, Keimatsu 1970 |
| E3: Eclipse corona morphology | 116 | 71-2024 CE | Stephenson 1997 |
| E4: Radiocarbon (IntCal20) | 9,501 | 55,000 years | Reimer et al. 2020 |
| E5: Be-10 (GISP2 ice core) | 387 | 40,000 years | Finkel & Nishiizumi 1997 |
| Star catalogs | 1,022+ | Hipparchus to Gaia | Toomer 1984, ESA 1997/2022 |
| Halley's Comet | 30 returns | 240 BCE - 1986 CE | Orbital calculation |

---

## Quick Start

```bash
git clone https://github.com/abelbleoworld-blip/astro-dating.git
cd astro-dating
pip install numpy scipy matplotlib astropy

# SOL-1 pipeline (solar activity prediction)
python src/sol1_e1_verify_fft.py       # Sunspots FFT
python src/sol1_e2_aurora_fft.py       # Aurora FFT
python src/sol1_e3_corona_fft.py       # Eclipse corona FFT
python src/sol1_e4_c14_fft.py          # Carbon-14 FFT
python src/sol1_e5_be10_fft.py         # Beryllium-10 FFT
python src/sol1_prediction.py          # Monte Carlo forecast
python src/sol1_vector_forecast.py     # 7-vector forecast

# Almagest dating
python src/almagest_date.py            # 15 stars, RMS by epoch
python src/almagest_1022.py            # Full catalog (1,022 stars)
python src/almagest_1022_gaia.py       # With Gaia DR3 proper motions
```

All data is public. All results are reproducible on any laptop in under 1 minute.

---

## Project Structure

```
astro-dating/
├── paper/          # Publication package (LaTeX, PDF, letters, audio)
├── src/            # 60 Python scripts
│   ├── sol1_*      # SOL-1 solar prediction pipeline (9 scripts)
│   ├── almagest_*  # Star catalog dating (3 scripts)
│   ├── f[1-5]_*    # 5 frontier problems
│   ├── g[1-6]_*    # Supplementary analyses
│   ├── h[1-5]_*    # Hermetic/Egyptian tradition
│   ├── i[6-10]_*   # Indian astronomy
│   ├── k[1-7]_*    # K-series (Korea, Aboriginal, Khmer, Dogon, Aztec, Inca, Arab)
│   ├── v1_*        # Vietnam chronology
│   └── p[1-4]_*    # Paleolithic astronomy
├── results/        # Visualizations + reports (80+ files)
├── data/           # Source data (IntCal20, GISP2, Almagest OCR 672 pages)
├── docs/           # 8 scientific reports + book chapters + education plans
├── audiobook/      # Full audiobook "Chronostars" (7 chapters, 153 MB mastered)
├── book/           # PDF + EPUB (Russian + English)
├── site/           # Website in 8 languages
└── release/        # Release PDFs + presentations
```

---

## Publication Package

| Item | Format | Status |
|------|--------|--------|
| Scientific paper (RevTeX4-2, 6 pages) | LaTeX / PDF | Ready |
| arXiv submission package | .tar.gz | Ready |
| Audiobook (7 chapters + full mastered) | MP3 (153 MB) | Ready |
| Book "Chronostars: The Sky Remembers" | PDF + EPUB (RU + EN) | Ready |
| 8 lectures (5 min each) | PDF | Ready |
| Website | 8 languages | Deployed |
| Letters to experts | Markdown | Ready |
| Viral Pack (Twitter, Telegram, Reddit) | Markdown | Ready |
| Business card with QR | PDF HD + PNG | Ready |

---

## Why It Matters

A Grand Solar Minimum won't cancel global warming — it will **combine** with it. The result is not cooling or warming, but **instability**: extreme winters next to extreme summers, 15-30% crop yield reduction, 15-30% increase in cosmic radiation affecting satellites, aviation, and astronaut safety.

The preparation window is 25-50 years. That's enough — if we start now.

---

## Citation

```bibtex
@misc{dmitriev2026sol1,
  author = {Dmitriev, Alexander A.},
  title = {AI-driven multi-proxy predictive system for solar activity
           over 55,000 years and probabilistic forecast of the next
           Grand Solar Minimum},
  year = {2026},
  doi = {10.5281/zenodo.19638005},
  url = {https://github.com/abelbleoworld-blip/astro-dating}
}
```

## Author

**Alexander A. Dmitriev, Ph.D.**
Russian National Public Library for Science and Technology (GPNTB Russia)
Network Scientific Laboratory (NSL) for Digital Transformation and AI, GPNTB Russia, Moscow, Russia

- ORCID: [0009-0000-6164-8474](https://orcid.org/0009-0000-6164-8474)
- DOI: [10.5281/zenodo.19638005](https://doi.org/10.5281/zenodo.19638005)
- Contact: a@aadmitrieff.com

## License

CC BY 4.0 — free to use with attribution.

---

*We're not asking you to believe us. We're asking you to check.*
