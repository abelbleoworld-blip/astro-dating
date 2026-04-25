/* global React, ReactDOM, METRICS, COUNTRIES, computeBOI */
const { useState, useMemo, useEffect, useRef } = React;

// ---------- helpers ----------
const fmt = (n, d = 2) => Number(n).toFixed(d);

function colorForScore(s) {
  // 5..10 → охра → желтоватый → зелёный
  const t = Math.max(0, Math.min(1, (s - 5.5) / 4));
  // interpolate oklch hand-tuned
  const stops = [
    [184, 92, 42],   // #b85c2a warm
    [176, 138, 62],  // #b08a3e gold
    [120, 130, 70],
    [60, 110, 70],
    [31, 95, 63],    // green
  ];
  const i = t * (stops.length - 1);
  const lo = Math.floor(i), hi = Math.min(stops.length - 1, lo + 1);
  const f = i - lo;
  const c = stops[lo].map((v, k) => Math.round(v + (stops[hi][k] - v) * f));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

// project lat/lon to map coordinates (Robinson-ish simplified)
function project(lat, lon, w, h) {
  const x = (lon + 180) / 360 * w;
  const y = (90 - lat) / 180 * h;
  return { x, y };
}

// ---------- WORLD MAP ----------
function WorldMap({ countries, scores, active, onPick, onHover }) {
  const W = 1100, H = 460;
  // crude world land paths (compact, indicative — not a real atlas)
  // approximate shapes drawn freehand-style
  const continents = [
    // North America blob
    "M 130 90 L 220 80 L 310 90 L 340 130 L 320 180 L 280 210 L 260 250 L 220 270 L 180 250 L 150 200 L 120 150 Z",
    // Central America / Caribbean
    "M 240 250 L 280 270 L 290 300 L 270 320 L 250 305 L 235 280 Z",
    // South America
    "M 290 300 L 340 310 L 360 360 L 350 420 L 320 440 L 300 415 L 285 370 L 280 330 Z",
    // Greenland
    "M 380 60 L 430 55 L 450 90 L 420 110 L 385 95 Z",
    // Europe
    "M 540 120 L 620 110 L 660 130 L 645 165 L 600 175 L 555 165 L 535 145 Z",
    // North Africa
    "M 555 175 L 660 180 L 680 220 L 650 260 L 600 270 L 560 245 L 545 210 Z",
    // Sub-Saharan Africa
    "M 600 270 L 670 275 L 700 320 L 685 380 L 645 410 L 610 395 L 590 350 L 595 305 Z",
    // Middle East
    "M 670 195 L 730 200 L 740 240 L 705 260 L 680 235 Z",
    // Russia / North Asia
    "M 660 90 L 920 85 L 950 130 L 920 155 L 820 165 L 720 145 L 670 125 Z",
    // South Asia
    "M 770 220 L 830 215 L 845 260 L 815 285 L 785 270 L 770 245 Z",
    // SE Asia islands
    "M 870 270 L 920 270 L 940 295 L 905 305 L 875 295 Z",
    // China / East Asia
    "M 830 165 L 920 160 L 945 200 L 915 235 L 870 230 L 840 200 Z",
    // Japan
    "M 950 175 L 970 170 L 985 200 L 970 215 L 955 200 Z",
    // Australia
    "M 880 350 L 960 345 L 980 380 L 955 405 L 905 405 L 880 385 Z",
    // New Zealand
    "M 990 410 L 1010 405 L 1015 430 L 1000 440 L 990 425 Z",
    // Iceland
    "M 510 95 L 530 92 L 535 108 L 520 115 L 508 105 Z",
  ];

  const tropicY = (lat) => (90 - lat) / 180 * H;

  const tip = useRef(null);
  const onMove = (e, c, score) => {
    if (tip.current) {
      tip.current.style.left = e.clientX + 14 + "px";
      tip.current.style.top = e.clientY + 14 + "px";
      tip.current.classList.add("show");
      tip.current.innerHTML = `<b>${c.code}</b>${c.name} · BOI ${fmt(score, 2)}`;
    }
    onHover && onHover(c);
  };
  const onLeave = () => {
    if (tip.current) tip.current.classList.remove("show");
    onHover && onHover(null);
  };

  return (
    <div className="map-wrap">
      <svg viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet">
        {/* graticule */}
        {[-60,-30,0,30,60].map(lat => (
          <line key={"h"+lat} x1={0} y1={tropicY(lat)} x2={W} y2={tropicY(lat)}
            className={lat === 0 ? "map-grat map-equator" : (Math.abs(lat) === 23 ? "map-grat map-tropic" : "map-grat")} />
        ))}
        {[-150,-120,-90,-60,-30,0,30,60,90,120,150].map(lon => (
          <line key={"v"+lon} x1={(lon+180)/360*W} y1={0} x2={(lon+180)/360*W} y2={H} className="map-grat" />
        ))}
        {/* tropics */}
        <line x1={0} y1={tropicY(23.4)} x2={W} y2={tropicY(23.4)} className="map-grat map-tropic" />
        <line x1={0} y1={tropicY(-23.4)} x2={W} y2={tropicY(-23.4)} className="map-grat map-tropic" />

        {/* bio-optimum band 30°–45° N and S */}
        <rect x={0} y={tropicY(45)} width={W} height={tropicY(30) - tropicY(45)} className="map-band" />
        <rect x={0} y={tropicY(-30)} width={W} height={tropicY(-45) - tropicY(-30)} className="map-band" />

        {/* land */}
        {continents.map((d, i) => <path key={i} d={d} className="map-land" />)}

        {/* country dots */}
        {countries.map(c => {
          const { x, y } = project(c.lat, c.lon, W, H);
          const s = scores[c.code];
          const r = 4 + (s - 6) * 1.6;
          const isActive = active === c.code;
          return (
            <g key={c.code} className={"dot-country" + (isActive ? " active" : "")}
               transform={`translate(${x},${y})`}
               onClick={() => onPick(c.code)}
               onMouseMove={(e) => onMove(e, c, s)}
               onMouseLeave={onLeave}>
              <circle r={Math.max(3, r)} fill={colorForScore(s)} stroke="#fbf8f0" strokeWidth="1.5" opacity="0.95" />
              {(isActive || s >= 8.8) && (
                <text y={-r - 4}>{c.code}</text>
              )}
            </g>
          );
        })}
      </svg>

      <div className="map-legend">
        <span>BOI</span>
        <div>
          <div className="scale">
            {[5.5, 6.5, 7.5, 8.5, 9.5].map(v => (
              <span key={v} style={{ background: colorForScore(v) }} />
            ))}
          </div>
          <div className="ends"><span>5.5</span><span>9.5+</span></div>
        </div>
        <span style={{ opacity: .6 }}>·</span>
        <span>30–45° оптимум</span>
      </div>

      <div className="map-info">
        Стран в выборке<br/>
        <b>{countries.length}</b>
      </div>

      <div ref={tip} className="tip" />
    </div>
  );
}

// ---------- WEIGHTS PANEL ----------
function WeightsPanel({ weights, setWeights }) {
  const reset = () => {
    const w = {};
    METRICS.forEach(m => w[m.key] = m.weight);
    setWeights(w);
  };
  const total = METRICS.reduce((s, m) => s + (weights[m.key] || 0), 0);

  return (
    <div className="panel weights-panel">
      <div className="panel-head">
        <div>
          <h2>Калибровка</h2>
          <div className="sub">Что важно именно вам</div>
        </div>
      </div>
      {METRICS.map(m => (
        <div key={m.key} className="weight-row">
          <div className="lbl">
            {m.label}
            <small>{m.short}</small>
          </div>
          <input type="range" min="0" max="0.3" step="0.005"
            value={weights[m.key] ?? m.weight}
            onChange={e => setWeights({ ...weights, [m.key]: parseFloat(e.target.value) })} />
          <div className="v">{((weights[m.key] ?? m.weight) * 100).toFixed(0)}%</div>
        </div>
      ))}
      <div className="weight-actions">
        <button className="btn primary" onClick={reset}>Сбросить</button>
        <div style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--muted)", letterSpacing: ".1em", textTransform: "uppercase", alignSelf: "center" }}>
          Σ {(total * 100).toFixed(0)}%
        </div>
      </div>
    </div>
  );
}

// ---------- RANKING ----------
function Ranking({ rows, sortKey, setSortKey, active, onPick, query, setQuery }) {
  const cols = [
    { k: "rank", l: "#", sortable: false },
    { k: "name", l: "Страна", sortable: true },
    { k: "boi", l: "BOI", sortable: true },
    { k: "climate", l: "CLM", sortable: true },
    { k: "longevity", l: "HAL", sortable: true },
    { k: "air", l: "AIR", sortable: true },
    { k: "uv", l: "UV", sortable: true },
  ];
  return (
    <div className="panel">
      <div className="panel-head">
        <div>
          <h2>Рейтинг</h2>
          <div className="sub">{rows.length} стран · отсортировано по {sortKey === "boi" ? "BOI" : sortKey}</div>
        </div>
        <div className="search-box">
          <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
            <circle cx="7" cy="7" r="5" />
            <path d="M11 11l3 3" />
          </svg>
          <input placeholder="Поиск..." value={query} onChange={e => setQuery(e.target.value)} />
        </div>
      </div>
      <div style={{ maxHeight: 580, overflow: "auto" }}>
        <table className="rank-table">
          <thead>
            <tr>
              {cols.map(c => (
                <th key={c.k} onClick={() => c.sortable && setSortKey(c.k === sortKey ? c.k : c.k)}>
                  {c.l}{sortKey === c.k && <span className="arrow">↓</span>}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={r.code} className={active === r.code ? "active" : ""} onClick={() => onPick(r.code)}>
                <td className={"rk" + (i < 3 ? " top" : "")}>{String(i + 1).padStart(2, "0")}</td>
                <td className="nm" colSpan="1">
                  <span style={{ display: "flex", gap: 10, alignItems: "baseline" }}>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, fontWeight: 700, color: "var(--muted)", letterSpacing: ".06em", width: 22 }}>{r.code}</span>
                    <span>
                      <b>{r.name}</b>
                      <small>{r.anchor}</small>
                    </span>
                  </span>
                </td>
                <td className="bar">
                  <div className="bar-row">
                    <div className="b" style={{ "--w": (r.boi / 10 * 100) + "%" }} />
                    <div className="v">{fmt(r.boi, 2)}</div>
                  </div>
                </td>
                <td className="metric">{fmt(r.climate, 1)}</td>
                <td className="metric">{fmt(r.longevity, 1)}</td>
                <td className="metric">{fmt(r.air, 1)}</td>
                <td className="metric">{fmt(r.uv, 1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ---------- DETAIL ----------
function Radar({ country }) {
  const size = 200, cx = size / 2, cy = size / 2, r = 78;
  const n = METRICS.length;
  const points = METRICS.map((m, i) => {
    const a = (Math.PI * 2 * i) / n - Math.PI / 2;
    const v = (country[m.key] / 10) * r;
    return { x: cx + Math.cos(a) * v, y: cy + Math.sin(a) * v, ax: cx + Math.cos(a) * r, ay: cy + Math.sin(a) * r, lx: cx + Math.cos(a) * (r + 14), ly: cy + Math.sin(a) * (r + 14), short: m.short };
  });
  return (
    <svg viewBox={`0 0 ${size} ${size}`}>
      {[.25, .5, .75, 1].map(t => (
        <polygon key={t} className="radar-grid"
          points={METRICS.map((_, i) => {
            const a = (Math.PI * 2 * i) / n - Math.PI / 2;
            return `${cx + Math.cos(a) * r * t},${cy + Math.sin(a) * r * t}`;
          }).join(" ")} />
      ))}
      {points.map((p, i) => <line key={i} className="radar-axis" x1={cx} y1={cy} x2={p.ax} y2={p.ay} />)}
      <polygon className="radar-shape" points={points.map(p => `${p.x},${p.y}`).join(" ")} />
      {points.map((p, i) => <circle key={i} className="radar-pt" cx={p.x} cy={p.y} r="2.2" />)}
      {points.map((p, i) => (
        <text key={i} className="radar-lbl" x={p.lx} y={p.ly} textAnchor="middle" dominantBaseline="middle">{p.short}</text>
      ))}
    </svg>
  );
}

function CountryDetail({ country, boi, onCompareAdd }) {
  if (!country) {
    return (
      <div className="panel detail-panel">
        <div className="detail-empty">
          ▽ Выберите страну<br/>
          на карте или в рейтинге
        </div>
      </div>
    );
  }
  // strong / weak
  const sorted = [...METRICS].sort((a, b) => country[b.key] - country[a.key]);
  const strong = sorted.slice(0, 2);
  const weak = sorted.slice(-2);

  return (
    <div className="panel detail-panel">
      <div className="detail-head">
        <div className="left">
          <div className="code">{country.code}</div>
          <div>
            <h2>{country.name}</h2>
            <div className="anchor">▸ {country.anchor} · {country.region}</div>
          </div>
        </div>
        <div className="boi">
          <b>{fmt(boi, 2)}</b>
          <span>BOI · из 10</span>
        </div>
      </div>

      <div className="radar-row">
        <div className="radar-wrap"><Radar country={country} /></div>
        <div className="metric-list">
          {METRICS.map(m => {
            const v = country[m.key];
            const isWeak = v < 7;
            return (
              <div key={m.key} className={"row" + (isWeak ? " weak" : "")}>
                <div className="lbl">{m.label}</div>
                <div className="b" style={{ "--w": (v / 10 * 100) + "%" }} />
                <div className="v">{fmt(v, 1)}</div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="detail-footer">
        <div>
          <h4>Сильные стороны</h4>
          <p>
            {strong.map((m, i) => (
              <span key={m.key}>
                <span className="strong">{m.label}</span> ({fmt(country[m.key], 1)}){i < strong.length - 1 ? " · " : ""}
              </span>
            ))}
            <br />
            {country.code === "PT" && "Широта 37°, средиземноморский климат, чистый воздух (PM2.5 ≈ 8), низкий радон."}
            {country.code === "JP" && "«Голубая зона» Окинавы, мировой лидер по HALE — 74 года здоровой жизни."}
            {country.code === "NZ" && "Чистейший воздух планеты (PM2.5 ≈ 5), морской климат, мало индустрии."}
            {country.code === "RU" && "Большая страна, но биооптимум сосредоточен в анклаве: Сочи, ЮБК — отдельный микроклимат."}
            {!["PT","JP","NZ","RU"].includes(country.code) && "Локальный микроклимат и инфраструктура усиливают базовые показатели."}
          </p>
        </div>
        <div>
          <h4>Слабые места</h4>
          <p>
            {weak.map((m, i) => (
              <span key={m.key}>
                <span className="weak">{m.label}</span> ({fmt(country[m.key], 1)}){i < weak.length - 1 ? " · " : ""}
              </span>
            ))}
            <br />
            <button className="btn" style={{ marginTop: 10 }} onClick={() => onCompareAdd(country.code)}>
              + В сравнение
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

// ---------- COMPARE BAR ----------
function CompareBar({ pair, scores, onRemove }) {
  const [a, b] = pair;
  const cA = a && COUNTRIES.find(c => c.code === a);
  const cB = b && COUNTRIES.find(c => c.code === b);
  const Side = ({ c }) => c ? (
    <div className="compare-side">
      <div className="nm">
        <b>{c.name}</b>
        <small>{c.code} · {c.anchor}</small>
      </div>
      <div className="scr">{fmt(scores[c.code], 2)}</div>
      <div className="x" onClick={() => onRemove(c.code)}>✕</div>
    </div>
  ) : (
    <div className="compare-side empty">▽ Выберите страну · кликните «+ В сравнение»</div>
  );
  return (
    <div className="compare-bar">
      <h3>Сравнение
        <small>A vs B по BOI</small>
      </h3>
      <Side c={cA} />
      <Side c={cB} />
    </div>
  );
}

// ---------- INSIGHTS ----------
function Insights({ rows }) {
  const top = rows[0];
  const bottom = rows[rows.length - 1];
  const above = rows.filter(r => r.boi >= 8.5).length;
  const avg = rows.reduce((s, r) => s + r.boi, 0) / rows.length;
  return (
    <div className="insights">
      <div className="insight">
        <div className="l">№1 в выборке</div>
        <div className="v"><em>{top?.name}</em></div>
        <div className="d">BOI {fmt(top?.boi, 2)} · {top?.anchor}</div>
      </div>
      <div className="insight">
        <div className="l">Стран ≥ 8.5</div>
        <div className="v"><em>{above}</em><span style={{ fontSize: 18, color: "var(--muted)" }}> / {rows.length}</span></div>
        <div className="d">узкая полоса биооптимума</div>
      </div>
      <div className="insight">
        <div className="l">Средний BOI</div>
        <div className="v">{fmt(avg, 2)}</div>
        <div className="d">по всей выборке, с учётом ваших весов</div>
      </div>
      <div className="insight">
        <div className="l">№{rows.length} в выборке</div>
        <div className="v warm"><em>{bottom?.name}</em></div>
        <div className="d">BOI {fmt(bottom?.boi, 2)} · слабые: {bottomWeak(bottom)}</div>
      </div>
    </div>
  );
}
function bottomWeak(c) {
  if (!c) return "";
  const sorted = [...METRICS].sort((a, b) => c[a.key] - c[b.key]);
  return sorted.slice(0, 2).map(m => m.short).join(" · ");
}

// ---------- ROOT ----------
function App() {
  const TWEAKS = /*EDITMODE-BEGIN*/{
    "theme": "paper",
    "showBand": true,
    "preset": "default"
  }/*EDITMODE-END*/;

  const [weights, setWeights] = useState(() => {
    const w = {};
    METRICS.forEach(m => w[m.key] = m.weight);
    return w;
  });
  const [active, setActive] = useState("PT");
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState("boi");
  const [pair, setPair] = useState(["PT", null]);
  const [page, setPage] = useState("atlas"); // atlas | research | method | russia
  const [userTier, setUserTier] = useState(() => (typeof window !== "undefined" && window.getCurrentTier) ? window.getCurrentTier() : "free");
  const [readingSlug, setReadingSlug] = useState(null);
  const [adminOpen, setAdminOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [payingTier, setPayingTier] = useState(null);
  const [theme, setTheme] = useState(() => {
    if (typeof window === "undefined") return "light";
    return localStorage.getItem("bo_theme") || "light";
  });

  useEffect(() => {
    document.body.setAttribute("data-theme", theme);
    localStorage.setItem("bo_theme", theme);
  }, [theme]);

  useEffect(() => {
    document.body.classList.toggle("edit-mode", editMode);
    document.body.classList.toggle("edit-mode-on", editMode);
  }, [editMode]);

  useEffect(() => {
    const sync = () => setUserTier(window.getCurrentTier());
    window.addEventListener("bo_tier_changed", sync);
    return () => window.removeEventListener("bo_tier_changed", sync);
  }, []);

  const handleChooseTier = (tierId) => {
    if (tierId === "free") { window.setCurrentTier(tierId); return; }
    setPayingTier(tierId);
  };
  const handleOpenResearch = (r) => setReadingSlug(r.slug);
  const handleCloseReader = () => setReadingSlug(null);

  const AccountChip = window.AccountChip;
  const ResearchHub = window.ResearchHub;
  const Reader = window.Reader;
  const AdminPanel = window.AdminPanel;
  const PaymentModal = window.PaymentModal;

  const scores = useMemo(() => {
    const s = {};
    COUNTRIES.forEach(c => { s[c.code] = computeBOI(c, weights); });
    return s;
  }, [weights]);

  const rows = useMemo(() => {
    let arr = COUNTRIES.map(c => ({ ...c, boi: scores[c.code] }));
    if (query) {
      const q = query.toLowerCase();
      arr = arr.filter(r => r.name.toLowerCase().includes(q) || r.code.toLowerCase().includes(q) || r.anchor.toLowerCase().includes(q));
    }
    arr.sort((a, b) => {
      const va = a[sortKey], vb = b[sortKey];
      if (typeof va === "number") return vb - va;
      return String(va).localeCompare(String(vb));
    });
    return arr;
  }, [scores, query, sortKey]);

  const activeCountry = COUNTRIES.find(c => c.code === active);

  const onCompareAdd = (code) => {
    setPair(p => {
      if (p[0] === code || p[1] === code) return p;
      if (!p[0]) return [code, p[1]];
      if (!p[1]) return [p[0], code];
      return [p[1], code];
    });
  };
  const onCompareRemove = (code) => {
    setPair(p => p.map(x => x === code ? null : x));
  };

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand" style={{ cursor: "pointer" }} onClick={() => setPage("atlas")}>BIO–OPTIMUM <span className="dot">●</span> WORLD INDEX</div>
        <nav>
          <a className={page === "atlas" ? "active" : ""} onClick={() => setPage("atlas")}>Атлас</a>
          <a className={page === "research" ? "active" : ""} onClick={() => setPage("research")}>Исследования</a>
          <a className={page === "method" ? "active" : ""} onClick={() => setPage("method")}>Метод</a>
          <a className={page === "russia" ? "active" : ""} onClick={() => setPage("russia")}>Россия</a>
        </nav>
        <AccountChip tier={userTier} onClick={() => setPage("research")} />
        <button className="theme-toggle" onClick={() => setTheme(theme === "dark" ? "light" : "dark")} title="Сменить тему">
          <span className="icon">
            {theme === "dark" ? (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            )}
          </span>
          {theme === "dark" ? "День" : "Ночь"}
        </button>
        <div className="live">v.2026.04</div>
      </header>

      {page === "atlas" && (<div className="atlas-page">
      <section className="hero">
        <div>
          <div className="kicker">Том I · Атлас живого тела · 2026</div>
          <h1>Где тело <em>дома</em>.<br/>Сорок стран<br/>под одной шкалой.</h1>
        </div>
        <div>
          <p className="lead" style={{ marginBottom: 22 }}>
            Bio-Optimum Index сводит десять параметров — климат, воздух, воду, радиацию, широту, долголетие — в один балл и показывает, где конверт условий человеческого тела сходится одновременно по всем векторам.
          </p>
          <div className="meta-grid">
            <div>Метод<br/><b>BOI · 10 факторов</b></div>
            <div>Источники<br/><b>WHO · NASA · IQAir</b></div>
            <div>Стран<br/><b>40 в выборке</b></div>
            <div>Шкала<br/><b>0 — 10</b></div>
          </div>
        </div>
      </section>

      <Insights rows={rows} />

      <div className="main-grid">
        <div className="panel map-panel">
          <div className="panel-head">
            <div>
              <h2>Атлас</h2>
              <div className="sub">Размер точки = BOI · цвет = интенсивность · полоса 30–45° — оптимум</div>
            </div>
          </div>
          <WorldMap countries={COUNTRIES} scores={scores} active={active} onPick={setActive} />
        </div>
        <WeightsPanel weights={weights} setWeights={setWeights} />
      </div>

      <div className="main-grid">
        <Ranking rows={rows} sortKey={sortKey} setSortKey={setSortKey} active={active} onPick={setActive} query={query} setQuery={setQuery} />
        <CountryDetail country={activeCountry} boi={scores[active]} onCompareAdd={onCompareAdd} />
      </div>

      <CompareBar pair={pair} scores={scores} onRemove={onCompareRemove} />

      <section className="essay">
        <h2>Тело — это <em>конверт</em>.<br/>Карта — это <em>выкройка</em>.</h2>
        <div className="cols">
          <p>Человеческая биохимия настроена под одну планету в очень узкой полосе. Конверт — это диапазон условий, внутри которого клетки работают без стресса: 22 °C средней температуры, 21 кПа парциального кислорода, фоновая радиация ниже 3 мЗв в год, PM2.5 в пределах единиц микрограммов на кубометр.</p>
          <p>Большую часть истории биология определяла, где живут люди. В XX веке — наоборот: инженерия позволила жить в Якутске и в Дубае, в Боготе на 2 600 м и в полярную ночь. Возможно — не значит оптимально. Тело по-прежнему платит налог на каждое отклонение от конверта.</p>
          <p>Этот рейтинг — попытка собрать налог в одну сумму. Не «лучшая страна для жизни» в социальном смысле — а место, где сумма физических векторов меньше всего штрафует биохимию. Веса можно перенастроить под свою биологию: кто-то чувствителен к УФ, кто-то к высоте, кто-то к холодной зиме.</p>
          <p>Полоса 30–45° параллели по обе стороны экватора — это не случайность. Средиземноморский климат, «голубые зоны» долголетия, мягкая зима, баланс УФ и витамина D — всё сходится здесь. Из 40 стран выборки в эту полосу попадают 22. Из них 12 — выше порога 8.5.</p>
        </div>
      </section>

      <footer className="foot">
        <div>BIO-OPTIMUM · WORLD INDEX · TOM I · 2026</div>
        <div>Метод BOI © A. Дмитриев · Данные: WHO 2023 · NASA · IQAir 2024 · IAEA</div>
      </footer>
      </div>)}

      {page === "research" && (
        <ResearchHub
          userTier={userTier}
          onOpen={handleOpenResearch}
          onChooseTier={handleChooseTier}
        />
      )}

      {page === "method" && (
        <div className="research-page" style={{ padding: "60px 0" }}>
          <div style={{ textAlign: "center", marginBottom: 48 }}>
            <div className="sub" style={{ fontFamily: "var(--font-mono)", fontSize: 11, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 14 }}>Том III · Метод</div>
            <h2 style={{ fontFamily: "var(--font-display)", fontSize: 48, fontWeight: 500, letterSpacing: "-.02em", margin: 0 }}>Whitepaper BOI</h2>
            <p style={{ color: "var(--ink-soft)", maxWidth: 520, margin: "16px auto 0" }}>Полная методология Bio-Optimum Index: 10 факторов, источники данных, формулы нормализации, весовые коэффициенты.</p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, maxWidth: 800, margin: "0 auto" }}>
            <div style={{ background: "var(--surface)", border: "1px solid var(--stroke)", borderRadius: 12, padding: 24 }}>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--accent)", marginBottom: 10 }}>Preview</div>
              <h3 style={{ fontFamily: "var(--font-display)", fontSize: 22, fontWeight: 500, margin: "0 0 12px" }}>10 факторов BOI</h3>
              <div style={{ fontSize: 13, color: "var(--ink-soft)", lineHeight: 1.6 }}>
                <p>1. <b>Climate</b> (0.18) — терморегуляция, близость к 22°C</p>
                <p>2. <b>HALE</b> (0.12) — здоровая продолжительность жизни (WHO)</p>
                <p>3. <b>Air Quality</b> (0.12) — PM2.5 (IQAir)</p>
                <p>4. <b>Water</b> (0.10) — доступ к чистой воде</p>
                <p>5. <b>Radiation</b> (0.10) — фоновый уровень (IAEA)</p>
                <p style={{ color: "var(--muted)" }}>6–10: Altitude, Latitude, Stability, UV, Risks...</p>
              </div>
              <p style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--muted)", marginTop: 12 }}>BOI = Σ(factor × weight) · scale 0–10</p>
            </div>
            <div style={{ background: "var(--surface)", border: "1px solid var(--stroke)", borderRadius: 12, padding: 24, position: "relative", overflow: "hidden" }}>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--warm)", marginBottom: 10 }}>Institutional</div>
              <h3 style={{ fontFamily: "var(--font-display)", fontSize: 22, fontWeight: 500, margin: "0 0 12px" }}>Полный Whitepaper</h3>
              <div style={{ fontSize: 13, color: "var(--ink-soft)", lineHeight: 1.6, filter: "blur(3px)" }}>
                <p>Нормализация: min-max с винсоризацией на 5/95 перцентили...</p>
                <p>Confidence scoring: мульти-источник с весом по актуальности...</p>
                <p>API schema: GET /api/bio-optimum?country=PRT&factors=all...</p>
                <p>Regression: коэффициенты R² по каждому фактору...</p>
              </div>
              <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.4)", backdropFilter: "blur(4px)" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--warm)", marginBottom: 8 }}>Institutional Plan</div>
                <button className="btn primary" onClick={() => handleChooseTier("institutional")}>Unlock · $29/mo →</button>
              </div>
            </div>
          </div>

          <div style={{ textAlign: "center", marginTop: 32 }}>
            <button className="btn ghost" onClick={() => setPage("research")} style={{ marginRight: 8 }}>Все исследования</button>
            <a className="btn ghost" href="https://aadmitrieff.com/worldrank.html" style={{ textDecoration: "none" }}>WorldRank Platform →</a>
          </div>
        </div>
      )}

      {page === "russia" && (
        <div className="research-page" style={{ padding: "60px 0" }}>
          <div style={{ textAlign: "center", marginBottom: 48 }}>
            <div className="sub" style={{ fontFamily: "var(--font-mono)", fontSize: 11, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--warm)", marginBottom: 14 }}>Том IV · Россия</div>
            <h2 style={{ fontFamily: "var(--font-display)", fontSize: 48, fontWeight: 500, letterSpacing: "-.02em", margin: 0 }}>Микроклиматические анклавы</h2>
            <p style={{ color: "var(--ink-soft)", maxWidth: 520, margin: "16px auto 0" }}>Шесть регионов с локальным BOI 7.0–7.8: ЮБК, Сочи, КМВ, Калининград, Краснодарский край, Ростов.</p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, maxWidth: 800, margin: "0 auto" }}>
            {[
              { name: "Крым · Ялта", boi: 7.8, strong: "Субтропический, защищён горами", icon: "🏖" },
              { name: "КМВ · Минводы", boi: 7.6, strong: "Минеральные источники", icon: "⛰" },
              { name: "Сочи · Адлер", boi: 7.5, strong: "Побережье, длинное солнце", icon: "🌊" },
              { name: "Краснодар", boi: 7.5, strong: "Плодородие, тёплая зима", icon: "🌾" },
              { name: "Калининград", boi: 7.4, strong: "Морской воздух, мягкая зима", icon: "🌊" },
              { name: "Ростов-на-Дону", boi: 7.3, strong: "2100 ч солнца/год", icon: "☀" },
            ].map((r, i) => (
              <div key={i} style={{ background: "var(--surface)", border: "1px solid var(--stroke)", borderRadius: 12, padding: 20, cursor: "pointer", transition: "border-color .15s, transform .15s" }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = "var(--warm)"; e.currentTarget.style.transform = "translateY(-2px)"; }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = ""; e.currentTarget.style.transform = ""; }}
                onClick={() => setPage("research")}
              >
                <div style={{ fontSize: 28, marginBottom: 8 }}>{r.icon}</div>
                <div style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 500, marginBottom: 4 }}>{r.name}</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 20, fontWeight: 700, color: "var(--accent)", marginBottom: 6 }}>{r.boi}</div>
                <div style={{ fontSize: 12, color: "var(--ink-soft)" }}>{r.strong}</div>
              </div>
            ))}
          </div>

          <div style={{ textAlign: "center", marginTop: 32 }}>
            <button className="btn primary" onClick={() => handleChooseTier("pro")}>Полный отчёт по России →</button>
          </div>
        </div>
      )}

      {readingSlug && (
        <Reader
          slug={readingSlug}
          userTier={userTier}
          onClose={handleCloseReader}
          onUpgrade={(needTier) => { handleCloseReader(); setPayingTier(needTier); }}
        />
      )}

      {payingTier && (
        <PaymentModal
          tierId={payingTier}
          onClose={() => setPayingTier(null)}
          onPaid={() => { window.setCurrentTier(payingTier); setPayingTier(null); }}
        />
      )}

      <button
        className={"admin-fab" + (adminOpen ? " active" : "")}
        onClick={() => setAdminOpen(!adminOpen)}
        title="Режим правки"
      >
        {adminOpen ? "✕" : "✎"}
        {!adminOpen && <span className="pulse" />}
      </button>

      {adminOpen && (
        <AdminPanel
          open={adminOpen}
          onClose={() => setAdminOpen(false)}
          editMode={editMode}
          setEditMode={setEditMode}
        />
      )}

      {editMode && (
        <div className="edit-mode-banner">
          <span className="ind" />
          Режим правки активен · кликайте по элементам с пунктиром
        </div>
      )}
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
