/* global React, TIERS, getAdminData, saveAdminData, isAdminMode, setAdminMode, updateTier, updateCopy, resetAdmin, aiPatch */
const { useState: useStateAd, useEffect: useEffectAd, useRef: useRefAd } = React;

window.AdminPanel = function AdminPanel({ open, onClose, editMode, setEditMode }) {
  const [tab, setTab] = useStateAd("ai");
  const [prompt, setPrompt] = useStateAd("");
  const [busy, setBusy] = useStateAd(false);
  const [result, setResult] = useStateAd(null);
  const [data, setData] = useStateAd(window.getAdminData());

  useEffectAd(() => {
    const sync = () => setData(window.getAdminData());
    window.addEventListener("bo_admin_changed", sync);
    return () => window.removeEventListener("bo_admin_changed", sync);
  }, []);

  if (!open) return null;

  const runAI = async () => {
    if (!prompt.trim()) return;
    setBusy(true);
    setResult(null);
    const r = await window.aiPatch(prompt);
    setResult(r);
    setBusy(false);
    if (r.ok) setPrompt("");
  };

  const presets = [
    "Скидка 20% на plus",
    "Цена pro 39",
    'Переименуй plus в "Standard"',
    "Сброс",
  ];

  const tiers = window.TIERS.map(t => ({ ...t, ...(data.tiers?.[t.id] || {}) }));

  return (
    <div className="admin-panel" onClick={e => e.stopPropagation()}>
      <div className="admin-head">
        <div className="ttl">
          Режим правки
          <span>Admin · Bio-Optimum</span>
        </div>
        <button className="x" onClick={onClose}>✕</button>
      </div>

      <div className="admin-tabs">
        <button className={tab === "ai" ? "active" : ""} onClick={() => setTab("ai")}>AI</button>
        <button className={tab === "tiers" ? "active" : ""} onClick={() => setTab("tiers")}>Тарифы</button>
        <button className={tab === "copy" ? "active" : ""} onClick={() => setTab("copy")}>Копирайт</button>
      </div>

      <div className="admin-body">
        {tab === "ai" && (
          <div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".12em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 8 }}>
              Опишите правку на естественном языке
            </div>
            <textarea
              className="ai-input"
              placeholder='Пример: «Сделай скидку 20% на тариф Plus», «Цена Pro 39», «Переименуй Plus в "Standard"»'
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              onKeyDown={e => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) runAI(); }}
            />
            <div className="ai-row">
              <button className="ai-btn" disabled={busy || !prompt.trim()} onClick={runAI}>
                {busy ? "Применяю…" : "Применить ⌘↵"}
              </button>
            </div>
            <div className="ai-presets">
              {presets.map(p => (
                <button key={p} className="ai-preset" onClick={() => setPrompt(p)}>{p}</button>
              ))}
            </div>

            <div className="ai-log">
              <h5>История правок</h5>
              {result && (
                <div className={"ai-log-item " + (result.ok ? "ok" : "fail")}>
                  {result.msg}
                </div>
              )}
              {(data.ai_log || []).slice(0, 8).map((l, i) => (
                <div key={i} className="ai-log-item ok">
                  {l.msg}
                  <span className="pmt">› {l.prompt}</span>
                </div>
              ))}
              {(!data.ai_log || data.ai_log.length === 0) && !result && (
                <div style={{ fontSize: 11, color: "var(--muted)", fontFamily: "var(--font-mono)", letterSpacing: ".08em" }}>
                  Пока пусто. Введите запрос ↑
                </div>
              )}
            </div>
          </div>
        )}

        {tab === "tiers" && (
          <div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".12em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 10 }}>
              Прямое редактирование
            </div>
            {tiers.map(t => (
              <div key={t.id} className="tier-edit">
                <h4>{t.name} <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--muted)", letterSpacing: ".12em", textTransform: "uppercase", marginLeft: 6 }}>{t.id}</span></h4>
                <div className="field">
                  <label>Имя</label>
                  <input value={t.name} onChange={e => window.updateTier(t.id, { name: e.target.value })} />
                </div>
                <div className="field">
                  <label>Цена $</label>
                  <input type="number" value={t.price} onChange={e => window.updateTier(t.id, { price: parseFloat(e.target.value) || 0 })} />
                </div>
                <div className="field">
                  <label>Период</label>
                  <input value={t.period} onChange={e => window.updateTier(t.id, { period: e.target.value })} />
                </div>
                <div className="field">
                  <label>Описание</label>
                  <textarea rows="2" value={t.desc} onChange={e => window.updateTier(t.id, { desc: e.target.value })} />
                </div>
              </div>
            ))}
          </div>
        )}

        {tab === "copy" && (
          <div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: ".12em", textTransform: "uppercase", color: "var(--muted)", marginBottom: 10 }}>
              Тексты сайта
            </div>
            <div className="tier-edit">
              <div className="field">
                <label>Hero kicker</label>
                <input
                  value={data.copy?.hero_kicker ?? "Том I · Атлас живого тела · 2026"}
                  onChange={e => window.updateCopy("hero_kicker", e.target.value)} />
              </div>
              <div className="field">
                <label>Hero title</label>
                <textarea rows="2"
                  value={data.copy?.hero_title ?? "Где тело дома. Сорок стран под одной шкалой."}
                  onChange={e => window.updateCopy("hero_title", e.target.value)} />
              </div>
              <div className="field">
                <label>Hero lead</label>
                <textarea rows="3"
                  value={data.copy?.hero_lead ?? ""}
                  placeholder="Подзаголовок героя…"
                  onChange={e => window.updateCopy("hero_lead", e.target.value)} />
              </div>
            </div>
            <div className="tier-edit">
              <div className="field">
                <label>Pricing H</label>
                <input
                  value={data.copy?.pricing_h ?? "Подписка"}
                  onChange={e => window.updateCopy("pricing_h", e.target.value)} />
              </div>
              <div className="field">
                <label>Pricing sub</label>
                <input
                  value={data.copy?.pricing_sub ?? "Доступ к информационным пакетам · API · BOI 2.0"}
                  onChange={e => window.updateCopy("pricing_sub", e.target.value)} />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="admin-foot">
        <button onClick={() => setEditMode(!editMode)}>
          {editMode ? "Скрыть рамки" : "Показать рамки"}
        </button>
        <button className="danger" onClick={() => { if (confirm("Сбросить все правки?")) window.resetAdmin(); }}>
          Сбросить
        </button>
      </div>
    </div>
  );
};
