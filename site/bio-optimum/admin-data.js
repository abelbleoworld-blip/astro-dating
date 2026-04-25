/* global React */
const { useState: useStateAdmin, useEffect: useEffectAdmin } = React;

// ---------- Admin store ----------
// Все правки хранятся в localStorage под ключом "bo_admin".
// Структура: { tiers: {plus: {price: 12, perks: [...]}}, copy: {hero_title: "..."}, ai_log: [...] }

const ADMIN_KEY = "bo_admin";

window.getAdminData = function() {
  try {
    const raw = localStorage.getItem(ADMIN_KEY);
    return raw ? JSON.parse(raw) : { tiers: {}, copy: {}, ai_log: [] };
  } catch { return { tiers: {}, copy: {}, ai_log: [] }; }
};
window.saveAdminData = function(data) {
  localStorage.setItem(ADMIN_KEY, JSON.stringify(data));
  window.dispatchEvent(new Event("bo_admin_changed"));
};
window.isAdminMode = function() {
  return localStorage.getItem("bo_admin_mode") === "1";
};
window.setAdminMode = function(v) {
  localStorage.setItem("bo_admin_mode", v ? "1" : "0");
  window.dispatchEvent(new Event("bo_admin_mode_changed"));
};

// Hook: get tier with overrides
window.useTiers = function() {
  const [data, setData] = useStateAdmin(window.getAdminData());
  useEffectAdmin(() => {
    const sync = () => setData(window.getAdminData());
    window.addEventListener("bo_admin_changed", sync);
    return () => window.removeEventListener("bo_admin_changed", sync);
  }, []);
  return window.TIERS.map(t => ({ ...t, ...(data.tiers?.[t.id] || {}) }));
};

// Hook: get copy with override
window.useCopy = function(key, fallback) {
  const [data, setData] = useStateAdmin(window.getAdminData());
  useEffectAdmin(() => {
    const sync = () => setData(window.getAdminData());
    window.addEventListener("bo_admin_changed", sync);
    return () => window.removeEventListener("bo_admin_changed", sync);
  }, []);
  return data.copy?.[key] ?? fallback;
};

window.updateTier = function(tierId, patch) {
  const d = window.getAdminData();
  d.tiers = d.tiers || {};
  d.tiers[tierId] = { ...(d.tiers[tierId] || {}), ...patch };
  window.saveAdminData(d);
};

window.updateCopy = function(key, value) {
  const d = window.getAdminData();
  d.copy = d.copy || {};
  d.copy[key] = value;
  window.saveAdminData(d);
};

window.resetAdmin = function() {
  localStorage.removeItem(ADMIN_KEY);
  window.dispatchEvent(new Event("bo_admin_changed"));
};

// AI patch — имитация AI-правки (на проде здесь fetch("/api/ai-patch"))
window.aiPatch = async function(prompt) {
  // примитивная локальная "ИИ"-логика по ключевым словам
  const p = prompt.toLowerCase();
  const log = (msg) => {
    const d = window.getAdminData();
    d.ai_log = d.ai_log || [];
    d.ai_log.unshift({ t: Date.now(), prompt, msg });
    window.saveAdminData(d);
  };

  // числа
  const numMatch = p.match(/(\d+(?:[.,]\d+)?)/);
  const num = numMatch ? parseFloat(numMatch[1].replace(",", ".")) : null;

  // тариф
  let tier = null;
  if (/plus|плюс/.test(p)) tier = "plus";
  else if (/pro|про/.test(p)) tier = "pro";
  else if (/inst|институт|корпорат|команд/.test(p)) tier = "inst";
  else if (/free|бесплат/.test(p)) tier = "free";

  await new Promise(r => setTimeout(r, 600 + Math.random() * 600));

  // patterns
  if (/(скидк|акци|sale|снизь|снизить|умень)/.test(p) && tier && num) {
    const orig = window.TIERS.find(t => t.id === tier).price;
    const newPrice = Math.max(0, Math.round(orig * (1 - num / 100)));
    window.updateTier(tier, { price: newPrice });
    const msg = `Применена скидка ${num}% к тарифу ${tier}: ${orig}$ → ${newPrice}$`;
    log(msg);
    return { ok: true, msg, changes: [{ kind: "tier", id: tier, field: "price", to: newPrice }] };
  }

  if (/(цен|price|стоим)/.test(p) && tier && num != null) {
    window.updateTier(tier, { price: num });
    const msg = `Цена тарифа ${tier} установлена в ${num}$`;
    log(msg);
    return { ok: true, msg, changes: [{ kind: "tier", id: tier, field: "price", to: num }] };
  }

  if (/(переименуй|rename|назван)/.test(p) && tier) {
    const m = prompt.match(/[«"„]([^»"“]+)[»"“]/);
    if (m) {
      window.updateTier(tier, { name: m[1] });
      const msg = `Тариф ${tier} переименован → "${m[1]}"`;
      log(msg);
      return { ok: true, msg };
    }
  }

  if (/(описан|desc|подзаг)/.test(p) && tier) {
    const m = prompt.match(/[«"„]([^»"“]+)[»"“]/);
    if (m) {
      window.updateTier(tier, { desc: m[1] });
      const msg = `Описание тарифа ${tier} обновлено`;
      log(msg);
      return { ok: true, msg };
    }
  }

  if (/(заголов|hero|hero_title|titl)/.test(p)) {
    const m = prompt.match(/[«"„]([^»"“]+)[»"“]/);
    if (m) {
      window.updateCopy("hero_title", m[1]);
      const msg = `Заголовок героя обновлён → "${m[1]}"`;
      log(msg);
      return { ok: true, msg };
    }
  }

  if (/сброс|reset/.test(p)) {
    window.resetAdmin();
    const msg = "Все правки сброшены";
    log(msg);
    return { ok: true, msg };
  }

  log("Не понял запрос. Попробуйте: «скидка 20% на plus», «цена pro 39», «переименуй plus в \"Standard\"»");
  return { ok: false, msg: "Не понял запрос. Примеры внизу." };
};
