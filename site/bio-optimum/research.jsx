/* global React, METRICS, COUNTRIES, TIERS, RESEARCH, getCurrentTier, setCurrentTier, canAccess, fetchResearch, renderMarkdown, TIER_RANK */
const { useState: useStateR, useEffect: useEffectR, useMemo: useMemoR } = React;

// ---------- Account chip (in topbar) ----------
window.AccountChip = function AccountChip({ tier, onClick }) {
  const t = TIERS.find(x => x.id === tier) || TIERS[0];
  return (
    <button className={"account-chip " + tier} onClick={onClick}>
      <span className="dot" />
      <span>Тариф: {t.name}</span>
    </button>
  );
};

// ---------- Research card ----------
function ResearchCard({ r, userTier, onOpen }) {
  const locked = !canAccess(r.tier, userTier);
  const tierObj = TIERS.find(t => t.id === r.tier);
  return (
    <div className={"r-card" + (locked ? " locked" : "")} onClick={() => onOpen(r)}>
      <div className="r-meta">
        <span>{r.region} · {r.minutes} мин</span>
        <span className={"r-tier " + r.tier}>{tierObj?.name || r.tier}</span>
      </div>
      <h3>{r.title}</h3>
      <div className="r-sum">{r.summary}</div>
      <div className="r-foot">
        <div className="r-tags">
          {r.tags.slice(0, 3).map(t => <span key={t} className="r-tag">#{t}</span>)}
        </div>
        <span>{r.date.slice(0, 7)}</span>
      </div>
    </div>
  );
}

// ---------- Reader (markdown viewer + paywall) ----------
function Reader({ slug, userTier, onClose, onUpgrade }) {
  const [content, setContent] = useStateR(null);
  const [loading, setLoading] = useStateR(true);

  useEffectR(() => {
    setLoading(true);
    fetchResearch(slug).then(r => {
      setContent(r);
      setLoading(false);
    });
  }, [slug]);

  useEffectR(() => {
    const onEsc = (e) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onEsc);
    return () => document.removeEventListener("keydown", onEsc);
  }, [onClose]);

  if (loading || !content) {
    return (
      <div className="reader-overlay" onClick={onClose}>
        <div className="reader" onClick={e => e.stopPropagation()}>
          <div className="reader-loading">Загрузка из API…</div>
        </div>
      </div>
    );
  }

  const locked = !canAccess(content.tier, userTier);
  // Free preview: show first ~30% of markdown
  let displayMd = content.md;
  if (locked) {
    const lines = content.md.split("\n");
    const cutoff = Math.max(8, Math.floor(lines.length * 0.3));
    displayMd = lines.slice(0, cutoff).join("\n");
  }

  const tierObj = TIERS.find(t => t.id === content.tier);
  const pwClass = content.tier === "plus" ? "" : (content.tier === "pro" ? "warm" : "gold");

  return (
    <div className="reader-overlay" onClick={onClose}>
      <div className="reader" onClick={e => e.stopPropagation()}>
        <button className="reader-close" onClick={onClose} aria-label="Закрыть">✕</button>
        <div className="reader-head">
          <div className="r-meta">
            <span>{content.region}</span>
            <span>·</span>
            <span>{content.minutes} мин чтения</span>
            <span>·</span>
            <span>{content.date}</span>
            <span style={{ marginLeft: "auto" }} className={"r-tier " + content.tier}>{tierObj?.name}</span>
          </div>
          <h1>{content.title}</h1>
          <div className="author">{content.author || "Bio-Optimum Research"}</div>
        </div>
        <div className="reader-body">
          <div dangerouslySetInnerHTML={{ __html: renderMarkdown(displayMd) }} />
          {locked && (
            <div className={"paywall " + pwClass}>
              <div className="lock-ico">🔒</div>
              <h4>Доступно на тарифе {tierObj?.name}</h4>
              <p>{tierObj?.desc} Это исследование — {content.minutes} минут чтения, {content.tags.join(", ")}.</p>
              <button className="pw-cta" onClick={() => { onUpgrade(content.tier); }}>
                Оформить за {tierObj?.price.toLocaleString("ru-RU")} ₽ {tierObj?.period}
              </button>
              <button className="pw-skip" onClick={onClose}>Вернуться к каталогу</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ---------- Pricing tiers ----------
function Pricing({ userTier, onChoose }) {
  const tiers = window.useTiers ? window.useTiers() : window.TIERS;
  return (
    <div className="pricing">
      <h3>Подписка</h3>
      <div className="lead">Доступ к информационным пакетам · API · BOI 2.0 · оплата в ₽</div>
      <div className="pricing-grid">
        {tiers.map(t => {
          const isCurrent = t.id === userTier;
          return (
            <div key={t.id} className={"tier" + (t.popular ? " popular" : "") + (isCurrent ? " current" : "")} onClick={() => !isCurrent && onChoose(t.id)}>
              {t.popular && !isCurrent && <div className="badge">Рекомендуем</div>}
              {isCurrent && <div className="badge cur">Ваш план</div>}
              <div className="t-name">{t.name}</div>
              <div className="t-price">
                {t.price === 0 ? "0 ₽" : t.price.toLocaleString("ru-RU") + " ₽"}
                <small>{t.period}</small>
              </div>
              <div className="t-desc">{t.desc}</div>
              <ul className="t-perks">
                {t.perks.map((p, i) => <li key={i}>{p}</li>)}
              </ul>
              <button className="t-cta" disabled={isCurrent} onClick={e => { e.stopPropagation(); !isCurrent && onChoose(t.id); }}>
                {isCurrent ? "✓ Активирован" : (t.price === 0 ? "Использовать Free" : "Оплатить " + t.price.toLocaleString("ru-RU") + " ₽")}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ---------- Research Hub page ----------
window.ResearchHub = function ResearchHub({ userTier, onOpen, onChooseTier }) {
  const [filterTier, setFilterTier] = useStateR("all");
  const [filterRegion, setFilterRegion] = useStateR("all");
  const [query, setQuery] = useStateR("");

  const regions = useMemoR(() => {
    const set = new Set(RESEARCH.map(r => r.region));
    return ["all", ...set];
  }, []);

  const filtered = useMemoR(() => {
    let arr = RESEARCH;
    if (filterTier !== "all") arr = arr.filter(r => r.tier === filterTier);
    if (filterRegion !== "all") arr = arr.filter(r => r.region === filterRegion);
    if (query) {
      const q = query.toLowerCase();
      arr = arr.filter(r =>
        r.title.toLowerCase().includes(q) ||
        r.summary.toLowerCase().includes(q) ||
        r.tags.some(t => t.toLowerCase().includes(q))
      );
    }
    return arr;
  }, [filterTier, filterRegion, query]);

  const totalsByTier = useMemoR(() => {
    const m = { free: 0, plus: 0, pro: 0, inst: 0 };
    RESEARCH.forEach(r => m[r.tier]++);
    return m;
  }, []);

  return (
    <div className="research-page">
      <section className="research-section">
        <div className="research-head">
          <div>
            <div className="sub">Том II · Исследования · API-канал</div>
            <h2>Глубже карты:<br/><em>исследования</em>.</h2>
            <p>Каждое исследование тянется по API в формате markdown и оформляется по экономической модели. Бесплатно — открытое ядро. По подписке — детальные региональные срезы, методология, доступ к API.</p>
          </div>
          <div>
            <div className="stat-row" style={{ flexWrap: "wrap", gap: 24 }}>
              <div>Всего публикаций<br/><b>{RESEARCH.length}</b></div>
              <div>Free<br/><b style={{ color: "var(--muted)" }}>{totalsByTier.free}</b></div>
              <div>Plus<br/><b style={{ color: "var(--green)" }}>{totalsByTier.plus}</b></div>
              <div>Pro<br/><b style={{ color: "var(--warm)" }}>{totalsByTier.pro}</b></div>
              <div>Inst.<br/><b style={{ color: "var(--gold)" }}>{totalsByTier.inst}</b></div>
            </div>
          </div>
        </div>

        <div className="research-filters">
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--muted)", marginRight: 4 }}>Тариф:</span>
          {[{ id: "all", n: "Все" }, ...TIERS.map(t => ({ id: t.id, n: t.name }))].map(t => (
            <button key={t.id} className={"chip" + (filterTier === t.id ? " active" : "")} onClick={() => setFilterTier(t.id)}>{t.n}</button>
          ))}
          <div className="sep" />
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--muted)", marginRight: 4 }}>Регион:</span>
          {regions.slice(0, 6).map(r => (
            <button key={r} className={"chip" + (filterRegion === r ? " active" : "")} onClick={() => setFilterRegion(r)}>{r === "all" ? "Все" : r}</button>
          ))}
          <div style={{ marginLeft: "auto" }}>
            <div className="search-box" style={{ width: 200 }}>
              <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="7" cy="7" r="5" />
                <path d="M11 11l3 3" />
              </svg>
              <input placeholder="Поиск по тегам..." value={query} onChange={e => setQuery(e.target.value)} />
            </div>
          </div>
        </div>

        <div className="research-grid">
          {filtered.map(r => (
            <ResearchCard key={r.id} r={r} userTier={userTier} onOpen={onOpen} />
          ))}
          {filtered.length === 0 && (
            <div style={{ gridColumn: "1 / -1", padding: 60, textAlign: "center", fontFamily: "var(--font-mono)", fontSize: 12, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--muted)", border: "1px dashed var(--line)", borderRadius: 4 }}>
              ▽ По фильтрам ничего не найдено
            </div>
          )}
        </div>

        <Pricing userTier={userTier} onChoose={onChooseTier} />
      </section>
    </div>
  );
};

window.Reader = Reader;
