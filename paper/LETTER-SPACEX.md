# Letter to SpaceX — English version

> Русская версия: [[LETTER-SPACEX-RU]]

Subject: Grand Solar Minimum forecast — quantified radiation risk for Starlink and Mars missions (open data, 55,000 years)

---

Dear SpaceX Radiation & Reliability Engineering Team,

I am writing with specific, quantified data that is directly relevant to two SpaceX operational concerns: Starlink constellation survivability and Mars crew radiation exposure planning.

## The Problem

Our SOL-1 pipeline analyzes 55,000 years of solar activity data from five independent physical proxies (tree rings, ice cores, ancient chronicles, aurora records, eclipse descriptions). The result:

**95.4% probability of a Grand Solar Minimum (GSM) before 2200 CE.**
Median onset: ~2126 CE. 68% CI: 2058–2206. Duration: 22 +/- 10 years.

A GSM is not a theoretical construct — it has happened repeatedly. The last one (Maunder Minimum, 1645–1715) is well-documented. The next one will occur during active Starlink operations and potentially during Mars colonization.

## What Changes During a GSM — Specific Numbers

### 1. Galactic Cosmic Ray (GCR) Flux: +15–30% baseline shift

During a GSM, the heliospheric magnetic field weakens, reducing its shielding against GCR. This is not a transient storm — it is a **decades-long baseline shift**.

- During solar maximum, GCR flux is at its lowest (heliospheric shielding is strongest)
- During a GSM, GCR flux increases by 15–30% above current levels
- **Duration**: 20–60 years continuously

This means every satellite, every astronaut, every Mars-bound crew operates in a permanently elevated radiation environment for decades.

### 2. Starlink: Increased Single-Event Upsets (SEU)

GCR-induced single-event effects (SEE) in satellite electronics scale approximately linearly with flux. A 20% GCR increase means:

- **~20% more bit-flips** in onboard memory and processors
- **Accelerated component degradation** (total ionizing dose accumulates faster)
- **More frequent anomaly events** requiring ground intervention

For context: in February 2022, SpaceX lost **40 of 49 Starlink satellites** launched during a moderate geomagnetic storm (Kp~5) due to increased atmospheric drag from upper atmosphere heating. During a GSM, both GCR-induced electronics degradation and storm-related drag risks change — not as single events, but as a permanent new baseline for the entire constellation's operational lifetime.

The Starlink constellation (currently 6,000+ satellites, planned 42,000) will need radiation-hardened designs optimized for **GSM-era GCR levels**, not current solar maximum levels.

### 3. Mars Missions: Crew Dose Increases

NASA's current Mars mission radiation budget assumes present-day solar modulation. During a GSM:

- **Transit dose** (6 months): increases from ~300 mSv to ~360–400 mSv (+20–30%)
- **Surface dose** (Mars has no magnetic field): increases proportionally
- **Career dose limit** (NASA 600 mSv) reached **faster** — potentially limiting mission duration or requiring additional shielding mass

The first Mars crews (2030s–2040s) may operate during the onset of a GSM. The 39% probability of GSM onset before 2060 is operationally significant for mission architecture decisions being made now.

### 4. Solar Power: Reduced Output

GSM correlates with:
- **2–5% reduction in total solar irradiance** (TSI)
- Affects solar panel efficiency for both Starlink (solar-powered) and Mars surface operations
- Coincides with period of maximum GCR exposure (worst combination)

## What We Provide (All Open)

| Resource | Link |
|----------|------|
| Full dataset + code | github.com/abelbleoworld-blip/astro-dating |
| DOI (permanent archive) | doi.org/10.5281/zenodo.19638005 |
| Scientific paper (LaTeX) | paper/sol1_paper.tex in repo |
| Monte Carlo results (500 realizations) | src/sol1_prediction_detailed.py |
| 7-vector forecast visualization | results/sol1_vector_forecast.png |

The pipeline is reproducible: Python + NumPy + SciPy. Any engineer can verify the results independently.

## Specific Recommendations

1. **Include GSM scenarios in Starlink v3/v4 radiation specs.** Current designs assume solar-cycle-average GCR. GSM shifts the average upward for 20+ years.

2. **Add GSM-onset probability to Mars mission risk matrices.** The 39% P(GSM before 2060) should inform shielding mass budget and crew rotation planning.

3. **Monitor solar cycle progression.** If Cycle 26 (2030s) is significantly weaker than Cycle 25, GSM probability increases substantially. This is a leading indicator SpaceX can track.

4. **Evaluate GCR-hardened electronics ROI.** If GCR baseline shifts +20% for 20 years, the amortized cost of radiation-hardened components may be lower than the replacement/anomaly cost of standard components.

## Comparison with Existing Forecasts

Our prediction (2058–2206, 68% CI) is most consistent with Steinhilber & Beer 2013 (ETH Zurich), who obtained 2090 +/- 30 using cosmogenic isotopes. We use the same methodological foundation but add three independent observational proxies (sunspot records, aurora catalogs, eclipse corona descriptions), bringing the total to five.

Zharkova's 2015 prediction of a Maunder-like minimum in the 2030s appears less likely — Solar Cycle 25 has exceeded her predicted decline.

## About the Author

Alexander A. Dmitriev, Ph.D. — researcher at the Russian National Public Library for Science and Technology (GPNTB Russia), Network Scientific Laboratory (NSL) for Digital Transformation and AI, GPNTB Russia, Moscow. Background in data analysis and computational methods, not astrophysics. The contribution is methodological: assembling five disparate proxy datasets into a single reproducible pipeline. The physics belongs to Finkel, Reimer, Usoskin, Steinhilber, and the other authors whose data we use.

ORCID: 0009-0000-6164-8474

---

This is not a request for funding or partnership. It is a data delivery. The numbers above are derived from public datasets, computed with open-source code, and independently verifiable.

If SpaceX radiation engineering finds this relevant, I am available for technical discussion at a@aadmitrieff.com.

Best regards,
Alexander A. Dmitriev, Ph.D.
GPNTB Russia, Network Scientific Laboratory (NSL)
Moscow, Russia
ORCID: 0009-0000-6164-8474
a@aadmitrieff.com

---

*P.S. The full version of this letter is in Russian — the language of Pushkin and Dostoevsky — and contains additional data: optimal Mars mission radiation window (2029–2037), dual stress scenario (GSM + anthropogenic warming on launch infrastructure), and independent chronological verification across 16 civilizations on 5 continents. See attached.*

---

**Delivery channels for this letter:**

| Channel | Target | Priority | Note |
|---------|--------|----------|------|
| **X (Twitter) — public thread** | @elonmusk, @SpaceX | **Highest** | Thread with key chart + GitHub link. Public = virality + peer review |
| Daniel Baker (CU Boulder LASP) | Bridge to SpaceX via academia | High | Real researcher, publishes on space weather |
| Conferences (AGU, COSPAR) | Starship radiation team | Medium | In-person contact |
