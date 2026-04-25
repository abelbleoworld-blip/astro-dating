/* global React, TIERS */
const { useState: useStateP } = React;

window.PaymentModal = function PaymentModal({ tierId, onClose, onPaid }) {
  const tiers = window.useTiers ? window.useTiers() : window.TIERS;
  const tier = tiers.find(t => t.id === tierId);
  const [method, setMethod] = useStateP("card");
  const [stage, setStage] = useStateP("form"); // form | processing | success
  const [card, setCard] = useStateP({ number: "", exp: "", cvv: "", name: "" });
  const [email, setEmail] = useStateP("");

  if (!tier) return null;

  const submit = () => {
    setStage("processing");
    setTimeout(() => setStage("success"), 1400);
  };

  const methods = [
    { id: "card", n: "Карта МИР / Visa / MC", s: "оплата картой РФ или зарубежной", ico: "MIR" },
    { id: "sbp", n: "СБП", s: "Система быстрых платежей · QR-код", ico: "СБП" },
    { id: "yoo", n: "ЮMoney", s: "электронный кошелёк", ico: "ЮM" },
    { id: "tinkoff", n: "T-Pay", s: "оплата по ссылке", ico: "T" },
  ];

  return (
    <div className="pay-overlay" onClick={onClose}>
      <div className="pay-modal" onClick={e => e.stopPropagation()}>
        {stage === "success" ? (
          <div className="pay-success">
            <div className="ok">✓</div>
            <h3>Оплата прошла</h3>
            <p>Тариф «{tier.name}» активирован. Доступ открыт.<br/>Чек отправлен на {email || "ваш email"}.</p>
            <button className="pay-cta" onClick={onPaid}>Перейти к исследованиям</button>
          </div>
        ) : (
          <>
            <div className="pay-head">
              <div className="kicker">Оформление подписки</div>
              <h3>Тариф «{tier.name}»</h3>
              <div className="price">
                {tier.price.toLocaleString("ru-RU")} ₽
                <small>{tier.period}</small>
              </div>
            </div>
            <div className="pay-body">
              <div className="pay-methods">
                <div className="lbl">Способ оплаты</div>
                {methods.map(m => (
                  <div key={m.id} className={"pay-method" + (method === m.id ? " active" : "")} onClick={() => setMethod(m.id)}>
                    <div className="ico">{m.ico}</div>
                    <div className="nm">{m.n}<small>{m.s}</small></div>
                    <div className="check" />
                  </div>
                ))}
              </div>

              {method === "card" && (
                <>
                  <input className="pay-input" placeholder="Номер карты · 0000 0000 0000 0000"
                    value={card.number} onChange={e => setCard({ ...card, number: e.target.value })} />
                  <div className="pay-card-row">
                    <input className="pay-input" placeholder="ММ / ГГ"
                      value={card.exp} onChange={e => setCard({ ...card, exp: e.target.value })} />
                    <input className="pay-input" placeholder="CVV"
                      value={card.cvv} onChange={e => setCard({ ...card, cvv: e.target.value })} />
                  </div>
                  <input className="pay-input" placeholder="Имя на карте"
                    value={card.name} onChange={e => setCard({ ...card, name: e.target.value })} />
                </>
              )}
              {method !== "card" && (
                <div style={{ padding: 14, border: "1px dashed var(--line)", borderRadius: 3, fontSize: 13, color: "var(--ink-soft)", marginBottom: 8 }}>
                  После нажатия «Оплатить» вы будете перенаправлены в {methods.find(m => m.id === method)?.n} для подтверждения платежа.
                </div>
              )}
              <input className="pay-input" placeholder="Email для чека"
                value={email} onChange={e => setEmail(e.target.value)} />

              <button className="pay-cta" disabled={stage === "processing"} onClick={submit}>
                {stage === "processing" ? "Обработка…" : `Оплатить ${tier.price.toLocaleString("ru-RU")} ₽`}
              </button>

              <div className="pay-foot">
                <span>🔒 Безопасное соединение</span>
                <span>Возврат в течение 14 дней</span>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
