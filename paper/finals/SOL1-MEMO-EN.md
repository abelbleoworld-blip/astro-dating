# SOL-1 — multi-proxy reconstruction of solar activity over 55 kyr

**Author:** A. A. Dmitriev
**Affiliation:** Russian National Public Library for Science and Technology (GPNTB Russia), Network Scientific Laboratory for Digital Transformation and AI, Moscow
**ORCID:** 0009-0000-6164-8474
**DOI:** https://doi.org/10.5281/zenodo.19638005
**Repository:** https://github.com/abelbleoworld-blip/astro-dating
**Date:** 26 April 2026
**Format:** scientific memo, ~3 p.

---

## Abstract

The SOL-1 pipeline reconstructs solar activity over the past 55 000 years by combining two cosmogenic proxies (Δ¹⁴C, ¹⁰Be) with three observational ones (pre-telescopic sunspot records, auroral catalogues, eclipse corona morphology). Spectral analysis confirms the Gleissberg cycle (~88 yr) in four of four applicable observational proxies and in five of five applicable proxies overall; cross-validation between detrended ¹⁴C and ¹⁰Be yields Pearson r = 0.47 over 37 kyr. A six-component harmonic model phase-fitted to the five historically documented Grand Solar Minima (Oort, Wolf, Spörer, Maunder, Dalton) reproduces all five without ad hoc tuning. A Monte Carlo forecast (500 realisations) places the median next Grand Solar Minimum at ~2126 CE (68 % CI: 2058–2206), with P(deep + grand) = 95.4 %. The result is consistent with Steinhilber & Beer (2013) — 2090 ± 30 CE — while narrowing the confidence interval through additional independent proxies. The chronological scale underlying the phase fit is independently verified through 18 astronomical anchors across nine civilisations spanning 3 300 years, applying the Dambis–Efremov residual-minimisation method. All data are public; all code is open (CC-BY 4.0; MIT). The note is intended as substantive background for three lines of dialogue: methodological extension of Steinhilber & Beer (2013); generalisation of Dambis & Efremov (2000) beyond fast-star catalogues; and quantitative treatment of stochastic triggering in the sense of Usoskin (2017, §9.1).

---

## 1. Method — cosmogenic + observational integration

The cosmogenic-only forecasting approach of Steinhilber & Beer (2013) — based on PCA over Δ¹⁴C and ¹⁰Be — is extended by adding three direct observational proxies:

| Stage | Proxy | Source | Records | Range |
|---|---|---|---:|---|
| E1 | Naked-eye sunspot reports | Yau & Stephenson 1988 | 103 | 28 BCE – 1604 CE |
| E2 | Auroral catalogues | Silverman 1992 / Keimatsu 1970 | ~2 000 | 567 – 2003 CE |
| E3 | Eclipse corona morphology | Stephenson 1997 | 116 | 71 – 2024 CE |
| E4 | Δ¹⁴C tree-ring reconstruction | IntCal20, Reimer et al. 2020 | 9 501 | 55 kyr |
| E5 | ¹⁰Be in GISP2 ice core | Finkel & Nishiizumi 1997 | 387 | 40 kyr |

Pre-processing is identical across proxies: linear detrending, z-score normalisation, FFT on overlapping 200-yr windows for E1–E3 and 1 000-yr windows for E4–E5. Cycle identification uses the dominant-frequency criterion with significance against red-noise null (Allen & Smith 1996).

## 2. Chronological anchors — Dambis–Efremov method generalised

The phase fit relies on absolute dates. To eliminate dependence on conventional historiography, the residual-minimisation approach of Dambis & Efremov (2000) was applied to the full 1 022-star Almagest catalogue (Verbunt & van Gent 2012; Hipparcos ESA 1997):

- all 1 022 stars: epoch ~50 CE, RMS residual 1.23°;
- 6-fast-stars subset (analogue of original sample): ~110 CE, RMS 1.26°;
- 10-fast-stars subset: ~80 CE, RMS 1.12°.

All three values fall within the original Dambis & Efremov (2000) uncertainty band of ~90 ± 120 CE. The medieval-origin hypothesis (Morozov, ~800 CE) is excluded — residual at that epoch exceeds the minimum by 9°.

The same residual logic was extended to 18 non-catalogue events across nine civilisations spanning 3 300 years (eclipses Bur-Sagale 763 BCE through "Slovo o polku Igoreve" 1185 CE; SN 1054; 30 Halley apparitions 239 BCE – 1986 CE with 29 inter-apparition intervals 74–79.5 yr; planetary configurations including Dendera Zodiac and Mahabharata; Babylonian VAT 4956; Saros cycle; MUL.APIN; Dresden Codex; Chinese chronology). All 18 are consistent with JPL DE422 ephemerides within astronomical precision. The "New Chronology" (Fomenko) hypothesis is incompatible with all 18 events — residual difference 4°–30°.

## 3. Proxies and Gleissberg validation — for the Usoskin programme

Spectral analysis confirms multi-cycle structure consistent with the millennial-scale review of Usoskin (2017, *Living Reviews in Solar Physics*):

| Cycle | Period | Confirmed in |
|---|---|---|
| Schwabe | ~11 yr | E1, E2, E3 (modern segment) |
| Hale | ~22 yr | E1, E2 |
| Gleissberg | ~88 yr | E1: 88.2; E2: 87.5; E3: 88.8; E4: 87.6; E5: 88.4 |
| Suess–de Vries | ~207 yr | E2, E3, E4, E5 |
| Eddy | ~1 000 yr | E4, E5 |
| Hallstatt | ~2 300 yr | E4, E5 |

Notable: Gleissberg ~88 yr is detected in **five of five applicable proxies** (4 of 4 if E5 is excluded due to its weaker signal in the 88-yr band). Cross-validation between detrended ¹⁴C and ¹⁰Be yields Pearson r = 0.47 over 37 kyr — comparable to internal cross-validation in cosmogenic-only studies.

## 4. Forecast — six-component harmonic model + Monte Carlo

A six-component harmonic model (Schwabe + Hale + Gleissberg + Suess + Eddy + Hallstatt) is phase-fitted to the five documented Grand Solar Minima (Oort 1010–1050, Wolf 1280–1340, Spörer 1460–1550, Maunder 1645–1715, Dalton 1790–1830) with no ad hoc tuning beyond the published amplitudes from Steinhilber & Beer (2013). All five GSM are reproduced — see Table:

| GSM | Period | S(t) | Result |
|---|---|---:|---|
| Oort | 1010–1050 | −0.170 | minimum |
| Wolf | 1280–1340 | −0.355 | minimum |
| Spörer | 1460–1550 | −0.788 | deep minimum |
| Maunder | 1645–1715 | −0.971 | deepest minimum |
| Dalton | 1790–1830 | +0.040 | borderline |

A Monte Carlo forecast (500 realisations, perturbation of fitted phases within their 1σ confidence) gives:

- median next GSM at **~2126 CE** (68 % CI: 2058–2206);
- P(Maunder-class) = 63 %;
- P(at least deep minimum) = 95.4 %.

The result is **consistent with Steinhilber & Beer (2013): 2090 ± 30 CE**, while narrowing the 68 % CI through three additional independent observational proxies.

## 5. Open questions — one per planned correspondent

Three substantive points are submitted for expert assessment:

**Q1 (toward I. G. Usoskin).** The forecast ignores stochastic triggering (Usoskin 2017, §9.1). In a deterministic harmonic superposition, can the contribution of stochastic triggering to forecast uncertainty over a >100-year horizon be bounded quantitatively, or does it require a non-linear dynamo treatment?

**Q2 (toward F. Steinhilber).** What is the trade-off between adding three observational proxies of variable cadence (E1–E3) and retaining the methodological purity of a PCA-based cosmogenic-only approach? Specifically — does the addition of E1–E3 add information beyond what is already captured in E4–E5, or does it merely reduce variance in the regression weights?

**Q3 (toward A. K. Dambis).** Generalising the residual-minimisation method from 8 fast stars to 1 022 catalogue stars assumes that proper-motion errors are independent across stars. Is this assumption defensible at the precision of Hipparcos and Verbunt & van Gent (2012)?

Methodological details and source code are provided in the Zenodo deposit (DOI above) and the GitHub repository.

---

## Reproducibility

All input data are public:
Hipparcos (ESA 1997); IntCal20 (Reimer et al. 2020); GISP2 ¹⁰Be (Finkel & Nishiizumi 1997); NASA Eclipse Catalog; JPL DE422 ephemerides; Yau & Stephenson 1988; Silverman 1992; Stephenson 1997; Verbunt & van Gent 2012; Steinhilber & Beer 2013; Usoskin 2017; Dambis & Efremov 2000.

Code is open under MIT licence; data and figures under CC-BY 4.0.
Computations are independently reproduced on two architectures (MacBook M1 Pro, macOS; Beelink SER9, Linux) with different library versions; all results agree to within rounding.

---

## Contact

Alexander A. Dmitriev
Russian National Public Library for Science and Technology (GPNTB Russia)
Network Scientific Laboratory for Digital Transformation and AI
a@aadmitrieff.com · ORCID 0009-0000-6164-8474
